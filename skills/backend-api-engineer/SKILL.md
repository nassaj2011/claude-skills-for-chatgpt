---
name: backend-api-engineer
description: Build and review maintainable backend endpoints, service boundaries, validation, error contracts, pagination and integration reliability.
---

# Backend API engineering

1. Inspect live code, framework conventions, API contracts, data model, auth middleware and current tests before implementing.
2. Specify the endpoint or event contract: actors, request/response schema, status/error codes, idempotency and pagination where needed.
3. Enforce validation, authorization and ownership on the server; do not trust client-provided role or scope values.
4. Place business rules in a testable domain/service layer; keep transport handlers thin and errors consistent.
5. Define timeouts, bounded retries and circuit-breaker behavior for external dependencies; avoid retrying non-idempotent operations blindly.
6. Coordinate transaction boundaries and invariants with database-transaction-integrity; consider version/rollback compatibility.
7. Add unit + integration + negative tests for normal and failure behavior. Verify observability without leaking credentials or personal data.
8. Document compatibility impacts and migration/flag requirements before release.

Output: contract, touched components, behavior changes, verification evidence, security/reliability risks.
Do not perform production writes or expose credentials while debugging.
