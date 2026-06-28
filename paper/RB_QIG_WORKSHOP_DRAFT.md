# Beyond PII Removal: Risk-Budgeted Generalization for LLM-Ready Sensitive Text

## Abstract

Sensitive text corpora are valuable for foundation-model training, retrieval, and evaluation, but common de-identification pipelines often focus on direct PII spans such as names, emails, and phone numbers. We study residual inference risk from quasi-identifiers: dates, locations, occupations, schools, demographic attributes, medical/legal/financial facts, family relations, and combinations that remain informative after direct redaction. We propose Risk-Budgeted Quasi-Identifier Generalization (RB-QIG), a lightweight transformation layer that scores quasi-identifiers by privacy risk and utility importance, then applies the least destructive generalization needed to satisfy a document-level risk budget. In a controlled synthetic benchmark, RB-QIG balanced reduces risk-weighted leakage to 23.6% [22.9, 24.5] while preserving 71.7% [70.8, 72.4] of utility facts, compared with 43.3% [39.9, 46.8] utility-fact preservation for blanket quasi-identifier redaction. On a 100-record English RAT-Bench pilot, direct redaction leaves 78.0% [73.4, 82.5] LLM-attacker risk-weighted leakage and a naive LLM sanitizer leaves 46.0% [40.1, 52.0], while RB-QIG balanced reduces it to 5.7% [3.2, 8.8]. We argue that responsible data transformation for foundation-model pipelines should evaluate what capable models can still infer, not only whether obvious PII spans were removed.

## 1. Introduction

Sensitive text contains information that could improve foundation models and downstream systems, but privacy risk often prevents direct use. Practical de-identification tools usually prioritize direct identifiers: names, emails, phone numbers, account IDs, addresses, and similar spans. This is necessary but incomplete. After direct identifiers are removed, text can still contain quasi-identifiers: combinations of age, location, occupation, school, demographic status, medical condition, legal event, family relation, or rare life history that allow a model or analyst to infer sensitive attributes.

This paper studies the gap between direct PII removal and residual inference risk. Our central claim is not that RB-QIG produces legally anonymous data. The claim is narrower: risk-aware generalization of quasi-identifiers can substantially reduce measured residual inference risk while preserving more task-relevant content than blanket redaction in controlled settings.

Contributions:

1. We define a practical taxonomy of quasi-identifiers for LLM-ready sensitive text.
2. We introduce RB-QIG, an auditable transformation policy that chooses generalizations under a document-level risk budget.
3. We evaluate direct redaction, blanket quasi-identifier redaction, and RB-QIG using deterministic leakage metrics and a cached LLM attacker.
4. We provide a failure taxonomy showing which residual cues still leak attributes after transformation.

## 2. Threat Model and Task

We assume an attacker receives transformed text, can use a capable LLM, and tries to infer benchmark attributes such as date of birth, demographic status, education, location, employment status, family structure, or sensitive domain facts. The attacker is restricted to benchmark attributes and is not asked to identify real people.

Inputs are synthetic or public benchmark records with known ground truth. We do not evaluate on private sensitive data.

Methods:

- **None:** original text.
- **Direct:** regex plus known benchmark direct identifiers.
- **LLM direct:** a naive LLM sanitizer applied after direct redaction.
- **Blanket QI:** redact all extracted quasi-identifiers.
- **RB-QIG strict / balanced / utility:** generalize selected quasi-identifiers under budgets 2, 4, and 6.

Metrics:

- exact attribute leakage,
- coarse attribute leakage,
- risk-weighted leakage,
- record compromise,
- token change rate,
- utility fact preservation.

## 3. Method

RB-QIG has four stages.

First, direct identifiers are removed using regexes and benchmark-provided direct identifiers. Second, quasi-identifiers are extracted either from oracle synthetic spans, a target-aware public benchmark extractor, or a blind extractor. Third, each quasi-identifier receives a privacy-risk score and utility-importance score. In the blind diagnostic, we also keep the extractor's suggested generalization and discard low-risk, high-utility candidates. Fourth, the system chooses transformations greedily by risk reduction per utility loss until document-level risk falls below a budget.

The document risk score is:

```text
doc_risk = sum_i privacy_risk_i + 0.5 * pairwise_linkability_count
```

RB-QIG applies generalization ladders instead of unconstrained rewriting. Examples:

- exact date -> year or decade,
- city/state -> broader region,
- rare occupation -> broad profession,
- disease name -> medical category,
- family detail -> broad relation,
- demographic value -> demographic attribute.

All edits are span replacements. This avoids unconstrained rewriting and makes every transformation auditable through a change log.

## 4. Experiments

### 4.1 Synthetic Controlled Benchmark

We generate 100 synthetic records across medical administration, legal intake, financial support, HR/workplace, and education-support domains. Each record includes direct identifiers, quasi-identifiers, ground-truth attributes, a utility label, and utility facts. This benchmark is controlled: oracle quasi-identifier spans are known.

### 4.2 RAT-Bench Public Pilot

We evaluate 100 English difficulty-1 RAT-Bench records. We use a cached target-aware extractor to find value-revealing spans and variants for benchmark target attributes. This setup isolates transformation behavior: given target quasi-identifiers, how should they be transformed? It is not a deployment-style blind extraction claim.

### 4.3 LLM Attacker

For the public benchmark, we run a cached LLM attacker on direct redaction, a naive LLM direct sanitizer, blanket QI redaction, and RB-QIG balanced. The attacker receives only transformed text and requested attribute names, then returns structured guesses with evidence. We score exact and coarse matches against benchmark ground truth.

### 4.4 Blind Extractor Diagnostics

To test deployment-style settings, we run a blind extractor without target attribute names. On synthetic records, we evaluate transformed outputs against the original oracle quasi-identifiers. On RAT-Bench, we run blind extraction over the 100 public records and evaluate against the benchmark QIs. A generic deterministic backstop adds common demographic, citizenship, education, employment, marital, and race/ethnicity cues that the blind LLM extractor often under-calls. These diagnostics ask whether risky spans can be discovered without being told which attributes will be scored. They apply a simple utility-aware conversion: low-risk, high-utility candidates are left unchanged, while retained candidates use the extractor's suggested generalization rather than a generic placeholder.

### 4.5 LLM Utility Judge

The deterministic utility metric is intentionally strict: it checks whether listed utility facts remain lexically or semantically matched through predefined acceptable terms. To test whether this underrates generalized text, we run a cached LLM utility judge on the 100-record synthetic benchmark and on the 100-record blind-backstop RAT-Bench outputs for direct redaction, blanket QI redaction, and RB-QIG balanced. The judge compares original and transformed text and scores downstream semantic utility without rewarding preserved direct identifiers.

## 5. Results

### 5.1 Synthetic Privacy-Utility Frontier

Source: `results/synthetic_100/metrics.csv`

| Method | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Utility facts | Token change |
|---|---:|---:|---:|---:|---:|---:|
| None | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% |
| Direct | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 13.5% |
| Blanket QI | 0.0% | 0.0% | 0.0% | 0.0% | 43.3% | 63.7% |
| RB-QIG strict | 0.0% | 0.0% | 32.8% | 16.1% | 48.3% | 59.3% |
| **RB-QIG balanced** | 0.0% | 0.0% | 49.1% | 23.6% | 71.7% | 59.0% |
| RB-QIG utility | 0.0% | 0.0% | 77.9% | 38.0% | 95.0% | 56.6% |

Direct redaction preserves utility but leaves all quasi-identifiers. Blanket QI redaction removes leakage but preserves only 43.3% of utility facts. RB-QIG balanced keeps risk-weighted leakage at 23.6% while preserving 71.7% of utility facts.

Bootstrap intervals over record IDs show the synthetic tradeoff is stable: RB-QIG balanced improves utility-fact preservation over blanket QI by 28.3 percentage points [25.2, 31.6], at the cost of 23.6 points [22.9, 24.5] additional risk-weighted leakage. This is the cleanest evidence for the intended privacy-utility frontier.

### 5.2 Synthetic LLM Utility Judge

Source: `results/synthetic_100/llm_utility_metrics.csv`

| Method | Label preserved | LLM fact preservation | Semantic utility |
|---|---:|---:|---:|
| Direct | 100.0% | 75.3% | 83.2% |
| Blanket QI | 99.0% | 69.1% | 76.8% |
| **RB-QIG balanced** | 100.0% | 71.3% | 79.4% |

The LLM utility judge gives a more forgiving view of blanket redaction than the deterministic utility metric: placeholders often preserve the broad task type even when specific utility facts are lost. RB-QIG balanced still has a small semantic-utility edge over blanket QI: +2.6 percentage points [0.6, 4.8]. Its LLM fact-preservation edge is +2.2 points [-0.2, 4.8], so we treat this as supportive but not decisive. The main utility claim remains the controlled deterministic utility-fact result.

### 5.3 Public RAT-Bench LLM Utility Caveat

Source: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_metrics.csv`

| Method | Label preserved | LLM fact preservation | Semantic utility |
|---|---:|---:|---:|
| Direct | 99.0% | 84.3% | 86.2% |
| Blanket QI | 99.0% | 53.8% | 62.6% |
| **RB-QIG balanced** | 96.0% | 55.5% | 62.2% |

The public utility judge is a cautionary result. Both blanket QI and RB-QIG balanced lose substantial utility relative to direct redaction, and RB-QIG balanced is statistically tied with blanket QI on semantic utility: -0.4 points [-4.2, 3.4]. Its public fact-preservation edge is also non-significant: +1.7 points [-3.4, 6.6]. This means the public RAT-Bench pilot supports the residual-risk claim, but not a public utility advantage over blanket redaction.

### 5.4 RAT-Bench Deterministic Leakage

Source: `results/ratbench_d1_api_100/metrics.csv`

| Method | Record compromise | Exact QI leak | Coarse QI leak | Risk-weighted leak | Utility facts | Token change |
|---|---:|---:|---:|---:|---:|---:|
| None | 92.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% |
| Direct | 92.0% | 94.9% | 94.9% | 93.8% | 100.0% | 0.9% |
| Blanket QI | 1.0% | 0.3% | 0.3% | 0.3% | 100.0% | 7.1% |
| RB-QIG strict | 1.0% | 0.3% | 51.8% | 23.1% | 100.0% | 7.0% |
| **RB-QIG balanced** | 1.0% | 0.8% | 63.0% | 28.6% | 100.0% | 7.0% |
| RB-QIG utility | 1.0% | 0.8% | 72.2% | 33.2% | 100.0% | 6.9% |

The public benchmark confirms the residual-risk motivation: direct redaction leaves 93.8% [91.0, 96.3] risk-weighted quasi-identifier leakage. RB-QIG balanced reduces deterministic risk-weighted leakage to 28.6% [25.4, 31.9], a paired reduction of 65.2 percentage points [61.4, 68.8].

### 5.5 RAT-Bench LLM Attacker

Source: `results/ratbench_d1_api_100/llm_attacker_metrics_with_llm_direct.csv`

| Method | Record compromise | Exact attr leak | Coarse attr leak | Risk-weighted leak |
|---|---:|---:|---:|---:|
| Direct | 76.0% | 74.9% | 81.2% | 78.0% |
| LLM direct | 34.0% | 48.7% | 52.8% | 46.0% |
| Blanket QI | 3.0% | 3.9% | 7.3% | 5.3% |
| **RB-QIG balanced** | 2.0% | 4.0% | 8.8% | 5.7% |

The LLM attacker recovers many attributes after direct redaction and after a naive LLM sanitizer. The sanitizer lowers risk-weighted leakage from 78.0% [73.4, 82.5] to 46.0% [40.1, 52.0], but RB-QIG balanced reduces it further to 5.7% [3.2, 8.8]. The paired RB-QIG reduction is 72.2 points [67.0, 77.4] relative to direct redaction and 40.2 points [33.1, 47.1] relative to the LLM sanitizer. RB-QIG balanced is statistically tied with blanket QI on this privacy metric: the paired risk-weighted difference is 0.5 points [-2.6, 3.6]. Therefore the public pilot supports the privacy reduction claim relative to direct and naive LLM redaction, but the utility advantage over blanket redaction currently comes from the synthetic controlled benchmark rather than RAT-Bench.

A 30-row English RAT-Bench difficulty-2 smoke gives the same qualitative LLM-attacker result on harder demographic-heavy rows. Direct redaction leaves 70.8% [56.4, 83.7] risk-weighted leakage, naive LLM sanitization leaves 56.9% [42.6, 71.3], and RB-QIG balanced lowers leakage to 13.1% [3.3, 25.0]. RB-QIG balanced is statistically tied with blanket QI on this smoke: -6.7 points [-20.0, 6.7].

A 20-record stronger-attacker smoke with `gpt-5.4-mini` is harsher on privacy methods, but preserves the main ordering. Direct redaction leaves 77.3% [64.1, 88.9] risk-weighted leakage, naive LLM sanitization leaves 40.2% [29.4, 51.1], and RB-QIG balanced leaves 18.0% [10.4, 26.2]. RB-QIG balanced is statistically tied with blanket QI: +2.0 points [-3.7, 6.9].

### 5.6 Blind Extractor Diagnostics

Source: `results/synthetic_30_blind_api/metrics.csv`

| Method | Risk-weighted leak | Utility facts | Token change |
|---|---:|---:|---:|
| Direct | 100.0% | 100.0% | 13.4% |
| Blanket QI | 3.2% | 36.1% | 62.9% |
| **RB-QIG balanced** | 5.2% | 43.3% | 55.8% |

Source: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/metrics.csv`

| Method | Record compromise | Exact QI leak | Risk-weighted leak | Token change |
|---|---:|---:|---:|---:|
| Direct | 39.0% | 94.4% | 94.3% | 0.9% |
| Blanket QI | 0.0% | 3.1% | 3.1% | 10.8% |
| **RB-QIG balanced** | 0.0% | 4.6% | 5.4% | 10.1% |

The utility-aware blind conversion improves utility relative to generic blind redaction on synthetic data, but the result remains diagnostic rather than a central claim. On synthetic records, RB-QIG balanced preserves 43.3% [35.0, 51.7] of utility facts and leaves 5.2% [1.7, 9.7] oracle-measured risk-weighted leakage. On public RAT-Bench, the raw blind extractor covers 72.8% of benchmark QI spans; the improved generic backstop raises coverage to 99.6% without additional API calls. Budget-fixed backstopped blind RB-QIG balanced reduces deterministic risk-weighted leakage relative to direct redaction by 88.9 points [85.0, 92.5], but it is 2.3 points [0.6, 4.9] leakier than blanket QI under deterministic coarse scoring.

The LLM attacker gives a more deployment-facing privacy read on the same blind-backstop outputs. Direct redaction leaves 78.1% [73.3, 82.9] LLM-attacker risk-weighted leakage, while RB-QIG balanced lowers it to 6.4% [3.9, 9.1], a paired reduction of 71.8 points [66.4, 76.9]. RB-QIG balanced and blanket QI are statistically tied under this attacker: -0.5 points [-2.5, 1.5]. This motivates better extraction-time coverage, utility scoring, and relational-cue handling, while avoiding the stronger claim that RB-QIG is more private than blanket redaction.

### 5.7 Failure Taxonomy

Source: `results/ratbench_d1_api_100/failure_taxonomy.md`

Representative positive examples, target-aware public comparisons, and a blind
public failure case are generated in `paper/QUALITATIVE_APPENDIX.md` by
`src/make_qualitative_appendix.py`.

Uncertainty reports are generated in `results/synthetic_100/bootstrap_report.md`, `results/synthetic_100/llm_utility_bootstrap_report.md`, `results/ratbench_d1_api_100/bootstrap_report.md`, `results/ratbench_d1_api_100/llm_bootstrap_report_with_llm_direct.md`, `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/bootstrap_report.md`, `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_bootstrap_report.md`, `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_bootstrap_report.md`, and `results/synthetic_30_blind_api/bootstrap_report.md`.

Residual leakage after RB-QIG comes mainly from:

- gendered context,
- marital or bereavement context,
- education institution or credential,
- citizenship phrasing,
- employment or armed-forces status,
- race or ethnicity variants,
- location context.

These are not just missed exact spans. They are relational and contextual cues. This supports the paper's broader point: privacy transformation should consider what models can infer, not just which spans match a PII schema.

## 6. Limitations and Ethics

RB-QIG is not an anonymization guarantee and should not be used as a legal-compliance claim. The current main public benchmark extraction is target-aware, so it evaluates transformation behavior under known benchmark attributes rather than fully blind deployment. The blind public and synthetic diagnostics suggest that utility-aware blind conversion helps but still leaves a difficult extraction and coverage tradeoff. The public LLM utility judge shows no meaningful utility advantage for RB-QIG over blanket QI on RAT-Bench, so the large utility claim remains limited to the controlled synthetic benchmark. LLM attackers and judges are low-cost automated evaluators and may under- or over-estimate real adversaries or utility needs.

All experiments use synthetic or public benchmark data. We do not attempt to identify real people or infer attributes about private individuals.

## 7. Discussion

The results support a workshop-ready claim: direct PII redaction leaves substantial residual inference risk, and risk-budgeted quasi-identifier handling can dramatically reduce measured leakage when quasi-identifiers are known or well extracted. Synthetic experiments show the intended privacy-utility tradeoff. RAT-Bench confirms the residual-risk problem with a public LLM-attacker evaluation. The remaining challenge is robust blind extraction that preserves task-relevant utility while covering relational cues.

The strongest final paper framing is therefore measurement plus method: RB-QIG is not a finished anonymizer, but a practical, auditable transformation layer and evaluation protocol for studying residual quasi-identifier risk in LLM-ready sensitive text.
