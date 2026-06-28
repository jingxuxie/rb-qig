# Bootstrap Confidence Intervals: ratbench_placeholder_variant_20260628

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 94.3% | [91.4%, 96.8%] | 100 |
| Blanket QI | 3.1% | [1.3%, 5.3%] | 100 |
| RB-QIG balanced | 5.4% | [2.8%, 8.5%] | 100 |
| RB-QIG placeholder | 4.1% | [1.7%, 7.1%] | 100 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 39.0% | [30.0%, 49.0%] | 100 |
| Blanket QI | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG balanced | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG placeholder | 0.0% | [0.0%, 0.0%] | 100 |

## utility_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 100.0% | [100.0%, 100.0%] | 100 |
| Blanket QI | 100.0% | [100.0%, 100.0%] | 100 |
| RB-QIG balanced | 100.0% | [100.0%, 100.0%] | 100 |
| RB-QIG placeholder | 100.0% | [100.0%, 100.0%] | 100 |

## token_change_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 0.9% | [0.8%, 1.0%] | 100 |
| Blanket QI | 10.8% | [9.9%, 11.6%] | 100 |
| RB-QIG balanced | 10.1% | [9.3%, 11.0%] | 100 |
| RB-QIG placeholder | 10.3% | [9.4%, 11.2%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| rbqig_b4_placeholder_minus_rbqig_b4 | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_placeholder_minus_rbqig_b4 | risk_weighted_leakage | -1.3% | [-2.3%, -0.4%] | 100 |
| rbqig_b4_placeholder_minus_rbqig_b4 | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_placeholder_minus_rbqig_b4 | token_change_rate | 0.2% | [0.1%, 0.2%] | 100 |
| rbqig_b4_placeholder_minus_blanket_qi | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_placeholder_minus_blanket_qi | risk_weighted_leakage | 1.0% | [0.0%, 3.0%] | 100 |
| rbqig_b4_placeholder_minus_blanket_qi | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_placeholder_minus_blanket_qi | token_change_rate | -0.5% | [-0.6%, -0.4%] | 100 |
| direct_minus_rbqig_b4_placeholder | record_compromise_rate | 39.0% | [30.0%, 49.0%] | 100 |
| direct_minus_rbqig_b4_placeholder | risk_weighted_leakage | 90.2% | [86.4%, 93.7%] | 100 |
| direct_minus_rbqig_b4_placeholder | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| direct_minus_rbqig_b4_placeholder | token_change_rate | -9.4% | [-10.2%, -8.6%] | 100 |
