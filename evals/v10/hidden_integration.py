"""Independent fixed integration regressions for three fictional projects.

Never copy this file into an agent workspace. TASK env selects one test class.
"""
import copy
import concurrent.futures
import os
import threading
import unittest

TASK=os.environ.get("SKILL_EVAL_TASK","")
@unittest.skipUnless(TASK=="BOOK","not this project")
class BookingTests(unittest.TestCase):
    def setUp(self):
        from booking.data import MemoryDB
        from booking.service import BookingService
        self.db=MemoryDB();self.s=BookingService(self.db)
    def reserve(self,tenant="t1",slot="s1",owner="a",key="k",amount=100):
        return self.s.reserve(tenant,slot,owner,key,amount)
    def test_create(self):
        b=self.reserve();self.assertEqual(b["id"],"t1:s1");self.assertEqual(b["state"],"PENDING")
    def test_retry_booking(self):
        a=self.reserve();self.assertEqual(self.reserve(),a);self.assertEqual(len(self.db.bookings),1)
    def test_reject_conflicting_owner(self):
        self.reserve()
        with self.assertRaises(ValueError):self.reserve(owner="other",key="other")
    def test_reject_changed_amount(self):
        self.reserve()
        with self.assertRaises(ValueError):self.reserve(amount=101)
    def test_tenant_independence(self):
        self.reserve();self.reserve(tenant="t2")
        self.assertEqual(len(self.db.bookings),2)
    def test_reject_bool_amount(self):
        with self.assertRaises(ValueError):self.reserve(amount=True)
    def test_reject_bad_identifiers(self):
        for v in ("",None,0):
            with self.subTest(v=v):
                with self.assertRaises(ValueError):self.reserve(tenant=v)
    def test_reject_bad_amount(self):
        with self.assertRaises(ValueError):self.reserve(amount=-1)
    def test_threaded_conflict(self):
        gate=threading.Barrier(8)
        def work(n):
            gate.wait(timeout=4)
            try:self.reserve(owner=str(n),key="id"+str(n));return True
            except ValueError:return False
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            wins=list(pool.map(work,range(8)))
        self.assertEqual(sum(wins),1);self.assertEqual(len(self.db.bookings),1)
    def test_confirm_once(self):
        b=self.reserve()
        self.assertEqual(self.s.confirm("t1",b["id"],"r1",100,True),"APPLIED")
        self.assertEqual(len(self.db.outbox),1)
    def test_confirm_replay(self):
        b=self.reserve();self.s.confirm("t1",b["id"],"r1",100,True)
        self.assertEqual(self.s.confirm("t1",b["id"],"r1",100,True),"REPLAY")
        self.assertEqual(len(self.db.outbox),1)
    def test_unverified_no_side_effects(self):
        b=self.reserve()
        with self.assertRaises(ValueError):self.s.confirm("t1",b["id"],"r1",100,False)
        self.assertEqual(self.db.bookings[b["id"]]["state"],"PENDING")
        self.assertEqual(len(self.db.outbox),0)
    def test_amount_mismatch(self):
        b=self.reserve()
        with self.assertRaises(ValueError):self.s.confirm("t1",b["id"],"r1",99,True)
    def test_cross_tenant_payment(self):
        b=self.reserve()
        with self.assertRaises(PermissionError):self.s.confirm("t2",b["id"],"r1",100,True)
    def test_receipt_uniqueness(self):
        a=self.reserve();b=self.reserve(slot="s2",key="k2")
        self.s.confirm("t1",a["id"],"receipt",100,True)
        with self.assertRaises(ValueError):self.s.confirm("t1",b["id"],"receipt",100,True)
        self.assertEqual(self.db.bookings[b["id"]]["state"],"PENDING")
    def test_wrong_replay(self):
        b=self.reserve();self.s.confirm("t1",b["id"],"receipt",100,True)
        with self.assertRaises(ValueError):self.s.confirm("t1",b["id"],"new_receipt",100,True)
    def test_tenant_queries(self):
        from booking.queries import get_booking,list_bookings
        b=self.reserve();self.reserve(tenant="t2")
        with self.assertRaises(PermissionError):get_booking(self.db,"t2",b["id"])
        self.assertEqual(len(list_bookings(self.db,"t1")),1)
    def test_defensive_copy(self):
        from booking.queries import get_booking,list_bookings
        b=self.reserve()
        get_booking(self.db,"t1",b["id"])["owner"]="evil"
        list_bookings(self.db,"t1")[0]["owner"]="evil"
        self.assertEqual(self.db.bookings[b["id"]]["owner"],"a")

@unittest.skipUnless(TASK=="AUTH","not this project")
class AuthTests(unittest.TestCase):
    def setUp(self):
        from portal.store import PortalStore
        self.s=PortalStore()
        self.s.reports={"a":{"id":"a","tenant":"t1","student_id":"student1",
                  "guardian_ids":["parent1"],"teacher_ids":["teacher1"],"score":90},
                  "b":{"id":"b","tenant":"t2","student_id":"student2",
                  "guardian_ids":["parent2"],"teacher_ids":["teacher2"],"score":80}}
    def actor(self,who,role,tenant="t1"):
        return {"id":who,"tenant":tenant,"role":role}
    def read(self,actor,key="a"):
        from portal.handlers import read_report
        return read_report(self.s,actor,key)
    def delete(self,actor,key="a"):
        from portal.handlers import delete_report
        return delete_report(self.s,actor,key)
    def export(self,actor):
        from portal.handlers import export_reports
        return export_reports(self.s,actor)
    def test_students_own(self):self.assertEqual(self.read(self.actor("student1","student"))["score"],90)
    def test_guardian_child(self):self.assertEqual(self.read(self.actor("parent1","parent"))["score"],90)
    def test_teacher_assigned(self):self.assertEqual(self.read(self.actor("teacher1","teacher"))["score"],90)
    def test_admin_read(self):self.assertEqual(self.read(self.actor("admin","admin"))["score"],90)
    def test_student_cross_tenant(self):
        with self.assertRaises(PermissionError):self.read(self.actor("student1","student"),"b")
    def test_admin_cross_tenant(self):
        with self.assertRaises(PermissionError):self.read(self.actor("admin","admin"),"b")
    def test_teacher_unassigned(self):
        with self.assertRaises(PermissionError):self.read(self.actor("other","teacher"))
    def test_parent_other_child(self):
        with self.assertRaises(PermissionError):self.read(self.actor("other","parent"))
    def test_parent_delete_denied(self):
        with self.assertRaises(PermissionError):self.delete(self.actor("parent1","parent"))
        self.assertIn("a",self.s.reports)
    def test_teacher_delete_denied(self):
        with self.assertRaises(PermissionError):self.delete(self.actor("teacher1","teacher"))
    def test_student_delete_denied(self):
        with self.assertRaises(PermissionError):self.delete(self.actor("student1","student"))
    def test_admin_cross_tenant_delete(self):
        with self.assertRaises(PermissionError):self.delete(self.actor("admin","admin"),"b")
    def test_admin_delete(self):
        self.assertIs(self.delete(self.actor("admin","admin")),True)
        self.assertNotIn("a",self.s.reports)
        self.assertEqual(len(self.s.audit),1)
    def test_repeat_delete_audit(self):
        self.delete(self.actor("admin","admin"))
        with self.assertRaises(KeyError):self.delete(self.actor("admin","admin"))
        self.assertEqual(len(self.s.audit),1)
    def test_export_admin_scoped(self):
        self.assertEqual([r["id"] for r in self.export(self.actor("admin","admin"))],["a"])
    def test_export_student_denied(self):
        with self.assertRaises(PermissionError):self.export(self.actor("student1","student"))
    def test_export_teacher_denied(self):
        with self.assertRaises(PermissionError):self.export(self.actor("teacher1","teacher"))
    def test_mutation_of_read(self):
        self.read(self.actor("admin","admin"))["score"]=0
        self.assertEqual(self.s.reports["a"]["score"],90)
    def test_mutation_of_export(self):
        self.export(self.actor("admin","admin"))[0]["score"]=0
        self.assertEqual(self.s.reports["a"]["score"],90)
    def test_unknown_role(self):
        with self.assertRaises(PermissionError):self.read(self.actor("root","superuser"))
    def test_extra_actor_field(self):
        actor=self.actor("admin","admin");actor["role_override"]="admin"
        with self.assertRaises(PermissionError):self.read(actor)

@unittest.skipUnless(TASK=="QUEUE","not this project")
class QueueTests(unittest.TestCase):
    def setUp(self):
        from notifier.store import QueueStore
        self.s=QueueStore()
        self.s.jobs={"a":{"id":"a","state":"PENDING","attempts":0,"worker":None,"lease_until":None},
                     "b":{"id":"b","state":"PENDING","attempts":0,"worker":None,"lease_until":None}}
    def claim(self,now=10,worker="w1",lease_seconds=30):
        from notifier.worker import claim
        return claim(self.s,now,worker,lease_seconds)
    def ack(self,job="a",worker="w1",receipt="r1",verified=True):
        from notifier.worker import ack
        return ack(self.s,job,worker,receipt,verified)
    def fail(self,job="a",worker="w1"):
        from notifier.worker import fail
        return fail(self.s,job,worker)
    def test_claim_sorted(self):
        self.assertEqual(self.claim()["id"],"a")
    def test_attempt_increment(self):
        self.claim();self.assertEqual(self.s.jobs["a"]["attempts"],1)
    def test_skip_active_lease(self):
        self.claim();self.assertEqual(self.claim(15,"w2")["id"],"b")
    def test_expired_reclaim(self):
        self.claim();self.s.jobs.pop("b")
        x=self.claim(40,"w2")
        self.assertEqual((x["id"],x["attempts"]),("a",2))
    def test_parallel_unique(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            x=list(pool.map(lambda w:self.claim(worker=w),("w1","w2")))
        self.assertEqual({row["id"] for row in x},{"a","b"})
    def test_attempts_exhausted(self):
        x=self.s.jobs["a"];x.update(state="RUNNING",attempts=3,worker="w1",lease_until=10)
        self.s.jobs.pop("b")
        self.assertIsNone(self.claim(11,"w2"));self.assertEqual(x["state"],"DEAD")
    def test_sent_not_reclaimed(self):
        self.s.jobs["a"]["state"]="SENT"
        self.assertEqual(self.claim()["id"],"b")
    def test_bad_worker(self):
        with self.assertRaises(ValueError):self.claim(worker="")
    def test_bad_lease(self):
        with self.assertRaises(ValueError):self.claim(lease_seconds=True)
    def test_verified_ack(self):
        self.claim();self.assertEqual(self.ack(),"APPLIED")
        self.assertEqual(self.s.jobs["a"]["state"],"SENT")
    def test_ack_replay(self):
        self.claim();self.ack()
        self.assertEqual(self.ack(),"REPLAY");self.assertEqual(len(self.s.receipts),1)
    def test_unverified_no_side_effect(self):
        self.claim()
        with self.assertRaises(ValueError):self.ack(verified=False)
        self.assertEqual(self.s.jobs["a"]["state"],"RUNNING")
    def test_wrong_worker_ack(self):
        self.claim()
        with self.assertRaises(PermissionError):self.ack(worker="other")
    def test_duplicate_receipt_other_job(self):
        self.claim();self.claim(worker="w2");self.ack()
        with self.assertRaises(ValueError):self.ack(job="b",worker="w2")
        self.assertEqual(self.s.jobs["b"]["state"],"RUNNING")
    def test_ack_conflicting_receipt(self):
        self.claim();self.ack()
        with self.assertRaises(ValueError):self.ack(receipt="different")
    def test_fail_retry(self):
        self.claim();self.assertIs(self.fail(),True)
        self.assertEqual(self.s.jobs["a"]["state"],"PENDING")
    def test_fail_dead_at_cap(self):
        self.s.jobs["a"].update(state="RUNNING",attempts=3,worker="w1",lease_until=40)
        self.fail();self.assertEqual(self.s.jobs["a"]["state"],"DEAD")
    def test_fail_wrong_worker(self):
        self.claim()
        with self.assertRaises(PermissionError):self.fail(worker="other")
    def test_cannot_ack_unclaimed(self):
        with self.assertRaises(ValueError):self.ack()
    def test_metrics(self):
        from notifier.metrics import counts
        self.claim()
        self.assertEqual(counts(self.s),{"PENDING":1,"RUNNING":1,"SENT":0,"DEAD":0})
    def test_copy(self):
        x=self.claim();x["attempts"]=900
        self.assertEqual(self.s.jobs["a"]["attempts"],1)
if __name__=="__main__":unittest.main()
