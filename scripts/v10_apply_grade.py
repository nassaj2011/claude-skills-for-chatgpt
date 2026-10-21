#!/usr/bin/env python3
"""Apply nine archived JSON multi-file replies into NEW isolated workspaces.

The model never edits these directories directly. Reject unknown paths, code
imports and invalid JSON. Run fixed developer-authored held-out tests in
separate subprocesses. Not a hardened OS execution sandbox.
"""
from __future__ import annotations
import hashlib
import json
import shutil
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"evals/v10"
sys.path.insert(0,str(ROOT/"scripts"))
import v10_grade as grade
ALLOWED={"BOOK":{"booking/service.py","booking/queries.py"},
         "AUTH":{"portal/policy.py","portal/handlers.py"},
         "QUEUE":{"notifier/worker.py","notifier/metrics.py"}}
def sha(b):return hashlib.sha256(b).hexdigest()
def parse_source(text):
    s=text.strip().lstrip("\ufeff")
    fence=chr(96)*3
    if s.startswith(fence):
        lines=s.splitlines()
        if lines[-1].strip()==fence:s="\n".join(lines[1:-1])
    return json.loads(s)
def main():
    log=BASE/"patch_journal.jsonl"
    events=[json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]
    valid={}
    for row in events:
        if row.get("status")!="COMPLETE":continue
        p=ROOT/row["file"]
        if p.is_file() and sha(p.read_bytes())==row["response_sha256"]:
            valid[(row["case"],row["arm"])]=row
    root=BASE/"patch_workspaces"
    if root.exists():raise FileExistsError("Refuse to overwrite previous patched workspace")
    root.mkdir()
    rows=[]
    for case in ALLOWED:
        for arm in ("baseline","active_control","candidate"):
            record=valid.get((case,arm))
            outcome={"case":case,"arm":arm,"response_sha256":record["response_sha256"] if record else None}
            if not record:
                outcome.update({"state":"MISSING_RESPONSE","passed":None,"total":0})
                rows.append(outcome);continue
            source=ROOT/record["file"]
            try:
                artifact=parse_source(source.read_text(encoding="utf-8-sig"))
                if not isinstance(artifact,dict) or set(artifact)!={"files"}:
                    raise ValueError("JSON must be exactly a files mapping")
                files=artifact["files"]
                if not isinstance(files,dict) or set(files)!=ALLOWED[case]:
                    raise ValueError("Unexpected or missing target paths")
                if any(not isinstance(code,str) or not code.strip() or len(code)>25000 for code in files.values()):
                    raise ValueError("Missing or oversized source")
                dst=root/f"{case}-{arm}"
                shutil.copytree(BASE/"templates"/case,dst)
                for rel,text in files.items():
                    target=dst/rel
                    if not target.is_file() or target.is_symlink():
                        raise ValueError("Disallowed output path")
                    target.write_text(text,encoding="utf-8")
                outcome.update(grade.run(case,arm,root_override=dst))
                outcome["applied_file_count"]=len(files)
            except (OSError,ValueError,TypeError,json.JSONDecodeError) as exc:
                outcome.update({"state":"INVALID_MODEL_FILE_OUTPUT","passed":0,"total":0,
                                "reason":str(exc)[:220]})
            rows.append(outcome)
            print("GRADE",case,arm,outcome["state"],outcome.get("passed"),"/",outcome.get("total"),flush=True)
    total={}
    for arm in ("baseline","active_control","candidate"):
        sub=[r for r in rows if r["arm"]==arm]
        total[arm]={"passed":sum(x.get("passed") or 0 for x in sub),
                    "total":sum(x["total"] for x in sub),
                    "valid_cases":sum(x["state"]=="TESTED" for x in sub)}
    output={"schema":1,"status":"ALL_NINE_GRADED" if all(r["state"]=="TESTED" for r in rows) else "PARTIAL",
            "tool_host":"MISSING; model produced full JSON source, external applier wrote to isolated fixtures",
            "grading_limit":"developer-maintained synthetic hidden tests; not OS hardened",
            "by_arm":total,"rows":rows}
    filename=BASE/"patch_scores.json"
    with filename.open("x",encoding="utf-8") as f:json.dump(output,f,ensure_ascii=False,indent=2)
    print(json.dumps({"status":output["status"],"by_arm":total},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
