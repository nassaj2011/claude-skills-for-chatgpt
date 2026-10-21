"""Post-hoc adversarial follow-up on v10 archival model code.

Exploratory checks: separately label changed/strengthened expectations, not
part of the preregistered 60-case trial. No real user data.
"""
import unittest
import os
TASK=os.environ.get("SKILL_EVAL_TASK")
@unittest.skipUnless(TASK=="BOOK","other")
class BookingMutation(unittest.TestCase):
 def setUp(self):
  from booking.data import MemoryDB
  from booking.service import BookingService
  self.db=MemoryDB();self.s=BookingService(self.db)
 def test_receipt_replay_requires_verification(self):
  b=self.s.reserve("t","slot","u","k",100)
  self.s.confirm("t",b["id"],"receipt",100,True)
  with self.assertRaises(ValueError):self.s.confirm("t",b["id"],"receipt",100,False)
 def test_reserve_result_is_not_internal(self):
  x=self.s.reserve("t","slot","u","k",100)
  x["owner"]="mal"
  self.assertEqual(self.db.bookings[x["id"]]["owner"],"u")
 def test_payment_amount_not_bool(self):
  b=self.s.reserve("t","slot","u","k",100)
  with self.assertRaises(ValueError):self.s.confirm("t",b["id"],"receipt",True,True)
 def test_receipt_index_consistency(self):
  b=self.s.reserve("t","slot","u","k",100)
  self.s.confirm("t",b["id"],"receipt",100,True)
  self.assertEqual(self.db.receipts["receipt"],b["id"])
@unittest.skipUnless(TASK=="AUTH","other")
class AuthMutation(unittest.TestCase):
 def setUp(self):
  from portal.store import PortalStore
  self.s=PortalStore()
  self.s.reports={"r":{"id":"r","tenant":"t","student_id":"s",
     "guardian_ids":["p"],"teacher_ids":["teacher"],"score":10}}
  self.actor={"id":"admin","tenant":"t","role":"admin"}
 def test_read_nested_list_defensive_copy(self):
  from portal.handlers import read_report
  read_report(self.s,self.actor,"r")["guardian_ids"].append("attacker")
  self.assertEqual(self.s.reports["r"]["guardian_ids"],["p"])
 def test_export_nested_list_defensive_copy(self):
  from portal.handlers import export_reports
  export_reports(self.s,self.actor)[0]["teacher_ids"].append("attacker")
  self.assertEqual(self.s.reports["r"]["teacher_ids"],["teacher"])
 def test_cross_tenant_no_side_effect(self):
  from portal.handlers import delete_report
  bad={"id":"admin2","tenant":"other","role":"admin"}
  with self.assertRaises(PermissionError):delete_report(self.s,bad,"r")
  self.assertIn("r",self.s.reports);self.assertEqual(self.s.audit,[])
 def test_unknown_role_fails_closed(self):
  from portal.handlers import read_report
  bad={"id":"admin","tenant":"t","role":"owner"}
  with self.assertRaises(PermissionError):read_report(self.s,bad,"r")
@unittest.skipUnless(TASK=="QUEUE","other")
class QueueMutation(unittest.TestCase):
 def setUp(self):
  from notifier.store import QueueStore
  self.s=QueueStore()
  self.s.jobs={"j":{"id":"j","state":"PENDING","attempts":0,"worker":None,"lease_until":None}}
 def test_verified_ack_no_double_receipt(self):
  from notifier.worker import claim,ack
  claim(self.s,10,"w")
  self.assertEqual(ack(self.s,"j","w","r",True),"APPLIED")
  self.assertEqual(ack(self.s,"j","w","r",True),"REPLAY")
  self.assertEqual(self.s.receipts,{"r":"j"})
 def test_lease_boundary(self):
  from notifier.worker import claim
  claim(self.s,10,"w",lease_seconds=30)
  self.assertIsNone(claim(self.s,39,"another"))
  self.assertEqual(claim(self.s,40,"another")["worker"],"another")
 def test_no_replay_without_verification(self):
  from notifier.worker import claim,ack
  claim(self.s,10,"w");ack(self.s,"j","w","r",True)
  with self.assertRaises(ValueError):ack(self.s,"j","w","r",False)
 def test_claim_result_not_internal(self):
  from notifier.worker import claim
  result=claim(self.s,10,"w")
  result["attempts"]=999
  self.assertEqual(self.s.jobs["j"]["attempts"],1)
if __name__=="__main__":unittest.main()
