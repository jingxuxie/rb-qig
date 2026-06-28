from __future__ import annotations

import argparse

from rbqig.io_utils import read_jsonl, write_jsonl
from rbqig.transform import METHODS, transform_records


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RB-QIG transformations.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", default="results/anonymized_outputs.jsonl")
    parser.add_argument("--methods", nargs="+", default=METHODS)
    args = parser.parse_args()

    records = read_jsonl(args.input)
    transformed = transform_records(records, args.methods)
    write_jsonl(args.out, transformed)
    print(f"Wrote {len(transformed)} transformed records to {args.out}")


if __name__ == "__main__":
    main()

