# Bootstrap Confidence Intervals: synthetic_100_priority0_qi_specificity

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## utility_weighted_specificity

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 100 |
| Direct | 100.0% | [100.0%, 100.0%] | 100 |
| Blanket QI | 25.0% | [25.0%, 25.0%] | 100 |
| RB-QIG strict | 37.0% | [36.8%, 37.2%] | 100 |
| RB-QIG balanced | 43.9% | [43.3%, 44.6%] | 100 |
| RB-QIG no-combo | 43.9% | [43.3%, 44.6%] | 100 |
| RB-QIG utility | 55.6% | [55.3%, 55.8%] | 100 |

## qi_specificity_score

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 100 |
| Direct | 100.0% | [100.0%, 100.0%] | 100 |
| Blanket QI | 25.0% | [25.0%, 25.0%] | 100 |
| RB-QIG strict | 38.1% | [37.8%, 38.4%] | 100 |
| RB-QIG balanced | 44.7% | [44.2%, 45.2%] | 100 |
| RB-QIG no-combo | 44.7% | [44.2%, 45.2%] | 100 |
| RB-QIG utility | 56.2% | [55.7%, 56.6%] | 100 |

## qi_generalized_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 0.0% | [0.0%, 0.0%] | 100 |
| Direct | 0.0% | [0.0%, 0.0%] | 100 |
| Blanket QI | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG strict | 32.8% | [32.0%, 33.6%] | 100 |
| RB-QIG balanced | 49.1% | [47.9%, 50.4%] | 100 |
| RB-QIG no-combo | 49.1% | [47.9%, 50.4%] | 100 |
| RB-QIG utility | 77.9% | [76.8%, 78.9%] | 100 |

## qi_placeholder_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 0.0% | [0.0%, 0.0%] | 100 |
| Direct | 0.0% | [0.0%, 0.0%] | 100 |
| Blanket QI | 100.0% | [100.0%, 100.0%] | 100 |
| RB-QIG strict | 67.2% | [66.4%, 68.0%] | 100 |
| RB-QIG balanced | 50.9% | [49.6%, 52.0%] | 100 |
| RB-QIG no-combo | 50.9% | [49.6%, 52.1%] | 100 |
| RB-QIG utility | 22.1% | [21.0%, 23.2%] | 100 |

## qi_exact_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 100 |
| Direct | 100.0% | [100.0%, 100.0%] | 100 |
| Blanket QI | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG strict | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG balanced | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG no-combo | 0.0% | [0.0%, 0.0%] | 100 |
| RB-QIG utility | 0.0% | [0.0%, 0.0%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| rbqig_b4_no_combo_minus_rbqig_b4 | utility_weighted_specificity | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_no_combo_minus_rbqig_b4 | qi_specificity_score | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_no_combo_minus_rbqig_b4 | qi_exact_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_no_combo_minus_rbqig_b4 | qi_generalized_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_no_combo_minus_rbqig_b4 | qi_placeholder_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | utility_weighted_specificity | 18.9% | [18.2%, 19.7%] | 100 |
| rbqig_b4_minus_blanket_qi | qi_specificity_score | 19.7% | [19.2%, 20.1%] | 100 |
| rbqig_b4_minus_blanket_qi | qi_exact_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | qi_generalized_rate | 49.1% | [47.9%, 50.4%] | 100 |
| rbqig_b4_minus_blanket_qi | qi_placeholder_rate | -49.1% | [-50.4%, -47.9%] | 100 |
| rbqig_b6_minus_rbqig_b2 | utility_weighted_specificity | 18.6% | [18.3%, 18.8%] | 100 |
| rbqig_b6_minus_rbqig_b2 | qi_specificity_score | 18.1% | [17.7%, 18.4%] | 100 |
| rbqig_b6_minus_rbqig_b2 | qi_exact_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b6_minus_rbqig_b2 | qi_generalized_rate | 45.1% | [44.3%, 45.9%] | 100 |
| rbqig_b6_minus_rbqig_b2 | qi_placeholder_rate | -45.1% | [-46.0%, -44.3%] | 100 |
