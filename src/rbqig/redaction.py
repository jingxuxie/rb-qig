from __future__ import annotations

import re


EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"\b(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}\b")
ZIP_RE = re.compile(r"\b\d{5}(?:-\d{4})?\b")
URL_RE = re.compile(r"\bhttps?://\S+\b")
PERSON_CONTEXT_RE = re.compile(
    r"\b(?i:my name is|my name's|my name’s|name is|name's|name’s|this is|i am|i'm)\s+"
    r"([A-Z][A-Za-z'’-]+(?:\s+[A-Z][A-Za-z'’-]+){0,2})\b"
)
PERSON_STOPWORDS = {
    "Doctor",
    "Patient",
    "Target",
    "Other",
    "Chatbot",
    "Person",
    "Hello",
    "Hi",
    "Sure",
    "Yes",
    "No",
}


def _placeholder(identifier_type: str) -> str:
    normalized = identifier_type.upper().replace(" ", "_")
    if normalized in {"EMAIL_ADDRESS"}:
        normalized = "EMAIL"
    return f"[{normalized}]"


def _replace_term(text: str, value: str, replacement: str) -> tuple[str, int]:
    if not value:
        return text, 0
    prefix = r"(?<![A-Za-z0-9_])" if value[0].isalnum() else ""
    suffix = r"(?![A-Za-z0-9_])" if value[-1].isalnum() else ""
    pattern = re.compile(prefix + re.escape(value) + suffix, flags=re.IGNORECASE)
    return pattern.subn(lambda _: replacement, text)


def infer_direct_identifiers(text: str, direct_identifiers: list[dict]) -> list[dict]:
    """Add lightweight direct-name cues that RAT-Bench metadata may omit."""
    out = [dict(identifier) for identifier in direct_identifiers]
    seen = {
        str(identifier.get("value", "")).casefold()
        for identifier in out
        if identifier.get("value")
    }

    def add_person(value: str) -> None:
        value = " ".join(value.split()).strip(" ,.;:")
        if not value or value in PERSON_STOPWORDS:
            return
        key = value.casefold()
        if key in seen:
            return
        seen.add(key)
        out.append({"type": "PERSON", "value": value, "source": "heuristic_context"})

    for match in PERSON_CONTEXT_RE.finditer(text):
        full_name = match.group(1)
        add_person(full_name)
        for part in full_name.split():
            if len(part) > 1:
                add_person(part)

    return out


def replace_direct_identifiers(text: str, direct_identifiers: list[dict]) -> tuple[str, list[dict]]:
    current = text
    changes: list[dict] = []
    direct_identifiers = infer_direct_identifiers(text, direct_identifiers)

    for regex, placeholder in [
        (EMAIL_RE, "[EMAIL]"),
        (PHONE_RE, "[PHONE]"),
        (URL_RE, "[URL]"),
        (ZIP_RE, "[ZIP]"),
    ]:
        for match in list(regex.finditer(current)):
            changes.append(
                {
                    "original_span": match.group(0),
                    "replacement": placeholder,
                    "category": placeholder.strip("[]").lower(),
                    "privacy_risk_before": 5,
                    "privacy_risk_after": 0,
                    "utility_importance": 0,
                    "kind": "direct_regex",
                }
            )
        current = regex.sub(placeholder, current)

    for identifier in sorted(direct_identifiers, key=lambda item: len(item["value"]), reverse=True):
        value = identifier["value"]
        if not value:
            continue
        replacement = _placeholder(identifier.get("type", "IDENTIFIER"))
        current, count = _replace_term(current, value, replacement)
        if count == 0:
            continue
        changes.append(
            {
                "original_span": value,
                "replacement": replacement,
                "category": identifier.get("type", "identifier").lower(),
                "privacy_risk_before": 5,
                "privacy_risk_after": 0,
                "utility_importance": 0,
                "kind": "direct_heuristic"
                if identifier.get("source") == "heuristic_context"
                else "direct_ground_truth",
            }
        )

    return current, changes
