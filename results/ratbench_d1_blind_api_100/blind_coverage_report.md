# Blind Extractor Coverage Report

Coverage is measured against original benchmark quasi-identifier spans.
A benchmark QI is covered when its normalized span overlaps a blind-extracted span in the same record.

## Overall

- Benchmark QI spans: 283
- Span coverage: 72.8% (206/283)
- Risk-weighted span coverage: 76.4%

## Coverage by Category

| Category | QI spans | Span coverage | Risk-weighted coverage |
| --- | ---: | ---: | ---: |
| date | 38 | 100.0% | 100.0% |
| demographic | 127 | 63.8% | 65.5% |
| location | 1 | 100.0% | 100.0% |
| other | 117 | 73.5% | 73.5% |

## Top Missed Attributes

| Attribute | Missed spans | Missed risk weight |
| --- | ---: | ---: |
| sex | 25 | 50.0 |
| schl | 15 | 45.0 |
| esr | 13 | 39.0 |
| marital_status | 13 | 39.0 |
| citizenship_status | 8 | 24.0 |
| rac2p | 3 | 9.0 |

## High-Risk Miss Examples

| Record | Attribute | Category | Risk | Span |
| --- | ---: | ---: | ---: | ---: |
| ratbench_english_19 | citizenship_status | demographic | 3 | born in the US |
| ratbench_english_20 | citizenship_status | demographic | 3 | born in the US |
| ratbench_english_23 | citizenship_status | demographic | 3 | born in the US |
| ratbench_english_26 | citizenship_status | demographic | 3 | born in the US |
| ratbench_english_57 | citizenship_status | demographic | 3 | born in the US |
| ratbench_english_79 | citizenship_status | demographic | 3 | not a citizen of the US |
| ratbench_english_86 | citizenship_status | demographic | 3 | not a citizen of the US |
| ratbench_english_98 | citizenship_status | demographic | 3 | born in the US |
| ratbench_english_13 | marital_status | demographic | 3 | married |
| ratbench_english_15 | marital_status | demographic | 3 | never married or under 15 years old |
| ratbench_english_24 | marital_status | demographic | 3 | divorced |
| ratbench_english_43 | marital_status | demographic | 3 | married |
