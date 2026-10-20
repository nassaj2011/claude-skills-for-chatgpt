import importlib.util
import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("privacy_inventory_gate", HERE / "inventory_gate.py")
app = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = app
spec.loader.exec_module(app)


class PrivacyInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((HERE / "sample.json").read_text(encoding="utf-8"))

    def test_clean_fictional_inventory_passes(self):
        self.assertEqual(app.validate(self.data)["decision"], "PASS")

    def test_phone_must_not_reach_analytics(self):
        changed = copy.deepcopy(self.data)
        changed["fields"][0]["recipients"].append({"name": "analytics"})
        report = app.validate(changed)
        self.assertEqual(report["decision"], "BLOCK")
        self.assertIn("analytics-pii", [f["rule"] for f in report["findings"]])

    def test_extra_fields_at_messaging_vendor_blocked(self):
        changed = copy.deepcopy(self.data)
        changed["fields"][1]["recipients"].append({"name": "messaging"})
        self.assertIn("overdisclosure", [f["rule"] for f in app.validate(changed)["findings"]])

    def test_unknown_retention_cannot_pass(self):
        changed = copy.deepcopy(self.data)
        changed["fields"][0]["retention_trigger"] = "TBD"
        self.assertEqual(app.validate(changed)["decision"], "BLOCK")

    def test_pending_legal_review_is_not_compliance(self):
        changed = copy.deepcopy(self.data)
        changed["fields"][0]["legal_basis_review"] = "PENDING"
        self.assertEqual(app.validate(changed)["decision"], "REVIEW")

    def test_missing_role_cannot_pass(self):
        changed = copy.deepcopy(self.data)
        changed["fields"][0]["access_roles"] = []
        self.assertEqual(app.validate(changed)["decision"], "BLOCK")

    def test_duplicate_field_detected(self):
        changed = copy.deepcopy(self.data)
        changed["fields"].append(copy.deepcopy(changed["fields"][0]))
        self.assertIn("duplicate", [f["rule"] for f in app.validate(changed)["findings"]])


if __name__ == "__main__":
    unittest.main()
