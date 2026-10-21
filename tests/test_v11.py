"""Read-only check of v0.11 stored, explicitly post-hoc follow-up evidence."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class V11(unittest.TestCase):
 def test_12_exploratory_cases_run_on_nine_archived_workspaces(self):
  data=json.loads((ROOT/"evals/v11_followup_scores.json").read_text(encoding="utf-8"))
  self.assertEqual(data["state"],"EXPLORATORY_POST_HOC")
  self.assertTrue(data["original_v10_scores_unchanged"])
  self.assertEqual(len(data["rows"]),9)
  self.assertEqual(data["total_distinct_test_methods"],12)
  self.assertEqual({(r["case"],r["arm"]) for r in data["rows"]},
   {(c,a) for c in ("BOOK","AUTH","QUEUE") for a in ("baseline","active_control","candidate")})
  for row in data["rows"]:
   self.assertEqual(row["state"],"TESTED")
   self.assertEqual((row["passed"],row["total"]),(4,4))
 def test_v10_original_scores_still_unchanged(self):
  original=json.loads((ROOT/"evals/v10/patch_scores.json").read_text(encoding="utf-8"))
  self.assertEqual({a:d["passed"] for a,d in original["by_arm"].items()},
                   {"baseline":60,"active_control":59,"candidate":60})
 def test_documented_not_native_codex(self):
  report=(ROOT/"evals/V0_11_HOST_AND_FOLLOWUP.md").read_text(encoding="utf-8")
  self.assertIn("NOT RUN",report)
  self.assertIn("post-hoc",report)
  self.assertTrue((ROOT/"evals/v11_adversarial_regression.py").is_file())
if __name__=="__main__":unittest.main()
