---
name: backend-debugging
description: Investigate backend defects using reproducible evidence, traces, hypotheses, binary isolation and regression tests. Use for crashes, incorrect business logic, intermittent failures, or API incidents.
---

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
