# Bootstrap Confidence Intervals: tab_echr_dev_30_llm_legal_utility_10_with_b6

Nonparametric bootstrap over record IDs. Intervals are percentile 95% CIs.

## legal_summary_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 100.0% | [100.0%, 100.0%] | 10 |
| Blanket QI | 100.0% | [100.0%, 100.0%] | 10 |
| RB-QIG balanced | 100.0% | [100.0%, 100.0%] | 10 |
| RB-QIG utility | 100.0% | [100.0%, 100.0%] | 10 |

## procedure_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 82.0% | [80.0%, 86.0%] | 10 |
| Blanket QI | 74.0% | [68.0%, 80.0%] | 10 |
| RB-QIG balanced | 76.0% | [70.0%, 80.0%] | 10 |
| RB-QIG utility | 78.0% | [72.0%, 84.0%] | 10 |

## legal_issue_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 84.0% | [76.0%, 92.0%] | 10 |
| Blanket QI | 78.0% | [74.0%, 80.0%] | 10 |
| RB-QIG balanced | 76.0% | [68.0%, 84.0%] | 10 |
| RB-QIG utility | 78.0% | [74.0%, 80.0%] | 10 |

## timeline_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 80.0% | [74.0%, 86.0%] | 10 |
| Blanket QI | 68.0% | [62.0%, 74.0%] | 10 |
| RB-QIG balanced | 62.0% | [56.0%, 68.0%] | 10 |
| RB-QIG utility | 64.0% | [60.0%, 70.0%] | 10 |

## outcome_or_remedy_preservation

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 58.0% | [44.0%, 70.0%] | 10 |
| Blanket QI | 54.0% | [40.0%, 66.0%] | 10 |
| RB-QIG balanced | 48.0% | [36.0%, 60.0%] | 10 |
| RB-QIG utility | 58.0% | [48.0%, 68.0%] | 10 |

## legal_specificity

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 70.0% | [64.0%, 76.0%] | 10 |
| Blanket QI | 52.0% | [46.0%, 58.0%] | 10 |
| RB-QIG balanced | 50.0% | [44.0%, 56.0%] | 10 |
| RB-QIG utility | 48.0% | [42.0%, 54.0%] | 10 |

## legal_task_utility

| Method | Mean | 95% CI | n |
|---|---:|---:|---:|
| Direct | 80.0% | [74.0%, 86.0%] | 10 |
| Blanket QI | 68.0% | [62.0%, 74.0%] | 10 |
| RB-QIG balanced | 68.0% | [62.0%, 74.0%] | 10 |
| RB-QIG utility | 68.0% | [62.0%, 74.0%] | 10 |

## Paired Contrasts

Positive values mean the first method has a larger metric value than the second.

| Comparison | Metric | Mean difference | 95% CI | n |
|---|---|---:|---:|---:|
| direct_minus_rbqig_b4 | legal_summary_preservation | 0.0% | [0.0%, 0.0%] | 10 |
| direct_minus_rbqig_b4 | procedure_preservation | 6.0% | [2.0%, 12.0%] | 10 |
| direct_minus_rbqig_b4 | legal_issue_preservation | 8.0% | [2.0%, 14.0%] | 10 |
| direct_minus_rbqig_b4 | timeline_preservation | 18.0% | [10.0%, 26.0%] | 10 |
| direct_minus_rbqig_b4 | outcome_or_remedy_preservation | 10.0% | [2.0%, 18.0%] | 10 |
| direct_minus_rbqig_b4 | legal_specificity | 20.0% | [10.0%, 30.0%] | 10 |
| direct_minus_rbqig_b4 | legal_task_utility | 12.0% | [6.0%, 18.0%] | 10 |
| direct_minus_rbqig_b6 | legal_summary_preservation | 0.0% | [0.0%, 0.0%] | 10 |
| direct_minus_rbqig_b6 | procedure_preservation | 4.0% | [-4.0%, 12.0%] | 10 |
| direct_minus_rbqig_b6 | legal_issue_preservation | 6.0% | [-2.0%, 14.0%] | 10 |
| direct_minus_rbqig_b6 | timeline_preservation | 16.0% | [8.0%, 24.0%] | 10 |
| direct_minus_rbqig_b6 | outcome_or_remedy_preservation | 0.0% | [-8.0%, 8.0%] | 10 |
| direct_minus_rbqig_b6 | legal_specificity | 22.0% | [14.0%, 30.0%] | 10 |
| direct_minus_rbqig_b6 | legal_task_utility | 12.0% | [6.0%, 18.0%] | 10 |
| rbqig_b4_minus_blanket_qi | legal_summary_preservation | 0.0% | [0.0%, 0.0%] | 10 |
| rbqig_b4_minus_blanket_qi | procedure_preservation | 2.0% | [-6.0%, 10.0%] | 10 |
| rbqig_b4_minus_blanket_qi | legal_issue_preservation | -2.0% | [-8.0%, 4.0%] | 10 |
| rbqig_b4_minus_blanket_qi | timeline_preservation | -6.0% | [-16.0%, 4.0%] | 10 |
| rbqig_b4_minus_blanket_qi | outcome_or_remedy_preservation | -6.0% | [-18.0%, 8.0%] | 10 |
| rbqig_b4_minus_blanket_qi | legal_specificity | -2.0% | [-12.0%, 8.0%] | 10 |
| rbqig_b4_minus_blanket_qi | legal_task_utility | 0.0% | [-10.0%, 10.0%] | 10 |
| rbqig_b6_minus_blanket_qi | legal_summary_preservation | 0.0% | [0.0%, 0.0%] | 10 |
| rbqig_b6_minus_blanket_qi | procedure_preservation | 4.0% | [-4.0%, 12.0%] | 10 |
| rbqig_b6_minus_blanket_qi | legal_issue_preservation | 0.0% | [-6.0%, 6.0%] | 10 |
| rbqig_b6_minus_blanket_qi | timeline_preservation | -4.0% | [-12.0%, 4.0%] | 10 |
| rbqig_b6_minus_blanket_qi | outcome_or_remedy_preservation | 4.0% | [-4.0%, 12.0%] | 10 |
| rbqig_b6_minus_blanket_qi | legal_specificity | -4.0% | [-12.0%, 4.0%] | 10 |
| rbqig_b6_minus_blanket_qi | legal_task_utility | 0.0% | [-8.0%, 8.0%] | 10 |
| rbqig_b6_minus_rbqig_b4 | legal_summary_preservation | 0.0% | [0.0%, 0.0%] | 10 |
| rbqig_b6_minus_rbqig_b4 | procedure_preservation | 2.0% | [-6.0%, 10.0%] | 10 |
| rbqig_b6_minus_rbqig_b4 | legal_issue_preservation | 2.0% | [-6.0%, 10.0%] | 10 |
| rbqig_b6_minus_rbqig_b4 | timeline_preservation | 2.0% | [-4.0%, 8.0%] | 10 |
| rbqig_b6_minus_rbqig_b4 | outcome_or_remedy_preservation | 10.0% | [-0.0%, 20.0%] | 10 |
| rbqig_b6_minus_rbqig_b4 | legal_specificity | -2.0% | [-12.0%, 8.0%] | 10 |
| rbqig_b6_minus_rbqig_b4 | legal_task_utility | 0.0% | [-8.0%, 8.0%] | 10 |
