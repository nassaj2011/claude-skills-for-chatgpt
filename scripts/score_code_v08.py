#!/usr/bin/env python3
"""Tests generated pure Python functions against fictional edge-case fixtures.

AST filtering and an isolated process are NOT a hardened OS sandbox.
Only execute on disposable non-sensitive environments.
"""
from __future__ import annotations
import argparse
import ast
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SAFE_CALLS={"len","isinstance","int","str","bool","type","all","any","sorted","set",
            "list","tuple","dict","range","enumerate","sum","min","max","abs"}
SAFE_ATTRS={"get","keys","items","values","strip","lower","upper","split",
            "startswith","endswith","isdigit","isdecimal","copy","append","join"}
BLOCKED=(ast.Import,ast.ImportFrom,ast.ClassDef,ast.AsyncFunctionDef,
         ast.With,ast.AsyncWith,ast.Try,ast.Raise,ast.Global,ast.Nonlocal,
         ast.Delete,ast.Lambda,ast.Yield,ast.YieldFrom,ast.Await)
VALID={"name":"demo","version":"1.2.3","source":"approved-registry",
       "integrity":"sha256:"+"a"*64,"license":"MIT","install_scripts":False}
CASES={
"H04-1":{"function":"decide_reservation","examples":[
 [{},{"slot_id":"x","owner":"u","request_key":"r","amount_minor":5},{"status":"CREATED","booking_id":"x:r"}],
 [{"x":{"owner":"u","request_key":"r","amount_minor":5,"booking_id":"b1"}},{"slot_id":"x","owner":"u","request_key":"r","amount_minor":5},{"status":"REPLAY","booking_id":"b1"}],
 [{"x":{"owner":"u","request_key":"r","amount_minor":5,"booking_id":"b1"}},{"slot_id":"x","owner":"v","request_key":"r","amount_minor":5},{"status":"CONFLICT","booking_id":None}],
 [{"x":{"owner":"u","request_key":"r","amount_minor":5,"booking_id":"b1"}},{"slot_id":"x","owner":"u","request_key":"r","amount_minor":6},{"status":"CONFLICT","booking_id":None}],
 [{},{"slot_id":"x","owner":"u","request_key":"r","amount_minor":True},{"status":"INVALID","booking_id":None}],
 [{},{"slot_id":"x","owner":"u","request_key":"","amount_minor":1},{"status":"INVALID","booking_id":None}],
 [{},{"slot_id":5,"owner":"u","request_key":"r","amount_minor":1},{"status":"INVALID","booking_id":None}],
 [{},{"owner":"u","request_key":"r","amount_minor":1},{"status":"INVALID","booking_id":None}],
 [{},{"slot_id":"x","owner":"u","request_key":"r","amount_minor":0},{"status":"INVALID","booking_id":None}],
 [{},{"slot_id":"x","owner":"u","request_key":"r","amount_minor":-2},{"status":"INVALID","booking_id":None}]
]},
"H14-1":{"function":"normalize_llm_payload","examples":[
 [{"decision":"answer","reason":"ok","tool":"none"},{"ok":True,"intent":"answer","error":None}],
 [{"decision":"refuse","reason":"","tool":"none"},{"ok":True,"intent":"refuse","error":None}],
 [{"decision":"lookup","reason":"ok","tool":"lookup_venue"},{"ok":True,"intent":"lookup","error":None}],
 [{"decision":"lookup","reason":"ok","tool":"none"},{"ok":False,"intent":None,"error":"INVALID"}],
 [{"decision":"answer","reason":"ok","tool":"lookup_venue"},{"ok":False,"intent":None,"error":"INVALID"}],
 [{"decision":"answer","reason":"ok","tool":"shell"},{"ok":False,"intent":None,"error":"INVALID"}],
 [{"decision":"answer","reason":"ok","tool":"none","extra":1},{"ok":False,"intent":None,"error":"INVALID"}],
 [{"decision":"answer","reason":"x"*121,"tool":"none"},{"ok":False,"intent":None,"error":"INVALID"}],
 [{"decision":"answer","reason":99,"tool":"none"},{"ok":False,"intent":None,"error":"INVALID"}],
 [[],{"ok":False,"intent":None,"error":"INVALID"}],
 [{"decision":"answer","tool":"none"},{"ok":False,"intent":None,"error":"INVALID"}]
]},
"H27-1":{"function":"assess_package","examples":[
 [VALID,"ALLOW"],[dict(VALID,version="^1.2.3"),"REVIEW"],
 [dict(VALID,source="git+https://example.invalid"),"REVIEW"],
 [dict(VALID,integrity=""),"REVIEW"],
 [dict(VALID,integrity="sha256:"+"g"*64),"REVIEW"],
 [dict(VALID,install_scripts=True),"REVIEW"],
 [dict(VALID,license=""),"REVIEW"],
 [dict(VALID,extra=1),"REVIEW"],[None,"REVIEW"],
 [dict(VALID,version="1.2"),"REVIEW"],
 [dict(VALID,integrity="sha256:"+"A"*64),"REVIEW"]]}
}
HARNESS = """import copy,json,runpy
from pathlib import Path
case=json.loads(Path('fixture.json').read_text(encoding='utf-8'))
fn=runpy.run_path('answer.py')[case['function']]
passed=[]
for row in case['examples']:
    first=copy.deepcopy(row[0]); original=copy.deepcopy(first)
    try:
        if case['function']=='decide_reservation':
            second=copy.deepcopy(row[1]); prev=copy.deepcopy(second)
            result=fn(first,second)
            good=(result==row[2] and first==original and second==prev)
        else:
            result=fn(first)
            if case['function']=='assess_package':
                good=(isinstance(result,dict) and set(result)=={'decision','reasons'}
                      and result['decision']==row[1]
                      and isinstance(result['reasons'],list)
                      and all(isinstance(x,str) and len(x)>0 for x in result['reasons'])
                      and (row[1]!='ALLOW' or result['reasons']==[])
                      and (row[1]!='REVIEW' or bool(result['reasons']))
                      and first==original)
            else:good=(result==row[1] and first==original)
    except Exception:good=False
    passed.append(bool(good))
print(json.dumps({'passed':sum(passed),'total':len(passed),'per_case':passed}))
"""

def clean(text):
    text=text.strip().lstrip("\ufeff")
    fence=chr(96)*3
    if text.startswith(fence):
        text=re.sub("^"+fence+r"(?:python)?[^\n]*\n","",text)
        text=re.sub(r"\n"+fence+r"\s*$","",text)
    return text.strip()

def static_review(code, function):
    try:tree=ast.parse(code)
    except SyntaxError as exc:return ["SyntaxError: "+str(exc)]
    problems=[]
    if len(tree.body)!=1 or not isinstance(tree.body[0],ast.FunctionDef) or tree.body[0].name!=function:
        problems.append("Require only the named pure function")
    for node in ast.walk(tree):
        if isinstance(node,BLOCKED):problems.append("Forbidden AST "+type(node).__name__)
        if isinstance(node,ast.Name) and (node.id.startswith("__") or node.id in
                {"exec","eval","open","input","print","getattr","setattr","delattr",
                 "globals","locals","vars","compile","breakpoint","__import__"}):
            problems.append("Forbidden identifier "+node.id)
        if isinstance(node,ast.Attribute) and node.attr not in SAFE_ATTRS:
            problems.append("Forbidden attribute "+node.attr)
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id not in SAFE_CALLS|{function}:
            problems.append("Unexpected callable "+node.func.id)
    return sorted(set(problems))

def evaluate(path,case):
    fixture=CASES[case]
    raw=clean(path.read_text(encoding="utf-8-sig"))
    issues=static_review(raw,fixture["function"])
    if issues:return {"id":case,"state":"REJECTED_STATIC_GUARD","passed":0,"total":len(fixture["examples"]),"issues":issues}
    with tempfile.TemporaryDirectory(prefix="heldout_v08_") as folder:
        p=Path(folder)
        (p/"answer.py").write_text(raw,encoding="utf-8")
        (p/"fixture.json").write_text(json.dumps(fixture),encoding="utf-8")
        (p/"judge.py").write_text(HARNESS,encoding="utf-8")
        try:
            run=subprocess.run([sys.executable,"-I","-S",str(p/"judge.py")],
                               cwd=p,timeout=5,capture_output=True,text=True,encoding="utf-8",
                               env={"PYTHONIOENCODING":"utf-8"})
        except subprocess.TimeoutExpired:
            return {"id":case,"state":"TIMEOUT","passed":0,"total":len(fixture["examples"])}
        if run.returncode:
            return {"id":case,"state":"RUNTIME_ERROR","passed":0,"total":len(fixture["examples"]),
                    "error":run.stderr[-250:]}
        try:result=json.loads(run.stdout.strip())
        except ValueError:
            return {"id":case,"state":"UNPARSEABLE_OUTPUT","passed":0,"total":len(fixture["examples"])}
        return {"id":case,"state":"TESTED","passed":result["passed"],"total":result["total"],
                "per_case":result["per_case"],"disclaimer":"AST check + temp subprocess, NOT a secure sandbox"}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case",choices=sorted(CASES),required=True)
    parser.add_argument("--response",type=Path,required=True)
    args=parser.parse_args()
    report=evaluate(args.response,args.case)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if report["state"]=="TESTED" else 1
if __name__=="__main__":raise SystemExit(main())
