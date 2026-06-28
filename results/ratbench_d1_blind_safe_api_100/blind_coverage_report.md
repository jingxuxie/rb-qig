# Blind Extractor Coverage Report

Coverage is measured against original benchmark quasi-identifier spans.
A benchmark QI is covered when its normalized span overlaps a blind-extracted span in the same record.

## Overall

- Benchmark QI spans: 283
- Span coverage: 97.5% (276/283)
- Risk-weighted span coverage: 97.7%

## Coverage by Category

| Category | QI spans | Span coverage | Risk-weighted coverage |
| --- | ---: | ---: | ---: |
| date | 38 | 100.0% | 100.0% |
| demographic | 127 | 97.6% | 97.6% |
| location | 1 | 100.0% | 100.0% |
| other | 117 | 96.6% | 96.6% |

## Top Missed Attributes

| Attribute | Missed spans | Missed risk weight |
| --- | ---: | ---: |
| schl | 2 | 6.0 |
| rac2p | 2 | 6.0 |
| marital_status | 2 | 6.0 |
| sex | 1 | 2.0 |

## High-Risk Miss Examples

| Record | Attribute | Category | Risk | Span |
| --- | ---: | ---: | ---: | ---: |
| ratbench_english_64 | marital_status | demographic | 3 | separated |
| ratbench_english_99 | marital_status | demographic | 3 | separated |
| ratbench_english_48 | rac2p | other | 3 | other Micronesian or in combination with other |
| ratbench_english_52 | rac2p | other | 3 | Filipino |
| ratbench_english_15 | schl | other | 3 | grade 10 |
| ratbench_english_32 | schl | other | 3 | grade 8 |
| ratbench_english_19 | sex | demographic | 2 | male |
