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
        "task_label_preserved": {"type": "boolean"},
        "task_content_score": {"type": "number"},
        "privacy_aware_utility_score": {"type": "integer"},
        "penalized_private_information_loss": {"type": "boolean"},
        "key_task_information_lost": {
            "type": "array",
            "items": {"type": "string"},
        },
        "rationale": {"type": "string"},
    },
    "required": [
        "task_label_preserved",
        "task_content_score",
        "privacy_aware_utility_score",
        "penalized_private_information_loss",
        "key_task_information_lost",
        "rationale",
    ],
}


SYSTEM_PROMPT = """You are evaluating privacy-aware utility for a public or synthetic anonymization benchmark.
Do not identify, investigate, or profile any real person.
Compare the original text to the transformed text only for the downstream task brief.

Important scoring rule:
- Do not penalize removal or generalization of direct identifiers or protected benchmark attributes listed in the input.
- Protected details include names, addresses, emails, phone numbers, exact dates of birth, exact locations, exact demographic values, case IDs, account numbers, and other benchmark quasi-identifiers.
- Reward broad non-identifying categories only when they preserve task-relevant meaning, such as age band for age-sensitive medical advice, employment category for work-status discussion, or legal role for case summarization.
- Bare placeholders count as weaker than meaningful categories only when the downstream task needs that category.
- Do not reward exact private values merely because they remain visible.

Return:
- task_label_preserved: whether the transformed text still supports the same downstream task type.
- task_content_score: 0.0 to 1.0 for non-private task content preserved.
- privacy_aware_utility_score: integer 0 to 5, where 0 is unusable and 5 preserves nearly all non-private task utility.
- penalized_private_information_loss: true only if your score still penalized the absence of protected private values.
- key_task_information_lost: short descriptions of non-private task information lost.
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


def task_brief(record: dict[str, Any]) -> str:
    label = str(record.get("ground_truth", {}).get("utility_label", ""))
    domain = str(record.get("domain", "")).lower()
    if label == "medical_consultation" or "medical" in domain:
        return (
            "Preserve the ability to summarize the medical consultation: symptoms, "
            "health concerns, clinician questions, advice, follow-up, and non-identifying "
            "clinical context. Exact personal identifiers and benchmark demographic values "
            "are protected and should not be required."
        )
    if label == "chatbot_assistance" or "chatbot" in domain:
        return (
            "Preserve the ability to summarize the assistance request and advice: user goals, "
            "recommendations, constraints, planning steps, and non-identifying eligibility "
            "context. Exact personal identifiers and benchmark demographic values are protected."
        )
    if label == "meeting_transcript" or "meeting" in domain:
        return (
            "Preserve the ability to summarize the administrative meeting: purpose, records "
            "being discussed, role or work context when non-identifying, action items, and "
            "follow-up. Exact contact, address, demographic, and identity details are protected."
        )
    if label == "legal_case_summary" or "legal" in domain:
        return (
            "Preserve the ability to write a neutral legal case summary: procedure, legal issue, "
            "chronology at a non-identifying granularity, parties' roles, and outcome or remedy. "
            "Exact case identifiers, names, dates, locations, and private party attributes are protected."
        )
    return (
        "Preserve the non-private task content and dialogue structure while ignoring direct "
        "identifiers and protected benchmark attributes."
    )


def protected_values(record: dict[str, Any]) -> list[dict[str, str]]:
    out = []
    for identifier in record.get("ground_truth", {}).get("direct_identifiers", []):
        value = str(identifier.get("value", "")).strip()
        if value:
            out.append({"type": str(identifier.get("type", "direct_identifier")), "value": value})
    for attribute, value in record.get("ground_truth", {}).get("attributes", {}).items():
        value_s = str(value).strip()
        if value_s:
            out.append({"type": str(attribute), "value": value_s})
    return out[:80]


def make_payload(record: dict[str, Any], model: str, max_output_tokens: int) -> dict[str, Any]:
    prompt = {
        "benchmark_id": record.get("id"),
        "method": record.get("method"),
        "domain": record.get("domain"),
        "utility_label": record.get("ground_truth", {}).get("utility_label", ""),
        "task_brief": task_brief(record),
        "protected_values_to_ignore_for_utility": protected_values(record),
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
                "name": "privacy_aware_utility",
                "schema": SCHEMA,
                "strict": True,
            }
        },
        "max_output_tokens": max_output_tokens,
        "store": False,
    }


def evaluate_utility(record: dict[str, Any], parsed: dict[str, Any]) -> dict[str, Any]:
    utility_score = int(clamp(float(parsed.get("privacy_aware_utility_score", 0)), 0, 5))
    content_score = clamp(float(parsed.get("task_content_score", 0.0)), 0.0, 1.0)
    label_preserved = bool(parsed.get("task_label_preserved", False))
    private_penalty = bool(parsed.get("penalized_private_information_loss", False))
    return {
        "id": record.get("id"),
        "method": record.get("method"),
        "domain": record.get("domain"),
        "privacy_aware_label_preservation": 1.0 if label_preserved else 0.0,
        "task_content_preservation": round(content_score, 6),
        "privacy_aware_utility": round(utility_score / 5.0, 6),
        "privacy_aware_utility_0_to_5": utility_score,
        "private_loss_penalty": 1.0 if private_penalty else 0.0,
        "key_task_information_lost": parsed.get("key_task_information_lost", [])[:8],
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
        "llm_direct": 2,
        "blanket_qi": 3,
        "rbqig_b2": 4,
        "rbqig_b4": 5,
        "rbqig_b4_no_combo": 6,
        "rbqig_b4_placeholder": 7,
        "rbqig_b6": 8,
    }
    out = []
    for method, method_rows in sorted(by_method.items(), key=lambda item: order.get(item[0], 99)):
        usage = usage_by_method.get(method, [])
        out.append(
            {
                "method": method,
                "n_records": len(method_rows),
                "privacy_aware_label_preservation": round(mean([r["privacy_aware_label_preservation"] for r in method_rows]), 4),
                "task_content_preservation": round(mean([r["task_content_preservation"] for r in method_rows]), 4),
                "privacy_aware_utility": round(mean([r["privacy_aware_utility"] for r in method_rows]), 4),
                "privacy_aware_utility_0_to_5": round(mean([r["privacy_aware_utility_0_to_5"] for r in method_rows]), 3),
                "private_loss_penalty_rate": round(mean([r["private_loss_penalty"] for r in method_rows]), 4),
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
            f"privacy_aware_utility={row['privacy_aware_utility_0_to_5']}/5, "
            f"content={row['task_content_preservation']:.2f}, cache={from_cache}"
        )

    return utility_rows, usage_rows, aggregate(utility_rows, usage_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run cached privacy-aware LLM utility evaluation.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--utility-out", required=True)
    parser.add_argument("--usage-out", required=True)
    parser.add_argument("--metrics-out", required=True)
    parser.add_argument("--cache-dir", default="results/api_cache/llm_privacy_aware_utility")
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
    print(f"Wrote privacy-aware utility metrics to {args.metrics_out}")
    print(f"Estimated API cost: ${sum(float(r['estimated_cost_usd']) for r in usage_rows):.6f}")


if __name__ == "__main__":
    main()
