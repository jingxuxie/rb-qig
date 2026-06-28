# Bootstrap Confidence Intervals: ratbench_d1_blind_backstop_api_100

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 98.9% | [97.4%, 100.0%] | 100 |
| Direct | 94.3% | [91.4%, 96.8%] | 100 |
| Blanket QI | 6.7% | [3.8%, 9.8%] | 100 |
| RB-QIG strict | 13.7% | [9.7%, 18.2%] | 100 |
| RB-QIG balanced | 17.3% | [13.1%, 22.0%] | 100 |
| RB-QIG utility | 20.4% | [15.7%, 25.6%] | 100 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 39.0% | [30.0%, 49.0%] | 100 |
| Direct | 39.0% | [29.0%, 48.0%] | 100 |
| Blanket QI | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG strict | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG balanced | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG utility | 0.0% | [0.0%, 0.0%] | 100 |

## utility_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 100 |
| Direct | 100.0% | [100.0%, 100.0%] | 100 |
| Blanket QI | 100.0% | [100.0%, 100.0%] | 100 |
| RB-QIG strict | 100.0% | [100.0%, 100.0%] | 100 |
| RB-QIG balanced | 100.0% | [100.0%, 100.0%] | 100 |
| RB-QIG utility | 100.0% | [100.0%, 100.0%] | 100 |

## token_change_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 0.0% | [0.0%, 0.0%] | 100 |
| Direct | 0.9% | [0.8%, 1.0%] | 100 |
| Blanket QI | 10.7% | [9.8%, 11.5%] | 100 |
| RB-QIG strict | 9.9% | [9.0%, 10.7%] | 100 |
| RB-QIG balanced | 9.8% | [8.9%, 10.6%] | 100 |
| RB-QIG utility | 9.6% | [8.8%, 10.5%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | record_compromise_rate | 39.0% | [30.0%, 49.0%] | 100 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 77.0% | [71.9%, 81.9%] | 100 |
| direct_minus_rbqig_b4 | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| direct_minus_rbqig_b4 | token_change_rate | -8.9% | [-9.8%, -8.1%] | 100 |
| direct_minus_blanket_qi | record_compromise_rate | 39.0% | [30.0%, 48.0%] | 100 |
| direct_minus_blanket_qi | risk_weighted_leakage | 87.6% | [83.6%, 91.4%] | 100 |
| direct_minus_blanket_qi | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| direct_minus_blanket_qi | token_change_rate | -9.8% | [-10.7%, -9.0%] | 100 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | 10.6% | [7.1%, 14.6%] | 100 |
| rbqig_b4_minus_blanket_qi | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | token_change_rate | -0.9% | [-1.1%, -0.7%] | 100 |
