#!/usr/bin/env python3
"""Deterministic 75-case scoring for three harder repeated Codex tasks.

Executes AST-filtered pure Python only inside an ephemeral folder and isolated
Python subprocess. THIS IS NOT AN OS SECURITY SANDBOX, not suitable for
untrusted unreviewed code or sensitive machines.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import importlib.util
import json
import statistics
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ROOTV=ROOT/"evals/v09"
s=importlib.util.spec_from_file_location("v08_code",ROOT/"scripts/score_code_v08.py")
v08=importlib.util.module_from_spec(s);s.loader.exec_module(v08)
cases={x["case"]:x for x in json.loads((ROOTV/"oracle_fixtures.json").read_text(encoding="utf-8"))["cases"]}
HARNESS = """import copy,json,runpy
from pathlib import Path
fixture=json.loads(Path('fixture.json').read_text(encoding='utf-8'))
fn=runpy.run_path('response.py')[fixture['function']]
passed=[]
for case in fixture['tests']:
    args=copy.deepcopy(case['args'])
    snapshot=copy.deepcopy(args)
    try:
        out=fn(*args)
        good=(out==case['expected'] and args==snapshot)
    except Exception:
        good=False
    passed.append(bool(good))
print(json.dumps({'passed':sum(passed),'total':len(passed),'per_case':passed}))
"""

def check(path,case):
    spec=cases[case];total=len(spec["tests"])
    try:text=v08.clean(path.read_text(encoding="utf-8-sig"))
    except OSError:return {"state":"MISSING","passed":None,"total":total}
    if len(text)>16000:return {"state":"TOO_LONG","passed":0,"total":total}
    problems=[p for p in v08.static_review(text,spec["function"]) if p!="Forbidden attribute add"]
    try:
        source_ast=ast.parse(text)
        nested_names={n.name for n in ast.walk(source_ast)
                      if isinstance(n,ast.FunctionDef) and n is not source_ast.body[0]}
        problems=[problem for problem in problems
                  if not (problem.startswith("Unexpected callable ")
                          and problem.removeprefix("Unexpected callable ") in nested_names)]
    except (SyntaxError,IndexError):
        pass
    if problems:return {"state":"STATIC_REJECT","passed":0,"total":total,"issues":problems}
    with tempfile.TemporaryDirectory(prefix="v09_grade_") as td:
        wd=Path(td)
        (wd/"response.py").write_text(text,encoding="utf-8")
        (wd/"fixture.json").write_text(json.dumps(spec,ensure_ascii=False),encoding="utf-8")
        (wd/"judge.py").write_text(HARNESS,encoding="utf-8")
        try:
            p=subprocess.run([sys.executable,"-I","-S",str(wd/"judge.py")],
                             cwd=wd,timeout=5,capture_output=True,text=True,encoding="utf-8",
                             env={"PYTHONIOENCODING":"utf-8"})
        except subprocess.TimeoutExpired:
            return {"state":"TIMEOUT","passed":0,"total":total}
        if p.returncode:return {"state":"RUNTIME_ERROR","passed":0,"total":total,"details":p.stderr[-270:]}
        try:result=json.loads(p.stdout.strip())
        except (json.JSONDecodeError,ValueError):
            return {"state":"INVALID_OUTPUT","passed":0,"total":total}
        return {"state":"TESTED","passed":result["passed"],"total":result["total"],
                "per_case":result["per_case"]}

def evaluate():
    file=ROOTV/"run_journal.jsonl"
    journal=[json.loads(line) for line in file.read_text(encoding="utf-8").splitlines() if line.strip()]
    valid={}
    for rec in journal:
        if rec.get("status")!="COMPLETED":continue
        path=ROOT/rec["file"]
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=rec["sha256"]:
            continue
        valid[(rec["case"],rec["arm"],rec["repeat"])]=rec
    rows=[]
    for case in ("P01","P02","P03"):
        for arm in ("baseline","active_control","candidate"):
            for rep in (1,2):
                key=(case,arm,rep)
                rec=valid.get(key)
                if not rec:
                    result={"state":"NOT_VERIFIED","passed":None,"total":len(cases[case]["tests"])}
                else:result=check(ROOT/rec["file"],case)
                rows.append({"case":case,"arm":arm,"repeat":rep,
                             "output_sha256":rec["sha256"] if rec else None,
                             "proxy_tokens":rec["proxy_tokens"] if rec else None,
                             **result})
    by_arm={}
    for arm in ("baseline","active_control","candidate"):
        subset=[r for r in rows if r["arm"]==arm]
        by_arm[arm]={"passed":sum(r["passed"] or 0 for r in subset),
                     "maximum":sum(r["total"] for r in subset),
                     "completed":sum(r["passed"] is not None for r in subset)}
    return {"schema":1,"status":"ALL_18_SCORED" if all(r["passed"] is not None for r in rows) else "PARTIAL",
            "oracle_cases":sum(len(c["tests"]) for c in cases.values()),
            "attempts":18,
            "fixture_limit":"Not hidden from repository reviewers; fictional deterministic exact-match test set",
            "sandbox_limit":"AST filter plus ephemeral Python subprocess, NOT a hardened sandbox",
            "token_balance":"o200k_base proxy only; not a model-internal tokenizer guarantee",
            "arms":by_arm,"rows":rows}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,default=ROOTV/"hard_pilot_scores.json")
    args=p.parse_args()
    result=evaluate()
    if args.output.exists() or args.output.is_symlink():
        p.error("Output exists: refuse overwrite")
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"arms":result["arms"],
                      "rows":[{k:v for k,v in r.items() if k in ("case","arm","repeat","state","passed","total","issues")}
                              for r in result["rows"]]},ensure_ascii=False,indent=2))
    return 0 if result["status"]=="ALL_18_SCORED" else 2

if __name__=="__main__":raise SystemExit(main())
