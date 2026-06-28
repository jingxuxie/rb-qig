# QI Semantic Specificity: synthetic_100_priority0

This no-API diagnostic uses benchmark quasi-identifier annotations.
Per QI, exact retained spans score 1.0, typed generalizations score 0.65,
bare placeholders score 0.25, and dropped information scores 0.0.
It is a semantic-specificity proxy, not a downstream task-accuracy metric.

| Method | Utility-weighted specificity | Exact | Generalized | Placeholder | Dropped |
| --- | ---: | ---: | ---: | ---: | ---: |
| none | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| direct | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| blanket_qi | 25.0% | 0.0% | 0.0% | 100.0% | 0.0% |
| rbqig_b2 | 37.0% | 0.0% | 32.8% | 67.2% | 0.0% |
| rbqig_b4 | 43.9% | 0.0% | 49.1% | 50.9% | 0.0% |
| rbqig_b4_no_combo | 43.9% | 0.0% | 49.1% | 50.9% | 0.0% |
| rbqig_b6 | 55.6% | 0.0% | 77.9% | 22.1% | 0.0% |
