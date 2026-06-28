# Plan-to-Evidence Audit

Generated from the original project plan and local artifacts. No API calls are
made by this audit.

## Executive Status

The project has enough evidence for a defensible 4-page workshop paper about
residual quasi-identifier risk and a lightweight risk-budgeted transformation
policy. The strongest supported claim is not that RB-QIG is a finished
anonymizer or that it dominates blanket redaction. The strongest supported
claim is that direct PII redaction and naive LLM sanitization leave large
residual LLM-inference risk, while RB-QIG sharply reduces that risk and exposes
a useful privacy-utility frontier in controlled settings.

Current readiness:

| Target | Readiness | Rationale |
| --- | --- | --- |
| Workshop short paper | Strong | 4-page manuscript, generated tables, bootstrap intervals, claim audit, qualitative appendix, and reviewer stress test are in place. |
| High-impact top-tier paper | Promising but incomplete | Now has a bounded TAB legal-domain diagnostic, a pattern-only Presidio-style baseline, a negative TAB legal-utility screen, a negative legal-role replacement check, a no-combo ablation, and a 50-record GPT-5.5 attacker check, but still needs stronger utility tasks before claims can scale beyond a pilot. |

## Research Questions

| Plan item | Current status | Evidence | Paper stance |
| --- | --- | --- | --- |
| RQ1: residual risk after direct PII removal | Supported | RAT-Bench direct redaction leaves 78.0% [73.4, 82.5] target-aware LLM-attacker risk and 78.1% [73.3, 82.9] blind-backstop LLM-attacker risk. | Make this a headline motivation. |
| RQ2: risk-budgeted transformation | Supported relative to direct and naive LLM redaction; not superior to blanket privacy | RB-QIG balanced reduces target-aware LLM risk to 5.7% [3.2, 8.8] and budget-fixed blind-backstop LLM risk to 6.4% [3.9, 9.1]. It is statistically tied with blanket under LLM attackers. | Claim large risk reduction, not privacy dominance over blanket QI. |
| RQ3: failure modes | Supported | Failure artifacts identify gendered language, marital/bereavement cues, education mentions, citizenship phrasing, race/ethnicity variants, employment context, and location context. | Use as evidence that inferability is broader than span recall. |
| RQ4: utility preservation | Mixed | Synthetic utility facts support a large RB-QIG edge over blanket: +28.3 points [25.2, 31.6]. Synthetic LLM utility gives only +2.6 [0.6, 4.8]. Budget-fixed blind public semantic utility is tied with blanket: -0.4 [-4.2, 3.4]. A 40-record privacy-aware public utility screen is also negative: -4.5 [-9.0, 0.0]. TAB legal-task utility is tied in the generic screen: balanced 0.0 [-10.0, 10.0], utility-budget 0.0 [-8.0, 8.0]. A legal-role TAB variant is worse than blanket on legal-task utility: -6.0 [-14.0, 2.0]. | Scope utility wins to controlled synthetic settings; present public utility as a caveat. |

## Planned Contributions

| Contribution from plan | Current status | Evidence artifact | Gap |
| --- | --- | --- | --- |
| Quasi-identifier taxonomy | Implemented and written | `paper/main.tex`, `prompts/qi_extractor.txt`, `src/api_qi_extractor.py` | Taxonomy could be expanded with a more formal category ablation later. |
| Risk-budgeted generalization algorithm | Implemented and written | `src/rbqig/transform.py`, `src/run_methods.py`, `paper/main.tex`, `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/budgetfix_report.md`, `results/followup_priority0_20260628/report.md` | Pairwise no-combo ablation is now run; it is non-discriminating under the balanced budget, so do not claim the pairwise term is independently validated. |
| Low-cost LLM-attacker protocol | Implemented | `src/llm_attack_eval.py`, `results/ratbench_d1_api_100/llm_attacker_metrics_with_llm_direct.csv`, `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_metrics.csv`, `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_gpt55_bootstrap_report.md` | Stronger-attacker robustness is now tested, but multi-model agreement remains incomplete. |
| Privacy-utility comparison | Implemented for core methods | `paper/generated/tables.md`, `paper/CLAIM_AUDIT.md` | Production de-identification baselines remain future work. |

## Baseline Coverage

| Planned baseline | Status | Evidence |
| --- | --- | --- |
| M0 no anonymization | Done | Synthetic and RAT-Bench deterministic tables. |
| M1 direct PII redaction | Done | Regex plus benchmark direct identifiers; appears in all tables. |
| M2 naive LLM direct sanitizer | Done for public target-aware RAT-Bench | `results/ratbench_d1_api_100/llm_attacker_metrics_with_llm_direct.csv`. |
| M3 blanket QI redaction | Done | Synthetic, target-aware public, and blind public tables. |
| M4 RB-QIG balanced | Done | Main method in all current evidence. |
| M5 RB-QIG strict | Done synthetically; deterministic public frontier plus public LLM smoke | Synthetic table, deterministic public frontier, and 40-record blind budget smoke. |
| M6 RB-QIG utility | Done synthetically; deterministic public frontier plus public LLM smoke | Synthetic table, deterministic public frontier, and 40-record blind budget smoke. |
| M7 production privacy filter or Presidio-style baseline | Partial pattern-only baseline done | `results/presidio_pattern_baseline_report.md` | Uses Presidio framework with custom patterns and no NER model. Useful as a practical lower bound, not full Presidio. |

## Dataset Coverage

| Planned dataset | Status | Evidence | Interpretation |
| --- | --- | --- | --- |
| RAT-Bench English easy, 100 rows | Done | `results/ratbench_d1_api_100/` | Main public target-aware transformation benchmark. |
| RAT-Bench harder rows | Partial | `results/ratbench_d2_api_30/` | Useful robustness smoke; not a replacement for a 100-row hard split. |
| RAT-Bench blind/deployment-style diagnostic | Done on same 100 D1 rows | `results/ratbench_d1_blind_backstop_v2_api_100/` for extraction coverage; `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/` for paper-facing transformed outputs | Strong stress test for extraction, with public utility caveat. |
| Synthetic LLM-ready sensitive snippets | Done, 100 oracle rows plus 30 blind diagnostic | `results/synthetic_100/`, `results/synthetic_30_blind_api/` | Strong controlled privacy-utility evidence. |
| TAB legal benchmark | Partial deterministic screen plus 10-document legal-utility screen done | `results/tab_echr_dev_30/tab_screen_report.md`, `results/tab_echr_dev_30/llm_legal_utility_10_with_b6_bootstrap_report.md`, `results/tab_echr_dev_30_legal_role/legal_role_screen_report.md` | Supports cross-domain residual-risk motivation; legal utility is inconclusive or negative and should not be used as a utility win. |
| Multilingual RAT-Bench | Not done | None | Lower priority for the current paper. |

## Metric Coverage

| Planned metric | Status | Evidence |
| --- | --- | --- |
| Direct identifier leakage | Done | Deterministic metrics in `results/*/metrics.csv`. |
| Record compromise | Done | Deterministic and LLM-attacker tables. |
| Exact/coarse attribute leakage | Done | Deterministic and LLM-attacker tables. |
| Risk-weighted leakage | Done | Main privacy metric across all result families. |
| Token change | Done | Deterministic tables. |
| Label preservation | Done | LLM utility tables and synthetic utility fields. |
| Utility fact preservation | Done | Synthetic deterministic and LLM utility tables. |
| chrF/BLEU | Not done | The current utility story uses task labels, fact checks, semantic LLM judging, and token change instead. |
| Bootstrap uncertainty | Done | `src/bootstrap_results.py` and generated bootstrap reports. |

## Ablation Coverage

| Planned ablation | Status | Evidence | Decision |
| --- | --- | --- | --- |
| Budgets 2/4/6 | Done on synthetic; deterministic public RAT-Bench/TAB frontier; limited public LLM smoke | Synthetic frontier, `results/followup_priority0_20260628/report.md`, and `results/ratbench_d1_blind_backstop_api_100/budget_variant_smoke_report.md` | Keep `rbqig_b4` as main. The deterministic frontier shows the budget knob trades leakage for QI specificity; the public LLM smoke did not justify more API budget. |
| Remove combination boost | Done, negative/tied | `results/followup_priority0_20260628/report.md` | Balanced no-combo produces identical transformed text and change logs on synthetic 100, blind RAT-Bench 100, and TAB 30. Treat the pairwise term as a design heuristic not isolated by this pilot. |
| Quasi-identifier type removal | Not done as a systematic ablation | Failure taxonomy gives qualitative type evidence. | Consider for a longer paper. |
| Attacker strength | Done for bounded robustness | 20-record `gpt-5.4-mini` target-aware smoke and 50-record GPT-5.5 blind-backstop check. | GPT-5.5 is harsher but preserves the direct-to-RB-QIG reduction; use it as a caveat rather than a headline win. |

## Artifact Readiness

| Artifact | Status |
| --- | --- |
| Main manuscript | `paper/main.tex` compiles as a 5-page COLM-formatted `paper/main.pdf`. |
| Generated result tables | `paper/generated/tables.md` and `paper/generated/tables.tex`. |
| Qualitative appendix | `paper/QUALITATIVE_APPENDIX.md`. |
| Claim audit | `paper/CLAIM_AUDIT.md`, currently 15/15 claim groups matched. |
| Reviewer stress test | `paper/REVIEWER_STRESS_TEST.md`. |
| Reproducibility commands | `README.md` and `RESEARCH_STATUS.md`. |
| API budget tracking | `RESEARCH_STATUS.md`, currently about $5.76 fresh-equivalent cached cost. |

## Claim Boundary

Make these claims:

- Direct PII redaction leaves substantial residual inference risk from
  quasi-identifiers.
- Naive LLM sanitization is materially better than direct redaction but still
  far leakier than explicit quasi-identifier transformation in the public pilot.
- RB-QIG gives a cheap, auditable transformation policy that sharply reduces
  measured residual risk relative to direct and naive LLM redaction.
- RB-QIG preserves more utility than blanket quasi-identifier redaction in the
  controlled synthetic benchmark.
- Blind quasi-identifier extraction and public utility preservation remain open
  problems.

Do not claim:

- legal anonymization,
- deployment readiness,
- state-of-the-art de-identification,
- privacy superiority over blanket QI redaction,
- public RAT-Bench utility superiority over blanket QI redaction.

## Next Best Work

The next experiment should only be run if it can be bounded and cheap.

| Priority | Action | Why | Stop rule |
| --- | --- | --- | --- |
| 1 | Improve task-realistic utility evaluation beyond broad labels. | Public and TAB utility remain the weakest part of the evidence package. | Keep any API usage under a small fixed cap and reuse transformed outputs. |
| 2 | Run a tiny multi-model attacker agreement check on an existing subset. | Tests whether the attacker conclusion depends on one model family after the GPT-5.5 caveat. | Keep under a small fixed API cap and reuse cached transformed outputs. |
| 3 | Tighten the 4-page manuscript after final template choice. | The evidence is stronger than the current space-limited narrative can fully express. | Preserve the 4-page limit and do not broaden claims. |

Avoid spending time on a full 300-row RAT-Bench expansion unless a reviewer or
target venue requires narrower confidence intervals.
