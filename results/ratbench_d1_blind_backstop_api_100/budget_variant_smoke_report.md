# RB-QIG Budget Variant Smoke Report

Date: 2026-06-27

This is an exploratory 40-record smoke test on the blind-backstop public RAT-Bench outputs. It checks whether stricter (`rbqig_b2`) or looser utility-budget (`rbqig_b6`) RB-QIG variants justify a full 100-record LLM attacker and utility-judge expansion.

The smoke used the first 40 records for each budget variant. Direct, blanket QI, and balanced (`rbqig_b4`) values are recomputed from the existing cached 100-record outputs on the same first 40 records.

## First-40 LLM Utility

| Method | n | Label preserved | LLM fact preservation | Semantic utility |
|---|---:|---:|---:|---:|
| Direct | 40 | 97.5% | 80.8% | 82.0% |
| Blanket QI | 40 | 97.5% | 53.2% | 65.0% |
| RB-QIG strict | 40 | 100.0% | 56.8% | 64.0% |
| RB-QIG balanced | 40 | 100.0% | 59.1% | 65.0% |
| RB-QIG utility | 40 | 97.5% | 56.5% | 60.5% |

## First-40 LLM Attacker

| Method | n | Record compromise | Exact attr leak | Coarse attr leak | Risk-weighted leak |
|---|---:|---:|---:|---:|---:|
| Direct | 40 | 45.0% | 72.6% | 77.0% | 75.5% |
| Blanket QI | 40 | 2.5% | 13.5% | 16.9% | 13.6% |
| RB-QIG strict | 40 | 0.0% | 12.1% | 13.3% | 11.8% |
| RB-QIG balanced | 40 | 2.5% | 9.2% | 11.3% | 8.6% |
| RB-QIG utility | 40 | 0.0% | 11.9% | 15.2% | 12.4% |

## Interpretation

- This smoke does not justify a full budget-sweep expansion.
- RB-QIG balanced is not worse than strict on semantic utility in the first 40 rows and has lower LLM-attacker risk-weighted leakage.
- RB-QIG utility is not a useful public frontier point in this smoke: it has lower semantic utility and higher attacker leakage than balanced.
- Keep the main paper focused on `rbqig_b4`; treat this as a negative exploratory result.

## API Cost

Fresh-equivalent cost for the four smoke runs:

| Run | Calls | Estimated cost |
|---|---:|---:|
| Utility judge, RB-QIG strict | 40 | $0.033425 |
| Utility judge, RB-QIG utility | 40 | $0.033659 |
| LLM attacker, RB-QIG strict | 40 | $0.020278 |
| LLM attacker, RB-QIG utility | 40 | $0.020684 |
| Total | 160 | $0.108046 |
