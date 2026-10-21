#!/usr/bin/env python3
"""Build three fictional multi-file regression projects; never touches real apps."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"evals/v10"
DATA={
"BOOK":{
"booking/__init__.py":"",
"booking/data.py":'''import threading

class MemoryDB:
    def __init__(self):
        self.lock = threading.RLock()
        self.bookings = {}
        self.slot_index = {}
        self.receipts = {}
        self.outbox = {}
''',
"booking/service.py":'''from .data import MemoryDB

class BookingService:
    def __init__(self, db):
        self.db = db

    def reserve(self, tenant, slot, owner, request_key, amount_minor):
        bid = tenant + ":" + slot
        if (tenant, slot) in self.db.slot_index:
            raise ValueError("slot already taken")
        record = {"id": bid, "tenant": tenant, "slot": slot,
                  "owner": owner, "request_key": request_key,
                  "amount_minor": amount_minor, "state": "PENDING", "receipt": None}
        self.db.bookings[bid] = record
        self.db.slot_index[(tenant, slot)] = bid
        return dict(record)

    def confirm(self, tenant, booking_id, receipt, amount_minor, verified):
        booking = self.db.bookings[booking_id]
        booking["state"] = "PAID"
        booking["receipt"] = receipt
        self.db.receipts[receipt] = booking_id
        event_id = str(len(self.db.outbox) + 1)
        self.db.outbox[event_id] = {"booking_id": booking_id, "kind": "payment_confirmed"}
        return "APPLIED"
''',
"booking/queries.py":'''def get_booking(db, tenant, booking_id):
    return db.bookings.get(booking_id)

def list_bookings(db, tenant):
    return list(db.bookings.values())
''',
"README.md":'''# Fictional booking and payment module
In-memory only, no actual payment provider, no customer data.
Fix the four module behaviors according to the evaluator task.
'''},
"AUTH":{
"portal/__init__.py":"",
"portal/store.py":'''class PortalStore:
    def __init__(self):
        self.reports = {}
        self.audit = []
''',
"portal/policy.py":'''def can_read(actor, report):
    return True

def can_delete(actor, report):
    return True

def can_export(actor):
    return True
''',
"portal/handlers.py":'''from .policy import can_read, can_delete, can_export

def read_report(store, actor, report_id):
    return store.reports[report_id]

def delete_report(store, actor, report_id):
    report = store.reports.pop(report_id)
    store.audit.append({"action": "delete", "report_id": report_id})
    return True

def export_reports(store, actor):
    return list(store.reports.values())
''',
"README.md":'''# Fictional student report API
No actual student information, accounts or live schools.
The store contains synthetic report objects only.
'''},
"QUEUE":{
"notifier/__init__.py":"",
"notifier/store.py":'''import threading

class QueueStore:
    def __init__(self):
        self.lock = threading.RLock()
        self.jobs = {}
        self.receipts = {}
''',
"notifier/worker.py":'''def claim(store, now, worker, lease_seconds=30):
    for job in store.jobs.values():
        if job["state"] != "SENT":
            job["state"] = "RUNNING"
            job["worker"] = worker
            job["lease_until"] = now + lease_seconds
            job["attempts"] += 1
            return dict(job)
    return None

def ack(store, job_id, worker, receipt, verified):
    job = store.jobs[job_id]
    job["state"] = "SENT"
    store.receipts[receipt] = job_id
    return "APPLIED"

def fail(store, job_id, worker):
    job = store.jobs[job_id]
    job["state"] = "PENDING"
    return True
''',
"notifier/metrics.py":'''def counts(store):
    return {"PENDING": sum(j["state"] == "PENDING" for j in store.jobs.values()),
            "RUNNING": sum(j["state"] == "RUNNING" for j in store.jobs.values()),
            "SENT": sum(j["state"] == "SENT" for j in store.jobs.values()),
            "DEAD": sum(j["state"] == "DEAD" for j in store.jobs.values())}
''',
"README.md":'''# Fictional notification state machine
No SMS, payment, customer records, network or external provider.
'''}
}

def main():
    BASE.mkdir(parents=True,exist_ok=True)
    root=BASE/"templates"
    if root.exists():raise FileExistsError("Template directory exists; never overwrite")
    for name,files in DATA.items():
        for rel,content in files.items():
            dst=root/name/rel
            dst.parent.mkdir(parents=True,exist_ok=True)
            dst.write_text(content,encoding="utf-8")
    print("SCAFFOLD_CREATED",len(DATA),"projects",sum(map(len,DATA.values())),"files")
if __name__=="__main__":main()
