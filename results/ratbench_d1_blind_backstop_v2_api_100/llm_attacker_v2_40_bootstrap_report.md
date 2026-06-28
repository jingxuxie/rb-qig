# Bootstrap Confidence Intervals: ratbench_d1_blind_backstop_v2_api_100_llm_attacker_v2_40

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## risk_weighted_leakage

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 75.5% | [67.8%, 82.7%] | 40 |
| Blanket QI | 8.5% | [3.8%, 14.0%] | 40 |
| RB-QIG balanced | 6.1% | [2.4%, 10.6%] | 40 |

## record_compromise_rate

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 45.0% | [30.0%, 60.0%] | 40 |
| Blanket QI | 2.5% | [0.0%, 7.5%] | 40 |
| RB-QIG balanced | 2.5% | [0.0%, 7.5%] | 40 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | record_compromise_rate | 42.5% | [27.5%, 57.5%] | 40 |
| direct_minus_rbqig_b4 | risk_weighted_leakage | 69.4% | [61.4%, 77.3%] | 40 |
| rbqig_b4_minus_blanket_qi | record_compromise_rate | 0.0% | [0.0%, 0.0%] | 40 |
| rbqig_b4_minus_blanket_qi | risk_weighted_leakage | -2.4% | [-6.6%, 1.2%] | 40 |
