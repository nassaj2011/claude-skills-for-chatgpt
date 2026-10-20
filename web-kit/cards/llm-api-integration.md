# ChatGPT Web: llm-api-integration

Original: https://github.com/nassaj2011/claude-skills-for-chatgpt

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

## Specialist workflow

# LLM API integration

1. Define user outcome, input/output schemas, privacy constraints, latency and cost budgets. Confirm why generative AI is needed.
2. Check current provider SDK/API documentation before choosing model names or interface features.
3. Separate the model adapter from application business rules; validate outputs, refusals, truncation, tool errors and untrusted retrieved data.
4. Specify prompt versioning, context budget, retrieval provenance, secret storage, rate limits and fallback behavior.
5. Make tool calls least-privilege and require authorization for external writes. Never treat model text as trusted commands.
6. Run fixture-based tests and scenario evaluations for task quality, hallucination, latency, price and safety; use representative failure cases.
7. Add bounded retry, backoff and monitoring without default collection of sensitive prompt content.

Output: provider-neutral diagram, schemas, evaluation harness plan, measured results and operating costs. Do not claim an API key or quota exists unless checked.

## Your task

[Replace with your actual request and non-sensitive code/context.]

## Response

Provide actionable deliverables, evidence/assumptions, checks NOT EXECUTED and risks.
