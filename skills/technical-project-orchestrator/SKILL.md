---
name: technical-project-orchestrator
description: Coordinate multi-stage product delivery from agreed requirements to PRs and releases with critical paths, scoped Codex tasks and evidence-based status.
---

# Technical project orchestration
1. Read task context, live repository issues/PRs and established ADRs. Keep confirmed facts distinct from remembered plans.
2. Define outcome, non-scope, acceptance gates, constraints, available owners and release environment.
3. Build a dependency graph from product scope to design, data, backend, frontend, QA, deployment and operations; minimize circular handoffs.
4. Split work into small executable tasks with IDs, paths, inputs, deliverables, dependencies, review owner and clear stop conditions.
5. Trigger companion skills only for material issues: architecture, DB integrity, security, UX, testing, deployment, observability.
6. Track status as PLANNED, READY, IN PROGRESS, BLOCKED, TESTED, RELEASED or DONE, with evidence. Code merged is not synonymous with deployed.
7. Protect ongoing user work: no unapproved destructive cleanup, environment changes, production writes or spurious repo cloning.

Output: critical path, task queue, dependency blockers, acceptance gates, evidence references and next actions.
Do not invent work progress or substitute planning for execution.
