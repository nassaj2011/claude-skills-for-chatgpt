# ChatGPT Web: load-resilience-testing

Original: https://github.com/nassaj2011/claude-skills-for-chatgpt

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

## Specialist workflow

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

## Your task

[Replace with your actual request and non-sensitive code/context.]

## Response

Provide actionable deliverables, evidence/assumptions, checks NOT EXECUTED and risks.
