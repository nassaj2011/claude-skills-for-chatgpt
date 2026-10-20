---
name: llm-api-integration
description: Design LLM-powered workflows using OpenAI, Anthropic or another provider with safe tool contracts, cost controls and offline evaluations.
---

# LLM API integration

1. Define user outcome, input/output schemas, privacy constraints, latency and cost budgets. Confirm why generative AI is needed.
2. Check current provider SDK/API documentation before choosing model names or interface features.
3. Separate the model adapter from application business rules; validate outputs, refusals, truncation, tool errors and untrusted retrieved data.
4. Specify prompt versioning, context budget, retrieval provenance, secret storage, rate limits and fallback behavior.
5. Make tool calls least-privilege and require authorization for external writes. Never treat model text as trusted commands.
6. Run fixture-based tests and scenario evaluations for task quality, hallucination, latency, price and safety; use representative failure cases.
7. Add bounded retry, backoff and monitoring without default collection of sensitive prompt content.

Output: provider-neutral diagram, schemas, evaluation harness plan, measured results and operating costs. Do not claim an API key or quota exists unless checked.
