from __future__ import annotations

import argparse
import json
import time
from copy import deepcopy
from pathlib import Path
from typing import Any

from api_qi_extractor import (
    DEFAULT_API_KEY_PATH,
    call_responses_api,
    estimate_cost,
    read_api_key,
    response_text,
    stable_hash,
)
from rbqig.io_utils import read_jsonl, write_jsonl
from rbqig.redaction import replace_direct_identifiers


SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "redacted_text": {"type": "string"},
    },
    "required": ["redacted_text"],
}


SYSTEM_PROMPT = """You are a conservative text de-identification assistant for a public benchmark.
Remove personally identifying information from the text.
Preserve non-identifying meaning, document structure, and already-redacted placeholders such as [PERSON].
Do not add facts, infer facts, summarize, or explain.
If a detail could identify a person because it is unusually specific, replace it with a broader phrase.
Return only the requested JSON object.
"""


def make_payload(record: dict[str, Any], model: str, max_output_tokens: int) -> dict[str, Any]:
    prompt = {
        "benchmark_id": record.get("id"),
        "source_method": record.get("method"),
        "text": record.get("transformed_text", ""),
    }
    return {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": [{"type": "input_text", "text": SYSTEM_PROMPT}],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": json.dumps(prompt, ensure_ascii=False)}],
            },
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "llm_direct_redaction",
                "schema": SCHEMA,
                "strict": True,
            }
        },
        "max_output_tokens": max_output_tokens,
        "store": False,
    }


def make_output_record(record: dict[str, Any], output_method: str, redacted_text: str) -> dict[str, Any]:
    out = deepcopy(record)
    out["method"] = output_method
    direct_ids = out.get("ground_truth", {}).get("direct_identifiers", [])
    cleaned, direct_changes = replace_direct_identifiers(redacted_text, direct_ids)
    out["transformed_text"] = cleaned
    out["change_log"] = list(out.get("change_log", [])) + [
        {
            "kind": "llm_direct_sanitizer",
            "source_method": record.get("method"),
        }
    ] + direct_changes
    return out


def run(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    api_key = read_api_key(args.api_key_path)
    records = read_jsonl(args.input)
    base_records = [row for row in records if row.get("method") == args.source_method]
    base_records = base_records[: args.max_calls] if args.max_calls else base_records

    cache_dir = Path(args.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    generated = []
    usage_rows = []
    for idx, record in enumerate(base_records, start=1):
        payload = make_payload(record, args.model, args.max_output_tokens)
        cache_key = stable_hash(
            {
                "version": 1,
                "model": args.model,
                "record_id": record.get("id"),
                "source_method": args.source_method,
                "output_method": args.output_method,
                "source_text": record.get("transformed_text", ""),
                "payload": payload,
            }
        )
        cache_path = cache_dir / f"{cache_key}.json"
        if cache_path.exists() and not args.no_cache:
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            response = cached["response"]
            from_cache = True
        else:
            if args.sleep_seconds and idx > 1:
                time.sleep(args.sleep_seconds)
            response = call_responses_api(api_key, payload)
            cache_path.write_text(
                json.dumps({"payload": payload, "response": response}, indent=2),
                encoding="utf-8",
            )
            from_cache = False

        parsed = json.loads(response_text(response))
        redacted_text = str(parsed.get("redacted_text", "")).strip()
        if not redacted_text:
            raise RuntimeError(f"Empty LLM redaction for {record.get('id')}")
        generated.append(make_output_record(record, args.output_method, redacted_text))

        usage = response.get("usage", {}) or {}
        usage_row = {
            "id": record.get("id"),
            "method": args.output_method,
            "source_method": args.source_method,
            "from_cache": from_cache,
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "estimated_cost_usd": estimate_cost(args.model, usage),
            "cache_path": str(cache_path),
        }
        usage_rows.append(usage_row)
        print(
            f"{idx}/{len(base_records)} {record.get('id')} {args.output_method}: "
            f"cache={from_cache}, tokens={usage_row['total_tokens']}"
        )

    if args.merge:
        kept = [row for row in records if row.get("method") != args.output_method]
        outputs = kept + generated
    else:
        outputs = generated
    return outputs, usage_rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a cached naive LLM direct-redaction baseline.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--usage-out", required=True)
    parser.add_argument("--cache-dir", default="results/api_cache/llm_direct_redact")
    parser.add_argument("--api-key-path", default=DEFAULT_API_KEY_PATH)
    parser.add_argument("--model", default="gpt-5.4-nano")
    parser.add_argument("--source-method", default="direct")
    parser.add_argument("--output-method", default="llm_direct")
    parser.add_argument("--max-calls", type=int, default=0)
    parser.add_argument("--max-output-tokens", type=int, default=1800)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--merge", action="store_true", help="Append generated rows to input rows.")
    args = parser.parse_args()

    outputs, usage_rows = run(args)
    write_jsonl(args.out, outputs)
    write_jsonl(args.usage_out, usage_rows)
    print(f"Wrote {len(outputs)} rows to {args.out}")
    print(f"Estimated API cost: ${sum(float(r['estimated_cost_usd']) for r in usage_rows):.6f}")


if __name__ == "__main__":
    main()
