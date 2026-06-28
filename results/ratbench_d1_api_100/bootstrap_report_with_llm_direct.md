# Bootstrap Confidence Intervals: ratbench_d1_api_100_deterministic_with_llm_direct

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 100 |
| Direct | 93.8% | [91.0%, 96.3%] | 100 |
| LLM direct | 59.5% | [53.6%, 65.1%] | 100 |
| Blanket QI | 0.3% | [0.0%, 0.6%] | 100 |
| RB-QIG strict | 23.1% | [19.6%, 26.5%] | 100 |
| RB-QIG balanced | 28.6% | [25.3%, 31.8%] | 100 |
| RB-QIG utility | 33.2% | [30.2%, 36.2%] | 100 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 92.0% | [86.0%, 97.0%] | 100 |
| Direct | 92.0% | [86.0%, 97.0%] | 100 |
| LLM direct | 57.0% | [47.0%, 67.0%] | 100 |
| Blanket QI | 1.0% | [0.0%, 3.0%] | 100 |
| RB-QIG strict | 1.0% | [0.0%, 3.0%] | 100 |
| RB-QIG balanced | 1.0% | [0.0%, 3.0%] | 100 |
| RB-QIG utility | 1.0% | [0.0%, 3.0%] | 100 |

## utility_fact_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 100.0% | [100.0%, 100.0%] | 100 |
| Direct | 100.0% | [100.0%, 100.0%] | 100 |
| LLM direct | 100.0% | [100.0%, 100.0%] | 100 |
| Blanket QI | 100.0% | [100.0%, 100.0%] | 100 |
| RB-QIG strict | 100.0% | [100.0%, 100.0%] | 100 |
| RB-QIG balanced | 100.0% | [100.0%, 100.0%] | 100 |
| RB-QIG utility | 100.0% | [100.0%, 100.0%] | 100 |

## token_change_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| None | 0.0% | [0.0%, 0.0%] | 100 |
| Direct | 0.9% | [0.8%, 1.0%] | 100 |
| LLM direct | 3.5% | [3.0%, 4.0%] | 100 |
| Blanket QI | 7.1% | [6.3%, 8.0%] | 100 |
| RB-QIG strict | 7.0% | [6.2%, 7.9%] | 100 |
| RB-QIG balanced | 7.0% | [6.1%, 7.8%] | 100 |
| RB-QIG utility | 6.9% | [6.1%, 7.8%] | 100 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | record_compromise_rate | 91.0% | [85.0%, 96.0%] | 100 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 65.2% | [61.5%, 69.0%] | 100 |
| direct_minus_rbqig_b4 | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| direct_minus_rbqig_b4 | token_change_rate | -6.1% | [-6.9%, -5.3%] | 100 |
| direct_minus_blanket_qi | record_compromise_rate | 91.0% | [85.0%, 96.0%] | 100 |
| direct_minus_blanket_qi | risk_weighted_leakage | 93.5% | [90.7%, 96.1%] | 100 |
| direct_minus_blanket_qi | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| direct_minus_blanket_qi | token_change_rate | -6.2% | [-7.1%, -5.4%] | 100 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | 28.3% | [25.0%, 31.6%] | 100 |
| rbqig_b4_minus_blanket_qi | utility_fact_preservation | 0.0% | [0.0%, 0.0%] | 100 |
| rbqig_b4_minus_blanket_qi | token_change_rate | -0.2% | [-0.2%, -0.1%] | 100 |
