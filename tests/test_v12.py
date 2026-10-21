"""Archived v0.11 evidence integrity, no generated-code execution."""
from __future__ import annotations
import ast
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
V11=ROOT/"evals/v12"
V10=ROOT/"evals/v10"

class AdversarialRegressionEvidence(unittest.TestCase):
    def test_34_posthoc_cases_are_syntax_valid(self):
        path=V11/"additional_cases.py"
        tree=ast.parse(path.read_text(encoding="utf-8"))
        classes={node.name:sum(isinstance(item,ast.FunctionDef) and item.name.startswith("test_")
                               for item in node.body)
                 for node in tree.body if isinstance(node,ast.ClassDef)}
        self.assertEqual(classes,{"BookingAdversarial":11,"PortalAdversarial":12,"QueueAdversarial":11})
    def test_authentic_original_run_archive_still_present(self):
        data=json.loads((V10/"patch_scores.json").read_text(encoding="utf-8"))
        self.assertEqual(data["status"],"ALL_NINE_GRADED")
        self.assertEqual(data["by_arm"]["baseline"]["passed"],60)
        self.assertEqual(data["by_arm"]["active_control"]["passed"],59)
        self.assertEqual(data["by_arm"]["candidate"]["passed"],60)
    def test_authoritative_posthoc_scoring(self):
        x=json.loads((V11/"posthoc_scores_v2.json").read_text(encoding="utf-8"))
        self.assertEqual(x["status"],"ALL_9_SCORED")
        self.assertEqual(x["study"],"POST_HOC_DIAGNOSTIC_NOT_BLINDED")
        self.assertEqual(x["new_model_calls"],0)
        self.assertEqual(len(x["rows"]),9)
        for arm in ("baseline","active_control","candidate"):
            self.assertEqual(x["by_arm"][arm],{"passed":34,"total":34})
        self.assertTrue(all(row["state"]=="TESTED" for row in x["rows"]))
    def test_first_run_is_filed_as_invalid_not_a_model_failure(self):
        bad=json.loads((V11/"posthoc_scores.json").read_text(encoding="utf-8"))
        self.assertEqual(bad["status"],"PARTIAL")
        self.assertTrue(all(r["state"]=="PARSE_ERROR" for r in bad["rows"]))
        self.assertTrue(all(r["total"]==0 for r in bad["rows"]))
    def test_skill_text_not_modified_by_evaluation(self):
        self.assertEqual(len(list((ROOT/"skills").glob("*/SKILL.md"))),29)
        self.assertEqual(len(list((ROOT/"web-kit/cards").glob("*.md"))),29)

if __name__=="__main__":unittest.main()
