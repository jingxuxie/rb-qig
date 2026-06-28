from __future__ import annotations

import argparse
from copy import deepcopy
from typing import Iterable, Iterator

import spacy
from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpArtifacts, NlpEngine

from rbqig.io_utils import read_jsonl, write_jsonl
from rbqig.transform import compute_doc_risk


METHOD_NAME = "presidio_pattern"


class BlankNlpEngine(NlpEngine):
    """Token-only NLP engine for Presidio pattern recognizers.

    This avoids downloading a spaCy NER model. It intentionally cannot detect
    person, location, or organization entities through learned NER.
    """

    def __init__(self) -> None:
        self.nlp = {"en": spacy.blank("en")}

    def load(self) -> None:
        return None

    def is_loaded(self) -> bool:
        return True

    def process_text(self, text: str, language: str) -> NlpArtifacts:
        doc = self.nlp[language](text)
        return NlpArtifacts(
            entities=[],
            tokens=doc,
            tokens_indices=[token.idx for token in doc],
            lemmas=[token.text.lower() for token in doc],
            nlp_engine=self,
            language=language,
        )

    def process_batch(
        self,
        texts: Iterable[str],
        language: str,
        batch_size: int = 1,
        n_process: int = 1,
        **kwargs,
    ) -> Iterator[tuple[str, NlpArtifacts]]:
        for text in texts:
            yield text, self.process_text(text, language)

    def is_stopword(self, word: str, language: str) -> bool:
        return self.nlp[language].vocab[word].is_stop

    def is_punct(self, word: str, language: str) -> bool:
        return self.nlp[language].vocab[word].is_punct

    def get_supported_entities(self) -> list[str]:
        return []

    def get_supported_languages(self) -> list[str]:
        return ["en"]


def make_pattern_recognizer(entity: str, patterns: list[tuple[str, str, float]]) -> PatternRecognizer:
    return PatternRecognizer(
        supported_entity=entity,
        patterns=[Pattern(name=name, regex=regex, score=score) for name, regex, score in patterns],
        supported_language="en",
    )


def make_analyzer() -> AnalyzerEngine:
    recognizers = [
        make_pattern_recognizer(
            "EMAIL_ADDRESS",
            [("email", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", 0.85)],
        ),
        make_pattern_recognizer(
            "PHONE_NUMBER",
            [("us_phone", r"\b(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}\b", 0.7)],
        ),
        make_pattern_recognizer(
            "URL",
            [("simple_url", r"\b(?:https?://|www\.)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\S*\b", 0.7)],
        ),
        make_pattern_recognizer(
            "US_SSN",
            [("ssn", r"\b\d{3}-\d{2}-\d{4}\b", 0.85)],
        ),
        make_pattern_recognizer(
            "US_ZIP_CODE",
            [("zip", r"\b\d{5}(?:-\d{4})?\b", 0.3)],
        ),
        make_pattern_recognizer(
            "CASE_CODE",
            [("legal_case_code", r"\b\d{2,6}/\d{2,4}\b", 0.6)],
        ),
        make_pattern_recognizer(
            "PERSON",
            [
                (
                    "self_introduction_name",
                    r"\b(?:my name is|my name's|my name's|name is|this is|i am|i'm)\s+"
                    r"([A-Z][A-Za-z'’-]+(?:\s+[A-Z][A-Za-z'’-]+){0,2})\b",
                    0.45,
                )
            ],
        ),
    ]
    registry = RecognizerRegistry(recognizers=recognizers, supported_languages=["en"])
    return AnalyzerEngine(
        registry=registry,
        nlp_engine=BlankNlpEngine(),
        supported_languages=["en"],
        context_aware_enhancer=None,
    )


def placeholder(entity_type: str) -> str:
    return f"[{entity_type.upper()}]"


def replacement_ranges(text: str, analyzer: AnalyzerEngine, score_threshold: float) -> list[dict]:
    results = analyzer.analyze(text=text, language="en", score_threshold=score_threshold)
    candidates = sorted(
        results,
        key=lambda item: (item.start, -(item.end - item.start), -item.score),
    )
    kept: list[dict] = []
    occupied: list[tuple[int, int]] = []
    for result in candidates:
        span = text[result.start : result.end]
        if any(not (result.end <= start or result.start >= end) for start, end in occupied):
            continue
        occupied.append((result.start, result.end))
        kept.append(
            {
                "start": result.start,
                "end": result.end,
                "entity_type": result.entity_type,
                "score": float(result.score),
                "span": span,
            }
        )
    return kept


def apply_replacements(text: str, ranges: list[dict]) -> tuple[str, list[dict]]:
    current = text
    changes = []
    for item in sorted(ranges, key=lambda entry: entry["start"], reverse=True):
        repl = placeholder(item["entity_type"])
        current = current[: item["start"]] + repl + current[item["end"] :]
        changes.append(
            {
                "original_span": item["span"],
                "replacement": repl,
                "category": item["entity_type"].lower(),
                "privacy_risk_before": 5,
                "privacy_risk_after": 0,
                "utility_importance": 0,
                "kind": "presidio_pattern",
                "score": round(float(item["score"]), 4),
            }
        )
    changes.reverse()
    return current, changes


def transform_record(record: dict, analyzer: AnalyzerEngine, score_threshold: float, method_name: str) -> dict:
    original_text = record["original_text"]
    ranges = replacement_ranges(original_text, analyzer, score_threshold)
    transformed_text, change_log = apply_replacements(original_text, ranges)
    qids = deepcopy(record.get("quasi_identifiers", []))
    doc_risk = compute_doc_risk(
        [
            {
                "idx": idx,
                "qi": qi,
                "level": 0,
                "current_risk": float(qi["privacy_risk"]),
                "current_utility_loss": 0.0,
            }
            for idx, qi in enumerate(qids)
        ]
    )
    return {
        "id": record["id"],
        "source": record["source"],
        "domain": record["domain"],
        "method": method_name,
        "original_text": original_text,
        "transformed_text": transformed_text,
        "change_log": change_log,
        "doc_risk_before": round(doc_risk, 3),
        "doc_risk_after": round(doc_risk, 3),
        "ground_truth": deepcopy(record.get("ground_truth", {})),
        "quasi_identifiers": qids,
        "eval_quasi_identifiers": deepcopy(record.get("eval_quasi_identifiers", qids)),
        "label_keywords": deepcopy(record.get("label_keywords", [])),
        "label_threshold": record.get("label_threshold", 1),
        "utility_facts": deepcopy(record.get("utility_facts", [])),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a Presidio-style pattern-only direct PII baseline.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--score-threshold", type=float, default=0.3)
    parser.add_argument("--method-name", default=METHOD_NAME)
    args = parser.parse_args()

    analyzer = make_analyzer()
    records = read_jsonl(args.input)
    transformed = [
        transform_record(record, analyzer, args.score_threshold, args.method_name)
        for record in records
    ]
    write_jsonl(args.out, transformed)
    n_changes = sum(len(row["change_log"]) for row in transformed)
    print(f"Wrote {len(transformed)} {args.method_name} records to {args.out}")
    print(f"Pattern detections: {n_changes}")


if __name__ == "__main__":
    main()
