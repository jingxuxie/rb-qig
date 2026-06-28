# Bootstrap Confidence Intervals: ratbench_placeholder_variant_20260628_privacy_aware_utility_50

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## privacy_aware_label_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 100.0% | [100.0%, 100.0%] | 50 |
| Blanket QI | 100.0% | [100.0%, 100.0%] | 50 |
| RB-QIG placeholder | 100.0% | [100.0%, 100.0%] | 50 |

## task_content_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 91.6% | [90.4%, 92.7%] | 50 |
| Blanket QI | 81.3% | [79.4%, 83.1%] | 50 |
| RB-QIG placeholder | 80.3% | [78.3%, 82.1%] | 50 |

## privacy_aware_utility

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 86.0% | [81.2%, 90.0%] | 50 |
| Blanket QI | 88.0% | [84.8%, 91.2%] | 50 |
| RB-QIG placeholder | 84.8% | [81.6%, 88.0%] | 50 |

## private_loss_penalty

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 2.0% | [0.0%, 6.0%] | 50 |
| Blanket QI | 2.0% | [0.0%, 6.0%] | 50 |
| RB-QIG placeholder | 0.0% | [0.0%, 0.0%] | 50 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| rbqig_b4_placeholder_minus_blanket_qi | privacy_aware_label_preservation | 0.0% | [0.0%, 0.0%] | 50 |
| rbqig_b4_placeholder_minus_blanket_qi | task_content_preservation | -1.1% | [-3.3%, 1.1%] | 50 |
| rbqig_b4_placeholder_minus_blanket_qi | privacy_aware_utility | -3.2% | [-7.2%, 0.8%] | 50 |
| rbqig_b4_placeholder_minus_blanket_qi | private_loss_penalty | -2.0% | [-6.0%, 0.0%] | 50 |
| direct_minus_rbqig_b4_placeholder | privacy_aware_label_preservation | 0.0% | [0.0%, 0.0%] | 50 |
| direct_minus_rbqig_b4_placeholder | task_content_preservation | 11.3% | [9.1%, 13.6%] | 50 |
| direct_minus_rbqig_b4_placeholder | privacy_aware_utility | 1.2% | [-4.4%, 6.0%] | 50 |
| direct_minus_rbqig_b4_placeholder | private_loss_penalty | 2.0% | [0.0%, 6.0%] | 50 |
