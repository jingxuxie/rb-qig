# QI Semantic Specificity: tab_echr_dev_30_priority0

This no-API diagnostic uses benchmark quasi-identifier annotations.
Per QI, exact retained spans score 1.0, typed generalizations score 0.65,
bare placeholders score 0.25, and dropped information scores 0.0.
It is a semantic-specificity proxy, not a downstream task-accuracy metric.

| Method | Utility-weighted specificity | Exact | Generalized | Placeholder | Dropped |
| --- | ---: | ---: | ---: | ---: | ---: |
| none | 99.8% | 99.8% | 0.0% | 0.0% | 0.2% |
| direct | 99.7% | 99.7% | 0.0% | 0.1% | 0.2% |
| blanket_qi | 25.0% | 0.0% | 0.0% | 100.0% | 0.0% |
| rbqig_b2 | 28.1% | 0.0% | 7.7% | 92.3% | 0.0% |
| rbqig_b4 | 31.2% | 0.0% | 15.5% | 84.5% | 0.0% |
| rbqig_b4_no_combo | 31.2% | 0.0% | 15.5% | 84.5% | 0.0% |
| rbqig_b6 | 34.3% | 0.0% | 23.2% | 76.8% | 0.0% |
