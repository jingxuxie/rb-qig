from __future__ import annotations

import random
from typing import Any


DOMAINS = [
    "medical_admin",
    "legal_intake",
    "financial_support",
    "hr_workplace",
    "education_support",
]

NAMES = [
    ("Maya Chen", "Emma"),
    ("Daniel Rivera", "Sofia"),
    ("Priya Nair", "Arjun"),
    ("Owen Gallagher", "Liam"),
    ("Aisha Thompson", "Nora"),
    ("Leo Martinez", "Mateo"),
    ("Hannah Kim", "Mina"),
    ("Noah Patel", "Isha"),
    ("Sofia Alvarez", "Lucas"),
    ("Ethan Brooks", "Grace"),
]

LOCATIONS = [
    ("Boise, Idaho", "a city in the U.S. Mountain West", "location", 4),
    ("Burlington, Vermont", "a small city in New England", "location", 4),
    ("Duluth, Minnesota", "a city in the upper Midwest", "location", 4),
    ("Asheville, North Carolina", "a city in the southeastern U.S.", "location", 4),
    ("Santa Fe, New Mexico", "a city in the U.S. Southwest", "location", 4),
    ("Bend, Oregon", "a city in the Pacific Northwest", "location", 4),
]

OCCUPATIONS = [
    ("lead Rust compiler engineer", "software professional", 4),
    ("pediatric neurosurgeon", "specialist physician", 5),
    ("wildfire insurance actuary", "insurance analyst", 4),
    ("tribal water-rights attorney", "public-interest attorney", 5),
    ("assistive-technology coordinator", "education support specialist", 4),
    ("oncology infusion pharmacist", "clinical pharmacy professional", 5),
]

EMPLOYERS = [
    ("a small oncology startup", "a healthcare technology company", 3),
    ("St. Agnes Regional Hospital", "a regional hospital", 4),
    ("Cedar Mutual Insurance", "an insurance company", 3),
    ("North Valley Legal Aid", "a legal services organization", 3),
    ("Mesa County School District", "a school district", 3),
    ("Riverbend Biologics", "a life-sciences company", 4),
]

CONDITIONS = [
    ("familial adenomatous polyposis", "an inherited gastrointestinal condition", 5),
    ("Ehlers-Danlos syndrome", "a connective-tissue condition", 4),
    ("early-onset Parkinson's disease", "a neurological condition", 5),
    ("aplastic anemia", "a serious blood disorder", 5),
    ("Type 1 diabetes with hypoglycemia unawareness", "a chronic endocrine condition", 4),
    ("post-transplant immunosuppression", "a transplant-related health condition", 5),
]

LEGAL_FACTS = [
    ("a March 2025 deportation hearing in Ada County", "a recent immigration proceeding", 5),
    ("a sealed juvenile guardianship case", "a family-law proceeding", 4),
    ("a whistleblower retaliation complaint filed in 2024", "an employment-law complaint", 4),
    ("a protective-order hearing after a January 2025 incident", "a recent protective-order matter", 5),
]

FINANCIAL_FACTS = [
    ("a Chapter 13 bankruptcy filed in May 2025", "a recent debt-restructuring process", 5),
    ("medical debt sent to collections after a rare-disease treatment", "medical debt in collections", 4),
    ("a wildfire-loss claim denied after the 2024 evacuation", "a denied property-loss claim", 4),
    ("student-loan garnishment after a disability leave", "a wage-garnishment issue", 4),
]

EDUCATION_FACTS = [
    ("Stanford CS class of 2013", "computer science graduate from a selective U.S. university", 4),
    ("University of Vermont nursing cohort of 2019", "nursing graduate from a regional university", 4),
    ("Gallatin High School class of 2025", "student at a local high school", 4),
    ("a doctoral program in computational linguistics at CU Boulder", "a graduate program in computing", 4),
]

DATES = [
    ("April 17, 2025", "recently", 3),
    ("June 3, 2024", "in 2024", 3),
    ("October 12, 2025", "in late 2025", 3),
    ("February 8, 2026", "in early 2026", 3),
]

AGES = [
    (29, "adult in their late 20s"),
    (34, "adult in their 30s"),
    (37, "adult in their 30s"),
    (42, "adult in their 40s"),
    (51, "adult in their 50s"),
]

FAMILY = [
    ("7-year-old daughter", "young child"),
    ("teenage son", "teenage child"),
    ("elderly mother", "older parent"),
    ("spouse", "family member"),
    ("younger brother with guardianship needs", "dependent family member"),
]


def make_qi(
    *,
    attribute: str,
    category: str,
    span: str,
    broad: str,
    privacy_risk: int,
    utility_importance: int,
    why_risky: str,
    placeholder: str | None = None,
    broad_risk: int = 1,
    broad_utility_loss: float = 1.0,
    redaction_utility_loss: float = 3.0,
) -> dict[str, Any]:
    placeholder = placeholder or f"[{category.upper()}]"
    return {
        "attribute": attribute,
        "category": category,
        "span": span,
        "privacy_risk": privacy_risk,
        "utility_importance": utility_importance,
        "risk_weight": max(1, privacy_risk),
        "why_risky": why_risky,
        "suggested_generalization": broad,
        "coarse_values": [broad],
        "levels": [
            {
                "replacement": broad,
                "privacy_risk_after": broad_risk,
                "utility_loss": broad_utility_loss,
                "kind": "generalize",
            },
            {
                "replacement": placeholder,
                "privacy_risk_after": 0,
                "utility_loss": redaction_utility_loss,
                "kind": "redact",
            },
        ],
    }


def _email_for(name: str, idx: int) -> str:
    local = name.lower().replace(" ", ".")
    return f"{local}{idx}@example.org"


def _phone_for(idx: int) -> str:
    return f"555-01{idx % 100:02d}-{(idx * 37) % 10000:04d}"


def _direct_identifiers(name: str, child: str, email: str, phone: str) -> list[dict]:
    name_parts = name.split()
    return [
        {"type": "PERSON", "value": name},
        {"type": "PERSON", "value": name_parts[0]},
        {"type": "PERSON", "value": name_parts[-1]},
        {"type": "PERSON", "value": child},
        {"type": "EMAIL", "value": email},
        {"type": "PHONE", "value": phone},
    ]


def _common_context(rng: random.Random, idx: int) -> dict[str, Any]:
    name, child = rng.choice(NAMES)
    age, age_broad = rng.choice(AGES)
    location, location_broad, _, location_risk = rng.choice(LOCATIONS)
    occupation, occupation_broad, occupation_risk = rng.choice(OCCUPATIONS)
    employer, employer_broad, employer_risk = rng.choice(EMPLOYERS)
    date, date_broad, date_risk = rng.choice(DATES)
    family, family_broad = rng.choice(FAMILY)
    email = _email_for(name, idx)
    phone = _phone_for(idx)
    return {
        "name": name,
        "child": child,
        "age": age,
        "age_broad": age_broad,
        "location": location,
        "location_broad": location_broad,
        "location_risk": location_risk,
        "occupation": occupation,
        "occupation_broad": occupation_broad,
        "occupation_risk": occupation_risk,
        "employer": employer,
        "employer_broad": employer_broad,
        "employer_risk": employer_risk,
        "date": date,
        "date_broad": date_broad,
        "date_risk": date_risk,
        "family": family,
        "family_broad": family_broad,
        "email": email,
        "phone": phone,
    }


def _common_qis(c: dict[str, Any], include_date: bool = True) -> list[dict[str, Any]]:
    qis = [
        make_qi(
            attribute="age",
            category="age",
            span=f"{c['age']}-year-old",
            broad=c["age_broad"],
            privacy_risk=3,
            utility_importance=2,
            why_risky="Exact age narrows identity in combination",
            placeholder="[AGE]",
            broad_risk=1,
            broad_utility_loss=0.5,
            redaction_utility_loss=2.0,
        ),
        make_qi(
            attribute="location",
            category="location",
            span=c["location"],
            broad=c["location_broad"],
            privacy_risk=c["location_risk"],
            utility_importance=3,
            why_risky="Fine-grained location narrows candidate population",
            placeholder="[LOCATION]",
            broad_risk=1,
            broad_utility_loss=1.0,
            redaction_utility_loss=3.0,
        ),
        make_qi(
            attribute="occupation",
            category="occupation",
            span=c["occupation"],
            broad=c["occupation_broad"],
            privacy_risk=c["occupation_risk"],
            utility_importance=4,
            why_risky="Rare occupation is linkable",
            placeholder="[OCCUPATION]",
            broad_risk=2,
            broad_utility_loss=0.75,
            redaction_utility_loss=3.5,
        ),
        make_qi(
            attribute="employer_or_industry",
            category="employer",
            span=c["employer"],
            broad=c["employer_broad"],
            privacy_risk=c["employer_risk"],
            utility_importance=3,
            why_risky="Employer links to public/professional records",
            placeholder="[EMPLOYER]",
            broad_risk=1,
            broad_utility_loss=0.75,
            redaction_utility_loss=3.0,
        ),
        make_qi(
            attribute="family_relation",
            category="family",
            span=c["family"],
            broad=c["family_broad"],
            privacy_risk=3,
            utility_importance=3,
            why_risky="Family details aid linkage",
            placeholder="[FAMILY]",
            broad_risk=1,
            broad_utility_loss=0.75,
            redaction_utility_loss=2.5,
        ),
    ]
    if include_date:
        qis.append(
            make_qi(
                attribute="date",
                category="date",
                span=c["date"],
                broad=c["date_broad"],
                privacy_risk=3,
                utility_importance=2,
                why_risky="Exact date is linkable to records",
                placeholder="[DATE]",
                broad_risk=1,
                broad_utility_loss=0.5,
                redaction_utility_loss=2.0,
            )
        )
    return qis


def _record_medical_admin(idx: int, rng: random.Random) -> dict[str, Any]:
    c = _common_context(rng, idx)
    condition, condition_broad, condition_risk = rng.choice(CONDITIONS)
    text = (
        f"{c['name']}, a {c['age']}-year-old {c['occupation']} at {c['employer']} "
        f"in {c['location']}, called from {c['phone']} and emailed {c['email']} "
        f"about prior authorization for a {c['family']} who had {c['date']} surgery for "
        f"{condition}."
    )
    qis = _common_qis(c, include_date=True)
    qis.append(
        make_qi(
            attribute="sensitive_attribute",
            category="medical",
            span=condition,
            broad=condition_broad,
            privacy_risk=condition_risk,
            utility_importance=5,
            why_risky="Rare diagnosis is sensitive and linkable",
            placeholder="[MEDICAL_CONDITION]",
            broad_risk=2,
            broad_utility_loss=0.5,
            redaction_utility_loss=4.0,
        )
    )
    return _assemble_record(
        idx,
        c,
        text,
        "medical_admin",
        "medical_prior_authorization",
        qis,
        label_keywords=["prior authorization", "surgery"],
        utility_facts=[
            ("administrative request", ["prior authorization"]),
            ("procedure context", ["surgery"]),
            ("condition family", [condition, condition_broad]),
            ("care recipient", [c["family"], c["family_broad"]]),
        ],
        sensitive_attribute=condition,
    )


def _record_legal_intake(idx: int, rng: random.Random) -> dict[str, Any]:
    c = _common_context(rng, idx)
    legal, legal_broad, legal_risk = rng.choice(LEGAL_FACTS)
    text = (
        f"{c['name']}, a {c['age']}-year-old {c['occupation']} at {c['employer']} "
        f"in {c['location']}, sent intake notes from {c['email']} about {legal}; "
        f"the issue also affects a {c['family']}."
    )
    qis = _common_qis(c, include_date=False)
    qis.append(
        make_qi(
            attribute="sensitive_attribute",
            category="legal",
            span=legal,
            broad=legal_broad,
            privacy_risk=legal_risk,
            utility_importance=5,
            why_risky="Legal fact may be public and sensitive",
            placeholder="[LEGAL_FACT]",
            broad_risk=2,
            broad_utility_loss=0.5,
            redaction_utility_loss=4.0,
        )
    )
    return _assemble_record(
        idx,
        c,
        text,
        "legal_intake",
        "legal_intake_triage",
        qis,
        label_keywords=["intake notes", "issue"],
        utility_facts=[
            ("intake context", ["intake notes"]),
            ("legal category", [legal, legal_broad]),
            ("affected family", [c["family"], c["family_broad"]]),
        ],
        sensitive_attribute=legal,
    )


def _record_financial_support(idx: int, rng: random.Random) -> dict[str, Any]:
    c = _common_context(rng, idx)
    financial, financial_broad, financial_risk = rng.choice(FINANCIAL_FACTS)
    text = (
        f"{c['name']} is a {c['age']}-year-old {c['occupation']} at {c['employer']} "
        f"near {c['location']}. In a support ticket sent from {c['email']}, "
        f"{c['name'].split()[0]} asked for hardship review because of {financial} "
        f"while supporting a {c['family']}."
    )
    qis = _common_qis(c, include_date=False)
    qis.append(
        make_qi(
            attribute="sensitive_attribute",
            category="financial",
            span=financial,
            broad=financial_broad,
            privacy_risk=financial_risk,
            utility_importance=5,
            why_risky="Financial hardship can identify and harm",
            placeholder="[FINANCIAL_FACT]",
            broad_risk=2,
            broad_utility_loss=0.5,
            redaction_utility_loss=4.0,
        )
    )
    return _assemble_record(
        idx,
        c,
        text,
        "financial_support",
        "financial_hardship_review",
        qis,
        label_keywords=["support ticket", "hardship review"],
        utility_facts=[
            ("support request", ["support ticket", "hardship review"]),
            ("financial issue", [financial, financial_broad]),
            ("family responsibility", [c["family"], c["family_broad"]]),
        ],
        sensitive_attribute=financial,
    )


def _record_hr_workplace(idx: int, rng: random.Random) -> dict[str, Any]:
    c = _common_context(rng, idx)
    condition, condition_broad, condition_risk = rng.choice(CONDITIONS)
    text = (
        f"{c['name']}, a {c['age']}-year-old {c['occupation']} at {c['employer']} "
        f"in {c['location']}, requested schedule flexibility after a {c['date']} "
        f"hospitalization related to {condition} and caregiving for a {c['family']}."
    )
    qis = _common_qis(c, include_date=True)
    qis.append(
        make_qi(
            attribute="sensitive_attribute",
            category="medical",
            span=condition,
            broad=condition_broad,
            privacy_risk=condition_risk,
            utility_importance=5,
            why_risky="Medical condition is sensitive",
            placeholder="[MEDICAL_CONDITION]",
            broad_risk=2,
            broad_utility_loss=0.5,
            redaction_utility_loss=4.0,
        )
    )
    return _assemble_record(
        idx,
        c,
        text,
        "hr_workplace",
        "workplace_accommodation",
        qis,
        label_keywords=["schedule flexibility", "hospitalization"],
        utility_facts=[
            ("workplace request", ["schedule flexibility"]),
            ("health event", ["hospitalization"]),
            ("condition family", [condition, condition_broad]),
            ("caregiving role", [c["family"], c["family_broad"], "caregiving"]),
        ],
        sensitive_attribute=condition,
    )


def _record_education_support(idx: int, rng: random.Random) -> dict[str, Any]:
    c = _common_context(rng, idx)
    education, education_broad, education_risk = rng.choice(EDUCATION_FACTS)
    condition, condition_broad, condition_risk = rng.choice(CONDITIONS)
    text = (
        f"{c['name']}, a {c['age']}-year-old connected to {education} in "
        f"{c['location']}, contacted support at {c['email']} about classroom "
        f"accommodations for {condition}; the request came from a {c['family']}."
    )
    qis = [
        make_qi(
            attribute="age",
            category="age",
            span=f"{c['age']}-year-old",
            broad=c["age_broad"],
            privacy_risk=3,
            utility_importance=2,
            why_risky="Exact age narrows identity",
            placeholder="[AGE]",
            broad_risk=1,
            broad_utility_loss=0.5,
            redaction_utility_loss=2.0,
        ),
        make_qi(
            attribute="education",
            category="education",
            span=education,
            broad=education_broad,
            privacy_risk=education_risk,
            utility_importance=4,
            why_risky="School and cohort are linkable",
            placeholder="[EDUCATION]",
            broad_risk=2,
            broad_utility_loss=0.75,
            redaction_utility_loss=3.5,
        ),
        make_qi(
            attribute="location",
            category="location",
            span=c["location"],
            broad=c["location_broad"],
            privacy_risk=c["location_risk"],
            utility_importance=3,
            why_risky="Fine-grained location narrows candidates",
            placeholder="[LOCATION]",
            broad_risk=1,
            broad_utility_loss=1.0,
            redaction_utility_loss=3.0,
        ),
        make_qi(
            attribute="sensitive_attribute",
            category="medical",
            span=condition,
            broad=condition_broad,
            privacy_risk=condition_risk,
            utility_importance=5,
            why_risky="Condition drives accommodation and is sensitive",
            placeholder="[MEDICAL_CONDITION]",
            broad_risk=2,
            broad_utility_loss=0.5,
            redaction_utility_loss=4.0,
        ),
        make_qi(
            attribute="family_relation",
            category="family",
            span=c["family"],
            broad=c["family_broad"],
            privacy_risk=3,
            utility_importance=3,
            why_risky="Family details aid linkage",
            placeholder="[FAMILY]",
            broad_risk=1,
            broad_utility_loss=0.75,
            redaction_utility_loss=2.5,
        ),
    ]
    return _assemble_record(
        idx,
        c,
        text,
        "education_support",
        "education_accommodation",
        qis,
        label_keywords=["classroom accommodations", "contacted support"],
        utility_facts=[
            ("accommodation request", ["classroom accommodations"]),
            ("condition family", [condition, condition_broad]),
            ("education context", [education, education_broad]),
            ("requester relation", [c["family"], c["family_broad"]]),
        ],
        sensitive_attribute=condition,
        education=education,
    )


def _assemble_record(
    idx: int,
    c: dict[str, Any],
    text: str,
    domain: str,
    label: str,
    qis: list[dict[str, Any]],
    label_keywords: list[str],
    utility_facts: list[tuple[str, list[str]]],
    sensitive_attribute: str,
    education: str = "",
) -> dict[str, Any]:
    return {
        "id": f"synth_{idx:04d}",
        "source": "synthetic",
        "domain": domain,
        "difficulty": "synthetic",
        "original_text": text,
        "quasi_identifiers": qis,
        "label_keywords": label_keywords,
        "label_threshold": max(1, min(2, len(label_keywords))),
        "utility_facts": [
            {"name": name, "acceptable_terms": terms} for name, terms in utility_facts
        ],
        "ground_truth": {
            "direct_identifiers": _direct_identifiers(
                c["name"], c["child"], c["email"], c["phone"]
            ),
            "attributes": {
                "age": str(c["age"]),
                "location": c["location"],
                "occupation": c["occupation"],
                "employer_or_industry": c["employer"],
                "education": education,
                "sensitive_attribute": sensitive_attribute,
                "family_relation": c["family"],
            },
            "utility_label": label,
        },
    }


FACTORIES = {
    "medical_admin": _record_medical_admin,
    "legal_intake": _record_legal_intake,
    "financial_support": _record_financial_support,
    "hr_workplace": _record_hr_workplace,
    "education_support": _record_education_support,
}


def make_records(n: int, seed: int = 7) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    records = []
    for idx in range(n):
        domain = DOMAINS[idx % len(DOMAINS)]
        records.append(FACTORIES[domain](idx, rng))
    return records
