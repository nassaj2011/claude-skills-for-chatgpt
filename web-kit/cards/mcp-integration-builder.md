# ChatGPT Web: mcp-integration-builder

Original: https://github.com/nassaj2011/claude-skills-for-chatgpt

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

## Specialist workflow

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

## Your task

[Replace with your actual request and non-sensitive code/context.]

## Response

Provide actionable deliverables, evidence/assumptions, checks NOT EXECUTED and risks.
