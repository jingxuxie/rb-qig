# Bootstrap Confidence Intervals: synthetic_100

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 100 |
| Direct | 100.0% | [100.0%, 100.0%] | 100 |
| Blanket QI | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG strict | 16.1% | [15.7%, 16.4%] | 100 |
| RB-QIG balanced | 23.6% | [22.9%, 24.5%] | 100 |
| RB-QIG utility | 38.0% | [37.5%, 38.4%] | 100 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 100 |
| Direct | 100.0% | [100.0%, 100.0%] | 100 |
| Blanket QI | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG strict | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG balanced | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG utility | 0.0% | [0.0%, 0.0%] | 100 |

## utility_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 100 |
| Direct | 100.0% | [100.0%, 100.0%] | 100 |
| Blanket QI | 43.3% | [39.9%, 46.8%] | 100 |
| RB-QIG strict | 48.3% | [45.3%, 51.4%] | 100 |
| RB-QIG balanced | 71.7% | [70.8%, 72.4%] | 100 |
| RB-QIG utility | 95.0% | [93.0%, 96.8%] | 100 |

## token_change_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 0.0% | [0.0%, 0.0%] | 100 |
| Direct | 13.4% | [12.6%, 14.3%] | 100 |
| Blanket QI | 63.7% | [62.9%, 64.4%] | 100 |
| RB-QIG strict | 59.3% | [58.7%, 60.0%] | 100 |
| RB-QIG balanced | 59.0% | [58.3%, 59.7%] | 100 |
| RB-QIG utility | 56.6% | [55.8%, 57.5%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | record_compromise_rate | 100.0% | [100.0%, 100.0%] | 100 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 76.4% | [75.5%, 77.2%] | 100 |
| direct_minus_rbqig_b4 | utility_fact_preservation | 28.3% | [27.6%, 29.2%] | 100 |
| direct_minus_rbqig_b4 | token_change_rate | -45.5% | [-46.3%, -44.7%] | 100 |
| direct_minus_blanket_qi | record_compromise_rate | 100.0% | [100.0%, 100.0%] | 100 |
| direct_minus_blanket_qi | risk_weighted_leakage | 100.0% | [100.0%, 100.0%] | 100 |
| direct_minus_blanket_qi | utility_fact_preservation | 56.7% | [53.1%, 60.2%] | 100 |
| direct_minus_blanket_qi | token_change_rate | -50.2% | [-51.1%, -49.4%] | 100 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | 23.6% | [22.9%, 24.5%] | 100 |
| rbqig_b4_minus_blanket_qi | utility_fact_preservation | 28.3% | [25.2%, 31.6%] | 100 |
| rbqig_b4_minus_blanket_qi | token_change_rate | -4.7% | [-5.3%, -4.1%] | 100 |
