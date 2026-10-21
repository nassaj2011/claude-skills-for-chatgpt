# v0.8.0 — Three-arm held-out pilot, actual model code testing

## Scope and experimental integrity

- **29 skills × 3 newly authored fictional prompts = 87 scenarios.**
- Bank: `evals/v08/heldout_87.json`. Only the **three code-writing cases** H04-1 (transactional booking decision), H14-1 (untrusted LLM response normalization) and H27-1 (dependency metadata policy) were executed. **The other 84 cases remain NOT RUN.**
- Three arms: baseline without supplementary instructions, a domain-neutral generic control of **exactly the same character length** as the specialist instructions, and the actual `SKILL.md` text. Matching characters is **not** the same as matching tokens or instruction information content; the generic control can have unnatural truncation and is an imperfect comparator.
- Randomized case/arm order used seed `v08-predeclared-01`. Nine independent Codex CLI `gpt-5.6-terra` read-only calls were completed against an isolated folder, not a production project.
- Initial **nine attempts failed before contacting the model** with a trusted-directory check. Adding `--skip-git-repo-check` for the dedicated isolated folder resolved the issue. These failures were preserved in `pilot_journal.jsonl`, not counted as model responses. **No output was overwritten.**
- Outputs with per-run input/output digests, timestamps, model name and status are archived in `evals/v08/runs/`; `scripts/verify_v08_pilot.py` checks all nine digests.
- No authenticating session IDs or native agent auto-routing were independently certified.

## Actual code-fixture results

| Fictional code problem | Baseline | Generic active control | Specialist skill |
|---|---:|---:|---:|
| H04-1 — transactional reservation function | 10/10 | 10/10 | 10/10 |
| H14-1 — untrusted LLM payload normalizer | 8/11 | 11/11 | 11/11 |
| H27-1 — dependency manifest triage | 11/11 | 11/11 | 11/11 |
| **Total** | **29/32** | **32/32** | **32/32** |

`scripts/score_code_v08.py` inspected AST and ran small deterministic synthetic Python fixtures in a temporary isolated Python subprocess with an execution timeout. **This is NOT a hardened security sandbox** and does NOT establish complete functional correctness or safety. Only generated pure-function text was run; no network, payment, customer data or deployment.

### Scorer correction

The first scorer mistakenly rejected safe `type`, `append`, and `join` constructs. The original `pilot_scores.json` was preserved as an obsolete intermediate result; the same nine model outputs were rescored with a minimal expanded allowlist, producing authoritative `pilot_scores_v2.json`. No model run was repeated for this correction. The scorer itself was created for this pilot and was not independently audited.

## What we learned

**No measured specialist-specific advantage over the length-matched generic control in these three simple code problems.** Generic and specialist arms each passed all 32 checks. Both exceeded the baseline (29/32), but with three cases and one trial per arm, we cannot attribute this difference causally.

All three cases exhibited a ceiling effect (especially booking and dependency checks), so later evaluation should use harder tasks with different failure conditions, behavioral mutation tests, multi-module coding and an independent security/review grader. Improve the generic control to match model token counts and avoid cut-off sentences; keep prompt generation/version frozen before the next run.

## Completion status

- 87 scenario bank: DESIGNED
- 9 text-only Codex generations: COMPLETED
- 9 synthetic code-fixture tests: EXECUTED
- 84 scenario runs: NOT RUN
- Blind Gemini and Claude scoring for this batch: NOT RUN
- General 8.5/10 quality claim: NOT ESTABLISHED
- Native ChatGPT Web project invocation: NOT TESTED

This release strengthens the **evaluation method**, not the skill descriptions or actual ChatGPT/Codex installation paths.
