---
name: qa-release-gatekeeper
description: Judge software release readiness from executed tests, change scope, migrations, security checks, incident risks and verified rollback.
---

# Release gatekeeping
1. Identify exact commit/PR set, release candidate, environment and impacted workflows. Inspect current evidence rather than relying on memory.
2. Define required gates proportionate to risks: unit, integration, E2E, authorization, migrations, concurrency, configuration, health and rollback.
3. For each gate mark PASS, FAIL, BLOCKED, NOT RUN or NOT APPLICABLE; include command, environment and timestamp when known.
4. Stop a release for unresolved high-impact data corruption, payment, security or unrecoverable migration risks.
5. Issue GO only with adequate real evidence. CONDITIONAL GO requires explicit accepted risks, accountable approver and mitigation. Otherwise NO-GO.
6. Plan smoke tests, post-deploy monitoring, incident contacts, halt thresholds and rollback criteria.
7. Never deploy, modify production, or mark a release complete without explicit authorization.

Output: GO/CONDITIONAL GO/NO-GO, exact SHA, evidence matrix, blockers, accepted risks, monitoring and rollback.
Missing evidence is NOT RUN, never PASS.
