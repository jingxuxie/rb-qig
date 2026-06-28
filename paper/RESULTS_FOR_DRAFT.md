# Results to Use in the RB-QIG Draft

Last updated: 2026-06-28

## Supported Claims

The current evidence supports these claims:

1. Direct PII redaction is not sufficient for LLM-ready sensitive text. On the 100-row RAT-Bench English difficulty-1 pilot, direct redaction removes direct identifiers but leaves 93.8% deterministic risk-weighted quasi-identifier leakage and 78.0% LLM-attacker risk-weighted leakage.
2. A naive LLM sanitizer is not enough. It lowers target-aware RAT-Bench LLM-attacker risk-weighted leakage to 46.0%, but remains far leakier than RB-QIG balanced at 5.7%.
3. RB-QIG substantially reduces residual inference risk relative to direct redaction and naive LLM sanitization. On the same public pilot, RB-QIG balanced reduces deterministic risk-weighted leakage to 28.6% and LLM-attacker risk-weighted leakage to 5.7%.
4. A 30-row RAT-Bench difficulty-2 smoke supports the same LLM-attacker story on harder demographic-heavy rows: direct 70.8%, naive LLM sanitizer 56.9%, RB-QIG balanced 13.1% risk-weighted leakage.
5. Stronger-attacker checks are harsher on privacy methods but preserve the direct-redaction failure story. A 20-record target-aware `gpt-5.4-mini` smoke gives direct 77.3%, naive LLM sanitizer 40.2%, RB-QIG balanced 18.0%, and blanket QI 16.0% risk-weighted leakage. A 50-record blind-backstop GPT-5.5 check gives direct 87.8% [81.7, 93.1], RB-QIG balanced 31.9% [24.7, 39.5], and blanket QI 29.7% [22.5, 37.6]; direct minus RB-QIG is +55.9 points [45.0, 65.7], while RB-QIG minus blanket is statistically tied at +2.2 points [-4.7, 9.0].
6. On controlled synthetic records, RB-QIG exposes a tunable privacy-utility frontier. RB-QIG balanced leaves 23.6% risk-weighted leakage while preserving 71.7% utility facts; blanket QI redaction removes leakage but preserves only 43.3% utility facts.
7. A cached LLM utility judge gives a more forgiving semantic view of synthetic utility, but shows only a modest RB-QIG balanced edge over blanket QI: 79.4% vs 76.8%, paired +2.6 points [0.6, 4.8].
8. Public RAT-Bench utility judging is a caveat, not a win: on budget-fixed blind-backstop public outputs, RB-QIG balanced and blanket QI are statistically tied on semantic utility, 62.2% versus 62.6%, paired -0.4 points [-4.2, 3.4]. A 50-record privacy-aware utility screen is negative for RB-QIG versus blanket: -6.4 points [-10.0, -2.8]. A safe-generalization v2 diagnostic removes literal instruction strings but still trails blanket by -5.6 points [-9.2, -1.6].
9. A no-API annotation-derived specificity diagnostic gives a narrow public utility signal: RB-QIG balanced retains more typed/generalized QI semantics than blanket placeholders by +6.8 points [4.7, 9.2] on blind RAT-Bench and +6.2 points [5.5, 6.9] on TAB.
10. A blind public RAT-Bench diagnostic confirms that deployment-style extraction is the main open problem but also gives a cheap improvement path: an improved generic backstop raises blind span coverage from 72.8% to 99.6%; budget-fixed backstopped blind RB-QIG balanced reduces deterministic risk-weighted leakage from direct redaction by 88.9 points [85.0, 92.5]. Under an LLM attacker, budget-fixed backstopped blind RB-QIG balanced reduces risk-weighted leakage from 78.1% [73.3, 82.9] to 6.4% [3.9, 9.1] and is statistically tied with blanket QI.
11. A no-API public deterministic budget frontier supports the budget knob as an interpretable control: on blind RAT-Bench, budgets 2/4/6 give 4.4%/5.4%/7.2% risk-weighted leakage and 30.1%/33.2%/36.4% QI specificity; on TAB, budgets 2/4/6 give 7.8%/12.3%/20.4% leakage and 28.1%/31.2%/34.3% specificity.
12. The pairwise-combination-risk ablation is negative/tied under the balanced budget: `rbqig_b4_no_combo` produces identical transformed text and change logs to `rbqig_b4` on synthetic 100, blind RAT-Bench 100, and TAB 30. Do not claim the pairwise term is independently validated by this pilot.
13. A 40-record public LLM budget-variant smoke does not justify additional API budget for a full LLM budget sweep: on the same first 40 blind-backstop rows, RB-QIG balanced has lower LLM-attacker risk than strict or utility-budget RB-QIG with no semantic-utility loss versus strict.
14. A 30-document TAB ECHR deterministic screen gives a second-domain residual-risk diagnostic: direct redaction leaves 99.8% risk-weighted leakage, while RB-QIG balanced lowers it to 12.3% [9.2, 15.7]. A 10-document TAB legal-task LLM utility screen is inconclusive: blanket QI, RB-QIG balanced, and RB-QIG utility all score 68.0% [62.0, 74.0]; RB-QIG balanced minus blanket is 0.0 points [-10.0, 10.0], and RB-QIG utility minus blanket is 0.0 points [-8.0, 8.0]. A legal-role replacement variant is also negative: it lowers deterministic RB-QIG leakage to 8.3% but scores 62.0% legal-task utility, -6.0 points [-14.0, 2.0] versus blanket QI.
15. A Presidio-style pattern-only baseline is weaker than the oracle-assisted direct baseline: on RAT-Bench it leaves 37.0% direct-ID leakage and 85.0% risk-weighted leakage; on TAB it leaves 100.0% direct-ID leakage because legal names and case identifiers are not common PII patterns.
16. The hardest residual failures are lexical and relational variants: widowhood from bereavement cues, sex from gendered language, education from school-name mentions, citizenship from non-citizen phrasing, and employment or armed-forces status from context.

Do not claim legal anonymization or deployment readiness.

## Bootstrap Uncertainty

Source reports:

- `results/synthetic_100/bootstrap_report.md`
- `results/synthetic_100/llm_utility_bootstrap_report.md`
- `results/ratbench_d1_api_100/bootstrap_report.md`
- `results/ratbench_d1_api_100/llm_bootstrap_report_with_llm_direct.md`
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_report.md`
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_bootstrap_report.md`
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_gpt55_bootstrap_report.md`
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_bootstrap_report.md`
- `results/followup_priority0_20260628/report.md`
- `results/followup_priority0_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_report.md`
- `results/followup_priority0_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_bootstrap_report.md`
- `results/synthetic_30_blind_api/bootstrap_report.md`

Key intervals use a nonparametric paired bootstrap over record IDs with 5,000 resamples.

| Result | Mean | 95% CI |
|---|---:|---:|
| Synthetic RB-QIG balanced risk-weighted leak | 23.6% | [22.9%, 24.5%] |
| Synthetic RB-QIG balanced utility facts | 71.7% | [70.8%, 72.4%] |
| Synthetic blanket QI utility facts | 43.3% | [39.9%, 46.8%] |
| Synthetic RB-QIG minus blanket utility facts | +28.3 pts | [+25.2, +31.6] |
| Synthetic LLM utility RB-QIG balanced semantic utility | 79.4% | [78.2%, 80.6%] |
| Synthetic LLM utility blanket QI semantic utility | 76.8% | [74.8%, 78.4%] |
| Synthetic LLM utility RB-QIG minus blanket semantic utility | +2.6 pts | [+0.6, +4.8] |
| Synthetic LLM utility RB-QIG minus blanket fact preservation | +2.2 pts | [-0.2, +4.8] |
| RAT-Bench deterministic direct risk-weighted leak | 93.8% | [91.0%, 96.3%] |
| RAT-Bench deterministic RB-QIG balanced risk-weighted leak | 28.6% | [25.4%, 31.9%] |
| RAT-Bench deterministic direct minus RB-QIG balanced | +65.2 pts | [+61.4, +68.8] |
| RAT-Bench LLM direct risk-weighted leak | 78.0% | [73.4%, 82.5%] |
| RAT-Bench LLM naive sanitizer risk-weighted leak | 46.0% | [40.1%, 52.0%] |
| RAT-Bench LLM RB-QIG balanced risk-weighted leak | 5.7% | [3.2%, 8.9%] |
| RAT-Bench LLM direct minus RB-QIG balanced | +72.2 pts | [+67.0, +77.4] |
| RAT-Bench LLM naive sanitizer minus RB-QIG balanced | +40.2 pts | [+33.1, +47.1] |
| RAT-Bench LLM RB-QIG balanced minus blanket QI | +0.5 pts | [-2.6, +3.6] |
| RAT-Bench difficulty-2 LLM direct risk-weighted leak | 70.8% | [56.4%, 83.7%] |
| RAT-Bench difficulty-2 LLM naive sanitizer risk-weighted leak | 56.9% | [42.6%, 71.3%] |
| RAT-Bench difficulty-2 LLM RB-QIG balanced risk-weighted leak | 13.1% | [3.3%, 25.0%] |
| RAT-Bench difficulty-2 LLM direct minus RB-QIG balanced | +57.6 pts | [+42.4, +72.8] |
| RAT-Bench difficulty-2 LLM naive sanitizer minus RB-QIG balanced | +43.8 pts | [+28.9, +58.4] |
| Stronger attacker direct risk-weighted leak | 77.3% | [64.1%, 88.9%] |
| Stronger attacker naive sanitizer risk-weighted leak | 40.2% | [29.4%, 51.1%] |
| Stronger attacker RB-QIG balanced risk-weighted leak | 18.0% | [10.4%, 26.2%] |
| Stronger attacker direct minus RB-QIG balanced | +59.3 pts | [+46.3, +72.4] |
| Stronger attacker naive sanitizer minus RB-QIG balanced | +22.2 pts | [+11.0, +34.2] |
| Blind RAT-Bench direct risk-weighted leak | 94.3% | [91.3%, 96.8%] |
| Blind RAT-Bench RB-QIG balanced risk-weighted leak | 5.4% | [2.8%, 8.5%] |
| Blind RAT-Bench direct minus RB-QIG balanced | +88.9 pts | [+85.0, +92.5] |
| Blind RAT-Bench RB-QIG balanced minus blanket QI | +2.3 pts | [+0.6, +4.9] |
| Blind RAT-Bench LLM direct risk-weighted leak | 78.1% | [73.3%, 82.9%] |
| Blind RAT-Bench LLM RB-QIG balanced risk-weighted leak | 6.4% | [3.9%, 9.1%] |
| Blind RAT-Bench LLM direct minus RB-QIG balanced | +71.8 pts | [+66.4, +76.9] |
| Blind RAT-Bench LLM RB-QIG balanced minus blanket QI | -0.5 pts | [-2.5, +1.5] |
| Blind RAT-Bench GPT-5.5 direct risk-weighted leak | 87.8% | [81.7%, 93.1%] |
| Blind RAT-Bench GPT-5.5 RB-QIG balanced risk-weighted leak | 31.9% | [24.7%, 39.5%] |
| Blind RAT-Bench GPT-5.5 blanket QI risk-weighted leak | 29.7% | [22.5%, 37.6%] |
| Blind RAT-Bench GPT-5.5 direct minus RB-QIG balanced | +55.9 pts | [+45.0, +65.7] |
| Blind RAT-Bench GPT-5.5 RB-QIG minus blanket QI | +2.2 pts | [-4.7, +9.0] |
| Blind RAT-Bench LLM utility direct semantic utility | 86.2% | [83.2%, 88.8%] |
| Blind RAT-Bench LLM utility blanket QI semantic utility | 62.6% | [59.2%, 66.0%] |
| Blind RAT-Bench LLM utility RB-QIG balanced semantic utility | 62.2% | [58.8%, 65.2%] |
| Blind RAT-Bench LLM utility RB-QIG minus blanket semantic utility | -0.4 pts | [-4.2, +3.4] |
| Blind RAT-Bench LLM utility RB-QIG minus blanket fact preservation | +1.7 pts | [-3.4, +6.6] |
| Blind RAT-Bench privacy-aware utility blanket QI | 88.0% | [84.8%, 91.2%] |
| Blind RAT-Bench privacy-aware utility RB-QIG balanced | 81.6% | [78.8%, 84.4%] |
| Blind RAT-Bench privacy-aware utility RB-QIG minus blanket | -6.4 pts | [-10.0, -2.8] |
| Blind RAT-Bench safe-v2 privacy-aware utility RB-QIG balanced | 82.4% | [79.6%, 85.2%] |
| Blind RAT-Bench safe-v2 privacy-aware utility RB-QIG minus blanket | -5.6 pts | [-9.2, -1.6] |
| Blind synthetic RB-QIG balanced risk-weighted leak | 5.2% | [1.7%, 9.7%] |
| Blind synthetic RB-QIG balanced utility facts | 43.3% | [35.0%, 51.7%] |
| Blind synthetic RB-QIG balanced minus blanket utility facts | +7.2 pts | [+3.3, +11.7] |

The uncertainty analysis strengthens the direct-redaction residual-risk claim. It also clarifies the main caveat: RB-QIG is statistically tied with blanket QI on both target-aware and blind-backstop RAT-Bench LLM privacy, and public blind-backstop utility judging does not show a meaningful RB-QIG utility advantage. Deterministic blind scoring still penalizes RB-QIG more than blanket because generalized coarse cues can match benchmark attributes. The utility advantage over blanket redaction should be claimed from the controlled synthetic benchmark, not from the current public RAT-Bench pilot.

## Main Synthetic Table

Source: `results/synthetic_100/metrics.csv`

| Method | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Utility facts | Token change |
|---|---:|---:|---:|---:|---:|---:|
| None | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% |
| Direct | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 13.5% |
| Blanket QI | 0.0% | 0.0% | 0.0% | 0.0% | 43.3% | 63.7% |
| RB-QIG strict | 0.0% | 0.0% | 32.8% | 16.1% | 48.3% | 59.3% |
| RB-QIG balanced | 0.0% | 0.0% | 49.1% | 23.6% | 71.7% | 59.0% |
| RB-QIG utility | 0.0% | 0.0% | 77.9% | 38.0% | 95.0% | 56.6% |

## Public RAT-Bench Deterministic Table

Source: `results/ratbench_d1_api_100/metrics.csv`

| Method | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Utility facts | Token change |
|---|---:|---:|---:|---:|---:|---:|
| None | 92.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% |
| Direct | 92.0% | 94.9% | 94.9% | 93.8% | 100.0% | 0.9% |
| Blanket QI | 1.0% | 0.3% | 0.3% | 0.3% | 100.0% | 7.1% |
| RB-QIG strict | 1.0% | 0.3% | 51.8% | 23.1% | 100.0% | 7.0% |
| RB-QIG balanced | 1.0% | 0.8% | 63.0% | 28.6% | 100.0% | 7.0% |
| RB-QIG utility | 1.0% | 0.8% | 72.2% | 33.2% | 100.0% | 6.9% |

## Public RAT-Bench LLM Attacker Table

Source: `results/ratbench_d1_api_100/llm_attacker_metrics_with_llm_direct.csv`

| Method | Record compromise | Exact attr leak | Coarse attr leak | Risk-weighted leak |
|---|---:|---:|---:|---:|
| Direct | 76.0% | 74.9% | 81.2% | 78.0% |
| LLM direct | 34.0% | 48.7% | 52.8% | 46.0% |
| Blanket QI | 3.0% | 3.9% | 7.3% | 5.3% |
| RB-QIG balanced | 2.0% | 4.0% | 8.8% | 5.7% |

## Blind Public RAT-Bench Diagnostic Table

Source: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/metrics.csv`

| Method | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Utility facts | Token change |
|---|---:|---:|---:|---:|---:|---:|
| Direct | 39.0% | 94.4% | 94.4% | 94.3% | 100.0% | 0.9% |
| Blanket QI | 0.0% | 3.1% | 3.1% | 3.1% | 100.0% | 10.8% |
| RB-QIG balanced | 0.0% | 4.6% | 6.4% | 5.4% | 100.0% | 10.1% |

Interpret this as a coverage stress test, not a utility result. The improved generic backstop raises benchmark QI span coverage from 72.8% to 99.6% with zero additional API calls. Backstopped blind RB-QIG catches enough risky spans to beat direct redaction sharply, but remains slightly leakier than blanket QI because coarse generalized cues can still support attribute recovery.

## Blind Public RAT-Bench LLM Attacker Table

Source: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_metrics.csv`

| Method | Record compromise | Exact attr leak | Coarse attr leak | Risk-weighted leak |
|---|---:|---:|---:|---:|
| Direct | 37.0% | 74.9% | 81.2% | 78.1% |
| Blanket QI | 1.0% | 5.4% | 8.3% | 6.8% |
| RB-QIG balanced | 1.0% | 5.3% | 7.4% | 6.4% |

Interpret this as the stronger deployment-style privacy check. The LLM attacker sees a large direct-to-RBQIG reduction and no meaningful RB-QIG versus blanket difference, despite deterministic coarse-leakage scoring being harsher on RB-QIG.

## GPT-5.5 Blind Public Strong-Attacker Table

Source: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_gpt55_metrics.csv`

| Method | Record compromise | Exact attr leak | Coarse attr leak | Risk-weighted leak |
|---|---:|---:|---:|---:|
| Direct | 40.0% | 86.4% | 90.1% | 87.8% |
| Blanket QI | 2.0% | 26.3% | 36.3% | 29.7% |
| RB-QIG balanced | 2.0% | 28.6% | 38.9% | 31.9% |

Interpret this as a robustness caveat. GPT-5.5 infers many more broad attributes from both privacy methods than the cheaper attacker, but direct redaction remains much leakier than RB-QIG balanced. RB-QIG balanced is statistically tied with blanket QI: +2.2 points [-4.7, +9.0].

## Synthetic LLM Utility Judge Table

Source: `results/synthetic_100/llm_utility_metrics.csv`

| Method | Label preserved | LLM fact preservation | Semantic utility |
|---|---:|---:|---:|
| Direct | 100.0% | 75.3% | 83.2% |
| Blanket QI | 99.0% | 69.1% | 76.8% |
| RB-QIG balanced | 100.0% | 71.3% | 79.4% |

Interpret this as a secondary utility check. It shows that generic placeholders can remain semantically useful for broad downstream decisions, but RB-QIG balanced still gives a small semantic-utility gain over blanket QI. The deterministic utility-fact result remains the stronger evidence for a large utility gap.

## Blind Public RAT-Bench LLM Utility Judge Table

Source: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_metrics.csv`

| Method | Label preserved | LLM fact preservation | Semantic utility |
|---|---:|---:|---:|
| Direct | 99.0% | 84.3% | 86.2% |
| Blanket QI | 99.0% | 53.8% | 62.6% |
| RB-QIG balanced | 96.0% | 55.5% | 62.2% |

Interpret this as a public utility caveat. Both privacy methods lose substantial semantic utility relative to direct redaction, and RB-QIG balanced is statistically tied with blanket QI on semantic utility: -0.4 points [-4.2, +3.4].

## Figures

- Synthetic privacy-utility frontier: `results/synthetic_100/figures/privacy_utility_frontier.svg`
- Synthetic leakage by method: `results/synthetic_100/figures/leakage_by_method.svg`
- RAT-Bench privacy-utility frontier: `results/ratbench_d1_api_100/figures/privacy_utility_frontier.svg`
- RAT-Bench leakage by method: `results/ratbench_d1_api_100/figures/leakage_by_method.svg`
- Blind RAT-Bench metrics: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/metrics.csv`
- Blind RAT-Bench bootstrap report: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_report.md`
- Blind RAT-Bench coverage report: `results/ratbench_d1_blind_backstop_v2_api_100/blind_coverage_report.md`
- Blind RAT-Bench LLM attacker metrics: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_metrics.csv`
- Blind RAT-Bench LLM attacker bootstrap report: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_bootstrap_report.md`
- Blind RAT-Bench GPT-5.5 attacker metrics: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_gpt55_metrics.csv`
- Blind RAT-Bench GPT-5.5 attacker bootstrap report: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_gpt55_bootstrap_report.md`
- Blind RAT-Bench LLM failure taxonomy: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_failure_taxonomy.md`
- Blind RAT-Bench figures: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/figures/`
- LLM-attacker outputs with naive sanitizer: `results/ratbench_d1_api_100/llm_attacker_outputs_with_llm_direct.jsonl`
- LLM-attacker metrics with naive sanitizer: `results/ratbench_d1_api_100/llm_attacker_metrics_with_llm_direct.csv`
- LLM-attacker bootstrap with naive sanitizer: `results/ratbench_d1_api_100/llm_bootstrap_report_with_llm_direct.md`
- LLM-attacker failure taxonomy: `results/ratbench_d1_api_100/failure_taxonomy.md`
- LLM utility judge outputs: `results/synthetic_100/llm_utility_outputs.jsonl`
- LLM utility judge metrics: `results/synthetic_100/llm_utility_metrics.csv`
- LLM utility bootstrap report: `results/synthetic_100/llm_utility_bootstrap_report.md`
- Blind RAT-Bench LLM utility judge outputs: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_outputs.jsonl`
- Blind RAT-Bench LLM utility judge metrics: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_metrics.csv`
- Blind RAT-Bench LLM utility bootstrap report: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_bootstrap_report.md`
- Blind RAT-Bench budget-fix report: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/budgetfix_report.md`
- Blind RAT-Bench privacy-aware utility screen: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/privacy_aware_utility_50_report.md`
- Blind RAT-Bench safe-generalization v2 diagnostic: `results/ratbench_d1_blind_backstop_v2_safe_budgetfix_api_100/safe_generalization_v2_report.md`
- Blind RAT-Bench budget-variant smoke report: `results/ratbench_d1_blind_backstop_api_100/budget_variant_smoke_report.md`
- Priority 0 follow-up report: `results/followup_priority0_20260628/report.md`
- Priority 0 blind RAT-Bench deterministic metrics: `results/followup_priority0_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/metrics.csv`
- Priority 0 TAB deterministic metrics: `results/followup_priority0_20260628/tab_echr_dev_30/metrics.csv`
- Blind synthetic diagnostic: `results/synthetic_30_blind_api/metrics.csv`
- Blind synthetic bootstrap report: `results/synthetic_30_blind_api/bootstrap_report.md`
- TAB ECHR deterministic screen: `results/tab_echr_dev_30/tab_screen_report.md`
- TAB ECHR metrics: `results/tab_echr_dev_30/metrics.csv`
- TAB ECHR bootstrap report: `results/tab_echr_dev_30/bootstrap_report.md`
- TAB ECHR legal-task LLM utility screen: `results/tab_echr_dev_30/llm_legal_utility_10_with_b6_bootstrap_report.md`
- TAB legal-role diagnostic: `results/tab_echr_dev_30_legal_role/legal_role_screen_report.md`
- Presidio-style pattern baseline report: `results/presidio_pattern_baseline_report.md`
- Presidio-style RAT-Bench metrics: `results/presidio_pattern_ratbench_d1_100/metrics.csv`
- Presidio-style TAB metrics: `results/presidio_pattern_tab_echr_dev_30/metrics.csv`
- Generated Markdown tables: `paper/generated/tables.md`
- Generated LaTeX tables: `paper/generated/tables.tex`
- Qualitative appendix with representative examples and failure mode: `paper/QUALITATIVE_APPENDIX.md`
- Qualitative appendix generator: `src/make_qualitative_appendix.py`
- Paper claim audit: `paper/CLAIM_AUDIT.md`
- Paper claim audit generator: `src/make_claim_audit.py`
- Plan-to-evidence audit: `paper/PLAN_TO_EVIDENCE_AUDIT.md`
- Reviewer-facing stress test: `paper/REVIEWER_STRESS_TEST.md`
- LaTeX manuscript source: `paper/main.tex`
- Bibliography: `paper/references.bib`
- Compiled 5-page COLM PDF: `paper/main.pdf`

## Recommended Paper Framing

Use a two-part empirical story:

1. Synthetic controlled benchmark: demonstrates the privacy-utility tradeoff and why generalization can be better than blanket redaction when utility facts matter.
2. Public RAT-Bench pilot: confirms that a low-cost LLM attacker can infer many target attributes after direct redaction and after a naive LLM sanitizer, and that RB-QIG-style quasi-identifier handling greatly reduces this residual risk.
3. Stronger-attacker caveat: GPT-5.5 recovers substantially more from both RB-QIG and blanket QI than the cheaper attacker. The direct-to-RB-QIG reduction survives, but the result argues against any near-zero residual-risk claim.
4. Synthetic LLM utility judge: gives a more semantic utility read. It supports only a modest RB-QIG balanced edge over blanket QI, which is useful because it prevents overclaiming from the stricter deterministic fact metric alone.
5. Public LLM utility judge: gives the counterweight. On budget-fixed blind-backstop RAT-Bench, RB-QIG balanced is statistically tied with blanket QI on semantic utility, so do not claim a public utility advantage.
6. Blind extractor diagnostics: show that deployment-style extraction can catch privacy risks but remains the bottleneck. On public RAT-Bench, an improved deterministic backstop cheaply raises coverage to 99.6% and cuts RB-QIG balanced deterministic leakage to 5.4% [2.8%, 8.5%]. Under the LLM attacker, blind RB-QIG balanced drops to 6.4% [3.9%, 9.1%] and is statistically tied with blanket QI; on synthetic data, blind RB-QIG preserves 43.3% [35.0%, 51.7%] utility facts at 5.2% [1.7%, 9.7%] oracle-measured risk-weighted leakage.
7. Budget diagnostics: keep the main paper on RB-QIG balanced. The deterministic public frontier shows the budget knob behaves monotonically in the expected direction, but the first-40 public LLM smoke did not find a better strict or utility-budget frontier point.
8. Pairwise no-combo ablation: report only as a limitation/diagnostic if space allows. The balanced no-combo variant is identical to balanced RB-QIG on all evaluated datasets, so the current pilot does not isolate the pairwise combination term.

Be explicit that the current RAT-Bench extraction is target-aware, not blind deployment extraction. Frame it as a controlled transformation benchmark: given target quasi-identifiers, how should they be transformed under a risk budget?

## Failure Taxonomy Categories

Use the generated failure-taxonomy tables from `results/ratbench_d1_api_100/failure_taxonomy.md` and `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_failure_taxonomy.md`.
The key residual leakage categories are:

- gendered context,
- marital or bereavement context,
- education institution or credential,
- citizenship phrasing,
- employment or armed-forces status,
- race or ethnicity variants.
