#!/usr/bin/env python3
"""Post-hoc 12 additional checks on archived nine v10 code workspaces.

This is exploratory (not preregistered) and cannot independently certify the
29 skills. Execute only on disposable fictional workspaces.
"""
from __future__ import annotations
import json
import subprocess
import sys
import tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import v10_grade
TEST=ROOT/"evals/v11_adversarial_regression.py"
WORK=ROOT/"evals/v10/patch_workspaces"
def main():
 rows=[]
 with tempfile.TemporaryDirectory(prefix="v11_followup_") as td:
  runner=Path(td)/"runner.py"
  runner.write_text(v10_grade.WORKER,encoding="utf-8")
  for case in ("BOOK","AUTH","QUEUE"):
   for arm in ("baseline","active_control","candidate"):
    target=WORK/(case+"-"+arm)
    anomalies=v10_grade.static_check(target,case)
    if anomalies:
     result={"state":"STATIC_REJECT","passed":0,"total":0,"issues":anomalies}
    else:
     env={"SKILL_EVAL_TASK":case,"PYTHONIOENCODING":"utf-8"}
     try:
      p=subprocess.run([sys.executable,"-I","-S",str(runner),str(target),str(TEST)],
                       cwd=td,env=env,timeout=12,capture_output=True,text=True)
      result=json.loads(p.stdout.strip())
      result["state"]="TESTED"
     except Exception as exc:
      result={"state":"RUN_FAILED","passed":0,"total":0,"message":str(exc)[:200]}
    rows.append({"case":case,"arm":arm,**result})
    print(case,arm,result["state"],result.get("passed"),"/",result.get("total"),flush=True)
 out={"schema":1,"state":"EXPLORATORY_POST_HOC","total_distinct_test_methods":12,
      "original_v10_scores_unchanged":True,
      "not_a_native_codex_skill_test":True,
      "rows":rows}
 target=ROOT/"evals/v11_followup_scores.json"
 with target.open("x",encoding="utf-8") as f:json.dump(out,f,ensure_ascii=False,indent=2)
if __name__=="__main__":main()
