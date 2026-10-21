#!/usr/bin/env python3
"""Resumable, host-independent three-arm multi-file code-generation trial.

Codex is READ-ONLY: source files are embedded in the prompt; model returns
a JSON mapping from relative path to full replacement source. A later,
separate deterministic program applies only allowlisted files to isolated
fixtures and executes held-out regressions. Does not use Codex tool host.
"""
from __future__ import annotations
import concurrent.futures as cf
import hashlib
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
import v10_multifile_runner as original
import v09_prompts as tokens
BASE=ROOT/"evals/v10"
ARCH=BASE/"runs_text_patch"
LOG=BASE/"patch_journal.jsonl"
LOCK=threading.Lock()
ALLOW={"BOOK":["booking/service.py","booking/queries.py"],
       "AUTH":["portal/policy.py","portal/handlers.py"],
       "QUEUE":["notifier/worker.py","notifier/metrics.py"]}
GENERIC=original.GENERIC
NOREPO=ROOT.parent/"_ClaudeSkillsEvalV10TextOnly"
def digest(x):return hashlib.sha256(x).hexdigest()
def utc():return datetime.now(timezone.utc).isoformat()
def base_prompt(task):
    files=original.DATA if False else None
    source=""
    root=BASE/"templates"/task
    for f in sorted(root.rglob("*.py")):
        source+=f"\n### FILE: {f.relative_to(root).as_posix()}\n"+f.read_text(encoding="utf-8")+"\n"
    return ("""FICTIONAL OFFLINE MULTI-FILE PYTHON REPAIR. DO NOT call tools,
read files, run commands, access the filesystem or external systems. ALL
source modules are provided in this prompt. Generate a complete replacement
for EXACTLY the two specified editable files. Response MUST be one valid JSON
object with single key "files" and a mapping of allowed relative file paths
to full replacement PYTHON SOURCE CODE STRINGS. Do NOT include Markdown,
explanation, tests, additional files or a patch/diff. Keep unchanged files
untouched. Use only Python standard library, and honor all negative cases.
No code executions or checks are claimed.

""" + f"REPLACE ONLY THESE TWO FILES: {', '.join(ALLOW[task])}\n\n"
 + f"REQUIREMENTS:\n{original.TASKS[task]}\n\nSOURCE FILES:\n{source}\n")
def make_prompt(task,arm):
    content=base_prompt(task)
    if arm=="baseline":return content
    if arm=="candidate":
        skill=(ROOT/"skills"/original.SKILLS[task]/"SKILL.md").read_text(encoding="utf-8-sig")
        return "SPECIALIST GUIDANCE:\n"+skill+"\n\n"+content
    if arm=="active_control":
        goal=tokens.token_count(make_prompt(task,"candidate"))
        out="GENERAL DOMAIN-NEUTRAL GUIDANCE:\n"
        while tokens.token_count(out+GENERIC+content)<=goal-5:
            out+=GENERIC
        for phrase in ("."," Check."," Review."," Done."," a"," b"," c"," yes"," ok"," "):
            while tokens.token_count(out+phrase+content)<=goal:
                if tokens.token_count(out+phrase+content)==tokens.token_count(out+content):break
                out+=phrase
        delta=goal-tokens.token_count(out+content)
        if delta>1:raise ValueError("Proxy mismatch "+task+" "+str(delta))
        return out+content
    raise ValueError("Invalid arm")
def run(job):
    case,arm=job
    dst=ARCH/f"{case}-{arm}.txt"
    if dst.exists():return {"case":case,"arm":arm,"state":"EXISTS_NOT_OVERWRITTEN"}
    prompt=make_prompt(case,arm)
    command=["codex","exec","--skip-git-repo-check","-m","gpt-5.6-terra",
             "--ephemeral","--ignore-user-config","-s","read-only",
             "-C",str(NOREPO),"-o",str(dst),"-"]
    begun=utc()
    try:
        p=subprocess.run(command,input=prompt,text=True,encoding="utf-8",
                         capture_output=True,timeout=250)
        status="COMPLETE" if p.returncode==0 and dst.is_file() and dst.stat().st_size>100 else "FAILED"
        err=p.stderr[-200:];rc=p.returncode
    except subprocess.TimeoutExpired:
        status="TIMEOUT";err="Codex 250s deadline";rc=None
    row={"case":case,"arm":arm,"status":status,"prompt_sha256":digest(prompt.encode("utf-8")),
         "response_sha256":digest(dst.read_bytes()) if dst.exists() else None,
         "file":dst.relative_to(ROOT).as_posix(),"proxy_tokens":tokens.token_count(prompt),
         "created":begun,"completed":utc(),"model":"gpt-5.6-terra",
         "sandbox":"read-only; no Code Mode host needed","returncode":rc,"stderr_tail":err}
    with LOCK:
        with LOG.open("a",encoding="utf-8",newline="\n") as f:f.write(json.dumps(row)+"\n")
        print("PATCH_RESPONSE",case,arm,status,"bytes",dst.stat().st_size if dst.exists() else 0,flush=True)
    return row
def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--max-new",type=int,default=9)
    args=p.parse_args()
    ARCH.mkdir(exist_ok=True)
    NOREPO.mkdir(exist_ok=True)
    for task in ALLOW:
        print("TOKENS",task,tokens.token_count(make_prompt(task,"active_control")),
              tokens.token_count(make_prompt(task,"candidate")),flush=True)
    jobs=[(task,arm) for task in ALLOW for arm in original.ARM]
    random.Random("v10-patch-preregistered-20261021").shuffle(jobs)
    pending=[job for job in jobs if not (ARCH/f"{job[0]}-{job[1]}.txt").exists()]
    with cf.ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(run,pending[:args.max_new]))
    print(json.dumps({"new_calls":len(results),
                      "complete":sum(x["status"]=="COMPLETE" for x in results),
                      "remaining":len(pending)-len(results)}),flush=True)
if __name__=="__main__":main()
