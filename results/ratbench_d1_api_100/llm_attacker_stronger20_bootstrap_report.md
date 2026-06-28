# Bootstrap Confidence Intervals: ratbench_d1_api_100_stronger20_llm_attacker

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 77.3% | [64.1%, 88.9%] | 20 |
| LLM direct | 40.2% | [29.4%, 51.1%] | 20 |
| Blanket QI | 16.0% | [9.4%, 22.6%] | 20 |
| RB-QIG balanced | 18.0% | [10.4%, 26.2%] | 20 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 80.0% | [60.0%, 95.0%] | 20 |
| LLM direct | 25.0% | [10.0%, 45.0%] | 20 |
| Blanket QI | 5.0% | [0.0%, 15.0%] | 20 |
| RB-QIG balanced | 10.0% | [0.0%, 25.0%] | 20 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_llm_direct | record_compromise_rate | 55.0% | [35.0%, 75.0%] | 20 |
| direct_minus_llm_direct | risk_weighted_leakage | 37.2% | [26.2%, 48.2%] | 20 |
| llm_direct_minus_rbqig_b4 | record_compromise_rate | 15.0% | [0.0%, 30.0%] | 20 |
| llm_direct_minus_rbqig_b4 | risk_weighted_leakage | 22.2% | [11.0%, 34.2%] | 20 |
| direct_minus_rbqig_b4 | record_compromise_rate | 70.0% | [50.0%, 90.0%] | 20 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 59.3% | [46.3%, 72.4%] | 20 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 5.0% | [0.0%, 15.0%] | 20 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | 2.0% | [-3.7%, 6.9%] | 20 |
