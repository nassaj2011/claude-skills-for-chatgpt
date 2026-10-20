# ChatGPT Web: backend-debugging

Original: https://github.com/nassaj2011/claude-skills-for-chatgpt

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

## Specialist workflow

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

## Your task

[Replace with your actual request and non-sensitive code/context.]

## Response

Provide actionable deliverables, evidence/assumptions, checks NOT EXECUTED and risks.
