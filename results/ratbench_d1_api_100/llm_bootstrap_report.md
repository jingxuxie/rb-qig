# Bootstrap Confidence Intervals: ratbench_d1_api_100_llm_attacker

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 78.0% | [73.4%, 82.5%] | 100 |
| Blanket QI | 5.3% | [2.7%, 8.1%] | 100 |
| RB-QIG balanced | 5.7% | [3.2%, 8.9%] | 100 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 76.0% | [67.0%, 84.0%] | 100 |
| Blanket QI | 3.0% | [0.0%, 7.0%] | 100 |
| RB-QIG balanced | 2.0% | [0.0%, 5.0%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | record_compromise_rate | 74.0% | [65.0%, 82.0%] | 100 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 72.2% | [67.1%, 77.4%] | 100 |
| direct_minus_blanket_qi | record_compromise_rate | 73.0% | [64.0%, 81.0%] | 100 |
| direct_minus_blanket_qi | risk_weighted_leakage | 72.7% | [67.5%, 77.9%] | 100 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | -1.0% | [-3.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | 0.5% | [-2.8%, 3.8%] | 100 |
