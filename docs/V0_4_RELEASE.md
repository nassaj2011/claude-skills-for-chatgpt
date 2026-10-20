# v0.4.0 — Executable reference slices and evidence-led skill evaluations

This release prioritizes **quality validation, not the number of skills**. The catalog remains at **29**.

## New executable reference slices (independent of production systems)

| Example | Skills illustrated | Evidence | Limitations |
| --- | --- | --- | --- |
| `examples/reference-platform/` | database transaction integrity, authorization boundaries, backend service, QA | 9 passing Python standard-library tests on Windows | SQLite-only, no real API authentication or payment signature validation |
| `examples/frontend-rtl/` | UI visual direction, design tokens, state, RTL, accessibility patterns | 5 passing Node tests and module syntax check | Vanilla JS, not React/Next.js or actual browser/a11y audit |
| `examples/observability-gate/` | monitoring and release gates, safe structured data, latency/availability | 6 passing Python tests and synthetic sample gate | No production telemetry, no real load testing |

The samples are fictional and contain no user private data, passwords or real payment transactions.

## All-skill benchmark design

`evals/29-skill-benchmark.json` includes **one distinct scenario for each of 29 skills**, with a user task, expected output, at least three weighted acceptance criteria, a negative activation case and explicit `NOT_RUN` state.

```bash
python scripts/validate_benchmark.py
python scripts/prepare_benchmark.py --case s04 --mode baseline --output baseline-new.txt
python scripts/prepare_benchmark.py --case s04 --mode candidate --output candidate-new.txt
```

The preparer **does not execute a model**. It creates files with exclusive-new semantics and is designed to make prompts reproducible. The candidate explicitly prepends local SKILL.md content; this tests **in-context instructions**, not native skill triggering.

## Real-model A/B experiment: two additional cases

Four independent read-only runs of Codex CLI 0.147.0 using `gpt-5.6-terra` were executed on two fictional examples, without tools, file edits or network. The exact prompts and raw response files are in `evals/prompts/` and `evals/runs/`. `evals/benchmarks/` contains the criteria and human-scored evidence records.

| Scenario | No skill | With skill text | Recorded weighted difference |
| --- | ---: | ---: | ---: |
| SQLite double booking and replay | 9/13 = 69.2% | 13/13 = 100% | +30.8 percentage points |
| Booking ownership and manager scope | 9/13 = 69.2% | 13/13 = 100% | +30.8 percentage points |

**Interpretation:** Both baseline responses identified the critical vulnerabilities correctly. The skill-instructed responses additionally addressed before/after-commit recovery, safe database migration, a permissions matrix and explicit unreviewed surfaces. The rubrics intentionally reward those professional deliverables.

**Limitations:** Only **one run per mode per scenario**, no blind graders, no independent validation of all assertions, no actual application patch generated/benchmarked by these four runs and no tested auto-activation behavior. The scoring is exploratory and **does not establish a 30.8% general model improvement**. Outcomes are not an excuse to raise all 29 subjective expert ratings to 8.5/10 without further evidence.

## Quality gates

```bash
python scripts/validate_skills.py
python scripts/audit_skills.py --root skills --fail-on review
python scripts/provenance.py
python scripts/validate_benchmark.py
python -m unittest discover -s tests -v
python -m unittest discover -s examples/reference-platform/tests -v
python -m unittest discover -s examples/observability-gate -p "test_*.py" -v
node --test examples/frontend-rtl/ui.test.mjs
```

A separate CI job checks recorded raw-output digests for each A/B pair. This validates **integrity of archived output**, not future prediction or authenticity of model authorship.

## Deferred next steps

- Repeat A/B for the remaining 27 skills, with multiple runs, real but non-sensitive code changes, controlled tool access, diverse models and independent scoring.
- Extend React/Next.js reference artifacts with actual React runtime tests and Playwright local browser execution.
- Add permission-safe MCP and provider API contract integration fixtures.
- Apply observability and backup drills to isolated deployed staging environments with explicit approval. Nothing in this release is certified for production.
