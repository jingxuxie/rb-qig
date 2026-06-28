# Bootstrap Confidence Intervals: ratbench_d1_blind_api_100

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 98.9% | [97.4%, 100.0%] | 100 |
| Direct | 94.8% | [92.0%, 97.2%] | 100 |
| Blanket QI | 32.1% | [26.1%, 38.4%] | 100 |
| RB-QIG strict | 35.0% | [28.7%, 41.3%] | 100 |
| RB-QIG balanced | 37.5% | [31.2%, 44.3%] | 100 |
| RB-QIG utility | 38.2% | [31.6%, 44.8%] | 100 |

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
| Direct | 0.8% | [0.7%, 0.9%] | 100 |
| Blanket QI | 9.7% | [8.9%, 10.6%] | 100 |
| RB-QIG strict | 8.9% | [8.0%, 9.7%] | 100 |
| RB-QIG balanced | 8.7% | [7.8%, 9.6%] | 100 |
| RB-QIG utility | 8.5% | [7.7%, 9.4%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | record_compromise_rate | 39.0% | [30.0%, 49.0%] | 100 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 57.3% | [50.4%, 63.9%] | 100 |
| direct_minus_rbqig_b4 | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| direct_minus_rbqig_b4 | token_change_rate | -7.9% | [-8.8%, -7.1%] | 100 |
| direct_minus_blanket_qi | record_compromise_rate | 39.0% | [30.0%, 48.0%] | 100 |
| direct_minus_blanket_qi | risk_weighted_leakage | 62.7% | [56.3%, 68.9%] | 100 |
| direct_minus_blanket_qi | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| direct_minus_blanket_qi | token_change_rate | -8.9% | [-9.8%, -8.1%] | 100 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | 5.4% | [1.8%, 9.8%] | 100 |
| rbqig_b4_minus_blanket_qi | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | token_change_rate | -1.0% | [-1.2%, -0.9%] | 100 |
