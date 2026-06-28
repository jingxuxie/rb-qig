from __future__ import annotations

import argparse

from rbqig.evaluate import evaluate_records
from rbqig.io_utils import read_jsonl, write_csv, write_jsonl


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate transformed RB-QIG outputs.")
    parser.add_argument("--input", default="results/anonymized_outputs.jsonl")
    parser.add_argument("--attacks-out", default="results/attacker_outputs.jsonl")
    parser.add_argument("--utility-out", default="results/utility_outputs.jsonl")
    parser.add_argument("--metrics-out", default="results/metrics.csv")
    args = parser.parse_args()

    records = read_jsonl(args.input)
    attacks, utility, metrics = evaluate_records(records)
    write_jsonl(args.attacks_out, attacks)
    write_jsonl(args.utility_out, utility)
    write_csv(args.metrics_out, metrics)
    print(f"Wrote metrics to {args.metrics_out}")


if __name__ == "__main__":
    main()

