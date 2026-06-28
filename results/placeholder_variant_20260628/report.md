# Budgeted Placeholder Rewrite Diagnostic

This no-training diagnostic tests `rbqig_b4_placeholder`, a conservative
fallback that uses the same RB-QIG balanced budget selection but renders each
selected quasi-identifier as a typed placeholder instead of an extractor-proposed
natural-language generalization. The goal is to separate the budget policy from
fragile surface rewrites such as `Generalize to ...` or `I am a marital status`.

## Commands

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/run_methods.py --input data/processed/ratbench_english_d1_100_blind_backstop_v2_api_qi.jsonl --out results/placeholder_variant_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl --methods direct blanket_qi rbqig_b4 rbqig_b4_placeholder
/home/eston/anaconda3/envs/rb_qig/bin/python src/evaluate_outputs.py --input results/placeholder_variant_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl --attacks-out results/placeholder_variant_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/attacker_outputs.jsonl --utility-out results/placeholder_variant_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/utility_outputs.jsonl --metrics-out results/placeholder_variant_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/metrics.csv
/home/eston/anaconda3/envs/rb_qig/bin/python src/qi_specificity_eval.py --input results/placeholder_variant_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl --source-name ratbench_placeholder_variant_20260628 --per-record-out results/placeholder_variant_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_per_record.jsonl --metrics-out results/placeholder_variant_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_metrics.csv --report-out results/placeholder_variant_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/qi_specificity_report.md
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/placeholder_variant_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl --source-type transformed --source-name ratbench_placeholder_variant_20260628 --cis-out results/placeholder_variant_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_cis.csv --contrasts-out results/placeholder_variant_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_contrasts.csv --report-out results/placeholder_variant_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_report.md --per-record-out results/placeholder_variant_20260628/ratbench_d1_blind_backstop_v2_budgetfix_api_100/per_record_metrics.csv --n-boot 5000 --seed 20260628 --comparisons rbqig_b4_placeholder:rbqig_b4 rbqig_b4_placeholder:blanket_qi direct:rbqig_b4_placeholder
```

The same deterministic screen was run on `data/processed/tab_echr_dev_30.jsonl`.
A bounded 50-record RAT-Bench privacy-aware utility screen was then run for
`direct`, `blanket_qi`, and `rbqig_b4_placeholder`.

## RAT-Bench Deterministic Result

| Method | Risk-weighted leak | QI specificity | Token change |
|---|---:|---:|---:|
| Blanket QI | 3.1% | 26.4% | 10.8% |
| RB-QIG balanced | 5.4% | 33.2% | 10.1% |
| RB-QIG placeholder | 4.1% | 27.1% | 10.3% |

Paired deterministic contrasts:

- Placeholder minus balanced risk: -1.3 points [-2.3, -0.4].
- Placeholder minus blanket risk: +1.0 points [0.0, 3.0].
- Placeholder removes the obvious rewrite artifacts in the first 100 rows:
  `rbqig_b4` has 15 rows with literal instruction phrases and 19 rows with
  simple grammar artifacts; `rbqig_b4_placeholder` has 0 of each.

## RAT-Bench Privacy-Aware Utility, 50 Records

| Method | Task content | Privacy-aware utility |
|---|---:|---:|
| Direct | 91.6% | 86.0% |
| Blanket QI | 81.3% | 88.0% |
| RB-QIG balanced | 77.7% | 81.6% |
| RB-QIG placeholder | 80.3% | 84.8% |

Paired utility contrasts:

- Placeholder minus balanced task content: +2.5 points [+0.3, +4.8].
- Placeholder minus balanced privacy-aware utility: +3.2 points [-0.8, +7.2].
- Placeholder minus blanket task content: -1.1 points [-3.3, +1.1].
- Placeholder minus blanket privacy-aware utility: -3.2 points [-7.2, +0.8].

Cache/cost:

- Direct and blanket rows reused cache.
- Placeholder utility screen added 50 fresh calls, 174,979 tokens, and $0.042431.
- Fresh-equivalent utility-judge cost for all 150 judged rows was $0.125621.

## TAB Deterministic Result

| Method | Risk-weighted leak | QI specificity | Token change |
|---|---:|---:|---:|
| Blanket QI | 0.0% | 25.0% | 14.0% |
| RB-QIG balanced | 12.3% | 31.2% | 13.9% |
| RB-QIG placeholder | 0.0% | 25.0% | 14.0% |

On TAB, placeholder mode degenerates to blanket QI: it removes the deterministic
coarse leakage left by RB-QIG balanced but also removes the specificity
advantage.

## Interpretation

`rbqig_b4_placeholder` is a useful fallback for paper discussion, not a new
headline method. It shows that the public utility failure is partly a surface
rewrite problem: replacing fragile natural-language generalizations with typed
placeholders visibly fixes artifacts and improves privacy-aware utility relative
to current RB-QIG. But it mostly gives up the specificity advantage that made
RB-QIG distinct from blanket QI, and it still does not establish public utility
superiority over blanket redaction. The next algorithmic step should be
context-aware fluent rewriting, not more evaluator spending on placeholder
variants.
