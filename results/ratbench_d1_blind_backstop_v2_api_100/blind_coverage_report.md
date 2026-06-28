# Blind Extractor Coverage Report

Coverage is measured against original benchmark quasi-identifier spans.
A benchmark QI is covered when its normalized span overlaps a blind-extracted span in the same record.

## Overall

- Benchmark QI spans: 283
- Span coverage: 99.6% (282/283)
- Risk-weighted span coverage: 99.8%

## Coverage by Category

| Category | QI spans | Span coverage | Risk-weighted coverage |
| --- | ---: | ---: | ---: |
| date | 38 | 100.0% | 100.0% |
| demographic | 127 | 99.2% | 99.4% |
| location | 1 | 100.0% | 100.0% |
| other | 117 | 100.0% | 100.0% |

## Top Missed Attributes

| Attribute | Missed spans | Missed risk weight |
| --- | ---: | ---: |
| sex | 1 | 2.0 |

## High-Risk Miss Examples

| Record | Attribute | Category | Risk | Span |
| --- | ---: | ---: | ---: | ---: |
| ratbench_english_19 | sex | demographic | 2 | male |
