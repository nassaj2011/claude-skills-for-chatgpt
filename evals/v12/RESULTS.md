# v0.12 — Expanded 34-case multi-file regressions (post-hoc) and host diagnostics

## Site-wide test status

**All 29 canonical skills passed structural/provenance validation. NOT all 29 passed functional skill-effectiveness tests.** Current public skill bundle and ChatGPT Web Kit remain on the same canonical source texts. No new skill quality certification is made here.

## Codex native file-edit blocker — confirmed experimentally

Environment: Windows, Codex CLI `0.147.0` at the existing `%LOCALAPPDATA%\Programs\OpenAI\Codex\bin\codex.exe`. Its sibling `codex-code-mode-host.exe` was missing. The originally available host file in a separate local OpenAI-managed plugin directory had a valid OpenAI Authenticode signature, but it proved *version-incompatible* with this CLI: IPC decoding rejected unexpected `code_mode_host_duration_ns`. Disabling the host via feature flag also failed closed, as expected.

An **isolated test-only copy** of the CLI was made under `H:\Projects\_CodexHostProbeV11\bin`, *not replacing the installed app*. The official host asset from the matching `openai/codex` GitHub release `rust-v0.147.0` was downloaded alongside it and its Windows Authenticode status was `Valid`. Local observed file size: `57,450,288` bytes; SHA-256: `37c23a542037e1bcfd0fa7eb4a150c697229d7ff31bf675c519d5bff7226b191`.

**Result:** The matched official host permitted a real sandboxed PowerShell **read** of a disposable local `a.txt` file. A requested write of another test file still failed with an explicit `read-only sandbox; rejected by user approval settings` error. Passing `-s workspace-write` did not change that effective read-only policy. **No native code write was achieved**, and sandbox/approval restrictions were not bypassed. No user production directories or installation binaries were modified.

Related official upstream issue: [openai/codex#38975](https://github.com/openai/codex/issues/38975) describes the exact Windows WinGet `0.147.0` missing-host package; [openai/codex#40817](https://github.com/openai/codex/issues/40817) documents Windows host deployment regressions. These issues are background information, not proof of a remedy for this machine.

## New diagnostic tests of previously archived nine multi-file model outputs

To avoid more model calls, the original nine valid `v0.10` JSON full-file replacement outputs were reused **without changes**. Each was already applied in separate, fictional Python project copies; the same original v0.10 test results were 60/60 baseline, 59/60 generic, 60/60 specialist.

A new supplementary suite `evals/v12/additional_cases.py`, **written after the model outputs**, tested 34 additional acceptance/failure behaviors on each arm:

| Project | New cases per arm | Baseline | Generic | Specialist |
| --- | ---: | ---: | ---: | ---: |
| Booking/payment and concurrency | 11 | 11/11 | 11/11 | 11/11 |
| Object authorization/tenant safety | 12 | 12/12 | 12/12 | 12/12 |
| Notification claim/lease/replay | 11 | 11/11 | 11/11 | 11/11 |
| **Total new post-hoc** | **34** | **34/34** | **34/34** | **34/34** |

There were **102 additional successful synthetic assertions** (3 arms × 34 cases). Combined descriptively with the previous 60-case suite, the outcomes are 94/94 baseline, 93/94 generic, 94/94 specialist. **This is not a new randomized experiment or evidence of an overall specialist effect.** The extra cases were written after answers existed and are not independently blinded.

### Grader-error audit

The first test run was invalid because of a missing closing parenthesis in the authored `additional_cases.py`; all nine rows showed `PARSE_ERROR` and 0 executed tests. This record is preserved as `posthoc_scores.json` (not a skill failure). The syntax error was corrected, and the authoritative re-run (without model calls) is `posthoc_scores_v2.json`. The generated model source itself was not changed between those scorer attempts.

### Reproduce

Read-only evidence verifier in CI:

```bash
python -m unittest discover -s tests -p test_v12.py -v
```

Rebuild the v0.10 archived synthetic workspaces using the SHA-256 manifest, then score them in a **disposable** Python environment:

```bash
python scripts/v12_prepare_workspaces.py   # reconstruct from archived hashes, no generated code execution
python scripts/v12_score.py --output evals/v12/posthoc_scores_rerun.json   # executes synthetic model code
```

The latter must be run only with a **new result path** because it refuses overwriting the archive, and it executes previously generated Python under an AST-limited subprocess. That is NOT a hardened OS sandbox. Do not repeat against private systems.

## Interpretation and next investment

More single-shot prompts plus unblinded tests on small fictional code can keep producing ceiling effects. The next defensible investment is **expanding beyond the same three skill types**, choosing tasks with meaningful ambiguity, cross-module failures, integration/tool limitations, and true repeated paired trials with independently held-out scoring. Neither native Codex file modification nor ChatGPT Web Project skill selection has yet been measured end-to-end. No 8.5/10 average quality claim is supported.
