from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from rbqig.io_utils import ensure_parent


TOKEN_RE = re.compile(r"[a-z0-9]+")


def norm(text: str) -> str:
    return " ".join(TOKEN_RE.findall(text.lower()))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def span_match(eval_span: str, blind_spans: list[str]) -> bool:
    target = norm(eval_span)
    if not target:
        return False
    for blind_span in blind_spans:
        candidate = norm(blind_span)
        if not candidate:
            continue
        if target in candidate or candidate in target:
            return True
    return False


def pct(num: float, den: float) -> str:
    if den <= 0:
        return "0.0%"
    return f"{100.0 * num / den:.1f}%"


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] + ["---:"] * (len(headers) - 1)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def analyze(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for record in records:
        blind_qis = record.get("quasi_identifiers", [])
        blind_spans = [str(qi.get("span", "")) for qi in blind_qis]
        blind_categories = {str(qi.get("category", "")) for qi in blind_qis}
        for qi in record.get("eval_quasi_identifiers", []):
            category = str(qi.get("category", "unknown"))
            risk = float(qi.get("risk_weight", qi.get("privacy_risk", 1.0)))
            covered = span_match(str(qi.get("span", "")), blind_spans)
            out.append(
                {
                    "id": record.get("id", ""),
                    "attribute": qi.get("attribute", ""),
                    "category": category,
                    "span": qi.get("span", ""),
                    "risk_weight": risk,
                    "span_covered": covered,
                    "category_present": category in blind_categories,
                }
            )
    return out


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    ensure_parent(path)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "attribute",
                "category",
                "span",
                "risk_weight",
                "span_covered",
                "category_present",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict[str, Any]], path: Path) -> None:
    total = len(rows)
    covered = sum(1 for row in rows if row["span_covered"])
    total_risk = sum(float(row["risk_weight"]) for row in rows)
    covered_risk = sum(float(row["risk_weight"]) for row in rows if row["span_covered"])

    by_category: dict[str, dict[str, float]] = defaultdict(lambda: {"n": 0, "covered": 0, "risk": 0.0, "covered_risk": 0.0})
    missed_by_attribute: Counter[str] = Counter()
    missed_risk_by_attribute: Counter[str] = Counter()
    for row in rows:
        stats = by_category[str(row["category"])]
        stats["n"] += 1
        stats["risk"] += float(row["risk_weight"])
        if row["span_covered"]:
            stats["covered"] += 1
            stats["covered_risk"] += float(row["risk_weight"])
        else:
            attr = str(row["attribute"])
            missed_by_attribute[attr] += 1
            missed_risk_by_attribute[attr] += float(row["risk_weight"])

    category_rows = []
    for category, stats in sorted(by_category.items()):
        category_rows.append(
            [
                category,
                str(int(stats["n"])),
                pct(stats["covered"], stats["n"]),
                pct(stats["covered_risk"], stats["risk"]),
            ]
        )

    missed_rows = []
    for attr, risk in missed_risk_by_attribute.most_common(12):
        missed_rows.append([attr, str(missed_by_attribute[attr]), f"{risk:.1f}"])

    examples = sorted(
        [row for row in rows if not row["span_covered"]],
        key=lambda row: (-float(row["risk_weight"]), str(row["category"]), str(row["attribute"])),
    )[:12]
    example_rows = [
        [
            str(row["id"]),
            str(row["attribute"]),
            str(row["category"]),
            str(row["risk_weight"]).rstrip("0").rstrip("."),
            str(row["span"]).replace("|", "/"),
        ]
        for row in examples
    ]

    parts = [
        "# Blind Extractor Coverage Report",
        "",
        "Coverage is measured against original benchmark quasi-identifier spans.",
        "A benchmark QI is covered when its normalized span overlaps a blind-extracted span in the same record.",
        "",
        "## Overall",
        "",
        f"- Benchmark QI spans: {total}",
        f"- Span coverage: {pct(covered, total)} ({covered}/{total})",
        f"- Risk-weighted span coverage: {pct(covered_risk, total_risk)}",
        "",
        "## Coverage by Category",
        "",
        md_table(["Category", "QI spans", "Span coverage", "Risk-weighted coverage"], category_rows),
        "",
        "## Top Missed Attributes",
        "",
        md_table(["Attribute", "Missed spans", "Missed risk weight"], missed_rows),
        "",
        "## High-Risk Miss Examples",
        "",
        md_table(["Record", "Attribute", "Category", "Risk", "Span"], example_rows),
        "",
    ]
    ensure_parent(path)
    path.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze blind QI extraction coverage against benchmark QIs.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-md", required=True)
    parser.add_argument("--out-csv", required=True)
    args = parser.parse_args()

    rows = analyze(read_jsonl(Path(args.input)))
    write_csv(rows, Path(args.out_csv))
    write_report(rows, Path(args.out_md))
    print(f"Wrote {args.out_md} and {args.out_csv}")


if __name__ == "__main__":
    main()
