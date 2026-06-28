# TAB ECHR 30-Document Deterministic Screen

This is a bounded second-domain diagnostic using the public TAB ECHR dev split.
No OpenAI API calls are made. The loader maps TAB `DIRECT` annotations to direct
identifiers and TAB `QUASI` annotations to quasi-identifiers, then reuses the
existing deterministic RB-QIG transformation and evaluator.

## Commands

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/load_tab.py --split dev --n 30 --annotator-mode first --out data/processed/tab_echr_dev_30.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/tab_echr_dev_30.jsonl --out results/tab_echr_dev_30/anonymized_outputs.jsonl
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/tab_echr_dev_30/anonymized_outputs.jsonl --attacks-out results/tab_echr_dev_30/attacker_outputs.jsonl --utility-out results/tab_echr_dev_30/utility_outputs.jsonl --metrics-out results/tab_echr_dev_30/metrics.csv
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/tab_echr_dev_30/anonymized_outputs.jsonl --source-type transformed --source-name tab_echr_dev_30 --cis-out results/tab_echr_dev_30/bootstrap_cis.csv --contrasts-out results/tab_echr_dev_30/bootstrap_contrasts.csv --report-out results/tab_echr_dev_30/bootstrap_report.md --per-record-out results/tab_echr_dev_30/per_record_metrics.csv --n-boot 5000 --seed 20260627 --comparisons direct:rbqig_b4 rbqig_b4:blanket_qi blanket_qi:rbqig_b4
```

## Metrics

Source: `results/tab_echr_dev_30/metrics.csv`

| Method | Direct ID leak | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Utility facts | Token change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| None | 100.0% | 100.0% | 99.8% | 99.8% | 99.9% | 100.0% | 0.0% |
| Direct | 0.0% | 100.0% | 99.7% | 99.7% | 99.8% | 100.0% | 1.0% |
| Blanket QI | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% | 100.0% | 14.0% |
| RB-QIG strict | 0.0% | 0.0% | 0.0% | 17.4% | 7.8% | 100.0% | 13.9% |
| RB-QIG balanced | 0.0% | 0.0% | 0.0% | 27.4% | 12.3% | 100.0% | 13.9% |
| RB-QIG utility | 0.0% | 0.0% | 0.0% | 43.6% | 20.4% | 100.0% | 13.9% |

Bootstrap source: `results/tab_echr_dev_30/bootstrap_report.md`

- Direct risk-weighted leakage: 99.8% [99.4, 100.0]
- RB-QIG balanced risk-weighted leakage: 12.3% [9.2, 15.7]
- Direct minus RB-QIG balanced risk-weighted leakage: +87.5 points [84.0, 90.6]
- RB-QIG balanced minus blanket QI risk-weighted leakage: +12.3 points [9.1, 15.8]

## Interpretation

- This supports the residual-risk story in a second public domain: direct
  redaction removes direct TAB identifiers but leaves nearly all TAB
  quasi-identifiers visible under deterministic scoring.
- RB-QIG balanced sharply reduces deterministic risk relative to direct
  redaction, but remains leakier than blanket QI because generalized dates,
  institutions, quantities, and participant roles still count as coarse
  recoverable cues.
- The current TAB utility proxy is deliberately weak. It only checks broad legal
  proceeding words, so 100% utility-fact preservation should not be used as a
  utility advantage claim.
- Treat this as a cross-domain deterministic diagnostic, not as a main paper
  utility result or deployment claim.

## Legal-Task LLM Utility Screen

To check whether the broad deterministic TAB utility proxy hides useful
differences, we ran a fixed 10-document LLM utility screen for
privacy-preserving legal case summarization. The final screen includes direct
redaction, blanket QI, RB-QIG balanced, and RB-QIG utility. It used 40
fresh-equivalent calls; the 10 new RB-QIG utility calls cost $0.008304.

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_legal_utility_eval.py --input results/tab_echr_dev_30/anonymized_outputs.jsonl --utility-out results/tab_echr_dev_30/llm_legal_utility_10_with_b6_outputs.jsonl --usage-out results/tab_echr_dev_30/llm_legal_utility_10_with_b6_usage.jsonl --metrics-out results/tab_echr_dev_30/llm_legal_utility_10_with_b6_metrics.csv --cache-dir results/api_cache/llm_legal_utility --methods direct blanket_qi rbqig_b4 rbqig_b6 --limit-records-per-method 10 --model gpt-5.4-nano --max-output-tokens 800
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/tab_echr_dev_30/llm_legal_utility_10_with_b6_outputs.jsonl --source-type metrics-jsonl --source-name tab_echr_dev_30_llm_legal_utility_10_with_b6 --cis-out results/tab_echr_dev_30/llm_legal_utility_10_with_b6_bootstrap_cis.csv --contrasts-out results/tab_echr_dev_30/llm_legal_utility_10_with_b6_bootstrap_contrasts.csv --report-out results/tab_echr_dev_30/llm_legal_utility_10_with_b6_bootstrap_report.md --per-record-out results/tab_echr_dev_30/llm_legal_utility_10_with_b6_per_record_metrics.csv --metrics legal_summary_preservation procedure_preservation legal_issue_preservation timeline_preservation outcome_or_remedy_preservation legal_specificity legal_task_utility --n-boot 5000 --seed 20260628 --comparisons direct:rbqig_b4 direct:rbqig_b6 rbqig_b4:blanket_qi rbqig_b6:blanket_qi rbqig_b6:rbqig_b4
```

Source: `results/tab_echr_dev_30/llm_legal_utility_10_with_b6_metrics.csv`

| Method | Legal summary preserved | Timeline | Legal specificity | Legal-task utility |
| --- | ---: | ---: | ---: | ---: |
| Direct | 100.0% | 80.0% | 70.0% | 80.0% |
| Blanket QI | 100.0% | 68.0% | 52.0% | 68.0% |
| RB-QIG balanced | 100.0% | 62.0% | 50.0% | 68.0% |
| RB-QIG utility | 100.0% | 64.0% | 48.0% | 68.0% |

Bootstrap source:
`results/tab_echr_dev_30/llm_legal_utility_10_with_b6_bootstrap_report.md`

- RB-QIG balanced minus blanket legal-task utility: 0.0 points [-10.0, 10.0]
- RB-QIG utility minus blanket legal-task utility: 0.0 points [-8.0, 8.0]
- RB-QIG utility minus RB-QIG balanced legal-task utility: 0.0 points [-8.0, 8.0]
- RB-QIG balanced minus blanket legal specificity: -2.0 points [-12.0, 8.0]
- Direct minus RB-QIG balanced legal-task utility: +12.0 points [6.0, 18.0]

Interpretation:

- The screen does not establish a TAB legal-utility advantage for RB-QIG or for
  the utility-budget variant.
- It is useful as a negative/caveat check: direct redaction preserves legal
  utility best, while both privacy methods lose legal timeline and specificity
  details. RB-QIG variants and blanket QI are statistically tied on legal-task
  utility, while `rbqig_b6` is substantially leakier in deterministic scoring.
