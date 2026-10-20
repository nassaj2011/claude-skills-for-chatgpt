---
name: qa-test-strategy
description: Create balanced automated test portfolios including unit, contract, integration, security, failure and performance checks. Use when planning test coverage or regression prevention.
---

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
