#!/usr/bin/env python3
"""Consolidate the 9 saved Codex responses; score three fictional pure-function contracts.

Scores are local fixture coverage, NOT overall skill quality or production proof.
Do not overwrite results, model outputs or the journal.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EVAL=ROOT/"evals/v08"
def load_module(path,name):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    return m
def main():
    score=load_module(ROOT/"scripts/score_code_v08.py","v08_score")
    journal=EVAL/"pilot_journal.jsonl"
    if not journal.is_file():raise FileNotFoundError(journal)
    records=[json.loads(line) for line in journal.read_text(encoding="utf-8").splitlines() if line.strip()]
    valid={}
    for item in records:
        if item.get("state")!="COMPLETE":continue
        f=ROOT/item["output_path"]
        if f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest()==item["output_sha256"]:
            valid[(item["case"],item["arm"])]=item
    rows=[]
    for case in ("H04-1","H14-1","H27-1"):
        for arm in ("baseline","active_control","candidate"):
            item=valid.get((case,arm))
            if item is None:
                rows.append({"case":case,"arm":arm,"state":"NOT_EXECUTED_OR_NOT_VERIFIED"})
                continue
            result=score.evaluate(ROOT/item["output_path"],case)
            rows.append({"case":case,"arm":arm,
                         "model":item["model"],"response_sha256":item["output_sha256"],
                         "prompt_sha256":item["prompt_sha256"],
                         "session_reliability":"CLI process completed; independent model identity NOT attested",
                         **result})
    status="ALL_NINE_SCORED" if all(row.get("state") in {
        "TESTED","REJECTED_STATIC_GUARD","TIMEOUT","RUNTIME_ERROR","UNPARSEABLE_OUTPUT"
    } for row in rows) else "PARTIAL"
    data={"schema":1,"status":status,"cases":3,"arms":3,
          "code_result_definition":"fixed fictional unit fixtures under AST-filtered temporary process",
          "warnings":["Not a hardened OS sandbox","3 tasks are too few for causal or statistical skill uplift",
                      "Character-length generic control, not token-length or quality-matched",
                      "No independent human blind review yet"],
          "rows":rows}
    out=EVAL/"pilot_scores_v2.json"
    with out.open("x",encoding="utf-8",newline="\n") as f:json.dump(data,f,indent=2,ensure_ascii=False)
    print(json.dumps({"status":status,"rows":[{"case":r["case"],"arm":r["arm"],
        "state":r["state"],"passed":r.get("passed"),"total":r.get("total")}
        for r in rows]},ensure_ascii=False,indent=2))
    return 0 if status=="ALL_NINE_SCORED" else 2
if __name__=="__main__":raise SystemExit(main())
