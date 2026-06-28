# Bootstrap Confidence Intervals: tab_echr_dev_30_qi_specificity

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## utility_weighted_specificity

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 99.8% | [99.4%, 100.0%] | 30 |
| Direct | 99.7% | [99.3%, 100.0%] | 30 |
| Blanket QI | 25.0% | [25.0%, 25.0%] | 30 |
| RB-QIG strict | 28.1% | [27.8%, 28.5%] | 30 |
| RB-QIG balanced | 31.2% | [30.5%, 31.9%] | 30 |
| RB-QIG utility | 34.3% | [33.3%, 35.4%] | 30 |

## qi_specificity_score

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 99.8% | [99.4%, 100.0%] | 30 |
| Direct | 99.7% | [99.3%, 100.0%] | 30 |
| Blanket QI | 25.0% | [25.0%, 25.0%] | 30 |
| RB-QIG strict | 28.1% | [27.7%, 28.4%] | 30 |
| RB-QIG balanced | 31.2% | [30.5%, 31.9%] | 30 |
| RB-QIG utility | 34.3% | [33.2%, 35.4%] | 30 |

## qi_generalized_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 0.0% | [0.0%, 0.0%] | 30 |
| Direct | 0.0% | [0.0%, 0.0%] | 30 |
| Blanket QI | 0.0% | [0.0%, 0.0%] | 30 |
| RB-QIG strict | 7.7% | [6.8%, 8.6%] | 30 |
| RB-QIG balanced | 15.5% | [13.7%, 17.3%] | 30 |
| RB-QIG utility | 23.2% | [20.6%, 25.9%] | 30 |

## qi_placeholder_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 0.0% | [0.0%, 0.0%] | 30 |
| Direct | 0.1% | [0.0%, 0.3%] | 30 |
| Blanket QI | 100.0% | [100.0%, 100.0%] | 30 |
| RB-QIG strict | 92.3% | [91.4%, 93.2%] | 30 |
| RB-QIG balanced | 84.5% | [82.7%, 86.2%] | 30 |
| RB-QIG utility | 76.8% | [74.2%, 79.4%] | 30 |

## qi_exact_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 99.8% | [99.4%, 100.0%] | 30 |
| Direct | 99.7% | [99.3%, 100.0%] | 30 |
| Blanket QI | 0.0% | [0.0%, 0.0%] | 30 |
| RB-QIG strict | 0.0% | [0.0%, 0.0%] | 30 |
| RB-QIG balanced | 0.0% | [0.0%, 0.0%] | 30 |
| RB-QIG utility | 0.0% | [0.0%, 0.0%] | 30 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| rbqig_b4_minus_blanket_qi | utility_weighted_specificity | 6.2% | [5.5%, 6.9%] | 30 |
| rbqig_b4_minus_blanket_qi | qi_specificity_score | 6.2% | [5.5%, 6.9%] | 30 |
| rbqig_b4_minus_blanket_qi | qi_generalized_rate | 15.5% | [13.7%, 17.2%] | 30 |
| rbqig_b4_minus_blanket_qi | qi_placeholder_rate | -15.5% | [-17.3%, -13.8%] | 30 |
| rbqig_b4_minus_blanket_qi | qi_exact_rate | 0.0% | [0.0%, 0.0%] | 30 |
| rbqig_b6_minus_blanket_qi | utility_weighted_specificity | 9.3% | [8.3%, 10.3%] | 30 |
| rbqig_b6_minus_blanket_qi | qi_specificity_score | 9.3% | [8.2%, 10.3%] | 30 |
| rbqig_b6_minus_blanket_qi | qi_generalized_rate | 23.2% | [20.6%, 25.9%] | 30 |
| rbqig_b6_minus_blanket_qi | qi_placeholder_rate | -23.2% | [-26.0%, -20.6%] | 30 |
| rbqig_b6_minus_blanket_qi | qi_exact_rate | 0.0% | [0.0%, 0.0%] | 30 |
| direct_minus_rbqig_b4 | utility_weighted_specificity | 68.6% | [67.7%, 69.3%] | 30 |
| direct_minus_rbqig_b4 | qi_specificity_score | 68.6% | [67.6%, 69.4%] | 30 |
| direct_minus_rbqig_b4 | qi_generalized_rate | -15.5% | [-17.3%, -13.7%] | 30 |
| direct_minus_rbqig_b4 | qi_placeholder_rate | -84.4% | [-86.2%, -82.8%] | 30 |
| direct_minus_rbqig_b4 | qi_exact_rate | 99.7% | [99.3%, 100.0%] | 30 |
