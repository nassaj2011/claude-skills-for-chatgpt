---
name: devops-ci-cd
description: Review, design and safely validate CI/CD pipelines, reproducible builds, release approvals, migrations, least-privilege secrets and rollback evidence across environments.
---

# DevOps and CI/CD — fail-closed release engineering

## Activation
Use when workflows/build/deployment config, migration rollout, releases, GitHub Actions, artifacts, environment drift or rollback are in scope. Do not refactor unrelated application logic or change active production infrastructure without specific authorization.

## Evidence-first pipeline
1. Discover exact repo, commit SHA, runtime, branch protections, deploy topology, available runner permissions, job environment, external registries, backups and owner-approved window. A generic YAML example is not evidence of the user's current setup.
2. Define immutable pipeline phases: checkout pinned source -> lint/type/unit -> contract/integration/security -> build artifact -> staging deploy -> smoke and invariant checks -> manual production authorization -> progressive rollout -> monitoring and rollback.
3. **Reduce capabilities:** default read-only token; grant write permissions only to a named scoped job. Pin third-party actions to trusted immutable commits where feasible, manage secret scopes and protected environments, avoid untrusted PR artifacts/scripts, masking-only strategies or inherited secrets on fork PRs.
4. Track artifact digests, lockfiles, SLSA-style provenance considerations and runtime compatibility. Record exact SHA, binary digest, versioned config and environment for each job.
5. For DB schema changes, plan expand/backfill/contract, mixed-version compatibility, backup verification, long-running locks and rollback. Do not assume downgrades are data-safe after schema contraction.
6. Simulate failure branches: lint fail, security scan unavailable, migration preflight fail, smoke fail, skipped required auth check, canceled deploy, unhealthy canary and missing backup restore evidence. Treat unknown/skipped as NOT RUN, not PASS.
7. Define a reversible staging rollout, clear owners/approval, alert thresholds and objective abort decision. Never merge/deploy by default merely because a request asks for pipeline design.
8. Compare proposed changes against observed CI runs; state which jobs were actually executed, pass/fail, and residual manual gates.

## Expected output
- Current-state topology + proposed workflow diff
- Permissions table: job | token rights | secrets | environment | trigger | approval
- Migration/rollback decision and canary failure matrix
- Evidence register: SHA, command/job, environment, timestamp, result, not-run status
- Explicit GO/NO-GO recommendation, approval owner and unresolved risks

## Local and Web mode
`examples/release-policy/` demonstrates an **offline policy evaluator**, not a deployer; it prevents skipped auth, unsafe migration and missing restore evidence from becoming GO. In ChatGPT Web, output a complete proposed workflow and user-run verification commands while marking jobs NOT RUN.

## Safety
Never modify CI secrets, external environments, deployment triggers, protected branches or delete resources without explicit approval. Repo-local passing unit tests do not prove real production deployment readiness.
