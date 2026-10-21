#!/usr/bin/env python3
"""Post-hoc adversarial regression scoring of nine archived multi-file artifacts.

No new model calls. Never run on real customer data or general untrusted code.
Source files were synthetically generated and AST-checked; process isolation
is NOT a security sandbox. Never overwrite the original v0.10 scores.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import v10_grade as base
SOURCE=ROOT/"evals/v10"
HERE=ROOT/"evals/v12"
def digest(x):return hashlib.sha256(x).hexdigest()
def verify_archive():
    records=[json.loads(line) for line in (SOURCE/"patch_journal.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    valid={}
    for r in records:
        if r.get("status")!="COMPLETE":continue
        file=ROOT/r["file"]
        if file.is_file() and digest(file.read_bytes())==r["response_sha256"]:
            valid[(r["case"],r["arm"])]=r
    required={(c,a) for c in ("BOOK","AUTH","QUEUE") for a in ("baseline","active_control","candidate")}
    if set(valid)!=required:raise RuntimeError("Expected exactly nine intact previously archived Codex responses")
    return valid
def score(task,arm):
    folder=SOURCE/"patch_workspaces"/f"{task}-{arm}"
    problems=base.static_check(folder,task)
    if problems:return {"state":"STATIC_REJECTED","passed":0,"total":0,"issues":problems}
    with tempfile.TemporaryDirectory(prefix="v11_posthoc_") as tmp:
        p=Path(tmp)/"runner.py"
        p.write_text(base.WORKER,encoding="utf-8")
        try:
            import os
            env={"SKILL_EVAL_TASK":task,"PYTHONIOENCODING":"utf-8"}
            finished=subprocess.run([sys.executable,"-I","-S",str(p),
                            str(folder),str(HERE/"additional_cases.py")],
                            cwd=tmp,env=env,capture_output=True,text=True,encoding="utf-8",timeout=18)
        except subprocess.TimeoutExpired:
            return {"state":"TIMEOUT","passed":0,"total":0}
        if finished.returncode not in (0,1):
            return {"state":"RUNNER_ERROR","passed":0,"total":0,"error":finished.stderr[-350:]}
        try:data=json.loads(finished.stdout.strip())
        except ValueError:
            return {"state":"PARSE_ERROR","passed":0,"total":0,"stdout":finished.stdout[-200:],
                    "stderr":finished.stderr[-250:]}
        if data["total"]<10:return {"state":"INCOMPLETE","passed":0,"total":data["total"],"issues":data["details"]}
        return {"state":"TESTED",**data}
def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'posthoc_scores_v2.json')
    args=parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        parser.error('Output exists; refusing overwrite')
    if args.output.parent.resolve()!=HERE.resolve():
        parser.error('Write result only inside evals/v12')
    valid=verify_archive()
    rows=[]
    for task in ("BOOK","AUTH","QUEUE"):
        for arm in ("baseline","active_control","candidate"):
            result=score(task,arm)
            row={"task":task,"arm":arm,"response_sha256":valid[(task,arm)]["response_sha256"],**result}
            rows.append(row)
            print("TEST",task,arm,row["state"],row["passed"],"/",row["total"],flush=True)
    summary={}
    for arm in ("baseline","active_control","candidate"):
        subset=[r for r in rows if r["arm"]==arm]
        summary[arm]={"passed":sum(r["passed"] for r in subset),
                      "total":sum(r["total"] for r in subset)}
    result={"schema":1,"study":"POST_HOC_DIAGNOSTIC_NOT_BLINDED",
            "original_v10_model_calls":9,"new_model_calls":0,
            "warnings":["Tests written after model responses and cannot be claimed pre-registered",
                        "Static AST guard and subprocess are NOT hardened sandbox",
                        "No independent holdout scorer; no broad causal efficacy claim"],
            "status":"ALL_9_SCORED" if all(r["state"]=="TESTED" for r in rows) else "PARTIAL",
            "by_arm":summary,"rows":rows}
    target=args.output
    with target.open("x",encoding="utf-8") as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({"status":result["status"],"by_arm":summary},ensure_ascii=False))
if __name__=="__main__":main()
