"""v0.9 evidence check: 3 hard tasks, 3 arms, 2 repeats each.

Offline, read-only. Does NOT execute any generated model-written code.
"""
from __future__ import annotations
import hashlib
import json
import unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EVAL=ROOT/"evals/v09"

class HardRepeatedEvaluationTests(unittest.TestCase):
    def test_three_harder_task_contracts(self):
        cases=json.loads((EVAL/"hard_cases.json").read_text(encoding="utf-8"))["cases"]
        self.assertEqual({c["id"] for c in cases},{"P01","P02","P03"})
        self.assertEqual(len({c["skill"] for c in cases}),3)
        self.assertTrue(all(len(c["contract"])>500 for c in cases))
    def test_oracle_has_many_negative_cases(self):
        cases=json.loads((EVAL/"oracle_fixtures.json").read_text(encoding="utf-8"))["cases"]
        self.assertEqual([len(x["tests"]) for x in cases],[23,25,27])
        self.assertEqual(sum(len(x["tests"]) for x in cases),75)
    def test_real_outputs_hashes_and_repeats(self):
        log=EVAL/"run_journal.jsonl"
        self.assertTrue(log.is_file())
        lines=[json.loads(x) for x in log.read_text(encoding="utf-8").splitlines() if x.strip()]
        complete={}
        for x in lines:
            if x.get("status")!="COMPLETED":continue
            path=ROOT/x["file"]
            self.assertTrue(path.is_file(),x["file"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),x["sha256"])
            key=(x["case"],x["arm"],x["repeat"])
            self.assertNotIn(key,complete)
            complete[key]=x
        expected={(case,arm,rep) for case in ("P01","P02","P03")
                  for arm in ("baseline","active_control","candidate") for rep in (1,2)}
        self.assertEqual(set(complete),expected)
        for case in ("P01","P02","P03"):
            for rep in (1,2):
                ctrl=complete[(case,"active_control",rep)]
                skill=complete[(case,"candidate",rep)]
                self.assertEqual(ctrl["proxy_tokens"],skill["proxy_tokens"])
                self.assertNotEqual(ctrl["prompt_sha256"],skill["prompt_sha256"])
    def test_persisted_grading_evidence(self):
        p=EVAL/"hard_pilot_scores.json"
        self.assertTrue(p.is_file())
        data=json.loads(p.read_text(encoding="utf-8"))
        self.assertEqual(data["status"],"ALL_18_SCORED")
        self.assertEqual(len(data["rows"]),18)
        self.assertEqual(sum(x["total"] for x in data["rows"]),450)
        self.assertTrue(all(x["passed"] is not None for x in data["rows"]))
    def test_old_skill_source_and_web_kit_not_modified(self):
        self.assertEqual(len(list((ROOT/"skills").glob("*/SKILL.md"))),29)
        self.assertEqual(len(list((ROOT/"web-kit/cards").glob("*.md"))),29)

if __name__=="__main__":unittest.main()
