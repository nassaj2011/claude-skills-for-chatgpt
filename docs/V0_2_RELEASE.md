# v0.2.0 — Seven risk-focused Agent Skills and executable safety tools

## New skills (22 → 29)

| New skill | Solves | Tooling |
| --- | --- | --- |
| code-review-pr | Reviews PR/CI/reviewer evidence, no implicit merge | `scripts/pr_review_report.py` |
| skill-evaluation-benchmark | Measures skill behavior instead of just formatting | `scripts/evaluate_skills.py`, `evals/cases.json` |
| agent-skill-security-auditor | Flags obvious unsafe skills prior to installation | `scripts/audit_skills.py` |
| backup-disaster-recovery | Backup integrity and isolated recovery drills | `scripts/backup_manifest.py` |
| dependency-supply-chain-auditor | Vulnerability, license, provenance and lockfile review | Host's audited package tooling |
| load-resilience-testing | Bounded, authorized reliability/load scenarios | Host's approved load tooling |
| project-bootstrap-environments | Reproducible, safe repository and environment setup | Host's own runtimes and CI |

## Runtime tooling examples

```bash
# Read-only skill audit (heuristic: clean is not guaranteed safe)
python scripts/audit_skills.py --root skills --json

# Preview installation. No writes until --apply, no existing skill overwritten.
python scripts/install.py --target ~/.agents/skills
python scripts/install.py --target ~/.agents/skills --apply

# A/B evaluator self-test with SYNTHETIC illustrative data
python scripts/evaluate_skills.py --cases evals/fixtures/demo_cases.json --baseline evals/fixtures/demo_baseline.json --candidate evals/fixtures/demo_candidate.json

# Read-only PR status and review comment summary; requires authenticated gh
python scripts/pr_review_report.py --repo YOUR/REPO --pr 123 --json

# Checksum-based backup verification only (NOT a restore test)
python scripts/backup_manifest.py --root /path/to/isolated/backup --write /outside-folder/manifest.json
python scripts/backup_manifest.py --root /path/to/isolated/backup --verify /outside-folder/manifest.json
```

## Quality gates and limitations

- All skill manifests must pass structure checks. The static security scan blocks the installer's high-severity matches; review all downloaded third-party material manually.
- The seven-case evaluation rubric **does not imply that seven real A/B model runs were executed**. Fixtures are explicitly synthetic and rejected by `--require-real`.
- Tests cover the Python helper tools; they do **not** certify production releases, security of untrusted skills, database recovery or load capacity.
- The Playwright example is a template: it requires an installed Playwright package and an explicitly authorized local server. It is not presented as an executed browser test.
- CI checks source consistency; a green workflow is **not** a platform deployment authorization.
- Public contribution policy: do not publish secrets, proprietary project artifacts or personal information.

## Changes compared to v0.1

New read-only security scanning, install preflight, human-scored comparison harness, PR evidence CLI, file-backup manifest verifier, seven rubric cases, illustrative fixtures, expanded standard-library unit tests and updated CI/docs.

Attribution and license details are in [ANTHROPIC_COMPARISON.md](ANTHROPIC_COMPARISON.md) and [LICENSE](../LICENSE).

## First actual-agent pilot

One read-only `gpt-5.6-terra` Codex A/B run was completed on a fictional PR-review decision. Both responses satisfied all scored criteria (100%/100%; no measured gain). The added skill text was prepended to the second prompt; this did **not** test host-native skill auto-selection. Read the [pilot record](../evals/PILOT_RESULT.md) before interpreting it. The remaining six newly added skills and full seven-case rubric have **not yet been benchmarked with actual model runs**.
