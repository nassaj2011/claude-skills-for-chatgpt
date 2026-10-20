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

## v0.4 extensions

- [Complete 29-case specification](29-skill-benchmark.json) — 29 thoughtfully designed **NOT_RUN** cases, not results
- [Archived 2-case A/B report](V0_4_RESULTS.md) — independent Codex sessions and inspectable saved responses
- [Reproducible prompt builder](../scripts/prepare_benchmark.py) — emits read-only baseline/candidate task text with `--case`, `--mode` and `--output`. It does **not** call a model, verify native skill routing or claim execution
- [Executable test suites](../docs/V0_4_RELEASE.md) — transaction, UI state and offline SLO gates, all run without private data

The catalog's earlier seven-case rubric and initial PR-review pilot remain preserved. To evaluate the remaining cases, repeat several genuine agent runs per case under matched conditions, score blind where possible and archive full outputs before making comparative claims.

## v0.6 prepared comparisons — not scored

Pre-registered prompts/rubrics for privacy, load resilience and visual assets are in `prompts/v05-privacy.txt`, `prompts/v06-load.txt`, `prompts/v06-visual.txt`, and `benchmarks/v06-*-criteria.json`. Model A/B could not be run because the Codex service returned HTTP 404; there are **no** valid v06 raw outputs or grades. See [V0_6_RESULTS.md](V0_6_RESULTS.md). Source and web distribution parity are checked separately and are not causal evidence.

## v0.7 — six matched real text-only Codex evaluations

See [case rubrics](v07-quality-benchmarks.json), [saved run manifest](v07-run-manifest.json) and [evaluation limitations](V0_7_RESULTS.md). Twelve raw text outputs exist in runs/v07-*.txt (the unrelated probe is excluded). Run `python scripts/verify_v07_runs.py` to verify their hashes. These six cases are **COMPLETE BUT UNSCORED**, so no verified skill quality uplift percentage is claimed.
