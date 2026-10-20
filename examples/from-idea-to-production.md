# Fictional end-to-end platform example: community sports reservations

This is a **fictional educational case**, not code or requirements copied from any existing product.

## 1. Discover
Request: "Create a system where a user can reserve one court slot and pay online."

Use `product-business-analyst`. Output: user journey, cancellation/refund questions, reservation duration, accessibility/RTL decisions and testable requirement IDs such as R-01 "one successful reservation for an available court slot".

**Gate:** requirements are approved; unresolved payment rules remain explicit open decisions.

## 2. Architect
Use `software-architect` and `database-transaction-integrity`. Model slot ownership, holds, reservation lifecycle, payment callback replay and atomic uniqueness constraints.

**Gate:** ADR explains concurrency handling, database invariant enforcement and failure recovery.

## 3. Design and build
Use `frontend-design-direction`, `theme-design-system`, `react-artifacts-builder` and `backend-api-engineer`. Cover keyboard focus, unavailable slots, interrupted checkout, validation errors and mobile layouts.

**Gate:** typed API responses, backend ownership checks and no secrets in the browser bundle.

## 4. Verify
Use `qa-test-strategy` + `playwright-webapp-testing` for authorized local tests. Include two users attempting the same slot and callback replay. Use `backend-debugging` for failed scenarios.

**Gate:** attach real commands, commit, environment, test results, logs and screenshots where available. Not-run checks remain not-run.

## 5. Release
Use `devops-ci-cd`, `security-authorization-auditor`, and `qa-release-gatekeeper` to review migrations, auth, staging smoke checks, backups and rollback. Only deploy with explicit authorization.

**Gate:** evidence-based GO/NO-GO with named risk owner.

## 6. Operate
Use `observability-monitoring` and `documentation-handover`. Define alerts for reservation errors, double-booking invariant breaks, callback replay failures and elevated checkout latency.

**Gate:** alert routing, on-call runbook and a tested incident drill.

## Example prompt

> Review my platform idea using product-business-analyst, then produce a scoped plan using software-architect and technical-project-orchestrator. List database, security and QA gates. Don't modify code until I approve the task boundary.

This does not execute a platform build; it demonstrates selection and handoff.
