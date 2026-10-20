"""v0.7 six-specialist compatibility and immutable evidence checks."""
from __future__ import annotations
import importlib.util
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILLS={"llm-api-integration":"llm-contract",
        "mcp-integration-builder":"mcp-contract",
        "devops-ci-cd":"release-policy",
        "dependency-supply-chain-auditor":"supply-chain",
        "backup-disaster-recovery":"restore-drill",
        "performance-accessibility":"perf-budget"}
spec=importlib.util.spec_from_file_location("verify_v07",ROOT/"scripts/verify_v07_runs.py")
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
prep=importlib.util.spec_from_file_location("prepare_v07",ROOT/"scripts/prepare_v07.py")
pmod=importlib.util.module_from_spec(prep);sys.modules[prep.name]=pmod;prep.loader.exec_module(pmod)

class V07Tests(unittest.TestCase):
 def test_six_revised_specialist_skills_have_web_limits(self):
  for name in SKILLS:
   with self.subTest(skill=name):
    text=(ROOT/"skills"/name/"SKILL.md").read_text(encoding="utf-8")
    self.assertIn("ChatGPT",text)
    self.assertTrue("NOT RUN" in text or "does **not** start" in text)
    self.assertGreater(len(text),2100)
 def test_each_example_has_an_actual_test_and_caveats(self):
  for example in SKILLS.values():
   here=ROOT/"examples"/example
   self.assertTrue(here.is_dir(),example)
   self.assertTrue(any(here.glob("test_*.py")),example)
   self.assertIn("not", (here/"README.md").read_text(encoding="utf-8").lower())
 def test_frozen_six_case_rubric_no_scores(self):
  raw=json.loads((ROOT/"evals/v07-quality-benchmarks.json").read_text(encoding="utf-8"))
  self.assertEqual(len(raw["cases"]),6)
  self.assertEqual(raw["status"],"RAW_RUNS_COMPLETED_NOT_GRADED")
  for c in raw["cases"]:
   self.assertIsNone(c["score"])
   self.assertEqual(c["baseline"],"COMPLETED_UNSCORED")
   self.assertEqual(c["candidate"],"COMPLETED_UNSCORED")
   self.assertEqual(len(c["criteria"]),5)
   self.assertEqual(sum(a["weight"] for a in c["criteria"]),12)
 def test_all_12_raw_codex_outputs_integrity(self):
  count,issues=module.verify(ROOT)
  self.assertEqual(count,6)
  self.assertEqual(issues,[])
 def test_candidate_starts_with_source_skill_text_baseline_does_not(self):
  data=json.loads((ROOT/"evals/v07-quality-benchmarks.json").read_text(encoding="utf-8"))
  for case in data["cases"]:
   baseline=pmod.build(case["id"],"baseline")
   candidate=pmod.build(case["id"],"candidate")
   self.assertIn(case["prompt"],baseline)
   self.assertIn(case["prompt"],candidate)
   self.assertNotIn("SPECIALIST WORKFLOW GUIDANCE",baseline)
   self.assertIn("SPECIALIST WORKFLOW GUIDANCE",candidate)
 def test_rebuilt_web_cards_contain_updated_skill(self):
  for name in SKILLS:
   raw=(ROOT/"skills"/name/"SKILL.md").read_text(encoding="utf-8")
   web=(ROOT/"web-kit/cards"/(name+".md")).read_text(encoding="utf-8")
   significant=raw.split("---",2)[-1].strip()
   self.assertIn(significant[:140],web)

if __name__=="__main__":unittest.main()
