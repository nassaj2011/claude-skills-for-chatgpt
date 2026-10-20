import importlib.util,sys,unittest
from pathlib import Path
f=Path(__file__).resolve().parent/"gate.py";s=importlib.util.spec_from_file_location("release_gate",f)
m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
def good():
 return dict(sha="abc1234",environment="staging",checks={k:"PASS" for k in m.CRITICAL},
             migration="PREFLIGHT_PASS",restore_drill=True,approved=True)
class ReleasePolicyTests(unittest.TestCase):
 def test_all_required_proven(self):
  self.assertEqual(m.decide(good())["verdict"],"ELIGIBLE_FOR_HUMAN_DECISION")
 def test_skipped_auth_blocks(self):
  e=good();e["checks"]["authorization"]="SKIPPED";self.assertEqual(m.decide(e)["verdict"],"NO_GO")
 def test_missing_staging_smoke_blocks(self):
  e=good();e["checks"]["staging_smoke"]="NOT_RUN";self.assertEqual(m.decide(e)["verdict"],"NO_GO")
 def test_unverified_migration_blocks(self):
  e=good();e["migration"]="NOT_RUN";self.assertIn("MIGRATION_NOT_VERIFIED",m.decide(e)["blockers"])
 def test_restore_unproved_blocks(self):
  e=good();e["restore_drill"]=False;self.assertIn("RESTORE_NOT_PROVEN",m.decide(e)["blockers"])
 def test_missing_approval_blocks(self):
  e=good();e["approved"]=False;self.assertIn("NO_ACCOUNTABLE_APPROVAL",m.decide(e)["blockers"])
 def test_unknown_status_rejected(self):
  e=good();e["checks"]["authorization"]="UNKNOWN"
  with self.assertRaises(ValueError):m.decide(e)
if __name__=="__main__":unittest.main()
