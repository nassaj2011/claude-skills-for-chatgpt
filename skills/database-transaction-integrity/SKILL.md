---
name: database-transaction-integrity
description: Safeguard SQL schemas, transactions, migrations, concurrent updates, payments, event consistency and audit ledgers. Use for persistent-state changes.
---

# Database and transactional integrity

1. Read the actual database dialect, schema, migrations, data access layer and callers. Never assume ORM definitions exactly match deployed schema.
2. Define business invariants: uniqueness, legal state transitions, ownership, referential integrity, monetary precision and conservation.
3. Model adversarial timing: duplicate requests, simultaneous updates, callback replay, out-of-order events, crash before/after commit and partial failures.
4. Choose enforcement layers: database UNIQUE/CHECK/FK, atomic conditional writes, locks, isolation, idempotency keys and durable outbox where warranted.
5. For money, use explicit minor units/precision, immutable or traceable ledger entries and a reconciliation strategy; prohibit silent balancing adjustments.
6. For migrations, detail expand/backfill/validate/contract, mixed-version compatibility, index/lock cost and rollback limitations.
7. Add concurrency and failure-injection tests plus queries that detect invariant violations; distinguish dry-run from production execution.
8. Gate risky migrations on verified backups, privileges, monitoring and an approved rollback strategy.

Output: invariant table (rule, enforcement, test), race/failure matrix, migration sequence and safe/conditional/blocked verdict.
Never run destructive SQL on production without explicit permission.
