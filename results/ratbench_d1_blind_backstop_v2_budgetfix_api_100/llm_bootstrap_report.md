# Bootstrap Confidence Intervals: ratbench_d1_blind_backstop_v2_budgetfix_api_100_llm_attacker

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 78.1% | [73.3%, 82.9%] | 100 |
| Blanket QI | 6.8% | [4.0%, 9.9%] | 100 |
| RB-QIG balanced | 6.4% | [3.9%, 9.1%] | 100 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 37.0% | [28.0%, 46.0%] | 100 |
| Blanket QI | 1.0% | [0.0%, 3.0%] | 100 |
| RB-QIG balanced | 1.0% | [0.0%, 3.0%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | record_compromise_rate | 36.0% | [27.0%, 45.0%] | 100 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 71.8% | [66.4%, 76.9%] | 100 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | -0.5% | [-2.5%, 1.5%] | 100 |
