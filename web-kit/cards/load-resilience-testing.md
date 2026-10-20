# ChatGPT Web: load-resilience-testing

Original: https://github.com/nassaj2011/claude-skills-for-chatgpt

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

## Specialist workflow

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

## Your task

[Replace with your actual request and non-sensitive code/context.]

## Response

Provide actionable deliverables, evidence/assumptions, checks NOT EXECUTED and risks.
