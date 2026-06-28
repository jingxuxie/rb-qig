# Bootstrap Confidence Intervals: ratbench_d1_blind_backstop_v2_budgetfix_api_100_llm_utility

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## llm_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 84.3% | [81.2%, 87.0%] | 100 |
| Blanket QI | 53.8% | [49.5%, 58.1%] | 100 |
| RB-QIG balanced | 55.5% | [52.0%, 58.7%] | 100 |

## semantic_utility_score

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 86.2% | [83.2%, 88.8%] | 100 |
| Blanket QI | 62.6% | [59.2%, 66.0%] | 100 |
| RB-QIG balanced | 62.2% | [58.8%, 65.2%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | llm_fact_preservation | 28.8% | [24.3%, 33.1%] | 100 |
| direct_minus_rbqig_b4 | semantic_utility_score | 24.0% | [19.8%, 28.2%] | 100 |
| rbqig_b4_minus_blanket_qi | llm_fact_preservation | 1.7% | [-3.4%, 6.6%] | 100 |
| rbqig_b4_minus_blanket_qi | semantic_utility_score | -0.4% | [-4.2%, 3.4%] | 100 |
