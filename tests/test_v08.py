"""Check 87 held-out scenarios and comparable prompt construction."""
from __future__ import annotations
import importlib.util
import json
import sys
import unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def module(name,file):
    s=importlib.util.spec_from_file_location(name,ROOT/"scripts"/file)
    m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
    return m
build=module("v08_prompt_maker","heldout_v08.py")
score=module("v08_code_score","score_code_v08.py")
class HeldOutBankTests(unittest.TestCase):
    def test_87_cases_three_per_skill(self):
        cases=build.load_cases()
        self.assertEqual(len(cases),87)
        self.assertEqual(len(Counter(c["skill"] for c in cases)),29)
        self.assertEqual(set(Counter(c["skill"] for c in cases).values()),{3})
        self.assertEqual(len(set(c["task"] for c in cases)),87)
    def test_three_arms_control_same_char_length(self):
        for code in ("H04-1","H14-1","H27-1"):
            p={arm:build.prompt(code,arm) for arm in ("baseline","active_control","candidate")}
            self.assertEqual(len(p["active_control"]),len(p["candidate"]))
            self.assertIn("SPECIALIST GUIDELINES",p["candidate"])
            self.assertNotIn("SPECIALIST GUIDELINES",p["active_control"])
            self.assertLess(len(p["baseline"]),len(p["candidate"]))
            self.assertIn("CODE EVALUATION CONTRACT",p["baseline"])
    def test_code_fixture_is_ready(self):
        self.assertEqual(set(score.CASES),{"H04-1","H14-1","H27-1"})
        for case in score.CASES.values():
            self.assertGreaterEqual(len(case["examples"]),10)
    def test_static_guard_rejects_unsafe_python(self):
        self.assertTrue(score.static_review("import os\ndef decide_reservation(a,b):pass","decide_reservation"))
        self.assertTrue(score.static_review("def assess_package(x):\n    open('secret')","assess_package"))
        self.assertFalse(score.static_review("def assess_package(x):\n    return {}","assess_package"))
    def test_not_claiming_87_completed(self):
        bank=json.loads((ROOT/"evals/v08/heldout_87.json").read_text(encoding="utf-8"))
        self.assertEqual(bank["status"],"DESIGNED_NOT_ALL_EXECUTED")
        self.assertTrue(all(c["state"]=="NOT_RUN" for c in bank["cases"]))
if __name__=="__main__":unittest.main()
