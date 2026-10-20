# Offline availability and latency release gate

This is a small, executable, standard-library **offline** sample. It is not a full observability backend or live SLO monitor. It demonstrates evidence-based gate decisions, explicit thresholds, deterministic p95 calculation and avoiding PII in metrics.

```bash
python examples/observability-gate/gate.py --sample examples/observability-gate/sample.jsonl
python -m unittest discover -s examples/observability-gate -p "test_*.py" -v
```

The sample is **synthetic** and should never be described as measured production performance. A green gate does not automatically authorize a deployment. Real production SLOs need service-level definitions, telemetry pipelines, high-cardinality controls, sampling considerations, burn-rate alerts, on-call routing and review of personal data exposure.

Related: `observability-monitoring`, `performance-accessibility`, `qa-release-gatekeeper`, `qa-test-strategy`, `devops-ci-cd`.
