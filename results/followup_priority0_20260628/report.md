# Priority 0 Follow-up Experiments

No API calls were used. All rows are deterministic evaluations over existing public or synthetic records.

## Pairwise-Combination-Risk Ablation

| Dataset | Method | Risk-weighted leakage | Utility/fact preservation | Token change |
| --- | ---: | ---: | ---: | ---: |
| Synthetic | RB-QIG balanced | 23.6% | 71.7% | 59.0% |
| Synthetic | RB-QIG no-combo | 23.6% | 71.7% | 59.0% |
| RAT-Bench blind | RB-QIG balanced | 5.4% | 100.0% | 10.1% |
| RAT-Bench blind | RB-QIG no-combo | 5.4% | 100.0% | 10.1% |
| TAB legal | RB-QIG balanced | 12.3% | 100.0% | 13.9% |
| TAB legal | RB-QIG no-combo | 12.3% | 100.0% | 13.9% |

### Interpretation

- Synthetic: no-combo is effectively tied with balanced on deterministic leakage.
- RAT-Bench blind: no-combo is effectively tied with balanced on deterministic leakage.
- TAB legal: no-combo is effectively tied with balanced on deterministic leakage.

### Mechanism Check

| Dataset | Identical transformed text | Identical change logs | Mean risk after balanced | Mean risk after no-combo |
| --- | ---: | ---: | ---: | ---: |
| Synthetic | 100.0% | 100.0% | 3.20 | 3.20 |
| RAT-Bench blind | 100.0% | 100.0% | 4.00 | 4.00 |
| TAB legal | 100.0% | 100.0% | 4.00 | 4.00 |

## Public Deterministic Budget Frontier

| Dataset | Budget | Risk-weighted leakage | QI specificity | Token change |
| --- | ---: | ---: | ---: | ---: |
| RAT-Bench blind | 2 | 4.4% | 30.1% | 10.4% |
| RAT-Bench blind | 4 | 5.4% | 33.2% | 10.1% |
| RAT-Bench blind | 6 | 7.2% | 36.4% | 9.9% |
| TAB legal | 2 | 7.8% | 28.1% | 13.9% |
| TAB legal | 4 | 12.3% | 31.2% | 13.9% |
| TAB legal | 6 | 20.4% | 34.3% | 13.9% |

## Paper-Facing Conclusion

The no-combo ablation should be framed as a deterministic diagnostic, not a deployment claim. The public budget frontier supports the budget knob as an interpretable utility-specificity control, while public utility remains weaker than in the controlled synthetic setting.
