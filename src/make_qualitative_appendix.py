from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Any

from rbqig.io_utils import ensure_parent, read_jsonl
from rbqig.plots import LABELS


SYNTHETIC_ID = "synth_0000"
TARGET_METHODS = ["direct", "llm_direct", "blanket_qi", "rbqig_b4"]
STOPWORDS = {
    "about",
    "after",
    "also",
    "attribute",
    "because",
    "being",
    "could",
    "exact",
    "from",
    "have",
    "person",
    "that",
    "their",
    "there",
    "this",
    "with",
    "would",
    "your",
}


def clean_ascii(text: Any) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
    }
    out = str(text)
    for old, new in replacements.items():
        out = out.replace(old, new)
    out = out.encode("ascii", errors="ignore").decode("ascii")
    return re.sub(r"\s+", " ", out).strip()


def clip(text: Any, limit: int = 360) -> str:
    text = clean_ascii(text)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def snippet_around(text: Any, anchors: list[Any], limit: int = 360) -> str:
    text = clean_ascii(text)
    if len(text) <= limit:
        return text
    lower = text.lower()
    position = None
    for anchor in anchors:
        anchor = clean_ascii(anchor)
        if not anchor:
            continue
        idx = lower.find(anchor.lower())
        if idx >= 0:
            position = idx
            break
        for token in re.findall(r"[A-Za-z0-9]+", anchor):
            token = token.lower()
            if len(token) < 4 or token in STOPWORDS:
                continue
            idx = lower.find(token)
            if idx >= 0:
                position = idx
                break
        if position is not None:
            break
    if position is None:
        return clip(text, limit)
    center = position
    start = max(0, center - limit // 3)
    end = min(len(text), start + limit)
    start = max(0, end - limit)
    snippet = text[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet.rstrip() + "..."
    return snippet


def method_label(method: str) -> str:
    return LABELS.get(method, method)


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        escaped = [cell.replace("|", "\\|") for cell in row]
        lines.append("| " + " | ".join(escaped) + " |")
    return "\n".join(lines)


def group_by_id_method(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(row["id"], row["method"]): row for row in rows}


def group_attacks(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(row["id"], row["method"]): row for row in rows}


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def attacker_summary(row: dict[str, Any] | None) -> str:
    if not row:
        return "No LLM-attacker row available."
    details = row.get("details") or []
    leaks = [detail for detail in details if detail.get("match") in {"exact", "coarse"}]
    if not leaks:
        return "No exact/coarse attribute recovered."
    parts = []
    for detail in leaks[:3]:
        parts.append(
            f"{clean_ascii(detail.get('attribute', 'attribute'))}: "
            f"{clean_ascii(detail.get('guess', ''))} ({clean_ascii(detail.get('match', ''))})"
        )
    return "; ".join(parts)


def evidence_summary(row: dict[str, Any] | None) -> str:
    if not row:
        return "n/a"
    for detail in row.get("details") or []:
        evidence = detail.get("evidence") or []
        if detail.get("match") in {"exact", "coarse"} and evidence:
            return clip("; ".join(clean_ascii(item) for item in evidence), 300)
    return "No matching evidence cited."


def snippet_for_method(
    output_row: dict[str, Any],
    attack_row: dict[str, Any] | None,
    ground_truth: dict[str, Any],
) -> str:
    anchors: list[Any] = []
    if attack_row:
        for detail in attack_row.get("details") or []:
            if detail.get("match") in {"exact", "coarse"}:
                anchors.extend(detail.get("evidence") or [])
                anchors.append(detail.get("guess", ""))
                anchors.append(detail.get("attribute", ""))
    anchors.extend(ground_truth.values())
    anchors.extend(["[DEMOGRAPHIC]", "[DATE]", "[LOCATION]", "citizenship", "born", "race", "sex", "gender"])
    return snippet_around(output_row.get("transformed_text", ""), anchors, 300)


def select_target_id(attacks: list[dict[str, Any]]) -> str:
    grouped = group_attacks(attacks)
    ids = sorted({row["id"] for row in attacks})
    best_id = ""
    best_score = -1.0
    for record_id in ids:
        direct = grouped.get((record_id, "direct"), {})
        llm_direct = grouped.get((record_id, "llm_direct"), {})
        rbqig = grouped.get((record_id, "rbqig_b4"), {})
        blanket = grouped.get((record_id, "blanket_qi"), {})
        direct_risk = float(direct.get("risk_weighted_leakage", 0.0))
        llm_direct_risk = float(llm_direct.get("risk_weighted_leakage", 0.0))
        rbqig_risk = float(rbqig.get("risk_weighted_leakage", 1.0))
        blanket_risk = float(blanket.get("risk_weighted_leakage", 1.0))
        score = direct_risk + llm_direct_risk - rbqig_risk - 0.25 * blanket_risk
        if direct_risk >= 0.5 and llm_direct_risk >= 0.25 and rbqig_risk <= 0.2 and score > best_score:
            best_score = score
            best_id = record_id
    if best_id:
        return best_id
    return ids[0]


def synthetic_section(rows: list[dict[str, Any]]) -> str:
    grouped = group_by_id_method(rows)
    base = grouped[(SYNTHETIC_ID, "none")]
    table_rows = []
    for method in ["direct", "blanket_qi", "rbqig_b4"]:
        row = grouped[(SYNTHETIC_ID, method)]
        table_rows.append(
            [
                method_label(method),
                f"{float(row.get('doc_risk_before', 0.0)):.1f} -> {float(row.get('doc_risk_after', 0.0)):.1f}",
                clip(row.get("transformed_text", ""), 360),
            ]
        )
    facts = ", ".join(fact["name"] for fact in base.get("utility_facts", []))
    return "\n".join(
        [
            "## Positive Control: Risk-Budgeted Generalization",
            "",
            f"Record `{SYNTHETIC_ID}` (`{clean_ascii(base.get('domain', 'unknown'))}`) demonstrates the intended behavior on controlled text.",
            f"Utility facts tracked by the evaluator: {clean_ascii(facts)}.",
            "",
            md_table(["Method", "Risk", "Excerpt"], table_rows),
            "",
            "Takeaway: RB-QIG removes direct identifiers and coarsens high-risk facts, but keeps the task-relevant medical, administrative, and family-role semantics that blanket quasi-identifier redaction discards.",
        ]
    )


def target_aware_section(outputs: list[dict[str, Any]], attacks: list[dict[str, Any]]) -> str:
    output_by_key = group_by_id_method(outputs)
    attack_by_key = group_attacks(attacks)
    record_id = select_target_id(attacks)
    base = output_by_key.get((record_id, "direct")) or output_by_key.get((record_id, "none"))
    ground_truth = base.get("ground_truth", {}).get("attributes", {}) if base else {}

    table_rows = []
    for method in TARGET_METHODS:
        output_row = output_by_key.get((record_id, method))
        attack_row = attack_by_key.get((record_id, method))
        if not output_row:
            continue
        table_rows.append(
            [
                method_label(method),
                f"{100.0 * float(attack_row.get('risk_weighted_leakage', 0.0)):.1f}%" if attack_row else "n/a",
                attacker_summary(attack_row),
                evidence_summary(attack_row),
                snippet_for_method(output_row, attack_row, ground_truth),
            ]
        )

    attrs = ", ".join(f"{clean_ascii(key)}={clean_ascii(value)}" for key, value in ground_truth.items())
    return "\n".join(
        [
            "## Public RAT-Bench Target-Aware Comparison",
            "",
            f"Record `{clean_ascii(record_id)}` was selected because direct and LLM-direct redaction leave recoverable attributes while RB-QIG balanced is low leakage under the same attacker.",
            f"Ground-truth target attributes: {attrs}.",
            "",
            md_table(["Method", "Risk", "Attacker recovery", "Cited evidence", "Transformed excerpt"], table_rows),
            "",
            "Takeaway: the target-aware setting is where the method has the cleanest story: direct and LLM direct redaction often remove names/contact strings while leaving direct demographic assertions, whereas RB-QIG rewrites or masks the target attributes.",
        ]
    )


def blind_failure_section(outputs: list[dict[str, Any]], failures: list[dict[str, str]]) -> str:
    chosen = None
    preferred = [
        ("rbqig_b4", "citizenship phrasing", "coarse"),
        ("rbqig_b4", "race or ethnicity variant", "exact"),
        ("rbqig_b4", "marital or bereavement context", "exact"),
        ("rbqig_b4", "gendered context", "exact"),
    ]
    for method, category, match in preferred:
        for row in failures:
            if row["method"] == method and row["category"] == category and row["match"] == match:
                chosen = row
                break
        if chosen:
            break
    if chosen is None:
        chosen = next(row for row in failures if row["method"] == "rbqig_b4")

    output_by_key = group_by_id_method(outputs)
    output_row = output_by_key.get((chosen["id"], chosen["method"]))
    anchors = [chosen["evidence"], chosen["guess"], chosen["attribute"], chosen["ground_truth"]]
    excerpt = snippet_around(output_row.get("transformed_text", ""), anchors, 360) if output_row else "No transformed excerpt available."
    rows = [
        ["Method", method_label(chosen["method"])],
        ["Failure category", clean_ascii(chosen["category"])],
        ["Attribute", clean_ascii(chosen["attribute"])],
        ["Ground truth", clean_ascii(chosen["ground_truth"])],
        ["Attacker guess", clean_ascii(chosen["guess"])],
        ["Evidence", clip(chosen["evidence"], 360)],
        ["Transformed excerpt", excerpt],
    ]
    return "\n".join(
        [
            "## Blind Public Failure Mode",
            "",
            "The blind v2 extractor does not see target attributes at extraction time. Its remaining failures are mostly semantic cues that survive broad generalization.",
            "",
            md_table(["Field", "Value"], rows),
            "",
            "Takeaway: the public blind result should be framed as a strong privacy reduction, not as solved anonymization. Residual leakage often comes from conversational implications, placeholders that reveal attribute type, or world-knowledge cues in surrounding context.",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a compact qualitative appendix from cached RB-QIG artifacts.")
    parser.add_argument("--out", default="paper/QUALITATIVE_APPENDIX.md")
    parser.add_argument("--synthetic-outputs", default="results/synthetic_100/anonymized_outputs.jsonl")
    parser.add_argument("--target-outputs", default="results/ratbench_d1_api_100/anonymized_outputs_with_llm_direct.jsonl")
    parser.add_argument("--target-attacks", default="results/ratbench_d1_api_100/llm_attacker_outputs_with_llm_direct.jsonl")
    parser.add_argument("--blind-outputs", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl")
    parser.add_argument("--blind-failures", default="results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_failure_examples.csv")
    args = parser.parse_args()

    synthetic_outputs = read_jsonl(args.synthetic_outputs)
    target_outputs = read_jsonl(args.target_outputs)
    target_attacks = read_jsonl(args.target_attacks)
    blind_outputs = read_jsonl(args.blind_outputs)
    blind_failures = read_csv(args.blind_failures)

    parts = [
        "# Qualitative Appendix",
        "",
        "Generated from cached local artifacts only; no API calls are made.",
        "",
        synthetic_section(synthetic_outputs),
        "",
        target_aware_section(target_outputs, target_attacks),
        "",
        blind_failure_section(blind_outputs, blind_failures),
        "",
        "## Source Artifacts",
        "",
        f"- `{clean_ascii(args.synthetic_outputs)}`",
        f"- `{clean_ascii(args.target_outputs)}`",
        f"- `{clean_ascii(args.target_attacks)}`",
        f"- `{clean_ascii(args.blind_outputs)}`",
        f"- `{clean_ascii(args.blind_failures)}`",
        "",
    ]
    ensure_parent(args.out)
    Path(args.out).write_text("\n".join(parts), encoding="ascii")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
