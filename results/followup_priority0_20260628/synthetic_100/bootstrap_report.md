# Bootstrap Confidence Intervals: synthetic_100_priority0

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 100 |
| Direct | 100.0% | [100.0%, 100.0%] | 100 |
| Blanket QI | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG strict | 16.1% | [15.7%, 16.4%] | 100 |
| RB-QIG balanced | 23.6% | [22.8%, 24.4%] | 100 |
| RB-QIG no-combo | 23.6% | [22.8%, 24.4%] | 100 |
| RB-QIG utility | 38.0% | [37.5%, 38.4%] | 100 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 100 |
| Direct | 100.0% | [100.0%, 100.0%] | 100 |
| Blanket QI | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG strict | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG balanced | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG no-combo | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG utility | 0.0% | [0.0%, 0.0%] | 100 |

## utility_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 100 |
| Direct | 100.0% | [100.0%, 100.0%] | 100 |
| Blanket QI | 43.3% | [40.0%, 46.8%] | 100 |
| RB-QIG strict | 48.3% | [45.4%, 51.3%] | 100 |
| RB-QIG balanced | 71.7% | [70.8%, 72.4%] | 100 |
| RB-QIG no-combo | 71.7% | [70.9%, 72.4%] | 100 |
| RB-QIG utility | 95.0% | [93.0%, 96.8%] | 100 |

## token_change_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 0.0% | [0.0%, 0.0%] | 100 |
| Direct | 13.4% | [12.5%, 14.3%] | 100 |
| Blanket QI | 63.7% | [63.0%, 64.4%] | 100 |
| RB-QIG strict | 59.3% | [58.7%, 60.0%] | 100 |
| RB-QIG balanced | 59.0% | [58.2%, 59.7%] | 100 |
| RB-QIG no-combo | 59.0% | [58.2%, 59.7%] | 100 |
| RB-QIG utility | 56.6% | [55.7%, 57.5%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| rbqig_b4_no_combo_minus_rbqig_b4 | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_no_combo_minus_rbqig_b4 | risk_weighted_leakage | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_no_combo_minus_rbqig_b4 | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_no_combo_minus_rbqig_b4 | token_change_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | 23.6% | [22.9%, 24.5%] | 100 |
| rbqig_b4_minus_blanket_qi | utility_fact_preservation | 28.3% | [25.1%, 31.4%] | 100 |
| rbqig_b4_minus_blanket_qi | token_change_rate | -4.7% | [-5.3%, -4.1%] | 100 |
| rbqig_b2_minus_rbqig_b4 | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b2_minus_rbqig_b4 | risk_weighted_leakage | -7.6% | [-8.1%, -7.1%] | 100 |
| rbqig_b2_minus_rbqig_b4 | utility_fact_preservation | -23.3% | [-25.6%, -20.9%] | 100 |
| rbqig_b2_minus_rbqig_b4 | token_change_rate | 0.4% | [0.2%, 0.6%] | 100 |
| rbqig_b6_minus_rbqig_b4 | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b6_minus_rbqig_b4 | risk_weighted_leakage | 14.3% | [13.7%, 15.0%] | 100 |
| rbqig_b6_minus_rbqig_b4 | utility_fact_preservation | 23.3% | [20.9%, 25.7%] | 100 |
| rbqig_b6_minus_rbqig_b4 | token_change_rate | -2.3% | [-2.8%, -1.9%] | 100 |
