from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from rbqig.io_utils import ensure_parent, read_jsonl


CATEGORY_BY_ATTRIBUTE = {
    "sex": "gendered context",
    "marital_status": "marital or bereavement context",
    "schl": "education institution or credential",
    "education": "education institution or credential",
    "citizenship_status": "citizenship phrasing",
    "esr": "employment or armed-forces context",
    "rac2p": "race or ethnicity variant",
    "race": "race or ethnicity variant",
    "date_of_birth": "date or age cue",
    "age": "date or age cue",
    "state_of_residence": "location cue",
    "location": "location cue",
}


def write_csv(path: str | Path, rows: list[dict[str, Any]]) -> None:
    ensure_parent(path)
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    counts: dict[tuple[str, str, str], int] = defaultdict(int)
    examples: dict[tuple[str, str, str], dict[str, Any]] = {}

    for record in records:
        method = record["method"]
        for detail in record.get("details", []):
            match = detail.get("match")
            if match not in {"exact", "coarse"}:
                continue
            attr = detail.get("attribute", "other")
            category = CATEGORY_BY_ATTRIBUTE.get(attr, "other quasi-identifier cue")
            key = (method, category, match)
            counts[key] += 1
            examples.setdefault(
                key,
                {
                    "method": method,
                    "category": category,
                    "match": match,
                    "id": record.get("id"),
                    "attribute": attr,
                    "ground_truth": detail.get("ground_truth", ""),
                    "guess": detail.get("guess", ""),
                    "evidence": "; ".join(detail.get("evidence", [])[:2]),
                },
            )

    count_rows = []
    for (method, category, match), count in sorted(counts.items()):
        count_rows.append(
            {
                "method": method,
                "category": category,
                "match": match,
                "count": count,
            }
        )
    return count_rows, list(examples.values())


def write_markdown(
    path: str | Path,
    source: str | Path,
    counts: list[dict[str, Any]],
    examples: list[dict[str, Any]],
) -> None:
    ensure_parent(path)
    lines = [
        "# LLM Attacker Failure Taxonomy",
        "",
        f"Source: `{source}`",
        "",
        "## Counts",
        "",
        "| Method | Category | Match | Count |",
        "|---|---|---|---:|",
    ]
    for row in counts:
        lines.append(f"| {row['method']} | {row['category']} | {row['match']} | {row['count']} |")

    lines.extend(["", "## Representative Examples", ""])
    lines.append("| Method | Category | Attribute | Ground truth | Guess | Evidence |")
    lines.append("|---|---|---|---|---|---|")
    for row in examples:
        method = str(row["method"]).replace("|", "/")
        category = str(row["category"]).replace("|", "/")
        attribute = str(row["attribute"]).replace("|", "/")
        ground_truth = str(row["ground_truth"]).replace("|", "/")
        guess = str(row["guess"]).replace("|", "/")
        evidence = str(row["evidence"]).replace("|", "/")
        lines.append(
            f"| {method} | {category} | {attribute} | "
            f"{ground_truth} | {guess} | {evidence} |"
        )

    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize LLM attacker leakage failures.")
    parser.add_argument("--input", default="results/ratbench_d1_api_30/llm_attacker_outputs.jsonl")
    parser.add_argument("--counts-out", default="results/ratbench_d1_api_30/failure_taxonomy.csv")
    parser.add_argument("--examples-out", default="results/ratbench_d1_api_30/failure_examples.csv")
    parser.add_argument("--md-out", default="results/ratbench_d1_api_30/failure_taxonomy.md")
    args = parser.parse_args()

    records = read_jsonl(args.input)
    counts, examples = summarize(records)
    write_csv(args.counts_out, counts)
    write_csv(args.examples_out, examples)
    write_markdown(args.md_out, args.input, counts, examples)
    print(f"Wrote failure taxonomy to {args.md_out}")


if __name__ == "__main__":
    main()
