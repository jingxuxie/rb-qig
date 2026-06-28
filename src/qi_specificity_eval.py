from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
from typing import Any

from rbqig.io_utils import contains_term, mean, read_jsonl, write_csv, write_jsonl


EXACT_SCORE = 1.0
GENERALIZED_SCORE = 0.65
PLACEHOLDER_SCORE = 0.25


def placeholder_for(qi: dict[str, Any]) -> str:
    return f"[{str(qi.get('category', 'other')).upper()}]"


def is_placeholder(text: str) -> bool:
    stripped = text.strip()
    return stripped.startswith("[") and stripped.endswith("]")


def qi_changes(record: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        change
        for change in record.get("change_log", [])
        if str(change.get("kind", "")).startswith(("rbqig_", "blanket_qi_"))
    ]


def find_change(
    qi: dict[str, Any],
    changes: list[dict[str, Any]],
    used: set[int],
) -> dict[str, Any] | None:
    span = str(qi.get("span", ""))
    attribute = str(qi.get("attribute", qi.get("category", "")))
    category = str(qi.get("category", ""))
    fallback = None
    for idx, change in enumerate(changes):
        if idx in used:
            continue
        if str(change.get("original_span", "")) != span:
            continue
        if str(change.get("attribute", "")) == attribute:
            used.add(idx)
            return change
        if str(change.get("category", "")) == category and fallback is None:
            fallback = idx
    if fallback is not None:
        used.add(fallback)
        return changes[fallback]
    return None


def generalized_terms(qi: dict[str, Any]) -> list[str]:
    terms = []
    for level in qi.get("levels", []):
        replacement = str(level.get("replacement", ""))
        if replacement and not is_placeholder(replacement):
            terms.append(replacement)
    for term in qi.get("coarse_values", []):
        if term and not is_placeholder(str(term)):
            terms.append(str(term))
    return list(dict.fromkeys(terms))


def classify_qi(
    record: dict[str, Any],
    qi: dict[str, Any],
    change: dict[str, Any] | None,
    *,
    exact_score: float,
    generalized_score: float,
    placeholder_score: float,
) -> dict[str, Any]:
    text = record.get("transformed_text", "")
    span = str(qi.get("span", ""))
    replacement = str(change.get("replacement", "")) if change else ""

    if change:
        if is_placeholder(replacement):
            status = "placeholder"
            score = placeholder_score
        else:
            status = "generalized"
            score = generalized_score
    elif contains_term(text, span):
        status = "exact"
        score = exact_score
    else:
        matched_generalization = next(
            (term for term in generalized_terms(qi) if contains_term(text, term)),
            "",
        )
        if matched_generalization:
            status = "generalized"
            score = generalized_score
            replacement = matched_generalization
        elif contains_term(text, placeholder_for(qi)):
            status = "placeholder"
            score = placeholder_score
            replacement = placeholder_for(qi)
        else:
            status = "dropped"
            score = 0.0

    return {
        "attribute": qi.get("attribute", qi.get("category", "")),
        "category": qi.get("category", ""),
        "span": span,
        "status": status,
        "replacement": replacement,
        "score": score,
        "utility_importance": float(qi.get("utility_importance", 1.0)),
    }


def score_record(
    record: dict[str, Any],
    *,
    exact_score: float,
    generalized_score: float,
    placeholder_score: float,
) -> dict[str, Any]:
    qids = record.get("eval_quasi_identifiers", record.get("quasi_identifiers", []))
    changes = qi_changes(record)
    used_changes: set[int] = set()
    details = []
    for qi in qids:
        change = find_change(qi, changes, used_changes)
        details.append(
            classify_qi(
                record,
                qi,
                change,
                exact_score=exact_score,
                generalized_score=generalized_score,
                placeholder_score=placeholder_score,
            )
        )

    n_qi = max(1, len(details))
    total_weight = sum(item["utility_importance"] for item in details) or 1.0
    weighted_score = sum(item["score"] * item["utility_importance"] for item in details) / total_weight
    unweighted_score = mean([item["score"] for item in details])
    by_status = defaultdict(int)
    for item in details:
        by_status[item["status"]] += 1

    return {
        "id": record["id"],
        "method": record["method"],
        "domain": record.get("domain", ""),
        "n_qis": len(details),
        "qi_specificity_score": round(unweighted_score, 6),
        "utility_weighted_specificity": round(weighted_score, 6),
        "qi_exact_rate": round(by_status["exact"] / n_qi, 6),
        "qi_generalized_rate": round(by_status["generalized"] / n_qi, 6),
        "qi_placeholder_rate": round(by_status["placeholder"] / n_qi, 6),
        "qi_dropped_rate": round(by_status["dropped"] / n_qi, 6),
        "details": details,
    }


def aggregate(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_method: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_method[row["method"]].append(row)

    order = {"none": 0, "direct": 1, "llm_direct": 2, "blanket_qi": 3, "rbqig_b2": 4, "rbqig_b4": 5, "rbqig_b6": 6}
    metrics = [
        "qi_specificity_score",
        "utility_weighted_specificity",
        "qi_exact_rate",
        "qi_generalized_rate",
        "qi_placeholder_rate",
        "qi_dropped_rate",
    ]
    out = []
    for method, method_rows in sorted(by_method.items(), key=lambda item: (order.get(item[0], 99), item[0])):
        row: dict[str, Any] = {"method": method, "n_records": len(method_rows)}
        for metric in metrics:
            row[metric] = round(mean([float(item[metric]) for item in method_rows]), 6)
        out.append(row)
    return out


def pct(value: float) -> str:
    return f"{100.0 * value:.1f}%"


def write_report(path: str | Path, source_name: str, metrics: list[dict[str, Any]]) -> None:
    lines = [
        f"# QI Semantic Specificity: {source_name}",
        "",
        "This no-API diagnostic uses benchmark quasi-identifier annotations.",
        "Per QI, exact retained spans score 1.0, typed generalizations score 0.65,",
        "bare placeholders score 0.25, and dropped information scores 0.0.",
        "It is a semantic-specificity proxy, not a downstream task-accuracy metric.",
        "",
        "| Method | Utility-weighted specificity | Exact | Generalized | Placeholder | Dropped |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in metrics:
        lines.append(
            "| {method} | {specificity} | {exact} | {generalized} | {placeholder} | {dropped} |".format(
                method=row["method"],
                specificity=pct(float(row["utility_weighted_specificity"])),
                exact=pct(float(row["qi_exact_rate"])),
                generalized=pct(float(row["qi_generalized_rate"])),
                placeholder=pct(float(row["qi_placeholder_rate"])),
                dropped=pct(float(row["qi_dropped_rate"])),
            )
        )
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate annotation-derived QI semantic specificity.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--source-name", default="")
    parser.add_argument("--per-record-out", required=True)
    parser.add_argument("--metrics-out", required=True)
    parser.add_argument("--report-out", required=True)
    parser.add_argument("--exact-score", type=float, default=EXACT_SCORE)
    parser.add_argument("--generalized-score", type=float, default=GENERALIZED_SCORE)
    parser.add_argument("--placeholder-score", type=float, default=PLACEHOLDER_SCORE)
    args = parser.parse_args()

    records = read_jsonl(args.input)
    rows = [
        score_record(
            record,
            exact_score=args.exact_score,
            generalized_score=args.generalized_score,
            placeholder_score=args.placeholder_score,
        )
        for record in records
    ]
    metrics = aggregate(rows)
    source_name = args.source_name or Path(args.input).stem
    write_jsonl(args.per_record_out, rows)
    write_csv(args.metrics_out, metrics)
    write_report(args.report_out, source_name, metrics)
    print(f"Wrote QI specificity metrics to {args.metrics_out}")


if __name__ == "__main__":
    main()
