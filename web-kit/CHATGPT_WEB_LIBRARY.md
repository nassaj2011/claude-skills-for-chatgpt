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
- backup-disaster-recovery: Plan and verify backup integrity, isolated restore drills, RPO/RTO objectives, application consistency, provenance and incident recovery with explicit authorization.
- code-review-pr: Review pull requests and code changes for correctness, security, API compatibility, missing tests and CI failures; inspect reviewer comments and GitHub checks before merge.
- database-transaction-integrity: Safeguard SQL schemas, transactions, migrations, concurrent updates, payments, event consistency and audit ledgers. Use for persistent-state changes.
- dependency-supply-chain-auditor: Trace dependency inventory, lockfile provenance, vulnerabilities, licenses, install-time scripts and CI action permissions with evidence-backed remediation.
- devops-ci-cd: Review, design and safely validate CI/CD pipelines, reproducible builds, release approvals, migrations, least-privilege secrets and rollback evidence across environments.
- documentation-handover: Create maintainable project documentation, ADR indexes, operator runbooks, release notes and contributor onboarding matched to actual code.
- frontend-design-direction: Create deliberate, distinctive, accessible frontend visual direction and interface composition grounded in the product's users and brand.
- llm-api-integration: Design and validate LLM application integrations, provider adapters, safe structured outputs, tool authorization, rate limits, budgets and reproducible offline evaluations.
- load-resilience-testing: Design and interpret authorized bounded load, concurrency, soak and resilience tests with explicit target isolation, abort thresholds, achieved metrics and recovery checks.
- mcp-integration-builder: Build or audit least-privilege MCP tools and third-party integrations with explicit schemas, user consent, typed errors, tool-output trust boundaries and replay-safe actions.
- observability-monitoring: Plan product telemetry, health checks, logs, metrics, traces, SLOs and incident response for live platforms.
- performance-accessibility: Diagnose web latency, accessibility and responsiveness with measured budgets, real browser interaction, assistive-tech limitations and proof of regression improvements.
- playwright-webapp-testing: Test authorized local or staging web apps with Playwright, browser logs, screenshots and reproducible frontend regressions.
- privacy-data-governance: Trace personal-data flows, minimization, user rights, retention, vendor transfers, deletion propagation and privacy release evidence for software platforms.
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
- visual-assets-design: Specify, produce where tools permit, and quality-check visual assets for apps, social and print with geometry, accessibility, typography, licensing and honest source-file delivery.

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

Plan and verify backup integrity, isolated restore drills, RPO/RTO objectives, application consistency, provenance and incident recovery with explicit authorization.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Backup and disaster recovery — restore evidence over backup status

## Trigger and safe boundary
Use for backups, migrations, data-loss resilience, disaster recovery, ransomware recovery and continuity plans. Nothing here authorizes restoring onto production or deleting retained backups. In ChatGPT Web with no filesystem tools, produce a runbook and label all verification NOT RUN.

## Specialist recovery protocol
1. Inventory critical data and *dependencies*: relational databases, files/object storage, key material (names only), WAL/PITR, worker queues, idempotency/payment state, DNS, runtime environment and third-party data. Identify system owners and blast radius.
2. Agree RPO (acceptable data loss), RTO (acceptable downtime), testing cadence, retention/jurisdiction and incident priorities with accountable stakeholders. Missing targets are OPEN DECISIONS, not inferred numbers.
3. Map backup type to consistency requirements: database-consistent dumps/snapshots, transaction logs, offsite/immutable copies, encrypted storage, key recovery, rotation and independent credentials. A list of backed-up files is not a database-consistent snapshot.
4. Check file-level checksum/catalogue manifests for tamper evidence, but separate **integrity** from **restorability**. Review metadata, last success timestamp, storage reachability, encryption key access and coverage of tenant/application tables.
5. Specify authorized **isolated restore** into a disposable environment, validate actor/tenant isolation, referential/financial integrity, queued job replay, payment side effects (disabled), health smoke and partial-failure recovery. Measure achieved restore time and point-in-time actual loss from controlled test markers.
6. Perform negative fault drills only inside a disposable test: missing object, corrupted archive, stale key, incomplete WAL and restored backup with pending deletion requests. Record fail-closed decisions and protected originals.
7. Release readiness requires actual restore evidence, responsible approval, measured RPO/RTO and known caveats. A backup dashboard showing green does not establish recovery.

## Deliverables
Protection matrix | backup schedule/retention/key owner | restore checklist | measured vs target RTO/RPO | consistency and access tests | failures and remediation owner | declared readiness GO/NO-GO/NOT TESTED.

## Executable reference
The repository provides `scripts/backup_manifest.py` for authorized backup-folder SHA-256 verification. A new `examples/restore-drill/` synthetic source-to-isolated-destination drill tests exact content recovery, corruption detection and no-overwrite, but **does not verify database consistency or production RTO**. All tests create temporary data.

## Hard limits
Never run an unapproved restore, expose backups with real personal data, claim encryption keys are recoverable without proof or automatically clean up user-owned originals.

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

Trace dependency inventory, lockfile provenance, vulnerabilities, licenses, install-time scripts and CI action permissions with evidence-backed remediation.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Dependency and supply-chain audit — provenance before scores

## Appropriate use
Apply to package upgrades, dependency threats, license approval, SBOM, registry trust, container base images, CI marketplace actions and lockfile integrity. Not a general code style check.

## Steps
1. Record exact source SHA and **actual** ecosystem manifests/lockfiles, package manager, runtime platform and environment. Do not guess dependency versions or introduce packages without permission.
2. Build direct/transitive inventory: package | pinned version/source | dependency path | runtime/dev | integrity/provenance | license/SPDX | repo evidence.
3. Identify registry substitution/typosquatting, dynamic dependency ranges, install/postinstall scripts, git-sourced tarballs, compromised CI actions, unverified binary downloads and overbroad workflow tokens. Use pinned trusted references where possible.
4. If authorized tools and databases are available, run read-only SBOM, vulnerability and license scanners; capture scanner/advisory database timestamps, severities, fixed ranges, false positives and coverage. Never fabricate live CVEs or current advisory conclusions.
5. Assess each potential finding for reachability, configuration, exposure, vulnerable call path and exploit prerequisites. CVSS alone is not deploy impact. Maintain separate VERIFIED / SUSPECTED / UNKNOWN.
6. Propose minimal upgrades with compatibility test matrix, safe lockfile regeneration plan, rollback and provenance checks; do not update installed dependencies automatically or alter public registry contents.
7. Gate critical issues on ownership, exact manifest change, actual rerun evidence and approval or documented exception with an expiry. A clean static lint check cannot certify the entire supply chain.

## Required output
Inventory + SBOM plan | suspicious source and script checks | evidence-linked risk table | fixed-range plan | license obligations | CI permissions recommendations | residual blind spots.

## Runnable reference
`examples/supply-chain/` implements a **toy lockfile policy linter** against synthetic dependency metadata. It flags floating ranges, non-registry sources and lifecycle script concerns but is NOT an npm/pip parser or live vulnerability feed. In ChatGPT Web without repository access, ask for redacted manifest excerpts and write commands to execute later, marked NOT RUN.

## Limitations
No unauthorized installs, silent upgrades, fabricated CVE matches, covert telemetry or unsupported license/legal conclusions.

---

## 8. devops-ci-cd

Review, design and safely validate CI/CD pipelines, reproducible builds, release approvals, migrations, least-privilege secrets and rollback evidence across environments.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

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

Design and validate LLM application integrations, provider adapters, safe structured outputs, tool authorization, rate limits, budgets and reproducible offline evaluations.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# LLM API integration — auditable implementation contract

## Trigger, exclusions and tool boundary
Use for LLM-assisted features, API/provider migration, structured answers, retrieval, agents with tools and inference reliability. Do not invoke for deterministic CRUD that needs no model. On ChatGPT web without an actual service connector, produce code/specifications and mark model calls and observed costs **NOT RUN**; pasting this skill does not grant API access.

## Review and engineering sequence
1. Clarify product outcome, user/tenant scope, prompt and output classifications, consent, jurisdictions, risk tolerance, minimum quality, timeout, budget and realistic latency. Verify from current provider docs before naming concrete model, pricing, SDK or feature.
2. **Separate roles:** model adapter, policy/authorization boundary, deterministic validation, tool executor, audit/metrics and domain transaction service. Model output is untrusted and must never directly authorize a write, payment or data access.
3. Create versioned typed JSON contracts. Bound input size, output size and schema depth, reject unknown keys, injection, truncation and invalid tool requests. Never parse a refusal or incomplete response as success.
4. Define prompt/data trust levels: developer policy, user request and retrieved/tool content. Treat retrieved web pages and documents as *data*, not instructions. Redact unnecessary personal data, keep provider credentials out of client bundles/logs and use explicit service-side secret handling.
5. Provide **bounded failure behavior**: timeout, transient retry/backoff, provider quota, 429, server errors, max attempts, idempotency for external side effects and budget exhaustion. Retry only safe read operations; do not retry a non-idempotent write after uncertain outcomes.
6. Evaluate offline first: golden fixtures for valid structured outputs, schema errors, refusals, prompt injection, oversized inputs, provider errors and double tool calls. For online model quality, preserve model/version, prompt, seed or sampling controls where supported, input case IDs, human scoring method and cost/tokens/latency if genuinely observed.
7. Gate release on actual acceptance tests, logs without raw sensitive prompts, permissions, trace IDs, cost limits, fallbacks and rollback to deterministic handling. Do not claim security or answer accuracy from unit tests alone.

## Required artifacts and decision
- Architecture and trust diagram; minimal adapter interface; JSON schema and rejection examples
- Provider-independent failure/timeout/retry matrix with exact ceilings and budget owner
- Tool permission matrix: actor | operation | resource | write confirmation | audit event
- Evaluation plan: labeled cases, metric, baseline, observed outputs and missing evidence
- Release decision PASS/FAIL/NOT RUN, including unresolved privacy, vendor and hallucination risks

## Executable reference
`examples/llm-contract/` is a **network-free** deterministic fake provider and gate suite that tests schema validation, tool authorization, injection-shaped text, quotas and retries. It does not call a real model or validate model quality. In ChatGPT web, provide its concepts and runnable examples for later execution without assuming Python is available.

## Forbidden shortcuts
Never secretly transmit user code or prompts, ask for tokens when not necessary, treat model output as authority or assert latest API pricing without source/date. Do not weaken tool permissions to make demos pass.

---

## 12. load-resilience-testing

Design and interpret authorized bounded load, concurrency, soak and resilience tests with explicit target isolation, abort thresholds, achieved metrics and recovery checks.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Load, concurrency and resilience — controlled test protocol

## Trigger and scope
Use for capacity, p95/p99 latency, error budgets, burst behavior, queues, failover, idempotency under load and saturation investigations. Do **not** invoke to fire traffic at an unapproved public host or for a routine, low-risk unit test.

## Before any traffic: hard authorization gate
1. Record owner/approval, exact target address/environment, test window, max duration, request ceiling, concurrency cap, rate cap, contact/abort channel and whether test accounts or costs are isolated.
2. **Default is DESIGN ONLY.** Without explicit approval and environment boundaries, output a script/plan without running it. Never infer authorization from having a URL, session token or repository access. Do not load test third-party services or shared production endpoints.
3. Prevent money transfers, customer notifications, irreversible writes, data exports, external API costs and tenant interference. Arrange synthetic fixtures, safe credentials, cleanup permission and downstream mocks before runs.

## Workload design
4. State workload: arrival rate versus closed-loop concurrency, endpoint mix, session think time, tenant/slot hotspots, representative payloads, warmup/steady/burst/recovery, ramp steps, maximum traffic **actually generated**, retries and timeout budgets.
5. Separate latency percentiles, achieved throughput, successes/errors, 429s, server saturation, DB connection/lock waits, queue depth, duplicates/data invariants and dependency rate limits. Sampling interval and monotonic clocks must be disclosed.
6. Use bounded phases: smoke -> realistic steady -> short peak -> recovery. Stop immediately for agreed overload signals, data invariant violations, unauthorized target change or spending thresholds. Never automatically retry destructive load phases.
7. Measure recovery, backlog drain and post-load integrity. Report confidence limits (sample size, cache effects, client bottleneck, mock dependencies, skew, observed vs configured throughput).

## Required deliverable
- **Authorization and limits table:** environment | approval/evidence | rps | concurrency | duration | total requests | abort triggers.
- **Workload plan:** exact phases, commands or pseudocode, synthetic data, rollback and monitoring ownership.
- **Metrics evidence:** achieved requests/sec, count, errors/429/timeout, p50/p95/p99, queue/DB/invariant checks and traces where available.
- **Results matrix:** each threshold PASS/FAIL/NOT RUN, baseline comparison, bottleneck hypotheses and prioritized mitigation.
- **Recovery and next experiment:** clear guardrails; no invented capacity or percentage improvements.

## Executable example and browser-only mode
examples/bounded-load/ is a local-only standard-library Python example that measures an intentionally tiny synthetic service using explicit loopback and hard request caps; this is **not evidence of real application capacity**.
In ChatGPT web without a load runner, generate only the approval request, bounded workload configuration, instrumented metrics plan and acceptance criteria. Mark all execution NOT RUN.

## Safety and reliability
Do not bypass rate limits, run stealth traffic, perform denial-of-service experiments against external targets or erase evidence. Never use public production endpoints without named explicit permission. If authorization is missing, the correct answer is an actionable **unexecuted** test plan.

---

## 13. mcp-integration-builder

Build or audit least-privilege MCP tools and third-party integrations with explicit schemas, user consent, typed errors, tool-output trust boundaries and replay-safe actions.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# MCP integration builder — contract, authority and evidence

## When to use
Choose for MCP servers, tool catalogs, service connectors, read-only search integrations or carefully authorized mutations. For ordinary REST APIs without an MCP interface, use a backend/API workflow instead.

## Implementation protocol
1. Verify whether a maintained existing connector already meets the user task; avoid inventing endpoints or promising access where no connector is installed. Record provider/API documentation version and the actual account/tenant access state.
2. Build a **small typed contract** per operation: stable tool name, plain-language purpose, input/output JSON shape, strict unknown-field rejection, maximum field lengths, pagination, bounded timeouts and stable machine-readable errors.
3. Create a **permission matrix** before code: caller identity, tenant/resource scope, tool read/write class, required consent and confirmation, audit event and escalation boundary. A tool description is never an authorization system; enforce checks at the service boundary.
4. Treat tool results and retrieved text as untrusted. Reject injected role instructions, never interpolate raw tool output into shell commands/SQL, and ensure sensitive data minimization, origin checks and redacted error responses.
5. Define transport/authentication and least-privilege secrets storage only after verifying platform/server requirements. Prefer independent narrow credentials; never expose tokens through model-visible outputs. Validate scopes for each request, not just at connection time.
6. For writes, use idempotency keys, duplicate/replay detection, explicit human approvals when sensitive, and reconciliation after uncertain timeouts. No auto-retry after a non-idempotent partial write.
7. Run negative tests for malformed input, unknown tools/fields, unauthorized actor/tenant, missing confirmation, duplicated requests, vendor 429/timeout, prompt-injection payloads and external network denial.
8. Publish read-only first and record versioned schemas, integration changes, revocation path, logs without personal identifiers and incident response. Never claim a provider connection from static mock tests.

## Deliverable
Tool catalog + JSON schema | trust/permission matrix | errors/retries/idempotency table | mock tests and truly executed outcomes | deployment/access setup | remaining risks and user actions.

## Local fixture and ChatGPT web
`examples/mcp-contract/` is an offline mock tool dispatcher with strict input validation, actor/tenant checks and replay handling. It does **not** start a network MCP server, prove MCP protocol interoperability or connect to a third-party app. In ChatGPT Web, provide a ready-to-integrate design; actually reading an account requires a connected authorized tool.

## Absolute limits
No hidden data collection, service-side credential leaks, unsolicited destructive actions or assumptions that the user granted external system access.

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

Diagnose web latency, accessibility and responsiveness with measured budgets, real browser interaction, assistive-tech limitations and proof of regression improvements.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Web performance and accessibility — measurable user journeys

## Scope and anti-trigger
Use for slow pages, Core Web Vitals, interaction lag, excessive bundles, image loading, keyboard navigation, screen-reader problems, WCAG-related audits and RTL responsive issues. Do not invoke a heavy browser audit for a documentation typo.

## Specialist process
1. Define users, languages (RTL/LTR), disabilities and devices, affected routes, browser/viewport/network, critical journeys and actual baseline. A synthetic desktop screenshot cannot prove phone accessibility or field performance.
2. Keep **observed** measurements distinct from targets: Web Vitals such as LCP, CLS and INP (where supported), request totals, transferred bytes, CPU long tasks, JS bundle and backend/database timings. Report real device versus laboratory method, percentile/sample count and measurement variability.
3. Identify the dominant root cause before changing code: layout shift source, oversized images, render waterfalls, unbounded state updates, expensive SQL, disabled caching or blocking third-party scripts.
4. Define testable budgets and gates with units, percentile and environment. Avoid invented Lighthouse/axe scores; when a tool is unavailable, specify it as NOT RUN and provide the commands.
5. Perform keyboard-only tab sequence, focus-visible and reset/return focus, form labels/errors, accessible names/roles, polite live regions, contrast, zoom/reflow, reduced motion and screen reader review. Automated passes do **not** prove WCAG conformance.
6. For Persian and mixed-direction UI, verify document language, RTL order, numeric input and localized status messaging, truncated text and mobile no-overflow behavior. Fix HTML semantics rather than relying exclusively on ARIA patches.
7. Prefer minimal reversible changes, then rerun the **same browser/device profile** and verify functional regression, accessibility and performance before claiming success.

## Evidence contract
Journey | baseline vs revised metric + units | tool/browser/viewport | p75 where applicable | screenshot/trace | issue severity | fix and owner | PASS/FAIL/NOT RUN. Separate user-impact claims from measured facts.

## Executable reference
The local `examples/frontend-rtl/browser_smoke.py` already checks real Edge RTL/keyboard behavior. New `examples/perf-budget/` measures a **self-hosted** synthetic page's visible DOM and request budget against declared thresholds using a local browser when installed; it makes no external requests. This does not substitute for axe, Lighthouse, production RUM or a human screen-reader audit.

## Security and compatibility
Do not run unapproved invasive testing on production endpoints, introduce telemetry collecting personal data or assert compliance based on a few scripted controls. On ChatGPT Web lacking browser tools, return a test plan and mark checks NOT RUN.

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

Trace personal-data flows, minimization, user rights, retention, vendor transfers, deletion propagation and privacy release evidence for software platforms.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Privacy and data governance — executable review contract

## Use when
The task involves personal data, logs/analytics, identity, marketing preferences, uploads, vendors, data exports or customer rights. Do not invoke for a purely static CSS change without user data.

## Evidence-first workflow
1. **Scope and authority.** Identify jurisdictions, controller/processor relationships, products, audiences, data subjects, environments and actual sources available. Label unknowns; do not assert GDPR or other legal compliance from generic guidance. Obtain qualified legal review for legal basis, cross-border transfers, sensitive classes and statutory timelines.
2. **Data map by field, not by feature name.** Record each field and purpose, source, processing system, recipient, access role, transmission/storage region, legal-basis question, retention trigger, deletion path and evidence reference. Include analytics, monitoring, test snapshots, exports, support tickets, message vendors and backups; distinguish operational logs from business records.
3. **Classify each disclosure.** Identify required vs optional fields, security/PII severity and whether user choice is required. Apply data minimization and pseudonymization at both collection and **each recipient boundary**; avoid raw phones, IDs or free-text payloads in analytics/traces.
4. **Map lifecycle.** Describe access/correction/export/deletion/withdrawal requests, system-of-record, processors, downstream copies, caches, archives, backups and restoration risk. Never promise instant erasure from immutable backups; state actual retention/restore quarantine controls and lawful exceptions as decisions.
5. **Tie risks to controls.** Specify owner, severity, exact remediation, source of verification, test case and blocker status. Prioritize unauthorized disclosures or unclear external sharing before cosmetic policy text.
6. **Verify on permitted environments.** Negative tests must cover role- and tenant-scope reads, analytics payload schema, CSV export permissions, deletion propagation, processor contracts, restored-backup deletion replay and incident logging without raw PII. Use synthetic records only.
7. **Decide and hand off.** Mark each gate PASS / FAIL / NOT RUN / NEEDS LEGAL REVIEW. Do not call legal compliance 'verified' solely because a checklist is complete.

## Required deliverable
- **Data-flow inventory:** field | source | purpose | recipient | basis to verify | region | retention trigger | deletion path | evidence.
- **Risk register:** severity | affected data | exploit/exposure pathway | owner | corrective action | acceptance test | status.
- **Lifecycle and user-rights map:** entrypoint, identity verification, response/exceptions, cascade, backup behavior.
- **Concrete acceptance tests** with an expected result; note tests not run and legal questions unresolved.
- **Executive decision** to proceed, block, or defer with explicit accountable sign-off, not a legal conclusion.

## Browser-only / ChatGPT web
If repository, storage, analytics configurations or tools are unavailable, ask for **redacted** schema/data-flow descriptions and produce an example matrix with NOT VERIFIED labels. Provide SQL or tests to run later rather than implying access. Never upload, store, echo or transmit real customer datasets unnecessarily.

## Verified local reference
An illustrative field-inventory validator and redacted sample live in examples/privacy-inventory/ in the public source checkout. They implement project-defined data policy checks, **not legal certification**. Run its tests only if a permitted local Python environment exists; otherwise use the checklist above.

## Safety constraints
No covert telemetry, hidden source-code collection, secret extraction or backdoor. Do not invent legal deadlines, consent grants, data-controller roles, contractual rights or privacy compliance. Never export real personal data into a public skill repository.

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

Specify, produce where tools permit, and quality-check visual assets for apps, social and print with geometry, accessibility, typography, licensing and honest source-file delivery.

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

# Visual asset design — creative direction to verifiable handoff

## When to apply
Use for app illustrations, logos, icons, posters, printable artwork, social cards, responsive hero visuals and campaign graphics. Do not call for an unrelated API/backend change.

## Specification before rendering
1. Establish medium, audience, placement, physical dimensions or screen size, aspect ratio, target platforms, pixel density, bleed/safe margin, available source files and whether an **editable source** is required. Resolve typography language, font licensing, brand colors, accessibility and legal claims.
2. Distinguish **reference media**, user-owned source, brand assets, AI-generated original work and externally licensed images. Record rights, attribution, permitted modifications, expiry/territory and any approvals; unclear rights are a blocker for publication.
3. Write a structured brief: hierarchy, concept and one visual focal point, tone, content, constraints, reference inspiration versus prohibited copying, responsive crop variants and localized text. Preserve user-supplied identities/details when editing and disclose uncertainty.
4. Choose output path based on available tools: (a) generate/edit a rendered image if an authorized image tool is available and requested, (b) create an inspectable SVG/HTML vector where source is requested, or (c) give a production-ready specification and clearly label it NOT RENDERED. Never claim an image file exists because a prompt was written.
5. Specify exact sizes and units (px, mm, dpi as appropriate), intended exports (SVG/PNG/JPG/PDF/print CMYK subject to service capability), sharpness/contrast, RTL shaping, text safe areas and source format. Do not present a raster screenshot as an editable layered design.
6. QA at final size: spelling and line breaks (especially Persian/Arabic), font fallback, copyright/trademarks, actual contrast, alignment, small-screen cropping, low-vision alternatives, transparency, bleed and printer profile. State which checks were visually inspected vs only specified.
7. Iterate against measured acceptance criteria and record versioned filenames, licensed inputs, source file and exports. Do not modify/destroy originals without explicit permission.

## Required deliverables
- **Asset brief:** intended use, audience, dimensions, copy, hierarchy, palette, reference constraints, localizations.
- **Production matrix:** artifact | editable source | export formats | dimensions | crop/bleed/safe zones | accessibility.
- **Rights register:** origin | owner/license | permitted use | credits/approval | status.
- **QA checklist:** test | tool/evidence | PASS / FAIL / NOT TESTED.
- **Handoff decision:** READY only for actually generated, rights-cleared and inspected assets; otherwise DRAFT / BLOCKED and exact next step; mark unavailable tool checks NOT RUN.

## Local reference and web fallback
examples/visual-asset/ contains an authored, accessible SVG card and standard-library checks for viewBox/dimensions, descriptive text, references and rights manifest. These **do not establish print color accuracy, legal rights or visual taste**.
In ChatGPT web, use available image tools when appropriate; if not, produce the brief and exact prompts/source code with the label NOT RENDERED. Do not pretend an AI image was created without an actual rendering tool.

## Security, rights, and privacy
No hidden trackers, external SVG dependencies, malicious scripts, unlicensed celebrity/brand claims, private user media uploads to public stores or silent likeness modifications. Preserve original source material; document every changed element.
