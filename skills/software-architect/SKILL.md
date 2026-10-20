---
name: software-architect
description: Design or review software architecture, bounded contexts, dependencies, ADRs, failure modes and compatibility across services. Use for consequential system changes.
---

# Software architecture

1. Read the repository, ADRs and contracts before describing the current architecture. Label unknown areas; do not invent diagrams.
2. Identify functional needs and operational requirements: latency, availability, security, growth, auditability, recovery, localization and team capacity.
3. Draw logical boundaries, data ownership, sync/async interactions and failure containment. Preserve existing public contracts unless explicitly approved.
4. Consider 2-3 concrete alternatives only when a meaningful trade-off exists; compare complexity, operational cost, reversibility and migration risk.
5. Evaluate failure modes (timeouts, duplicate requests, partial writes, unhealthy dependencies) and what the system does during degradation.
6. Specify a proposed ADR: context, decision, rejected options, consequences, date and evidence.
7. Sequence rollout: compatibility, feature flags when useful, migration, tests, telemetry and rollback trigger.

Handoff: data changes to database-transaction-integrity; permissions to security-authorization-auditor; release risk to qa-release-gatekeeper.
Output: observed architecture, decision, affected contracts, proposed ADR, delivery slices and unanswered questions.
Never treat a speculative improvement as an authorized rewrite.
