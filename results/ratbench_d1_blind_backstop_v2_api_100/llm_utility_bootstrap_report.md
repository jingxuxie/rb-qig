# Bootstrap Confidence Intervals: ratbench_d1_blind_backstop_v2_api_100_llm_utility

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## llm_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 84.3% | [81.3%, 87.0%] | 100 |
| Blanket QI | 53.8% | [49.6%, 58.0%] | 100 |
| RB-QIG balanced | 55.8% | [52.4%, 59.2%] | 100 |

## semantic_utility_score

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 86.2% | [83.4%, 88.8%] | 100 |
| Blanket QI | 62.6% | [59.2%, 66.0%] | 100 |
| RB-QIG balanced | 62.6% | [59.2%, 66.0%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | llm_fact_preservation | 28.5% | [23.9%, 32.8%] | 100 |
| direct_minus_rbqig_b4 | semantic_utility_score | 23.6% | [19.4%, 27.8%] | 100 |
| rbqig_b4_minus_blanket_qi | llm_fact_preservation | 2.0% | [-2.8%, 6.8%] | 100 |
| rbqig_b4_minus_blanket_qi | semantic_utility_score | -0.0% | [-3.6%, 3.4%] | 100 |
