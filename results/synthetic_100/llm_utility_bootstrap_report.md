# Bootstrap Confidence Intervals: synthetic_100_llm_utility

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## llm_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 75.3% | [73.3%, 77.3%] | 100 |
| Blanket QI | 69.1% | [66.6%, 71.4%] | 100 |
| RB-QIG balanced | 71.3% | [69.6%, 73.0%] | 100 |

## semantic_utility_score

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 83.2% | [81.8%, 84.8%] | 100 |
| Blanket QI | 76.8% | [74.8%, 78.4%] | 100 |
| RB-QIG balanced | 79.4% | [78.2%, 80.6%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | llm_fact_preservation | 4.0% | [1.6%, 6.4%] | 100 |
| direct_minus_rbqig_b4 | semantic_utility_score | 3.8% | [2.0%, 5.8%] | 100 |
| direct_minus_blanket_qi | llm_fact_preservation | 6.2% | [3.4%, 8.9%] | 100 |
| direct_minus_blanket_qi | semantic_utility_score | 6.4% | [4.4%, 8.6%] | 100 |
| rbqig_b4_minus_blanket_qi | llm_fact_preservation | 2.2% | [-0.2%, 4.8%] | 100 |
| rbqig_b4_minus_blanket_qi | semantic_utility_score | 2.6% | [0.6%, 4.8%] | 100 |
