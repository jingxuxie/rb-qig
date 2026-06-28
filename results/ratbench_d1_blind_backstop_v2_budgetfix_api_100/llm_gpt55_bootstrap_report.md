# Bootstrap Confidence Intervals: ratbench_d1_blind_backstop_v2_budgetfix_api_100_gpt55_attacker50

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 87.8% | [81.7%, 93.1%] | 50 |
| Blanket QI | 29.7% | [22.5%, 37.6%] | 50 |
| RB-QIG balanced | 31.9% | [24.7%, 39.5%] | 50 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 40.0% | [26.0%, 54.0%] | 50 |
| Blanket QI | 2.0% | [0.0%, 6.0%] | 50 |
| RB-QIG balanced | 2.0% | [0.0%, 6.0%] | 50 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | record_compromise_rate | 38.0% | [24.0%, 52.0%] | 50 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 55.9% | [45.0%, 65.7%] | 50 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 50 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | 2.2% | [-4.7%, 9.0%] | 50 |
