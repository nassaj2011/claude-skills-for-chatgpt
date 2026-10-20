# v0.3.0 — Trust, install safety and evidence hardening

## Implemented improvements

1. **Fail-closed installer on unknown content.** HIGH static indicators block unconditionally; REVIEW indicators block `--apply` until explicit `--accept-review` after manual inspection. Existing installed skills are never overwritten, and symlink/junction destination paths are rejected. Each new skill is staged, re-audited and promoted with a same-folder rename. Failed staging is reported, not secretly deleted.
2. **Traceable publisher provenance.** `CATALOG.json` records the 29 original SKILL.md SHA-256 hashes, source GitHub URL, release version and no-tracking indicators; `scripts/provenance.py` verifies current source files. Hashes are not equivalent to signed publisher identity.
3. **Optional local installation receipt.** `--receipt <new-path>` writes an opt-in on-device JSON log. Neither installation nor verification transmits source code or user IDs to the publisher.
4. **Stronger PR report.** The read-only GitHub helper paginates general/inline review comments, checks review-thread resolution via GraphQL where authorized, and treats neutral/skipped/unknown CI checks as incomplete. `evidence_ready` is a narrow indicator, not automatic merge authorization.
5. **Grounded A/B claims.** `evaluate_skills.py --require-real` now validates a distinct recorded session for each run and verifies SHA-256 of saved raw output files within the repository. Scores still reflect supplied judgments and cannot prove causal improvement.
6. **Adversarial regression suite.** Tests cover suspicious/unsafe skill content, no-overwrite, staged install, provenance tampering, unknown CI and unresolved review threads, and evaluation output tampering.
7. **Privacy policy** clearly prohibits covert tracking, future code access and sending users' code. No such feature has been added.

## Run quality gates

```bash
python scripts/validate_skills.py
python scripts/audit_skills.py --root skills --fail-on review
python scripts/provenance.py
python -m unittest discover -s tests -v
python scripts/evaluate_skills.py --cases evals/pilot_cases.json --baseline evals/runs/pilot-pr-baseline.json --candidate evals/runs/pilot-pr-candidate.json --require-real
```

The last command verifies integrity of recorded historical output, not a fresh model run.

## Known limitations / deferred work

- A heuristic scanner does not prove a downloaded Agent Skill is benign, especially obfuscated instructions and external dependencies.
- A same-parent rename is not a complete multi-skill transaction and may not be safe against a hostile local actor racing filesystem operations.
- A SHA-256 catalog cannot authenticate the publisher on its own. Signed release verification and GitHub organization policies are separate steps.
- PR reporting requires authenticated GitHub CLI, does not inspect diff semantics and may lack review-thread API permission; unknown values are disclosed.
- Real-world A/B efficacy remains unproven across all 29 skills; one historical small pilot showed no improvement.
- No production load test, database recovery drill or full browser UI run is claimed.
- Users' existing manually installed skills are **not silently overwritten** by upgrading this repository.

See [provenance and privacy](PROVENANCE_AND_PRIVACY.md) and [security policy](SECURITY.md).
