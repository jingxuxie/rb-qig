from __future__ import annotations

from collections import defaultdict
from typing import Any

from .io_utils import contains_term, mean, token_change_rate


def _direct_identifier_leak(record: dict[str, Any]) -> tuple[int, list[str]]:
    text = record["transformed_text"]
    leaked = []
    for identifier in record.get("ground_truth", {}).get("direct_identifiers", []):
        value = identifier.get("value", "")
        if value and contains_term(text, value):
            leaked.append(value)
    return (1 if leaked else 0), leaked


def _qi_leakage(record: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, float]]:
    text = record["transformed_text"]
    q_results = []
    exact_count = 0
    coarse_count = 0
    weighted_score = 0.0
    total_weight = 0.0
    compromised = 0

    eval_qis = record.get("eval_quasi_identifiers", record.get("quasi_identifiers", []))
    for qi in eval_qis:
        span = qi.get("span", "")
        exact = contains_term(text, span)
        coarse_terms = list(qi.get("coarse_values", []))
        for level in qi.get("levels", []):
            if level.get("kind") == "generalize":
                coarse_terms.append(level.get("replacement", ""))
        coarse_match = ""
        for term in coarse_terms:
            if term and contains_term(text, term):
                coarse_match = term
                break
        coarse = bool(exact or coarse_match)
        weight = float(qi.get("risk_weight", qi.get("privacy_risk", 1)))
        exact_count += int(exact)
        coarse_count += int(coarse)
        total_weight += weight
        weighted_score += weight * (1.0 if exact else 0.5 if coarse else 0.0)
        if exact and int(qi.get("privacy_risk", 0)) >= 4:
            compromised = 1
        q_results.append(
            {
                "attribute": qi.get("attribute", qi.get("category", "")),
                "category": qi.get("category", ""),
                "span": span,
                "privacy_risk": qi.get("privacy_risk", 0),
                "exact": exact,
                "coarse": coarse,
                "matched_coarse_term": coarse_match,
            }
        )

    n_qi = max(1, len(eval_qis))
    return q_results, {
        "exact_attribute_leakage": exact_count / n_qi,
        "coarse_attribute_leakage": coarse_count / n_qi,
        "risk_weighted_leakage": weighted_score / max(total_weight, 1.0),
        "record_compromised": float(compromised),
    }


def _utility(record: dict[str, Any]) -> tuple[dict[str, Any], dict[str, float]]:
    text = record["transformed_text"]
    keyword_hits = 0
    for keyword in record.get("label_keywords", []):
        if contains_term(text, keyword):
            keyword_hits += 1
    threshold = int(record.get("label_threshold", 1))
    label_preserved = 1.0 if keyword_hits >= threshold else 0.0

    fact_results = []
    preserved_facts = 0
    for fact in record.get("utility_facts", []):
        matched_terms = [
            term for term in fact.get("acceptable_terms", []) if contains_term(text, term)
        ]
        preserved = bool(matched_terms)
        preserved_facts += int(preserved)
        fact_results.append(
            {
                "name": fact.get("name", ""),
                "preserved": preserved,
                "matched_terms": matched_terms[:3],
            }
        )

    facts_total = max(1, len(record.get("utility_facts", [])))
    token_change = token_change_rate(record["original_text"], text)
    details = {
        "label_keyword_hits": keyword_hits,
        "label_preserved": bool(label_preserved),
        "fact_results": fact_results,
    }
    metrics = {
        "label_preservation": label_preserved,
        "utility_fact_preservation": preserved_facts / facts_total,
        "token_change_rate": token_change,
    }
    return details, metrics


def evaluate_records(records: list[dict[str, Any]]) -> tuple[list[dict], list[dict], list[dict]]:
    attack_rows = []
    utility_rows = []
    metric_rows = per_record_metrics(records)

    for record in records:
        direct_leak, direct_values = _direct_identifier_leak(record)
        qi_details, privacy = _qi_leakage(record)
        utility_details, utility = _utility(record)

        attack_rows.append(
            {
                "id": record["id"],
                "method": record["method"],
                "domain": record["domain"],
                "direct_identifier_leak": direct_leak,
                "direct_identifier_values": direct_values,
                "record_compromised": privacy["record_compromised"],
                "attribute_evidence": qi_details,
            }
        )
        utility_rows.append(
            {
                "id": record["id"],
                "method": record["method"],
                "domain": record["domain"],
                **utility_details,
            }
        )

    return attack_rows, utility_rows, aggregate_metrics(metric_rows)


def per_record_metrics(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    metric_rows = []
    for record in records:
        direct_leak, _direct_values = _direct_identifier_leak(record)
        _qi_details, privacy = _qi_leakage(record)
        _utility_details, utility = _utility(record)
        metric_rows.append(
            {
                "id": record["id"],
                "method": record["method"],
                "domain": record["domain"],
                "direct_identifier_leakage": float(direct_leak),
                **privacy,
                **utility,
            }
        )
    return metric_rows


def aggregate_metrics(per_record_metrics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_method: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in per_record_metrics:
        by_method[row["method"]].append(row)

    method_order = {
        "none": 0,
        "direct": 1,
        "llm_direct": 2,
        "blanket_qi": 3,
        "rbqig_b2": 4,
        "rbqig_b4": 5,
        "rbqig_b6": 6,
    }
    metrics = []
    for method, rows in sorted(by_method.items(), key=lambda item: method_order.get(item[0], 99)):
        metrics.append(
            {
                "method": method,
                "n_records": len(rows),
                "direct_identifier_leakage": round(mean([r["direct_identifier_leakage"] for r in rows]), 4),
                "record_compromise_rate": round(mean([r["record_compromised"] for r in rows]), 4),
                "exact_attribute_leakage": round(mean([r["exact_attribute_leakage"] for r in rows]), 4),
                "coarse_attribute_leakage": round(mean([r["coarse_attribute_leakage"] for r in rows]), 4),
                "risk_weighted_leakage": round(mean([r["risk_weighted_leakage"] for r in rows]), 4),
                "label_preservation": round(mean([r["label_preservation"] for r in rows]), 4),
                "utility_fact_preservation": round(mean([r["utility_fact_preservation"] for r in rows]), 4),
                "token_change_rate": round(mean([r["token_change_rate"] for r in rows]), 4),
                "api_calls": 0,
                "estimated_cost_usd": 0.0,
            }
        )
    return metrics
