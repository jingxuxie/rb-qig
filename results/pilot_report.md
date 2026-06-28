# RB-QIG Synthetic Pilot Report

Records: 30
Seed: 7
API calls: 0

## Main Table

| Method | Direct ID leak | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Label preservation | Utility facts | Token change |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| None | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% |
| Direct | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 13.4% |
| Blanket QI | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 43.3% | 63.7% |
| RB-QIG strict | 0.0% | 0.0% | 0.0% | 32.8% | 16.1% | 100.0% | 48.3% | 59.0% |
| RB-QIG balanced | 0.0% | 0.0% | 0.0% | 49.1% | 23.6% | 100.0% | 71.7% | 58.5% |
| RB-QIG utility | 0.0% | 0.0% | 0.0% | 77.9% | 38.1% | 100.0% | 95.0% | 56.2% |

## Fast Interpretation

- Direct redaction leaves 100.0% risk-weighted quasi-identifier leakage in this controlled pilot.
- RB-QIG balanced leaves 23.6% risk-weighted leakage while preserving 71.7% of utility facts.
- Blanket QI redaction preserves 43.3% of utility facts.

This supports the planned paper framing only as a synthetic control: direct PII removal is insufficient, blanket QI redaction damages utility, and risk-budgeted generalization exposes a tunable privacy-utility tradeoff.

## Important Limitation

The current run uses synthetic ground-truth quasi-identifier spans. It validates the pipeline mechanics but not extraction robustness. The next publishable step is an API-extracted or public-benchmark run on RAT-Bench records.
