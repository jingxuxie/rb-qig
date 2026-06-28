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
        "legal_summary_preserved": {"type": "boolean"},
        "procedure_score": {"type": "integer"},
        "legal_issue_score": {"type": "integer"},
        "timeline_score": {"type": "integer"},
        "outcome_or_remedy_score": {"type": "integer"},
        "specificity_score": {"type": "integer"},
        "overall_utility_score": {"type": "integer"},
        "key_information_lost": {
            "type": "array",
            "items": {"type": "string"},
        },
        "rationale": {"type": "string"},
    },
    "required": [
        "legal_summary_preserved",
        "procedure_score",
        "legal_issue_score",
        "timeline_score",
        "outcome_or_remedy_score",
        "specificity_score",
        "overall_utility_score",
        "key_information_lost",
        "rationale",
    ],
}


SYSTEM_PROMPT = """You are evaluating anonymized public legal benchmark text for downstream legal-case summarization utility.
Do not identify, investigate, or profile any real person.
Use only the original and transformed text supplied in the prompt.
Do not reward preservation of direct identifiers such as names, case numbers, phone numbers, addresses, or exact IDs.

Score whether the transformed text still supports a useful neutral legal case summary:
- procedure_score: case origin, court/application posture, admissibility or notice/procedure context.
- legal_issue_score: complaint, charge, alleged violation, legal issue, or dispute type.
- timeline_score: legally relevant sequence and temporal granularity, without rewarding exact dates as identifiers.
- outcome_or_remedy_score: judgment, sentence, release, payment, compensation, or procedural outcome/remedy.
- specificity_score: useful non-direct legal detail retained through categories or generalizations, where bare placeholders are less useful than typed generalizations.
- overall_utility_score: overall usefulness for a privacy-preserving legal case summary.

Each score is an integer from 0 to 5. A score of 5 means nearly all task-relevant meaning is preserved; 3 means partially useful; 0 means unusable.
Generalizations count as useful when they preserve legal meaning. Bare placeholders count as low-specificity unless surrounding text still makes the legal meaning clear.
Return concise JSON only.
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


def clamp_score(value: Any) -> int:
    try:
        numeric = int(round(float(value)))
    except (TypeError, ValueError):
        numeric = 0
    return max(0, min(5, numeric))


def make_payload(record: dict[str, Any], model: str, max_output_tokens: int) -> dict[str, Any]:
    prompt = {
        "benchmark_id": record.get("id"),
        "method": record.get("method"),
        "domain": record.get("domain"),
        "task": "privacy-preserving legal case summary",
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
                "name": "legal_utility_preservation",
                "schema": SCHEMA,
                "strict": True,
            }
        },
        "max_output_tokens": max_output_tokens,
        "store": False,
    }


def score_record(record: dict[str, Any], parsed: dict[str, Any]) -> dict[str, Any]:
    scores = {
        "procedure_preservation": clamp_score(parsed.get("procedure_score")) / 5.0,
        "legal_issue_preservation": clamp_score(parsed.get("legal_issue_score")) / 5.0,
        "timeline_preservation": clamp_score(parsed.get("timeline_score")) / 5.0,
        "outcome_or_remedy_preservation": clamp_score(parsed.get("outcome_or_remedy_score")) / 5.0,
        "legal_specificity": clamp_score(parsed.get("specificity_score")) / 5.0,
        "legal_task_utility": clamp_score(parsed.get("overall_utility_score")) / 5.0,
    }
    return {
        "id": record.get("id"),
        "method": record.get("method"),
        "domain": record.get("domain"),
        "legal_summary_preservation": 1.0 if parsed.get("legal_summary_preserved") else 0.0,
        **{key: round(value, 6) for key, value in scores.items()},
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

    order = {"direct": 1, "blanket_qi": 2, "rbqig_b4": 3, "rbqig_b6": 4}
    metrics = [
        "legal_summary_preservation",
        "procedure_preservation",
        "legal_issue_preservation",
        "timeline_preservation",
        "outcome_or_remedy_preservation",
        "legal_specificity",
        "legal_task_utility",
    ]
    out = []
    for method, method_rows in sorted(by_method.items(), key=lambda item: order.get(item[0], 99)):
        usage = usage_by_method.get(method, [])
        row: dict[str, Any] = {"method": method, "n_records": len(method_rows)}
        for metric in metrics:
            row[metric] = round(mean([float(item[metric]) for item in method_rows]), 4)
        row["api_calls"] = sum(0 if item["from_cache"] else 1 for item in usage)
        row["estimated_cost_usd"] = round(sum(float(item["estimated_cost_usd"]) for item in usage), 6)
        out.append(row)
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
    if args.max_calls:
        selected = selected[: args.max_calls]

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
        row = score_record(record, parsed)
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
            f"legal={row['legal_task_utility']:.2f}, "
            f"specificity={row['legal_specificity']:.2f}, cache={from_cache}"
        )

    return utility_rows, usage_rows, aggregate(utility_rows, usage_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run cached TAB legal-task LLM utility evaluation.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--utility-out", required=True)
    parser.add_argument("--usage-out", required=True)
    parser.add_argument("--metrics-out", required=True)
    parser.add_argument("--cache-dir", default="results/api_cache/llm_legal_utility")
    parser.add_argument("--api-key-path", default=DEFAULT_API_KEY_PATH)
    parser.add_argument("--model", default="gpt-5.4-nano")
    parser.add_argument("--methods", nargs="+", default=["direct", "blanket_qi", "rbqig_b4"])
    parser.add_argument("--ids", nargs="*", default=[])
    parser.add_argument("--limit-records-per-method", type=int, default=0)
    parser.add_argument("--max-calls", type=int, default=0)
    parser.add_argument("--max-output-tokens", type=int, default=800)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()

    utility_rows, usage_rows, metrics = run(args)
    write_jsonl(args.utility_out, utility_rows)
    write_jsonl(args.usage_out, usage_rows)
    write_csv(args.metrics_out, metrics)
    print(f"Wrote legal utility metrics to {args.metrics_out}")
    print(f"Estimated API cost: ${sum(float(row['estimated_cost_usd']) for row in usage_rows):.6f}")


if __name__ == "__main__":
    main()
