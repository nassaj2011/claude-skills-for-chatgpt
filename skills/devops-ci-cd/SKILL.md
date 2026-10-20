---
name: devops-ci-cd
description: Design reliable CI/CD, infrastructure configuration, staging/prod separation, deployment and rollback workflows for authorized repositories.
---

# DevOps and delivery pipeline
1. Read actual deployment topology, CI workflows, runtime, database migration approach, environments, branch protections and secrets storage.
2. Specify a staged pipeline: lint/typecheck, unit, contract/integration, security checks where useful, build, deploy, smoke and monitor.
3. Use least-privilege CI tokens, dependency pinning where practical, no secrets in logs and controlled artifact provenance.
4. Define reproducible environment configuration and promotion; keep staging vs production boundaries explicit.
5. Make DB migrations backward-compatible; include backups, feature flags/canary and rollback for consequential releases.
6. Validate pipeline safely before enabling production actions; do not replace active CI or deploy without approval.
7. Record run link, SHA, environment, actual checks and failure response. Avoid saying the pipeline passed if not executed.

Output: current-state topology, proposed workflow, environment matrix, approvals, rollback criteria and verified tests.
Deployment is a distinct authorized action, not implied by writing a workflow file.
