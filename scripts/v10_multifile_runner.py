#!/usr/bin/env python3
"""Three-arm Codex edit trial against copied multi-file fictional projects.

9 workspaces, max 2 concurrent. Does not touch production apps or canonical
skills. No hidden tests in agent workspaces. Generic control matches candidate
with o200k_base PROXY tokens, which is not Terra's attested tokenizer.
"""
from __future__ import annotations
import concurrent.futures as futures
import hashlib
import importlib.util
import json
import random
import shutil
import subprocess
import sys
import threading
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import v09_prompts as p09
BASE=ROOT/"evals/v10"
TEMPLATES=BASE/"templates"
WORK=BASE/"workspaces"
RUNS=BASE/"runs"
LOG=BASE/"run_journal.jsonl"
LOCK=threading.Lock()
ARM=("baseline","active_control","candidate")
SKILLS={"BOOK":"database-transaction-integrity",
        "AUTH":"security-authorization-auditor",
        "QUEUE":"backend-debugging"}
TASKS={
"BOOK":"""Repair booking/service.py and booking/queries.py and any supporting files necessary for atomic in-memory booking operations. MemoryDB stores bookings, slot_index, receipts and outbox; db.lock is an RLock.
reserve(tenant,slot,owner,request_key,amount_minor): nonempty string identifiers, positive integer amount but NOT bool. One booking ID tenant:slot per tenant and slot. Repeat the EXACT same (tenant,slot,owner,request_key,amount) request returns a copy of existing record; conflicting caller or amount must raise ValueError without mutations. Different tenants may reserve the same slot. Reservation and index update must be protected by one lock to avoid concurrent duplicates.
confirm(tenant,booking_id,receipt,amount_minor,verified): require verified is LITERAL True, nonempty receipt and matching tenant, amount and booking; mismatches and reused receipt for another booking raise ValueError with no state changes. A cross-tenant attempt must raise PermissionError. First success sets PAID, receipt, receipts[receipt]=booking_id and EXACTLY one payment_confirmed outbox entry, returns "APPLIED". Identical replay returns "REPLAY" without changing the outbox. Different receipt after payment is rejected. All related writes protected by one lock.
get_booking(db,tenant,booking_id): raises PermissionError if booking belongs to other tenant, returns a defensive copy for own tenant, None if missing. list_bookings(db,tenant): tenant-filtered list of defensive copies. Never expose a mutable underlying dictionary or leak another tenant's bookings. Keep the four-module API stable; do not rewrite tests or use external dependencies.""",
"AUTH":"""Fix portal/policy.py and portal/handlers.py (and other existing modules if necessary). The trusted actor is a dict with EXACT keys id, tenant, role; nonempty string values, role one of student/parent/teacher/admin. Each report is a dict with fields id, tenant, student_id, guardian_ids (list of actor IDs), teacher_ids (list of actor IDs), score.
read_report(store,actor,report_id): raise KeyError if missing, PermissionError if malformed actor, cross-tenant or not authorized; allow same-tenant student for own student_id, parent if actor id in guardian_ids, teacher if actor id in teacher_ids, admin if same tenant. Return a defensive copy.
delete_report: ONLY same-tenant admin may delete. Unauthorized raises PermissionError without mutations. Successful deletion returns True, removes report and appends EXACTLY one audit event with action=delete and report_id; second delete raises KeyError and must not duplicate audit.
export_reports: ONLY validated admin. Return only same-tenant reports, each as a defensive copy; no other role may export. Keep function signatures stable. No external dependencies, no HTTP server, no accounts or actual student records. Preserve other tenants' data under all denial paths.""",
"QUEUE":"""Repair notifier/worker.py, notifier/store.py and notifier/metrics.py as necessary. Jobs dict stores id, state (PENDING/RUNNING/SENT/DEAD), attempts int, worker, lease_until; store.lock is an RLock and store.receipts maps unique provider receipt to job ID.
claim(store,now,worker,lease_seconds=30): validate nonempty worker, positive integer lease_seconds excluding bool. Acquire store.lock; deterministically choose lexicographically first eligible job (PENDING or expired RUNNING with now >= lease_until), NEVER an active leased or SENT/DEAD job. Increment attempts exactly once and assign worker/state RUNNING/lease_until now+lease_seconds. Jobs already at >=3 attempts become DEAD when discovered expired; do not claim them. Return a defensive copy or None if none eligible. Prevent two workers claiming the same job simultaneously.
ack(store,job_id,worker,receipt,verified): require literal True and nonempty receipt, reject malformed/unclaimed job with ValueError, wrong worker with PermissionError. Claim owner's RUNNING job transitions to SENT, registers unique receipt, returns "APPLIED". Identical same-job receipt replay on SENT returns "REPLAY" without mutation. Reject different receipt on SENT and receipt already assigned to another job with ValueError and zero side effects.
fail(store,job_id,worker): only current worker of RUNNING job may fail; wrong worker raises PermissionError. Return True; if attempts >=3 mark DEAD, else PENDING and release worker/lease. counts(store) returns exact PENDING/RUNNING/SENT/DEAD counts. All state transitions lock-protected. No actual SMS or network, and do not modify or remove tests."""
}
HEADER="""You are repairing a three-or-four-file fictional Python project in the CURRENT working directory, not writing just an explanation. Inspect only this working folder, edit the module source files in place, and preserve module/function interfaces. You MAY run local offline Python syntax/smoke checks on this fictional code. Do not browse or call network, inspect other user repositories, access credentials, modify outside the current working directory, or change test/evaluation results. All data are synthetic. End with a concise list of files edited and any checks actually run. If an action was not run, say so.

"""
GENERIC=("Analyze the project files and user request precisely. Make sure the requested behavior is reflected in code, not only explanations. "
 "Consider interfaces, consistency between files, expected behavior on unusual inputs, repeatability, testability, and whether proposed changes introduce regressions. "
 "Do not invent results of tools or validations. Prefer simple, maintainable logic. After editing, compare what you changed against the requested behaviors. "
 "Use clear error handling and align with existing interfaces. Avoid unsupported guarantees and provide a short relevant handoff. ")
def sha(data):return hashlib.sha256(data).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def count(text):return p09.token_count(text)
def prompt(task,arm):
    base=HEADER+f"PROJECT TASK {task}:\n"+TASKS[task]
    if arm=="baseline":return base
    if arm=="candidate":
        skill=(ROOT/"skills"/SKILLS[task]/"SKILL.md").read_text(encoding="utf-8-sig")
        return HEADER+"SPECIALIST GUIDANCE:\n"+skill+"\n\n"+f"PROJECT TASK {task}:\n"+TASKS[task]
    if arm=="active_control":
        target=count(prompt(task,"candidate"))
        start=HEADER+"GENERAL DOMAIN-NEUTRAL REVIEW GUIDANCE:\n"
        end="\n\n"+f"PROJECT TASK {task}:\n"+TASKS[task]
        output=start
        while count(output+GENERIC+end)<=target-4:
            output+=GENERIC
        for piece in ("."," Check."," Review."," Note."," a"," b"," c"," ok"," 1"," 2"," 3"," "):
            while count(output+piece+end)<=target:
                if count(output+piece+end)==count(output+end):break
                output+=piece
        diff=target-count(output+end)
        if diff>1:raise RuntimeError(f"Token balancing mismatch {task}: {diff}")
        return output+end
    raise ValueError("Invalid arm")
def prepare():
    if WORK.exists():raise FileExistsError("No overwrite of existing v10 workspaces")
    WORK.mkdir(parents=True)
    RUNS.mkdir(exist_ok=True)
    for task in SKILLS:
        for arm in ARM:
            shutil.copytree(TEMPLATES/task,WORK/f"{task}-{arm}")
def read_done():
    done={}
    if not LOG.exists():return done
    for line in LOG.read_text(encoding="utf-8").splitlines():
        try:
            rec=json.loads(line)
            if rec["status"]=="COMPLETED" and (ROOT/rec["file"]).is_file():
                f=ROOT/rec["file"]
                if sha(f.read_bytes())==rec["output_sha256"]:
                    done[(rec["case"],rec["arm"])]=rec
        except (KeyError,ValueError,OSError):pass
    return done
def run_one(task,arm):
    workspace=WORK/f"{task}-{arm}"
    outfile=RUNS/f"{task}-{arm}.txt"
    if outfile.exists():
        return {"case":task,"arm":arm,"status":"PRESERVED_EXISTING"}
    question=prompt(task,arm)
    command=["codex","exec","--skip-git-repo-check","-m","gpt-5.6-terra",
             "--ephemeral","--ignore-user-config","-s","workspace-write",
             "-C",str(workspace),"-o",str(outfile),"-"]
    began=now()
    try:
        result=subprocess.run(command,input=question,encoding="utf-8",
                              text=True,capture_output=True,timeout=220)
        status="COMPLETED" if result.returncode==0 and outfile.exists() and outfile.stat().st_size>60 else "FAILED"
        tail=result.stderr[-200:]
        rc=result.returncode
    except subprocess.TimeoutExpired:
        status="TIMEOUT";tail="220s timeout";rc=None
    rec={"case":task,"arm":arm,"status":status,"started":began,"ended":now(),
         "model":"gpt-5.6-terra","sandbox":"workspace-write in synthetic isolated case",
         "file":outfile.relative_to(ROOT).as_posix(),
         "output_sha256":sha(outfile.read_bytes()) if outfile.exists() else None,
         "prompt_sha256":sha(question.encode("utf-8")),"proxy_tokens":count(question),
         "returncode":rc,"stderr_tail":tail,
         "changed_code_not_yet_scored":True}
    with LOCK:
        with LOG.open("a",encoding="utf-8",newline="\n") as f:
            f.write(json.dumps(rec,ensure_ascii=False)+"\n")
        print("DONE",task,arm,status,"tokens",rec["proxy_tokens"],"rc",rc,flush=True)
    return rec
def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--init",action="store_true")
    p.add_argument("--max-new",type=int,default=9)
    args=p.parse_args()
    if args.init:prepare()
    for task in SKILLS:
        a=count(prompt(task,"candidate"));b=count(prompt(task,"active_control"))
        print("BALANCE",task,a,b,flush=True)
        if abs(a-b)>1:raise ValueError("Unmatched proxy token lengths")
    tasks=[(t,a) for t in SKILLS for a in ARM]
    random.Random("v10-fixed-order-20261021").shuffle(tasks)
    done=read_done()
    pending=[x for x in tasks if x not in done and not (RUNS/f"{x[0]}-{x[1]}.txt").exists()]
    with futures.ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(lambda x:run_one(*x),pending[:args.max_new]))
    final=read_done()
    print(json.dumps({"status":"COMPLETE" if len(final)==9 else "PARTIAL",
                      "verified_models":len(final),"expected":9,
                      "new_calls":len(results)},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
