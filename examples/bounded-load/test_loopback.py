import importlib.util
import sys
import unittest
from pathlib import Path

DIR = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("bounded_load", DIR / "loopback_harness.py")
app = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = app
spec.loader.exec_module(app)


class BoundedLoadTests(unittest.TestCase):
    def test_actual_loopback_traffic_with_hard_caps(self):
        out = app.run(requests=12, workers=3)
        self.assertEqual(out["observed"], 12)
        self.assertEqual(out["requested"], 12)
        self.assertEqual(out["status"], "PASS")
        self.assertEqual(out["errors"], 0)
        self.assertGreater(out["achieved_rps"], 0)
        self.assertLessEqual(out["p50_ms"], out["p95_ms"])
        self.assertLessEqual(out["p95_ms"], out["p99_ms"])

    def test_reject_unbounded_request_count(self):
        with self.assertRaisesRegex(ValueError, "1..60"):
            app.run(requests=61)

    def test_reject_zero_workers(self):
        with self.assertRaises(ValueError):
            app.run(requests=1, workers=0)

    def test_reject_excessive_workers(self):
        with self.assertRaises(ValueError):
            app.run(requests=1, workers=7)

    def test_reject_excessive_timeout(self):
        with self.assertRaises(ValueError):
            app.run(requests=1, workers=1, timeout=30)

    def test_percentile_nearest_rank(self):
        self.assertEqual(app.percentile([1, 2, 3, 4, 5], 95), 5)
        self.assertEqual(app.percentile([1, 2, 3, 4, 5], 50), 3)

    def test_reject_empty_samples(self):
        with self.assertRaises(ValueError):
            app.percentile([], 95)


if __name__ == "__main__":
    unittest.main()
