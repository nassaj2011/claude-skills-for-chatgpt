---
name: security-authorization-auditor
description: Audit authentication, authorization, roles, object ownership, API defenses, secrets and abuse protections against the repository's actual implementation.
---

# Security and authorization auditing

1. Bound the review and identify actors, assets, trust boundaries, identity/session model and privileged operations.
2. Trace each selected route from authentication through policy checks, service logic and database filters.
3. Test for horizontal/vertical privilege escalation, broken object ownership, tenant leakage, mass assignment, TOCTOU and unauthenticated paths.
4. Check relevant threats: validation/injection, CSRF/CORS where applicable, rate limits, webhook authenticity, session invalidation, replay and sensitive logging.
5. Produce a permissions matrix (role × resource × action) and negative tests: wrong owner, wrong role, expired session, replay, missing credentials.
6. Grade findings by concrete likelihood and impact; distinguish confirmed findings, suspected risks and unreviewed surfaces.
7. Specify the smallest effective remedy and a regression test. Do not claim a penetration test when only static review occurred.

Output: evidence paths, threat scenario, severity, fix, test and residual risk.
Never reveal secrets, run unauthorized external scans, or change live credentials without approval.
