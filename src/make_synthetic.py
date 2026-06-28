from __future__ import annotations

import argparse

from rbqig.io_utils import write_jsonl
from rbqig.synthetic import make_records


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic RB-QIG records.")
    parser.add_argument("--n", type=int, default=30)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--out", default="data/synthetic/synthetic_30.jsonl")
    args = parser.parse_args()

    records = make_records(args.n, args.seed)
    write_jsonl(args.out, records)
    print(f"Wrote {len(records)} records to {args.out}")


if __name__ == "__main__":
    main()

