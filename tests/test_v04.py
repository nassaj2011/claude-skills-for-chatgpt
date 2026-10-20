"""v0.4 benchmark coverage and grounded A/B regression checks."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from prepare_benchmark import prepare
from validate_benchmark import validate
from evaluate_skills import compare, verify_run_artifact


class V04Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / "evals/29-skill-benchmark.json").read_text(encoding="utf-8"))

    def test_every_skill_has_one_case(self):
        count, errors = validate(ROOT / "skills", ROOT / "evals/29-skill-benchmark.json")
        self.assertEqual(count, 29)
        self.assertEqual(errors, [])

    def test_all_cases_are_marked_not_run(self):
        self.assertTrue(all(c["score"] is None and c["execution_status"] == "NOT_RUN"
                            for c in self.data["cases"]))

    def test_prompt_preparation_preserves_exact_task(self):
        for case in self.data["cases"]:
            baseline = prepare(self.data, ROOT / "skills", case["id"], "baseline")
            candidate = prepare(self.data, ROOT / "skills", case["id"], "candidate")
            self.assertIn(case["prompt"], baseline)
            self.assertIn(case["prompt"], candidate)
            self.assertNotIn("BENCHMARK SKILL INSTRUCTIONS", baseline)
            self.assertIn("BENCHMARK SKILL INSTRUCTIONS", candidate)
            self.assertGreater(len(candidate), len(baseline))

    def test_unknown_case_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown"):
            prepare(self.data, ROOT / "skills", "does-not-exist", "baseline")

    def test_real_benchmark_outputs_are_attached_and_consistent(self):
        for slug in ["db", "security"]:
            prefix = ROOT / "evals"
            rubric = json.loads((prefix / "benchmarks" / f"v04-{slug}-criteria.json").read_text(encoding="utf-8"))
            baseline = json.loads((prefix / "runs" / f"v04-{slug}-baseline.json").read_text(encoding="utf-8"))
            candidate = json.loads((prefix / "runs" / f"v04-{slug}-candidate.json").read_text(encoding="utf-8"))
            self.assertNotEqual(baseline["metadata"]["session_id"], candidate["metadata"]["session_id"])
            verify_run_artifact(baseline, ROOT)
            verify_run_artifact(candidate, ROOT)
            report = compare(rubric, baseline, candidate)
            self.assertEqual(report["evaluation_type"], "HUMAN_SCORED_AGENT_RUNS")
            self.assertGreaterEqual(report["candidate_score"], report["baseline_score"])

    def test_demo_scripts_exist_but_do_not_claim_production(self):
        paths = [
            "examples/reference-platform/booking.py",
            "examples/frontend-rtl/ui.mjs",
            "examples/observability-gate/gate.py",
        ]
        for rel in paths:
            self.assertTrue((ROOT / rel).is_file(), rel)
            readme = ROOT / Path(rel).parent / "README.md"
            self.assertTrue(readme.is_file(), rel)
            self.assertIn("not", readme.read_text(encoding="utf-8").lower())


if __name__ == "__main__":
    unittest.main()
