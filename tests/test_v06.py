"""Version 0.6 skills: ensure evaluation integrity and delivery parity."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ("privacy-data-governance", "load-resilience-testing", "visual-assets-design")
PROMPTS = {
    "privacy": ROOT / "evals/prompts/v05-privacy.txt",
    "load": ROOT / "evals/prompts/v06-load.txt",
    "visual": ROOT / "evals/prompts/v06-visual.txt",
}


class V06QualityContracts(unittest.TestCase):
    def test_specialist_skills_require_actual_evidence(self):
        for name in TARGETS:
            with self.subTest(name=name):
                text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("ChatGPT web", text)
                self.assertIn("NOT RUN", text)
                self.assertIn("evidence", text.lower())
                self.assertGreater(len(text), 2500)

    def test_genuine_executable_examples_are_present(self):
        for rel in (
            "examples/privacy-inventory/inventory_gate.py",
            "examples/bounded-load/loopback_harness.py",
            "examples/visual-asset/asset_gate.py",
            "examples/visual-asset/booking-social.svg",
            "examples/visual-asset/rights.json",
        ):
            self.assertTrue((ROOT / rel).is_file(), rel)

    def test_model_experiment_rubrics_are_frozen_and_unscored(self):
        for kind, path in PROMPTS.items():
            self.assertTrue(path.is_file(), str(path))
            self.assertGreater(len(path.read_text(encoding="utf-8")), 200)
            rubric = json.loads((ROOT / "evals/benchmarks" / f"v06-{kind}-criteria.json").read_text(encoding="utf-8"))
            self.assertEqual(len(rubric["cases"]), 1)
            case = rubric["cases"][0]
            self.assertEqual(case["id"], "v06-" + kind)
            self.assertEqual(len(case["criteria"]), 5)
            self.assertEqual(sum(c["weight"] for c in case["criteria"]), 12)
            self.assertTrue(all(len(c["description"]) > 25 for c in case["criteria"]))

    def test_no_fabricated_v06_agent_results_committed(self):
        self.assertEqual(list((ROOT / "evals/runs").glob("v06-*.json")), [])
        self.assertEqual(list((ROOT / "evals/runs").glob("v06-*.txt")), [])

    def test_web_and_canonical_skill_text_remain_in_sync(self):
        for name in TARGETS:
            original = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            web = (ROOT / "web-kit/cards" / f"{name}.md").read_text(encoding="utf-8")
            heading = original.split("\n", 5)[-1]
            self.assertIn(heading[:70], web)


if __name__ == "__main__":
    unittest.main()
