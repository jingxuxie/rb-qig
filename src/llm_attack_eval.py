from __future__ import annotations

import argparse
import csv
import json
import re
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
from rbqig.io_utils import contains_term, ensure_parent, mean, read_jsonl, simple_tokens, write_jsonl


UNKNOWN_MARKERS = {
    "",
    "unknown",
    "not enough information",
    "not enough info",
    "not specified",
    "cannot determine",
    "unclear",
    "redacted",
    "masked",
}


SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "guesses": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "attribute": {"type": "string"},
                    "guess": {"type": "string"},
                    "confidence": {"type": "number"},
                    "evidence": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": ["attribute", "guess", "confidence", "evidence"],
            },
        }
    },
    "required": ["guesses"],
}


SYSTEM_PROMPT = """You are evaluating a public or synthetic privacy benchmark.
Do not try to identify a real person.
Infer only the requested benchmark attributes from the provided transformed text.
If the text gives only a broad category, report that broad category instead of guessing a specific hidden value.
If an attribute is not inferable, use "unknown".
Keep evidence short and quote only cues present in the text.
"""


def make_payload(record: dict[str, Any], model: str, max_output_tokens: int) -> dict[str, Any]:
    attrs = record.get("ground_truth", {}).get("attributes", {})
    requested = list(attrs.keys())
    prompt = {
        "benchmark_id": record.get("id"),
        "method": record.get("method"),
        "requested_attributes": requested,
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
                "name": "attribute_inference",
                "schema": SCHEMA,
                "strict": True,
            }
        },
        "max_output_tokens": max_output_tokens,
        "store": False,
    }


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


def is_unknown(guess: str) -> bool:
    cleaned = " ".join(simple_tokens(guess))
    if cleaned in UNKNOWN_MARKERS:
        return True
    lower = guess.strip().lower()
    return any(marker == lower for marker in UNKNOWN_MARKERS)


def value_alternatives(value: str) -> list[str]:
    out = [value]
    if "/" in value:
        out.extend(part.strip() for part in value.split("/") if part.strip())
    lower = value.lower()
    if "united states" in lower:
        out.extend(["united states", "us", "u s", "usa", "u s a"])
    if "born in the us" in lower or "born in the united states" in lower:
        out.extend(["born in the us", "born in the united states", "us born", "u s born"])
    return list(dict.fromkeys(out))


def years_in(text: str) -> list[int]:
    return [int(match) for match in re.findall(r"\b(19\d{2}|20\d{2})\b", text)]


def decade_label(year: int) -> str:
    return f"{str(year)[:3]}0s"


def meaningful_tokens(text: str) -> set[str]:
    stop = {"a", "an", "the", "of", "in", "or", "and", "status", "attribute"}
    return {token for token in simple_tokens(text) if len(token) > 2 and token not in stop}


def match_guess(attribute: str, value: str, guess: str) -> str:
    if is_unknown(guess):
        return "unknown"

    for alt in value_alternatives(value):
        if alt and (contains_term(guess, alt) or contains_term(alt, guess)):
            return "exact"

    if attribute == "date_of_birth":
        value_years = years_in(value)
        guess_years = years_in(guess)
        if value_years and guess_years and value_years[0] in guess_years:
            return "coarse"
        if value_years and decade_label(value_years[0]).lower() in guess.lower():
            return "coarse"

    value_tokens = meaningful_tokens(value)
    guess_tokens = meaningful_tokens(guess)
    if value_tokens and guess_tokens and value_tokens.intersection(guess_tokens):
        return "coarse"

    return "wrong"


def risk_weights(record: dict[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}
    for qi in record.get("eval_quasi_identifiers", record.get("quasi_identifiers", [])):
        attr = qi.get("attribute", qi.get("category", ""))
        out[attr] = max(out.get(attr, 0.0), float(qi.get("risk_weight", qi.get("privacy_risk", 1))))
    return out


def evaluate_attack(record: dict[str, Any], parsed: dict[str, Any]) -> dict[str, Any]:
    attrs = record.get("ground_truth", {}).get("attributes", {})
    guesses = {item.get("attribute"): item for item in parsed.get("guesses", [])}
    weights = risk_weights(record)
    exact = 0
    coarse = 0
    total = 0
    weighted = 0.0
    weight_total = 0.0
    compromised = 0
    details = []

    for attr, value in attrs.items():
        item = guesses.get(attr, {})
        guess = str(item.get("guess", "unknown"))
        match = match_guess(attr, str(value), guess)
        weight = weights.get(attr, 1.0)
        total += 1
        weight_total += weight
        if match == "exact":
            exact += 1
            coarse += 1
            weighted += weight
            if weight >= 4:
                compromised = 1
        elif match == "coarse":
            coarse += 1
            weighted += 0.5 * weight
        details.append(
            {
                "attribute": attr,
                "ground_truth": value,
                "guess": guess,
                "match": match,
                "confidence": item.get("confidence", 0.0),
                "evidence": item.get("evidence", [])[:5],
                "risk_weight": weight,
            }
        )

    return {
        "id": record.get("id"),
        "method": record.get("method"),
        "domain": record.get("domain"),
        "record_compromised": compromised,
        "exact_attribute_leakage": exact / max(total, 1),
        "coarse_attribute_leakage": coarse / max(total, 1),
        "risk_weighted_leakage": weighted / max(weight_total, 1.0),
        "details": details,
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
                "record_compromise_rate": round(mean([r["record_compromised"] for r in method_rows]), 4),
                "exact_attribute_leakage": round(mean([r["exact_attribute_leakage"] for r in method_rows]), 4),
                "coarse_attribute_leakage": round(mean([r["coarse_attribute_leakage"] for r in method_rows]), 4),
                "risk_weighted_leakage": round(mean([r["risk_weighted_leakage"] for r in method_rows]), 4),
                "api_calls": sum(0 if r["from_cache"] else 1 for r in usage),
                "estimated_cost_usd": round(sum(float(r["estimated_cost_usd"]) for r in usage), 6),
            }
        )
    return out


def make_usage_row(
    record: dict[str, Any],
    response: dict[str, Any],
    model: str,
    from_cache: bool,
    cache_path: Path,
    parse_status: str,
) -> dict[str, Any]:
    usage = response.get("usage", {}) or {}
    return {
        "id": record.get("id"),
        "method": record.get("method"),
        "from_cache": from_cache,
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "total_tokens": usage.get("total_tokens", 0),
        "estimated_cost_usd": estimate_cost(model, usage),
        "cache_path": str(cache_path),
        "response_status": response.get("status", ""),
        "parse_status": parse_status,
    }


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
        capped = []
        for row in selected:
            method = row.get("method")
            if counts[method] >= args.limit_records_per_method:
                continue
            capped.append(row)
            counts[method] += 1
        selected = capped
    selected = selected[: args.max_calls] if args.max_calls else selected

    cache_dir = Path(args.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    attack_rows = []
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

        parse_status = "ok"
        try:
            parsed = json.loads(response_text(response))
        except json.JSONDecodeError as exc:
            usage_rows.append(
                make_usage_row(
                    record,
                    response,
                    args.model,
                    from_cache,
                    cache_path,
                    f"parse_error:{response.get('status', '')}",
                )
            )
            if args.retry_max_output_tokens <= args.max_output_tokens:
                raise
            retry_payload = make_payload(record, args.model, args.retry_max_output_tokens)
            retry_cache_key = stable_hash(
                {
                    "version": 1,
                    "model": args.model,
                    "record_id": record.get("id"),
                    "method": record.get("method"),
                    "payload": retry_payload,
                }
            )
            retry_cache_path = cache_dir / f"{retry_cache_key}.json"
            if retry_cache_path.exists() and not args.no_cache:
                cached = json.loads(retry_cache_path.read_text(encoding="utf-8"))
                response = cached["response"]
                from_cache = True
            else:
                response = call_responses_api(api_key, retry_payload)
                retry_cache_path.write_text(
                    json.dumps({"payload": retry_payload, "response": response}, indent=2),
                    encoding="utf-8",
                )
                from_cache = False
            cache_path = retry_cache_path
            parse_status = f"retry_ok:{args.retry_max_output_tokens}"
            try:
                parsed = json.loads(response_text(response))
            except json.JSONDecodeError as retry_exc:
                raise RuntimeError(
                    f"Could not parse model response for {record.get('id')} "
                    f"{record.get('method')}; cache={cache_path}"
                ) from retry_exc
        row = evaluate_attack(record, parsed)
        row["raw_guesses"] = parsed
        attack_rows.append(row)

        usage_rows.append(
            make_usage_row(record, response, args.model, from_cache, cache_path, parse_status)
        )
        print(
            f"{idx}/{len(selected)} {record.get('id')} {record.get('method')}: "
            f"risk={row['risk_weighted_leakage']:.3f}, cache={from_cache}"
        )

    return attack_rows, usage_rows, aggregate(attack_rows, usage_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run cached LLM attacker evaluation.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--attacks-out", required=True)
    parser.add_argument("--usage-out", required=True)
    parser.add_argument("--metrics-out", required=True)
    parser.add_argument("--cache-dir", default="results/api_cache/llm_attacker")
    parser.add_argument("--api-key-path", default=DEFAULT_API_KEY_PATH)
    parser.add_argument("--model", default="gpt-5.4-nano")
    parser.add_argument("--methods", nargs="+", default=["direct", "blanket_qi", "rbqig_b4"])
    parser.add_argument("--ids", nargs="*", default=[])
    parser.add_argument("--limit-records-per-method", type=int, default=0)
    parser.add_argument("--max-calls", type=int, default=0)
    parser.add_argument("--max-output-tokens", type=int, default=900)
    parser.add_argument("--retry-max-output-tokens", type=int, default=0)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()

    attack_rows, usage_rows, metrics = run(args)
    write_jsonl(args.attacks_out, attack_rows)
    write_jsonl(args.usage_out, usage_rows)
    write_csv(args.metrics_out, metrics)
    print(f"Wrote LLM attacker metrics to {args.metrics_out}")
    print(f"Estimated API cost: ${sum(float(r['estimated_cost_usd']) for r in usage_rows):.6f}")


if __name__ == "__main__":
    main()
