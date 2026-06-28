# Budget-Fixed Blind RAT-Bench Backstop v2

This branch reruns the blind public RAT-Bench v2 transformation after fixing the
RB-QIG optimizer so it scans forward to the next risk-reducing candidate level
instead of stopping when an intermediate generalization has no immediate risk
drop.

Source input: `data/processed/ratbench_english_d1_100_blind_backstop_v2_api_qi.jsonl`

Corrected output directory: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/`

## Budget Check

The previous v2 transformed outputs had document-risk budget violations for
RB-QIG variants because some low-risk QIs needed to skip a same-risk
generalization before reaching a redaction level. The corrected outputs have no
violations:

| Method | Max doc risk after |
|---|---:|
| RB-QIG strict | 2.0 |
| RB-QIG balanced | 4.0 |
| RB-QIG utility | 6.0 |

## Deterministic Metrics

| Method | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Token change |
|---|---:|---:|---:|---:|---:|
| Direct | 39.0% | 94.4% | 94.4% | 94.3% | 0.9% |
| Blanket QI | 0.0% | 3.1% | 3.1% | 3.1% | 10.8% |
| RB-QIG balanced | 0.0% | 4.6% | 6.4% | 5.4% | 10.1% |

Bootstrap:

- Direct risk-weighted leakage: 94.3% [91.3, 96.8]
- RB-QIG balanced risk-weighted leakage: 5.4% [2.8, 8.5]
- Direct minus RB-QIG balanced: +88.9 points [85.0, 92.5]
- RB-QIG balanced minus blanket QI: +2.3 points [0.6, 4.9]

## LLM Attacker

| Method | Record compromise | Exact attr leak | Coarse attr leak | Risk-weighted leak |
|---|---:|---:|---:|---:|
| Direct | 37.0% | 74.9% | 81.2% | 78.1% |
| Blanket QI | 1.0% | 5.4% | 8.3% | 6.8% |
| RB-QIG balanced | 1.0% | 5.3% | 7.4% | 6.4% |

Bootstrap:

- Direct LLM risk-weighted leakage: 78.1% [73.3, 82.9]
- RB-QIG balanced LLM risk-weighted leakage: 6.4% [3.9, 9.1]
- Direct minus RB-QIG balanced: +71.8 points [66.4, 76.9]
- RB-QIG balanced minus blanket QI: -0.5 points [-2.5, 1.5]

## LLM Utility

| Method | Label preserved | LLM fact preservation | Semantic utility |
|---|---:|---:|---:|
| Direct | 99.0% | 84.3% | 86.2% |
| Blanket QI | 99.0% | 53.8% | 62.6% |
| RB-QIG balanced | 96.0% | 55.5% | 62.2% |

Bootstrap:

- Blanket QI semantic utility: 62.6% [59.2, 66.0]
- RB-QIG balanced semantic utility: 62.2% [58.8, 65.2]
- RB-QIG balanced minus blanket QI: -0.4 points [-4.2, 3.4]
- RB-QIG balanced minus blanket QI fact preservation: +1.7 points [-3.4, 6.6]

## Cost

The corrected transformation, deterministic scoring, specificity scoring,
failure analysis, plotting, and bootstrapping are local. Rerunning the LLM
attacker and standard utility judge made 20 new RB-QIG calls each because
direct and blanket rows reused cache.

| Judge | New calls | New tokens | New cost |
|---|---:|---:|---:|
| LLM attacker | 20 | 34,420 | $0.010325 |
| LLM utility | 20 | 64,999 | $0.016377 |

## Interpretation

This is the authoritative paper-facing blind public v2 result. The budget fix
does not change the qualitative story: blind backstopped RB-QIG sharply reduces
residual risk relative to direct redaction, is statistically tied with blanket
QI under the LLM attacker, remains slightly leakier than blanket under
deterministic coarse scoring, and does not show a public semantic-utility
advantage over blanket redaction.
