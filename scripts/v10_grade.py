#!/usr/bin/env python3
"""Score archived multi-file Codex workspaces with isolated synthetic regressions.

Not an OS sandbox. The test process runs developer-authored synthetic fixture
code inside a temporary Python process; no real identities, payments or services.
Only files inside the v10 copied workspaces are inspected.
"""
from __future__ import annotations
import ast
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"evals/v10"
ALLOWED_ROOTS={"BOOK","AUTH","QUEUE"}
ALLOWED_IMPORTS={"threading","copy","booking","portal","notifier"}
WORKER = """import importlib.util,io,json,os,sys,unittest
from pathlib import Path
workspace=Path(sys.argv[1])
fixture=Path(sys.argv[2])
sys.path.insert(0,str(workspace))
spec=importlib.util.spec_from_file_location('hidden_v10',str(fixture))
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
suite=unittest.defaultTestLoader.loadTestsFromModule(module)
output=io.StringIO()
results=unittest.TextTestRunner(stream=output,verbosity=1).run(suite)
total=results.testsRun
skipped=len(results.skipped)
bad=len(results.failures)+len(results.errors)
print(json.dumps({'total':total-skipped,'passed':total-skipped-bad,
                  'failed':len(results.failures),'errors':len(results.errors),
                  'skipped_other_projects':skipped,
                  'failure_descriptions':[str(x[0]) for x in results.failures+results.errors][:8],
                  'details':output.getvalue()[-1700:]}))
"""
def checksum(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def static_check(root,task):
    anomalies=[]
    if root.is_symlink() or not root.is_dir():return ["Workspace unavailable"]
    for f in root.rglob("*"):
        if f.is_symlink():anomalies.append("Symlink not allowed: "+str(f));continue
        if not f.is_file():continue
        rel=f.relative_to(root).as_posix()
        if len(f.read_bytes())>40000:anomalies.append("Oversized file: "+rel)
        if f.suffix not in {".py",".md",".pyc"}:
            if "__pycache__" not in str(f):anomalies.append("Unexpected file type: "+rel)
            continue
        if f.suffix==".py":
            try:tree=ast.parse(f.read_text(encoding="utf-8-sig"))
            except Exception:
                anomalies.append("Cannot parse "+rel)
                continue
            for node in ast.walk(tree):
                if isinstance(node,(ast.Import,ast.ImportFrom)):
                    names=[x.name.split(".")[0] for x in node.names] if isinstance(node,ast.Import) else [(node.module or "").split(".")[0]]
                    if isinstance(node,ast.ImportFrom) and node.level>0:
                        names=[]
                    if any(x and x not in ALLOWED_IMPORTS for x in names):
                        anomalies.append("Unexpected import: "+rel+" "+str(names))
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in {"eval","exec","open","compile","__import__"}:
                    anomalies.append("Suspicious Python eval/io: "+rel)
    return anomalies
def run(task,arm,root_override=None):
    root=Path(root_override) if root_override is not None else BASE/"workspaces"/f"{task}-{arm}"
    checks=static_check(root,task)
    if checks:return {"state":"REJECTED_STATIC","passed":0,"total":0,"issues":checks[:12]}
    with tempfile.TemporaryDirectory(prefix="v10_hidden_grade_") as td:
        worker=Path(td)/"runner.py"
        worker.write_text(WORKER,encoding="utf-8")
        env={"PYTHONIOENCODING":"utf-8","SKILL_EVAL_TASK":task}
        try:
            done=subprocess.run([sys.executable,"-I","-S",str(worker),str(root),str(BASE/"hidden_integration.py")],
                                cwd=td,env=env,timeout=16,capture_output=True,text=True,encoding="utf-8")
        except subprocess.TimeoutExpired:
            return {"state":"TIMEOUT","passed":0,"total":0}
        if done.returncode not in (0,1):
            return {"state":"RUNNER_ERROR","passed":0,"total":0,"stderr":done.stderr[-300:]}
        try:obj=json.loads(done.stdout.strip())
        except ValueError:
            return {"state":"NOT_PARSED","passed":0,"total":0,"stderr":done.stderr[-300:],"stdout":done.stdout[-200:]}
        if obj["total"]<15:return {"state":"INCOMPLETE_TEST_SUITE",**obj}
        return {"state":"TESTED",**obj}
def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,default=BASE/"integration_scores.json")
    args=p.parse_args()
    if args.output.exists():p.error("Refusing overwrite of existing results")
    archive=BASE/"run_journal.jsonl"
    entries=[json.loads(x) for x in archive.read_text(encoding="utf-8").splitlines() if x.strip()]
    valid={}
    for item in entries:
        if item.get("status")!="COMPLETED":continue
        file=ROOT/item["file"]
        if file.is_file() and checksum(file)==item["output_sha256"]:
            valid[(item["case"],item["arm"])]=item
    results=[]
    for task in ("BOOK","AUTH","QUEUE"):
        for arm in ("baseline","active_control","candidate"):
            rec=valid.get((task,arm))
            row={"case":task,"arm":arm,"output_sha256":rec["output_sha256"] if rec else None,
                 "proxy_tokens":rec["proxy_tokens"] if rec else None}
            if rec:row.update(run(task,arm))
            else:row.update({"state":"NOT_VERIFIED","passed":None,"total":0})
            results.append(row)
            print("SCORE",task,arm,row["state"],row.get("passed"),"/",row.get("total"),flush=True)
    by_arm={}
    for arm in ("baseline","active_control","candidate"):
        group=[x for x in results if x["arm"]==arm]
        by_arm[arm]={"passed":sum(x["passed"] or 0 for x in group),
                     "total":sum(x["total"] for x in group)}
    data={"schema":1,"status":"ALL_NINE_GRADED" if all(x["state"]=="TESTED" for x in results) else "PARTIAL",
          "testing_mode":"9 real isolated model workspaces, external held-out 3-project regression suite",
          "os_isolation":"NOT a secure OS sandbox; fictional only",
          "trust":"Workspace-write model sessions, no real providers or production data",
          "by_arm":by_arm,"rows":results}
    args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":data["status"],"by_arm":by_arm},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
