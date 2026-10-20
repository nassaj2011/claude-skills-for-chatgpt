---
name: documentation-handover
description: Create maintainable project documentation, ADR indexes, operator runbooks, release notes and contributor onboarding matched to actual code.
---

# Documentation and handover
1. Establish audience: developer, QA, operator, stakeholder or end user. Match granularity and language to the task.
2. Inspect code and existing docs before asserting endpoints, commands, versions or environment details.
3. Keep a single source of truth; link to authoritative contracts and avoid duplicating volatile secrets/config.
4. Document setup, local validation, architecture boundaries, task flows, known risks, recovery and owner escalation as applicable.
5. Use runnable examples with safe placeholders; test commands when feasible and label untested steps.
6. Document breaking changes, migration sequence and version-dependent behavior in release notes.
7. Provide maintenance ownership and a review trigger when underlying code changes.

Output: updated docs, evidence references, audience assumptions, tested examples and unresolved accuracy checks.
Avoid publishing internal URLs, keys, customer data, or project-specific proprietary material.
