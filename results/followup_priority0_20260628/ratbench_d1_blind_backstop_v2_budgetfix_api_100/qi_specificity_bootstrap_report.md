# Bootstrap Confidence Intervals: ratbench_d1_blind_backstop_v2_budgetfix_api_100_priority0_qi_specificity

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## utility_weighted_specificity

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 99.1% | [98.0%, 100.0%] | 100 |
| Direct | 95.5% | [93.4%, 97.5%] | 100 |
| Blanket QI | 26.4% | [24.8%, 28.2%] | 100 |
| RB-QIG strict | 30.1% | [27.8%, 32.7%] | 100 |
| RB-QIG balanced | 33.2% | [30.4%, 35.9%] | 100 |
| RB-QIG no-combo | 33.2% | [30.5%, 36.1%] | 100 |
| RB-QIG utility | 36.4% | [33.3%, 39.6%] | 100 |

## qi_specificity_score

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 99.1% | [98.0%, 100.0%] | 100 |
| Direct | 95.5% | [93.2%, 97.5%] | 100 |
| Blanket QI | 26.4% | [24.8%, 28.1%] | 100 |
| RB-QIG strict | 30.1% | [27.8%, 32.9%] | 100 |
| RB-QIG balanced | 33.2% | [30.5%, 36.1%] | 100 |
| RB-QIG no-combo | 33.2% | [30.4%, 36.0%] | 100 |
| RB-QIG utility | 36.4% | [33.3%, 39.5%] | 100 |

## qi_generalized_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 0.0% | [0.0%, 0.0%] | 100 |
| Direct | 0.0% | [0.0%, 0.0%] | 100 |
| Blanket QI | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG strict | 7.5% | [4.4%, 11.1%] | 100 |
| RB-QIG balanced | 14.7% | [10.5%, 19.3%] | 100 |
| RB-QIG no-combo | 14.7% | [10.5%, 19.2%] | 100 |
| RB-QIG utility | 20.3% | [15.3%, 25.6%] | 100 |

## qi_placeholder_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 0.8% | [0.0%, 2.0%] | 100 |
| Direct | 4.5% | [2.4%, 7.0%] | 100 |
| Blanket QI | 93.1% | [89.5%, 96.2%] | 100 |
| RB-QIG strict | 84.5% | [79.5%, 89.1%] | 100 |
| RB-QIG balanced | 77.1% | [71.5%, 82.5%] | 100 |
| RB-QIG no-combo | 77.1% | [71.2%, 82.7%] | 100 |
| RB-QIG utility | 70.3% | [63.8%, 76.6%] | 100 |

## qi_exact_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 98.9% | [97.5%, 100.0%] | 100 |
| Direct | 94.4% | [91.6%, 96.8%] | 100 |
| Blanket QI | 3.1% | [1.3%, 5.2%] | 100 |
| RB-QIG strict | 4.1% | [1.7%, 7.2%] | 100 |
| RB-QIG balanced | 4.3% | [2.0%, 7.4%] | 100 |
| RB-QIG no-combo | 4.3% | [1.8%, 7.4%] | 100 |
| RB-QIG utility | 5.6% | [2.5%, 9.3%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| rbqig_b4_no_combo_minus_rbqig_b4 | utility_weighted_specificity | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_no_combo_minus_rbqig_b4 | qi_specificity_score | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_no_combo_minus_rbqig_b4 | qi_exact_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_no_combo_minus_rbqig_b4 | qi_generalized_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_no_combo_minus_rbqig_b4 | qi_placeholder_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | utility_weighted_specificity | 6.8% | [4.7%, 9.2%] | 100 |
| rbqig_b4_minus_blanket_qi | qi_specificity_score | 6.8% | [4.7%, 9.2%] | 100 |
| rbqig_b4_minus_blanket_qi | qi_exact_rate | 1.2% | [0.0%, 3.5%] | 100 |
| rbqig_b4_minus_blanket_qi | qi_generalized_rate | 14.7% | [10.6%, 19.2%] | 100 |
| rbqig_b4_minus_blanket_qi | qi_placeholder_rate | -16.0% | [-21.0%, -11.5%] | 100 |
| rbqig_b6_minus_rbqig_b2 | utility_weighted_specificity | 6.2% | [4.2%, 8.6%] | 100 |
| rbqig_b6_minus_rbqig_b2 | qi_specificity_score | 6.2% | [4.3%, 8.6%] | 100 |
| rbqig_b6_minus_rbqig_b2 | qi_exact_rate | 1.5% | [0.0%, 4.0%] | 100 |
| rbqig_b6_minus_rbqig_b2 | qi_generalized_rate | 12.8% | [8.9%, 17.1%] | 100 |
| rbqig_b6_minus_rbqig_b2 | qi_placeholder_rate | -14.3% | [-18.8%, -10.1%] | 100 |
