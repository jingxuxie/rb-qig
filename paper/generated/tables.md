# Generated Paper Tables

Cells are percentages. The manuscript tables report point estimates for compactness.

## Synthetic Controlled Benchmark

| Method | Risk-weighted leak | Utility facts | Token change |
| --- | ---: | ---: | ---: |
| None | 100.0 | 100.0 | 0.0 |
| Direct | 100.0 | 100.0 | 13.5 |
| Blanket QI | 0.0 | 43.3 | 63.7 |
| RB-QIG strict | 16.1 | 48.3 | 59.3 |
| RB-QIG balanced | 23.6 | 71.7 | 59.0 |
| RB-QIG utility | 38.0 | 95.0 | 56.6 |

## RAT-Bench LLM Attacker

| Method | Record compromise | Exact attr leak | Coarse attr leak | Risk-weighted leak |
| --- | ---: | ---: | ---: | ---: |
| Direct | 76.0 | 74.9 | 81.2 | 78.0 |
| LLM direct | 34.0 | 48.7 | 52.8 | 46.0 |
| Blanket QI | 3.0 | 3.9 | 7.3 | 5.3 |
| RB-QIG balanced | 2.0 | 4.0 | 8.8 | 5.7 |

## Synthetic LLM Utility Judge

| Method | Label preserved | LLM fact preservation | Semantic utility |
| --- | ---: | ---: | ---: |
| Direct | 100.0 | 75.3 | 83.2 |
| Blanket QI | 99.0 | 69.1 | 76.8 |
| RB-QIG balanced | 100.0 | 71.3 | 79.4 |

## Blind Public RAT-Bench Stress Test

| Method | LLM risk-weighted leak | Semantic utility | LLM fact preservation |
| --- | ---: | ---: | ---: |
| Direct | 78.1 | 86.2 | 84.3 |
| Blanket QI | 6.8 | 62.6 | 53.8 |
| RB-QIG balanced | 6.4 | 62.2 | 55.5 |

## Blind Synthetic Diagnostic

| Method | Risk-weighted leak | Utility facts | Token change |
| --- | ---: | ---: | ---: |
| Direct | 100.0 | 100.0 | 13.4 |
| Blanket QI | 3.2 | 36.1 | 62.9 |
| RB-QIG balanced | 5.2 | 43.3 | 55.8 |
