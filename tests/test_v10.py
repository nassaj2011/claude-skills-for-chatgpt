"""Read-only verification of archived 29-skill coverage and nine v10 model outputs.

Never executes model-written Python in CI. Hidden fixture grading was run
separately on disposable fictional workspaces.
"""
from __future__ import annotations
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"evals/v10"
CASES=("BOOK","AUTH","QUEUE")
ARMS=("baseline","active_control","candidate")
EXPECTED={"baseline":(60,60),"active_control":(59,60),"candidate":(60,60)}

class MultiFileEvidence(unittest.TestCase):
    def test_all_29_have_only_structural_certification(self):
        data=json.loads((BASE/"skill_coverage_29.json").read_text(encoding="utf-8"))
        self.assertEqual(data["total"],29)
        self.assertEqual(len(data["skills"]),29)
        self.assertEqual(data["all_skill_real_world_quality_pass"],"NOT ESTABLISHED")
        self.assertTrue(all(x["fully_verified_real_world_skill"]=="NO" for x in data["skills"]))
    def test_9_text_only_archive_sha256(self):
        rows=[json.loads(s) for s in (BASE/"patch_journal.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
        good={}
        for row in rows:
            if row["status"]!="COMPLETE":continue
            key=(row["case"],row["arm"])
            self.assertNotIn(key,good)
            self.assertEqual(row["sandbox"],"read-only; no Code Mode host needed")
            p=ROOT/row["file"]
            self.assertTrue(p.is_file())
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),row["response_sha256"])
            good[key]=row
        self.assertEqual(set(good),{(case,arm) for case in CASES for arm in ARMS})
        for case in CASES:
            self.assertEqual(good[(case,"active_control")]["proxy_tokens"],
                             good[(case,"candidate")]["proxy_tokens"])
    def test_scored_fixture_results_no_exaggeration(self):
        result=json.loads((BASE/"patch_scores.json").read_text(encoding="utf-8"))
        self.assertEqual(result["status"],"ALL_NINE_GRADED")
        self.assertEqual(len(result["rows"]),9)
        for arm,(passed,total) in EXPECTED.items():
            self.assertEqual((result["by_arm"][arm]["passed"],result["by_arm"][arm]["total"]),
                             (passed,total))
        self.assertTrue(all(x["state"]=="TESTED" for x in result["rows"]))
    def test_three_isolated_scaffolds(self):
        for task in CASES:
            self.assertTrue((BASE/"templates"/task/"README.md").is_file())
        self.assertTrue((BASE/"hidden_integration.py").is_file())
    def test_original_nine_host_failed_are_not_coded_as_success(self):
        result=json.loads((BASE/"integration_scores.json").read_text(encoding="utf-8"))
        self.assertEqual(result["status"],"PARTIAL")
        self.assertTrue(any(x["state"]=="REJECTED_STATIC" for x in result["rows"]))

if __name__=="__main__":unittest.main()
