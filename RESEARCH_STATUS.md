# RB-QIG Research Status

Last updated: 2026-06-28

## What Is Implemented

- Stdlib-only synthetic benchmark generator with direct identifiers, quasi-identifiers, utility labels, and utility facts.
- Direct identifier redaction using regexes plus known benchmark direct identifiers.
- Heuristic direct-name redaction for public benchmark rows whose metadata omits explicit names but whose text states names in dialogue.
- Baselines: no anonymization, direct redaction, blanket QI redaction.
- RB-QIG variants: strict budget 2, balanced budget 4, utility budget 6.
- Deterministic leakage proxy for exact/coarse quasi-identifier leakage.
- Deterministic utility proxy for task label and utility fact preservation.
- SVG plots for privacy-utility frontier and leakage by method.
- Conservative RAT-Bench English difficulty-1 loader through the Hugging Face rows API.
- Cached OpenAI API quasi-identifier extractor for public RAT-Bench rows.
- Cached OpenAI API LLM attacker for transformed public benchmark rows.
- Cached OpenAI API LLM utility judge for transformed synthetic and public benchmark rows.
- Cached OpenAI API privacy-aware utility diagnostic for public benchmark rows.
- No-API annotation-derived QI semantic-specificity diagnostic for public transformed outputs.
- Cached naive LLM direct-redaction baseline (`llm_direct`) for the planned M2 comparison.
- 30-row RAT-Bench English difficulty-2 robustness smoke with target-aware extraction, naive LLM sanitizer, and LLM-attacker evaluation.
- 20-record stronger-attacker smoke with `gpt-5.4-mini` on the target-aware public pilot.
- 30-document TAB ECHR deterministic second-domain screen using public annotations and no API calls.
- 10-document TAB ECHR legal-task LLM utility screen using 40 fresh-equivalent calls, including a utility-budget variant check; the 10 new `rbqig_b6` calls cost $0.008304.
- Bounded TAB legal-role generalization diagnostic; the 10 new changed-RB-QIG legal-utility calls cost $0.008006 and did not improve legal-task utility.
- Presidio-style pattern-only direct PII baseline using custom patterns and no NER model.
- Paired bootstrap confidence intervals for deterministic and LLM-attacker metrics.
- LLM attacker scoring now uses `eval_quasi_identifiers` when present, so blind-extraction evaluations are weighted against the benchmark QIs rather than extractor-specific attribute names.
- Utility-aware blind extraction conversion that keeps suggested generalizations and drops low-risk, high-utility candidates.
- Blind public RAT-Bench diagnostic that evaluates blind extracted spans against the original benchmark QIs.
- Generic deterministic backstop for blind extraction of common demographic, citizenship, education, employment, marital, and race/ethnicity cues.
- Improved blind-backstop v2 that adds separated-status, grade-level, gendered-term, and race/ethnicity lexical coverage.
- Budget-enforcing RB-QIG optimizer fix that scans forward to the next risk-reducing candidate level.
- Paper table generator for Markdown and LaTeX result tables.
- Qualitative appendix generator for positive examples, target-aware public comparisons, and blind public failure modes.
- Claim audit generator that ties headline paper claims to local CSV and report artifacts.
- Compiled 4-page LaTeX manuscript draft with bibliography and reproducibility appendix.

## Current Synthetic Control Result

Command:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_pilot.py --n 100 --seed 7 --out-dir results/synthetic_100
```

Metrics: `results/synthetic_100/metrics.csv`

| Method | Direct ID leak | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Utility facts | Token change |
|---|---:|---:|---:|---:|---:|---:|---:|
| None | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% |
| Direct | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 13.5% |
| Blanket QI | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 43.3% | 63.7% |
| RB-QIG strict | 0.0% | 0.0% | 0.0% | 32.8% | 16.1% | 48.3% | 59.3% |
| RB-QIG balanced | 0.0% | 0.0% | 0.0% | 49.1% | 23.6% | 71.7% | 59.0% |
| RB-QIG utility | 0.0% | 0.0% | 0.0% | 77.9% | 38.0% | 95.0% | 56.6% |

Interpretation:

- The synthetic control supports the core tradeoff: direct PII redaction leaves quasi-identifiers intact, blanket QI redaction eliminates leakage but destroys many utility facts, and RB-QIG gives a tunable middle ground.
- The balanced setting is the most paper-friendly synthetic point: 23.6% risk-weighted coarse leakage with 71.7% utility-fact preservation.
- Bootstrap intervals are tight for the main synthetic tradeoff: RB-QIG balanced risk-weighted leakage is 23.6% [22.9%, 24.5%], utility-fact preservation is 71.7% [70.8%, 72.4%], and its utility advantage over blanket QI is +28.3 points [+25.2, +31.6].
- This is not publishable alone because it uses known synthetic quasi-identifier spans.

## Synthetic LLM Utility Judge Result

Command:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_utility_eval.py --input results/synthetic_100/anonymized_outputs.jsonl --utility-out results/synthetic_100/llm_utility_outputs.jsonl --usage-out results/synthetic_100/llm_utility_usage.jsonl --metrics-out results/synthetic_100/llm_utility_metrics.csv --cache-dir results/api_cache/llm_utility --methods direct blanket_qi rbqig_b4 --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/synthetic_100/llm_utility_outputs.jsonl --source-type metrics-jsonl --source-name synthetic_100_llm_utility --cis-out results/synthetic_100/llm_utility_bootstrap_cis.csv --contrasts-out results/synthetic_100/llm_utility_bootstrap_contrasts.csv --report-out results/synthetic_100/llm_utility_bootstrap_report.md --per-record-out results/synthetic_100/llm_utility_per_record_metrics.csv --metrics label_preservation llm_fact_preservation semantic_utility_score --n-boot 5000 --seed 20260627
```

Metrics: `results/synthetic_100/llm_utility_metrics.csv`

Estimated fresh-equivalent utility-judge cost: $0.080109.

| Method | Label preserved | LLM fact preservation | Semantic utility |
|---|---:|---:|---:|
| Direct | 100.0% | 75.3% | 83.2% |
| Blanket QI | 99.0% | 69.1% | 76.8% |
| RB-QIG balanced | 100.0% | 71.3% | 79.4% |

Interpretation:

- The LLM utility judge is more forgiving than the deterministic utility-fact metric because it treats placeholders and broad context as partially useful for downstream decisions.
- RB-QIG balanced has a small semantic-utility edge over blanket QI: +2.6 points [+0.6, +4.8].
- RB-QIG balanced has only a borderline LLM fact-preservation edge over blanket QI: +2.2 points [-0.2, +4.8].
- This should be framed as a calibration result that prevents overclaiming: the large utility advantage appears in the stricter controlled fact metric, while a semantic judge still sees a modest RB-QIG advantage.

## Current RAT-Bench Smoke Test

Commands:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/load_ratbench.py --n 30 --config english --difficulty 1 --out data/processed/ratbench_english_d1_30.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/ratbench_english_d1_30.jsonl --out results/ratbench_d1_30/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/ratbench_d1_30/anonymized_outputs.jsonl --attacks-out results/ratbench_d1_30/attacker_outputs.jsonl --utility-out results/ratbench_d1_30/utility_outputs.jsonl --metrics-out results/ratbench_d1_30/metrics.csv
```

Metrics: `results/ratbench_d1_30/metrics.csv`

| Method | Direct ID leak | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak |
|---|---:|---:|---:|---:|---:|
| None | 93.3% | 46.7% | 97.2% | 97.2% | 97.2% |
| Direct | 0.0% | 46.7% | 92.3% | 92.3% | 92.7% |
| Blanket QI | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| RB-QIG strict | 0.0% | 0.0% | 0.0% | 81.1% | 38.9% |
| RB-QIG balanced | 0.0% | 0.0% | 23.9% | 94.9% | 57.3% |
| RB-QIG utility | 0.0% | 0.0% | 43.7% | 95.6% | 67.1% |

Interpretation:

- This smoke test confirms the residual-risk motivation on public data: direct redaction still leaves high indirect-identifier leakage.
- The current RAT-Bench adapter is not yet a fair RB-QIG evaluation. It uses one exact target span per indirect identifier; the source text often contains repeated or variant mentions that remain untouched.
- The RAT-Bench utility proxy is weak because the dataset includes multiple scenarios but the current loader only checks generic consultation terms.

## Current API-Extracted RAT-Bench Pilot

Commands:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/load_ratbench.py --n 100 --config english --difficulty 1 --out data/processed/ratbench_english_d1_100.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/api_qi_extractor.py --input data/processed/ratbench_english_d1_100.jsonl --out data/processed/ratbench_english_d1_100_api_qi.jsonl --usage-out results/ratbench_d1_api_100/usage.json --cache-dir results/api_cache/qi_extractor --n 100 --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/ratbench_english_d1_100_api_qi.jsonl --out results/ratbench_d1_api_100/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/ratbench_d1_api_100/anonymized_outputs.jsonl --attacks-out results/ratbench_d1_api_100/attacker_outputs.jsonl --utility-out results/ratbench_d1_api_100/utility_outputs.jsonl --metrics-out results/ratbench_d1_api_100/metrics.csv
```

Metrics: `results/ratbench_d1_api_100/metrics.csv`

API usage: `results/ratbench_d1_api_100/usage.json`

Estimated extractor cost: $0.075506 for the current 100-row public RAT-Bench run.

| Method | Direct ID leak | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Utility facts | Token change |
|---|---:|---:|---:|---:|---:|---:|---:|
| None | 91.0% | 92.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% |
| Direct | 0.0% | 92.0% | 94.9% | 94.9% | 93.8% | 100.0% | 0.9% |
| Blanket QI | 0.0% | 1.0% | 0.3% | 0.3% | 0.3% | 100.0% | 7.1% |
| RB-QIG strict | 0.0% | 1.0% | 0.3% | 51.8% | 23.1% | 100.0% | 7.0% |
| RB-QIG balanced | 0.0% | 1.0% | 0.8% | 63.0% | 28.6% | 100.0% | 7.0% |
| RB-QIG utility | 0.0% | 1.0% | 0.8% | 72.2% | 33.2% | 100.0% | 6.9% |

Interpretation:

- This is the best deterministic public-data result so far. Direct redaction leaves 93.8% risk-weighted leakage, while RB-QIG balanced lowers it to 28.6% under the target-aware extractor plus deterministic variant expansion.
- Paired bootstrap intervals show this deterministic reduction is stable: direct minus RB-QIG balanced is +65.2 risk-weighted leakage points [+61.4, +68.8].
- Blanket QI redaction still wins on privacy, but RAT-Bench difficulty-1 rows are short structured attributes in long transcripts, so token-change utility does not strongly penalize blanket redaction.
- The current extractor is target-aware: it uses the benchmark ground-truth attributes to find all mentions and variants. This is acceptable as a controlled benchmark transformation test but should be disclosed clearly.
- The RAT-Bench utility metrics now confirm that all methods preserve broad scenario content, but they still do not distinguish useful semantic preservation. The synthetic benchmark remains the stronger privacy-utility tradeoff evidence.

## Blind RAT-Bench Extractor Diagnostic with Generic Backstop

Commands:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/api_qi_extractor.py --blind --eval-against-original-qis --input data/processed/ratbench_english_d1_100.jsonl --out data/processed/ratbench_english_d1_100_blind_backstop_api_qi.jsonl --usage-out results/ratbench_d1_blind_backstop_api_100/usage.json --cache-dir results/api_cache/ratbench_blind_qi_extractor --n 100 --model gpt-5.4-nano --max-output-tokens 2200
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/ratbench_english_d1_100_blind_backstop_api_qi.jsonl --out results/ratbench_d1_blind_backstop_api_100/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/ratbench_d1_blind_backstop_api_100/anonymized_outputs.jsonl --attacks-out results/ratbench_d1_blind_backstop_api_100/attacker_outputs.jsonl --utility-out results/ratbench_d1_blind_backstop_api_100/utility_outputs.jsonl --metrics-out results/ratbench_d1_blind_backstop_api_100/metrics.csv
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_blind_backstop_api_100/anonymized_outputs.jsonl --source-type transformed --source-name ratbench_d1_blind_backstop_api_100 --cis-out results/ratbench_d1_blind_backstop_api_100/bootstrap_cis.csv --contrasts-out results/ratbench_d1_blind_backstop_api_100/bootstrap_contrasts.csv --report-out results/ratbench_d1_blind_backstop_api_100/bootstrap_report.md --per-record-out results/ratbench_d1_blind_backstop_api_100/per_record_metrics.csv --n-boot 5000 --seed 20260627
/home/eston/anaconda3/envs/rb_qig/bin/python src/analyze_blind_coverage.py --input data/processed/ratbench_english_d1_100_blind_backstop_api_qi.jsonl --out-md results/ratbench_d1_blind_backstop_api_100/blind_coverage_report.md --out-csv results/ratbench_d1_blind_backstop_api_100/blind_coverage.csv
```

Metrics: `results/ratbench_d1_blind_backstop_api_100/metrics.csv`

Estimated fresh-equivalent blind extractor cost: $0.134941. The backstop rerun used 100/100 cached extractor responses and made zero uncached API calls.

| Method | Direct ID leak | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Utility facts | Token change |
|---|---:|---:|---:|---:|---:|---:|---:|
| None | 91.0% | 39.0% | 98.9% | 98.9% | 98.9% | 100.0% | 0.0% |
| Direct | 0.0% | 39.0% | 94.4% | 94.4% | 94.3% | 100.0% | 0.9% |
| Blanket QI | 0.0% | 0.0% | 6.6% | 6.6% | 6.7% | 100.0% | 10.7% |
| RB-QIG strict | 0.0% | 0.0% | 7.6% | 20.5% | 13.7% | 100.0% | 9.8% |
| RB-QIG balanced | 0.0% | 0.0% | 8.1% | 27.8% | 17.3% | 100.0% | 9.7% |
| RB-QIG utility | 0.0% | 0.0% | 9.3% | 33.2% | 20.4% | 100.0% | 9.6% |

Interpretation:

- This is the deployment-style public benchmark stress test: the extractor does not receive target attribute names, and evaluation is against the original RAT-Bench QIs.
- A raw blind extractor covered 72.8% of benchmark QI spans; adding a generic deterministic backstop raises span coverage to 97.5% and risk-weighted coverage to 97.7%.
- Backstopped blind RB-QIG balanced substantially improves over direct redaction: risk-weighted leakage drops from 94.3% [91.4%, 96.8%] to 17.3% [13.1%, 22.0%], a paired drop of 77.0 points [71.9, 81.9].
- Blanket QI redaction remains safer than RB-QIG balanced under blind extraction, with RB-QIG leaving +10.6 points [7.1, 14.6] more risk-weighted leakage.
- The deterministic RAT-Bench utility proxy remains uninformative in this setup because all methods preserve the broad scenario facts; use this result as a blind-extraction coverage limitation, not a utility win.

This original blind-backstop result is superseded for paper-facing claims by the improved v2 backstop below.

## Blind RAT-Bench LLM Attacker Result

Command:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_attack_eval.py --input results/ratbench_d1_blind_backstop_api_100/anonymized_outputs.jsonl --attacks-out results/ratbench_d1_blind_backstop_api_100/llm_attacker_outputs.jsonl --usage-out results/ratbench_d1_blind_backstop_api_100/llm_attacker_usage.jsonl --metrics-out results/ratbench_d1_blind_backstop_api_100/llm_attacker_metrics.csv --cache-dir results/api_cache/llm_attacker --methods direct blanket_qi rbqig_b4 --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_blind_backstop_api_100/llm_attacker_outputs.jsonl --source-type llm-attacker --source-name ratbench_d1_blind_backstop_api_100_llm_attacker --cis-out results/ratbench_d1_blind_backstop_api_100/llm_bootstrap_cis.csv --contrasts-out results/ratbench_d1_blind_backstop_api_100/llm_bootstrap_contrasts.csv --report-out results/ratbench_d1_blind_backstop_api_100/llm_bootstrap_report.md --per-record-out results/ratbench_d1_blind_backstop_api_100/llm_per_record_metrics.csv --n-boot 5000 --seed 20260627
/home/eston/anaconda3/envs/rb_qig/bin/python src/analyze_failures.py --input results/ratbench_d1_blind_backstop_api_100/llm_attacker_outputs.jsonl --counts-out results/ratbench_d1_blind_backstop_api_100/llm_failure_taxonomy.csv --examples-out results/ratbench_d1_blind_backstop_api_100/llm_failure_examples.csv --md-out results/ratbench_d1_blind_backstop_api_100/llm_failure_taxonomy.md
```

Metrics: `results/ratbench_d1_blind_backstop_api_100/llm_attacker_metrics.csv`

The first full run added 200 uncached API calls because direct rows reused the existing cache and blanket/RB-QIG rows were new. A later scorer-only rerun used 300/300 cached responses after fixing benchmark-QI risk weighting.

| Method | Record compromise | Exact attr leak | Coarse attr leak | Risk-weighted leak |
|---|---:|---:|---:|---:|
| Direct | 37.0% | 74.9% | 81.2% | 78.1% |
| Blanket QI | 1.0% | 10.8% | 13.7% | 11.4% |
| RB-QIG balanced | 1.0% | 10.3% | 12.8% | 10.6% |

Interpretation:

- This is the strongest deployment-style public result so far: with blind extraction plus a deterministic backstop, RB-QIG balanced reduces LLM-attacker risk-weighted leakage from 78.1% [73.5%, 82.6%] to 10.6% [7.2%, 14.4%].
- The paired direct-to-RB-QIG reduction is +67.6 points [62.5, 72.8].
- RB-QIG balanced and blanket QI are statistically tied for LLM-attacker privacy: RB-QIG minus blanket is -0.8 points [-4.0, +2.6].
- This reconciles the deterministic and LLM views: deterministic coarse leakage still penalizes RB-QIG more than blanket, but the model attacker does not recover substantially more benchmark attributes from RB-QIG than from blanket.
- Residual LLM leaks are mostly gendered context, marital/family phrasing, citizenship phrasing, education cues, race/ethnicity variants, and location references.

## Blind RAT-Bench LLM Utility Judge Result

Command:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_utility_eval.py --input results/ratbench_d1_blind_backstop_api_100/anonymized_outputs.jsonl --utility-out results/ratbench_d1_blind_backstop_api_100/llm_utility_outputs.jsonl --usage-out results/ratbench_d1_blind_backstop_api_100/llm_utility_usage.jsonl --metrics-out results/ratbench_d1_blind_backstop_api_100/llm_utility_metrics.csv --cache-dir results/api_cache/llm_utility --methods direct blanket_qi rbqig_b4 --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_blind_backstop_api_100/llm_utility_outputs.jsonl --source-type metrics-jsonl --source-name ratbench_d1_blind_backstop_api_100_llm_utility --cis-out results/ratbench_d1_blind_backstop_api_100/llm_utility_bootstrap_cis.csv --contrasts-out results/ratbench_d1_blind_backstop_api_100/llm_utility_bootstrap_contrasts.csv --report-out results/ratbench_d1_blind_backstop_api_100/llm_utility_bootstrap_report.md --per-record-out results/ratbench_d1_blind_backstop_api_100/llm_utility_per_record_metrics.csv --metrics label_preservation llm_fact_preservation semantic_utility_score --n-boot 5000 --seed 20260627
```

Metrics: `results/ratbench_d1_blind_backstop_api_100/llm_utility_metrics.csv`

Estimated fresh-equivalent utility-judge cost for this public 300-call table: $0.240443.

| Method | Label preserved | LLM fact preservation | Semantic utility |
|---|---:|---:|---:|
| Direct | 99.0% | 84.3% | 86.2% |
| Blanket QI | 99.0% | 52.6% | 62.4% |
| RB-QIG balanced | 98.0% | 55.7% | 62.0% |

Interpretation:

- This is a public utility caveat, not a new RB-QIG win. Both blanket QI and RB-QIG balanced lose substantial semantic utility relative to direct redaction.
- RB-QIG balanced is statistically tied with blanket QI on public semantic utility: -0.4 points [-3.6, +3.0].
- RB-QIG balanced has only a non-significant public fact-preservation edge over blanket QI: +3.1 points [-1.6, +7.7].
- The large utility advantage over blanket redaction remains supported by the controlled synthetic benchmark, not by current public RAT-Bench utility judging.

This original blind-backstop LLM result is superseded for paper-facing claims by the improved v2 backstop below.

## Budget-Fixed Improved Blind RAT-Bench Backstop v2

Commands:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/api_qi_extractor.py --blind --eval-against-original-qis --input data/processed/ratbench_english_d1_100.jsonl --out data/processed/ratbench_english_d1_100_blind_backstop_v2_api_qi.jsonl --usage-out results/ratbench_d1_blind_backstop_v2_api_100/usage.json --cache-dir results/api_cache/ratbench_blind_qi_extractor --n 100 --model gpt-5.4-nano --max-output-tokens 2200
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/ratbench_english_d1_100_blind_backstop_v2_api_qi.jsonl --out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl --attacks-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/attacker_outputs.jsonl --utility-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/utility_outputs.jsonl --metrics-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/metrics.csv
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl --source-type transformed --source-name ratbench_d1_blind_backstop_v2_budgetfix_api_100 --cis-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_cis.csv --contrasts-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_contrasts.csv --report-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_report.md --per-record-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/per_record_metrics.csv --n-boot 5000 --seed 20260628 --comparisons direct:rbqig_b4 rbqig_b4:blanket_qi
/home/eston/anaconda3/envs/rb_qig/bin/python src/analyze_blind_coverage.py --input data/processed/ratbench_english_d1_100_blind_backstop_v2_api_qi.jsonl --out-md results/ratbench_d1_blind_backstop_v2_api_100/blind_coverage_report.md --out-csv results/ratbench_d1_blind_backstop_v2_api_100/blind_coverage.csv
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_attack_eval.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl --attacks-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_outputs.jsonl --usage-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_usage.jsonl --metrics-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_metrics.csv --cache-dir results/api_cache/llm_attacker --methods direct blanket_qi rbqig_b4 --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_outputs.jsonl --source-type llm-attacker --source-name ratbench_d1_blind_backstop_v2_budgetfix_api_100_llm_attacker --cis-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_bootstrap_cis.csv --contrasts-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_bootstrap_contrasts.csv --report-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_bootstrap_report.md --per-record-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_per_record_metrics.csv --n-boot 5000 --seed 20260628 --comparisons direct:rbqig_b4 rbqig_b4:blanket_qi
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_utility_eval.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl --utility-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_outputs.jsonl --usage-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_usage.jsonl --metrics-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_metrics.csv --cache-dir results/api_cache/llm_utility --methods direct blanket_qi rbqig_b4 --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_outputs.jsonl --source-type metrics-jsonl --source-name ratbench_d1_blind_backstop_v2_budgetfix_api_100_llm_utility --cis-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_bootstrap_cis.csv --contrasts-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_bootstrap_contrasts.csv --report-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_bootstrap_report.md --per-record-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_per_record_metrics.csv --metrics label_preservation llm_fact_preservation semantic_utility_score --n-boot 5000 --seed 20260628 --comparisons direct:rbqig_b4 rbqig_b4:blanket_qi
```

Coverage: `results/ratbench_d1_blind_backstop_v2_api_100/blind_coverage_report.md`

- Benchmark QI span coverage: 99.6% (282/283), up from 97.5% for the original backstop.
- Risk-weighted span coverage: 99.8%.
- The only remaining missed benchmark span is one low-risk sex attribute whose benchmark value is not stated verbatim.

Budget-fix report: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/budgetfix_report.md`

Deterministic metrics: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/metrics.csv`

| Method | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Utility facts | Token change |
|---|---:|---:|---:|---:|---:|---:|
| Direct | 39.0% | 94.4% | 94.4% | 94.3% | 100.0% | 0.9% |
| Blanket QI | 0.0% | 3.1% | 3.1% | 3.1% | 100.0% | 10.8% |
| RB-QIG balanced | 0.0% | 4.6% | 6.4% | 5.4% | 100.0% | 10.1% |

LLM-attacker metrics: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_metrics.csv`

| Method | Record compromise | Exact attr leak | Coarse attr leak | Risk-weighted leak |
|---|---:|---:|---:|---:|
| Direct | 37.0% | 74.9% | 81.2% | 78.1% |
| Blanket QI | 1.0% | 5.4% | 8.3% | 6.8% |
| RB-QIG balanced | 1.0% | 5.3% | 7.4% | 6.4% |

LLM-utility metrics: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_metrics.csv`

| Method | Label preserved | LLM fact preservation | Semantic utility |
|---|---:|---:|---:|
| Direct | 99.0% | 84.3% | 86.2% |
| Blanket QI | 99.0% | 53.8% | 62.6% |
| RB-QIG balanced | 96.0% | 55.5% | 62.2% |

Interpretation:

- The v2 deterministic backstop closes the obvious lexical coverage misses (`separated`, grade-level phrases, gendered terms, and Filipino/Micronesian ethnicity cues) without new extractor API calls.
- The optimizer budget fix removes all RB-QIG document-risk budget violations in the transformed outputs; max document risk after transformation is 2.0, 4.0, and 6.0 for the strict, balanced, and utility variants.
- This is now the strongest deployment-style public privacy result: RB-QIG balanced reduces LLM-attacker risk-weighted leakage from 78.1% [73.3%, 82.9%] to 6.4% [3.9%, 9.1%].
- The paired direct-to-RB-QIG LLM reduction is +71.8 points [66.4, 76.9].
- RB-QIG balanced and blanket QI remain statistically tied under the LLM attacker: -0.5 points [-2.5, +1.5].
- Deterministic scoring still finds RB-QIG balanced slightly leakier than blanket QI: +2.3 points [0.6, 4.9].
- Public semantic utility remains a caveat: RB-QIG balanced is 62.2% [58.8, 65.2] versus 62.6% [59.2, 66.0] for blanket QI, with paired RB-QIG minus blanket -0.4 points [-4.2, +3.4].
- A no-API annotation-specificity diagnostic gives a narrow public utility signal: RB-QIG balanced has +6.8 specificity points [4.7, 9.2] over blanket QI on blind RAT-Bench and +6.2 points [5.5, 6.9] on TAB. This measures retained typed/generalized QI semantics, not task accuracy.
- A value-free safe-label smoke did not improve public utility or privacy materially, so it is a negative diagnostic rather than a main paper point.
- A 40-record privacy-aware utility screen also does not rescue the public utility claim: RB-QIG balanced scores 83.0% [78.5, 87.0] versus 87.5% [83.5, 91.5] for blanket QI, a paired -4.5 points [-9.0, 0.0].

## Blind RAT-Bench Budget Variant Smoke

Report: `results/ratbench_d1_blind_backstop_api_100/budget_variant_smoke_report.md`

This was a bounded 40-record exploratory check to decide whether strict (`rbqig_b2`) or utility-budget (`rbqig_b6`) variants justify a full 100-record public LLM attacker and utility-judge sweep. Direct, blanket QI, and balanced (`rbqig_b4`) values below are recomputed from existing cached 100-record outputs on the same first 40 records.

| Method | LLM risk-weighted leak | Semantic utility | LLM fact preservation |
|---|---:|---:|---:|
| Direct | 75.5% | 82.0% | 80.8% |
| Blanket QI | 13.6% | 65.0% | 53.2% |
| RB-QIG strict | 11.8% | 64.0% | 56.8% |
| RB-QIG balanced | 8.6% | 65.0% | 59.1% |
| RB-QIG utility | 12.4% | 60.5% | 56.5% |

Interpretation:

- The smoke does not justify spending more API budget on a full budget sweep.
- RB-QIG balanced is not worse than strict on semantic utility in the first 40 rows and has lower LLM-attacker risk-weighted leakage.
- RB-QIG utility is not a useful public frontier point in this smoke: it has lower semantic utility and higher attacker leakage than balanced.
- Keep the main paper focused on `rbqig_b4`; treat this as a negative exploratory result.
- Fresh-equivalent cost for the four smoke runs was $0.108046 across 160 API calls.

## LLM Attacker Result with Naive LLM Sanitizer Baseline

Command:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_direct_redact.py --input results/ratbench_d1_api_100/anonymized_outputs.jsonl --out results/ratbench_d1_api_100/anonymized_outputs_with_llm_direct.jsonl --usage-out results/ratbench_d1_api_100/llm_direct_usage.jsonl --cache-dir results/api_cache/llm_direct_redact --merge --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_attack_eval.py --input results/ratbench_d1_api_100/anonymized_outputs_with_llm_direct.jsonl --attacks-out results/ratbench_d1_api_100/llm_attacker_outputs_with_llm_direct.jsonl --usage-out results/ratbench_d1_api_100/llm_attacker_usage_with_llm_direct.jsonl --metrics-out results/ratbench_d1_api_100/llm_attacker_metrics_with_llm_direct.csv --cache-dir results/api_cache/llm_attacker --methods direct llm_direct blanket_qi rbqig_b4 --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_api_100/llm_attacker_outputs_with_llm_direct.jsonl --source-type llm-attacker --source-name ratbench_d1_api_100_llm_attacker_with_llm_direct --cis-out results/ratbench_d1_api_100/llm_bootstrap_cis_with_llm_direct.csv --contrasts-out results/ratbench_d1_api_100/llm_bootstrap_contrasts_with_llm_direct.csv --report-out results/ratbench_d1_api_100/llm_bootstrap_report_with_llm_direct.md --per-record-out results/ratbench_d1_api_100/llm_per_record_metrics_with_llm_direct.csv --n-boot 5000 --seed 20260627 --comparisons direct:llm_direct llm_direct:rbqig_b4 direct:rbqig_b4 rbqig_b4:blanket_qi
```

Metrics: `results/ratbench_d1_api_100/llm_attacker_metrics_with_llm_direct.csv`

The naive sanitizer itself cost $0.201144 fresh-equivalent. The LLM-attacker table added 100 new `llm_direct` attacker calls; direct, blanket, and RB-QIG rows reused cache. Fresh-equivalent attacker cost for the full 400-row table is $0.192689, of which $0.047406 is the new `llm_direct` attacker baseline.

| Method | Record compromise | Exact attr leak | Coarse attr leak | Risk-weighted leak |
|---|---:|---:|---:|---:|
| Direct | 76.0% | 74.9% | 81.2% | 78.0% |
| LLM direct | 34.0% | 48.7% | 52.8% | 46.0% |
| Blanket QI | 3.0% | 3.9% | 7.3% | 5.3% |
| RB-QIG balanced | 2.0% | 4.0% | 8.8% | 5.7% |

Interpretation:

- The LLM attacker confirms the main privacy story on public data: direct redaction leaves substantial residual inference risk.
- A naive LLM sanitizer improves over direct redaction but is still far leakier than RB-QIG: risk-weighted leakage is 46.0% [40.1%, 52.0%] for `llm_direct` versus 5.7% [3.2%, 8.8%] for RB-QIG balanced.
- Bootstrap intervals show the direct-to-RB-QIG reduction is large: direct minus RB-QIG balanced is +72.2 risk-weighted leakage points [+67.0, +77.4].
- Bootstrap intervals also show RB-QIG substantially improves over the naive sanitizer: `llm_direct` minus RB-QIG balanced is +40.2 risk-weighted leakage points [+33.1, +47.1].
- Under the current RAT-Bench difficulty-1 setup, RB-QIG balanced and blanket QI are statistically tied for measured privacy: RB-QIG minus blanket is +0.5 points [-2.6, +3.6]. This is not a utility win for RB-QIG on RAT-Bench because these rows are long transcripts where removing target attributes changes few tokens.
- Remaining RB-QIG leaks are informative failure cases: widowhood from bereavement cues, sex from gendered language, education from school-name mentions, citizenship from non-citizen phrasing, and employment/armed-forces status from occupation-context cues.
- This supports a mature short-paper narrative: RB-QIG reduces LLM inference risk dramatically relative to both direct PII redaction and naive LLM sanitization, but robust quasi-identifier generalization requires handling indirect lexical variants and relational cues.

## RAT-Bench Difficulty-2 Robustness Smoke

Commands:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/load_ratbench.py --n 30 --config english --difficulty 2 --out data/processed/ratbench_english_d2_30.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/api_qi_extractor.py --input data/processed/ratbench_english_d2_30.jsonl --out data/processed/ratbench_english_d2_30_api_qi.jsonl --usage-out results/ratbench_d2_api_30/usage.json --cache-dir results/api_cache/qi_extractor --n 30 --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/ratbench_english_d2_30_api_qi.jsonl --out results/ratbench_d2_api_30/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/ratbench_d2_api_30/anonymized_outputs.jsonl --attacks-out results/ratbench_d2_api_30/attacker_outputs.jsonl --utility-out results/ratbench_d2_api_30/utility_outputs.jsonl --metrics-out results/ratbench_d2_api_30/metrics.csv
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_direct_redact.py --input results/ratbench_d2_api_30/anonymized_outputs.jsonl --out results/ratbench_d2_api_30/anonymized_outputs_with_llm_direct.jsonl --usage-out results/ratbench_d2_api_30/llm_direct_usage.jsonl --cache-dir results/api_cache/llm_direct_redact --merge --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_attack_eval.py --input results/ratbench_d2_api_30/anonymized_outputs_with_llm_direct.jsonl --attacks-out results/ratbench_d2_api_30/llm_attacker_outputs_with_llm_direct.jsonl --usage-out results/ratbench_d2_api_30/llm_attacker_usage_with_llm_direct.jsonl --metrics-out results/ratbench_d2_api_30/llm_attacker_metrics_with_llm_direct.csv --cache-dir results/api_cache/llm_attacker --methods direct llm_direct blanket_qi rbqig_b4 --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d2_api_30/llm_attacker_outputs_with_llm_direct.jsonl --source-type llm-attacker --source-name ratbench_d2_api_30_llm_attacker_with_llm_direct --cis-out results/ratbench_d2_api_30/llm_bootstrap_cis_with_llm_direct.csv --contrasts-out results/ratbench_d2_api_30/llm_bootstrap_contrasts_with_llm_direct.csv --report-out results/ratbench_d2_api_30/llm_bootstrap_report_with_llm_direct.md --per-record-out results/ratbench_d2_api_30/llm_per_record_metrics_with_llm_direct.csv --n-boot 5000 --seed 20260627 --comparisons direct:llm_direct llm_direct:rbqig_b4 direct:rbqig_b4 rbqig_b4:blanket_qi
```

Extractor cost: $0.016848. Naive sanitizer cost: $0.062732. LLM-attacker cost: $0.051632.

Deterministic metrics: `results/ratbench_d2_api_30/metrics_with_llm_direct.csv`

| Method | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Token change |
|---|---:|---:|---:|---:|---:|
| Direct | 76.7% | 94.6% | 94.6% | 94.3% | 0.1% |
| LLM direct | 63.3% | 68.6% | 68.6% | 68.2% | 3.2% |
| Blanket QI | 0.0% | 0.6% | 0.6% | 0.6% | 2.7% |
| RB-QIG balanced | 0.0% | 3.9% | 93.3% | 48.3% | 2.6% |

LLM-attacker metrics: `results/ratbench_d2_api_30/llm_attacker_metrics_with_llm_direct.csv`

| Method | Record compromise | Exact attr leak | Coarse attr leak | Risk-weighted leak |
|---|---:|---:|---:|---:|
| Direct | 70.0% | 70.6% | 70.6% | 70.8% |
| LLM direct | 60.0% | 57.2% | 57.2% | 56.9% |
| Blanket QI | 13.3% | 20.0% | 20.0% | 19.8% |
| RB-QIG balanced | 13.3% | 13.3% | 13.3% | 13.1% |

Interpretation:

- Difficulty-2 is a harder, more demographic-heavy 30-row smoke, not a new main benchmark.
- The target-aware extractor found 8.4 spans per record on average, mostly demographic and location cues.
- Deterministic coarse scoring is harsher on RB-QIG here because generalized demographic placeholders still count as coarse matches.
- The LLM attacker supports the same qualitative story as difficulty-1: RB-QIG balanced sharply improves over direct and naive LLM redaction. Direct minus RB-QIG balanced is +57.6 risk-weighted leakage points [+42.4, +72.8]; naive LLM sanitizer minus RB-QIG balanced is +43.8 points [+28.9, +58.4].
- RB-QIG balanced and blanket QI are statistically tied under the LLM attacker: RB-QIG minus blanket is -6.7 points [-20.0, +6.7].

## Stronger-Attacker Smoke

Command:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_attack_eval.py --input results/ratbench_d1_api_100/anonymized_outputs_with_llm_direct.jsonl --attacks-out results/ratbench_d1_api_100/llm_attacker_stronger20_outputs.jsonl --usage-out results/ratbench_d1_api_100/llm_attacker_stronger20_usage.jsonl --metrics-out results/ratbench_d1_api_100/llm_attacker_stronger20_metrics.csv --cache-dir results/api_cache/llm_attacker --methods direct llm_direct blanket_qi rbqig_b4 --model gpt-5.4-mini --limit-records-per-method 20
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_api_100/llm_attacker_stronger20_outputs.jsonl --source-type llm-attacker --source-name ratbench_d1_api_100_stronger20_llm_attacker --cis-out results/ratbench_d1_api_100/llm_attacker_stronger20_bootstrap_cis.csv --contrasts-out results/ratbench_d1_api_100/llm_attacker_stronger20_bootstrap_contrasts.csv --report-out results/ratbench_d1_api_100/llm_attacker_stronger20_bootstrap_report.md --per-record-out results/ratbench_d1_api_100/llm_attacker_stronger20_per_record_metrics.csv --n-boot 5000 --seed 20260627 --comparisons direct:llm_direct llm_direct:rbqig_b4 direct:rbqig_b4 rbqig_b4:blanket_qi
```

Metrics: `results/ratbench_d1_api_100/llm_attacker_stronger20_metrics.csv`

Fresh-equivalent cost: $0.143337 for 80 calls.

| Method | Record compromise | Exact attr leak | Coarse attr leak | Risk-weighted leak |
|---|---:|---:|---:|---:|
| Direct | 80.0% | 76.8% | 81.3% | 77.3% |
| LLM direct | 25.0% | 43.4% | 49.7% | 40.2% |
| Blanket QI | 5.0% | 17.4% | 22.0% | 16.0% |
| RB-QIG balanced | 10.0% | 16.2% | 24.9% | 18.0% |

Interpretation:

- The stronger model is harsher on privacy methods than `gpt-5.4-nano`, especially on generalized or placeholder-heavy rows.
- The main comparison survives: direct minus RB-QIG balanced is +59.3 risk-weighted leakage points [+46.3, +72.4], and naive LLM sanitizer minus RB-QIG balanced is +22.2 points [+11.0, +34.2].
- RB-QIG balanced remains statistically tied with blanket QI under the stronger attacker: +2.0 points [-3.7, +6.9].
- Treat this as an attacker-strength robustness smoke, not a replacement for the 100-row low-cost attacker table.

## Bootstrap Analysis Artifacts

Commands:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/synthetic_100/anonymized_outputs.jsonl --source-type transformed --source-name synthetic_100 --cis-out results/synthetic_100/bootstrap_cis.csv --contrasts-out results/synthetic_100/bootstrap_contrasts.csv --report-out results/synthetic_100/bootstrap_report.md --per-record-out results/synthetic_100/per_record_metrics.csv --n-boot 5000 --seed 20260627
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/synthetic_100/llm_utility_outputs.jsonl --source-type metrics-jsonl --source-name synthetic_100_llm_utility --cis-out results/synthetic_100/llm_utility_bootstrap_cis.csv --contrasts-out results/synthetic_100/llm_utility_bootstrap_contrasts.csv --report-out results/synthetic_100/llm_utility_bootstrap_report.md --per-record-out results/synthetic_100/llm_utility_per_record_metrics.csv --metrics label_preservation llm_fact_preservation semantic_utility_score --n-boot 5000 --seed 20260627
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_api_100/anonymized_outputs.jsonl --source-type transformed --source-name ratbench_d1_api_100_deterministic --cis-out results/ratbench_d1_api_100/bootstrap_cis.csv --contrasts-out results/ratbench_d1_api_100/bootstrap_contrasts.csv --report-out results/ratbench_d1_api_100/bootstrap_report.md --per-record-out results/ratbench_d1_api_100/per_record_metrics.csv --n-boot 5000 --seed 20260627
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_api_100/llm_attacker_outputs_with_llm_direct.jsonl --source-type llm-attacker --source-name ratbench_d1_api_100_llm_attacker_with_llm_direct --cis-out results/ratbench_d1_api_100/llm_bootstrap_cis_with_llm_direct.csv --contrasts-out results/ratbench_d1_api_100/llm_bootstrap_contrasts_with_llm_direct.csv --report-out results/ratbench_d1_api_100/llm_bootstrap_report_with_llm_direct.md --per-record-out results/ratbench_d1_api_100/llm_per_record_metrics_with_llm_direct.csv --n-boot 5000 --seed 20260627 --comparisons direct:llm_direct llm_direct:rbqig_b4 direct:rbqig_b4 rbqig_b4:blanket_qi
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_blind_backstop_api_100/anonymized_outputs.jsonl --source-type transformed --source-name ratbench_d1_blind_backstop_api_100 --cis-out results/ratbench_d1_blind_backstop_api_100/bootstrap_cis.csv --contrasts-out results/ratbench_d1_blind_backstop_api_100/bootstrap_contrasts.csv --report-out results/ratbench_d1_blind_backstop_api_100/bootstrap_report.md --per-record-out results/ratbench_d1_blind_backstop_api_100/per_record_metrics.csv --n-boot 5000 --seed 20260627
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_blind_backstop_api_100/llm_attacker_outputs.jsonl --source-type llm-attacker --source-name ratbench_d1_blind_backstop_api_100_llm_attacker --cis-out results/ratbench_d1_blind_backstop_api_100/llm_bootstrap_cis.csv --contrasts-out results/ratbench_d1_blind_backstop_api_100/llm_bootstrap_contrasts.csv --report-out results/ratbench_d1_blind_backstop_api_100/llm_bootstrap_report.md --per-record-out results/ratbench_d1_blind_backstop_api_100/llm_per_record_metrics.csv --n-boot 5000 --seed 20260627
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_blind_backstop_api_100/llm_utility_outputs.jsonl --source-type metrics-jsonl --source-name ratbench_d1_blind_backstop_api_100_llm_utility --cis-out results/ratbench_d1_blind_backstop_api_100/llm_utility_bootstrap_cis.csv --contrasts-out results/ratbench_d1_blind_backstop_api_100/llm_utility_bootstrap_contrasts.csv --report-out results/ratbench_d1_blind_backstop_api_100/llm_utility_bootstrap_report.md --per-record-out results/ratbench_d1_blind_backstop_api_100/llm_utility_per_record_metrics.csv --metrics label_preservation llm_fact_preservation semantic_utility_score --n-boot 5000 --seed 20260627
```

The bootstrap layer gives paper-ready uncertainty for the main claims without spending more API budget.

## API Budget

Cached API usage currently present in this workspace:

| Cache | Files | Tokens | Estimated cost |
|---|---:|---:|---:|
| QI extractor | 131 | 264,898 | $0.092983 |
| LLM attacker | 1,148 | 1,947,320 | $0.662570 |
| LLM direct sanitizer | 130 | 376,483 | $0.263876 |
| Blind QI extractor | 30 | 27,785 | $0.021809 |
| Blind RAT-Bench QI extractor | 100 | 252,021 | $0.134941 |
| LLM utility judge | 864 | 2,015,506 | $0.532039 |
| LLM privacy-aware utility judge | 120 | 419,418 | $0.100685 |
| LLM legal utility judge | 50 | 125,308 | $0.039890 |
| Total | 2,573 | 5,428,739 | $1.848793 |

## Blind Synthetic Extractor Check

Command:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/api_qi_extractor.py --blind --eval-against-original-qis --input data/synthetic/synthetic_30.jsonl --out data/processed/synthetic_30_blind_api_qi.jsonl --usage-out results/synthetic_30_blind_api/usage.json --cache-dir results/api_cache/blind_qi_extractor --n 30 --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/synthetic_30_blind_api_qi.jsonl --out results/synthetic_30_blind_api/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/synthetic_30_blind_api/anonymized_outputs.jsonl --attacks-out results/synthetic_30_blind_api/attacker_outputs.jsonl --utility-out results/synthetic_30_blind_api/utility_outputs.jsonl --metrics-out results/synthetic_30_blind_api/metrics.csv
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/synthetic_30_blind_api/anonymized_outputs.jsonl --source-type transformed --source-name synthetic_30_blind_api --cis-out results/synthetic_30_blind_api/bootstrap_cis.csv --contrasts-out results/synthetic_30_blind_api/bootstrap_contrasts.csv --report-out results/synthetic_30_blind_api/bootstrap_report.md --per-record-out results/synthetic_30_blind_api/per_record_metrics.csv --n-boot 5000 --seed 20260627
```

Metrics: `results/synthetic_30_blind_api/metrics.csv`

| Method | Risk-weighted leak | Utility facts | Token change |
|---|---:|---:|---:|
| Direct | 100.0% | 100.0% | 13.4% |
| Blanket QI | 3.2% | 36.1% | 62.9% |
| RB-QIG balanced | 5.2% | 43.3% | 55.8% |

Interpretation:

- The blind rerun used cached extractor responses only; every row was `cache=True`, so no new API requests were made.
- Keeping richer suggested generalizations and dropping low-risk/high-utility blind candidates improves RB-QIG balanced utility-fact preservation from the earlier 32.5% to 43.3% [35.0%, 51.7%].
- The tradeoff is that oracle-measured risk-weighted leakage rises to 5.2% [1.7%, 9.7%]. This is still a diagnostic result: deployment-style blind extraction needs better utility-aware filtering and semantic utility evaluation, while the target-aware benchmark result isolates transformation behavior.

## TAB ECHR Second-Domain Deterministic Screen

Command:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/load_tab.py --split dev --n 30 --annotator-mode first --out data/processed/tab_echr_dev_30.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/tab_echr_dev_30.jsonl --out results/tab_echr_dev_30/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/tab_echr_dev_30/anonymized_outputs.jsonl --attacks-out results/tab_echr_dev_30/attacker_outputs.jsonl --utility-out results/tab_echr_dev_30/utility_outputs.jsonl --metrics-out results/tab_echr_dev_30/metrics.csv
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/tab_echr_dev_30/anonymized_outputs.jsonl --source-type transformed --source-name tab_echr_dev_30 --cis-out results/tab_echr_dev_30/bootstrap_cis.csv --contrasts-out results/tab_echr_dev_30/bootstrap_contrasts.csv --report-out results/tab_echr_dev_30/bootstrap_report.md --per-record-out results/tab_echr_dev_30/per_record_metrics.csv --n-boot 5000 --seed 20260627 --comparisons direct:rbqig_b4 rbqig_b4:blanket_qi blanket_qi:rbqig_b4
```

Report: `results/tab_echr_dev_30/tab_screen_report.md`

| Method | Risk-weighted leak | Utility facts | Token change |
|---|---:|---:|---:|
| Direct | 99.8% | 100.0% | 1.0% |
| Blanket QI | 0.0% | 100.0% | 14.0% |
| RB-QIG balanced | 12.3% | 100.0% | 13.9% |

Interpretation:

- This is a useful second-domain deterministic diagnostic, not a main utility
  result.
- Direct TAB redaction leaves nearly all TAB quasi-identifiers visible under
  deterministic scoring; RB-QIG balanced reduces risk-weighted leakage by 87.5
  points [84.0, 90.6] relative to direct redaction.
- RB-QIG balanced remains leakier than blanket QI by 12.3 points [9.1, 15.8],
  because generalized dates, institutions, quantities, and participant roles
  still count as coarse recoverable cues.
- The TAB deterministic utility proxy is too broad to support a utility
  advantage claim. A 10-document legal-task LLM utility screen is also
  inconclusive: blanket QI, RB-QIG balanced, and RB-QIG utility all score 68.0%
  [62.0, 74.0] overall legal-task utility. RB-QIG balanced minus blanket is 0.0
  points [-10.0, 10.0], and RB-QIG utility minus blanket is 0.0 points [-8.0,
  8.0]. Direct redaction remains higher at 80.0% [74.0, 86.0].

## TAB Legal-Role Generalization Diagnostic

Report: `results/tab_echr_dev_30_legal_role/legal_role_screen_report.md`

This was a bounded branch to test whether more legally meaningful replacements
such as `a domestic court`, `a custodial sentence`, and `a compensation amount`
improve TAB legal-task utility.

| Method | Deterministic risk-weighted leak | Legal-task utility | Timeline | Legal specificity |
|---|---:|---:|---:|---:|
| Direct | 99.8% | 80.0% | 80.0% | 70.0% |
| Blanket QI | 0.0% | 68.0% | 68.0% | 52.0% |
| RB-QIG balanced legal-role | 8.3% | 62.0% | 62.0% | 50.0% |

Interpretation:

- Legal-role replacements reduce deterministic RB-QIG balanced leakage relative
  to the generic TAB RB-QIG screen, from 12.3% to 8.3%.
- They do not improve legal-task utility: RB-QIG balanced legal-role minus
  blanket QI is -6.0 points [-14.0, 2.0].
- This closes the obvious "better labels might fix TAB utility" branch as a
  negative diagnostic. The likely remaining issue is that short role labels
  still disrupt chronology and legal specificity.
- The run added 10 uncached calls, 24,946 tokens, and $0.008006. Direct and
  blanket rows reused the existing legal utility cache.

## Presidio-Style Pattern Baseline

Command:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/presidio_pattern_baseline.py --input data/processed/ratbench_english_d1_100_api_qi.jsonl --out results/presidio_pattern_ratbench_d1_100/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/presidio_pattern_baseline.py --input data/processed/tab_echr_dev_30.jsonl --out results/presidio_pattern_tab_echr_dev_30/anonymized_outputs.jsonl
```

Report: `results/presidio_pattern_baseline_report.md`

| Dataset | Method | Direct ID leak | Risk-weighted leak | Token change |
|---|---|---:|---:|---:|
| RAT-Bench D1 100 | Presidio pattern-only | 37.0% | 85.0% | 1.5% |
| RAT-Bench D1 100 | RB-QIG balanced | 0.0% | 28.6% | 7.0% |
| TAB ECHR 30 | Presidio pattern-only | 100.0% | 99.8% | 0.4% |
| TAB ECHR 30 | RB-QIG balanced | 0.0% | 12.3% | 13.9% |

Interpretation:

- This is a practical lower-bound baseline, not full Presidio. It uses Presidio
  framework pattern recognizers with a blank tokenizer and no downloaded NER
  model.
- The existing direct baseline is oracle-assisted and stronger on direct IDs:
  it removes all benchmark direct identifiers, while the pattern-only baseline
  leaves direct-ID leakage in 37% of RAT-Bench rows and 100% of TAB rows.
- This strengthens the paper's conservative framing: the main direct baseline
  is not weak, and common PII patterns are not enough for legal-domain text.

## Revised Next Research Step

Generated paper tables:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/make_paper_tables.py
```

Outputs:

- `paper/generated/tables.md`
- `paper/generated/tables.tex`

Generated qualitative appendix:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/make_qualitative_appendix.py
```

Output:

- `paper/QUALITATIVE_APPENDIX.md`

Generated paper claim audit:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/make_claim_audit.py
```

Output:

- `paper/CLAIM_AUDIT.md` (15/15 audited claim groups matched `paper/main.tex`)

Plan-to-evidence audit:

- `paper/PLAN_TO_EVIDENCE_AUDIT.md`

Reviewer-facing stress test:

- `paper/REVIEWER_STRESS_TEST.md`

Current manuscript:

```bash
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Artifacts:

- `paper/main.tex`
- `paper/references.bib`
- `paper/main.pdf` (verified 4 pages with `pdfinfo`)
- `paper/QUALITATIVE_APPENDIX.md`
- `paper/CLAIM_AUDIT.md`
- `paper/PLAN_TO_EVIDENCE_AUDIT.md`
- `paper/REVIEWER_STRESS_TEST.md`

1. Improve task-realistic utility evaluation beyond broad labels; public and TAB utility remain the weakest evidence.
2. Run a tiny multi-model attacker agreement check only under a fixed API cap.
3. Tighten the 4-page manuscript for the target workshop style once the final template is chosen.
4. Improve blind extractor coverage and utility-aware generalization before making any deployment-style claim.
5. Consider scaling RAT-Bench beyond 100 rows only if the paper needs tighter confidence intervals; the 40-record budget-variant smoke did not justify a full public budget sweep.
