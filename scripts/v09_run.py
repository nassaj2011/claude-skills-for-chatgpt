#!/usr/bin/env python3
"""Bounded resumable 3-arm repeated evaluation: 3 cases x 3 arms x 2 repeats.

Two concurrent Codex read-only jobs max; no real repo access by model; no
overwrites or background promises. Failures stay in JSONL, never hidden.
"""
from __future__ import annotations
import argparse
import concurrent.futures as cf
import hashlib
import json
import random
import re
import shutil
import subprocess
import sys
import threading
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import v09_prompts as pm
EVAL=ROOT/"evals/v09"
RUNS=EVAL/"runs"
LOG=EVAL/"run_journal.jsonl"
LOCK=threading.Lock()
ISOLATED=ROOT.parent/"_ClaudeSkillsEvalV09Isolated"
ARMS=("baseline","active_control","candidate")
CASES=("P01","P02","P03")

def hash_bytes(data):return hashlib.sha256(data).hexdigest()
def utc():return datetime.now(timezone.utc).isoformat()
def get_previous():
    valid={}
    if not LOG.exists():return valid
    for line in LOG.read_text(encoding="utf-8").splitlines():
        try:
            row=json.loads(line)
            if row.get("status")!="COMPLETED":continue
            path=ROOT/row["file"]
            if path.is_file() and hash_bytes(path.read_bytes())==row.get("sha256"):
                valid[(row["case"],row["arm"],row["repeat"])]=row
        except (OSError,ValueError,KeyError):continue
    return valid

def call(job,model,timeout):
    case,arm,rep=job
    path=RUNS/f"{case}-{arm}-r{rep}.txt"
    if path.exists():
        return {"case":case,"arm":arm,"repeat":rep,"status":"PRESERVED_EXISTING_NO_RETRY"}
    text=pm.prompt(case,arm)
    before=utc()
    cmd=["codex","exec","--skip-git-repo-check","-m",model,"--ephemeral",
         "--ignore-user-config","-s","read-only","-C",str(ISOLATED),
         "-o",str(path),"-"]
    try:
        proc=subprocess.run(cmd,input=text,text=True,encoding="utf-8",
                            capture_output=True,timeout=timeout)
        status="COMPLETED" if proc.returncode==0 and path.exists() and path.stat().st_size>100 else "FAILED"
        error=proc.stderr[-300:]
        rc=proc.returncode
        ids=re.findall(r"(?:session id|session_id):\s*([0-9a-f-]{30,40})",proc.stderr,re.I)
    except subprocess.TimeoutExpired:
        status="TIMEOUT";error=f"timeout {timeout}s";rc=None;ids=[]
    result={"case":case,"arm":arm,"repeat":rep,"status":status,"model":model,
            "prompt_sha256":hash_bytes(text.encode("utf-8")),
            "proxy_tokens":pm.token_count(text),
            "proxy_tokenizer":"o200k_base","started":before,"ended":utc(),
            "file":path.relative_to(ROOT).as_posix(),
            "sha256":hash_bytes(path.read_bytes()) if path.exists() else None,
            "bytes":path.stat().st_size if path.exists() else 0,
            "session_id":ids[-1] if ids else None,
            "return_code":rc,"stderr_tail":error}
    with LOCK:
        with LOG.open("a",encoding="utf-8",newline="\n") as f:f.write(json.dumps(result,ensure_ascii=False)+"\n")
        print(json.dumps({k:result[k] for k in ("case","arm","repeat","status","bytes","proxy_tokens")}),flush=True)
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model",default="gpt-5.6-terra")
    ap.add_argument("--workers",type=int,default=2)
    ap.add_argument("--max-new",type=int,default=18)
    ap.add_argument("--timeout",type=int,default=220)
    a=ap.parse_args()
    if not 1<=a.workers<=2 or not 0<=a.max_new<=18 or not 30<=a.timeout<=400:
        ap.error("Bounded workers, calls or timeout exceeded")
    RUNS.mkdir(exist_ok=True)
    ISOLATED.mkdir(exist_ok=True)
    if not shutil.which("codex"):ap.error("Codex unavailable")
    for case in CASES:
        assert abs(pm.token_count(pm.prompt(case,"candidate"))-pm.token_count(pm.prompt(case,"active_control")))<=1
    jobs=[(case,arm,rep) for rep in (1,2) for case in CASES for arm in ARMS]
    random.Random("v09-fixed-20261021").shuffle(jobs)
    valid=get_previous()
    pending=[]
    for job in jobs:
        if job in valid:print("SKIP_VERIFIED",job,flush=True)
        elif (RUNS/f"{job[0]}-{job[1]}-r{job[2]}.txt").exists():
            print("PRESERVE_UNVERIFIED",job,flush=True)
        else:pending.append(job)
    submitted=pending[:a.max_new]
    with cf.ThreadPoolExecutor(max_workers=a.workers) as pool:
        outcomes=list(pool.map(lambda x:call(x,a.model,a.timeout),submitted))
    post=get_previous()
    summary={"status":"COMPLETE" if len(post)==18 else "PARTIAL",
             "valid_outputs":len(post),"required":18,"new_calls":len(submitted),
             "failures":sum(x["status"]!="COMPLETED" for x in outcomes),
             "unstarted":len(pending)-len(submitted),"token_balance":"within 1 token o200k_base",
             "code_fixtures":"NOT_RUN"}
    print(json.dumps(summary,ensure_ascii=False),flush=True)
    return 0 if summary["status"]=="COMPLETE" else 2

if __name__=="__main__":raise SystemExit(main())
