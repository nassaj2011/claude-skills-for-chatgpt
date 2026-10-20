# ChatGPT Web: skill-evaluation-benchmark

Original: https://github.com/nassaj2011/claude-skills-for-chatgpt

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

## Specialist workflow

# Skill evaluation and benchmarking

This evaluates *agent behavior*, not only whether SKILL.md parses.

1. State the skill's intended improvement and when it should **not** trigger. Choose representative task prompts, a negative routing case, and objective or human-reviewable success criteria.
2. Freeze comparable inputs: repository commit, target model/settings, prompt, tools, task data and time budget. Record any unavoidable differences.
3. Run baseline **without** skill and candidate **with** skill independently where the coding agent is available; retain full output or reproducible artifacts. Do not synthesize results to pretend a model ran.
4. Score each run against named weighted criteria; provide specific evidence for passed criteria. Include correctness, safety, scope adherence, command/test evidence, cost/latency when available and unnecessary skill triggering.
5. Record ratings in the `evals/runs/*.json` schema described in `evals/README.md`; use `python scripts/evaluate_skills.py --baseline ... --candidate ...` to calculate comparison.
6. Inspect actual failures and variance over more than one case; note subjective scoring and the difference between a benchmark and production validation.
7. Refine the skill's trigger/workflow and rerun the same held-out checks; do not optimize solely for a tiny public test set.

Output: experiment setup, model/tool versions, baseline and candidate evidence, weighted scores, per-case deltas, untested risks and go/no-go recommendation. The provided demo fixture is *synthetic* and must never be cited as an actual LLM benchmark.

## Execution dependency

The scorer `scripts/evaluate_skills.py` and fixtures `evals/` are distributed in the **source repository** rather than copied by the skill installer. Clone and inspect the public repository first or implement the scoring protocol with tools already available. The `--require-real` option now verifies saved raw-output digests and independent session identifiers, but does not independently authenticate the executing model.

## v0.4 real-run fixtures and 29-case coverage

`evals/29-skill-benchmark.json` supplies a designed-but-**not-run** criterion set for every skill. `scripts/prepare_benchmark.py` emits reproducible baseline or skill-instructed prompts without executing a model. Two additional real, read-only Codex A/B pairs are recorded in `evals/runs/v04-*.txt` with manually scored rubrics under `evals/benchmarks/`. These are **in-context skill instruction** tests, not native host auto-trigger tests; use multiple replications and blind graders before asserting general benefit.

## Your task

[Replace with your actual request and non-sensitive code/context.]

## Response

Provide actionable deliverables, evidence/assumptions, checks NOT EXECUTED and risks.
