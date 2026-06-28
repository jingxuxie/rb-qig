# Bootstrap Confidence Intervals: ratbench_d1_blind_backstop_v2_budgetfix_api_100_privacy_aware_utility_50

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## privacy_aware_label_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 100.0% | [100.0%, 100.0%] | 50 |
| Blanket QI | 100.0% | [100.0%, 100.0%] | 50 |
| RB-QIG balanced | 100.0% | [100.0%, 100.0%] | 50 |

## task_content_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 91.6% | [90.4%, 92.7%] | 50 |
| Blanket QI | 81.3% | [79.4%, 83.1%] | 50 |
| RB-QIG balanced | 77.7% | [75.5%, 79.8%] | 50 |

## privacy_aware_utility

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 86.0% | [81.2%, 90.0%] | 50 |
| Blanket QI | 88.0% | [84.8%, 91.2%] | 50 |
| RB-QIG balanced | 81.6% | [78.8%, 84.4%] | 50 |

## private_loss_penalty

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 2.0% | [0.0%, 6.0%] | 50 |
| Blanket QI | 2.0% | [0.0%, 6.0%] | 50 |
| RB-QIG balanced | 0.0% | [0.0%, 0.0%] | 50 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | privacy_aware_label_preservation | 0.0% | [0.0%, 0.0%] | 50 |
| direct_minus_rbqig_b4 | task_content_preservation | 13.8% | [11.3%, 16.6%] | 50 |
| direct_minus_rbqig_b4 | privacy_aware_utility | 4.4% | [-0.4%, 8.8%] | 50 |
| direct_minus_rbqig_b4 | private_loss_penalty | 2.0% | [0.0%, 6.0%] | 50 |
| rbqig_b4_minus_blanket_qi | privacy_aware_label_preservation | 0.0% | [0.0%, 0.0%] | 50 |
| rbqig_b4_minus_blanket_qi | task_content_preservation | -3.6% | [-5.9%, -1.4%] | 50 |
| rbqig_b4_minus_blanket_qi | privacy_aware_utility | -6.4% | [-10.0%, -2.8%] | 50 |
| rbqig_b4_minus_blanket_qi | private_loss_penalty | -2.0% | [-6.0%, 0.0%] | 50 |
