from __future__ import annotations

import argparse
import csv
import random
from collections import defaultdict
from pathlib import Path
from typing import Any

from rbqig.evaluate import per_record_metrics
from rbqig.io_utils import ensure_parent, mean, read_jsonl, write_csv
from rbqig.plots import LABELS


METHOD_ORDER = {
    "none": 0,
    "direct": 1,
    "llm_direct": 2,
    "blanket_qi": 3,
    "rbqig_b2": 4,
    "rbqig_b4": 5,
    "rbqig_b6": 6,
}


DEFAULT_METRICS = [
    "direct_identifier_leakage",
    "record_compromise_rate",
    "exact_attribute_leakage",
    "coarse_attribute_leakage",
    "risk_weighted_leakage",
    "label_preservation",
    "utility_fact_preservation",
    "token_change_rate",
]


def read_csv(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def normalize_metric_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        normalized = {
            "id": row["id"],
            "method": row["method"],
            "domain": row.get("domain", ""),
        }
        for key, value in row.items():
            if key in {"id", "method", "domain", "details", "raw_guesses", "attribute_evidence"}:
                continue
            metric = "record_compromise_rate" if key == "record_compromised" else key
            try:
                normalized[metric] = float(value)
            except (TypeError, ValueError):
                continue
        out.append(normalized)
    return out


def load_metric_rows(path: str | Path, source_type: str) -> list[dict[str, Any]]:
    if source_type == "transformed":
        return normalize_metric_rows(per_record_metrics(read_jsonl(path)))
    if source_type == "llm-attacker":
        return normalize_metric_rows(read_jsonl(path))
    if source_type == "metrics-jsonl":
        return normalize_metric_rows(read_jsonl(path))
    if source_type == "metrics-csv":
        return normalize_metric_rows(read_csv(path))
    raise ValueError(f"Unknown source type: {source_type}")


def available_metrics(rows: list[dict[str, Any]], requested: list[str]) -> list[str]:
    keys = set()
    for row in rows:
        keys.update(row.keys())
    return [metric for metric in requested if metric in keys]


def values_by_method(rows: list[dict[str, Any]], metrics: list[str]) -> dict[str, dict[str, dict[str, float]]]:
    values: dict[str, dict[str, dict[str, float]]] = defaultdict(dict)
    for row in rows:
        values[row["method"]][row["id"]] = {
            metric: float(row[metric])
            for metric in metrics
            if metric in row
        }
    return values


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = pct * (len(ordered) - 1)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def bootstrap_mean(
    rng: random.Random,
    method_values: dict[str, dict[str, float]],
    metric: str,
    n_boot: int,
) -> tuple[float, float, float, int]:
    ids = [record_id for record_id, row in method_values.items() if metric in row]
    point = mean([method_values[record_id][metric] for record_id in ids])
    samples = []
    for _ in range(n_boot):
        draw = [rng.choice(ids) for _ in ids]
        samples.append(mean([method_values[record_id][metric] for record_id in draw]))
    return point, percentile(samples, 0.025), percentile(samples, 0.975), len(ids)


def bootstrap_diff(
    rng: random.Random,
    left_values: dict[str, dict[str, float]],
    right_values: dict[str, dict[str, float]],
    metric: str,
    n_boot: int,
) -> tuple[float, float, float, int]:
    ids = [
        record_id
        for record_id in sorted(set(left_values).intersection(right_values))
        if metric in left_values[record_id] and metric in right_values[record_id]
    ]
    point = mean([left_values[record_id][metric] - right_values[record_id][metric] for record_id in ids])
    samples = []
    for _ in range(n_boot):
        draw = [rng.choice(ids) for _ in ids]
        samples.append(mean([left_values[record_id][metric] - right_values[record_id][metric] for record_id in draw]))
    return point, percentile(samples, 0.025), percentile(samples, 0.975), len(ids)


def parse_comparisons(raw: list[str], methods: set[str]) -> list[tuple[str, str]]:
    if raw:
        return [tuple(item.split(":", 1)) for item in raw if ":" in item]
    candidates = [("direct", "rbqig_b4"), ("direct", "blanket_qi"), ("rbqig_b4", "blanket_qi")]
    return [(left, right) for left, right in candidates if left in methods and right in methods]


def pct(value: float) -> str:
    return f"{100.0 * value:.1f}%"


def method_label(method: str) -> str:
    return LABELS.get(method, method)


def sort_methods(methods: set[str]) -> list[str]:
    return sorted(methods, key=lambda method: (METHOD_ORDER.get(method, 99), method))


def write_report(
    path: str | Path,
    source_name: str,
    ci_rows: list[dict[str, Any]],
    contrast_rows: list[dict[str, Any]],
) -> None:
    ensure_parent(path)
    focus_metrics = [
        "risk_weighted_leakage",
        "record_compromise_rate",
        "utility_fact_preservation",
        "llm_fact_preservation",
        "semantic_utility_score",
        "utility_weighted_specificity",
        "qi_specificity_score",
        "qi_generalized_rate",
        "qi_placeholder_rate",
        "qi_exact_rate",
        "legal_summary_preservation",
        "procedure_preservation",
        "legal_issue_preservation",
        "timeline_preservation",
        "outcome_or_remedy_preservation",
        "legal_specificity",
        "legal_task_utility",
        "privacy_aware_label_preservation",
        "task_content_preservation",
        "privacy_aware_utility",
        "private_loss_penalty",
        "token_change_rate",
    ]
    by_metric = defaultdict(list)
    for row in ci_rows:
        by_metric[row["metric"]].append(row)

    lines = [
        f"# Bootstrap Confidence Intervals: {source_name}",
        "",
        "Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.",
        "",
    ]
    for metric in focus_metrics:
        rows = by_metric.get(metric, [])
        if not rows:
            continue
        lines.extend(
            [
                f"## {metric}",
                "",
                "| Method | Mean | 95% CI | n |",
                "|---|---:|---:|---:|",
            ]
        )
        for row in sorted(rows, key=lambda item: (METHOD_ORDER.get(str(item["method"]), 99), str(item["method"]))):
            lines.append(
                "| {method} | {mean} | [{low}, {high}] | {n} |".format(
                    method=method_label(str(row["method"])),
                    mean=pct(float(row["mean"])),
                    low=pct(float(row["ci_low"])),
                    high=pct(float(row["ci_high"])),
                    n=row["n_records"],
                )
            )
        lines.append("")

    if contrast_rows:
        lines.extend(
            [
                "## Paired Contrasts",
                "",
                "Positive values mean the first method has a larger metric value than the second.",
                "",
                "| Comparison | Metric | Mean difference | 95% CI | n |",
                "|---|---|---:|---:|---:|",
            ]
        )
        for row in contrast_rows:
            if row["metric"] not in focus_metrics:
                continue
            lines.append(
                "| {comparison} | {metric} | {mean} | [{low}, {high}] | {n} |".format(
                    comparison=row["comparison"],
                    metric=row["metric"],
                    mean=pct(float(row["mean_diff"])),
                    low=pct(float(row["ci_low"])),
                    high=pct(float(row["ci_high"])),
                    n=row["n_records"],
                )
            )
        lines.append("")

    Path(path).write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap RB-QIG result confidence intervals.")
    parser.add_argument("--input", required=True)
    parser.add_argument(
        "--source-type",
        choices=["transformed", "llm-attacker", "metrics-jsonl", "metrics-csv"],
        required=True,
    )
    parser.add_argument("--source-name", required=True)
    parser.add_argument("--cis-out", required=True)
    parser.add_argument("--contrasts-out", required=True)
    parser.add_argument("--report-out")
    parser.add_argument("--per-record-out")
    parser.add_argument("--n-boot", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=20260627)
    parser.add_argument("--metrics", nargs="*", default=DEFAULT_METRICS)
    parser.add_argument("--comparisons", nargs="*", default=[])
    args = parser.parse_args()

    rows = load_metric_rows(args.input, args.source_type)
    metrics = available_metrics(rows, args.metrics)
    values = values_by_method(rows, metrics)
    methods = set(values)
    comparisons = parse_comparisons(args.comparisons, methods)
    rng = random.Random(args.seed)

    ci_rows = []
    for method in sort_methods(methods):
        for metric in metrics:
            point, low, high, n_records = bootstrap_mean(rng, values[method], metric, args.n_boot)
            ci_rows.append(
                {
                    "source": args.source_name,
                    "method": method,
                    "metric": metric,
                    "mean": round(point, 6),
                    "ci_low": round(low, 6),
                    "ci_high": round(high, 6),
                    "n_records": n_records,
                    "n_boot": args.n_boot,
                    "seed": args.seed,
                }
            )

    contrast_rows = []
    for left, right in comparisons:
        for metric in metrics:
            point, low, high, n_records = bootstrap_diff(rng, values[left], values[right], metric, args.n_boot)
            contrast_rows.append(
                {
                    "source": args.source_name,
                    "comparison": f"{left}_minus_{right}",
                    "metric": metric,
                    "mean_diff": round(point, 6),
                    "ci_low": round(low, 6),
                    "ci_high": round(high, 6),
                    "n_records": n_records,
                    "n_boot": args.n_boot,
                    "seed": args.seed,
                }
            )

    write_csv(args.cis_out, ci_rows)
    write_csv(args.contrasts_out, contrast_rows)
    if args.per_record_out:
        write_csv(args.per_record_out, rows)
    if args.report_out:
        write_report(args.report_out, args.source_name, ci_rows, contrast_rows)
    print(f"Wrote {len(ci_rows)} CI rows and {len(contrast_rows)} contrast rows")


if __name__ == "__main__":
    main()
