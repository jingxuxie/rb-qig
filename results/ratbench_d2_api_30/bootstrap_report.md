# Bootstrap Confidence Intervals: ratbench_d2_api_30_deterministic

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 30 |
| Direct | 94.3% | [85.9%, 100.0%] | 30 |
| Blanket QI | 0.6% | [0.0%, 1.7%] | 30 |
| RB-QIG strict | 31.1% | [21.8%, 40.6%] | 30 |
| RB-QIG balanced | 48.3% | [43.0%, 53.4%] | 30 |
| RB-QIG utility | 50.4% | [46.6%, 55.0%] | 30 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 80.0% | [63.3%, 93.3%] | 30 |
| Direct | 76.7% | [60.0%, 90.0%] | 30 |
| Blanket QI | 0.0% | [0.0%, 0.0%] | 30 |
| RB-QIG strict | 0.0% | [0.0%, 0.0%] | 30 |
| RB-QIG balanced | 0.0% | [0.0%, 0.0%] | 30 |
| RB-QIG utility | 0.0% | [0.0%, 0.0%] | 30 |

## utility_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 96.7% | [91.7%, 100.0%] | 30 |
| Direct | 96.7% | [91.7%, 100.0%] | 30 |
| Blanket QI | 96.7% | [91.7%, 100.0%] | 30 |
| RB-QIG strict | 96.7% | [91.7%, 100.0%] | 30 |
| RB-QIG balanced | 96.7% | [91.7%, 100.0%] | 30 |
| RB-QIG utility | 96.7% | [91.7%, 100.0%] | 30 |

## token_change_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 0.0% | [0.0%, 0.0%] | 30 |
| Direct | 0.1% | [0.0%, 0.1%] | 30 |
| Blanket QI | 2.7% | [2.0%, 3.4%] | 30 |
| RB-QIG strict | 2.6% | [1.9%, 3.4%] | 30 |
| RB-QIG balanced | 2.6% | [1.9%, 3.4%] | 30 |
| RB-QIG utility | 2.6% | [1.9%, 3.3%] | 30 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | record_compromise_rate | 76.7% | [60.0%, 90.0%] | 30 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 46.0% | [37.1%, 53.3%] | 30 |
| direct_minus_rbqig_b4 | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 30 |
| direct_minus_rbqig_b4 | token_change_rate | -2.5% | [-3.3%, -1.8%] | 30 |
| direct_minus_blanket_qi | record_compromise_rate | 76.7% | [60.0%, 90.0%] | 30 |
| direct_minus_blanket_qi | risk_weighted_leakage | 93.7% | [85.4%, 99.4%] | 30 |
| direct_minus_blanket_qi | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 30 |
| direct_minus_blanket_qi | token_change_rate | -2.6% | [-3.4%, -1.9%] | 30 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 30 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | 47.7% | [42.6%, 52.8%] | 30 |
| rbqig_b4_minus_blanket_qi | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 30 |
| rbqig_b4_minus_blanket_qi | token_change_rate | -0.1% | [-0.1%, -0.0%] | 30 |
