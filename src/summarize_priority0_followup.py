from __future__ import annotations

import argparse
import csv
from pathlib import Path

from rbqig.io_utils import ensure_parent, mean, read_jsonl
from rbqig.plots import LABELS


DATASETS = [
    (
        "Synthetic",
        "results/followup_priority0_20260628/synthetic_100/metrics.csv",
        "results/followup_priority0_20260628/synthetic_100/qi_specificity_metrics.csv",
    ),
    (
        "RAT-Bench blind",
        "results/followup_priority0_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/metrics.csv",
        "results/followup_priority0_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_metrics.csv",
    ),
    (
        "TAB legal",
        "results/followup_priority0_20260628/tab_echr_dev_30/metrics.csv",
        "results/followup_priority0_20260628/tab_echr_dev_30/qi_specificity_metrics.csv",
    ),
]


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def by_method(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["method"]: row for row in rows}


def pct(value: str | float) -> str:
    return f"{100.0 * float(value):.1f}%"


def method_label(method: str) -> str:
    return LABELS.get(method, method)


def md_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] + ["---:"] * (len(headers) - 1)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def no_combo_rows() -> tuple[list[list[str]], list[str]]:
    rows = []
    observations = []
    for dataset, metrics_path, _specificity_path in DATASETS:
        metrics = by_method(read_csv(metrics_path))
        balanced = metrics["rbqig_b4"]
        no_combo = metrics["rbqig_b4_no_combo"]
        for method, row in [("rbqig_b4", balanced), ("rbqig_b4_no_combo", no_combo)]:
            rows.append(
                [
                    dataset,
                    method_label(method),
                    pct(row["risk_weighted_leakage"]),
                    pct(row["utility_fact_preservation"]),
                    pct(row["token_change_rate"]),
                ]
            )
        delta = float(no_combo["risk_weighted_leakage"]) - float(balanced["risk_weighted_leakage"])
        if delta > 0.005:
            observations.append(
                f"- {dataset}: no-combo has higher deterministic leakage by {pct(delta)}, so the pairwise term matters."
            )
        elif delta < -0.005:
            observations.append(
                f"- {dataset}: no-combo has lower deterministic leakage by {pct(-delta)}; this pilot does not support the pairwise term on leakage alone."
            )
        else:
            observations.append(
                f"- {dataset}: no-combo is effectively tied with balanced on deterministic leakage."
            )
    return rows, observations


def no_combo_identity_rows() -> list[list[str]]:
    rows = []
    for dataset, metrics_path, _specificity_path in DATASETS:
        outputs_path = Path(metrics_path).with_name("anonymized_outputs.jsonl")
        records = read_jsonl(outputs_path)
        balanced = {record["id"]: record for record in records if record["method"] == "rbqig_b4"}
        no_combo = {
            record["id"]: record for record in records if record["method"] == "rbqig_b4_no_combo"
        }
        ids = sorted(set(balanced).intersection(no_combo))
        same_text = mean(
            [
                float(balanced[record_id]["transformed_text"] == no_combo[record_id]["transformed_text"])
                for record_id in ids
            ]
        )
        same_changes = mean(
            [
                float(balanced[record_id]["change_log"] == no_combo[record_id]["change_log"])
                for record_id in ids
            ]
        )
        rows.append(
            [
                dataset,
                pct(same_text),
                pct(same_changes),
                f"{mean([float(balanced[record_id]['doc_risk_after']) for record_id in ids]):.2f}",
                f"{mean([float(no_combo[record_id]['doc_risk_after']) for record_id in ids]):.2f}",
            ]
        )
    return rows


def budget_rows() -> list[list[str]]:
    rows = []
    for dataset, metrics_path, specificity_path in DATASETS[1:]:
        metrics = by_method(read_csv(metrics_path))
        specificity = by_method(read_csv(specificity_path))
        for method, budget in [("rbqig_b2", "2"), ("rbqig_b4", "4"), ("rbqig_b6", "6")]:
            metric_row = metrics[method]
            specificity_row = specificity[method]
            rows.append(
                [
                    dataset,
                    budget,
                    pct(metric_row["risk_weighted_leakage"]),
                    pct(specificity_row["utility_weighted_specificity"]),
                    pct(metric_row["token_change_rate"]),
                ]
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize Priority 0 follow-up experiments.")
    parser.add_argument("--out", default="results/followup_priority0_20260628/report.md")
    args = parser.parse_args()

    ablation_rows, observations = no_combo_rows()
    identity_rows = no_combo_identity_rows()
    frontier_rows = budget_rows()
    lines = [
        "# Priority 0 Follow-up Experiments",
        "",
        "No API calls were used. All rows are deterministic evaluations over existing public or synthetic records.",
        "",
        "## Pairwise-Combination-Risk Ablation",
        "",
        *md_table(
            ["Dataset", "Method", "Risk-weighted leakage", "Utility/fact preservation", "Token change"],
            ablation_rows,
        ),
        "",
        "### Interpretation",
        "",
        *observations,
        "",
        "### Mechanism Check",
        "",
        *md_table(
            [
                "Dataset",
                "Identical transformed text",
                "Identical change logs",
                "Mean risk after balanced",
                "Mean risk after no-combo",
            ],
            identity_rows,
        ),
        "",
        "## Public Deterministic Budget Frontier",
        "",
        *md_table(
            ["Dataset", "Budget", "Risk-weighted leakage", "QI specificity", "Token change"],
            frontier_rows,
        ),
        "",
        "## Paper-Facing Conclusion",
        "",
        "The no-combo ablation should be framed as a deterministic diagnostic, not a deployment claim. "
        "The public budget frontier supports the budget knob as an interpretable utility-specificity control, "
        "while public utility remains weaker than in the controlled synthetic setting.",
        "",
    ]
    ensure_parent(args.out)
    Path(args.out).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
