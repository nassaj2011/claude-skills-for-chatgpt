---
name: playwright-webapp-testing
description: Test authorized local or staging web apps with Playwright, browser logs, screenshots and reproducible frontend regressions.
---

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
