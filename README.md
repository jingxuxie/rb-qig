# RB-QIG: Risk-Budgeted Quasi-Identifier Generalization

This repository contains a fast research prototype for the workshop plan in
`rb_qig_workshop_plan.md`.

Current status:

- Synthetic controlled benchmark plus a 100-row public RAT-Bench pilot.
- No API calls by default.
- No third-party Python packages required.
- OpenAI API calls are optional, cached, and currently used for RAT-Bench
  quasi-identifier extraction, LLM-attacker evaluation, and utility judging.

## Quick Start

The available conda environment on this machine is named `rb_qig`.

```bash
conda run -n rb_qig python src/run_pilot.py --n 30 --seed 7
```

Outputs:

- `data/synthetic/synthetic_30.jsonl`
- `results/anonymized_outputs.jsonl`
- `results/attacker_outputs.jsonl`
- `results/utility_outputs.jsonl`
- `results/metrics.csv`
- `results/pilot_report.md`
- `results/qualitative_examples.md`
- `results/figures/privacy_utility_frontier.svg`
- `results/figures/leakage_by_method.svg`

For the larger synthetic control used in the current results:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_pilot.py --n 100 --seed 7 --out-dir results/synthetic_100
```

For the conservative public-data smoke test:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/load_ratbench.py --n 30 --config english --difficulty 1 --out data/processed/ratbench_english_d1_30.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/ratbench_english_d1_30.jsonl --out results/ratbench_d1_30/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/ratbench_d1_30/anonymized_outputs.jsonl --attacks-out results/ratbench_d1_30/attacker_outputs.jsonl --utility-out results/ratbench_d1_30/utility_outputs.jsonl --metrics-out results/ratbench_d1_30/metrics.csv
/home/eston/anaconda3/envs/rb_qig/bin/python src/plot_results.py --metrics results/ratbench_d1_30/metrics.csv --out-dir results/ratbench_d1_30/figures
```

For the current API-extracted RAT-Bench pilot:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/load_ratbench.py --n 100 --config english --difficulty 1 --out data/processed/ratbench_english_d1_100.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/api_qi_extractor.py --input data/processed/ratbench_english_d1_100.jsonl --out data/processed/ratbench_english_d1_100_api_qi.jsonl --usage-out results/ratbench_d1_api_100/usage.json --cache-dir results/api_cache/qi_extractor --n 100 --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/ratbench_english_d1_100_api_qi.jsonl --out results/ratbench_d1_api_100/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/ratbench_d1_api_100/anonymized_outputs.jsonl --attacks-out results/ratbench_d1_api_100/attacker_outputs.jsonl --utility-out results/ratbench_d1_api_100/utility_outputs.jsonl --metrics-out results/ratbench_d1_api_100/metrics.csv
/home/eston/anaconda3/envs/rb_qig/bin/python src/plot_results.py --metrics results/ratbench_d1_api_100/metrics.csv --out-dir results/ratbench_d1_api_100/figures
```

For the current LLM-attacker table:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_direct_redact.py --input results/ratbench_d1_api_100/anonymized_outputs.jsonl --out results/ratbench_d1_api_100/anonymized_outputs_with_llm_direct.jsonl --usage-out results/ratbench_d1_api_100/llm_direct_usage.jsonl --cache-dir results/api_cache/llm_direct_redact --merge --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_attack_eval.py --input results/ratbench_d1_api_100/anonymized_outputs_with_llm_direct.jsonl --attacks-out results/ratbench_d1_api_100/llm_attacker_outputs_with_llm_direct.jsonl --usage-out results/ratbench_d1_api_100/llm_attacker_usage_with_llm_direct.jsonl --metrics-out results/ratbench_d1_api_100/llm_attacker_metrics_with_llm_direct.csv --cache-dir results/api_cache/llm_attacker --methods direct llm_direct blanket_qi rbqig_b4 --model gpt-5.4-nano
```

For the 30-row RAT-Bench difficulty-2 robustness smoke:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/load_ratbench.py --n 30 --config english --difficulty 2 --out data/processed/ratbench_english_d2_30.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/api_qi_extractor.py --input data/processed/ratbench_english_d2_30.jsonl --out data/processed/ratbench_english_d2_30_api_qi.jsonl --usage-out results/ratbench_d2_api_30/usage.json --cache-dir results/api_cache/qi_extractor --n 30 --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/ratbench_english_d2_30_api_qi.jsonl --out results/ratbench_d2_api_30/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/ratbench_d2_api_30/anonymized_outputs.jsonl --attacks-out results/ratbench_d2_api_30/attacker_outputs.jsonl --utility-out results/ratbench_d2_api_30/utility_outputs.jsonl --metrics-out results/ratbench_d2_api_30/metrics.csv
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_direct_redact.py --input results/ratbench_d2_api_30/anonymized_outputs.jsonl --out results/ratbench_d2_api_30/anonymized_outputs_with_llm_direct.jsonl --usage-out results/ratbench_d2_api_30/llm_direct_usage.jsonl --cache-dir results/api_cache/llm_direct_redact --merge --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_attack_eval.py --input results/ratbench_d2_api_30/anonymized_outputs_with_llm_direct.jsonl --attacks-out results/ratbench_d2_api_30/llm_attacker_outputs_with_llm_direct.jsonl --usage-out results/ratbench_d2_api_30/llm_attacker_usage_with_llm_direct.jsonl --metrics-out results/ratbench_d2_api_30/llm_attacker_metrics_with_llm_direct.csv --cache-dir results/api_cache/llm_attacker --methods direct llm_direct blanket_qi rbqig_b4 --model gpt-5.4-nano
```

For the 20-record stronger-attacker smoke:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_attack_eval.py --input results/ratbench_d1_api_100/anonymized_outputs_with_llm_direct.jsonl --attacks-out results/ratbench_d1_api_100/llm_attacker_stronger20_outputs.jsonl --usage-out results/ratbench_d1_api_100/llm_attacker_stronger20_usage.jsonl --metrics-out results/ratbench_d1_api_100/llm_attacker_stronger20_metrics.csv --cache-dir results/api_cache/llm_attacker --methods direct llm_direct blanket_qi rbqig_b4 --model gpt-5.4-mini --limit-records-per-method 20
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_api_100/llm_attacker_stronger20_outputs.jsonl --source-type llm-attacker --source-name ratbench_d1_api_100_stronger20_llm_attacker --cis-out results/ratbench_d1_api_100/llm_attacker_stronger20_bootstrap_cis.csv --contrasts-out results/ratbench_d1_api_100/llm_attacker_stronger20_bootstrap_contrasts.csv --report-out results/ratbench_d1_api_100/llm_attacker_stronger20_bootstrap_report.md --per-record-out results/ratbench_d1_api_100/llm_attacker_stronger20_per_record_metrics.csv --n-boot 5000 --seed 20260627 --comparisons direct:llm_direct llm_direct:rbqig_b4 direct:rbqig_b4 rbqig_b4:blanket_qi
```

For the blind public RAT-Bench extractor diagnostic:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/api_qi_extractor.py --blind --eval-against-original-qis --input data/processed/ratbench_english_d1_100.jsonl --out data/processed/ratbench_english_d1_100_blind_backstop_v2_api_qi.jsonl --usage-out results/ratbench_d1_blind_backstop_v2_api_100/usage.json --cache-dir results/api_cache/ratbench_blind_qi_extractor --n 100 --model gpt-5.4-nano --max-output-tokens 2200
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/ratbench_english_d1_100_blind_backstop_v2_api_qi.jsonl --out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl --attacks-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/attacker_outputs.jsonl --utility-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/utility_outputs.jsonl --metrics-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/metrics.csv
/home/eston/anaconda3/envs/rb_qig/bin/python src/plot_results.py --metrics results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/metrics.csv --out-dir results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/figures
/home/eston/anaconda3/envs/rb_qig/bin/python src/analyze_blind_coverage.py --input data/processed/ratbench_english_d1_100_blind_backstop_v2_api_qi.jsonl --out-md results/ratbench_d1_blind_backstop_v2_api_100/blind_coverage_report.md --out-csv results/ratbench_d1_blind_backstop_v2_api_100/blind_coverage.csv
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_attack_eval.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl --attacks-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_outputs.jsonl --usage-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_usage.jsonl --metrics-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_metrics.csv --cache-dir results/api_cache/llm_attacker --methods direct blanket_qi rbqig_b4 --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/analyze_failures.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_outputs.jsonl --counts-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_failure_taxonomy.csv --examples-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_failure_examples.csv --md-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_failure_taxonomy.md
```

For the current synthetic LLM utility-judge table:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_utility_eval.py --input results/synthetic_100/anonymized_outputs.jsonl --utility-out results/synthetic_100/llm_utility_outputs.jsonl --usage-out results/synthetic_100/llm_utility_usage.jsonl --metrics-out results/synthetic_100/llm_utility_metrics.csv --cache-dir results/api_cache/llm_utility --methods direct blanket_qi rbqig_b4 --model gpt-5.4-nano
```

For the current blind public RAT-Bench LLM utility-judge table:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_utility_eval.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl --utility-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_outputs.jsonl --usage-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_usage.jsonl --metrics-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_metrics.csv --cache-dir results/api_cache/llm_utility --methods direct blanket_qi rbqig_b4 --model gpt-5.4-nano
```

For the no-API QI semantic-specificity diagnostic:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/qi_specificity_eval.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl --source-name ratbench_d1_blind_backstop_v2_budgetfix_api_100_qi_specificity --per-record-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_per_record.jsonl --metrics-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_metrics.csv --report-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_report.md
/home/eston/anaconda3/envs/rb_qig/bin/python src/qi_specificity_eval.py --input results/tab_echr_dev_30/anonymized_outputs.jsonl --source-name tab_echr_dev_30_qi_specificity --per-record-out results/tab_echr_dev_30/qi_specificity_per_record.jsonl --metrics-out results/tab_echr_dev_30/qi_specificity_metrics.csv --report-out results/tab_echr_dev_30/qi_specificity_report.md
```

For bootstrap confidence intervals:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/synthetic_100/anonymized_outputs.jsonl --source-type transformed --source-name synthetic_100 --cis-out results/synthetic_100/bootstrap_cis.csv --contrasts-out results/synthetic_100/bootstrap_contrasts.csv --report-out results/synthetic_100/bootstrap_report.md --per-record-out results/synthetic_100/per_record_metrics.csv --n-boot 5000 --seed 20260627
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/synthetic_100/llm_utility_outputs.jsonl --source-type metrics-jsonl --source-name synthetic_100_llm_utility --cis-out results/synthetic_100/llm_utility_bootstrap_cis.csv --contrasts-out results/synthetic_100/llm_utility_bootstrap_contrasts.csv --report-out results/synthetic_100/llm_utility_bootstrap_report.md --per-record-out results/synthetic_100/llm_utility_per_record_metrics.csv --metrics label_preservation llm_fact_preservation semantic_utility_score --n-boot 5000 --seed 20260627
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_api_100/anonymized_outputs.jsonl --source-type transformed --source-name ratbench_d1_api_100_deterministic --cis-out results/ratbench_d1_api_100/bootstrap_cis.csv --contrasts-out results/ratbench_d1_api_100/bootstrap_contrasts.csv --report-out results/ratbench_d1_api_100/bootstrap_report.md --per-record-out results/ratbench_d1_api_100/per_record_metrics.csv --n-boot 5000 --seed 20260627
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_api_100/llm_attacker_outputs_with_llm_direct.jsonl --source-type llm-attacker --source-name ratbench_d1_api_100_llm_attacker_with_llm_direct --cis-out results/ratbench_d1_api_100/llm_bootstrap_cis_with_llm_direct.csv --contrasts-out results/ratbench_d1_api_100/llm_bootstrap_contrasts_with_llm_direct.csv --report-out results/ratbench_d1_api_100/llm_bootstrap_report_with_llm_direct.md --per-record-out results/ratbench_d1_api_100/llm_per_record_metrics_with_llm_direct.csv --n-boot 5000 --seed 20260627 --comparisons direct:llm_direct llm_direct:rbqig_b4 direct:rbqig_b4 rbqig_b4:blanket_qi
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl --source-type transformed --source-name ratbench_d1_blind_backstop_v2_budgetfix_api_100 --cis-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_cis.csv --contrasts-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_contrasts.csv --report-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_report.md --per-record-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/per_record_metrics.csv --n-boot 5000 --seed 20260628 --comparisons direct:rbqig_b4 rbqig_b4:blanket_qi
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_outputs.jsonl --source-type llm-attacker --source-name ratbench_d1_blind_backstop_v2_budgetfix_api_100_llm_attacker --cis-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_bootstrap_cis.csv --contrasts-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_bootstrap_contrasts.csv --report-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_bootstrap_report.md --per-record-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_per_record_metrics.csv --n-boot 5000 --seed 20260628 --comparisons direct:rbqig_b4 rbqig_b4:blanket_qi
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_outputs.jsonl --source-type metrics-jsonl --source-name ratbench_d1_blind_backstop_v2_budgetfix_api_100_llm_utility --cis-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_bootstrap_cis.csv --contrasts-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_bootstrap_contrasts.csv --report-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_bootstrap_report.md --per-record-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_per_record_metrics.csv --metrics label_preservation llm_fact_preservation semantic_utility_score --n-boot 5000 --seed 20260628 --comparisons direct:rbqig_b4 rbqig_b4:blanket_qi
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_per_record.jsonl --source-type metrics-jsonl --source-name ratbench_d1_blind_backstop_v2_budgetfix_api_100_qi_specificity --cis-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_bootstrap_cis.csv --contrasts-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_bootstrap_contrasts.csv --report-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_bootstrap_report.md --per-record-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_bootstrap_per_record_metrics.csv --metrics utility_weighted_specificity qi_specificity_score qi_generalized_rate qi_placeholder_rate qi_exact_rate --n-boot 5000 --seed 20260628 --comparisons rbqig_b4:blanket_qi rbqig_b6:blanket_qi direct:rbqig_b4
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/tab_echr_dev_30/qi_specificity_per_record.jsonl --source-type metrics-jsonl --source-name tab_echr_dev_30_qi_specificity --cis-out results/tab_echr_dev_30/qi_specificity_bootstrap_cis.csv --contrasts-out results/tab_echr_dev_30/qi_specificity_bootstrap_contrasts.csv --report-out results/tab_echr_dev_30/qi_specificity_bootstrap_report.md --per-record-out results/tab_echr_dev_30/qi_specificity_bootstrap_per_record_metrics.csv --metrics utility_weighted_specificity qi_specificity_score qi_generalized_rate qi_placeholder_rate qi_exact_rate --n-boot 5000 --seed 20260627 --comparisons rbqig_b4:blanket_qi rbqig_b6:blanket_qi direct:rbqig_b4
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/synthetic_30_blind_api/anonymized_outputs.jsonl --source-type transformed --source-name synthetic_30_blind_api --cis-out results/synthetic_30_blind_api/bootstrap_cis.csv --contrasts-out results/synthetic_30_blind_api/bootstrap_contrasts.csv --report-out results/synthetic_30_blind_api/bootstrap_report.md --per-record-out results/synthetic_30_blind_api/per_record_metrics.csv --n-boot 5000 --seed 20260627
```

For generated paper tables:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/make_paper_tables.py
```

Outputs:

- `paper/generated/tables.md`
- `paper/generated/tables.tex`

For generated qualitative examples and failure-mode appendix:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/make_qualitative_appendix.py
```

Output:

- `paper/QUALITATIVE_APPENDIX.md`

For the paper claim audit:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/make_claim_audit.py
```

Output:

- `paper/CLAIM_AUDIT.md`

Plan-to-evidence audit for checking the original project plan against current
results:

- `paper/PLAN_TO_EVIDENCE_AUDIT.md`

Reviewer-facing claim and limitation stress test:

- `paper/REVIEWER_STRESS_TEST.md`

For the current LaTeX manuscript:

```bash
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Outputs:

- `paper/main.tex`
- `paper/references.bib`
- `paper/main.pdf`

For the blind synthetic extractor diagnostic:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/api_qi_extractor.py --blind --eval-against-original-qis --input data/synthetic/synthetic_30.jsonl --out data/processed/synthetic_30_blind_api_qi.jsonl --usage-out results/synthetic_30_blind_api/usage.json --cache-dir results/api_cache/blind_qi_extractor --n 30 --model gpt-5.4-nano
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/synthetic_30_blind_api_qi.jsonl --out results/synthetic_30_blind_api/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/synthetic_30_blind_api/anonymized_outputs.jsonl --attacks-out results/synthetic_30_blind_api/attacker_outputs.jsonl --utility-out results/synthetic_30_blind_api/utility_outputs.jsonl --metrics-out results/synthetic_30_blind_api/metrics.csv
```

For the TAB ECHR second-domain deterministic screen:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/load_tab.py --split dev --n 30 --annotator-mode first --out data/processed/tab_echr_dev_30.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/tab_echr_dev_30.jsonl --out results/tab_echr_dev_30/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/tab_echr_dev_30/anonymized_outputs.jsonl --attacks-out results/tab_echr_dev_30/attacker_outputs.jsonl --utility-out results/tab_echr_dev_30/utility_outputs.jsonl --metrics-out results/tab_echr_dev_30/metrics.csv
```

Reports:

- `results/tab_echr_dev_30/tab_screen_report.md`
- `results/tab_echr_dev_30/llm_legal_utility_10_with_b6_bootstrap_report.md`
- `results/tab_echr_dev_30_legal_role/legal_role_screen_report.md`

For the bounded 10-document TAB legal-task LLM utility screen:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_legal_utility_eval.py --input results/tab_echr_dev_30/anonymized_outputs.jsonl --utility-out results/tab_echr_dev_30/llm_legal_utility_10_with_b6_outputs.jsonl --usage-out results/tab_echr_dev_30/llm_legal_utility_10_with_b6_usage.jsonl --metrics-out results/tab_echr_dev_30/llm_legal_utility_10_with_b6_metrics.csv --cache-dir results/api_cache/llm_legal_utility --methods direct blanket_qi rbqig_b4 rbqig_b6 --limit-records-per-method 10 --model gpt-5.4-nano --max-output-tokens 800
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/tab_echr_dev_30/llm_legal_utility_10_with_b6_outputs.jsonl --source-type metrics-jsonl --source-name tab_echr_dev_30_llm_legal_utility_10_with_b6 --cis-out results/tab_echr_dev_30/llm_legal_utility_10_with_b6_bootstrap_cis.csv --contrasts-out results/tab_echr_dev_30/llm_legal_utility_10_with_b6_bootstrap_contrasts.csv --report-out results/tab_echr_dev_30/llm_legal_utility_10_with_b6_bootstrap_report.md --per-record-out results/tab_echr_dev_30/llm_legal_utility_10_with_b6_per_record_metrics.csv --metrics legal_summary_preservation procedure_preservation legal_issue_preservation timeline_preservation outcome_or_remedy_preservation legal_specificity legal_task_utility --n-boot 5000 --seed 20260628 --comparisons direct:rbqig_b4 direct:rbqig_b6 rbqig_b4:blanket_qi rbqig_b6:blanket_qi rbqig_b6:rbqig_b4
```

The generic with-`rbqig_b6` screen has $0.031884 fresh-equivalent cost. It is a
caveat, not a utility win: blanket QI, RB-QIG balanced, and RB-QIG utility are
tied on legal-task utility.

A follow-up legal-role generalization diagnostic is also negative:
`results/tab_echr_dev_30_legal_role/legal_role_screen_report.md`. It added 10
uncached calls ($0.008006) and found RB-QIG balanced legal-role below blanket QI
on legal-task utility: -6.0 points [-14.0, 2.0].

For the Presidio-style pattern-only practical baseline:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/presidio_pattern_baseline.py --input data/processed/ratbench_english_d1_100_api_qi.jsonl --out results/presidio_pattern_ratbench_d1_100/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/presidio_pattern_baseline.py --input data/processed/tab_echr_dev_30.jsonl --out results/presidio_pattern_tab_echr_dev_30/anonymized_outputs.jsonl
```

Report:

- `results/presidio_pattern_baseline_report.md`

## Interpretation Boundary

The synthetic benchmark is a controlled screen. It is useful for testing the
privacy-utility framing and implementation, but it should not be the only paper
evidence. The current public evidence is the 100-row RAT-Bench pilot with
target-aware QI extraction, a cached LLM attacker, and a blind public extractor
stress test.

The current RAT-Bench loader is intentionally conservative: it uses explicit
difficulty-1 rows and only creates quasi-identifier spans when the target value
appears in the text. It is a public-data smoke test, not the final benchmark
protocol.

The API extractor is also a pilot. It is target-aware for RAT-Bench: it uses the
benchmark ground-truth attributes to find all value-revealing spans and variants
in the public text. That is useful for measuring transformation behavior, but it
is not yet a deployment-style blind extractor.

The blind public RAT-Bench diagnostic is the deployment-style stress test. It
shows that blind RB-QIG balanced still reduces risk-weighted leakage relative to
direct redaction. An improved generic deterministic backstop raises benchmark QI
span coverage from 72.8% to 99.6% without additional API calls, but RB-QIG
remains slightly leakier than blanket QI redaction because generalized coarse
cues can still support attribute recovery under deterministic scoring. Under the LLM
attacker, blind-backstop RB-QIG balanced is statistically tied with blanket QI
while still sharply reducing leakage relative to direct redaction.

The LLM attacker table is useful paper evidence for residual inference risk, but
it currently covers only 100 English difficulty-1 RAT-Bench rows.

Bootstrap intervals are available for the current synthetic, deterministic
RAT-Bench, LLM-attacker, LLM utility-judge, blind public RAT-Bench, and blind
synthetic diagnostic tables. They support a strong claim that RB-QIG reduces
residual risk relative to direct redaction, but they do not support a claim that
RB-QIG is more private than blanket QI redaction on the current RAT-Bench pilot.
The LLM utility judge supports only a modest semantic-utility edge for RB-QIG
over blanket QI on synthetic data. On public blind RAT-Bench, it shows no
meaningful RB-QIG utility edge over blanket QI, so the larger utility claim
should be made from the controlled deterministic utility-fact metric. The
annotation-derived specificity diagnostic adds a narrow public utility signal:
RB-QIG balanced preserves more typed/generalized QI semantics than blanket
placeholders, but this is not downstream task accuracy.

The blind synthetic extractor diagnostic is intentionally treated as a
limitation result: utility-aware conversion improves semantic preservation over
generic blind redaction, but robust blind quasi-identifier extraction remains an
open problem.
