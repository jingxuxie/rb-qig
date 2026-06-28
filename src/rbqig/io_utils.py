from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Iterable


TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


def ensure_parent(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def read_jsonl(path: str | Path) -> list[dict]:
    records: list[dict] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def write_jsonl(path: str | Path, records: Iterable[dict]) -> None:
    ensure_parent(path)
    with Path(path).open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n")


def write_csv(path: str | Path, rows: list[dict]) -> None:
    ensure_parent(path)
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    fieldnames = list(rows[0].keys())
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize(text: str) -> str:
    return " ".join(TOKEN_RE.findall(text.lower()))


def contains_term(text: str, term: str) -> bool:
    if not term:
        return False
    text_tokens = simple_tokens(text)
    term_tokens = simple_tokens(term)
    if not term_tokens:
        return False
    if len(term_tokens) > len(text_tokens):
        return False
    for idx in range(0, len(text_tokens) - len(term_tokens) + 1):
        if text_tokens[idx : idx + len(term_tokens)] == term_tokens:
            return True
    return False


def simple_tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def token_change_rate(original: str, transformed: str) -> float:
    original_tokens = simple_tokens(original)
    transformed_tokens = simple_tokens(transformed)
    if not original_tokens:
        return 0.0
    original_counts = Counter(original_tokens)
    transformed_counts = Counter(transformed_tokens)
    overlap = 0
    for token, count in original_counts.items():
        overlap += min(count, transformed_counts.get(token, 0))
    return max(0.0, min(1.0, 1.0 - overlap / len(original_tokens)))


def mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def pct(value: float) -> str:
    return f"{100.0 * value:.1f}%"
