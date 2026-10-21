"""Supplementary post-hoc diagnostic regressions for v0.10 fictional modules.

Authored AFTER previous results; not preregistered or genuinely blinded.
Run only on the archived synthetic multi-file projects, not real user systems.
"""
import concurrent.futures
import copy
import os
import threading
import unittest

TASK=os.environ.get("SKILL_EVAL_TASK","")

@unittest.skipUnless(TASK=="BOOK","other project")
class BookingAdversarial(unittest.TestCase):
    def setUp(self):
        from booking.data import MemoryDB
        from booking.service import BookingService
        self.db=MemoryDB();self.s=BookingService(self.db)
    def reserve(self,**kw):
        v={"tenant":"t","slot":"s","owner":"alice","request_key":"k","amount_minor":100}
        v.update(kw)
        return self.s.reserve(**v)
    def test_owner_required_and_is_string(self):
        for bad in ("",None,0):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):self.reserve(owner=bad)
        self.assertFalse(self.db.bookings)
    def test_request_key_required(self):
        for bad in ("",None,False):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):self.reserve(request_key=bad)
    def test_slot_required(self):
        for bad in ("",None,0):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):self.reserve(slot=bad)
    def test_same_request_retry_after_payment(self):
        x=self.reserve()
        self.s.confirm("t",x["id"],"rec1",100,True)
        y=self.reserve()
        self.assertEqual(y["state"],"PAID")
        self.assertEqual(len(self.db.bookings),1)
        self.assertEqual(len(self.db.outbox),1)
    def test_simultaneous_same_request(self):
        go=threading.Barrier(10)
        def work(_):
            go.wait(timeout=5)
            return self.reserve()
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as p:
            outcomes=list(p.map(work,range(10)))
        self.assertEqual(len(outcomes),10)
        self.assertEqual(len(self.db.bookings),1)
        self.assertTrue(all(x["id"]=="t:s" for x in outcomes))
    def test_simultaneous_receipt_replay(self):
        x=self.reserve();go=threading.Barrier(8)
        def work(_):
            go.wait(timeout=5)
            return self.s.confirm("t",x["id"],"same",100,True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            outcomes=list(pool.map(work,range(8)))
        self.assertEqual(outcomes.count("APPLIED"),1)
        self.assertEqual(outcomes.count("REPLAY"),7)
        self.assertEqual(len(self.db.outbox),1)
        self.assertEqual(len(self.db.receipts),1)
    def test_simultaneous_distinct_receipts(self):
        x=self.reserve();go=threading.Barrier(6)
        def work(i):
            go.wait(timeout=5)
            try:return self.s.confirm("t",x["id"],"r"+str(i),100,True)
            except ValueError:return "REJECTED"
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            outcomes=list(pool.map(work,range(6)))
        self.assertEqual(outcomes.count("APPLIED"),1)
        self.assertEqual(outcomes.count("REJECTED"),5)
        self.assertEqual(len(self.db.outbox),1)
        self.assertEqual(len(self.db.receipts),1)
    def test_invalid_receipt_type_no_mutation(self):
        x=self.reserve()
        for receipt in ("",None,0):
            with self.subTest(receipt=receipt):
                with self.assertRaises(ValueError):
                    self.s.confirm("t",x["id"],receipt,100,True)
        self.assertEqual(self.db.bookings[x["id"]]["state"],"PENDING")
    def test_provider_verified_bool_only(self):
        x=self.reserve()
        with self.assertRaises(ValueError):
            self.s.confirm("t",x["id"],"rec",100,1)
        self.assertEqual(self.db.bookings[x["id"]]["state"],"PENDING")
    def test_missing_booking_returns_none(self):
        from booking.queries import get_booking
        self.assertIsNone(get_booking(self.db,"t","missing"))
    def test_defensive_paid_replay_return(self):
        x=self.reserve()
        self.s.confirm("t",x["id"],"rec",100,True)
        y=self.reserve();y["owner"]="changed";y["receipt"]="fake"
        self.assertEqual(self.db.bookings[x["id"]]["owner"],"alice")
        self.assertEqual(self.db.bookings[x["id"]]["receipt"],"rec")

@unittest.skipUnless(TASK=="AUTH","other project")
class PortalAdversarial(unittest.TestCase):
    def setUp(self):
        from portal.store import PortalStore
        self.db=PortalStore()
        self.db.reports={
            "a":{"id":"a","tenant":"t1","student_id":"s1",
                 "guardian_ids":["p1"],"teacher_ids":["teach1"],"score":75},
            "b":{"id":"b","tenant":"t1","student_id":"s2",
                 "guardian_ids":["p2"],"teacher_ids":["teach2"],"score":85},
            "c":{"id":"c","tenant":"t2","student_id":"s3",
                 "guardian_ids":["p1"],"teacher_ids":["teach1"],"score":95}}
        self.admin={"id":"admin","tenant":"t1","role":"admin"}
    def actor(self,who,role="admin",tenant="t1"):
        return {"id":who,"role":role,"tenant":tenant}
    def test_reject_actor_missing_field(self):
        from portal.handlers import read_report
        for field in ("id","role","tenant"):
            data=dict(self.admin);data.pop(field)
            with self.subTest(field=field):
                with self.assertRaises(PermissionError):read_report(self.db,data,"a")
    def test_reject_actor_non_dict(self):
        from portal.handlers import export_reports
        for data in (None,[],"admin"):
            with self.subTest(actor=str(data)):
                with self.assertRaises(PermissionError):export_reports(self.db,data)
    def test_reject_actor_non_string_value(self):
        from portal.handlers import read_report
        for field,value in (("id",0),("tenant",0),("role",True)):
            data=dict(self.admin);data[field]=value
            with self.subTest(field=field):
                with self.assertRaises(PermissionError):read_report(self.db,data,"a")
    def test_parent_not_entitled_to_sibling(self):
        from portal.handlers import read_report
        with self.assertRaises(PermissionError):
            read_report(self.db,self.actor("p1","parent"),"b")
    def test_teacher_not_entitled_other_assigned(self):
        from portal.handlers import read_report
        with self.assertRaises(PermissionError):
            read_report(self.db,self.actor("teach1","teacher"),"b")
    def test_foreign_tenant_in_membership_still_denied(self):
        from portal.handlers import read_report
        with self.assertRaises(PermissionError):
            read_report(self.db,self.actor("p1","parent"),"c")
    def test_read_nested_fields_are_defensive(self):
        from portal.handlers import read_report
        row=read_report(self.db,self.admin,"a")
        row["guardian_ids"].append("attacker")
        row["teacher_ids"].append("attacker")
        self.assertEqual(self.db.reports["a"]["guardian_ids"],["p1"])
        self.assertEqual(self.db.reports["a"]["teacher_ids"],["teach1"])
    def test_export_nested_fields_are_defensive(self):
        from portal.handlers import export_reports
        rows=export_reports(self.db,self.admin)
        rows[0]["guardian_ids"].append("attacker")
        self.assertEqual(self.db.reports["a"]["guardian_ids"],["p1"])
    def test_non_admin_export_cannot_leak_even_one(self):
        from portal.handlers import export_reports
        for actor in (self.actor("s1","student"),self.actor("p1","parent"),self.actor("teach1","teacher")):
            with self.subTest(role=actor["role"]):
                with self.assertRaises(PermissionError):export_reports(self.db,actor)
    def test_admin_delete_not_other_tenant(self):
        from portal.handlers import delete_report
        with self.assertRaises(PermissionError):delete_report(self.db,self.admin,"c")
        self.assertEqual(self.db.audit,[])
        self.assertIn("c",self.db.reports)
    def test_missing_report_no_audit(self):
        from portal.handlers import delete_report
        with self.assertRaises(KeyError):delete_report(self.db,self.admin,"missing")
        self.assertEqual(self.db.audit,[])
    def test_admin_actor_dict_unmodified(self):
        from portal.handlers import read_report,export_reports,delete_report
        a=copy.deepcopy(self.admin)
        read_report(self.db,a,"a")
        export_reports(self.db,a)
        delete_report(self.db,a,"b")
        self.assertEqual(a,self.admin)

@unittest.skipUnless(TASK=="QUEUE","other project")
class QueueAdversarial(unittest.TestCase):
    def setUp(self):
        from notifier.store import QueueStore
        self.db=QueueStore()
        self.db.jobs={
            "a":{"id":"a","state":"PENDING","attempts":0,"worker":None,"lease_until":None},
            "b":{"id":"b","state":"PENDING","attempts":0,"worker":None,"lease_until":None}}
    def claim(self,**kwargs):
        from notifier.worker import claim
        v={"now":10,"worker":"w1","lease_seconds":20};v.update(kwargs)
        return claim(self.db,**v)
    def test_invalid_lease_cases(self):
        for lease in (0,-1,True,1.5,None):
            with self.subTest(lease=lease):
                with self.assertRaises(ValueError):self.claim(lease_seconds=lease)
        self.assertEqual(self.db.jobs["a"]["attempts"],0)
    def test_invalid_worker_cases(self):
        for worker in ("",None,0):
            with self.subTest(worker=worker):
                with self.assertRaises(ValueError):self.claim(worker=worker)
    def test_at_lease_boundary_reclaim(self):
        self.claim()
        self.db.jobs.pop("b")
        res=self.claim(now=30,worker="w2")
        self.assertEqual((res["id"],res["attempts"]),("a",2))
    def test_parallel_more_workers_than_jobs(self):
        gate=threading.Barrier(12)
        def work(i):
            gate.wait(timeout=5)
            return self.claim(worker="w"+str(i))
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
            got=list(pool.map(work,range(12)))
        ids=[x["id"] for x in got if x is not None]
        self.assertEqual(sorted(ids),["a","b"])
    def test_ack_provider_verified_strict(self):
        from notifier.worker import ack
        self.claim()
        with self.assertRaises(ValueError):ack(self.db,"a","w1","r",1)
        self.assertEqual(self.db.jobs["a"]["state"],"RUNNING")
    def test_ack_receipt_nonempty_string(self):
        from notifier.worker import ack
        self.claim()
        for receipt in ("",None,0):
            with self.subTest(receipt=receipt):
                with self.assertRaises(ValueError):ack(self.db,"a","w1",receipt,True)
        self.assertFalse(self.db.receipts)
    def test_fail_unclaimed_cannot_change_state(self):
        from notifier.worker import fail
        with self.assertRaises((ValueError,PermissionError)):fail(self.db,"a","w1")
        self.assertEqual(self.db.jobs["a"]["state"],"PENDING")
    def test_fail_sent_cannot_change_state(self):
        from notifier.worker import ack,fail
        self.claim()
        ack(self.db,"a","w1","r1",True)
        with self.assertRaises((ValueError,PermissionError)):fail(self.db,"a","w1")
        self.assertEqual(self.db.jobs["a"]["state"],"SENT")
    def test_claim_no_jobs_returns_none(self):
        self.db.jobs.clear()
        self.assertIsNone(self.claim())
    def test_metrics_dead_and_sent(self):
        from notifier.worker import ack
        from notifier.metrics import counts
        self.claim()
        ack(self.db,"a","w1","r1",True)
        self.db.jobs["b"]["state"]="DEAD"
        self.assertEqual(counts(self.db),{"PENDING":0,"RUNNING":0,"SENT":1,"DEAD":1})
    def test_ack_unknown_job_rejects_without_receipt(self):
        from notifier.worker import ack
        with self.assertRaises((ValueError,KeyError,PermissionError)):
            ack(self.db,"missing","w1","r1",True)
        self.assertFalse(self.db.receipts)
