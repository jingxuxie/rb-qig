# Bootstrap Confidence Intervals: ratbench_d1_blind_backstop_api_100_llm_attacker

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 78.1% | [73.5%, 82.6%] | 100 |
| Blanket QI | 11.4% | [7.8%, 15.3%] | 100 |
| RB-QIG balanced | 10.6% | [7.2%, 14.4%] | 100 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 37.0% | [27.0%, 47.0%] | 100 |
| Blanket QI | 1.0% | [0.0%, 3.0%] | 100 |
| RB-QIG balanced | 1.0% | [0.0%, 3.0%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | record_compromise_rate | 36.0% | [26.0%, 45.0%] | 100 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 67.6% | [62.5%, 72.8%] | 100 |
| direct_minus_blanket_qi | record_compromise_rate | 36.0% | [27.0%, 45.0%] | 100 |
| direct_minus_blanket_qi | risk_weighted_leakage | 66.8% | [61.1%, 72.3%] | 100 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | -0.8% | [-4.0%, 2.6%] | 100 |
