---
name: observability-monitoring
description: Plan product telemetry, health checks, logs, metrics, traces, SLOs and incident response for live platforms.
---

# Observability and operations
1. Define user-critical outcomes and failure modes. Choose meaningful golden signals: latency, traffic, errors and saturation plus business integrity metrics.
2. Design structured logs with correlation IDs and appropriate privacy redaction. Distinguish debug logs from audit records.
3. Define metrics with stable labels/cardinality, units, sample rates, ownership, targets and alert thresholds justified by impact.
4. Add distributed tracing where cross-service latency/root-cause analysis warrants it; avoid tracing secrets or personal payloads.
5. Specify probes, dashboards, on-call runbooks, incident severity and escalation; route alerts to an accountable owner.
6. Define SLO/error budget for critical journeys when evidence supports a measurable target.
7. Verify alerts and recovery drills in a safe environment, then capture gaps and rollback triggers.

Output: telemetry contract, dashboard panels, alerts, runbook, test evidence and costs.
Do not claim monitoring is operational merely because instrumentation code exists.
