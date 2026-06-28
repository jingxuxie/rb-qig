# Bootstrap Confidence Intervals: ratbench_d1_blind_backstop_api_100_llm_utility

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## llm_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 84.3% | [81.3%, 87.0%] | 100 |
| Blanket QI | 52.6% | [48.5%, 56.7%] | 100 |
| RB-QIG balanced | 55.7% | [52.0%, 59.4%] | 100 |

## semantic_utility_score

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 86.2% | [83.4%, 88.8%] | 100 |
| Blanket QI | 62.4% | [59.0%, 65.8%] | 100 |
| RB-QIG balanced | 62.0% | [58.6%, 65.2%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | llm_fact_preservation | 28.6% | [23.7%, 33.1%] | 100 |
| direct_minus_rbqig_b4 | semantic_utility_score | 24.2% | [20.0%, 28.2%] | 100 |
| direct_minus_blanket_qi | llm_fact_preservation | 31.7% | [26.4%, 36.7%] | 100 |
| direct_minus_blanket_qi | semantic_utility_score | 23.8% | [19.6%, 28.0%] | 100 |
| rbqig_b4_minus_blanket_qi | llm_fact_preservation | 3.1% | [-1.6%, 7.7%] | 100 |
| rbqig_b4_minus_blanket_qi | semantic_utility_score | -0.4% | [-3.6%, 3.0%] | 100 |
