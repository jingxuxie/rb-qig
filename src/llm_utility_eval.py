from __future__ import annotations

import argparse
import csv
import json
import time
from collections import defaultdict
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
from rbqig.io_utils import ensure_parent, mean, read_jsonl, write_jsonl


SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "label_preserved": {"type": "boolean"},
        "fact_preservation_score": {"type": "number"},
        "semantic_utility_score": {"type": "integer"},
        "key_information_lost": {
            "type": "array",
            "items": {"type": "string"},
        },
        "rationale": {"type": "string"},
    },
    "required": [
        "label_preserved",
        "fact_preservation_score",
        "semantic_utility_score",
        "key_information_lost",
        "rationale",
    ],
}


SYSTEM_PROMPT = """You are evaluating utility preservation for a public or synthetic anonymization benchmark.
Do not identify, investigate, or profile any real person.
Compare the original text to the transformed text only for downstream task utility.
Do not reward preservation of names, emails, phone numbers, addresses, account IDs, or other direct identifiers.
Generalized descriptions count as useful if they preserve the task-relevant meaning needed for the stated utility label.
Redaction placeholders count as missing unless surrounding context still makes the task-relevant meaning clear.

Return:
- label_preserved: whether the transformed text still supports the same utility label.
- fact_preservation_score: 0.0 to 1.0, the fraction of listed utility facts preserved semantically.
- semantic_utility_score: integer 0 to 5, where 0 is unusable, 3 is partially usable, and 5 preserves nearly all task-relevant meaning.
- key_information_lost: short descriptions of important task-relevant information lost.
- rationale: one concise sentence.
"""


def write_csv(path: str | Path, rows: list[dict[str, Any]]) -> None:
    ensure_parent(path)
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def make_payload(record: dict[str, Any], model: str, max_output_tokens: int) -> dict[str, Any]:
    prompt = {
        "benchmark_id": record.get("id"),
        "method": record.get("method"),
        "domain": record.get("domain"),
        "utility_label": record.get("ground_truth", {}).get("utility_label", ""),
        "utility_facts": record.get("utility_facts", []),
        "original_text": record.get("original_text", ""),
        "transformed_text": record.get("transformed_text", ""),
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
                "name": "utility_preservation",
                "schema": SCHEMA,
                "strict": True,
            }
        },
        "max_output_tokens": max_output_tokens,
        "store": False,
    }


def evaluate_utility(record: dict[str, Any], parsed: dict[str, Any]) -> dict[str, Any]:
    semantic_score = int(clamp(float(parsed.get("semantic_utility_score", 0)), 0, 5))
    fact_score = clamp(float(parsed.get("fact_preservation_score", 0.0)), 0.0, 1.0)
    label_preserved = bool(parsed.get("label_preserved", False))
    return {
        "id": record.get("id"),
        "method": record.get("method"),
        "domain": record.get("domain"),
        "label_preservation": 1.0 if label_preserved else 0.0,
        "llm_fact_preservation": round(fact_score, 6),
        "semantic_utility_score": round(semantic_score / 5.0, 6),
        "semantic_utility_score_0_to_5": semantic_score,
        "key_information_lost": parsed.get("key_information_lost", [])[:8],
        "rationale": str(parsed.get("rationale", ""))[:500],
        "raw_utility_judgment": parsed,
    }


def aggregate(rows: list[dict[str, Any]], usage_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_method: dict[str, list[dict[str, Any]]] = defaultdict(list)
    usage_by_method: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_method[row["method"]].append(row)
    for row in usage_rows:
        usage_by_method[row["method"]].append(row)

    order = {
        "none": 0,
        "direct": 1,
        "blanket_qi": 2,
        "rbqig_b2": 3,
        "rbqig_b4": 4,
        "rbqig_b4_no_combo": 5,
        "rbqig_b4_placeholder": 6,
        "rbqig_b6": 7,
    }
    out = []
    for method, method_rows in sorted(by_method.items(), key=lambda item: order.get(item[0], 99)):
        usage = usage_by_method.get(method, [])
        out.append(
            {
                "method": method,
                "n_records": len(method_rows),
                "label_preservation": round(mean([r["label_preservation"] for r in method_rows]), 4),
                "llm_fact_preservation": round(mean([r["llm_fact_preservation"] for r in method_rows]), 4),
                "semantic_utility_score": round(mean([r["semantic_utility_score"] for r in method_rows]), 4),
                "semantic_utility_score_0_to_5": round(mean([r["semantic_utility_score_0_to_5"] for r in method_rows]), 3),
                "api_calls": sum(0 if r["from_cache"] else 1 for r in usage),
                "estimated_cost_usd": round(sum(float(r["estimated_cost_usd"]) for r in usage), 6),
            }
        )
    return out


def run(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    api_key = read_api_key(args.api_key_path)
    all_records = read_jsonl(args.input)
    methods = set(args.methods)
    selected = [row for row in all_records if row.get("method") in methods]
    if args.ids:
        allowed_ids = set(args.ids)
        selected = [row for row in selected if row.get("id") in allowed_ids]
    if args.limit_records_per_method:
        counts: dict[str, int] = defaultdict(int)
        limited = []
        for row in selected:
            method = row.get("method", "")
            if counts[method] >= args.limit_records_per_method:
                continue
            counts[method] += 1
            limited.append(row)
        selected = limited
    selected = selected[: args.max_calls] if args.max_calls else selected

    cache_dir = Path(args.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    utility_rows = []
    usage_rows = []

    for idx, record in enumerate(selected, start=1):
        payload = make_payload(record, args.model, args.max_output_tokens)
        cache_key = stable_hash(
            {
                "version": 1,
                "model": args.model,
                "record_id": record.get("id"),
                "method": record.get("method"),
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
        row = evaluate_utility(record, parsed)
        utility_rows.append(row)

        usage = response.get("usage", {}) or {}
        usage_row = {
            "id": record.get("id"),
            "method": record.get("method"),
            "from_cache": from_cache,
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "estimated_cost_usd": estimate_cost(args.model, usage),
            "cache_path": str(cache_path),
        }
        usage_rows.append(usage_row)
        print(
            f"{idx}/{len(selected)} {record.get('id')} {record.get('method')}: "
            f"utility={row['semantic_utility_score_0_to_5']}/5, "
            f"facts={row['llm_fact_preservation']:.2f}, cache={from_cache}"
        )

    return utility_rows, usage_rows, aggregate(utility_rows, usage_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run cached LLM utility preservation evaluation.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--utility-out", required=True)
    parser.add_argument("--usage-out", required=True)
    parser.add_argument("--metrics-out", required=True)
    parser.add_argument("--cache-dir", default="results/api_cache/llm_utility")
    parser.add_argument("--api-key-path", default=DEFAULT_API_KEY_PATH)
    parser.add_argument("--model", default="gpt-5.4-nano")
    parser.add_argument("--methods", nargs="+", default=["direct", "blanket_qi", "rbqig_b4"])
    parser.add_argument("--ids", nargs="*", default=[])
    parser.add_argument("--limit-records-per-method", type=int, default=0)
    parser.add_argument("--max-calls", type=int, default=0)
    parser.add_argument("--max-output-tokens", type=int, default=700)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()

    utility_rows, usage_rows, metrics = run(args)
    write_jsonl(args.utility_out, utility_rows)
    write_jsonl(args.usage_out, usage_rows)
    write_csv(args.metrics_out, metrics)
    print(f"Wrote LLM utility metrics to {args.metrics_out}")
    print(f"Estimated API cost: ${sum(float(r['estimated_cost_usd']) for r in usage_rows):.6f}")


if __name__ == "__main__":
    main()
