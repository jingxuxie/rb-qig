# Paper Claim Audit

Generated from local CSV/report artifacts. No API calls are made.

Summary: 15/15 audited claim groups have matching paper snippets.

| Claim | Description | Paper check | Interpretation |
| --- | --- | --- | --- |
| C1 | Controlled synthetic frontier headline. | PASS | Supports the large utility-preservation claim only in the controlled setting. |
| C2 | Synthetic RB-QIG utility advantage over blanket redaction. | PASS | This is the strongest utility result and should stay scoped to synthetic utility facts. |
| C3 | Synthetic LLM utility judge gives only a modest semantic edge. | PASS | Prevents overclaiming from the deterministic synthetic utility metric. |
| C4 | Target-aware RAT-Bench LLM attacker headline. | PASS | Supports residual-risk reduction relative to direct and naive LLM redaction. |
| C5 | Target-aware paired LLM-attacker reductions and blanket tie. | PASS | The CI crossing zero for RB-QIG minus blanket supports the tied-privacy caveat. |
| C6 | Difficulty-2 smoke maintains the same qualitative ordering. | PASS | Robustness smoke only; n=30 is not a replacement for the main 100-row table. |
| C7 | Stronger-attacker smoke preserves the main ordering. | PASS | Robustness smoke only; n=20 is intentionally small. |
| C8 | Blind extractor coverage improves with the v2 backstop. | PASS | Supports the extraction-bottleneck discussion without claiming deployment readiness. |
| C9 | Blind deterministic stress-test reduction and deterministic blanket gap. | PASS | Shows strong direct-to-RB-QIG reduction but deterministic scoring still favors blanket QI. |
| C10 | Blind LLM-attacker stress test ties RB-QIG with blanket QI. | PASS | This is the strongest deployment-style privacy claim and includes the blanket-tie caveat. |
| C11 | Public blind utility judge does not support an RB-QIG utility edge. | PASS | Important negative/caveat claim: public utility advantage is not established. |
| C12 | Blind synthetic diagnostic remains a limitation result. | PASS | Supports the limitation paragraph; this should not be framed as solved blind extraction. |
| C13 | TAB ECHR deterministic screen is cross-domain residual-risk support. | PASS | Supports a second-domain residual-risk diagnostic and an inconclusive TAB legal-utility caveat. |
| C14 | Presidio-style pattern baseline is a practical lower-bound diagnostic. | PASS | Supports the practical-baseline caveat without claiming full Presidio coverage. |
| C15 | Annotation-derived public specificity shows a small RB-QIG edge over blanket placeholders. | PASS | Supports a narrow public utility diagnostic while preserving the LLM-utility caveat. |

## C1: Controlled synthetic frontier headline.

Paper snippet check: **PASS**

Sources:
- `results/synthetic_100/metrics.csv`
- `results/synthetic_100/bootstrap_cis.csv`

Evidence:
- RB-QIG balanced risk-weighted leakage: 23.6% [22.9, 24.5]
- RB-QIG balanced utility facts: 71.7% [70.8, 72.4]
- Blanket QI utility facts: 43.3% [39.9, 46.8]

## C2: Synthetic RB-QIG utility advantage over blanket redaction.

Paper snippet check: **PASS**

Sources:
- `results/synthetic_100/bootstrap_contrasts.csv`

Evidence:
- RB-QIG balanced minus blanket utility facts: +28.3 points [25.2, 31.6]

## C3: Synthetic LLM utility judge gives only a modest semantic edge.

Paper snippet check: **PASS**

Sources:
- `results/synthetic_100/llm_utility_metrics.csv`
- `results/synthetic_100/llm_utility_bootstrap_cis.csv`
- `results/synthetic_100/llm_utility_bootstrap_contrasts.csv`

Evidence:
- RB-QIG balanced semantic utility: 79.4% [78.2, 80.6]
- Blanket QI semantic utility: 76.8% [74.8, 78.4]
- RB-QIG balanced minus blanket semantic utility: +2.6 points [0.6, 4.8]

## C4: Target-aware RAT-Bench LLM attacker headline.

Paper snippet check: **PASS**

Sources:
- `results/ratbench_d1_api_100/llm_attacker_metrics_with_llm_direct.csv`
- `results/ratbench_d1_api_100/llm_bootstrap_cis_with_llm_direct.csv`

Evidence:
- Direct risk-weighted leakage: 78.0% [73.4, 82.5]
- Naive LLM sanitizer risk-weighted leakage: 46.0% [40.1, 52.0]
- RB-QIG balanced risk-weighted leakage: 5.7% [3.2, 8.8]

## C5: Target-aware paired LLM-attacker reductions and blanket tie.

Paper snippet check: **PASS**

Sources:
- `results/ratbench_d1_api_100/llm_bootstrap_contrasts_with_llm_direct.csv`

Evidence:
- Direct minus RB-QIG balanced: +72.2 points [67.0, 77.4]
- Naive LLM sanitizer minus RB-QIG balanced: +40.2 points [33.1, 47.1]
- RB-QIG balanced minus blanket QI: +0.5 points [-2.6, 3.6]

## C6: Difficulty-2 smoke maintains the same qualitative ordering.

Paper snippet check: **PASS**

Sources:
- `results/ratbench_d2_api_30/llm_attacker_metrics_with_llm_direct.csv`
- `results/ratbench_d2_api_30/llm_bootstrap_cis_with_llm_direct.csv`

Evidence:
- Direct risk-weighted leakage: 70.8% [56.4, 83.7]
- Naive LLM sanitizer risk-weighted leakage: 56.9% [42.6, 71.3]
- RB-QIG balanced risk-weighted leakage: 13.1% [3.3, 25.0]

## C7: Stronger-attacker smoke preserves the main ordering.

Paper snippet check: **PASS**

Sources:
- `results/ratbench_d1_api_100/llm_attacker_stronger20_metrics.csv`
- `results/ratbench_d1_api_100/llm_attacker_stronger20_bootstrap_cis.csv`

Evidence:
- Direct risk-weighted leakage: 77.3% [64.1, 88.9]
- RB-QIG balanced risk-weighted leakage: 18.0% [10.4, 26.2]
- Blanket QI risk-weighted leakage: 16.0% [9.4, 22.6]

## C8: Blind extractor coverage improves with the v2 backstop.

Paper snippet check: **PASS**

Sources:
- `results/ratbench_d1_blind_api_100/blind_coverage_report.md`
- `results/ratbench_d1_blind_backstop_v2_api_100/blind_coverage_report.md`

Evidence:
- Raw blind span coverage: 72.8%
- V2 backstopped blind span coverage: 99.6%

## C9: Blind deterministic stress-test reduction and deterministic blanket gap.

Paper snippet check: **PASS**

Sources:
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/metrics.csv`
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_cis.csv`
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_contrasts.csv`

Evidence:
- Direct risk-weighted leakage: 94.3% [91.3, 96.8]
- RB-QIG balanced risk-weighted leakage: 5.4% [2.8, 8.5]
- Direct minus RB-QIG balanced: +88.9 points [85.0, 92.5]
- RB-QIG balanced minus blanket QI: +2.3 points [0.6, 4.9]

## C10: Blind LLM-attacker stress test ties RB-QIG with blanket QI.

Paper snippet check: **PASS**

Sources:
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_metrics.csv`
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_bootstrap_cis.csv`
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_bootstrap_contrasts.csv`

Evidence:
- Direct risk-weighted leakage: 78.1% [73.3, 82.9]
- RB-QIG balanced risk-weighted leakage: 6.4% [3.9, 9.1]
- RB-QIG balanced minus blanket QI: -0.5 points [-2.5, 1.5]

## C11: Public blind utility judge does not support an RB-QIG utility edge.

Paper snippet check: **PASS**

Sources:
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_metrics.csv`
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_bootstrap_cis.csv`
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_bootstrap_contrasts.csv`

Evidence:
- Blanket QI semantic utility: 62.6% [59.2, 66.0]
- RB-QIG balanced semantic utility: 62.2% [58.8, 65.2]
- RB-QIG balanced minus blanket semantic utility: -0.4 points [-4.2, 3.4]

## C12: Blind synthetic diagnostic remains a limitation result.

Paper snippet check: **PASS**

Sources:
- `results/synthetic_30_blind_api/bootstrap_cis.csv`

Evidence:
- RB-QIG balanced utility facts: 43.3% [35.0, 51.7]
- RB-QIG balanced risk-weighted leakage: 5.2% [1.7, 9.7]

## C13: TAB ECHR deterministic screen is cross-domain residual-risk support.

Paper snippet check: **PASS**

Sources:
- `results/tab_echr_dev_30/metrics.csv`
- `results/tab_echr_dev_30/bootstrap_cis.csv`
- `results/tab_echr_dev_30/bootstrap_contrasts.csv`
- `results/tab_echr_dev_30/llm_legal_utility_10_bootstrap_cis.csv`
- `results/tab_echr_dev_30/llm_legal_utility_10_bootstrap_contrasts.csv`

Evidence:
- Direct risk-weighted leakage: 99.8% [99.4, 100.0]
- RB-QIG balanced risk-weighted leakage: 12.3% [9.2, 15.7]
- Direct minus RB-QIG balanced: +87.5 points [84.0, 90.6]
- RB-QIG balanced minus blanket QI: +12.3 points [9.1, 15.8]
- RB-QIG balanced legal-task utility: 68.0% [62.0, 74.0]
- Blanket QI legal-task utility: 68.0% [62.0, 74.0]
- RB-QIG balanced minus blanket legal-task utility: 0.0 points [-10.0, 10.0]

## C14: Presidio-style pattern baseline is a practical lower-bound diagnostic.

Paper snippet check: **PASS**

Sources:
- `results/presidio_pattern_ratbench_d1_100/metrics.csv`
- `results/presidio_pattern_ratbench_d1_100/bootstrap_cis.csv`
- `results/presidio_pattern_tab_echr_dev_30/metrics.csv`
- `results/presidio_pattern_tab_echr_dev_30/bootstrap_cis.csv`

Evidence:
- RAT-Bench Presidio-pattern direct identifier leakage: 37.0% [28.0, 46.0]
- RAT-Bench Presidio-pattern risk-weighted leakage: 85.0% [80.6, 89.0]
- TAB Presidio-pattern direct identifier leakage: 100.0% [100.0, 100.0]

## C15: Annotation-derived public specificity shows a small RB-QIG edge over blanket placeholders.

Paper snippet check: **PASS**

Sources:
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_bootstrap_contrasts.csv`
- `results/tab_echr_dev_30/qi_specificity_bootstrap_contrasts.csv`

Evidence:
- Blind RAT-Bench RB-QIG balanced minus blanket specificity: +6.8 points [4.7, 9.2]
- TAB RB-QIG balanced minus blanket specificity: +6.2 points [5.5, 6.9]
