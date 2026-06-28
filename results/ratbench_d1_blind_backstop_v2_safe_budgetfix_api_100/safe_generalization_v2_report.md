# Safe-Generalization v2 Diagnostic

This diagnostic regenerates blind-backstop v2 RAT-Bench inputs with
`--safe-blind-generalizations`, using 100/100 cached extractor responses. The
goal was to test whether replacing extractor-written instructions such as
`Generalize to ...` with stable category labels improves RB-QIG utility.

Artifacts:

- Safe input: `data/processed/ratbench_english_d1_100_blind_backstop_v2_safe_api_qi.jsonl`
- Transformed outputs: `results/ratbench_d1_blind_backstop_v2_safe_budgetfix_api_100/anonymized_outputs.jsonl`
- Deterministic metrics: `results/ratbench_d1_blind_backstop_v2_safe_budgetfix_api_100/metrics.csv`
- Privacy-aware utility metrics: `results/ratbench_d1_blind_backstop_v2_safe_budgetfix_api_100/llm_privacy_aware_utility_50_metrics.csv`
- Privacy-aware bootstrap report: `results/ratbench_d1_blind_backstop_v2_safe_budgetfix_api_100/llm_privacy_aware_utility_50_bootstrap_report.md`

## Deterministic Metrics

| Method | Risk-weighted leak | QI specificity | Token change |
|---|---:|---:|---:|
| Blanket QI | 3.1% | 26.4% | 10.8% |
| RB-QIG balanced, current v2 | 5.4% | 33.2% | 10.1% |
| RB-QIG balanced, safe v2 | 6.7% | 33.7% | 10.2% |

The safe-v2 outputs remove literal instruction phrases from RB-QIG balanced
text: 0/100 rows contain `Generalize to`, `Remove or generalize`, or `e.g.`.

## Privacy-Aware Utility, 50 Records

| Method | Task content | Privacy-aware utility |
|---|---:|---:|
| Direct | 91.6% | 86.0% |
| Blanket QI | 81.3% | 88.0% |
| RB-QIG balanced, current v2 | 77.7% | 81.6% |
| RB-QIG balanced, safe v2 | 77.1% | 82.4% |

Paired safe-v2 RB-QIG balanced minus blanket QI:

- Task content preservation: -4.3 points [-6.5, -2.1]
- Privacy-aware utility: -5.6 points [-9.2, -1.6]

Cache/cost:

- Safe extractor regeneration: 100/100 cache hits; no fresh extractor calls.
- Safe-v2 privacy-aware utility: 150 judged rows, 128 cache hits, 22 fresh calls.
- Fresh added utility-judge cost: $0.019092.
- Fresh-equivalent utility-judge cost for all rows: $0.125907.

## Interpretation

Safe generalizations fix a real text-quality artifact but do not change the
paper-level conclusion. The safe labels slightly improve privacy-aware utility
over the current v2 RB-QIG output, but RB-QIG remains below blanket QI and
deterministic risk rises from 5.4% to 6.7%. Treat this as a closed negative
diagnostic and do not spend more attacker budget on this variant unless the
rewrite policy itself changes.
