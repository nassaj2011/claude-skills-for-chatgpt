#!/usr/bin/env python3
"""Resumable v0.8 Codex 3-arm pilot; fictional text-only code-generation prompts.

Never overwrites any existing output. No production writes or external accounts.
Does NOT execute model-written code; score_code_v08.py is a separate guarded step.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import random
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EVAL=ROOT/"evals/v08"
RUNS=EVAL/"runs"
JOURNAL=EVAL/"pilot_journal.jsonl"
VALID=("H04-1","H14-1","H27-1")
ARMS=("baseline","active_control","candidate")
def stamp():return datetime.now(timezone.utc).isoformat()
def sha(data):return hashlib.sha256(data).hexdigest()
def generator():
    path=ROOT/"scripts/heldout_v08.py"
    spec=importlib.util.spec_from_file_location("v08_prompts",path)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model",default="gpt-5.6-terra")
    parser.add_argument("--seed",default="v08-predeclared-01")
    parser.add_argument("--max-new",default=9,type=int)
    parser.add_argument("--timeout",default=240,type=int)
    a=parser.parse_args()
    if not 0<=a.max_new<=9 or not 30<=a.timeout<=600:parser.error("Invalid bounded run count/deadline")
    bank=json.loads((EVAL/"heldout_87.json").read_text(encoding="utf-8"))
    assert len(bank["cases"])==87 and len({case["skill"] for case in bank["cases"]})==29
    if a.max_new and not shutil.which("codex"):parser.error("Codex CLI not installed")
    prompt=generator().prompt
    RUNS.mkdir(parents=True,exist_ok=True)
    jobs=[(case,arm) for case in VALID for arm in ARMS]
    random.Random(a.seed).shuffle(jobs)
    verified=set()
    if JOURNAL.exists():
        for line in JOURNAL.read_text(encoding="utf-8").splitlines():
            try:
                v=json.loads(line);path=ROOT/v["output_path"]
                if (v.get("state")=="COMPLETE" and path.is_file()
                    and sha(path.read_bytes())==v["output_sha256"]):
                    verified.add((v["case"],v["arm"]))
            except (ValueError,KeyError,OSError):pass
    calls=0
    for case,arm in jobs:
        file=RUNS/f"{case}-{arm}.txt"
        if file.exists():
            print(("SKIP_VERIFIED" if (case,arm) in verified else "PRESERVE_UNVERIFIED_EXISTING"),case,arm,flush=True)
            continue
        if calls>=a.max_new:
            print("PENDING",case,arm,flush=True)
            continue
        calls+=1
        folder=ROOT.parent/"_ClaudeSkillsEvalV08Isolated"
        folder.mkdir(exist_ok=True)
        source=prompt(case,arm)
        command=["codex","exec","--skip-git-repo-check","-m",a.model,"--ephemeral","--ignore-user-config",
                 "-s","read-only","-C",str(folder),"-o",str(file),"-"]
        start=stamp()
        print("START",calls,"/",a.max_new,case,arm,flush=True)
        try:
            proc=subprocess.run(command,input=source,encoding="utf-8",
                                text=True,capture_output=True,timeout=a.timeout,check=False)
            rc=proc.returncode
            state="COMPLETE" if rc==0 and file.exists() and file.stat().st_size>80 else "FAILED"
            err=(proc.stderr or "")[-240:]
        except subprocess.TimeoutExpired:
            rc=None;state="TIMEOUT";err=f"Codex exceeded {a.timeout}s"
        record={"case":case,"arm":arm,"model":a.model,"state":state,
                "prompt_sha256":sha(source.encode("utf-8")),
                "started_utc":start,"ended_utc":stamp(),
                "output_path":file.relative_to(ROOT).as_posix(),
                "output_sha256":sha(file.read_bytes()) if file.is_file() else None,
                "output_bytes":file.stat().st_size if file.is_file() else 0,
                "returncode":rc,"stderr_tail":err,"executed_generated_code":False}
        with JOURNAL.open("a",encoding="utf-8",newline="\n") as handle:
            handle.write(json.dumps(record,ensure_ascii=False)+"\n")
        if state=="COMPLETE":verified.add((case,arm))
        print(json.dumps({"case":case,"arm":arm,"state":state,"bytes":record["output_bytes"]}),flush=True)
    summary={"state":"PILOT_GENERATION_COMPLETE" if len(verified)==9 else "PILOT_INCOMPLETE",
             "valid_outputs":len(verified),"planned":9,"new_calls":calls,
             "code_execution":"NOT_EXECUTED","journal":str(JOURNAL)}
    print(json.dumps(summary,ensure_ascii=False),flush=True)
    return 0 if len(verified)==9 else 2
if __name__=="__main__":raise SystemExit(main())
