# v0.10.0 — Multi-file skill integration pilot and 29-skill coverage audit

## Answer to the site-wide quality question

**NO: all 29 published skills have NOT passed functional or real-world end-to-end tests.** All 29 canonical SKILL.md records and mirrored ChatGPT Web Kit have passed the repository's structural/provenance checks. That does not establish quality, reproducible performance lift, native agent routing or integration success for all 29.

An explicit skill-by-skill record is in `skill_coverage_29.json`. It distinguishes historical in-context evaluations, earlier 3-arm pure-function trials, this three-project pilot and unmeasured web/native runtime behavior. No skill is labeled fully production-certified.

## Experiment design

Three independent *synthetic multi-file Python modules*:

1. **BOOK** (booking/data.py, booking/service.py, booking/queries.py): atomic reservation, payment replay/idempotency, receipt uniqueness, transactional outbox and tenant-safe reads.
2. **AUTH** (portal/store.py, portal/policy.py, portal/handlers.py): tenant/role-object authorization, no cross-tenant read/delete/export, audit integrity.
3. **QUEUE** (notifier/store.py, notifier/worker.py, notifier/metrics.py): lease claim concurrency, retry/dead letter, provider receipt replay and observable counts.

Three arms per task: baseline task, generic domain-neutral active control, and full corresponding specialist SKILL.md, with generic and candidate matched for **o200k_base proxy tokens** (BOOK 1251; AUTH 937; QUEUE 1102). This is not attested model-internal tokenizer matching or equivalent instruction quality.

## Failed native Code Mode attempt — evidence retained

Nine `codex exec --sandbox workspace-write` sessions returned normal CLI exit codes but reported **`codex-code-mode-host.exe` missing**. They inspected/changed no files. They were incorrectly marked as COMPLETED based on process exit status in the first runner; the archived text shows blockage. Their initial grader `integration_scores.json` is **NOT VALID model performance evidence**; do not treat it as nine code-edit successes. Original blocked responses and journal are preserved under `runs/` and `run_journal.jsonl`.

## Completed fallback: real multi-file code generation and external application

The model was supplied every source file directly in a read-only prompt and had to return **full replacement content for two coordinated modules** inside a strict JSON `files` mapping. All nine model calls completed. An independent script validated exact allowlisted paths, copied fresh templates to isolated folders, applied the replacement files, and ran the *same* developer-authored hidden regressions outside the model prompt.

**What this measures:** the model's ability to propose coherent working **multi-file** modifications under a fully supplied source context. It does **not** measure tool-driven file browsing, Codex's actual edit operations, native Skill auto-selection, or real production repositories.

### Real regression results (one trial per arm and project)

| Scenario | Baseline | Generic matched control | Specialist skill |
|---|---:|---:|---:|
| Booking/payment | 18/18 | 18/18 | 18/18 |
| Authorization/privacy | 21/21 | 21/21 | 21/21 |
| Notification worker | 21/21 | 20/21 | 21/21 |
| **Total** | **60/60** | **59/60** | **60/60** |

The generic QUEUE response mishandled an unclaimed-job acknowledgement by raising PermissionError instead of the required ValueError. Other test cases passed. Tests include synthetic concurrency, tenant-scope denial, idempotency, outbox, work leases and receipt uniqueness.

**No proof of general specialist uplift.** The baseline scored a perfect 60/60; candidate exceeded generic by only one assertion. The rubric is still ceiling-prone, there were only three tasks and one call per arm, and the grader's design and fault assumptions were not independently audited.

## Verifying claims without running model-written code

```powershell
python -m unittest discover -s tests -p test_v10.py -v
python scripts/build_web_kit.py
python scripts/validate_skills.py
```

The above only validates archived response checksums, 29-skill coverage metadata and persisted grading evidence. It does **not** execute untrusted generated functions. The local-only `scripts/v10_apply_grade.py` executed generated Python against fictional regression fixtures with an AST heuristic and `python -I -S` subprocess; **not a hardened OS sandbox**. Use a disposable VM or equivalent isolated environment if repeating with untrusted code. Do not run these tests on actual customer data.

## Coverage gaps

- 26 of 29 skills had **no v0.10 multi-file exercise**.
- No full end-to-end on all 29 skills, no long-run repeats for v0.10, no actual browser Projects upload/routing test, and no native Codex tool host available.
- Static security lint, unit tests of example tools and archived textual A/B sessions are useful supporting evidence, not a site-wide 'passed' certificate.
- Next useful experiment: repair/enable the legitimate Codex host (not circumvent environment controls), choose more difficult multi-module change requests with independent externally checked oracles, and repeat matched trials. Consider a cross-provider model replication (Gemini, Claude) but do not share the scoring key with judges.
