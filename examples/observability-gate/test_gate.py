import importlib.util
import sys
import unittest
from pathlib import Path

source = Path(__file__).resolve().parent / "gate.py"
spec = importlib.util.spec_from_file_location("observability_gate", source)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class GateTests(unittest.TestCase):
    def test_good_synthetic_sample(self):
        events = [{"status": 200, "latency_ms": v} for v in range(50, 150)]
        report = mod.evaluate(events)
        self.assertEqual(report["decision"], "PASS")
        self.assertEqual(report["p95_ms"], 144)

    def test_error_budget_exceeded(self):
        events = [{"status": 200, "latency_ms": 100} for _ in range(98)]
        events += [{"status": 500, "latency_ms": 100} for _ in range(2)]
        self.assertEqual(mod.evaluate(events)["decision"], "BLOCK")

    def test_latency_budget_exceeded(self):
        events = [{"status": 200, "latency_ms": 100}] * 9 + [{"status": 200, "latency_ms": 900}]
        self.assertEqual(mod.evaluate(events, max_p95_ms=200)["decision"], "BLOCK")

    def test_reject_sensitive_fields(self):
        with self.assertRaisesRegex(ValueError, "sensitive"):
            mod.evaluate([{"status": 200, "latency_ms": 100, "email": "a@example.test"}])

    def test_missing_events_fail_closed(self):
        with self.assertRaises(ValueError):
            mod.evaluate([])

    def test_nan_latency_denied(self):
        with self.assertRaises(ValueError):
            mod.evaluate([{"status": 200, "latency_ms": float("nan")}])


if __name__ == "__main__":
    unittest.main()
