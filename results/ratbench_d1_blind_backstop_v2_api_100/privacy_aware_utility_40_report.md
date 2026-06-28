# Privacy-Aware Utility Screen

This bounded 40-record screen re-scores the original blind public v2 outputs
with a utility judge that does not penalize removal or generalization of private
protected attributes unless a coarse, non-identifying category is needed for the
downstream task.

Artifacts:

- Outputs: `results/ratbench_d1_blind_backstop_v2_api_100/llm_privacy_aware_utility_40_outputs.jsonl`
- Metrics: `results/ratbench_d1_blind_backstop_v2_api_100/llm_privacy_aware_utility_40_metrics.csv`
- Bootstrap report: `results/ratbench_d1_blind_backstop_v2_api_100/llm_privacy_aware_utility_40_bootstrap_report.md`

## Metrics

| Method | Privacy-aware label | Task content | Privacy-aware utility | Private-loss penalty |
|---|---:|---:|---:|---:|
| Direct | 100.0% | 91.7% | 86.5% | 0.0% |
| Blanket QI | 100.0% | 82.0% | 87.5% | 2.5% |
| RB-QIG balanced | 100.0% | 79.6% | 83.0% | 0.0% |

Paired RB-QIG balanced minus blanket QI:

- Task content preservation: -2.4 points [-5.3, 0.4]
- Privacy-aware utility: -4.5 points [-9.0, 0.0]
- Private-loss penalty: -2.5 points [-7.5, 0.0]

Cost: 120 new calls, 419,418 tokens, and $0.100685.

## Interpretation

This is a useful diagnostic but not a paper headline. Privacy-aware framing
raises the utility scores of privacy methods relative to a stricter public
utility judge, but it still does not produce an RB-QIG utility advantage over
blanket QI on public RAT-Bench. The result supports the current caveat: the
utility win is controlled-synthetic, while public utility evaluation remains
the weakest evidence.
