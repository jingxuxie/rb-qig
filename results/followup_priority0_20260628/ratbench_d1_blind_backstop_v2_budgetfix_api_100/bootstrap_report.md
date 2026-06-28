# Bootstrap Confidence Intervals: ratbench_d1_blind_backstop_v2_budgetfix_api_100_priority0

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 98.9% | [97.3%, 100.0%] | 100 |
| Direct | 94.3% | [91.3%, 96.8%] | 100 |
| Blanket QI | 3.1% | [1.2%, 5.3%] | 100 |
| RB-QIG strict | 4.4% | [2.0%, 7.4%] | 100 |
| RB-QIG balanced | 5.4% | [2.8%, 8.5%] | 100 |
| RB-QIG no-combo | 5.4% | [2.8%, 8.4%] | 100 |
| RB-QIG utility | 7.2% | [3.9%, 10.9%] | 100 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 39.0% | [30.0%, 49.0%] | 100 |
| Direct | 39.0% | [29.0%, 49.0%] | 100 |
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
| Blanket QI | 100.0% | [100.0%, 100.0%] | 100 |
| RB-QIG strict | 100.0% | [100.0%, 100.0%] | 100 |
| RB-QIG balanced | 100.0% | [100.0%, 100.0%] | 100 |
| RB-QIG no-combo | 100.0% | [100.0%, 100.0%] | 100 |
| RB-QIG utility | 100.0% | [100.0%, 100.0%] | 100 |

## token_change_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 0.0% | [0.0%, 0.0%] | 100 |
| Direct | 0.9% | [0.8%, 1.0%] | 100 |
| Blanket QI | 10.8% | [9.9%, 11.6%] | 100 |
| RB-QIG strict | 10.4% | [9.5%, 11.2%] | 100 |
| RB-QIG balanced | 10.1% | [9.3%, 11.0%] | 100 |
| RB-QIG no-combo | 10.1% | [9.3%, 11.0%] | 100 |
| RB-QIG utility | 9.9% | [9.1%, 10.7%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| rbqig_b4_no_combo_minus_rbqig_b4 | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_no_combo_minus_rbqig_b4 | risk_weighted_leakage | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_no_combo_minus_rbqig_b4 | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_no_combo_minus_rbqig_b4 | token_change_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | 2.3% | [0.6%, 4.8%] | 100 |
| rbqig_b4_minus_blanket_qi | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | token_change_rate | -0.7% | [-0.8%, -0.6%] | 100 |
| rbqig_b2_minus_rbqig_b4 | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b2_minus_rbqig_b4 | risk_weighted_leakage | -1.0% | [-1.8%, -0.2%] | 100 |
| rbqig_b2_minus_rbqig_b4 | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b2_minus_rbqig_b4 | token_change_rate | 0.3% | [0.2%, 0.3%] | 100 |
| rbqig_b6_minus_rbqig_b4 | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b6_minus_rbqig_b4 | risk_weighted_leakage | 1.8% | [0.3%, 4.3%] | 100 |
| rbqig_b6_minus_rbqig_b4 | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b6_minus_rbqig_b4 | token_change_rate | -0.2% | [-0.3%, -0.2%] | 100 |
