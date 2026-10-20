# Platform delivery workflow

The lifecycle is not an inflexible sequence: choose only applicable skills. Every gate requires evidence.

| Gate | Questions | Skills | Deliverable |
| --- | --- | --- | --- |
| G0 Problem | Who has which problem and what proves it? | product-business-analyst | PRD draft, acceptance tests, MVP scope |
| G1 Design | How will this fit existing systems and trust boundaries? | software-architect, privacy-data-governance, security-authorization-auditor | ADR, interface contracts, risk register |
| G2 UX | Can each actor complete key flows in all states? | frontend-design-direction, theme-design-system, performance-accessibility | Screen/state inventory and verified UI |
| G3 Implementation | Do contracts and data invariants hold? | react-artifacts-builder, backend-api-engineer, database-transaction-integrity | Reviewed code and tests |
| G4 Integration | Are vendor calls least-privilege and reliable? | mcp-integration-builder, llm-api-integration | Contract tests, quota/error policy |
| G5 Verification | What actually passed, failed, or wasn't run? | qa-test-strategy, playwright-webapp-testing, backend-debugging | Evidence-based test matrix |
| G6 Release | Is this exact SHA safe to deploy and recover? | devops-ci-cd, qa-release-gatekeeper | GO / CONDITIONAL GO / NO-GO and rollout plan |
| G7 Operations | Can the team detect and recover from incidents? | observability-monitoring, documentation-handover | Metrics, alerts, runbooks |

## Handoff contract

At any boundary, pass:
- Objective and explicitly approved scope
- Current commit, environment and evidence links (when available)
- Inputs/contracts, acceptance criteria and non-goals
- Risks, dependencies, owner and decision needed
- Tests actually run versus tests merely proposed

## Evidence policy

- `PASS` only after execution with a traceable environment; `NOT RUN` is not `PASS`.
- Deployment or production write requires explicit authorization.
- No secret-bearing artifacts, customer data, or proprietary repository snippets in public issues.
- If a host lacks tools, keep the skill's guidance but clearly state the verification or execution limitation.

## Typical multi-skill combinations

- Booking/payment: product-business-analyst → software-architect → database-transaction-integrity → security-authorization-auditor → qa-test-strategy → qa-release-gatekeeper.
- New dashboard: product-business-analyst → frontend-design-direction → theme-design-system → react-artifacts-builder → playwright-webapp-testing → performance-accessibility.
- API integration: software-architect → mcp-integration-builder (if MCP is warranted) or backend-api-engineer → security-authorization-auditor → qa-test-strategy → observability-monitoring.
- Production bug: backend-debugging or playwright-webapp-testing → smallest repair → regression test → qa-release-gatekeeper.
