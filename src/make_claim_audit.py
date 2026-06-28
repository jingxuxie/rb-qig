from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rbqig.io_utils import ensure_parent


@dataclass
class Claim:
    claim_id: str
    description: str
    source_paths: list[str]
    evidence: list[str]
    paper_snippets: list[str]
    interpretation: str


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def by_method(path: str | Path) -> dict[str, dict[str, str]]:
    return {row["method"]: row for row in read_csv(path)}


def metric_lookup(path: str | Path) -> dict[tuple[str, str], dict[str, str]]:
    return {(row["method"], row["metric"]): row for row in read_csv(path)}


def contrast_lookup(path: str | Path) -> dict[tuple[str, str], dict[str, str]]:
    return {(row["comparison"], row["metric"]): row for row in read_csv(path)}


def pct(value: Any, signed: bool = False) -> str:
    number = round(100.0 * float(value) + 1e-9, 1)
    if number == 0:
        number = 0.0
    if signed and number > 0:
        return f"+{number:.1f}"
    return f"{number:.1f}"


def ci(row: dict[str, str], signed: bool = False) -> str:
    low = pct(row["ci_low"], signed=signed)
    high = pct(row["ci_high"], signed=signed)
    return f"[{low}, {high}]"


def metric_value(
    metrics: dict[str, dict[str, str]],
    cis: dict[tuple[str, str], dict[str, str]],
    method: str,
    metric: str,
) -> str:
    ci_row = cis[(method, metric)]
    value = pct(ci_row["mean"])
    interval = ci(ci_row)
    return f"{value}% {interval}"


def contrast_value(
    contrasts: dict[tuple[str, str], dict[str, str]],
    comparison: str,
    metric: str,
    signed_mean: bool = True,
    signed_ci: bool = False,
) -> str:
    row = contrasts[(comparison, metric)]
    value = pct(row["mean_diff"], signed=signed_mean)
    interval = ci(row, signed=signed_ci)
    return f"{value} points {interval}"


def extract_report_pct(path: str | Path, label: str) -> str:
    text = Path(path).read_text(encoding="utf-8")
    match = re.search(rf"{re.escape(label)}:\s+([0-9.]+)%", text)
    if not match:
        raise ValueError(f"Could not find {label!r} in {path}")
    return f"{float(match.group(1)):.1f}%"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def check_snippets(paper_text: str, snippets: list[str]) -> tuple[str, list[str]]:
    normalized = normalize(paper_text)
    missing = [snippet for snippet in snippets if normalize(snippet) not in normalized]
    if missing:
        return "MISSING", missing
    return "PASS", []


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        escaped = [cell.replace("|", "\\|").replace("\n", "<br>") for cell in row]
        lines.append("| " + " | ".join(escaped) + " |")
    return "\n".join(lines)


def build_claims(args: argparse.Namespace) -> list[Claim]:
    synthetic_metrics = by_method(args.synthetic_metrics)
    synthetic_cis = metric_lookup(args.synthetic_cis)
    synthetic_contrasts = contrast_lookup(args.synthetic_contrasts)

    synthetic_utility_metrics = by_method(args.synthetic_utility_metrics)
    synthetic_utility_cis = metric_lookup(args.synthetic_utility_cis)
    synthetic_utility_contrasts = contrast_lookup(args.synthetic_utility_contrasts)

    ratbench_llm_metrics = by_method(args.ratbench_llm_metrics)
    ratbench_llm_cis = metric_lookup(args.ratbench_llm_cis)
    ratbench_llm_contrasts = contrast_lookup(args.ratbench_llm_contrasts)

    d2_metrics = by_method(args.d2_llm_metrics)
    d2_cis = metric_lookup(args.d2_llm_cis)

    stronger_metrics = by_method(args.stronger_llm_metrics)
    stronger_cis = metric_lookup(args.stronger_llm_cis)

    blind_metrics = by_method(args.blind_metrics)
    blind_cis = metric_lookup(args.blind_cis)
    blind_contrasts = contrast_lookup(args.blind_contrasts)

    blind_llm_metrics = by_method(args.blind_llm_metrics)
    blind_llm_cis = metric_lookup(args.blind_llm_cis)
    blind_llm_contrasts = contrast_lookup(args.blind_llm_contrasts)

    blind_utility_metrics = by_method(args.blind_utility_metrics)
    blind_utility_cis = metric_lookup(args.blind_utility_cis)
    blind_utility_contrasts = contrast_lookup(args.blind_utility_contrasts)
    blind_specificity_contrasts = contrast_lookup(args.blind_specificity_contrasts)

    blind_synth_cis = metric_lookup(args.blind_synth_cis)

    tab_metrics = by_method(args.tab_metrics)
    tab_cis = metric_lookup(args.tab_cis)
    tab_contrasts = contrast_lookup(args.tab_contrasts)
    tab_legal_utility_cis = metric_lookup(args.tab_legal_utility_cis)
    tab_legal_utility_contrasts = contrast_lookup(args.tab_legal_utility_contrasts)
    tab_specificity_contrasts = contrast_lookup(args.tab_specificity_contrasts)

    pattern_ratbench_metrics = by_method(args.pattern_ratbench_metrics)
    pattern_ratbench_cis = metric_lookup(args.pattern_ratbench_cis)
    pattern_tab_metrics = by_method(args.pattern_tab_metrics)
    pattern_tab_cis = metric_lookup(args.pattern_tab_cis)

    raw_blind_coverage = extract_report_pct(args.raw_blind_coverage, "Span coverage")
    v2_blind_coverage = extract_report_pct(args.v2_blind_coverage, "Span coverage")

    return [
        Claim(
            "C1",
            "Controlled synthetic frontier headline.",
            [args.synthetic_metrics, args.synthetic_cis],
            [
                f"RB-QIG balanced risk-weighted leakage: {metric_value(synthetic_metrics, synthetic_cis, 'rbqig_b4', 'risk_weighted_leakage')}",
                f"RB-QIG balanced utility facts: {metric_value(synthetic_metrics, synthetic_cis, 'rbqig_b4', 'utility_fact_preservation')}",
                f"Blanket QI utility facts: {metric_value(synthetic_metrics, synthetic_cis, 'blanket_qi', 'utility_fact_preservation')}",
            ],
            [
                "23.6\\% [22.9, 24.5]",
                "71.7\\% [70.8, 72.4]",
                "43.3\\% [39.9, 46.8]",
            ],
            "Supports the large utility-preservation claim only in the controlled setting.",
        ),
        Claim(
            "C2",
            "Synthetic RB-QIG utility advantage over blanket redaction.",
            [args.synthetic_contrasts],
            [
                "RB-QIG balanced minus blanket utility facts: "
                + contrast_value(synthetic_contrasts, "rbqig_b4_minus_blanket_qi", "utility_fact_preservation")
            ],
            ["+28.3 points [25.2, 31.6]"],
            "This is the strongest utility result and should stay scoped to synthetic utility facts.",
        ),
        Claim(
            "C3",
            "Synthetic LLM utility judge gives only a modest semantic edge.",
            [args.synthetic_utility_metrics, args.synthetic_utility_cis, args.synthetic_utility_contrasts],
            [
                f"RB-QIG balanced semantic utility: {metric_value(synthetic_utility_metrics, synthetic_utility_cis, 'rbqig_b4', 'semantic_utility_score')}",
                f"Blanket QI semantic utility: {metric_value(synthetic_utility_metrics, synthetic_utility_cis, 'blanket_qi', 'semantic_utility_score')}",
                "RB-QIG balanced minus blanket semantic utility: "
                + contrast_value(synthetic_utility_contrasts, "rbqig_b4_minus_blanket_qi", "semantic_utility_score"),
            ],
            ["+2.6 points [0.6, 4.8]"],
            "Prevents overclaiming from the deterministic synthetic utility metric.",
        ),
        Claim(
            "C4",
            "Target-aware RAT-Bench LLM attacker headline.",
            [args.ratbench_llm_metrics, args.ratbench_llm_cis],
            [
                f"Direct risk-weighted leakage: {metric_value(ratbench_llm_metrics, ratbench_llm_cis, 'direct', 'risk_weighted_leakage')}",
                f"Naive LLM sanitizer risk-weighted leakage: {metric_value(ratbench_llm_metrics, ratbench_llm_cis, 'llm_direct', 'risk_weighted_leakage')}",
                f"RB-QIG balanced risk-weighted leakage: {metric_value(ratbench_llm_metrics, ratbench_llm_cis, 'rbqig_b4', 'risk_weighted_leakage')}",
            ],
            [
                "78.0\\% [73.4, 82.5]",
                "46.0\\%",
                "5.7\\% [3.2, 8.8]",
            ],
            "Supports residual-risk reduction relative to direct and naive LLM redaction.",
        ),
        Claim(
            "C5",
            "Target-aware paired LLM-attacker reductions and blanket tie.",
            [args.ratbench_llm_contrasts],
            [
                "Direct minus RB-QIG balanced: "
                + contrast_value(ratbench_llm_contrasts, "direct_minus_rbqig_b4", "risk_weighted_leakage"),
                "Naive LLM sanitizer minus RB-QIG balanced: "
                + contrast_value(ratbench_llm_contrasts, "llm_direct_minus_rbqig_b4", "risk_weighted_leakage"),
                "RB-QIG balanced minus blanket QI: "
                + contrast_value(ratbench_llm_contrasts, "rbqig_b4_minus_blanket_qi", "risk_weighted_leakage"),
            ],
            [
                "72.2 points [67.0, 77.4]",
                "40.2 points [33.1, 47.1]",
                "0.5 points [-2.6, 3.6]",
            ],
            "The CI crossing zero for RB-QIG minus blanket supports the tied-privacy caveat.",
        ),
        Claim(
            "C6",
            "Difficulty-2 smoke maintains the same qualitative ordering.",
            [args.d2_llm_metrics, args.d2_llm_cis],
            [
                f"Direct risk-weighted leakage: {metric_value(d2_metrics, d2_cis, 'direct', 'risk_weighted_leakage')}",
                f"Naive LLM sanitizer risk-weighted leakage: {metric_value(d2_metrics, d2_cis, 'llm_direct', 'risk_weighted_leakage')}",
                f"RB-QIG balanced risk-weighted leakage: {metric_value(d2_metrics, d2_cis, 'rbqig_b4', 'risk_weighted_leakage')}",
            ],
            ["70.8\\% and 56.9\\%", "13.1\\% [3.3, 25.0]"],
            "Robustness smoke only; n=30 is not a replacement for the main 100-row table.",
        ),
        Claim(
            "C7",
            "Stronger-attacker smoke preserves the main ordering.",
            [args.stronger_llm_metrics, args.stronger_llm_cis],
            [
                f"Direct risk-weighted leakage: {metric_value(stronger_metrics, stronger_cis, 'direct', 'risk_weighted_leakage')}",
                f"RB-QIG balanced risk-weighted leakage: {metric_value(stronger_metrics, stronger_cis, 'rbqig_b4', 'risk_weighted_leakage')}",
                f"Blanket QI risk-weighted leakage: {metric_value(stronger_metrics, stronger_cis, 'blanket_qi', 'risk_weighted_leakage')}",
            ],
            ["18.0\\% versus 77.3\\%"],
            "Robustness smoke only; n=20 is intentionally small.",
        ),
        Claim(
            "C8",
            "Blind extractor coverage improves with the v2 backstop.",
            [args.raw_blind_coverage, args.v2_blind_coverage],
            [
                f"Raw blind span coverage: {raw_blind_coverage}",
                f"V2 backstopped blind span coverage: {v2_blind_coverage}",
            ],
            ["72.8\\%", "99.6\\%"],
            "Supports the extraction-bottleneck discussion without claiming deployment readiness.",
        ),
        Claim(
            "C9",
            "Blind deterministic stress-test reduction and deterministic blanket gap.",
            [args.blind_metrics, args.blind_cis, args.blind_contrasts],
            [
                f"Direct risk-weighted leakage: {metric_value(blind_metrics, blind_cis, 'direct', 'risk_weighted_leakage')}",
                f"RB-QIG balanced risk-weighted leakage: {metric_value(blind_metrics, blind_cis, 'rbqig_b4', 'risk_weighted_leakage')}",
                "Direct minus RB-QIG balanced: "
                + contrast_value(blind_contrasts, "direct_minus_rbqig_b4", "risk_weighted_leakage"),
                "RB-QIG balanced minus blanket QI: "
                + contrast_value(blind_contrasts, "rbqig_b4_minus_blanket_qi", "risk_weighted_leakage"),
            ],
            [
                "94.3\\% [91.3, 96.8]",
                "5.4\\% [2.8, 8.5]",
                "88.9 points [85.0, 92.5]",
                "2.3 points [0.6, 4.9]",
            ],
            "Shows strong direct-to-RB-QIG reduction but deterministic scoring still favors blanket QI.",
        ),
        Claim(
            "C10",
            "Blind LLM-attacker stress test ties RB-QIG with blanket QI.",
            [args.blind_llm_metrics, args.blind_llm_cis, args.blind_llm_contrasts],
            [
                f"Direct risk-weighted leakage: {metric_value(blind_llm_metrics, blind_llm_cis, 'direct', 'risk_weighted_leakage')}",
                f"RB-QIG balanced risk-weighted leakage: {metric_value(blind_llm_metrics, blind_llm_cis, 'rbqig_b4', 'risk_weighted_leakage')}",
                "RB-QIG balanced minus blanket QI: "
                + contrast_value(blind_llm_contrasts, "rbqig_b4_minus_blanket_qi", "risk_weighted_leakage"),
            ],
            [
                "78.1\\% [73.3, 82.9]",
                "6.4\\% [3.9, 9.1]",
                "-0.5 points [-2.5, 1.5]",
            ],
            "This is the strongest deployment-style privacy claim and includes the blanket-tie caveat.",
        ),
        Claim(
            "C11",
            "Public blind utility judge does not support an RB-QIG utility edge.",
            [args.blind_utility_metrics, args.blind_utility_cis, args.blind_utility_contrasts],
            [
                f"Blanket QI semantic utility: {metric_value(blind_utility_metrics, blind_utility_cis, 'blanket_qi', 'semantic_utility_score')}",
                f"RB-QIG balanced semantic utility: {metric_value(blind_utility_metrics, blind_utility_cis, 'rbqig_b4', 'semantic_utility_score')}",
                "RB-QIG balanced minus blanket semantic utility: "
                + contrast_value(
                    blind_utility_contrasts,
                    "rbqig_b4_minus_blanket_qi",
                    "semantic_utility_score",
                    signed_mean=False,
                ),
            ],
            ["-0.4 semantic-utility points [-4.2, 3.4]"],
            "Important negative/caveat claim: public utility advantage is not established.",
        ),
        Claim(
            "C12",
            "Blind synthetic diagnostic remains a limitation result.",
            [args.blind_synth_cis],
            [
                f"RB-QIG balanced utility facts: {metric_value({'rbqig_b4': {}}, blind_synth_cis, 'rbqig_b4', 'utility_fact_preservation')}",
                f"RB-QIG balanced risk-weighted leakage: {metric_value({'rbqig_b4': {}}, blind_synth_cis, 'rbqig_b4', 'risk_weighted_leakage')}",
            ],
            ["43.3\\% [35.0, 51.7]", "5.2\\% [1.7, 9.7]"],
            "Supports the limitation paragraph; this should not be framed as solved blind extraction.",
        ),
        Claim(
            "C13",
            "TAB ECHR deterministic screen is cross-domain residual-risk support.",
            [
                args.tab_metrics,
                args.tab_cis,
                args.tab_contrasts,
                args.tab_legal_utility_cis,
                args.tab_legal_utility_contrasts,
            ],
            [
                f"Direct risk-weighted leakage: {metric_value(tab_metrics, tab_cis, 'direct', 'risk_weighted_leakage')}",
                f"RB-QIG balanced risk-weighted leakage: {metric_value(tab_metrics, tab_cis, 'rbqig_b4', 'risk_weighted_leakage')}",
                "Direct minus RB-QIG balanced: "
                + contrast_value(tab_contrasts, "direct_minus_rbqig_b4", "risk_weighted_leakage"),
                "RB-QIG balanced minus blanket QI: "
                + contrast_value(tab_contrasts, "rbqig_b4_minus_blanket_qi", "risk_weighted_leakage"),
                f"RB-QIG balanced legal-task utility: {metric_value({'rbqig_b4': {}}, tab_legal_utility_cis, 'rbqig_b4', 'legal_task_utility')}",
                f"Blanket QI legal-task utility: {metric_value({'blanket_qi': {}}, tab_legal_utility_cis, 'blanket_qi', 'legal_task_utility')}",
                "RB-QIG balanced minus blanket legal-task utility: "
                + contrast_value(
                    tab_legal_utility_contrasts,
                    "rbqig_b4_minus_blanket_qi",
                    "legal_task_utility",
                    signed_mean=False,
                ),
            ],
            [
                "99.8\\% [99.4, 100.0]",
                "12.3\\% [9.2, 15.7]",
                "68.0\\% [62.0, 74.0]",
                "0.0 points [-10.0, 10.0]",
            ],
            "Supports a second-domain residual-risk diagnostic and an inconclusive TAB legal-utility caveat.",
        ),
        Claim(
            "C14",
            "Presidio-style pattern baseline is a practical lower-bound diagnostic.",
            [args.pattern_ratbench_metrics, args.pattern_ratbench_cis, args.pattern_tab_metrics, args.pattern_tab_cis],
            [
                f"RAT-Bench Presidio-pattern direct identifier leakage: {metric_value(pattern_ratbench_metrics, pattern_ratbench_cis, 'presidio_pattern', 'direct_identifier_leakage')}",
                f"RAT-Bench Presidio-pattern risk-weighted leakage: {metric_value(pattern_ratbench_metrics, pattern_ratbench_cis, 'presidio_pattern', 'risk_weighted_leakage')}",
                f"TAB Presidio-pattern direct identifier leakage: {metric_value(pattern_tab_metrics, pattern_tab_cis, 'presidio_pattern', 'direct_identifier_leakage')}",
            ],
            [
                "37.0\\% [28.0, 46.0]",
                "85.0\\% [80.6, 89.0]",
                "100.0\\%",
            ],
            "Supports the practical-baseline caveat without claiming full Presidio coverage.",
        ),
        Claim(
            "C15",
            "Annotation-derived public specificity shows a small RB-QIG edge over blanket placeholders.",
            [args.blind_specificity_contrasts, args.tab_specificity_contrasts],
            [
                "Blind RAT-Bench RB-QIG balanced minus blanket specificity: "
                + contrast_value(
                    blind_specificity_contrasts,
                    "rbqig_b4_minus_blanket_qi",
                    "utility_weighted_specificity",
                ),
                "TAB RB-QIG balanced minus blanket specificity: "
                + contrast_value(
                    tab_specificity_contrasts,
                    "rbqig_b4_minus_blanket_qi",
                    "utility_weighted_specificity",
                ),
            ],
            [
                "+6.8 points [4.7, 9.2]",
                "+6.2 [5.5, 6.9]",
            ],
            "Supports a narrow public utility diagnostic while preserving the LLM-utility caveat.",
        ),
    ]


def write_audit(args: argparse.Namespace, claims: list[Claim]) -> None:
    paper_text = Path(args.paper_tex).read_text(encoding="utf-8")
    rows = []
    detail_parts = [
        "# Paper Claim Audit",
        "",
        "Generated from local CSV/report artifacts. No API calls are made.",
        "",
    ]

    pass_count = 0
    for claim in claims:
        status, missing = check_snippets(paper_text, claim.paper_snippets)
        if status == "PASS":
            pass_count += 1
        rows.append(
            [
                claim.claim_id,
                claim.description,
                status,
                claim.interpretation,
            ]
        )
        detail_parts.extend(
            [
                f"## {claim.claim_id}: {claim.description}",
                "",
                f"Paper snippet check: **{status}**",
                "",
                "Sources:",
                *[f"- `{path}`" for path in claim.source_paths],
                "",
                "Evidence:",
                *[f"- {item}" for item in claim.evidence],
                "",
            ]
        )
        if missing:
            detail_parts.extend(["Missing snippets:", *[f"- `{snippet}`" for snippet in missing], ""])

    summary = [
        f"Summary: {pass_count}/{len(claims)} audited claim groups have matching paper snippets.",
        "",
        md_table(["Claim", "Description", "Paper check", "Interpretation"], rows),
        "",
    ]
    ensure_parent(args.out)
    Path(args.out).write_text("\n".join(detail_parts[:4] + summary + detail_parts[4:]), encoding="ascii")
    print(f"Wrote {args.out} ({pass_count}/{len(claims)} snippet checks passed)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an audit tying paper claims to local result artifacts.")
    parser.add_argument("--out", default="paper/CLAIM_AUDIT.md")
    parser.add_argument("--paper-tex", default="paper/main.tex")
    parser.add_argument("--synthetic-metrics", default="results/synthetic_100/metrics.csv")
    parser.add_argument("--synthetic-cis", default="results/synthetic_100/bootstrap_cis.csv")
    parser.add_argument("--synthetic-contrasts", default="results/synthetic_100/bootstrap_contrasts.csv")
    parser.add_argument("--synthetic-utility-metrics", default="results/synthetic_100/llm_utility_metrics.csv")
    parser.add_argument("--synthetic-utility-cis", default="results/synthetic_100/llm_utility_bootstrap_cis.csv")
    parser.add_argument("--synthetic-utility-contrasts", default="results/synthetic_100/llm_utility_bootstrap_contrasts.csv")
    parser.add_argument("--ratbench-llm-metrics", default="results/ratbench_d1_api_100/llm_attacker_metrics_with_llm_direct.csv")
    parser.add_argument("--ratbench-llm-cis", default="results/ratbench_d1_api_100/llm_bootstrap_cis_with_llm_direct.csv")
    parser.add_argument("--ratbench-llm-contrasts", default="results/ratbench_d1_api_100/llm_bootstrap_contrasts_with_llm_direct.csv")
    parser.add_argument("--d2-llm-metrics", default="results/ratbench_d2_api_30/llm_attacker_metrics_with_llm_direct.csv")
    parser.add_argument("--d2-llm-cis", default="results/ratbench_d2_api_30/llm_bootstrap_cis_with_llm_direct.csv")
    parser.add_argument("--stronger-llm-metrics", default="results/ratbench_d1_api_100/llm_attacker_stronger20_metrics.csv")
    parser.add_argument("--stronger-llm-cis", default="results/ratbench_d1_api_100/llm_attacker_stronger20_bootstrap_cis.csv")
    parser.add_argument("--raw-blind-coverage", default="results/ratbench_d1_blind_api_100/blind_coverage_report.md")
    parser.add_argument("--v2-blind-coverage", default="results/ratbench_d1_blind_backstop_v2_api_100/blind_coverage_report.md")
    parser.add_argument("--blind-metrics", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/metrics.csv")
    parser.add_argument("--blind-cis", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_cis.csv")
    parser.add_argument("--blind-contrasts", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_contrasts.csv")
    parser.add_argument("--blind-llm-metrics", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_metrics.csv")
    parser.add_argument("--blind-llm-cis", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_bootstrap_cis.csv")
    parser.add_argument("--blind-llm-contrasts", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_bootstrap_contrasts.csv")
    parser.add_argument("--blind-utility-metrics", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_metrics.csv")
    parser.add_argument("--blind-utility-cis", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_bootstrap_cis.csv")
    parser.add_argument("--blind-utility-contrasts", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_bootstrap_contrasts.csv")
    parser.add_argument("--blind-specificity-contrasts", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_bootstrap_contrasts.csv")
    parser.add_argument("--blind-synth-cis", default="results/synthetic_30_blind_api/bootstrap_cis.csv")
    parser.add_argument("--tab-metrics", default="results/tab_echr_dev_30/metrics.csv")
    parser.add_argument("--tab-cis", default="results/tab_echr_dev_30/bootstrap_cis.csv")
    parser.add_argument("--tab-contrasts", default="results/tab_echr_dev_30/bootstrap_contrasts.csv")
    parser.add_argument("--tab-legal-utility-cis", default="results/tab_echr_dev_30/llm_legal_utility_10_bootstrap_cis.csv")
    parser.add_argument("--tab-legal-utility-contrasts", default="results/tab_echr_dev_30/llm_legal_utility_10_bootstrap_contrasts.csv")
    parser.add_argument("--tab-specificity-contrasts", default="results/tab_echr_dev_30/qi_specificity_bootstrap_contrasts.csv")
    parser.add_argument("--pattern-ratbench-metrics", default="results/presidio_pattern_ratbench_d1_100/metrics.csv")
    parser.add_argument("--pattern-ratbench-cis", default="results/presidio_pattern_ratbench_d1_100/bootstrap_cis.csv")
    parser.add_argument("--pattern-tab-metrics", default="results/presidio_pattern_tab_echr_dev_30/metrics.csv")
    parser.add_argument("--pattern-tab-cis", default="results/presidio_pattern_tab_echr_dev_30/bootstrap_cis.csv")
    args = parser.parse_args()

    write_audit(args, build_claims(args))


if __name__ == "__main__":
    main()
