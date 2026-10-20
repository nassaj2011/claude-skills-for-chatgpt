# Agent skill A/B evaluation protocol

The rubric in [cases.json](cases.json) contains **seven realistic prompts**, one for each new v0.2 skill, with independent weighted success criteria. **These are test cases, not evidence that an agent has been evaluated.**

## Run a genuine comparison

1. Choose one case from `cases.json`, freeze commit, model, tool permissions and environment. Keep the task data constant.
2. Execute the baseline without the targeted skill. Save exact prompt, command, timestamp, token/cost usage if available, and full output/observable artifacts.
3. Execute a separate session with the skill deliberately enabled or selected. Same model, tools and budget; save all output.
4. Independent reviewer marks each criterion `passed: true|false` with a nonempty `evidence` identifying an output file, log line, repository diff, runtime check or explicit absence.
5. Put all **seven** cases in both run files before running the comparison CLI. No partial results are silently ignored.
6. Run several repetitions and include routing negative cases to measure variance and accidental activation; do not publish one small trial as definitive.

Run-file schema:

```json
{
  "metadata": {
    "run_id": "real-model-run-2026-10-20-a",
    "synthetic": false,
    "model": "exact-model-id",
    "environment": "OS, repo SHA, agent CLI versions, permitted tools",
    "notes": "cost/latency and links to archived complete responses"
  },
  "results": {
    "pr-gate-01": {
      "conditional-verdict": {
        "passed": true,
        "evidence": "results/pr-gate-01/with-skill.txt: lines 18-22"
      }
    }
  }
}
```

The example is illustrative; actual run files must include **every** case and rubric criterion.

## Test the scorer itself (synthetic fixture)

```bash
python scripts/evaluate_skills.py --cases evals/fixtures/demo_cases.json --baseline evals/fixtures/demo_baseline.json --candidate evals/fixtures/demo_candidate.json
```

This produces `SYNTHETIC_DEMONSTRATION` and **must not be reported as an actual model-quality improvement**. `--require-real` will reject the supplied synthetic example.

To run genuine results:
```bash
python scripts/evaluate_skills.py --cases evals/cases.json --baseline evals/runs/real_baseline.json --candidate evals/runs/real_candidate.json --require-real --json
```

**Limitations:** Manual boolean scores can be biased; external reviewers and objective executable tests improve confidence. No score establishes causal effect without controlling run conditions and variance. A skill's mere installation is not evidence that it triggered.

## First actual-agent pilot

The [PR-review A/B pilot](PILOT_RESULT.md) contains saved genuine Codex output for the same fictional review scenario with and without the `code-review-pr` instruction text. Both runs scored 100% (0 percentage-point change); this small pilot does not prove benefit or harm and was not a host-native automatic skill-trigger test.

Recompute the recorded judgments:
```bash
python scripts/evaluate_skills.py --cases evals/pilot_cases.json --baseline evals/runs/pilot-pr-baseline.json --candidate evals/runs/pilot-pr-candidate.json --require-real
```
