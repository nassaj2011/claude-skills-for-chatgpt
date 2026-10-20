# ChatGPT Web: devops-ci-cd

Original: https://github.com/nassaj2011/claude-skills-for-chatgpt

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

## Specialist workflow

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

## CI demonstration

The repository's `.github/workflows/validate.yml` runs source manifest scans, checksum verification, 29-case benchmark validation, Python domain regression, dependency-free RTL UI tests and historical A/B raw-output digest checks. This pipeline validates the **skill kit and examples**, not any user's application or deployment. For production CI/CD, add environment-specific migration/rollback approvals.

## Your task

[Replace with your actual request and non-sensitive code/context.]

## Response

Provide actionable deliverables, evidence/assumptions, checks NOT EXECUTED and risks.
