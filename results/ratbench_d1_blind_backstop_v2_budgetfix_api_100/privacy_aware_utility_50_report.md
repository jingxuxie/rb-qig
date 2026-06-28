# Privacy-Aware Utility Screen, 50 Records

This bounded screen evaluates the paper-facing budget-fixed blind-backstop v2
RAT-Bench outputs with the privacy-aware utility judge. The judge is instructed
not to penalize removal or generalization of direct identifiers or protected
benchmark quasi-identifiers unless the downstream task needs a coarse,
non-identifying category.

Artifacts:

- Outputs: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_privacy_aware_utility_50_outputs.jsonl`
- Metrics: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_privacy_aware_utility_50_metrics.csv`
- Bootstrap report: `results/ratbench_d1_blind_backstop_v2_budgetfix_api_100/llm_privacy_aware_utility_50_bootstrap_report.md`

## Metrics

| Method | Privacy-aware label | Task content | Privacy-aware utility | Private-loss penalty |
|---|---:|---:|---:|---:|
| Direct | 100.0% | 91.6% | 86.0% | 2.0% |
| Blanket QI | 100.0% | 81.3% | 88.0% | 2.0% |
| RB-QIG balanced | 100.0% | 77.7% | 81.6% | 0.0% |

Paired RB-QIG balanced minus blanket QI:

- Task content preservation: -3.6 points [-5.9, -1.4]
- Privacy-aware utility: -6.4 points [-10.0, -2.8]
- Private-loss penalty: -2.0 points [-6.0, 0.0]

Cache/cost:

- 150 judged rows, 113 cache hits, 37 fresh calls.
- Fresh added cost: $0.031086.
- Fresh-equivalent cost for all rows: $0.125911.

## Interpretation

The privacy-aware framing does not rescue the public RAT-Bench utility claim.
RB-QIG balanced remains below blanket QI on task content and privacy-aware
utility. This supports the paper's conservative boundary: public utility
preservation remains an open problem, while the positive utility claim should
stay scoped to controlled synthetic utility facts.
