from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from typing import Any

from rbqig.io_utils import write_jsonl


DATASET = "imperial-cpg/rat-bench"
API_URL = "https://datasets-server.huggingface.co/rows"


CODE_MAP = {
    "CIT": ("citizenship_status", "demographic", 3, "citizenship or residency status"),
    "DOB": ("date_of_birth", "date", 5, "date of birth"),
    "MAR": ("marital_status", "demographic", 3, "marital or household status"),
    "SEX": ("sex", "demographic", 2, "sex or gender"),
    "ST": ("state_of_residence", "location", 4, "U.S. state"),
    "AGE": ("age", "age", 3, "age bucket"),
    "NAME": ("name", "person", 5, "person name"),
}


def fetch_rows(config: str, split: str, offset: int, length: int) -> dict[str, Any]:
    params = urllib.parse.urlencode(
        {
            "dataset": DATASET,
            "config": config,
            "split": split,
            "offset": offset,
            "length": length,
        }
    )
    url = f"{API_URL}?{params}"
    with urllib.request.urlopen(url, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))


def find_text_span(text: str, value: str) -> str:
    if not value:
        return ""
    idx = text.lower().find(value.lower())
    if idx < 0:
        return ""
    return text[idx : idx + len(value)]


def generalize_value(code: str, value: str) -> tuple[str, int, float]:
    code = code.upper()
    lower = value.lower()
    if code == "DOB":
        year = ""
        for token in value.replace(",", " ").split():
            if token.isdigit() and len(token) == 4:
                year = token
                break
        if year:
            decade = f"{year[:3]}0s"
            return f"a birth date in the {decade}", 1, 1.0
        return "a date of birth", 1, 1.25
    if code == "ST":
        return "a U.S. state", 1, 1.0
    if code == "CIT":
        if "born" in lower or "citizen" in lower:
            return "a citizenship status", 1, 0.75
        return "a residency or citizenship status", 1, 0.75
    if code == "MAR":
        return "a marital status", 1, 0.75
    if code == "SEX":
        return "a demographic attribute", 1, 1.0
    if code == "AGE":
        return "an age bucket", 1, 0.75
    return "a demographic attribute", 1, 1.0


def make_qi(code: str, value: str, span: str) -> dict[str, Any]:
    attribute, category, privacy_risk, broad_label = CODE_MAP.get(
        code.upper(), (code.lower(), "other", 3, "attribute")
    )
    broad, broad_risk, broad_loss = generalize_value(code, value)
    return {
        "attribute": attribute,
        "category": category,
        "span": span,
        "privacy_risk": privacy_risk,
        "utility_importance": 2,
        "risk_weight": max(1, privacy_risk),
        "why_risky": f"RAT-Bench target {broad_label}",
        "suggested_generalization": broad,
        "coarse_values": [broad],
        "levels": [
            {
                "replacement": broad,
                "privacy_risk_after": broad_risk,
                "utility_loss": broad_loss,
                "kind": "generalize",
            },
            {
                "replacement": f"[{category.upper()}]",
                "privacy_risk_after": 0,
                "utility_loss": 3.0,
                "kind": "redact",
            },
        ],
    }


def direct_identifiers(row: dict[str, Any]) -> list[dict[str, str]]:
    out = []
    direct = row.get("direct_identifiers") or {}
    for key, value in direct.items():
        if value is None:
            continue
        value_s = str(value)
        if value_s:
            out.append({"type": key.upper(), "value": value_s})
            if key.lower() == "name":
                parts = value_s.split()
                for part in parts:
                    if len(part) > 1:
                        out.append({"type": key.upper(), "value": part})
    return out


def scenario_utility(scenario: str) -> tuple[list[str], int, list[dict[str, Any]], str]:
    normalized = scenario.lower()
    if "medical" in normalized:
        return (
            ["doctor", "patient", "check-up", "symptoms", "medical"],
            1,
            [
                {
                    "name": "medical dialogue structure",
                    "acceptable_terms": ["doctor", "patient"],
                },
                {
                    "name": "health discussion",
                    "acceptable_terms": ["check-up", "symptoms", "medical", "health"],
                },
            ],
            "medical_consultation",
        )
    if "chatbot" in normalized:
        return (
            ["chatbot", "person", "help", "recommend", "planning"],
            1,
            [
                {
                    "name": "chatbot dialogue structure",
                    "acceptable_terms": ["chatbot", "person"],
                },
                {
                    "name": "assistance request",
                    "acceptable_terms": ["help", "recommend", "planning", "advice"],
                },
            ],
            "chatbot_assistance",
        )
    if "meeting" in normalized:
        return (
            ["target", "other", "meeting", "call", "records"],
            1,
            [
                {
                    "name": "meeting dialogue structure",
                    "acceptable_terms": ["target", "other"],
                },
                {
                    "name": "administrative discussion",
                    "acceptable_terms": ["meeting", "call", "records", "follow-up"],
                },
            ],
            "meeting_transcript",
        )
    return (
        ["transcript", "conversation"],
        1,
        [
            {
                "name": "conversation structure",
                "acceptable_terms": ["transcript", "conversation"],
            }
        ],
        "conversation",
    )


def convert_row(config: str, row: dict[str, Any], include_unmatched: bool) -> dict[str, Any] | None:
    text = row.get("text") or ""
    qids = []
    attributes = {}
    for code, value in (row.get("indirect_identifiers") or {}).items():
        if value is None:
            continue
        value_s = str(value)
        span = find_text_span(text, value_s)
        if not span and not include_unmatched:
            continue
        qids.append(make_qi(code, value_s, span or value_s))
        attr_name = CODE_MAP.get(code.upper(), (code.lower(),))[0]
        attributes[attr_name] = value_s

    if not qids:
        return None

    scenario = row.get("scenario") or "consultation"
    label_keywords, label_threshold, utility_facts, utility_label = scenario_utility(scenario)
    return {
        "id": f"ratbench_{config}_{row.get('id')}",
        "source": "ratbench",
        "domain": scenario,
        "difficulty": str(row.get("difficulty", "")),
        "original_text": text,
        "quasi_identifiers": qids,
        "label_keywords": label_keywords,
        "label_threshold": label_threshold,
        "utility_facts": utility_facts,
        "ground_truth": {
            "direct_identifiers": direct_identifiers(row),
            "attributes": attributes,
            "utility_label": utility_label,
        },
        "ratbench_meta": {
            "config": config,
            "row_id": row.get("id"),
            "features": row.get("features", []),
            "difficulty": row.get("difficulty"),
        },
    }


def load_records(
    *,
    n: int,
    config: str,
    split: str,
    difficulty: int | None,
    include_unmatched: bool,
    page_size: int,
) -> list[dict[str, Any]]:
    records = []
    offset = 0
    while len(records) < n:
        payload = fetch_rows(config, split, offset, page_size)
        rows = payload.get("rows", [])
        if not rows:
            break
        for item in rows:
            row = item["row"]
            if difficulty is not None and int(row.get("difficulty", -1)) != difficulty:
                continue
            converted = convert_row(config, row, include_unmatched=include_unmatched)
            if converted is None:
                continue
            records.append(converted)
            if len(records) >= n:
                break
        offset += len(rows)
        if offset >= int(payload.get("num_rows_total", offset)):
            break
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Load a RAT-Bench subset through the HF rows API.")
    parser.add_argument("--n", type=int, default=30)
    parser.add_argument("--config", default="english")
    parser.add_argument("--split", default="train")
    parser.add_argument("--difficulty", type=int, default=1)
    parser.add_argument("--include-unmatched", action="store_true")
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--out", default="data/processed/ratbench_english_d1_30.jsonl")
    args = parser.parse_args()

    records = load_records(
        n=args.n,
        config=args.config,
        split=args.split,
        difficulty=args.difficulty,
        include_unmatched=args.include_unmatched,
        page_size=args.page_size,
    )
    write_jsonl(args.out, records)
    print(f"Wrote {len(records)} RAT-Bench records to {args.out}")
    if len(records) < args.n:
        print(f"Warning: requested {args.n} records but only loaded {len(records)}")


if __name__ == "__main__":
    main()
