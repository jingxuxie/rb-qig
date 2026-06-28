# Bootstrap Confidence Intervals: ratbench_d2_api_30_llm_attacker_with_llm_direct

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 70.8% | [56.4%, 83.7%] | 30 |
| LLM direct | 56.9% | [42.6%, 71.3%] | 30 |
| Blanket QI | 19.8% | [6.7%, 34.6%] | 30 |
| RB-QIG balanced | 13.1% | [3.3%, 25.0%] | 30 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 70.0% | [53.3%, 86.7%] | 30 |
| LLM direct | 60.0% | [43.3%, 76.7%] | 30 |
| Blanket QI | 13.3% | [3.3%, 26.7%] | 30 |
| RB-QIG balanced | 13.3% | [3.3%, 26.7%] | 30 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_llm_direct | record_compromise_rate | 10.0% | [-3.3%, 23.3%] | 30 |
| direct_minus_llm_direct | risk_weighted_leakage | 13.9% | [-1.3%, 29.4%] | 30 |
| llm_direct_minus_rbqig_b4 | record_compromise_rate | 46.7% | [30.0%, 66.7%] | 30 |
| llm_direct_minus_rbqig_b4 | risk_weighted_leakage | 43.8% | [28.9%, 58.4%] | 30 |
| direct_minus_rbqig_b4 | record_compromise_rate | 56.7% | [40.0%, 73.3%] | 30 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 57.6% | [42.4%, 72.8%] | 30 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 0.0% | [-10.0%, 10.0%] | 30 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | -6.7% | [-20.0%, 6.7%] | 30 |
