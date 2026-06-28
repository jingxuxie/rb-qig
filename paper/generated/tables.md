# Generated Paper Tables

Cells are percentages. Brackets show bootstrap 95% confidence intervals.

## Synthetic Controlled Benchmark

| Method | Risk-weighted leak | Utility facts | Token change |
| --- | ---: | ---: | ---: |
| None | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] |
| Direct | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 13.5 [12.6, 14.3] |
| Blanket QI | 0.0 [0.0, 0.0] | 43.3 [39.9, 46.8] | 63.7 [62.9, 64.4] |
| RB-QIG strict | 16.1 [15.7, 16.4] | 48.3 [45.3, 51.4] | 59.3 [58.7, 60.0] |
| RB-QIG balanced | 23.6 [22.9, 24.5] | 71.7 [70.8, 72.4] | 59.0 [58.3, 59.7] |
| RB-QIG utility | 38.0 [37.5, 38.4] | 95.0 [93.0, 96.8] | 56.6 [55.8, 57.5] |

## RAT-Bench LLM Attacker

| Method | Record compromise | Exact attr leak | Coarse attr leak | Risk-weighted leak |
| --- | ---: | ---: | ---: | ---: |
| Direct | 76.0 [67.0, 84.0] | 74.9 [69.5, 80.0] | 81.2 [76.8, 85.4] | 78.0 [73.4, 82.5] |
| LLM direct | 34.0 [25.0, 43.0] | 48.7 [42.6, 54.6] | 52.8 [46.5, 58.7] | 46.0 [40.1, 52.0] |
| Blanket QI | 3.0 [0.0, 7.0] | 3.9 [1.5, 7.0] | 7.3 [4.3, 10.8] | 5.3 [2.7, 8.3] |
| RB-QIG balanced | 2.0 [0.0, 5.0] | 4.0 [1.6, 6.9] | 8.8 [5.3, 12.8] | 5.7 [3.2, 8.8] |

## Synthetic LLM Utility Judge

| Method | Label preserved | LLM fact preservation | Semantic utility |
| --- | ---: | ---: | ---: |
| Direct | 100.0 | 75.3 [73.3, 77.3] | 83.2 [81.8, 84.8] |
| Blanket QI | 99.0 | 69.1 [66.6, 71.4] | 76.8 [74.8, 78.4] |
| RB-QIG balanced | 100.0 | 71.3 [69.6, 73.0] | 79.4 [78.2, 80.6] |

## Blind Public RAT-Bench Stress Test

| Method | LLM risk-weighted leak | Semantic utility | LLM fact preservation |
| --- | ---: | ---: | ---: |
| Direct | 78.1 [73.3, 82.9] | 86.2 [83.2, 88.8] | 84.3 [81.2, 87.0] |
| Blanket QI | 6.8 [4.0, 9.9] | 62.6 [59.2, 66.0] | 53.8 [49.5, 58.1] |
| RB-QIG balanced | 6.4 [3.9, 9.1] | 62.2 [58.8, 65.2] | 55.5 [52.0, 58.7] |

## Blind Synthetic Diagnostic

| Method | Risk-weighted leak | Utility facts | Token change |
| --- | ---: | ---: | ---: |
| Direct | 100.0 [100.0, 100.0] | 100.0 [100.0, 100.0] | 13.4 [11.8, 15.1] |
| Blanket QI | 3.2 [0.9, 6.1] | 36.1 [29.4, 43.1] | 62.9 [60.5, 65.3] |
| RB-QIG balanced | 5.2 [1.7, 9.7] | 43.3 [35.0, 51.7] | 55.8 [53.1, 58.3] |
