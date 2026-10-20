# Executable booking integrity reference (Python + SQLite)

A deliberately **small, fictional and non-production** booking domain for an isolated local test database. It demonstrates how `database-transaction-integrity`, `security-authorization-auditor`, `backend-api-engineer`, `qa-test-strategy`, `backend-debugging` and `qa-release-gatekeeper` can turn requirements into executable invariant tests.

## Local tests (zero third-party dependencies)

```bash
python -m unittest discover -s examples/reference-platform/tests -v
```

Nine regression cases exercise duplicate booking, six competing clients, request payload/idempotency collision, wrong-owner access, unverified/mismatched payment, replayed provider receipt, duplicate provider references and invalid actor/payload. All tests create disposable SQLite databases and **do not connect to production**.

## Scope and known gaps

- The `Actor` passed to domain methods is assumed to have been authenticated in an upstream trusted layer. This specimen contains **no session middleware or production user identity provider**.
- The keyword `verified=True` on `finalize()` is a **test seam**, not proof of provider authenticity. A real payment integration must independently check the provider signature, merchant account, currency, amount, callback timestamp and replay policy **before** calling this function.
- `UNIQUE(slot_id)` enforces at most one booking per slot forever; cancellation and rebooking would require a more nuanced partial uniqueness/state model for a real product.
- SQLite WAL is for local demonstration, not a substitute for PostgreSQL locking/isolation tests or operational backup policy.
- No HTTP API, authorization token, emails, PII, secrets, real payments or external network calls.

## Traceability

| Requirement | Enforced by | Test |
| --- | --- | --- |
| One reservation per slot | UNIQUE(slot_id), BEGIN IMMEDIATE | `test_concurrent_clients_produce_single_booking` |
| Same idempotency key means same payload | composite primary key plus payload check | `test_request_key_payload_collision_rejected` |
| Wrong owner cannot view/pay | owner predicates | `test_wrong_owner_cannot_pay_or_view` |
| One payment receipt for one booking | UNIQUE(provider_ref) and UNIQUE(booking_id) | `test_paid_replay_exact_once` |
| Atomic domain event recording | outbox write in same transaction | `test_paid_replay_exact_once` |

Do not use this educational module as a directly deployable payment/booking application.
