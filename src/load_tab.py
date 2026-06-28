from __future__ import annotations

import argparse
import json
import re
import urllib.request
from typing import Any

from rbqig.io_utils import write_jsonl


RAW_BASE = "https://raw.githubusercontent.com/NorskRegnesentral/text-anonymization-benchmark/master"
DEFAULT_FILES = {
    "train": f"{RAW_BASE}/echr_train.json",
    "dev": f"{RAW_BASE}/echr_dev.json",
    "test": f"{RAW_BASE}/echr_test.json",
}


CATEGORY_MAP = {
    "CODE": "legal",
    "DATETIME": "date",
    "DEM": "demographic",
    "LOC": "location",
    "ORG": "organization",
    "PERSON": "person",
    "QUANTITY": "quantity",
}


def fetch_json(url: str) -> list[dict[str, Any]]:
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def _first_annotator(doc: dict[str, Any]) -> dict[str, Any]:
    annotations = doc.get("annotations") or {}
    if not annotations:
        return {"entity_mentions": []}
    name = sorted(annotations)[0]
    return annotations[name]


def _merge_mentions(doc: dict[str, Any]) -> list[dict[str, Any]]:
    seen: set[tuple[int, int, str, str]] = set()
    merged = []
    for annotation in (doc.get("annotations") or {}).values():
        for mention in annotation.get("entity_mentions", []):
            key = (
                int(mention.get("start_offset", -1)),
                int(mention.get("end_offset", -1)),
                str(mention.get("span_text", "")),
                str(mention.get("identifier_type", "")),
            )
            if key in seen:
                continue
            seen.add(key)
            merged.append(mention)
    return sorted(merged, key=lambda item: (item.get("start_offset", 0), item.get("end_offset", 0)))


def mentions_for_doc(doc: dict[str, Any], annotator_mode: str) -> list[dict[str, Any]]:
    if annotator_mode == "merge":
        return _merge_mentions(doc)
    return _first_annotator(doc).get("entity_mentions", [])


def category_for(entity_type: str) -> str:
    return CATEGORY_MAP.get(entity_type.upper(), "other")


def risk_for(entity_type: str, span: str, confidential_status: str) -> int:
    entity_type = entity_type.upper()
    if entity_type == "DATETIME":
        risk = 4 if re.search(r"\b\d{1,2}\s+[A-Za-z]+\s+\d{4}\b", span) else 3
    elif entity_type == "PERSON":
        risk = 4
    elif entity_type in {"ORG", "CODE"}:
        risk = 4
    elif entity_type in {"LOC", "DEM", "QUANTITY"}:
        risk = 3
    else:
        risk = 3
    if confidential_status and confidential_status != "NOT_CONFIDENTIAL":
        risk += 1
    return max(1, min(5, risk))


def generic_generalization_for(entity_type: str, span: str) -> tuple[str, int, float]:
    entity_type = entity_type.upper()
    if entity_type == "DATETIME":
        years = re.findall(r"\b(1[0-9]{3}|20[0-9]{2})\b", span)
        if years:
            decade = f"{years[-1][:3]}0s"
            return f"a date in the {decade}", 1, 1.0
        return "a date", 1, 1.0
    if entity_type == "PERSON":
        return "a legal participant", 1, 1.5
    if entity_type == "ORG":
        return "an organization or institution", 1, 1.25
    if entity_type == "LOC":
        return "a location", 1, 1.0
    if entity_type == "DEM":
        return "a demographic attribute", 1, 1.0
    if entity_type == "CODE":
        return "a case reference", 1, 1.0
    if entity_type == "QUANTITY":
        return "a case-related quantity", 1, 1.0
    return "a case-related detail", 1, 1.0


def legal_role_generalization_for(entity_type: str, span: str) -> tuple[str, int, float]:
    entity_type = entity_type.upper()
    lowered = span.lower()
    if entity_type == "DATETIME":
        has_year = re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b", span)
        if re.search(r"\b(year|years|month|months|day|days)\b", lowered) and not has_year:
            return "a case duration", 1, 0.75
        return generic_generalization_for(entity_type, span)
    if entity_type == "ORG":
        if "court of cassation" in lowered:
            return "a high appellate court", 1, 0.75
        if "court" in lowered or "tribunal" in lowered:
            return "a domestic court", 1, 0.75
        if "prosecutor" in lowered:
            return "a prosecutor's office", 1, 0.75
        if "security directorate" in lowered or "police" in lowered:
            return "a law-enforcement authority", 1, 0.75
        if "prison" in lowered or "detention" in lowered:
            return "a detention facility", 1, 0.75
        if "ministry" in lowered or "government" in lowered:
            return "a government authority", 1, 0.75
        if "bank" in lowered:
            return "a financial institution", 1, 0.75
        return "a legal institution", 1, 0.9
    if entity_type == "QUANTITY":
        if re.search(r"\b(imprisonment|prison|sentence|sentenced|penalty|years?|months?)\b", lowered):
            return "a custodial sentence", 1, 0.75
        if re.search(r"\b(usd|trl|euro|lira|liras|dollar|dollars|compensation|damage|pecuniary)\b", lowered):
            return "a compensation amount", 1, 0.75
        if re.search(r"\b(defendant|defendants|accused|applicant|applicants|person|persons|employee|employees)\b", lowered):
            return "multiple case participants", 1, 0.75
        return "a legally relevant quantity", 1, 0.9
    if entity_type == "LOC":
        return "a domestic location", 1, 0.75
    if entity_type == "DEM":
        return "a party status attribute", 1, 0.75
    if entity_type == "CODE":
        return "a case reference", 1, 0.75
    if entity_type == "PERSON":
        return "a legal participant", 1, 1.25
    if "accident" in lowered or "shock" in lowered:
        return "a case incident detail", 1, 0.75
    if "farm" in lowered or "property" in lowered:
        return "case property", 1, 0.75
    return "a legally relevant detail", 1, 0.9


def generalization_for(entity_type: str, span: str, mode: str) -> tuple[str, int, float]:
    if mode == "legal_role":
        return legal_role_generalization_for(entity_type, span)
    return generic_generalization_for(entity_type, span)


def make_qi(mention: dict[str, Any], idx: int, generalization_mode: str) -> dict[str, Any]:
    entity_type = str(mention.get("entity_type", "OTHER"))
    span = str(mention.get("span_text", ""))
    category = category_for(entity_type)
    risk = risk_for(entity_type, span, str(mention.get("confidential_status", "")))
    broad, broad_risk, utility_loss = generalization_for(entity_type, span, generalization_mode)
    attr = f"tab_{category}_{idx:03d}"
    return {
        "attribute": attr,
        "category": category,
        "span": span,
        "privacy_risk": risk,
        "utility_importance": 3 if category in {"date", "organization", "quantity", "legal"} else 2,
        "risk_weight": risk,
        "why_risky": f"TAB {entity_type} {mention.get('identifier_type', '')}".strip(),
        "suggested_generalization": broad,
        "coarse_values": [broad],
        "levels": [
            {
                "replacement": broad,
                "privacy_risk_after": broad_risk,
                "utility_loss": utility_loss,
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


def direct_identifier(mention: dict[str, Any]) -> dict[str, str]:
    entity_type = str(mention.get("entity_type", "OTHER")).upper()
    span = str(mention.get("span_text", ""))
    return {"type": entity_type, "value": span}


def convert_doc(
    doc: dict[str, Any],
    mentions: list[dict[str, Any]],
    generalization_mode: str,
) -> dict[str, Any] | None:
    qids = []
    direct_ids = []
    attributes = {}
    for mention in mentions:
        identifier_type = str(mention.get("identifier_type", "")).upper()
        span = str(mention.get("span_text", ""))
        if not span:
            continue
        if identifier_type == "DIRECT":
            direct_ids.append(direct_identifier(mention))
        elif identifier_type == "QUASI":
            qi = make_qi(mention, len(qids) + 1, generalization_mode)
            qids.append(qi)
            attributes[qi["attribute"]] = span

    if not qids:
        return None

    doc_id = str(doc.get("doc_id", "unknown"))
    return {
        "id": f"tab_echr_{doc_id}",
        "source": "tab_echr",
        "domain": "legal_case",
        "original_text": str(doc.get("text", "")),
        "quasi_identifiers": qids,
        "label_keywords": ["court", "applicant", "application", "article", "judgment"],
        "label_threshold": 2,
        "utility_facts": [
            {
                "name": "legal proceeding structure",
                "acceptable_terms": ["court", "applicant", "application", "judgment"],
            },
            {
                "name": "legal issue framing",
                "acceptable_terms": ["article", "complaint", "proceedings", "case"],
            },
        ],
        "ground_truth": {
            "direct_identifiers": direct_ids,
            "attributes": attributes,
            "utility_label": "legal_case_summary",
        },
        "tab_meta": {
            "doc_id": doc_id,
            "dataset_type": doc.get("dataset_type", ""),
            "task": doc.get("task", ""),
            "quality_checked": doc.get("quality_checked", False),
            "n_direct_identifiers": len(direct_ids),
            "n_quasi_identifiers": len(qids),
            "generalization_mode": generalization_mode,
        },
    }


def load_records(*, url: str, n: int, annotator_mode: str, generalization_mode: str) -> list[dict[str, Any]]:
    docs = fetch_json(url)
    records = []
    for doc in docs:
        mentions = mentions_for_doc(doc, annotator_mode)
        converted = convert_doc(doc, mentions, generalization_mode)
        if converted is None:
            continue
        records.append(converted)
        if len(records) >= n:
            break
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Load a small TAB ECHR subset.")
    parser.add_argument("--split", choices=sorted(DEFAULT_FILES), default="dev")
    parser.add_argument("--url", default="")
    parser.add_argument("--n", type=int, default=30)
    parser.add_argument("--annotator-mode", choices=["first", "merge"], default="first")
    parser.add_argument("--generalization-mode", choices=["generic", "legal_role"], default="generic")
    parser.add_argument("--out", default="data/processed/tab_echr_dev_30.jsonl")
    args = parser.parse_args()

    url = args.url or DEFAULT_FILES[args.split]
    records = load_records(
        url=url,
        n=args.n,
        annotator_mode=args.annotator_mode,
        generalization_mode=args.generalization_mode,
    )
    write_jsonl(args.out, records)
    print(f"Wrote {len(records)} TAB records to {args.out}")
    if len(records) < args.n:
        print(f"Warning: requested {args.n} records but only loaded {len(records)}")


if __name__ == "__main__":
    main()
