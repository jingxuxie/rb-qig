# Bootstrap Confidence Intervals: ratbench_d1_blind_backstop_v2_api_100_llm_utility_v2_40

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## llm_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 80.8% | [74.6%, 86.1%] | 40 |
| Blanket QI | 55.1% | [48.3%, 61.5%] | 40 |
| RB-QIG balanced | 57.0% | [51.2%, 62.5%] | 40 |

## semantic_utility_score

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 82.0% | [76.0%, 86.5%] | 40 |
| Blanket QI | 65.0% | [59.5%, 70.0%] | 40 |
| RB-QIG balanced | 64.5% | [60.0%, 69.0%] | 40 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | llm_fact_preservation | 23.8% | [14.6%, 32.4%] | 40 |
| direct_minus_rbqig_b4 | semantic_utility_score | 17.5% | [10.0%, 24.0%] | 40 |
| rbqig_b4_minus_blanket_qi | llm_fact_preservation | 1.9% | [-5.5%, 9.2%] | 40 |
| rbqig_b4_minus_blanket_qi | semantic_utility_score | -0.5% | [-5.5%, 4.0%] | 40 |
