from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from rbqig.io_utils import contains_term, ensure_parent, read_jsonl, write_jsonl
from rbqig.synthetic import make_qi


DEFAULT_API_KEY_PATH = "/home/eston/colm_workshop/apikey.txt"
RESPONSES_URL = "https://api.openai.com/v1/responses"

# Current standard pricing from the OpenAI pricing page, USD per 1M tokens.
MODEL_PRICING = {
    "gpt-5.4-nano": {"input": 0.20, "output": 1.25},
    "gpt-5.4-mini": {"input": 0.75, "output": 4.50},
    "gpt-5.5": {"input": 5.00, "output": 30.00},
}

CATEGORY_BY_ATTRIBUTE = {
    "citizenship_status": "demographic",
    "date_of_birth": "date",
    "state_of_residence": "location",
    "location": "location",
    "sex": "demographic",
    "marital_status": "demographic",
    "age": "age",
    "race": "demographic",
    "education": "education",
}


ATTRIBUTE_SAFE_GENERALIZATIONS = {
    "age": "an age range",
    "citizenship_status": "a citizenship or birthplace status",
    "date_of_birth": "a birth date",
    "education": "an education context",
    "employment_status": "an employment status",
    "marital_status": "a marital status",
    "race": "a race or ethnicity",
    "race_ethnicity": "a race or ethnicity",
    "rac2p": "a race or ethnicity",
    "sex": "a sex or gender attribute",
    "state_of_residence": "a broader location",
}


SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "quasi_identifiers": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "attribute": {"type": "string"},
                    "category": {"type": "string"},
                    "spans": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "privacy_risk": {"type": "integer"},
                    "utility_importance": {"type": "integer"},
                    "suggested_generalization": {"type": "string"},
                    "why_risky": {"type": "string"},
                },
                "required": [
                    "attribute",
                    "category",
                    "spans",
                    "privacy_risk",
                    "utility_importance",
                    "suggested_generalization",
                    "why_risky",
                ],
            },
        }
    },
    "required": ["quasi_identifiers"],
}


SYSTEM_PROMPT = """You are annotating a public synthetic anonymization benchmark.
Do not identify or investigate any real person.
Find text spans that reveal the supplied benchmark target attributes.
Return only spans that appear verbatim in the text.
Include repeated mentions and common variants when they reveal the same target.
Prefer short exact spans over full sentences.
Do not include direct identifiers such as names, emails, or phone numbers unless they also reveal a supplied target attribute.
Do not include field labels, questions, or headings that merely request an attribute unless the target value is asserted in the same span.
For example, do not output "sex" by itself for a sex target; output "I am male" or "female" when those spans assert the value.
Use categories from this set when possible: location, date, age, occupation, employer, education, medical, legal, financial, family, event, rare_fact, demographic, other.
Use privacy_risk and utility_importance integers from 0 to 5.
"""


BLIND_SYSTEM_PROMPT = """You are annotating a synthetic or public anonymization benchmark.
Do not identify or investigate any real person.
Find quasi-identifiers: spans that may not identify a person alone but could reveal sensitive attributes or support re-identification when combined with other details.
Return only spans that appear verbatim in the text.
Include repeated mentions and common variants when they reveal the same target.
Prefer short exact spans over full sentences.
Do not include direct identifiers such as names, emails, phone numbers, addresses, or IDs unless they also reveal a quasi-identifier category such as location, date, age, occupation, employer, education, medical, legal, financial, family, event, rare fact, or demographic status.
Do not include field labels, questions, or headings that merely request an attribute unless the target value is asserted in the same span.
Use categories from this set when possible: location, date, age, occupation, employer, education, medical, legal, financial, family, event, rare_fact, demographic, other.
Use privacy_risk and utility_importance integers from 0 to 5.
"""


GENERIC_BLIND_PATTERNS = [
    (
        "sex",
        "demographic",
        r"\b(?:male|female|man|woman|men|women)\b",
        2,
        "a sex or gender attribute",
        "Generic sex or gender cue",
    ),
    (
        "marital_status",
        "demographic",
        r"\b(?:never married|married|divorced|separated|widowed|widow|spouse|wife|husband)\b",
        3,
        "a marital or family status",
        "Generic marital-status cue",
    ),
    (
        "citizenship_status",
        "demographic",
        r"\b(?:not a citizen of the US|not a U\.S\. citizen|not a US citizen|born in the US|born in the United States|U\.S\. citizen|US citizen|naturalized citizen|citizen by naturalization)\b",
        3,
        "a citizenship status",
        "Generic citizenship cue",
    ),
    (
        "education",
        "education",
        r"\b(?:grade\s+\d{1,2}|\d{1,2}(?:st|nd|rd|th)\s+grade|bachelor'?s|bachelors|master'?s|masters|associate'?s|associates|doctorate|ph\.?d\.?|ged|high school diploma|some college|college degree)\b(?: degree)?(?: in [A-Za-z][A-Za-z ]{1,40})?",
        3,
        "an education category",
        "Generic education cue",
    ),
    (
        "employment_status",
        "occupation",
        r"\b(?:civilian employed|with a job but not at work|not at work|looking for work|self-employed|active duty|armed forces|employed|unemployed|retired)\b",
        3,
        "an employment status",
        "Generic employment-status cue",
    ),
    (
        "race_ethnicity",
        "demographic",
        r"\b(?:Native American|American Indian|Alaska Native|Pacific Islander|Cherokee|Houma|Hispanic|Latino|Latina|Asian|Black|White|Filipino|Laotian|Micronesian)\b",
        4,
        "a race or ethnicity category",
        "Generic race or ethnicity cue",
    ),
]


def stable_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def read_api_key(path: str) -> str:
    key = Path(path).read_text(encoding="utf-8").strip()
    if not key:
        raise RuntimeError(f"API key file is empty: {path}")
    return key


def response_text(response: dict[str, Any]) -> str:
    if isinstance(response.get("output_text"), str):
        return response["output_text"]
    chunks = []
    for item in response.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                chunks.append(content.get("text", ""))
    return "\n".join(chunk for chunk in chunks if chunk)


def make_request_payload(
    record: dict[str, Any],
    model: str,
    max_output_tokens: int,
    *,
    blind: bool = False,
) -> dict[str, Any]:
    attrs = record.get("ground_truth", {}).get("attributes", {})
    user_prompt = {
        "benchmark_id": record.get("id"),
        "difficulty": record.get("difficulty"),
        "text": record.get("original_text", ""),
    }
    if not blind:
        user_prompt["target_attributes"] = attrs
    return {
        "model": model,
        "input": [
            {
                "role": "system",
                "content": [{"type": "input_text", "text": BLIND_SYSTEM_PROMPT if blind else SYSTEM_PROMPT}],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": json.dumps(user_prompt, ensure_ascii=False),
                    }
                ],
            },
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "qi_mentions",
                "schema": SCHEMA,
                "strict": True,
            }
        },
        "max_output_tokens": max_output_tokens,
        "store": False,
    }


def call_responses_api(api_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        RESPONSES_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"OpenAI API HTTP {exc.code}: {body}") from exc


def _decade_from_value(value: str) -> str:
    for token in value.replace(",", " ").split():
        if token.isdigit() and len(token) == 4:
            return f"{token[:3]}0s"
    return ""


def default_generalization(record: dict[str, Any], attribute: str, category: str) -> str:
    attrs = record.get("ground_truth", {}).get("attributes", {})
    value = str(attrs.get(attribute, ""))
    if attribute == "date_of_birth":
        decade = _decade_from_value(value)
        if decade:
            return f"a birth date in the {decade}"
        return "a birth date"
    if attribute == "citizenship_status":
        return "a citizenship status"
    if attribute in {"state_of_residence", "location"} or category == "location":
        return "a broader location"
    if attribute in {"sex", "marital_status", "race"}:
        return "a demographic attribute"
    if attribute == "education":
        return "an education category"
    if category == "demographic":
        return "a demographic attribute"
    return f"a generalized {category}"


def normalize_attribute(attribute: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", attribute.lower()).strip("_")
    aliases = {
        "date": "date",
        "date_of_birth": "date_of_birth",
        "dob": "date_of_birth",
        "born_in_the_us": "citizenship_status",
        "born_in_the_united_states": "citizenship_status",
        "birthplace": "citizenship_status",
        "country_of_birth": "citizenship_status",
        "marital_status": "marital_status",
        "marital": "marital_status",
        "sex": "sex",
        "gender": "sex",
        "race": "race",
        "race_ethnicity": "race_ethnicity",
        "ethnicity": "race_ethnicity",
        "rac2p": "rac2p",
        "occupation_education_context_school": "education",
    }
    return aliases.get(normalized, normalized)


def safe_blind_generalization(attribute: str, category: str, suggested: str) -> str:
    normalized = normalize_attribute(attribute)
    if normalized in ATTRIBUTE_SAFE_GENERALIZATIONS:
        return ATTRIBUTE_SAFE_GENERALIZATIONS[normalized]
    if "birth" in normalized and "date" in normalized:
        return "a birth date"
    if "citizen" in normalized or "born" in normalized:
        return "a citizenship or birthplace status"
    if "marital" in normalized or "spouse" in normalized:
        return "a marital status"
    if "race" in normalized or "ethnic" in normalized:
        return "a race or ethnicity"
    if "sex" in normalized or "gender" in normalized:
        return "a sex or gender attribute"
    if "education" in normalized or "school" in normalized:
        return "an education context"
    if "employment" in normalized or "occupation" in normalized or "retire" in normalized:
        return "an employment or occupation status"
    if "email" in normalized or "phone" in normalized or "card" in normalized:
        return "a redacted direct identifier"

    if category == "date":
        return "a date"
    if category == "location":
        return "a broader location"
    if category == "age":
        return "an age range"
    if category == "education":
        return "an education context"
    if category == "occupation":
        return "an employment or occupation status"
    if category == "family":
        return "a family relationship"
    if category == "medical":
        return "medical information"
    if category == "legal":
        return "legal information"
    if category == "financial":
        return "financial information"
    if category == "demographic":
        return "a demographic attribute"
    if suggested:
        return "a generalized quasi-identifier"
    return f"a generalized {category}"


def expand_api_qis(
    record: dict[str, Any],
    api_output: dict[str, Any],
    *,
    blind: bool = False,
    safe_blind_generalizations: bool = False,
) -> list[dict[str, Any]]:
    text = record.get("original_text", "")
    qids = []
    seen = set()
    for item in api_output.get("quasi_identifiers", []):
        attribute = item.get("attribute", "other")
        category = CATEGORY_BY_ATTRIBUTE.get(attribute) or item.get("category") or "other"
        privacy_risk = int(item.get("privacy_risk", 3))
        utility_importance = int(item.get("utility_importance", 2))
        if blind and privacy_risk <= 2 and utility_importance >= 3:
            continue
        suggested = str(item.get("suggested_generalization", "")).strip()
        if blind and safe_blind_generalizations:
            broad = safe_blind_generalization(attribute, category, suggested)
            broad_risk = 1
        else:
            broad = suggested if blind and suggested else default_generalization(record, attribute, category)
            broad_risk = 1 if privacy_risk <= 3 else 2
        why = item.get("why_risky", "API-extracted quasi-identifier")
        for span in item.get("spans", []):
            span = str(span).strip()
            if "?" in span:
                continue
            if not span or not contains_term(text, span):
                continue
            key = (attribute, span.lower())
            if key in seen:
                continue
            seen.add(key)
            qids.append(
                make_qi(
                    attribute=attribute,
                    category=category,
                    span=span,
                    broad=broad,
                    privacy_risk=max(0, min(5, privacy_risk)),
                    utility_importance=max(0, min(5, utility_importance)),
                    why_risky=why[:120],
                    placeholder=f"[{category.upper()}]",
                    broad_risk=broad_risk,
                    broad_utility_loss=0.75,
                    redaction_utility_loss=3.0,
                )
            )
    if blind:
        qids.extend(generic_blind_backstop_qis(record, seen))
    else:
        qids.extend(heuristic_variant_qis(record, seen))
    return qids


def add_variant(
    out: list[dict[str, Any]],
    seen: set[tuple[str, str]],
    record: dict[str, Any],
    attribute: str,
    category: str,
    span: str,
    privacy_risk: int,
    why: str,
) -> None:
    text = record.get("original_text", "")
    span = span.strip()
    if not span or not contains_term(text, span):
        return
    key = (attribute, span.lower())
    if key in seen:
        return
    seen.add(key)
    out.append(
        make_qi(
            attribute=attribute,
            category=category,
            span=span,
            broad=default_generalization(record, attribute, category),
            privacy_risk=privacy_risk,
            utility_importance=2,
            why_risky=why,
            placeholder=f"[{category.upper()}]",
            broad_risk=1 if privacy_risk <= 3 else 2,
            broad_utility_loss=0.75,
            redaction_utility_loss=3.0,
        )
    )


def add_blind_backstop_qi(
    out: list[dict[str, Any]],
    seen: set[tuple[str, str]],
    record: dict[str, Any],
    attribute: str,
    category: str,
    span: str,
    privacy_risk: int,
    broad: str,
    why: str,
) -> None:
    span = span.strip()
    if not span:
        return
    lower_span = span.lower()
    if any(existing_span == lower_span for _, existing_span in seen):
        return
    key = (attribute, lower_span)
    seen.add(key)
    out.append(
        make_qi(
            attribute=attribute,
            category=category,
            span=span,
            broad=broad,
            privacy_risk=privacy_risk,
            utility_importance=2,
            why_risky=why,
            placeholder=f"[{category.upper()}]",
            broad_risk=1 if privacy_risk <= 3 else 2,
            broad_utility_loss=0.75,
            redaction_utility_loss=3.0,
        )
    )


def generic_blind_backstop_qis(record: dict[str, Any], seen: set[tuple[str, str]]) -> list[dict[str, Any]]:
    text = record.get("original_text", "")
    out: list[dict[str, Any]] = []
    for attribute, category, pattern, privacy_risk, broad, why in GENERIC_BLIND_PATTERNS:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            add_blind_backstop_qi(
                out,
                seen,
                record,
                attribute,
                category,
                match.group(0),
                privacy_risk,
                broad,
                why,
            )
    return out


def heuristic_variant_qis(record: dict[str, Any], seen: set[tuple[str, str]]) -> list[dict[str, Any]]:
    attrs = record.get("ground_truth", {}).get("attributes", {})
    out: list[dict[str, Any]] = []
    for attribute, raw_value in attrs.items():
        value = str(raw_value)
        lower = value.lower()
        category = CATEGORY_BY_ATTRIBUTE.get(attribute, "demographic")

        if attribute in {"rac2p", "race"}:
            add_variant(out, seen, record, attribute, "demographic", value, 4, "Race or ethnicity value")
            if lower in {"cherokee", "houma"}:
                for span in ["Native", "Native American", "Indigenous"]:
                    add_variant(out, seen, record, attribute, "demographic", span, 3, "Tribal affiliation cue")

        if attribute == "marital_status":
            add_variant(out, seen, record, attribute, "demographic", value, 3, "Marital status value")
            if "married" in lower:
                for span in ["married", "wife", "husband", "spouse"]:
                    add_variant(out, seen, record, attribute, "demographic", span, 3, "Marital relationship cue")
            if "divorced" in lower:
                for span in ["divorced", "ex-wife", "ex-husband", "ex-spouse"]:
                    add_variant(out, seen, record, attribute, "demographic", span, 3, "Divorce status cue")
            if "widowed" in lower:
                for span in ["widowed", "widow", "late husband", "late wife", "late spouse"]:
                    add_variant(out, seen, record, attribute, "demographic", span, 3, "Widowhood cue")

        if attribute == "sex":
            add_variant(out, seen, record, attribute, "demographic", value, 2, "Sex or gender value")
            if lower == "female":
                for span in ["female", "woman", "women", "girls", "she/her"]:
                    add_variant(out, seen, record, attribute, "demographic", span, 2, "Gendered cue")
            if lower == "male":
                for span in ["male", "man", "men", "boys", "he/him"]:
                    add_variant(out, seen, record, attribute, "demographic", span, 2, "Gendered cue")

        if attribute == "citizenship_status":
            add_variant(out, seen, record, attribute, "demographic", value, 3, "Citizenship value")
            if "not a citizen" in lower:
                for span in ["not a citizen", "not a US citizen", "not a U.S. citizen", "non-US citizen", "non-U.S. citizen"]:
                    add_variant(out, seen, record, attribute, "demographic", span, 3, "Citizenship cue")
            if "born in the us" in lower or "born in the united states" in lower:
                for span in ["born in the US", "born in the United States", "U.S.-born", "US-born"]:
                    add_variant(out, seen, record, attribute, "demographic", span, 3, "Citizenship birthplace cue")
            if "naturalization" in lower or "naturalized" in lower:
                for span in ["naturalized", "naturalization", "citizen by naturalization", "U.S. citizen by naturalization", "US citizen by naturalization"]:
                    add_variant(out, seen, record, attribute, "demographic", span, 3, "Naturalization cue")

    return out


def estimate_cost(model: str, usage: dict[str, Any]) -> float:
    pricing = MODEL_PRICING.get(model)
    if not pricing:
        return 0.0
    input_tokens = float(usage.get("input_tokens", 0) or 0)
    output_tokens = float(usage.get("output_tokens", 0) or 0)
    return (
        input_tokens * pricing["input"] / 1_000_000
        + output_tokens * pricing["output"] / 1_000_000
    )


def extract_records(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    api_key = read_api_key(args.api_key_path)
    records = read_jsonl(args.input)[: args.n]
    out_records = []
    usage_rows = []
    cache_dir = Path(args.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    for idx, record in enumerate(records, start=1):
        payload = make_request_payload(record, args.model, args.max_output_tokens, blind=args.blind)
        cache_key = stable_hash(
            {
                "model": args.model,
                "record_id": record.get("id"),
                "payload": payload,
                "version": 1 if args.blind else 2,
                "blind": args.blind,
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

        raw_text = response_text(response)
        parsed = json.loads(raw_text)
        converted = dict(record)
        original_qis = record.get("quasi_identifiers", [])
        converted["quasi_identifiers"] = expand_api_qis(
            record,
            parsed,
            blind=args.blind,
            safe_blind_generalizations=args.safe_blind_generalizations,
        )
        if args.eval_against_original_qis:
            converted["eval_quasi_identifiers"] = original_qis
        converted["api_qi_extractor"] = {
            "model": args.model,
            "blind": args.blind,
            "safe_blind_generalizations": args.safe_blind_generalizations,
            "from_cache": from_cache,
            "raw_output": parsed,
            "cache_path": str(cache_path),
        }
        out_records.append(converted)

        usage = response.get("usage", {}) or {}
        usage_rows.append(
            {
                "id": record.get("id"),
                "from_cache": from_cache,
                "input_tokens": usage.get("input_tokens", 0),
                "output_tokens": usage.get("output_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
                "estimated_cost_usd": estimate_cost(args.model, usage),
                "n_qi_spans": len(converted["quasi_identifiers"]),
            }
        )
        print(
            f"{idx}/{len(records)} {record.get('id')}: "
            f"{len(converted['quasi_identifiers'])} QI spans, cache={from_cache}"
        )

    summary = {
        "model": args.model,
        "n_records": len(out_records),
        "estimated_cost_usd": round(sum(row["estimated_cost_usd"] for row in usage_rows), 6),
        "usage": usage_rows,
    }
    return out_records, summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract quasi-identifier spans with OpenAI API.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--usage-out", default="results/api_qi_extractor_usage.json")
    parser.add_argument("--cache-dir", default="results/api_cache/qi_extractor")
    parser.add_argument("--api-key-path", default=DEFAULT_API_KEY_PATH)
    parser.add_argument("--model", default="gpt-5.4-nano")
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--max-output-tokens", type=int, default=1600)
    parser.add_argument("--sleep-seconds", type=float, default=0.0)
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--blind", action="store_true")
    parser.add_argument("--eval-against-original-qis", action="store_true")
    parser.add_argument("--safe-blind-generalizations", action="store_true")
    args = parser.parse_args()

    records, summary = extract_records(args)
    write_jsonl(args.out, records)
    ensure_parent(args.usage_out)
    Path(args.usage_out).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote {len(records)} API-extracted records to {args.out}")
    print(f"Estimated API cost: ${summary['estimated_cost_usd']:.6f}")


if __name__ == "__main__":
    main()
