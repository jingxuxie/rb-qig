from __future__ import annotations

from pathlib import Path

from .io_utils import ensure_parent, pct
from .plots import LABELS


def _metric(metrics: list[dict], method: str, key: str) -> float:
    for row in metrics:
        if row["method"] == method:
            return float(row[key])
    return 0.0


def write_pilot_report(path: str | Path, metrics: list[dict], n: int, seed: int) -> None:
    direct_leak = _metric(metrics, "direct", "risk_weighted_leakage")
    rb_leak = _metric(metrics, "rbqig_b4", "risk_weighted_leakage")
    blanket_util = _metric(metrics, "blanket_qi", "utility_fact_preservation")
    rb_util = _metric(metrics, "rbqig_b4", "utility_fact_preservation")

    lines = [
        "# RB-QIG Synthetic Pilot Report",
        "",
        f"Records: {n}",
        f"Seed: {seed}",
        "API calls: 0",
        "",
        "## Main Table",
        "",
        "| Method | Direct ID leak | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Label preservation | Utility facts | Token change |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in metrics:
        lines.append(
            "| {method} | {direct} | {comp} | {exact} | {coarse} | {weighted} | {label} | {facts} | {token} |".format(
                method=LABELS.get(row["method"], row["method"]),
                direct=pct(float(row["direct_identifier_leakage"])),
                comp=pct(float(row["record_compromise_rate"])),
                exact=pct(float(row["exact_attribute_leakage"])),
                coarse=pct(float(row["coarse_attribute_leakage"])),
                weighted=pct(float(row["risk_weighted_leakage"])),
                label=pct(float(row["label_preservation"])),
                facts=pct(float(row["utility_fact_preservation"])),
                token=pct(float(row["token_change_rate"])),
            )
        )

    lines.extend(
        [
            "",
            "## Fast Interpretation",
            "",
            f"- Direct redaction leaves {pct(direct_leak)} risk-weighted quasi-identifier leakage in this controlled pilot.",
            f"- RB-QIG balanced leaves {pct(rb_leak)} risk-weighted leakage while preserving {pct(rb_util)} of utility facts.",
            f"- Blanket QI redaction preserves {pct(blanket_util)} of utility facts.",
            "",
            "This supports the planned paper framing only as a synthetic control: direct PII removal is insufficient, blanket QI redaction damages utility, and risk-budgeted generalization exposes a tunable privacy-utility tradeoff.",
            "",
            "## Important Limitation",
            "",
            "The current run uses synthetic ground-truth quasi-identifier spans. It validates the pipeline mechanics but not extraction robustness. The next publishable step is an API-extracted or public-benchmark run on RAT-Bench records.",
        ]
    )
    ensure_parent(path)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_qualitative_examples(path: str | Path, transformed: list[dict], limit: int = 3) -> None:
    by_id: dict[str, dict[str, dict]] = {}
    for row in transformed:
        by_id.setdefault(row["id"], {})[row["method"]] = row

    lines = ["# Qualitative Examples", ""]
    for record_id, methods in list(by_id.items())[:limit]:
        original = methods.get("none")
        if not original:
            continue
        lines.extend([f"## {record_id}: {original['domain']}", ""])
        lines.extend(["### Original", "", original["original_text"], ""])
        for method in ["direct", "blanket_qi", "rbqig_b4"]:
            row = methods.get(method)
            if not row:
                continue
            lines.extend(
                [
                    f"### {LABELS.get(method, method)}",
                    "",
                    row["transformed_text"],
                    "",
                    f"Document risk: {row['doc_risk_before']} -> {row['doc_risk_after']}",
                    "",
                ]
            )
        lines.append("---")
        lines.append("")
    ensure_parent(path)
    Path(path).write_text("\n".join(lines), encoding="utf-8")

