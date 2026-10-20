import importlib.util,sys,unittest
from pathlib import Path
p=Path(__file__).resolve().parent/"browser_budget.py"
s=importlib.util.spec_from_file_location("perf_budget",p);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
def metric():return dict(nodes=20,resources=2,horizontal_overflow=0,js_errors=0,external_requests=0)
class PerfBudgetTests(unittest.TestCase):
 def test_small_local_fixture_accepted(self):self.assertEqual(m.assess(metric())["status"],"PASS_LOCAL_BROWSER_BUDGET")
 def test_dom_budget_exceeded(self):
  self.assertIn("DOM_NODE_BUDGET",m.assess(dict(metric(),nodes=100))["failed"])
 def test_resource_budget_exceeded(self):
  self.assertIn("RESOURCE_COUNT_BUDGET",m.assess(dict(metric(),resources=20))["failed"])
 def test_horizontal_overflow_blocked(self):
  self.assertIn("MOBILE_HORIZONTAL_OVERFLOW",m.assess(dict(metric(),horizontal_overflow=5))["failed"])
 def test_external_requests_blocked(self):
  self.assertIn("UNEXPECTED_EXTERNAL_TRAFFIC",m.assess(dict(metric(),external_requests=1))["failed"])
 def test_invalid_metrics_not_valid_evidence(self):
  with self.assertRaises(ValueError):m.assess(dict(metric(),nodes=None))
if __name__=="__main__":unittest.main()
