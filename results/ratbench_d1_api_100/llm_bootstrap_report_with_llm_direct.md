# Bootstrap Confidence Intervals: ratbench_d1_api_100_llm_attacker_with_llm_direct

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 78.0% | [73.4%, 82.5%] | 100 |
| LLM direct | 46.0% | [40.1%, 52.0%] | 100 |
| Blanket QI | 5.3% | [2.7%, 8.3%] | 100 |
| RB-QIG balanced | 5.7% | [3.2%, 8.8%] | 100 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 76.0% | [67.0%, 84.0%] | 100 |
| LLM direct | 34.0% | [25.0%, 43.0%] | 100 |
| Blanket QI | 3.0% | [0.0%, 7.0%] | 100 |
| RB-QIG balanced | 2.0% | [0.0%, 5.0%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_llm_direct | record_compromise_rate | 42.0% | [31.0%, 53.0%] | 100 |
| direct_minus_llm_direct | risk_weighted_leakage | 32.0% | [25.8%, 38.3%] | 100 |
| llm_direct_minus_rbqig_b4 | record_compromise_rate | 32.0% | [22.0%, 42.0%] | 100 |
| llm_direct_minus_rbqig_b4 | risk_weighted_leakage | 40.2% | [33.1%, 47.1%] | 100 |
| direct_minus_rbqig_b4 | record_compromise_rate | 74.0% | [65.0%, 82.0%] | 100 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 72.2% | [67.0%, 77.4%] | 100 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | -1.0% | [-3.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | 0.5% | [-2.6%, 3.6%] | 100 |
