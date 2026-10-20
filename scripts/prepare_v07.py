#!/usr/bin/env python3
"""Print a v0.7 fictional task with optional specialist source text.

No model call, network, code execution or secret handling. Outputs to stdout.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def build(case_id:str,mode:str)->str:
    data=json.loads((ROOT/"evals/v07-quality-benchmarks.json").read_text(encoding="utf-8"))
    records=[c for c in data["cases"] if c["id"]==case_id]
    if len(records)!=1:raise ValueError("Unknown case ID")
    if mode not in {"baseline","candidate"}:raise ValueError("Invalid mode")
    case=records[0]
    common="Fictional read-only evaluation. Do not inspect private files, use tools, access network, change code or claim tests. Respond with verifiable specialist analysis. State NOT RUN for absent evidence.\n"
    if mode=="baseline":return common+"\n"+case["prompt"]+"\n"
    path=ROOT/"skills"/case["skill"]/"SKILL.md"
    if not path.is_file() or path.is_symlink():raise ValueError("Missing skill")
    return common+"\nSPECIALIST WORKFLOW GUIDANCE:\n"+path.read_text(encoding="utf-8")+"\n\nSAME FICTIONAL TASK:\n"+case["prompt"]+"\n"

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case",required=True)
    parser.add_argument("--mode",required=True,choices=("baseline","candidate"))
    args=parser.parse_args()
    print(build(args.case,args.mode),end="")

if __name__=="__main__":main()
