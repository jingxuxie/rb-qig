# Bootstrap Confidence Intervals: tab_placeholder_variant_20260628

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 99.8% | [99.4%, 100.0%] | 30 |
| Blanket QI | 0.0% | [0.0%, 0.1%] | 30 |
| RB-QIG balanced | 12.3% | [9.2%, 15.8%] | 30 |
| RB-QIG placeholder | 0.0% | [0.0%, 0.1%] | 30 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 100.0% | [100.0%, 100.0%] | 30 |
| Blanket QI | 0.0% | [0.0%, 0.0%] | 30 |
| RB-QIG balanced | 0.0% | [0.0%, 0.0%] | 30 |
| RB-QIG placeholder | 0.0% | [0.0%, 0.0%] | 30 |

## utility_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 100.0% | [100.0%, 100.0%] | 30 |
| Blanket QI | 100.0% | [100.0%, 100.0%] | 30 |
| RB-QIG balanced | 100.0% | [100.0%, 100.0%] | 30 |
| RB-QIG placeholder | 100.0% | [100.0%, 100.0%] | 30 |

## token_change_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 1.0% | [0.8%, 1.3%] | 30 |
| Blanket QI | 14.0% | [12.0%, 16.0%] | 30 |
| RB-QIG balanced | 13.9% | [11.9%, 15.9%] | 30 |
| RB-QIG placeholder | 14.0% | [12.1%, 16.0%] | 30 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| rbqig_b4_placeholder_minus_rbqig_b4 | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 30 |
| rbqig_b4_placeholder_minus_rbqig_b4 | risk_weighted_leakage | -12.3% | [-15.9%, -9.1%] | 30 |
| rbqig_b4_placeholder_minus_rbqig_b4 | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 30 |
| rbqig_b4_placeholder_minus_rbqig_b4 | token_change_rate | 0.1% | [0.0%, 0.1%] | 30 |
| rbqig_b4_placeholder_minus_blanket_qi | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 30 |
| rbqig_b4_placeholder_minus_blanket_qi | risk_weighted_leakage | 0.0% | [0.0%, 0.0%] | 30 |
| rbqig_b4_placeholder_minus_blanket_qi | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 30 |
| rbqig_b4_placeholder_minus_blanket_qi | token_change_rate | 0.0% | [0.0%, 0.0%] | 30 |
| direct_minus_rbqig_b4_placeholder | record_compromise_rate | 100.0% | [100.0%, 100.0%] | 30 |
| direct_minus_rbqig_b4_placeholder | risk_weighted_leakage | 99.8% | [99.4%, 100.0%] | 30 |
| direct_minus_rbqig_b4_placeholder | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 30 |
| direct_minus_rbqig_b4_placeholder | token_change_rate | -13.0% | [-14.9%, -11.1%] | 30 |
