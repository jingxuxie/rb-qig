# Bootstrap Confidence Intervals: ratbench_d1_blind_backstop_v2_safe_budgetfix_api_100_privacy_aware_utility_50

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
| RB-QIG balanced | 77.1% | [74.9%, 79.2%] | 50 |

## privacy_aware_utility

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 86.0% | [81.2%, 90.0%] | 50 |
| Blanket QI | 88.0% | [84.8%, 91.2%] | 50 |
| RB-QIG balanced | 82.4% | [79.6%, 85.2%] | 50 |

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
| direct_minus_rbqig_b4 | task_content_preservation | 14.5% | [11.8%, 17.3%] | 50 |
| direct_minus_rbqig_b4 | privacy_aware_utility | 3.6% | [-1.2%, 8.0%] | 50 |
| direct_minus_rbqig_b4 | private_loss_penalty | 2.0% | [0.0%, 6.0%] | 50 |
| rbqig_b4_minus_blanket_qi | privacy_aware_label_preservation | 0.0% | [0.0%, 0.0%] | 50 |
| rbqig_b4_minus_blanket_qi | task_content_preservation | -4.3% | [-6.5%, -2.1%] | 50 |
| rbqig_b4_minus_blanket_qi | privacy_aware_utility | -5.6% | [-9.2%, -1.6%] | 50 |
| rbqig_b4_minus_blanket_qi | private_loss_penalty | -2.0% | [-6.0%, 0.0%] | 50 |
