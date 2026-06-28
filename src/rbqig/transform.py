from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

from .redaction import infer_direct_identifiers, replace_direct_identifiers


METHODS = [
    "none",
    "direct",
    "blanket_qi",
    "rbqig_b2",
    "rbqig_b4",
    "rbqig_b6",
]


def _budget_for(method: str) -> float:
    if method == "rbqig_b2":
        return 2.0
    if method == "rbqig_b4":
        return 4.0
    if method == "rbqig_b6":
        return 6.0
    raise ValueError(f"Method has no risk budget: {method}")


def _pairwise_boost(risks: list[float]) -> float:
    linkable = sum(1 for risk in risks if risk >= 3.0)
    return 0.5 * (linkable * (linkable - 1) / 2)


def compute_doc_risk(states: list[dict[str, Any]]) -> float:
    risks = [float(state["current_risk"]) for state in states]
    return sum(risks) + _pairwise_boost(risks)


def _initial_states(record: dict[str, Any]) -> list[dict[str, Any]]:
    states = []
    for idx, qi in enumerate(record.get("quasi_identifiers", [])):
        states.append(
            {
                "idx": idx,
                "qi": qi,
                "level": 0,
                "current_risk": float(qi["privacy_risk"]),
                "current_utility_loss": 0.0,
            }
        )
    return states


def _next_candidate(state: dict[str, Any]) -> dict[str, Any] | None:
    levels = state["qi"].get("levels", [])
    for next_level in range(state["level"] + 1, len(levels) + 1):
        level_spec = levels[next_level - 1]
        next_risk = float(level_spec["privacy_risk_after"])
        next_loss = float(level_spec["utility_loss"])
        risk_drop = float(state["current_risk"]) - next_risk
        if risk_drop <= 0:
            continue
        utility_loss = max(0.0, next_loss - float(state["current_utility_loss"]))
        return {
            "score": risk_drop / max(utility_loss, 0.25),
            "risk_drop": risk_drop,
            "utility_loss": utility_loss,
            "next_level": next_level,
            "next_risk": next_risk,
            "next_loss": next_loss,
            "state": state,
            "level_spec": level_spec,
        }
    return None


def _choose_budgeted_levels(record: dict[str, Any], budget: float) -> tuple[list[dict[str, Any]], float, float]:
    states = _initial_states(record)
    initial_risk = compute_doc_risk(states)
    current_risk = initial_risk

    while current_risk > budget:
        candidates = [_next_candidate(state) for state in states]
        candidates = [candidate for candidate in candidates if candidate is not None]
        if not candidates:
            break
        best = max(
            candidates,
            key=lambda item: (
                item["score"],
                item["risk_drop"],
                -item["utility_loss"],
                item["state"]["qi"]["privacy_risk"],
            ),
        )
        state = best["state"]
        state["level"] = best["next_level"]
        state["current_risk"] = best["next_risk"]
        state["current_utility_loss"] = best["next_loss"]
        current_risk = compute_doc_risk(states)

    return states, initial_risk, current_risk


def _replace_all(text: str, replacements: list[tuple[str, str]]) -> str:
    current = text
    for original, replacement in sorted(replacements, key=lambda pair: len(pair[0]), reverse=True):
        if not original:
            continue
        prefix = r"(?<![A-Za-z0-9_])" if original[0].isalnum() else ""
        suffix = r"(?![A-Za-z0-9_])" if original[-1].isalnum() else ""
        pattern = re.compile(prefix + re.escape(original) + suffix, flags=re.IGNORECASE)
        current = pattern.sub(lambda _: replacement, current)
    return current


def _qi_change(qi: dict[str, Any], replacement: str, risk_after: float, kind: str) -> dict[str, Any]:
    return {
        "original_span": qi["span"],
        "replacement": replacement,
        "category": qi["category"],
        "attribute": qi.get("attribute", qi["category"]),
        "privacy_risk_before": qi["privacy_risk"],
        "privacy_risk_after": risk_after,
        "utility_importance": qi["utility_importance"],
        "kind": kind,
    }


def transform_record(record: dict[str, Any], method: str) -> dict[str, Any]:
    if method not in METHODS:
        raise ValueError(f"Unknown method {method}. Expected one of {METHODS}.")

    original_text = record["original_text"]
    direct_ids = infer_direct_identifiers(
        original_text, record.get("ground_truth", {}).get("direct_identifiers", [])
    )
    ground_truth = deepcopy(record.get("ground_truth", {}))
    ground_truth["direct_identifiers"] = deepcopy(direct_ids)
    doc_risk_before = compute_doc_risk(_initial_states(record))

    if method == "none":
        transformed = original_text
        change_log: list[dict[str, Any]] = []
        doc_risk_after = doc_risk_before
    elif method == "direct":
        transformed, change_log = replace_direct_identifiers(original_text, direct_ids)
        doc_risk_after = doc_risk_before
    else:
        transformed = original_text
        change_log = []
        doc_risk_after = doc_risk_before

    if method == "blanket_qi":
        replacements = []
        for qi in record.get("quasi_identifiers", []):
            replacement = f"[{qi['category'].upper()}]"
            replacements.append((qi["span"], replacement))
            change_log.append(_qi_change(qi, replacement, 0.0, "blanket_qi_redact"))
        transformed = _replace_all(transformed, replacements)
        transformed, direct_changes = replace_direct_identifiers(transformed, direct_ids)
        change_log.extend(direct_changes)
        doc_risk_after = 0.0

    if method.startswith("rbqig_"):
        states, doc_risk_before, doc_risk_after = _choose_budgeted_levels(
            record, _budget_for(method)
        )
        replacements = []
        for state in states:
            if state["level"] == 0:
                continue
            qi = state["qi"]
            level_spec = qi["levels"][state["level"] - 1]
            replacement = level_spec["replacement"]
            replacements.append((qi["span"], replacement))
            change_log.append(
                _qi_change(
                    qi,
                    replacement,
                    float(level_spec["privacy_risk_after"]),
                    f"rbqig_{level_spec['kind']}",
                )
            )
        transformed = _replace_all(transformed, replacements)
        transformed, direct_changes = replace_direct_identifiers(transformed, direct_ids)
        change_log.extend(direct_changes)

    return {
        "id": record["id"],
        "source": record["source"],
        "domain": record["domain"],
        "method": method,
        "original_text": original_text,
        "transformed_text": transformed,
        "change_log": change_log,
        "doc_risk_before": round(doc_risk_before, 3),
        "doc_risk_after": round(doc_risk_after, 3),
        "ground_truth": ground_truth,
        "quasi_identifiers": deepcopy(record.get("quasi_identifiers", [])),
        "eval_quasi_identifiers": deepcopy(record.get("eval_quasi_identifiers", record.get("quasi_identifiers", []))),
        "label_keywords": deepcopy(record.get("label_keywords", [])),
        "label_threshold": record.get("label_threshold", 1),
        "utility_facts": deepcopy(record.get("utility_facts", [])),
    }


def transform_records(records: list[dict[str, Any]], methods: list[str]) -> list[dict[str, Any]]:
    outputs = []
    for method in methods:
        for record in records:
            outputs.append(transform_record(record, method))
    return outputs
