# RB-QIG Figure Plan

This file describes the figure placeholders inserted into `paper/main.tex`. The goal is to make the paper faster to understand and reduce the number overload in the main text.

## Figure 1: Conceptual overview

**Purpose:** Help a reviewer understand the paper in 10 seconds.

**Where:** Introduction.

**Recommended design:** Three-panel schematic.

### Panel A: Why direct PII removal fails

Show a short text snippet before/after direct redaction.

Example:

```text
Original:
Maria Chen, a 34-year-old oncology infusion pharmacist in Asheville, emailed ...

Direct redaction:
[PERSON], a 34-year-old oncology infusion pharmacist in Asheville, emailed ...
```

Highlight the surviving quasi-identifiers:

- age
- rare occupation
- location
- institution/domain cue
- family relation
- date/event
- condition/legal/financial fact

Main label: **Direct identifiers removed; inferable profile remains.**

### Panel B: RB-QIG pipeline

Draw boxes with arrows:

```text
Candidate QIs
   ↓
Risk + utility scores
   ↓
Generalization ladders
   ↓
Budgeted greedy edits
   ↓
Transformed text + audit log
```

Use one example ladder:

```text
Asheville, NC → city in southeastern U.S. → U.S. region → [LOCATION]
```

### Panel C: Main empirical message

Use a small icon-based frontier:

```text
Direct redaction: high utility, high leakage
Blanket QI: low leakage, low utility
RB-QIG: controlled middle ground
```

Avoid many numbers in this figure. It should be a conceptual anchor.

## Figure 2: Privacy--utility frontier

**Purpose:** Replace dense synthetic and utility tables with an intuitive plot.

**Where:** Experiments/results transition.

**Recommended design:** Two panels.

### Panel A: Synthetic controlled frontier

Data source:

- `results/synthetic_100/metrics.csv`
- `results/synthetic_100/bootstrap_cis.csv`

Plot:

- X-axis: risk-weighted leakage, lower is better.
- Y-axis: utility-fact preservation, higher is better.
- Points:
  - Direct
  - Blanket QI
  - RB-QIG strict
  - RB-QIG balanced
  - RB-QIG utility
- Connect RB-QIG strict → balanced → utility with a line.
- Use arrows or a label: **better = upper-left**.

Expected visual message:

- Direct is upper-right: useful but leaky.
- Blanket QI is lower-left: safe but low utility.
- RB-QIG points form a tunable frontier.

### Panel B: Blind public RAT-Bench utility caveat

Data sources:

- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_metrics.csv`
- `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_utility_metrics.csv`

Plot:

- X-axis: LLM risk-weighted leakage.
- Y-axis: semantic utility.
- Points:
  - Direct
  - Blanket QI
  - RB-QIG balanced

Expected visual message:

- RB-QIG and Blanket QI are close on privacy.
- Public semantic utility does not show a meaningful RB-QIG advantage.
- This supports a careful, honest narrative.

## Figure 3: Attacker robustness

**Purpose:** Make the GPT-5.5 and multi-model results easy to read.

**Where:** Results section, after the stronger-attacker paragraph.

**Recommended design:** Grouped bar chart.

Data sources:

- low-cost/nano blind attacker:
  - `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_metrics.csv`
- mini attacker:
  - `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_attacker_mini20_metrics.csv`
- GPT-5.5 attacker:
  - use your new GPT-5.5 metrics artifact, likely under `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/`

Plot:

- X-axis groups: Direct, Blanket QI, RB-QIG balanced.
- Bars: low-cost attacker, mini attacker, GPT-5.5 attacker.
- Y-axis: risk-weighted leakage.
- Optional: bootstrap confidence intervals as error bars.

Expected visual message:

- Stronger attackers increase absolute leakage.
- Direct redaction remains worst.
- RB-QIG and Blanket QI remain close.
- The method should not be sold as an anonymization guarantee.

## Figure 4: Budget frontier and domain transfer

**Purpose:** Show that the risk budget is a real policy knob.

**Where:** Results section, after the budget-diagnostics paragraph.

**Recommended design:** Two-panel scatter/line plot.

### Panel A: Blind RAT-Bench budget frontier

Data source:

- budget diagnostic artifacts for blind RAT-Bench, or the values currently in the draft.

Plot:

- X-axis: deterministic risk-weighted leakage.
- Y-axis: annotation-derived QI specificity.
- Points: RB-QIG budget 2, 4, 6, plus Blanket QI.
- Connect budget 2 → budget 4 → budget 6.

Expected visual message:

- Larger budgets preserve more specificity but leak more.
- Blanket QI is low leakage and low specificity.

### Panel B: TAB budget frontier

Data source:

- TAB budget diagnostic artifacts.

Same axes and point types as Panel A.

Expected visual message:

- The same qualitative budget trend appears in a second domain.

## Table strategy

Keep only these tables in the main paper:

1. QI taxonomy table.
2. Headline result map.
3. Failure-category table.

Move detailed numeric tables to the appendix using:

```latex
\appendix
\section{Detailed Numeric Tables}
\input{generated/tables.tex}
```

This keeps the main paper readable while preserving reproducibility and evidence.

## Main-text number policy

Use numbers only when they anchor a core claim.

Recommended main-text numbers:

- One synthetic headline:
  - RB-QIG balanced: 23.6% leakage, 71.7% utility facts.
  - Blanket QI: 0.0% leakage, 43.3% utility facts.
- One target-aware RAT-Bench headline:
  - Direct: 78.0%.
  - Naive LLM: 46.0%.
  - RB-QIG: 5.7%.
- One stronger-attacker headline:
  - GPT-5.5 raises leakage but preserves ordering.

Everything else should be in figures, tables, or appendix.
