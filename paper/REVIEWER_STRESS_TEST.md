# Reviewer Stress Test

This file is a paper-readiness checklist for likely reviewer objections. It is
not a substitute for the manuscript; it records how to keep the claims ambitious
but defensible.

## Current High-Level Position

The strongest defensible paper claim is:

> Direct PII redaction leaves substantial residual LLM-inference risk from
> quasi-identifiers. RB-QIG is a lightweight, auditable transformation layer
> that sharply reduces this risk when quasi-identifiers are known or well
> extracted. It preserves more utility than blanket quasi-identifier redaction
> in controlled synthetic settings, while public RAT-Bench utility remains a
> caveat rather than a win.

Do not claim:

- legal anonymization,
- deployment readiness,
- privacy superiority over blanket QI redaction,
- a public LLM-judge semantic-utility advantage over blanket redaction,
- state-of-the-art de-identification.

## Likely Objections and Responses

| Objection | Evidence-backed response | Manuscript stance |
| --- | --- | --- |
| The method is simple. | That is the point for a workshop transformation layer: span replacements, a logged risk/utility score, and a greedy risk-budget policy make the system auditable and cheap. The contribution is the residual-risk framing plus an evaluated policy, not a large model. | Keep "lightweight" and "auditable"; avoid presenting RB-QIG as a complex algorithmic breakthrough. |
| Target-aware extraction is unrealistic. | The target-aware RAT-Bench run is explicitly a controlled transformation benchmark. A separate blind public stress test scores against benchmark QIs and shows raw blind coverage 72.8%, v2 backstopped coverage 99.6%, and budget-fixed blind RB-QIG LLM risk 6.4% [3.9, 9.1]. | State target-aware extraction before results; frame blind extraction as the open problem. |
| Utility advantage is only synthetic. | Mostly. Synthetic deterministic utility gives RB-QIG a large edge over blanket QI: 71.7% [70.8, 72.4] vs 43.3% [39.9, 46.8]. Synthetic LLM utility gives only a modest semantic edge: +2.6 points [0.6, 4.8]. Budget-fixed public blind RAT-Bench semantic utility is tied with blanket: -0.4 points [-4.2, 3.4]. A 40-record privacy-aware public utility diagnostic is also negative: -4.5 points [-9.0, 0.0]. A no-API annotation-specificity diagnostic gives a narrow public signal: +6.8 points [4.7, 9.2] on blind RAT-Bench and +6.2 [5.5, 6.9] on TAB. | Claim large utility only in controlled synthetic facts; frame public specificity as a proxy, not task accuracy. |
| Blanket redaction is just as private. | On LLM-attacker privacy, RB-QIG is statistically tied with blanket in both target-aware and blind public settings: target-aware +0.5 points [-2.6, 3.6], budget-fixed blind -0.5 points [-2.5, 1.5]. The value of RB-QIG is the privacy reduction relative to direct and naive LLM redaction, plus synthetic utility preservation. | Do not claim privacy superiority over blanket; claim a more useful point on the controlled privacy-utility frontier. |
| LLM attacker and utility judge may be noisy. | The paper uses paired bootstrap intervals, deterministic metrics, cached structured model outputs, a 30-row harder D2 smoke, a 20-record stronger-attacker smoke, and a 30-document TAB deterministic screen. The claim audit checks 15/15 headline claim groups against local artifacts. | Present LLM metrics as evaluation evidence, not proof of real-world risk bounds. |
| The benchmark is small. | The main public result is 100 English difficulty-1 records; D2 and stronger-attacker runs are deliberately short smokes. This is enough for a workshop claim about a practical evaluation protocol, not enough for a benchmark-saturation claim. | Call it a pilot and stress test; avoid saying "comprehensive". |
| The result is only one domain. | A bounded 30-document TAB ECHR deterministic screen now gives second-domain evidence that direct redaction leaves high quasi-identifier leakage and RB-QIG reduces it. A 10-document TAB legal-task LLM utility screen is inconclusive, with blanket QI, RB-QIG balanced, and RB-QIG utility all at 68.0% [62.0, 74.0]. A legal-role TAB variant is negative: RB-QIG balanced legal-role scores 62.0%, -6.0 points [-14.0, 2.0] versus blanket QI. | Mention TAB only as cross-domain residual-risk support unless stronger utility evaluation is added. |
| Baselines are weak. | The current baselines cover conceptual extremes: direct redaction, naive LLM direct sanitizer, blanket QI redaction, and no transformation. A Presidio-style pattern-only baseline was added as a practical lower bound; it is weaker than the oracle-assisted direct baseline and misses legal identifiers without NER. | Present it as a caveat, not full Presidio. |
| Generalization can leak through placeholders or context. | The failure taxonomy shows exactly this: gendered context, marital or bereavement context, education cues, citizenship phrasing, employment/armed-forces context, race/ethnicity variants, and location context. | Use this as evidence for the inferability argument, not as a minor bug. |
| Risk and utility scores are subjective. | Scores are intentionally transparent and auditable. The synthetic benchmark isolates the scoring tradeoff; public results test whether the policy still reduces measured inference risk. | Present scores as a first operationalization, not as universal risk estimates. |
| The method might distort meaning. | RB-QIG uses span replacements and logged transformation ladders rather than unconstrained rewriting. The LLM utility judge still shows public semantic utility losses, which are reported as limitations. | Keep the "span replacement" design choice visible. |
| Privacy/legal concerns. | All experiments use synthetic or public benchmark data; the paper explicitly does not attempt to identify real people or infer private attributes about individuals. | Keep ethics and no-legal-anonymization language prominent. |

## Evidence Anchors

- Plan-to-evidence audit: `paper/PLAN_TO_EVIDENCE_AUDIT.md`
- Main claim audit: `paper/CLAIM_AUDIT.md`
- Synthetic controlled benchmark: `results/synthetic_100/metrics.csv`
- Synthetic bootstrap intervals: `results/synthetic_100/bootstrap_cis.csv`
- Synthetic utility judge: `results/synthetic_100/llm_utility_metrics.csv`
- Target-aware public LLM attacker: `results/ratbench_d1_api_100/llm_attacker_metrics_with_llm_direct.csv`
- Target-aware public LLM contrasts: `results/ratbench_d1_api_100/llm_bootstrap_contrasts_with_llm_direct.csv`
- Blind public coverage: `results/ratbench_d1_blind_backstop_v2_api_100/blind_coverage_report.md`
- Blind public LLM attacker: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_metrics.csv`
- Blind public utility judge: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_metrics.csv`
- TAB ECHR deterministic screen: `results/tab_echr_dev_30/tab_screen_report.md`
- Presidio-style pattern baseline: `results/presidio_pattern_baseline_report.md`
- Qualitative examples and failure case: `paper/QUALITATIVE_APPENDIX.md`

## High-Value Next Work If Time Allows

1. Improve task-realistic utility evaluation beyond broad labels.
2. Run a small multi-model attacker agreement check on the 20-record stronger-attacker subset.
3. Convert the manuscript to the final workshop template once released or confirmed.
4. Add a compact appendix table showing residual failure categories by method.

## Final Claim Discipline

Use this one-sentence conclusion:

> RB-QIG is not a finished anonymizer; it is an auditable transformation and
> evaluation protocol showing that quasi-identifier generalization can sharply
> reduce residual LLM inference risk while preserving useful semantics in
> controlled settings.
