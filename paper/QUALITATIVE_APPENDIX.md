# Qualitative Appendix

Generated from cached local artifacts only; no API calls are made.

## Positive Control: Risk-Budgeted Generalization

Record `synth_0000` (`medical_admin`) demonstrates the intended behavior on controlled text.
Utility facts tracked by the evaluator: administrative request, procedure context, condition family, care recipient.

| Method | Risk | Excerpt |
| --- | --- | --- |
| Direct | 36.5 -> 36.5 | [PERSON], a 34-year-old oncology infusion pharmacist at a small oncology startup in Asheville, North Carolina, called from [PHONE] and emailed [EMAIL] about prior authorization for a younger brother with guardianship needs who had April 17, 2025 surgery for familial adenomatous polyposis. |
| Blanket QI | 36.5 -> 0.0 | [PERSON], a [AGE] [OCCUPATION] at [EMPLOYER] in [LOCATION], called from [PHONE] and emailed [EMAIL] about prior authorization for a [FAMILY] who had [DATE] surgery for [MEDICAL]. |
| RB-QIG balanced | 36.5 -> 3.0 | [PERSON], a [AGE] [OCCUPATION] at a healthcare technology company in a city in the southeastern U.S., called from [PHONE] and emailed [EMAIL] about prior authorization for a dependent family member who had [DATE] surgery for [MEDICAL_CONDITION]. |

Takeaway: RB-QIG removes direct identifiers and coarsens high-risk facts, but keeps the task-relevant medical, administrative, and family-role semantics that blanket quasi-identifier redaction discards.

## Public RAT-Bench Target-Aware Comparison

Record `ratbench_english_14` was selected because direct and LLM-direct redaction leave recoverable attributes while RB-QIG balanced is low leakage under the same attacker.
Ground-truth target attributes: citizenship_status=Born in the US, rac2p=Japanese, sex=Female.

| Method | Risk | Attacker recovery | Cited evidence | Transformed excerpt |
| --- | --- | --- | --- | --- |
| Direct | 100.0% | citizenship_status: born in the US (citizenship implied) (exact); rac2p: Japanese (exact); sex: female (exact) | "I was born in the US-Minneapolis" | ...Wood." And yes, if you could suggest a mellow playlist too, that would be lovely. By the way, I was born in the US-Minneapolis, to be exact-but my parents made sure I grew up surrounded by Japanese traditions, especially food and New Year's celebrations. Chatbot: That sounds like a wonderful way to... |
| LLM direct | 100.0% | citizenship_status: born in the US (citizenship implied) (exact); rac2p: Japanese (exact); sex: female (exact) | "I was born in the US-[CITY], to be exact" | ...Wood." And yes, if you could suggest a mellow playlist too, that would be lovely. By the way, I was born in the US-[CITY], to be exact-but my parents made sure I grew up surrounded by Japanese traditions, especially food and New Year's celebrations. Chatbot: That sounds like a wonderful way to grow... |
| Blanket QI | 0.0% | No exact/coarse attribute recovered. | No matching evidence cited. | ...ictable! For reading, do you prefer fiction, nonfiction, or maybe something specifically related to [DEMOGRAPHIC] culture or history? And when it comes to music, what genres do you enjoy? I can recommend playlists based on your preferences. Person: [DEMOGRAPHIC] literature does catch my attention, a... |
| RB-QIG balanced | 0.0% | No exact/coarse attribute recovered. | No matching evidence cited. | ...ictable! For reading, do you prefer fiction, nonfiction, or maybe something specifically related to [DEMOGRAPHIC] culture or history? And when it comes to music, what genres do you enjoy? I can recommend playlists based on your preferences. Person: [DEMOGRAPHIC] literature does catch my attention, a... |

Takeaway: the target-aware setting is where the method has the cleanest story: direct and LLM direct redaction often remove names/contact strings while leaving direct demographic assertions, whereas RB-QIG rewrites or masks the target attributes.

## Blind Public Failure Mode

The blind v2 extractor does not see target attributes at extraction time. Its remaining failures are mostly semantic cues that survive broad generalization.

| Field | Value |
| --- | --- |
| Method | RB-QIG balanced |
| Failure category | citizenship phrasing |
| Attribute | citizenship_status |
| Ground truth | Born abroad of American parent(s) |
| Attacker guess | citizen (via American parent) |
| Evidence | "my parent is American, so I have citizenship through them"; "verify the expiration date and billing address" (contextual unrelated) |
| Transformed excerpt | ...We like to make sure everything's up to date before [OCCUPATION]. Target: Sure, no problem. I was [DEMOGRAPHIC], but my parent is American, so I have citizenship through them. Other: Perfect, thanks for clarifying. Sometimes that comes up with I-9 forms. And for demographic records, can you tell me how you identify in terms of race, sex, and marital status?... |

Takeaway: the public blind result should be framed as a strong privacy reduction, not as solved anonymization. Residual leakage often comes from conversational implications, placeholders that reveal attribute type, or world-knowledge cues in surrounding context.

## Source Artifacts

- `results/synthetic_100/anonymized_outputs.jsonl`
- `results/ratbench_d1_api_100/anonymized_outputs_with_llm_direct.jsonl`
- `results/ratbench_d1_api_100/llm_attacker_outputs_with_llm_direct.jsonl`
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl`
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_failure_examples.csv`
