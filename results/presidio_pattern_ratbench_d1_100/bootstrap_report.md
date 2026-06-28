# Bootstrap Confidence Intervals: presidio_pattern_ratbench_d1_100

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 93.8% | [91.0%, 96.4%] | 100 |
| Blanket QI | 0.3% | [0.0%, 0.6%] | 100 |
| RB-QIG balanced | 28.6% | [25.3%, 31.8%] | 100 |
| presidio_pattern | 85.0% | [80.6%, 89.0%] | 100 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 92.0% | [86.0%, 97.0%] | 100 |
| Blanket QI | 1.0% | [0.0%, 3.0%] | 100 |
| RB-QIG balanced | 1.0% | [0.0%, 3.0%] | 100 |
| presidio_pattern | 90.0% | [84.0%, 95.0%] | 100 |

## utility_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 100.0% | [100.0%, 100.0%] | 100 |
| Blanket QI | 100.0% | [100.0%, 100.0%] | 100 |
| RB-QIG balanced | 100.0% | [100.0%, 100.0%] | 100 |
| presidio_pattern | 100.0% | [100.0%, 100.0%] | 100 |

## token_change_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 0.9% | [0.8%, 1.0%] | 100 |
| Blanket QI | 7.1% | [6.3%, 8.0%] | 100 |
| RB-QIG balanced | 7.0% | [6.2%, 7.8%] | 100 |
| presidio_pattern | 1.5% | [1.3%, 1.7%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| presidio_pattern_minus_direct | record_compromise_rate | -2.0% | [-5.0%, 0.0%] | 100 |
| presidio_pattern_minus_direct | risk_weighted_leakage | -8.8% | [-12.0%, -6.0%] | 100 |
| presidio_pattern_minus_direct | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| presidio_pattern_minus_direct | token_change_rate | 0.6% | [0.4%, 0.8%] | 100 |
| presidio_pattern_minus_rbqig_b4 | record_compromise_rate | 89.0% | [83.0%, 95.0%] | 100 |
| presidio_pattern_minus_rbqig_b4 | risk_weighted_leakage | 56.4% | [51.0%, 61.5%] | 100 |
| presidio_pattern_minus_rbqig_b4 | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| presidio_pattern_minus_rbqig_b4 | token_change_rate | -5.5% | [-6.3%, -4.7%] | 100 |
| direct_minus_rbqig_b4 | record_compromise_rate | 91.0% | [85.0%, 96.0%] | 100 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 65.2% | [61.4%, 68.8%] | 100 |
| direct_minus_rbqig_b4 | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| direct_minus_rbqig_b4 | token_change_rate | -6.1% | [-6.9%, -5.3%] | 100 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | 28.3% | [25.0%, 31.6%] | 100 |
| rbqig_b4_minus_blanket_qi | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | token_change_rate | -0.2% | [-0.2%, -0.1%] | 100 |
