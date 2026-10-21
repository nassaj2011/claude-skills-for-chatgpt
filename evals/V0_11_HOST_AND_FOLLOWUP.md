# v0.11 — Host diagnosis and post-hoc adversarial regressions

## Codex host diagnosis (read only)
Connected desktop: native Windows `C:\Users\Almas\AppData\Local\Programs\OpenAI\Codex\bin\codex.exe`, CLI version 0.147.0 (installed binary last modified August 9 2026). Installation directory contains **only codex.exe**. `codex-code-mode-host.exe` was not found by the system lookup or recursive installation-directory search. Nine former workspace-write model attempts (v0.10) reported the missing host and made **no file edits**. Their process exit code was misleading; they do **not** count as successful real tool-edit executions.

No installation/upgrade, unsigned host substitution, unsafe sandbox bypass, environmental security-policy change or production change was performed. Resolve using an official verified Codex distribution or support channel and retest on a disposable project after user approval. The read-only, host-independent JSON file replacement path remains a measurement of **text-generated multi-file code correctness**, not native agent file operations.

## New, explicitly post-hoc exploratory checks

After inspecting v0.10 outputs, twelve additional synthetic regression methods were run for all nine archived multi-file model outputs (3 projects x 3 prompt arms). These include booking confirmation replay and input validity; tenant authorization and nested defensive copies; queue lease boundary, provider verification and copy isolation. Source: `evals/v11_adversarial_regression.py`. Runner: `scripts/v11_regrade.py`. Archived result: `evals/v11_followup_scores.json`.

| Area | Baseline | Generic active control | Specialist |
| --- | ---: | ---: | ---: |
| Booking/payment | 4/4 | 4/4 | 4/4 |
| Authorization | 4/4 | 4/4 | 4/4 |
| Queue/worker | 4/4 | 4/4 | 4/4 |
| **Total** | **12/12** | **12/12** | **12/12** |

**108 successful individual test invocations** (12 test methods x 9 outputs). These checks were written after observing prior results, are not blinded and were not preregistered. They cannot establish general skill uplift or 29-skill functional certification. They add checks, but are still ceiling-limited.

## What has, and has not, passed

- 29/29 SKILL.md structural validation: PASS on previous release; source skills unchanged.
- Nine archived multi-file model outputs: all passed this post-hoc check, without specialist-specific gain.
- Native Codex integration and tool-driven editing: NOT RUN due to missing host.
- Real ChatGPT Web skills use, cross-client skill recognition and effect: NOT MEASURED.
- Entire 29-skill professional quality >=8.5/10: NOT PROVEN.
- 26 skills with no multi-file experiment remain untested for that methodology.

## Next meaningful gates

1. Restore officially supported Codex tool-host installation only with approved installation instructions; do not infer that turning on unsafe filesystem permissions will fix missing binaries.
2. Design more demanding real-world-like **independent hidden acceptance contracts** for skills not yet exercised, ideally external or reviewer-written and versioned before model calls.
3. Test identical problems under three arms with several independent trials; constrain compute costs and record code quality and independent correctness separately.
4. Run at least one ChatGPT Web manual invocation to test its actual user-facing workflow rather than extrapolating Codex behavior.
