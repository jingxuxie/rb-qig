# Bootstrap Confidence Intervals: synthetic_30_blind_api

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 30 |
| Direct | 100.0% | [100.0%, 100.0%] | 30 |
| Blanket QI | 3.2% | [0.9%, 6.1%] | 30 |
| RB-QIG strict | 4.3% | [1.5%, 7.8%] | 30 |
| RB-QIG balanced | 5.2% | [1.7%, 9.7%] | 30 |
| RB-QIG utility | 5.2% | [1.7%, 9.7%] | 30 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 30 |
| Direct | 100.0% | [100.0%, 100.0%] | 30 |
| Blanket QI | 0.0% | [0.0%, 0.0%] | 30 |
| RB-QIG strict | 0.0% | [0.0%, 0.0%] | 30 |
| RB-QIG balanced | 3.3% | [0.0%, 10.0%] | 30 |
| RB-QIG utility | 3.3% | [0.0%, 10.0%] | 30 |

## utility_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 30 |
| Direct | 100.0% | [100.0%, 100.0%] | 30 |
| Blanket QI | 36.1% | [29.4%, 43.1%] | 30 |
| RB-QIG strict | 41.4% | [33.1%, 49.2%] | 30 |
| RB-QIG balanced | 43.3% | [35.0%, 51.7%] | 30 |
| RB-QIG utility | 43.3% | [35.0%, 51.7%] | 30 |

## token_change_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 0.0% | [0.0%, 0.0%] | 30 |
| Direct | 13.4% | [11.8%, 15.1%] | 30 |
| Blanket QI | 62.9% | [60.5%, 65.3%] | 30 |
| RB-QIG strict | 59.0% | [56.4%, 61.5%] | 30 |
| RB-QIG balanced | 55.8% | [53.1%, 58.3%] | 30 |
| RB-QIG utility | 52.7% | [49.9%, 55.6%] | 30 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | record_compromise_rate | 96.7% | [90.0%, 100.0%] | 30 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 94.8% | [90.2%, 98.3%] | 30 |
| direct_minus_rbqig_b4 | utility_fact_preservation | 56.7% | [48.9%, 65.0%] | 30 |
| direct_minus_rbqig_b4 | token_change_rate | -42.4% | [-45.5%, -38.9%] | 30 |
| direct_minus_blanket_qi | record_compromise_rate | 100.0% | [100.0%, 100.0%] | 30 |
| direct_minus_blanket_qi | risk_weighted_leakage | 96.8% | [93.8%, 99.1%] | 30 |
| direct_minus_blanket_qi | utility_fact_preservation | 63.9% | [56.9%, 70.8%] | 30 |
| direct_minus_blanket_qi | token_change_rate | -49.5% | [-52.9%, -45.9%] | 30 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 3.3% | [0.0%, 10.0%] | 30 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | 2.0% | [0.0%, 5.7%] | 30 |
| rbqig_b4_minus_blanket_qi | utility_fact_preservation | 7.2% | [3.3%, 11.7%] | 30 |
| rbqig_b4_minus_blanket_qi | token_change_rate | -7.1% | [-8.9%, -5.5%] | 30 |
