# Bootstrap Confidence Intervals: ratbench_d1_blind_backstop_v2_api_100_privacy_aware_utility_40

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## privacy_aware_label_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 100.0% | [100.0%, 100.0%] | 40 |
| Blanket QI | 100.0% | [100.0%, 100.0%] | 40 |
| RB-QIG balanced | 100.0% | [100.0%, 100.0%] | 40 |

## task_content_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 91.7% | [90.3%, 93.0%] | 40 |
| Blanket QI | 82.0% | [80.1%, 83.8%] | 40 |
| RB-QIG balanced | 79.6% | [77.1%, 81.8%] | 40 |

## privacy_aware_utility

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 86.5% | [82.5%, 90.5%] | 40 |
| Blanket QI | 87.5% | [83.5%, 91.5%] | 40 |
| RB-QIG balanced | 83.0% | [78.5%, 87.0%] | 40 |

## private_loss_penalty

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 0.0% | [0.0%, 0.0%] | 40 |
| Blanket QI | 2.5% | [0.0%, 7.5%] | 40 |
| RB-QIG balanced | 0.0% | [0.0%, 0.0%] | 40 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | privacy_aware_label_preservation | 0.0% | [0.0%, 0.0%] | 40 |
| direct_minus_rbqig_b4 | task_content_preservation | 12.1% | [9.6%, 14.8%] | 40 |
| direct_minus_rbqig_b4 | privacy_aware_utility | 3.5% | [-1.5%, 9.0%] | 40 |
| direct_minus_rbqig_b4 | private_loss_penalty | 0.0% | [0.0%, 0.0%] | 40 |
| rbqig_b4_minus_blanket_qi | privacy_aware_label_preservation | 0.0% | [0.0%, 0.0%] | 40 |
| rbqig_b4_minus_blanket_qi | task_content_preservation | -2.4% | [-5.3%, 0.4%] | 40 |
| rbqig_b4_minus_blanket_qi | privacy_aware_utility | -4.5% | [-9.0%, 0.0%] | 40 |
| rbqig_b4_minus_blanket_qi | private_loss_penalty | -2.5% | [-7.5%, 0.0%] | 40 |
