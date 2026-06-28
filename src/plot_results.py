from __future__ import annotations

import argparse
import csv

from rbqig.plots import plot_leakage_by_method, plot_privacy_utility


def _read_metrics(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot RB-QIG metrics.")
    parser.add_argument("--metrics", default="results/metrics.csv")
    parser.add_argument("--out-dir", default="results/figures")
    args = parser.parse_args()

    metrics = _read_metrics(args.metrics)
    plot_privacy_utility(metrics, f"{args.out_dir}/privacy_utility_frontier.svg")
    plot_leakage_by_method(metrics, f"{args.out_dir}/leakage_by_method.svg")
    print(f"Wrote figures to {args.out_dir}")


if __name__ == "__main__":
    main()

