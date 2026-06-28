# Presidio-Style Pattern Baseline

This report adds a practical direct-PII baseline without downloading a spaCy NER
model. It uses the Presidio analyzer framework with a blank tokenizer and custom
pattern recognizers for emails, phone numbers, URLs, SSNs, ZIP-like numbers,
case-code-like numbers, and self-introduction names. Because it has no learned
NER model, it should be interpreted as a pattern-only practical lower bound, not
as full Presidio with person/location/organization NER.

No OpenAI API calls are made.

## Commands

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/presidio_pattern_baseline.py --input data/processed/ratbench_english_d1_100_api_qi.jsonl --out results/presidio_pattern_ratbench_d1_100/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/presidio_pattern_baseline.py --input data/processed/tab_echr_dev_30.jsonl --out results/presidio_pattern_tab_echr_dev_30/anonymized_outputs.jsonl
```

The comparison files combine the Presidio-style baseline with the existing
direct, blanket QI, and RB-QIG balanced outputs:

- `results/presidio_pattern_ratbench_d1_100/combined_outputs.jsonl`
- `results/presidio_pattern_tab_echr_dev_30/combined_outputs.jsonl`

## RAT-Bench English D1 100

Source: `results/presidio_pattern_ratbench_d1_100/metrics.csv`

| Method | Direct ID leak | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Token change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Direct oracle-assisted | 0.0% | 92.0% | 94.9% | 94.9% | 93.8% | 0.9% |
| Presidio pattern-only | 37.0% | 90.0% | 85.3% | 85.3% | 85.0% | 1.5% |
| Blanket QI | 0.0% | 1.0% | 0.3% | 0.3% | 0.3% | 7.1% |
| RB-QIG balanced | 0.0% | 1.0% | 0.8% | 63.0% | 28.6% | 7.0% |

Bootstrap source:
`results/presidio_pattern_ratbench_d1_100/bootstrap_report.md`

- Presidio pattern-only risk-weighted leakage: 85.0% [80.6, 89.0]
- Presidio pattern-only direct identifier leakage: 37.0% [28.0, 46.0]
- Presidio pattern-only minus RB-QIG balanced risk-weighted leakage: +56.4
  points [51.0, 61.5]

Interpretation:

- The paper's existing direct baseline is conservative because it receives
  benchmark direct identifiers and removes all direct-ID leaks.
- A practical pattern-only Presidio-style baseline leaves direct identifiers in
  37% of RAT-Bench rows and still leaves high quasi-identifier leakage.
- This supports the main residual-risk framing without needing a full
  production de-identification pipeline.

## TAB ECHR 30

Source: `results/presidio_pattern_tab_echr_dev_30/metrics.csv`

| Method | Direct ID leak | Record compromise | Exact QI leak | Risk-weighted leak | Token change |
| --- | ---: | ---: | ---: | ---: | ---: |
| Direct oracle-assisted | 0.0% | 100.0% | 99.7% | 99.8% | 1.0% |
| Presidio pattern-only | 100.0% | 100.0% | 99.7% | 99.8% | 0.4% |
| Blanket QI | 0.0% | 0.0% | 0.0% | 0.0% | 14.0% |
| RB-QIG balanced | 0.0% | 0.0% | 0.0% | 12.3% | 13.9% |

Bootstrap source:
`results/presidio_pattern_tab_echr_dev_30/bootstrap_report.md`

- Presidio pattern-only direct identifier leakage: 100.0% [100.0, 100.0]
- Presidio pattern-only risk-weighted leakage: 99.8% [99.4, 100.0]
- Presidio pattern-only minus RB-QIG balanced risk-weighted leakage: +87.5
  points [83.9, 90.6]

Interpretation:

- Pattern-only recognizers do not catch the legal names and case identifiers
  marked as direct identifiers in TAB.
- This is a useful negative result: legal-domain de-identification needs NER or
  domain-specific identifiers, not just common PII patterns.
- It should not be framed as a full Presidio evaluation.
