from __future__ import annotations

import argparse
from pathlib import Path

from rbqig.evaluate import evaluate_records
from rbqig.io_utils import write_csv, write_jsonl
from rbqig.plots import plot_leakage_by_method, plot_privacy_utility
from rbqig.report import write_pilot_report, write_qualitative_examples
from rbqig.synthetic import make_records
from rbqig.transform import METHODS, transform_records


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the stdlib-only RB-QIG pilot.")
    parser.add_argument("--n", type=int, default=30)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--out-dir", default="results")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    data_path = Path("data/synthetic") / f"synthetic_{args.n}.jsonl"
    transformed_path = out_dir / "anonymized_outputs.jsonl"
    attacks_path = out_dir / "attacker_outputs.jsonl"
    utility_path = out_dir / "utility_outputs.jsonl"
    metrics_path = out_dir / "metrics.csv"

    records = make_records(args.n, args.seed)
    write_jsonl(data_path, records)

    transformed = transform_records(records, METHODS)
    write_jsonl(transformed_path, transformed)
    for method in METHODS:
        method_rows = [row for row in transformed if row["method"] == method]
        write_jsonl(out_dir / "transformed" / f"{method}.jsonl", method_rows)

    attacks, utility, metrics = evaluate_records(transformed)
    write_jsonl(attacks_path, attacks)
    write_jsonl(utility_path, utility)
    write_csv(metrics_path, metrics)

    figure_dir = out_dir / "figures"
    plot_privacy_utility(metrics, figure_dir / "privacy_utility_frontier.svg")
    plot_leakage_by_method(metrics, figure_dir / "leakage_by_method.svg")
    write_pilot_report(out_dir / "pilot_report.md", metrics, args.n, args.seed)
    write_qualitative_examples(out_dir / "qualitative_examples.md", transformed)

    print(f"Wrote synthetic records: {data_path}")
    print(f"Wrote transformed outputs: {transformed_path}")
    print(f"Wrote metrics: {metrics_path}")
    print(f"Wrote report: {out_dir / 'pilot_report.md'}")
    print(f"Wrote figures: {figure_dir}")


if __name__ == "__main__":
    main()

