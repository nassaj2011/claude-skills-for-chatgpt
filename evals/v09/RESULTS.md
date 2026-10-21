# v0.9 — Harder, token-matched repeated pilot

**Executed 21 Oct 2026.** This is an evaluation-method revision, NOT a change to the 29 source skills. Scope: three new, fictional pure-function coding scenarios × three prompt arms × two independent Codex runs = 18 completed model responses. Every model-written function was checked against the same contract fixture.

## Design

- Tasks: `P01` validate/replay-safe booking payment finalization (23 tests), `P02` enforce tenant/role/confirmation/idempotency boundaries on untrusted LLM tool calls (25 tests), `P03` validate nested transitive package provenance with explicit failure reasons (27 tests).
- Conditions: (1) baseline task only, (2) task + generic domain-neutral instructions, (3) task + full matching `SKILL.md` instructions. For each scenario, generic and specialist **total prompt counts** were matched at 790, 1067 and 931 tokens respectively, measured by **tiktoken o200k_base**. This is a **proxy**: it does NOT establish exact matching under the model's internal tokenization or equivalent information content.
- Same model `gpt-5.6-terra`, CLI 0.147.0, `--ephemeral --ignore-user-config --skip-git-repo-check -s read-only` in an independent local non-Git folder. Two read-only jobs at most concurrently, deterministic job-order randomization. Each response saved as-is under `evals/v09/runs/`; SHA-256, proxy token count, time, optional session identifier, failures in `run_journal.jsonl`.
- 18 model calls completed with zero failed calls. No production repository, account, database or third-party API was accessed by model sessions.

## Tested source-code correctness

| Case | Baseline / 2 runs | Generic / 2 runs | Specialist / 2 runs |
|---|---:|---:|---:|
| P01 — payment finalization | 46 / 46 | 46 / 46 | 46 / 46 |
| P02 — LLM tool authorization | 50 / 50 | 50 / 50 | 50 / 50 |
| P03 — dependency provenance | 52 / 54 | 53 / 54 | 53 / 54 |
| **Total** | **148 / 150 (98.7%)** | **149 / 150 (99.3%)** | **149 / 150 (99.3%)** |

The 75 specified cases are replayed against 6 model responses per task (450 binary fixture checks in total). An AST screening tool and temporary `python -I -S` subprocess evaluated pure functions with a five-second timeout. **These are NOT hardened OS sandbox or comprehensive security proofs.**

To avoid unfairly rejecting ordinary safe Python, the grader was adjusted for locally defined helper functions and the basic `set.add` method. This allowance applied identically to all three conditions. The input/output test oracle was saved before the scoring run. This is a developer-maintained grader, not an independent audit.

## Interpretation

The specialist instructions again **do not beat the token-balanced generic control** on these scenarios. On P03 one of two generic outputs and one of two specialist outputs failed one test each, whereas each baseline failed one. The aggregate improvement over baseline is **one assertion out of 150** in each instructed arm, not evidence of causal or statistically significant skill-specific lift.

Results are extremely close to the ceiling, even after harder tasks, so broad rubric scores or a claim of an overall quality >=8.5/10 would be unjustified. More useful next evaluations must require multi-file changes, realistic fixtures, partial information, authorization decisions and independent side-effect-safe integration tests. Exact 0–10 skill quality should be treated as **unproven**.

## Reproduce without more model calls

```powershell
python -m unittest discover -s tests -p test_v09.py -v
python scripts/v09_grade.py --output evals/v09/another_nonexisting_score_file.json
```

The second command actually executes archived model-written code under AST filtering, so use a safe disposable environment. Standard CI should only run the first, **read-only checksum and result validator**.

## Boundaries

- No prompts or raw result of the other 26 skills were executed in this v0.9 pilot.
- No native skill autoload, browser ChatGPT Projects routing, actual GitHub pipeline deployment, MCP server or external provider integration was tested.
- External package `tiktoken` was placed under a dedicated local isolated folder on the user's computer; it is not required by the standard offline CI tests, ChatGPT Web users or the 29 canonical skills.
- Model token counts are proxy counts, and control quality is not necessarily matched even when token counts are equal.
