# Bootstrap Confidence Intervals: tab_echr_dev_30_llm_utility_smoke

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## llm_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 83.0% | [76.0%, 89.0%] | 5 |
| Blanket QI | 67.2% | [61.0%, 72.2%] | 5 |
| RB-QIG balanced | 61.0% | [50.0%, 72.0%] | 5 |

## semantic_utility_score

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 84.0% | [80.0%, 92.0%] | 5 |
| Blanket QI | 64.0% | [60.0%, 72.0%] | 5 |
| RB-QIG balanced | 68.0% | [60.0%, 76.0%] | 5 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | llm_fact_preservation | 22.0% | [8.0%, 36.0%] | 5 |
| direct_minus_rbqig_b4 | semantic_utility_score | 16.0% | [8.0%, 20.0%] | 5 |
| rbqig_b4_minus_blanket_qi | llm_fact_preservation | -6.2% | [-21.0%, 6.8%] | 5 |
| rbqig_b4_minus_blanket_qi | semantic_utility_score | 4.0% | [-8.0%, 16.0%] | 5 |
