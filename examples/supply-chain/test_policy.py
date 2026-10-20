import copy,importlib.util,json,sys,unittest
from pathlib import Path
here=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location("dependency_policy",here/"policy.py")
m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
class SupplyPolicyTests(unittest.TestCase):
 @classmethod
 def setUpClass(c):c.data=json.loads((here/"sample.json").read_text(encoding="utf-8"))
 def test_pinned_example(self):self.assertEqual(m.review(self.data)["decision"],"PASS_STATIC_METADATA")
 def test_version_range_flagged(self):
  x=copy.deepcopy(self.data);x["packages"][0]["version"]="^1.2"
  self.assertEqual(m.review(x)["decision"],"REVIEW")
 def test_unverified_external_source_flagged(self):
  x=copy.deepcopy(self.data);x["packages"][0]["source"]="git+https://invalid.local/dependency"
  self.assertEqual(m.review(x)["decision"],"REVIEW")
 def test_missing_integrity_flagged(self):
  x=copy.deepcopy(self.data);x["packages"][0]["integrity"]=""
  self.assertEqual(m.review(x)["decision"],"REVIEW")
 def test_install_time_side_effects_flagged(self):
  x=copy.deepcopy(self.data);x["packages"][0]["install_scripts"]=True
  self.assertEqual(m.review(x)["decision"],"REVIEW")
 def test_license_review_needed(self):
  x=copy.deepcopy(self.data);x["packages"][0]["license"]=""
  self.assertEqual(m.review(x)["decision"],"REVIEW")
 def test_malformed_metadata_rejected(self):
  with self.assertRaises(ValueError):m.review({"packages":[{"name":"only"}]})
if __name__=="__main__":unittest.main()
