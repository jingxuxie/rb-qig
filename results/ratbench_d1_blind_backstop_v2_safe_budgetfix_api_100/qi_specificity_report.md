# QI Semantic Specificity: ratbench_d1_blind_backstop_v2_safe_budgetfix_api_100

This no-API diagnostic uses benchmark quasi-identifier annotations.
Per QI, exact retained spans score 1.0, typed generalizations score 0.65,
bare placeholders score 0.25, and dropped information scores 0.0.
It is a semantic-specificity proxy, not a downstream task-accuracy metric.

| Method | Utility-weighted specificity | Exact | Generalized | Placeholder | Dropped |
| --- | ---: | ---: | ---: | ---: | ---: |
| none | 99.1% | 98.9% | 0.0% | 0.8% | 0.3% |
| direct | 95.5% | 94.4% | 0.0% | 4.5% | 1.1% |
| blanket_qi | 26.4% | 3.1% | 0.0% | 93.1% | 3.8% |
| rbqig_b2 | 30.2% | 4.1% | 7.8% | 84.3% | 3.8% |
| rbqig_b4 | 33.7% | 4.1% | 16.5% | 75.6% | 3.8% |
| rbqig_b4_no_combo | 33.7% | 4.1% | 16.5% | 75.6% | 3.8% |
| rbqig_b6 | 36.6% | 4.1% | 23.8% | 68.3% | 3.8% |
