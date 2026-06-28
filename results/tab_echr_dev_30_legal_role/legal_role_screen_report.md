# TAB ECHR Legal-Role Generalization Diagnostic

This bounded diagnostic tests whether more legally meaningful quasi-identifier
generalizations improve TAB legal-task utility. It keeps the original generic
TAB screen unchanged and derives a separate input where selected TAB
generalizations use labels such as `a domestic court`, `a detention facility`,
`a custodial sentence`, and `a compensation amount`.

## Commands

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/load_tab.py --split dev --n 30 --annotator-mode first --generalization-mode legal_role --out data/processed/tab_echr_dev_30_legal_role.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/tab_echr_dev_30_legal_role.jsonl --out results/tab_echr_dev_30_legal_role/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/tab_echr_dev_30_legal_role/anonymized_outputs.jsonl --attacks-out results/tab_echr_dev_30_legal_role/attacker_outputs.jsonl --utility-out results/tab_echr_dev_30_legal_role/utility_outputs.jsonl --metrics-out results/tab_echr_dev_30_legal_role/metrics.csv
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/tab_echr_dev_30_legal_role/anonymized_outputs.jsonl --source-type transformed --source-name tab_echr_dev_30_legal_role --cis-out results/tab_echr_dev_30_legal_role/bootstrap_cis.csv --contrasts-out results/tab_echr_dev_30_legal_role/bootstrap_contrasts.csv --report-out results/tab_echr_dev_30_legal_role/bootstrap_report.md --per-record-out results/tab_echr_dev_30_legal_role/per_record_metrics.csv --n-boot 5000 --seed 20260628 --comparisons direct:rbqig_b4 rbqig_b4:blanket_qi blanket_qi:rbqig_b4
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_legal_utility_eval.py --input results/tab_echr_dev_30_legal_role/anonymized_outputs.jsonl --utility-out results/tab_echr_dev_30_legal_role/llm_legal_utility_10_outputs.jsonl --usage-out results/tab_echr_dev_30_legal_role/llm_legal_utility_10_usage.jsonl --metrics-out results/tab_echr_dev_30_legal_role/llm_legal_utility_10_metrics.csv --cache-dir results/api_cache/llm_legal_utility --methods direct blanket_qi rbqig_b4 --limit-records-per-method 10 --model gpt-5.4-nano --max-output-tokens 800
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/tab_echr_dev_30_legal_role/llm_legal_utility_10_outputs.jsonl --source-type metrics-jsonl --source-name tab_echr_dev_30_legal_role_llm_legal_utility_10 --cis-out results/tab_echr_dev_30_legal_role/llm_legal_utility_10_bootstrap_cis.csv --contrasts-out results/tab_echr_dev_30_legal_role/llm_legal_utility_10_bootstrap_contrasts.csv --report-out results/tab_echr_dev_30_legal_role/llm_legal_utility_10_bootstrap_report.md --per-record-out results/tab_echr_dev_30_legal_role/llm_legal_utility_10_per_record_metrics.csv --metrics legal_summary_preservation procedure_preservation legal_issue_preservation timeline_preservation outcome_or_remedy_preservation legal_specificity legal_task_utility --n-boot 5000 --seed 20260628 --comparisons direct:rbqig_b4 rbqig_b4:blanket_qi
```

## Results

Deterministic metrics:

| Method | Risk-weighted leak | Coarse QI leak | Token change |
| --- | ---: | ---: | ---: |
| Direct | 99.8% | 99.7% | 1.0% |
| Blanket QI | 0.0% | 0.0% | 14.0% |
| RB-QIG balanced | 8.3% | 18.7% | 13.9% |
| RB-QIG utility | 15.6% | 33.3% | 13.8% |

Legal-task LLM utility on the fixed first 10 TAB documents:

| Method | Legal-task utility | Timeline | Legal specificity |
| --- | ---: | ---: | ---: |
| Direct | 80.0% | 80.0% | 70.0% |
| Blanket QI | 68.0% | 68.0% | 52.0% |
| RB-QIG balanced | 62.0% | 62.0% | 50.0% |

Bootstrap source:
`results/tab_echr_dev_30_legal_role/llm_legal_utility_10_bootstrap_report.md`

- RB-QIG balanced minus blanket legal-task utility: -6.0 points [-14.0, 2.0].
- RB-QIG balanced minus blanket timeline preservation: -6.0 points [-14.0, 2.0].
- RB-QIG balanced minus blanket legal specificity: -2.0 points [-12.0, 8.0].
- Direct minus RB-QIG balanced legal-task utility: +18.0 points [14.0, 20.0].

The run added 10 uncached OpenAI calls for changed RB-QIG rows: 24,946 tokens,
estimated cost $0.008006. Direct and blanket rows reused the existing cache.

## Interpretation

This is a closed negative branch. Legal-role generalizations improve
deterministic privacy relative to the generic TAB RB-QIG screen, but they do
not improve task-realistic legal utility. The likely issue is that replacing
many case-specific dates, institutions, and quantities with short role labels
still disrupts chronology and legal specificity. Keep the main paper focused on
the generic TAB screen as residual-risk support and treat public legal utility
as a caveat.
