# ChatGPT Web — 29 Specialist Workflows

Source: https://github.com/nassaj2011/claude-skills-for-chatgpt

This is a portable instruction library, NOT an installed/native skill.
Use the uploaded file in ChatGPT chat or Project; name the relevant skill.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

## Skill index

- agent-skill-security-auditor: Inspect Agent Skills for dangerous instructions, unexpected scripts, credential exfiltration, symlinks, scope escalation and third-party provenance before installation.
- backend-api-engineer: Build and review maintainable backend endpoints, service boundaries, validation, error contracts, pagination and integration reliability.
- backend-debugging: Investigate backend defects using reproducible evidence, traces, hypotheses, binary isolation and regression tests. Use for crashes, incorrect business logic, intermittent failures, or API incidents.
- backup-disaster-recovery: Plan, validate and exercise backups, restoration, integrity, recovery time objectives and recovery point objectives for production software and databases.
- code-review-pr: Review pull requests and code changes for correctness, security, API compatibility, missing tests and CI failures; inspect reviewer comments and GitHub checks before merge.
- database-transaction-integrity: Safeguard SQL schemas, transactions, migrations, concurrent updates, payments, event consistency and audit ledgers. Use for persistent-state changes.
- dependency-supply-chain-auditor: Review package dependencies, vulnerable versions, licenses, lockfiles, build provenance and CI security for web and backend repositories.
- devops-ci-cd: Design reliable CI/CD, infrastructure configuration, staging/prod separation, deployment and rollback workflows for authorized repositories.
- documentation-handover: Create maintainable project documentation, ADR indexes, operator runbooks, release notes and contributor onboarding matched to actual code.
- frontend-design-direction: Create deliberate, distinctive, accessible frontend visual direction and interface composition grounded in the product's users and brand.
- llm-api-integration: Design LLM-powered workflows using OpenAI, Anthropic or another provider with safe tool contracts, cost controls and offline evaluations.
- load-resilience-testing: Plan and conduct authorized, bounded load, soak, concurrency and fault-tolerance testing against isolated environments with measurable SLO criteria.
- mcp-integration-builder: Design or implement MCP servers and third-party integrations with explicit tool schemas, authentication, permissions, testability and safe retries.
- observability-monitoring: Plan product telemetry, health checks, logs, metrics, traces, SLOs and incident response for live platforms.
- performance-accessibility: Assess and improve web performance and accessibility with measurable budgets, controlled profiling, and user-centered prioritization.
- playwright-webapp-testing: Test authorized local or staging web apps with Playwright, browser logs, screenshots and reproducible frontend regressions.
- privacy-data-governance: Review personal-data flows, retention, consent, access controls and data minimization for software product features.
- product-business-analyst: Turn a product idea into evidence-based discovery, PRD, user journeys, scope, measurable acceptance criteria, and a prioritized MVP. Use for product definition or ambiguous features.
- project-bootstrap-environments: Bootstrap a reproducible software project with local, development, test, staging and production environment isolation, safe secrets, CI and onboarding.
- qa-release-gatekeeper: Judge software release readiness from executed tests, change scope, migrations, security checks, incident risks and verified rollback.
- qa-test-strategy: Create balanced automated test portfolios including unit, contract, integration, security, failure and performance checks. Use when planning test coverage or regression prevention.
- react-artifacts-builder: Build multi-component interactive web interfaces using a compatible React stack, routing, state and UI primitives where appropriate.
- security-authorization-auditor: Audit authentication, authorization, roles, object ownership, API defenses, secrets and abuse protections against the repository's actual implementation.
- skill-authoring-toolkit: Create and maintain reusable Agent Skills in SKILL.md format, with precise triggers, testable workflows, safe tool permissions and validation.
- skill-evaluation-benchmark: Evaluate whether an agent skill actually improves task outcomes using repeatable tasks, baseline-versus-skill runs, human-scored criteria and variance analysis.
- software-architect: Design or review software architecture, bounded contexts, dependencies, ADRs, failure modes and compatibility across services. Use for consequential system changes.
- technical-project-orchestrator: Coordinate multi-stage product delivery from agreed requirements to PRs and releases with critical paths, scoped Codex tasks and evidence-based status.
- theme-design-system: Define and evolve a cohesive web or mobile design system with accessible tokens, typography, color, component variants and usage rules.
- visual-assets-design: Plan visual assets for product websites and marketing materials with clear creative briefs, deliverable specifications and rights checks.

---

## 1. agent-skill-security-auditor

Inspect Agent Skills for dangerous instructions, unexpected scripts, credential exfiltration, symlinks, scope escalation and third-party provenance before installation.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Security audit for untrusted Agent Skills

A skill folder is executable guidance, not a sandbox: all third-party skills require source review before installing or running scripts.

1. Establish upstream repository, exact commit, license, maintainer and why the capability is needed; avoid installing unknown collections wholesale.
2. Inventory SKILL.md, scripts, embedded assets, nested references, symlinks and executable binaries. Note external URLs, shell commands, pip/npm install hooks and network calls.
3. Run `python scripts/audit_skills.py --root path/to/skills --json` to find **heuristic indicators** (unsafe shell pipelines, destructive actions, credential paths, instruction override, unexpected binaries/symlinks). Treat scanner results as leads, not a security guarantee.
4. Manually inspect suspicious code, transitive dependencies and whether apparent "do not run" examples are false positives. Never execute an untrusted audit target.
5. Compare declared scope and actual commands: filesystem reads, network destinations, GitHub permissions, browser automation, production mutation and secrets access.
6. Classify APPROVE / REVIEW / REJECT with documented provenance, findings, residual risk and owner permission. Any high-risk unresolved behavior blocks installation.
7. Prefer explicit user-scope, no-overwrite installation; pin revision and re-audit when upgrading.

Output: inventory, findings with file/line/reason, rights/provenance, tool permissions, mitigation and decision. A clean static scan **does not certify safety** or detect every prompt injection.

## Execution dependency

The static scanner is `scripts/audit_skills.py` in the **public source checkout**. Installing only this SKILL.md does not install the Python utility. Use a locally inspected copy of the repository or conduct manual source review when the helper is absent. Never fetch-and-execute an unknown scanner; absence of a scanner is not an approval to install untrusted skills.

---

## 2. backend-api-engineer

Build and review maintainable backend endpoints, service boundaries, validation, error contracts, pagination and integration reliability.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Backend API engineering

1. Inspect live code, framework conventions, API contracts, data model, auth middleware and current tests before implementing.
2. Specify the endpoint or event contract: actors, request/response schema, status/error codes, idempotency and pagination where needed.
3. Enforce validation, authorization and ownership on the server; do not trust client-provided role or scope values.
4. Place business rules in a testable domain/service layer; keep transport handlers thin and errors consistent.
5. Define timeouts, bounded retries and circuit-breaker behavior for external dependencies; avoid retrying non-idempotent operations blindly.
6. Coordinate transaction boundaries and invariants with database-transaction-integrity; consider version/rollback compatibility.
7. Add unit + integration + negative tests for normal and failure behavior. Verify observability without leaking credentials or personal data.
8. Document compatibility impacts and migration/flag requirements before release.

Output: contract, touched components, behavior changes, verification evidence, security/reliability risks.
Do not perform production writes or expose credentials while debugging.

## Reference service boundary

The `examples/reference-platform` project demonstrates transaction-safe application-domain logic for bookings and receipts. No HTTP API or real identity provider is bundled: design response contracts and server-side authentication separately, and verify route-to-service authorization through integration tests. A green domain test cannot establish API compliance.

---

## 3. backend-debugging

Investigate backend defects using reproducible evidence, traces, hypotheses, binary isolation and regression tests. Use for crashes, incorrect business logic, intermittent failures, or API incidents.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Evidence-driven backend debugging
1. Record the exact symptom, environment, versions, affected endpoints and last known good state; separate user report from verified behavior.
2. Find an independently reproducible minimal case using safe test data. Capture structured logs, correlation IDs, stack traces and relevant request IDs; redact secrets.
3. Draft competing hypotheses ordered by evidence and blast radius. Inspect recent diffs, transaction boundaries, config drift, queue timing and dependency failures.
4. Instrument narrowly; never replace evidence with guesses or massive logging of production personal data.
5. Isolate a root cause by a controlled test, diff, breakpoint, replay or focused probe. Distinguish root cause from triggering symptom.
6. Implement the smallest corrective patch, add a regression test that failed before and passes after, and inspect adjacent failure paths.
7. Verify rollback and monitor relapse signals. When evidence is missing, report the most efficient next experiment.

Output: symptom, reproduction, evidence, ruled-out hypotheses, cause confidence, patch, before/after test result and unresolved risks.
Do not claim the bug is fixed solely because a patch compiled.

---

## 4. backup-disaster-recovery

Plan, validate and exercise backups, restoration, integrity, recovery time objectives and recovery point objectives for production software and databases.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Backup and disaster recovery

Use for backup policies, release/migration protection, ransomware resilience or availability-critical incidents; do not conduct a live restore without authorization.

1. Inventory data stores, object storage, configuration, secrets (tracked without exposing values), infrastructure state and external dependencies; identify a responsible owner.
2. Agree on **RPO** (maximum tolerated data loss) and **RTO** (maximum recovery time), legal retention and critical customer journeys. Do not invent targets.
3. Define backup methods consistent with application/database guarantees: PITR/WAL or equivalent, logical vs physical snapshots, encryption, immutable/offsite copy, retention and rotation.
4. Verify consistency across dependent stores and replay behavior, including pending background jobs and payment/provider state.
5. Inspect non-sensitive manifest/checksum evidence; use `python scripts/backup_manifest.py --root <backup-folder> --write <new-manifest.json>` and `--verify <manifest.json>` on authorized file backup snapshots. This checks file integrity, **not** database restore correctness.
6. Design an isolated, non-production restore drill that measures elapsed recovery, data invariants, application health and audit completeness; never overwrite live data.
7. Record drill failures, missing backups, responsible follow-ups and a rollback/emergency communication runbook.

Output: RPO/RTO, protection map, restore runbook, actual drill evidence versus planned checks, consistency risks and status. Never call a backup proven until an authorized restore test has passed.

## Execution dependency

The optional checksum utility `scripts/backup_manifest.py` is provided in the source repository. A standalone installed SKILL.md has no bundled backup binary and does not create real database backups. Use only authorized local tooling and never claim RPO/RTO or restore readiness from a hash check.

---

## 5. code-review-pr

Review pull requests and code changes for correctness, security, API compatibility, missing tests and CI failures; inspect reviewer comments and GitHub checks before merge.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Evidence-based PR and code review

Use when an actual diff, PR, merge request, or requested code review exists; do not imply a PR exists because a branch exists.

1. Identify target repository, base/head, exact diff and user-approved scope; read applicable AGENTS.md/ADRs and functional acceptance criteria.
2. Inspect changed code and its callers for behavior regressions, missing server-side authorization, race conditions, schema/API compatibility, performance and observability impacts.
3. Where GitHub CLI is authorized, run the repo's read-only `scripts/pr_review_report.py --repo OWNER/REPO --pr N` and inspect reviews, inline and general comments, and CI check status. For other hosts use equivalent authenticated read-only tools.
4. Identify findings with **severity**, **path and line**, triggering scenario, impact and concrete correction; separate confirmed defects from hypotheses.
5. Verify that requested changes are within scope, relevant test coverage exists, and required CI gates have actually completed. Do not infer that all review threads are resolved from a mere list of comments.
6. Recommend a merge verdict: READY, NEEDS CHANGES, or INSUFFICIENT EVIDENCE. Do not merge, push, dismiss reviews, or resolve threads without authorization.
7. When asked to fix, implement narrow changes on an authorized branch and repeat targeted tests and review.

Handoff to database-transaction-integrity for concurrency/schema changes; security-authorization-auditor for privilege surfaces; qa-release-gatekeeper for release decision.

Output: PR SHA/base, evidence table (severity, file:line, effect, fix), CI/review summary, missing tests and verdict. If tools/data unavailable, report NOT CHECKED rather than PASS.

## Execution dependency

The optional `pr_review_report.py` helper lives in the **source repository's** `scripts/` folder, not inside this installed SKILL.md folder. If the source checkout and authenticated GitHub CLI are available, run that helper from the checkout. Otherwise use documented read-only `gh pr view`, `gh api` and actual diff review, or mark evidence NOT CHECKED. Do not download or execute remote scripts as a shortcut.

---

## 6. database-transaction-integrity

Safeguard SQL schemas, transactions, migrations, concurrent updates, payments, event consistency and audit ledgers. Use for persistent-state changes.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Database and transactional integrity

1. Read the actual database dialect, schema, migrations, data access layer and callers. Never assume ORM definitions exactly match deployed schema.
2. Define business invariants: uniqueness, legal state transitions, ownership, referential integrity, monetary precision and conservation.
3. Model adversarial timing: duplicate requests, simultaneous updates, callback replay, out-of-order events, crash before/after commit and partial failures.
4. Choose enforcement layers: database UNIQUE/CHECK/FK, atomic conditional writes, locks, isolation, idempotency keys and durable outbox where warranted.
5. For money, use explicit minor units/precision, immutable or traceable ledger entries and a reconciliation strategy; prohibit silent balancing adjustments.
6. For migrations, detail expand/backfill/validate/contract, mixed-version compatibility, index/lock cost and rollback limitations.
7. Add concurrency and failure-injection tests plus queries that detect invariant violations; distinguish dry-run from production execution.
8. Gate risky migrations on verified backups, privileges, monitoring and an approved rollback strategy.

Output: invariant table (rule, enforcement, test), race/failure matrix, migration sequence and safe/conditional/blocked verdict.
Never run destructive SQL on production without explicit permission.

## Local executable verification

The public source checkout includes `examples/reference-platform/booking.py` and nine database tests. On an authorized local checkout run `python -m unittest discover -s examples/reference-platform/tests -v`. Review its README for limits: SQLite semantics and an injected `verified` flag are **not** production payment-provider authentication. The negative tests include six-client contention, duplicate provider receipt, mismatched amount and ownership denial. Never generalize passing local tests to production DB migrations.

---

## 7. dependency-supply-chain-auditor

Review package dependencies, vulnerable versions, licenses, lockfiles, build provenance and CI security for web and backend repositories.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Software supply-chain auditing

1. Read ecosystem manifests and lockfiles (npm/pnpm/yarn, pip/uv/poetry, containers, infrastructure) from the current commit; avoid hallucinating dependency versions.
2. Create a dependency inventory by direct/transitive path, runtime vs development scope, update cadence and source provenance.
3. Run available **read-only** vulnerability/license/SBOM tools against approved manifests; capture exact commands, scanner DB timestamp and warnings about false positives.
4. For relevant advisories assess reachability, exposure, exploit preconditions and available patched ranges. Do not rate severity from CVSS alone.
5. Review install scripts, CI actions, third-party binaries, GitHub token permissions, pinned artifacts and provenance/signature verification where warranted.
6. Propose the smallest compatible remediation; model lockfile churn, API breakage, rollback and regression suite. Never auto-upgrade or install dependencies without scope approval.
7. Track accepted risk, ownership and retest date; do not present a scanner pass as an exhaustive security guarantee.

Output: inventory, evidence-backed vulnerabilities and licenses, prioritized upgrade plan, supply-chain controls, CI gate and unassessed components.

---

## 8. devops-ci-cd

Design reliable CI/CD, infrastructure configuration, staging/prod separation, deployment and rollback workflows for authorized repositories.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

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

---

## 9. documentation-handover

Create maintainable project documentation, ADR indexes, operator runbooks, release notes and contributor onboarding matched to actual code.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Documentation and handover
1. Establish audience: developer, QA, operator, stakeholder or end user. Match granularity and language to the task.
2. Inspect code and existing docs before asserting endpoints, commands, versions or environment details.
3. Keep a single source of truth; link to authoritative contracts and avoid duplicating volatile secrets/config.
4. Document setup, local validation, architecture boundaries, task flows, known risks, recovery and owner escalation as applicable.
5. Use runnable examples with safe placeholders; test commands when feasible and label untested steps.
6. Document breaking changes, migration sequence and version-dependent behavior in release notes.
7. Provide maintenance ownership and a review trigger when underlying code changes.

Output: updated docs, evidence references, audience assumptions, tested examples and unresolved accuracy checks.
Avoid publishing internal URLs, keys, customer data, or project-specific proprietary material.

---

## 10. frontend-design-direction

Create deliberate, distinctive, accessible frontend visual direction and interface composition grounded in the product's users and brand.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Frontend design direction

1. Establish audience, primary task, brand, information hierarchy, target devices and emotional tone. Explore references only when authorized/available.
2. Choose a clear visual concept justified by product context, rather than adding gradients or illustrations by default.
3. Plan hierarchy: navigation, primary action, content density, typography, spacing, rhythm, imagery and meaningful empty states.
4. Sketch interactions and account for loading, error, partial data, zero results, disabled actions, destructive confirmation and permission denial.
5. Design mobile-first; consider touch targets, keyboard navigation, readable contrast, screen readers, RTL and localization.
6. Implement against the project's current design system/components; avoid unrelated framework changes or broad refactors.
7. Use screenshots and browser testing when a UI execution environment exists; correct broken layouts before calling it done.

Output: visual rationale, key screen/state inventory, responsive rules, implementation details, visual verification and limitations.
Do not substitute a static mockup for functioning behavior when the user requested an application.

## Local RTL example

Review `examples/frontend-rtl/index.html` and `tokens.css` for a Persian RTL accessible-form prototype. The `node --test examples/frontend-rtl/ui.test.mjs` check covers state logic only. Perform real browser layout, keyboard and screen-reader checks before asserting visual/accessibility quality.

---

## 11. llm-api-integration

Design LLM-powered workflows using OpenAI, Anthropic or another provider with safe tool contracts, cost controls and offline evaluations.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# LLM API integration

1. Define user outcome, input/output schemas, privacy constraints, latency and cost budgets. Confirm why generative AI is needed.
2. Check current provider SDK/API documentation before choosing model names or interface features.
3. Separate the model adapter from application business rules; validate outputs, refusals, truncation, tool errors and untrusted retrieved data.
4. Specify prompt versioning, context budget, retrieval provenance, secret storage, rate limits and fallback behavior.
5. Make tool calls least-privilege and require authorization for external writes. Never treat model text as trusted commands.
6. Run fixture-based tests and scenario evaluations for task quality, hallucination, latency, price and safety; use representative failure cases.
7. Add bounded retry, backoff and monitoring without default collection of sensitive prompt content.

Output: provider-neutral diagram, schemas, evaluation harness plan, measured results and operating costs. Do not claim an API key or quota exists unless checked.

---

## 12. load-resilience-testing

Plan and conduct authorized, bounded load, soak, concurrency and fault-tolerance testing against isolated environments with measurable SLO criteria.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Load and resilience testing

1. Confirm **explicit authorization**, environment, owner, test windows, resource limits and stop conditions; default to isolated staging/local, never public production.
2. Define workload model: arrival pattern, concurrent users, sessions, hotspots, request mixture, representative data and baseline SLOs. Identify costly external integrations.
3. Keep test data synthetic, disable real monetary side effects and coordinate database quotas, email/SMS and vendor rate limits.
4. Use bounded gradual ramp-up: smoke -> realistic steady -> short peak -> recovery; reserve saturation or fault injection for a specifically approved environment.
5. Measure response distribution p50/p95/p99, error rates, queue/backlog, CPU/memory, database locks/connections and invariant breaches such as duplicate bookings.
6. Correlate server metrics and traces; investigate bottlenecks before tuning. Record actual generated load rather than only configured targets.
7. Define abort triggers and verify cooldown/recovery; report safe operating envelope with caveats. Do not automatically retry loads on failure.

Output: signed-off test boundary, script/tool versions, scenario, achieved throughput, latency/error metrics, failure evidence, suggested mitigations and NOT TESTED items.
This skill provides a protocol, **not permission to stress any live endpoint**.

---

## 13. mcp-integration-builder

Design or implement MCP servers and third-party integrations with explicit tool schemas, authentication, permissions, testability and safe retries.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# MCP and service integrations

1. Establish the user task and verify whether an existing maintained MCP connector already serves it. Build a server only if the gap justifies maintenance.
2. Inventory the external service's current documented API, auth/consent, rate limits, latency, quotas, billing and permission boundaries.
3. Design a minimal typed MCP tool surface: precise names/descriptions, JSON schemas, stable IDs, pagination and consistent errors.
4. Separate read-only operations from writes and destructive actions; require confirmation for sensitive mutations, scoped credentials and an auditable action log.
5. Validate untrusted tool output, limit data exposure, avoid prompt injection, and never put tokens in logs or returned model text.
6. Implement bounded timeout/retry/backoff with idempotency awareness; support health checks and safe failure messages.
7. Test schema validation, auth denial, API failure, rate limits and malicious input; document setup and least-privilege deployment.

Output: tool catalog, trust diagram, credentials handling, implementation plan/code, test evidence and operational cost.
MCP does not grant access automatically; users must explicitly authorize/connect services.

---

## 14. observability-monitoring

Plan product telemetry, health checks, logs, metrics, traces, SLOs and incident response for live platforms.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Observability and operations
1. Define user-critical outcomes and failure modes. Choose meaningful golden signals: latency, traffic, errors and saturation plus business integrity metrics.
2. Design structured logs with correlation IDs and appropriate privacy redaction. Distinguish debug logs from audit records.
3. Define metrics with stable labels/cardinality, units, sample rates, ownership, targets and alert thresholds justified by impact.
4. Add distributed tracing where cross-service latency/root-cause analysis warrants it; avoid tracing secrets or personal payloads.
5. Specify probes, dashboards, on-call runbooks, incident severity and escalation; route alerts to an accountable owner.
6. Define SLO/error budget for critical journeys when evidence supports a measurable target.
7. Verify alerts and recovery drills in a safe environment, then capture gaps and rollback triggers.

Output: telemetry contract, dashboard panels, alerts, runbook, test evidence and costs.
Do not claim monitoring is operational merely because instrumentation code exists.

## Offline SLO calculation specimen

Run `python examples/observability-gate/gate.py --sample examples/observability-gate/sample.jsonl` and `python -m unittest discover -s examples/observability-gate -p "test_*.py" -v`. These are synthetic sanitized request samples; the calculated 95th percentile and error budget do **not** prove operational telemetry, production SLO attainment or release readiness.

---

## 15. performance-accessibility

Assess and improve web performance and accessibility with measurable budgets, controlled profiling, and user-centered prioritization.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Performance and accessibility
1. Establish audience, critical devices/network conditions, accessible interaction needs and baseline user journeys.
2. Measure first: profiling, bundle size, request waterfall, query timing, core web vitals where feasible; state tool and environment.
3. Find the real bottleneck before refactoring: expensive renders, waterfalls, slow queries, oversized assets or long tasks.
4. Define realistic performance budgets and verify key interactions with mobile throttling where possible.
5. Audit semantic markup, contrast, keyboard order, screen-reader labels, focus, dynamic announcements, touch targets and reduced motion.
6. Propose minimal incremental fixes that preserve behavior; run regression and a11y checks again.
7. State which items require human assistive-tech review and what was not tested.

Output: measured baseline, prioritized findings, affected routes/components, remediation, measured change and outstanding accessibility risks.
Do not claim WCAG conformity from automated scanning alone.

## Local accessibility/performance boundary

The `examples/frontend-rtl` specimen provides focus-visible, reduced-motion and semantic-label patterns, while `examples/observability-gate` provides an offline latency gate. Neither replaces axe/Lighthouse/browser measurements, WCAG audits or real field performance data. State the measured-versus-proposed boundary in all outcomes.

---

## 16. playwright-webapp-testing

Test authorized local or staging web apps with Playwright, browser logs, screenshots and reproducible frontend regressions.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Playwright webapp testing

1. Confirm target URL, environment and permissions, test account, run command and non-production fixtures.
2. Review current tests and prefer stable accessible locators (roles, names, test IDs) over brittle selectors.
3. Verify server readiness without stopping unrelated active processes.
4. Exercise risk-based flows including success, loading, empty, errors, validation, permission denial, keyboard use and mobile widths.
5. Record console exceptions, failing requests, screenshots and traces where supported; use deterministic fixtures and avoid arbitrary sleeps.
6. Reset test data safely; do not perform real payments or destructive actions without permission.
7. Report the commit, exact test command, pass/fail/not-run outcomes, expected vs actual and reproduction steps.

Output: executable test plan, evidence, regression candidates and prioritized defects. Do not claim Playwright was run unless it was actually executed.

## Demo and evidence

The optional `examples/playwright/smoke.spec.ts` is an executable template only when a compatible runner and approved local app already exist. The separate `examples/frontend-rtl` does not auto-run Playwright. Browser observations must be captured from an actual browser run; unit-test passes are not browser-pass evidence.

---

## 17. privacy-data-governance

Review personal-data flows, retention, consent, access controls and data minimization for software product features.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Privacy and data governance
1. Inventory data types, sources, purpose, processors, storage region, recipients and lifecycle. Identify special or regulated data if relevant.
2. Document lawful/contractual bases and jurisdictional requirements as items to verify with counsel; do not give unsupported legal conclusions.
3. Minimize collection, data exposure in analytics/logs, default retention and third-party transfers.
4. Verify rights workflows where applicable: export, correction, deletion, withdrawal, access logging and processor obligations.
5. Coordinate encryption, secrets, authorization, tenancy and backup retention with security and infrastructure reviewers.
6. Add tests for role-based data access, expired retention, deletion propagation and incident response paths.
7. Treat policy and user promises as requirements only if approved by the product owner.

Output: data flow map, classification, risk register, controls, decisions requiring legal input and executable verification plan.
Never export or publish confidential customer data in repository examples.

---

## 18. product-business-analyst

Turn a product idea into evidence-based discovery, PRD, user journeys, scope, measurable acceptance criteria, and a prioritized MVP. Use for product definition or ambiguous features.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Product discovery and PRD

1. Identify problem, target users, context, jobs-to-be-done, measurable outcome, constraints and current alternatives. Distinguish known observations, stakeholder claims and hypotheses.
2. Map the user journey including onboarding, success, errors, cancellation, permissions, retries, localization and accessibility.
3. Define MVP and explicit out-of-scope features; prioritize by user value, evidence, delivery effort and risk. Do not assume a named framework is the right one.
4. Produce numbered requirements with actor, trigger, behavior, data needs, error handling and Given/When/Then acceptance tests.
5. List decisions requiring stakeholder input rather than inventing prices, SLAs, regulatory promises or authorization rules.
6. Define KPIs with units, numerator/denominator, measurement owner and guardrails.
7. Handoff approved requirements to architecture; mark unapproved proposals clearly.

Output: one-page problem framing, journeys, PRD requirements, acceptance criteria, MVP boundary, risks and success metrics.
Check: every in-scope feature has a testable outcome; no silently fabricated business policy.

---

## 19. project-bootstrap-environments

Bootstrap a reproducible software project with local, development, test, staging and production environment isolation, safe secrets, CI and onboarding.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Reproducible project bootstrap

1. Determine whether this is a new repository or an existing product. Inspect README, AGENTS.md, lockfiles, project structure, and running processes; do not scaffold over existing code.
2. Select a stack from approved requirements and delivery constraints. Avoid imposing Docker, monorepos or framework rewrites unnecessarily.
3. Define dev/test/staging/production boundaries, disposable fixtures, a secret-free .env.example and credential provisioning policies.
4. Pin runtime and package versions where practical. Establish reproducible builds, safe migrations, lint/typecheck/test commands and small CI gates.
5. Use least-privilege CI access; protect real secrets and never commit .env files or credentials.
6. Document bootstrap, smoke and teardown commands for supported OSes with disk/resource requirements; do not delete user files as a cleanup shortcut.
7. Test from a fresh isolated checkout if authorized and feasible; disclose missing prerequisites and nondeterministic setup steps.

Output: repository layout, environment contract, onboarding commands, clean setup evidence, CI plan and remaining constraints.
Never claim fresh-machine reproducibility without testing it.

---

## 20. qa-release-gatekeeper

Judge software release readiness from executed tests, change scope, migrations, security checks, incident risks and verified rollback.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Release gatekeeping
1. Identify exact commit/PR set, release candidate, environment and impacted workflows. Inspect current evidence rather than relying on memory.
2. Define required gates proportionate to risks: unit, integration, E2E, authorization, migrations, concurrency, configuration, health and rollback.
3. For each gate mark PASS, FAIL, BLOCKED, NOT RUN or NOT APPLICABLE; include command, environment and timestamp when known.
4. Stop a release for unresolved high-impact data corruption, payment, security or unrecoverable migration risks.
5. Issue GO only with adequate real evidence. CONDITIONAL GO requires explicit accepted risks, accountable approver and mitigation. Otherwise NO-GO.
6. Plan smoke tests, post-deploy monitoring, incident contacts, halt thresholds and rollback criteria.
7. Never deploy, modify production, or mark a release complete without explicit authorization.

Output: GO/CONDITIONAL GO/NO-GO, exact SHA, evidence matrix, blockers, accepted risks, monitoring and rollback.
Missing evidence is NOT RUN, never PASS.

## Executable evidence gate

The source checkout includes `examples/observability-gate/gate.py` with explicit availability and p95 thresholds and an intentionally synthetic fixture. Use actual authorized telemetry and inspect all CI/security/migration checks for a genuine release decision; never promote a synthetic sample or an isolated GREEN result into production authorization.

---

## 21. qa-test-strategy

Create balanced automated test portfolios including unit, contract, integration, security, failure and performance checks. Use when planning test coverage or regression prevention.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Risk-based automated testing
1. Identify business-critical journeys and consequences of failure. Prioritize money, access, data integrity, customer-facing continuity and integrations.
2. Inventory existing test runners, fixtures, CI time budget and coverage gaps from repository evidence.
3. Define a layered strategy: fast unit tests for rules, contract/integration tests for boundaries, E2E for essential journeys.
4. Include negative tests, validation, permissions, retry/idempotency, concurrency, timeout, timezone/localization and migration compatibility where relevant.
5. Use deterministic data and reliable setup/teardown. Distinguish mocks from real integration; minimize flaky sleeps.
6. Capture command, environment, commit and pass/fail/not-run for every executed check.
7. Define quality gates proportional to risk, not arbitrary 100% coverage targets. Identify what remains untested.

Output: test pyramid/matrix, test IDs, fixture needs, CI stages, execution evidence and next high-value tests.
Do not describe proposed tests as passed tests.

## Runnable example portfolio

Use `examples/reference-platform/tests` for invariant/negative/concurrency tests, `examples/frontend-rtl/ui.test.mjs` for pure UI-state tests and `examples/observability-gate/test_gate.py` for deterministic quality checks. Add request/contract/browser tests separately for a full test pyramid. Record test runner output, commit and environment; never claim E2E coverage from pure function tests.

---

## 22. react-artifacts-builder

Build multi-component interactive web interfaces using a compatible React stack, routing, state and UI primitives where appropriate.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Multi-component web app builder

1. Confirm requested deliverable: mockup, reusable component, interactive local demo, or production feature. Never imply a demo is a deployed system.
2. Inspect package versions, React framework (Next.js/Vite/etc.), existing routes, UI components and build/test commands.
3. Choose a minimal component hierarchy, state ownership, data loading and routing model. Use actual project libraries; do not assume Tailwind or shadcn is installed.
4. Separate view state, server state and derived state; validate form inputs and handle loading, empty, error, retry and offline states.
5. Include accessible semantics and keyboard/focus behavior for overlays, menus and forms.
6. Keep API contracts typed where feasible; never embed tokens/secrets in client bundles.
7. Run formatting, typecheck, tests and build where available; if unable to execute, identify that explicitly.
8. For complex interaction, verify through playwright-webapp-testing and capture reproducible evidence.

Output: files changed, architecture sketch, interaction states, test commands/results and remaining caveats.
Prefer working features to ornamental complexity.

## State-machine reference

Use `examples/frontend-rtl/ui.mjs` to inspect loading/success/error/reset transitions and safe text rendering, with `node --test examples/frontend-rtl/ui.test.mjs`. This example deliberately uses framework-free JavaScript, **not React**, so it can inform React state management but does not validate hooks, hydration or Next.js routing. Write framework-specific tests in the target project.

---

## 23. security-authorization-auditor

Audit authentication, authorization, roles, object ownership, API defenses, secrets and abuse protections against the repository's actual implementation.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Security and authorization auditing

1. Bound the review and identify actors, assets, trust boundaries, identity/session model and privileged operations.
2. Trace each selected route from authentication through policy checks, service logic and database filters.
3. Test for horizontal/vertical privilege escalation, broken object ownership, tenant leakage, mass assignment, TOCTOU and unauthenticated paths.
4. Check relevant threats: validation/injection, CSRF/CORS where applicable, rate limits, webhook authenticity, session invalidation, replay and sensitive logging.
5. Produce a permissions matrix (role × resource × action) and negative tests: wrong owner, wrong role, expired session, replay, missing credentials.
6. Grade findings by concrete likelihood and impact; distinguish confirmed findings, suspected risks and unreviewed surfaces.
7. Specify the smallest effective remedy and a regression test. Do not claim a penetration test when only static review occurred.

Output: evidence paths, threat scenario, severity, fix, test and residual risk.
Never reveal secrets, run unauthorized external scans, or change live credentials without approval.

## Local regression evidence

Use the fictional ownership and permission checks in `examples/reference-platform/tests/test_booking.py`, plus benchmark `v04-security` under `evals/benchmarks/` for a deliberately vulnerable API example. The benchmark has archived real-model read-only outputs but no verified production exploit or penetration test. A run of `python -m unittest discover -s examples/reference-platform/tests -v` tests domain ownership, not session-auth middleware or network security.

---

## 24. skill-authoring-toolkit

Create and maintain reusable Agent Skills in SKILL.md format, with precise triggers, testable workflows, safe tool permissions and validation.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Author reliable Agent Skills
1. Identify one specialized recurring task and examples where existing agent instructions underperform. Avoid a general-purpose catchall skill.
2. Write a concise frontmatter name (lowercase kebab-case) and description explaining *when* to use the skill, plus relevant exclusions.
3. Place essential decision rules, required evidence, safety boundaries and expected outputs in SKILL.md. Keep instructions short enough to be selectively loaded.
4. Add references/ only for substantial task-specific details and scripts/ only for deterministic repeatable work. No placeholder dependencies.
5. Separate planning from execution; never use a skill to expand user authorization or bypass platform restrictions.
6. Create example triggers and counterexamples to test routing; include a success/failure rubric and compare against a baseline without the skill.
7. Run the repository validator and tests; update documentation and examples. Review any third-party borrowed content and its specific license.

Output: installable folder, trigger cases, expected outputs, validation evidence and update notes.
A SKILL.md file cannot confer permissions, network access, native ChatGPT installation or tool availability.

---

## 25. skill-evaluation-benchmark

Evaluate whether an agent skill actually improves task outcomes using repeatable tasks, baseline-versus-skill runs, human-scored criteria and variance analysis.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Skill evaluation and benchmarking

This evaluates *agent behavior*, not only whether SKILL.md parses.

1. State the skill's intended improvement and when it should **not** trigger. Choose representative task prompts, a negative routing case, and objective or human-reviewable success criteria.
2. Freeze comparable inputs: repository commit, target model/settings, prompt, tools, task data and time budget. Record any unavoidable differences.
3. Run baseline **without** skill and candidate **with** skill independently where the coding agent is available; retain full output or reproducible artifacts. Do not synthesize results to pretend a model ran.
4. Score each run against named weighted criteria; provide specific evidence for passed criteria. Include correctness, safety, scope adherence, command/test evidence, cost/latency when available and unnecessary skill triggering.
5. Record ratings in the `evals/runs/*.json` schema described in `evals/README.md`; use `python scripts/evaluate_skills.py --baseline ... --candidate ...` to calculate comparison.
6. Inspect actual failures and variance over more than one case; note subjective scoring and the difference between a benchmark and production validation.
7. Refine the skill's trigger/workflow and rerun the same held-out checks; do not optimize solely for a tiny public test set.

Output: experiment setup, model/tool versions, baseline and candidate evidence, weighted scores, per-case deltas, untested risks and go/no-go recommendation. The provided demo fixture is *synthetic* and must never be cited as an actual LLM benchmark.

## Execution dependency

The scorer `scripts/evaluate_skills.py` and fixtures `evals/` are distributed in the **source repository** rather than copied by the skill installer. Clone and inspect the public repository first or implement the scoring protocol with tools already available. The `--require-real` option now verifies saved raw-output digests and independent session identifiers, but does not independently authenticate the executing model.

## v0.4 real-run fixtures and 29-case coverage

`evals/29-skill-benchmark.json` supplies a designed-but-**not-run** criterion set for every skill. `scripts/prepare_benchmark.py` emits reproducible baseline or skill-instructed prompts without executing a model. Two additional real, read-only Codex A/B pairs are recorded in `evals/runs/v04-*.txt` with manually scored rubrics under `evals/benchmarks/`. These are **in-context skill instruction** tests, not native host auto-trigger tests; use multiple replications and blind graders before asserting general benefit.

---

## 26. software-architect

Design or review software architecture, bounded contexts, dependencies, ADRs, failure modes and compatibility across services. Use for consequential system changes.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Software architecture

1. Read the repository, ADRs and contracts before describing the current architecture. Label unknown areas; do not invent diagrams.
2. Identify functional needs and operational requirements: latency, availability, security, growth, auditability, recovery, localization and team capacity.
3. Draw logical boundaries, data ownership, sync/async interactions and failure containment. Preserve existing public contracts unless explicitly approved.
4. Consider 2-3 concrete alternatives only when a meaningful trade-off exists; compare complexity, operational cost, reversibility and migration risk.
5. Evaluate failure modes (timeouts, duplicate requests, partial writes, unhealthy dependencies) and what the system does during degradation.
6. Specify a proposed ADR: context, decision, rejected options, consequences, date and evidence.
7. Sequence rollout: compatibility, feature flags when useful, migration, tests, telemetry and rollback trigger.

Handoff: data changes to database-transaction-integrity; permissions to security-authorization-auditor; release risk to qa-release-gatekeeper.
Output: observed architecture, decision, affected contracts, proposed ADR, delivery slices and unanswered questions.
Never treat a speculative improvement as an authorized rewrite.

---

## 27. technical-project-orchestrator

Coordinate multi-stage product delivery from agreed requirements to PRs and releases with critical paths, scoped Codex tasks and evidence-based status.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Technical project orchestration
1. Read task context, live repository issues/PRs and established ADRs. Keep confirmed facts distinct from remembered plans.
2. Define outcome, non-scope, acceptance gates, constraints, available owners and release environment.
3. Build a dependency graph from product scope to design, data, backend, frontend, QA, deployment and operations; minimize circular handoffs.
4. Split work into small executable tasks with IDs, paths, inputs, deliverables, dependencies, review owner and clear stop conditions.
5. Trigger companion skills only for material issues: architecture, DB integrity, security, UX, testing, deployment, observability.
6. Track status as PLANNED, READY, IN PROGRESS, BLOCKED, TESTED, RELEASED or DONE, with evidence. Code merged is not synonymous with deployed.
7. Protect ongoing user work: no unapproved destructive cleanup, environment changes, production writes or spurious repo cloning.

Output: critical path, task queue, dependency blockers, acceptance gates, evidence references and next actions.
Do not invent work progress or substitute planning for execution.

---

## 28. theme-design-system

Define and evolve a cohesive web or mobile design system with accessible tokens, typography, color, component variants and usage rules.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Theme and design-system factory

1. Read brand identity, screenshots and the existing token/component stack. Preserve established brand rules unless redesign was requested.
2. Describe 2 viable visual directions with rationale rooted in audience and domain; choose one after considering accessibility and technical cost.
3. Specify semantic color tokens (surface, text, border, focus, danger, success), light/dark variants, typography scales, spacing, radius and motion preferences.
4. Map tokens to actual component primitives (buttons, inputs, nav, dialogs, tables, alerts) and their hover/focus/disabled/error/loading states.
5. Ensure minimum readable contrast, visible keyboard focus, reduced-motion support, RTL/localization and responsive breakpoints where relevant.
6. Provide a migration map for existing styles; avoid generating a parallel design system that conflicts with shipped components.
7. Validate representative screens at mobile, tablet and desktop widths and collect visual regression evidence.

Output: theme rationale, token table or CSS variables, component state matrix, sample usage and integration notes.
Do not claim WCAG compliance without measured checks.

## Token reference

Inspect `examples/frontend-rtl/tokens.css` for semantic light/dark tokens, logical layout properties, focus outlines and reduced-motion preference. This is a testable starting point rather than a general-purpose component library. Measure actual contrast and RTL behavior in a browser before certification.

---

## 29. visual-assets-design

Plan visual assets for product websites and marketing materials with clear creative briefs, deliverable specifications and rights checks.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Visual assets and graphic design
1. Define medium, audience, dimensions/aspect ratio, brand constraints, intended placement, accessibility needs and delivery file formats.
2. Choose a coherent visual concept grounded in the product rather than generic decorative motifs.
3. Inventory which assets must be created versus sourced; verify usage rights, brand claims and required attributions.
4. For image generation, specify subject, composition, lighting, typography constraints, crop-safe areas and iteration criteria; use an authorized image tool if available.
5. Review readability, contrast, layout at final display/print size, responsive crops and image optimization.
6. Export using the requested editable/source format when supported; a raster preview is not an editable design file.
7. Label generated or proposed assets honestly; do not state final assets were delivered without actually creating and inspecting them.

Output: brief, visual direction, production specifications, asset inventory, usage rights and QA checklist.
