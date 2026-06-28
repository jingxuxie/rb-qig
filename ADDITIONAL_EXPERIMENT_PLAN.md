# Additional Experiments Plan for RB-QIG

This plan prioritizes experiments that make the workshop paper more complete without turning the project into a large-scale training effort. The current repository is **not fully no-API** anymore: no API calls are required for the default synthetic pipeline, but the current paper evidence uses cached API calls for RAT-Bench quasi-identifier extraction, LLM-attacker evaluation, and utility judging.

## Recommended claim boundary

Keep the paper's main claim disciplined:

> Direct PII redaction and naive LLM sanitization leave substantial residual quasi-identifier inference risk. RB-QIG sharply reduces measured residual risk relative to those baselines and preserves more utility than blanket quasi-identifier redaction in controlled synthetic settings. Public utility preservation and robust blind extraction remain open problems.

Do **not** claim legal anonymization, deployment readiness, state-of-the-art de-identification, privacy superiority over blanket QI redaction, or public RAT-Bench utility superiority over blanket QI redaction.

## Priority 0: no-API experiments first

These improve the paper without spending API budget.

### 0.1 Pairwise-combination-risk ablation

**Question:** Does the pairwise combination penalty in the document risk score matter?

Current score:

```text
R(x) = sum_i r_i + 0.5 * C(number of high-risk spans, 2)
```

Add a variant:

```text
RB-QIG no-combo: R(x) = sum_i r_i
```

Run it on:

- `results/synthetic_100/`
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/` using deterministic scoring
- `results/tab_echr_dev_30/` using deterministic scoring

Report:

| Dataset | Method | Risk-weighted leakage | Utility/fact preservation | Token change |
|---|---:|---:|---:|---:|
| Synthetic | RB-QIG balanced | existing | existing | existing |
| Synthetic | RB-QIG no-combo | new | new | new |
| RAT-Bench blind | RB-QIG balanced | existing | existing | existing |
| RAT-Bench blind | RB-QIG no-combo | new | new | new |

**Interpretation:** If no-combo is worse, this justifies the combination-risk term. If it is tied, the paper can honestly say the heuristic works but the current pilot does not isolate the pairwise term.

### 0.2 Public budget sweep with deterministic scoring

You already have strict/balanced/utility variants on synthetic. Add a deterministic public sweep for:

```text
rbqig_b2, rbqig_b4, rbqig_b6
```

Run on:

- RAT-Bench D1 blind-backstop 100
- TAB 30

Report a compact frontier:

| Dataset | Budget | Risk-weighted leakage ↓ | QI specificity ↑ | Token change ↓ |
|---|---:|---:|---:|---:|
| RAT-Bench blind | 2 |  |  |  |
| RAT-Bench blind | 4 |  |  |  |
| RAT-Bench blind | 6 |  |  |  |
| TAB | 2 |  |  |  |
| TAB | 4 |  |  |  |
| TAB | 6 |  |  |  |

**Interpretation:** This shows the budget knob is meaningful beyond the synthetic benchmark.

### 0.3 Failure-category appendix table

Convert the current qualitative failure examples into a compact table:

| Failure type | Example cue | Why direct span removal misses it | Possible fix |
|---|---|---|---|
| Relational implication | `my parent is American` | citizenship is inferred, not named | relation-aware rewrite |
| Gendered language | pronouns or family roles | sex is inferred from context | neutralization pass |
| Cultural cue | heritage or tradition mention | race/ethnicity inferred from culture | broader cultural placeholder |
| Institution cue | school/employer name | education/employment inferred | institution ladder |
| Placeholder leakage | `[DEMOGRAPHIC]` in heritage context | placeholder reveals attribute type | neutral placeholder policy |

This is a high-value analysis improvement and does not require new API calls.

## Priority 1: bounded GPT-5.5 experiment

### 1.1 Strong-attacker robustness check

**Question:** Do the main privacy conclusions hold under a stronger attacker?

Use existing transformed outputs. Do not rerun extraction. Do not ask GPT-5.5 to create sanitized text. Use it only as an evaluator/attacker.

Recommended setting:

```text
Dataset: RAT-Bench D1 blind-backstop 100
Methods: direct, blanket_qi, rbqig_b4
Optional method: llm_direct if already present in the file
Model: gpt-5.5
Records: start with 50 per method; expand to 100 only if cost is comfortable
Prompt: same structured attacker prompt as src/llm_attack_eval.py
```

Suggested command pattern:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/llm_attack_eval.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/anonymized_outputs.jsonl --attacks-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_gpt55_outputs.jsonl --usage-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_gpt55_usage.jsonl --metrics-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_gpt55_metrics.csv --cache-dir results/api_cache/llm_attacker_gpt55 --methods direct blanket_qi rbqig_b4 --model gpt-5.5 --limit-records-per-method 50
```

Then bootstrap:

```bash
/home/eston/anaconda3/envs/rb_qig/bin/python src/bootstrap_results.py --input results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_gpt55_outputs.jsonl --source-type llm-attacker --source-name ratbench_d1_blind_gpt55_attacker --cis-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_gpt55_bootstrap_cis.csv --contrasts-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_gpt55_bootstrap_contrasts.csv --report-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_gpt55_bootstrap_report.md --per-record-out results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_gpt55_per_record_metrics.csv --n-boot 5000 --seed 20260628 --comparisons direct:rbqig_b4 rbqig_b4:blanket_qi
```

Add only a short robustness paragraph unless the result is very clean.

Possible outcomes:

- **Good:** GPT-5.5 preserves the ordering: direct redaction is high leakage; RB-QIG stays near blanket redaction.
- **Acceptable:** GPT-5.5 recovers more from RB-QIG than the cheaper attacker, but RB-QIG remains far below direct redaction.
- **Bad but publishable:** GPT-5.5 recovers many RB-QIG attributes. Report this as evidence that current ladders need stronger semantic neutralization; the paper becomes a sharper warning paper.

### 1.2 Multi-model attacker agreement

Run the same 20--50 record subset with:

```text
gpt-5.4-nano
gpt-5.4-mini
gpt-5.5
```

Report agreement on exact/coarse leakage:

| Pair | Exact-leak agreement | Coarse-leak agreement | Notes |
|---|---:|---:|---|
| nano vs mini |  |  |  |
| nano vs GPT-5.5 |  |  |  |
| mini vs GPT-5.5 |  |  |  |

This addresses the reviewer objection that the attacker is noisy or model-specific.

## Priority 2: utility experiments

Utility is the weakest part of the current evidence. Do not spend most of the remaining time only making the attacker stronger while leaving utility weak.

### 2.1 Privacy-aware utility judge on public RAT-Bench

The current public LLM utility judge ties RB-QIG and blanket redaction. Add a more task-like judge that asks:

```text
Can the transformed text still support the benign conversational/task intent, excluding protected demographic attributes?
```

Score:

- task intent preserved
- non-sensitive constraints preserved
- answerability preserved
- sensitive attribute not required

Run only 30--50 records. Compare direct, blanket_qi, and rbqig_b4.

### 2.2 TAB legal task utility, slightly larger if cheap

Current TAB legal utility is inconclusive. If any TAB API experiment is run, use a bounded 20-document screen and evaluate specific slots:

- procedural posture
- legal issue category
- timeline order
- remedy/outcome
- party role without party identity

Stop if RB-QIG is still tied with or worse than blanket after 20 documents.

## Priority 3: practical baseline

### 3.1 Full Presidio baseline if environment allows

The current practical baseline is pattern-only and should be described as a lower bound. If dependency setup is easy, add:

```text
Presidio Analyzer + Anonymizer with default recognizers
```

Run on:

- RAT-Bench D1 100
- TAB 30

Compare pattern-only, full Presidio, oracle direct redaction, blanket QI, and RB-QIG. Skip this if setup becomes expensive; the manuscript already labels the current baseline as pattern-only.

## Cost and privacy guardrails

Use only public or synthetic benchmark records. Do not send private user data to any API. Keep GPT-5.5 experiments bounded to 50 records per method until cost is observed. Cache every request and record model, prompt version, timestamp, and token usage.

## Minimal package before submission

1. Add the polished manuscript text.
2. Add a short current-API-usage statement in the paper and README.
3. Run the no-combo ablation on synthetic and blind RAT-Bench.
4. Run GPT-5.5 attacker on 50 blind RAT-Bench records using existing outputs.
5. Add one paragraph on stronger-attacker robustness.
6. Add one appendix table on residual failure categories.
7. Keep the claim boundary disciplined.
