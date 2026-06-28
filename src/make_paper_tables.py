from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

from rbqig.io_utils import ensure_parent
from rbqig.plots import LABELS


METHODS = ["none", "direct", "llm_direct", "blanket_qi", "rbqig_b2", "rbqig_b4", "rbqig_b6"]


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def by_method(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["method"]: row for row in rows}


def ci_lookup(rows: list[dict[str, str]]) -> dict[tuple[str, str], tuple[float, float, float]]:
    out = {}
    for row in rows:
        out[(row["method"], row["metric"])] = (
            float(row["mean"]),
            float(row["ci_low"]),
            float(row["ci_high"]),
        )
    return out


def pct(value: float) -> str:
    return f"{100.0 * value + 1e-9:.1f}"


def cell(value: str | float, ci: tuple[float, float, float] | None = None) -> str:
    point = float(value)
    if ci is None:
        return pct(point)
    _mean, low, high = ci
    return f"{pct(point)} [{pct(low)}, {pct(high)}]"


def method_label(method: str) -> str:
    return LABELS.get(method, method)


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] + ["---:"] * (len(headers) - 1)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def latex_escape(text: str) -> str:
    return (
        text.replace("\\", "\\textbackslash{}")
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("_", "\\_")
        .replace("#", "\\#")
    )


def latex_table(caption: str, label: str, headers: list[str], rows: list[list[str]]) -> str:
    cols = "l" + "r" * (len(headers) - 1)
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\begingroup",
        "\\setlength{\\tabcolsep}{3pt}",
        "\\small",
        f"\\caption{{{latex_escape(caption)}}}",
        f"\\label{{{label}}}",
        f"\\begin{{tabular}}{{{cols}}}",
        "\\toprule",
        " & ".join(latex_escape(header) for header in headers) + " \\\\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(latex_escape(item) for item in row) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\endgroup", "\\end{table}"])
    return "\n".join(lines)


def main_synthetic_rows(metrics_path: str, cis_path: str) -> list[list[str]]:
    metrics = by_method(read_csv(metrics_path))
    cis = ci_lookup(read_csv(cis_path))
    rows = []
    for method in METHODS:
        if method not in metrics:
            continue
        row = metrics[method]
        rows.append(
            [
                method_label(method),
                cell(row["risk_weighted_leakage"], cis.get((method, "risk_weighted_leakage"))),
                cell(row["utility_fact_preservation"], cis.get((method, "utility_fact_preservation"))),
                cell(row["token_change_rate"], cis.get((method, "token_change_rate"))),
            ]
        )
    return rows


def ratbench_llm_rows(metrics_path: str, cis_path: str) -> list[list[str]]:
    metrics = by_method(read_csv(metrics_path))
    cis = ci_lookup(read_csv(cis_path))
    rows = []
    for method in ["direct", "llm_direct", "blanket_qi", "rbqig_b4"]:
        if method not in metrics:
            continue
        row = metrics[method]
        rows.append(
            [
                method_label(method),
                cell(row["record_compromise_rate"], cis.get((method, "record_compromise_rate"))),
                cell(row["exact_attribute_leakage"], cis.get((method, "exact_attribute_leakage"))),
                cell(row["coarse_attribute_leakage"], cis.get((method, "coarse_attribute_leakage"))),
                cell(row["risk_weighted_leakage"], cis.get((method, "risk_weighted_leakage"))),
            ]
        )
    return rows


def blind_rows(metrics_path: str, cis_path: str) -> list[list[str]]:
    metrics = by_method(read_csv(metrics_path))
    cis = ci_lookup(read_csv(cis_path))
    rows = []
    for method in ["direct", "blanket_qi", "rbqig_b4"]:
        row = metrics[method]
        rows.append(
            [
                method_label(method),
                cell(row["risk_weighted_leakage"], cis.get((method, "risk_weighted_leakage"))),
                cell(row["utility_fact_preservation"], cis.get((method, "utility_fact_preservation"))),
                cell(row["token_change_rate"], cis.get((method, "token_change_rate"))),
            ]
        )
    return rows


def blind_public_rows(
    attacker_metrics_path: str,
    attacker_cis_path: str,
    utility_metrics_path: str,
    utility_cis_path: str,
) -> list[list[str]]:
    attacker_metrics = by_method(read_csv(attacker_metrics_path))
    attacker_cis = ci_lookup(read_csv(attacker_cis_path))
    utility_metrics = by_method(read_csv(utility_metrics_path))
    utility_cis = ci_lookup(read_csv(utility_cis_path))
    rows = []
    for method in ["direct", "blanket_qi", "rbqig_b4"]:
        attacker_row = attacker_metrics[method]
        utility_row = utility_metrics[method]
        rows.append(
            [
                method_label(method),
                cell(
                    attacker_row["risk_weighted_leakage"],
                    attacker_cis.get((method, "risk_weighted_leakage")),
                ),
                cell(
                    utility_row["semantic_utility_score"],
                    utility_cis.get((method, "semantic_utility_score")),
                ),
                cell(
                    utility_row["llm_fact_preservation"],
                    utility_cis.get((method, "llm_fact_preservation")),
                ),
            ]
        )
    return rows


def llm_utility_rows(metrics_path: str, cis_path: str) -> list[list[str]]:
    metrics = by_method(read_csv(metrics_path))
    cis = ci_lookup(read_csv(cis_path))
    rows = []
    for method in ["direct", "blanket_qi", "rbqig_b4"]:
        row = metrics[method]
        rows.append(
            [
                method_label(method),
                cell(row["label_preservation"]),
                cell(row["llm_fact_preservation"], cis.get((method, "llm_fact_preservation"))),
                cell(row["semantic_utility_score"], cis.get((method, "semantic_utility_score"))),
            ]
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate paper-ready RB-QIG tables.")
    parser.add_argument("--out-md", default="paper/generated/tables.md")
    parser.add_argument("--out-tex", default="paper/generated/tables.tex")
    parser.add_argument("--synthetic-metrics", default="results/synthetic_100/metrics.csv")
    parser.add_argument("--synthetic-cis", default="results/synthetic_100/bootstrap_cis.csv")
    parser.add_argument("--llm-metrics", default="results/ratbench_d1_api_100/llm_attacker_metrics_with_llm_direct.csv")
    parser.add_argument("--llm-cis", default="results/ratbench_d1_api_100/llm_bootstrap_cis_with_llm_direct.csv")
    parser.add_argument("--blind-metrics", default="results/synthetic_30_blind_api/metrics.csv")
    parser.add_argument("--blind-cis", default="results/synthetic_30_blind_api/bootstrap_cis.csv")
    parser.add_argument("--blind-public-attacker-metrics", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_metrics.csv")
    parser.add_argument("--blind-public-attacker-cis", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_bootstrap_cis.csv")
    parser.add_argument("--blind-public-utility-metrics", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_metrics.csv")
    parser.add_argument("--blind-public-utility-cis", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_bootstrap_cis.csv")
    parser.add_argument("--llm-utility-metrics", default="results/synthetic_100/llm_utility_metrics.csv")
    parser.add_argument("--llm-utility-cis", default="results/synthetic_100/llm_utility_bootstrap_cis.csv")
    args = parser.parse_args()

    synthetic_headers = ["Method", "Risk-weighted leak", "Utility facts", "Token change"]
    llm_headers = ["Method", "Record compromise", "Exact attr leak", "Coarse attr leak", "Risk-weighted leak"]
    llm_utility_headers = ["Method", "Label preserved", "LLM fact preservation", "Semantic utility"]
    blind_headers = ["Method", "Risk-weighted leak", "Utility facts", "Token change"]
    blind_public_headers = ["Method", "LLM risk-weighted leak", "Semantic utility", "LLM fact preservation"]

    synthetic = main_synthetic_rows(args.synthetic_metrics, args.synthetic_cis)
    llm = ratbench_llm_rows(args.llm_metrics, args.llm_cis)
    llm_utility = llm_utility_rows(args.llm_utility_metrics, args.llm_utility_cis)
    blind = blind_rows(args.blind_metrics, args.blind_cis)
    blind_public = blind_public_rows(
        args.blind_public_attacker_metrics,
        args.blind_public_attacker_cis,
        args.blind_public_utility_metrics,
        args.blind_public_utility_cis,
    )

    md_parts = [
        "# Generated Paper Tables",
        "",
        "Cells are percentages. Brackets show bootstrap 95% confidence intervals.",
        "",
        "## Synthetic Controlled Benchmark",
        "",
        md_table(synthetic_headers, synthetic),
        "",
        "## RAT-Bench LLM Attacker",
        "",
        md_table(llm_headers, llm),
        "",
        "## Synthetic LLM Utility Judge",
        "",
        md_table(llm_utility_headers, llm_utility),
        "",
        "## Blind Public RAT-Bench Stress Test",
        "",
        md_table(blind_public_headers, blind_public),
        "",
        "## Blind Synthetic Diagnostic",
        "",
        md_table(blind_headers, blind),
        "",
    ]
    ensure_parent(args.out_md)
    Path(args.out_md).write_text("\n".join(md_parts), encoding="utf-8")

    tex_parts = [
        "% Generated by src/make_paper_tables.py. Percent values omit the percent sign.",
        latex_table(
            "Synthetic controlled benchmark. Brackets show bootstrap 95% confidence intervals.",
            "tab:synthetic",
            synthetic_headers,
            synthetic,
        ),
        "",
        latex_table(
            "RAT-Bench LLM attacker results. Brackets show bootstrap 95% confidence intervals.",
            "tab:ratbench-llm",
            llm_headers,
            llm,
        ),
        "",
        latex_table(
            "Synthetic LLM utility judge results. Brackets show bootstrap 95% confidence intervals.",
            "tab:llm-utility",
            llm_utility_headers,
            llm_utility,
        ),
        "",
        latex_table(
            "Blind public RAT-Bench stress test. Brackets show bootstrap 95% confidence intervals.",
            "tab:blind-public",
            blind_public_headers,
            blind_public,
        ),
        "",
    ]
    ensure_parent(args.out_tex)
    Path(args.out_tex).write_text("\n".join(tex_parts), encoding="utf-8")
    print(f"Wrote {args.out_md} and {args.out_tex}")


if __name__ == "__main__":
    main()
