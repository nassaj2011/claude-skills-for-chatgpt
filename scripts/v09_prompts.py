#!/usr/bin/env python3
"""Construct reproducible three-arm prompts with proxy tokenizer balancing.

o200k_base is a public proxy and is NOT attested as GPT-5.6 Terra's tokenizer.
Generic control matches candidate by total prompt token count (within 1).
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/"_ClaudeSkillsEvalV09Deps"))
import tiktoken

enc=tiktoken.get_encoding("o200k_base")
HEAD=("FICTIONAL CODE-GENERATION EVALUATION. No tools, network, private files or claims "
      "about executed tests. Implement exactly the one function specified in TASK and "
      "CONTRACT. Output ONLY executable Python source; no Markdown fences, no imports.\n\n")
NEUTRAL=[
"Identify the precise requested deliverable, distinguish supplied facts from assumptions, and obey the stated response format. ",
"Look for missing inputs, incompatible statements, unhandled edge cases, and contradictions in the instructions. ",
"Make a careful first pass through the problem and another pass looking for overlooked conditions. ",
"Use clear names and avoid unnecessary complexity so that the resulting artifact can be reviewed by another engineer. ",
"When certainty is limited, rely on the explicit information in the task rather than inventing details. ",
"Consider how a future reader would verify that the result satisfies the request, and keep conclusions evidence-based. ",
"Before finishing, check whether every requested element is present and if the output includes unrelated material. ",
"Prefer precise, minimal, self-contained work products with stable behavior under ordinary circumstances. ",
"Review assumptions about types, boundaries, names, order, formatting and completeness without making unsupported claims. ",
"Use straightforward reasoning, keep separate concerns explicit and avoid repeating boilerplate that does not help. ",
"Where choices exist, choose an approach compatible with the limitations stated in the request. ",
"Consider potential failure cases, understand what the result promises, and do not exaggerate guarantees. "
]
FINISH=[" Review.", " Check.", " Confirm.", " Verify.", " Note.", " Done.", " Yes.", " OK.", " Valid.", " Ready.", " a", " b", " c", ".", " "]

def cases():
    return {c["id"]:c for c in json.loads((ROOT/"evals/v09/hard_cases.json").read_text(encoding="utf-8"))["cases"]}
def token_count(s):return len(enc.encode(s))
def task_section(case):
    return (f"TASK {case['id']}:\n{case['task']}\n\nSTRICT FUNCTION CONTRACT:\n"
            +case["contract"]+"\n")
def candidate(case):
    f=ROOT/"skills"/case["skill"]/"SKILL.md"
    source=f.read_text(encoding="utf-8-sig")
    return HEAD+"SPECIALIST GUIDANCE:\n"+source+"\n\n"+task_section(case)
def control(case, target):
    before=HEAD+"GENERAL TASK-NEUTRAL GUIDANCE:\n"
    after="\n\n"+task_section(case)
    cur=before
    pos=0
    while pos<120 and token_count(cur+NEUTRAL[pos%len(NEUTRAL)]+after)<=target-6:
        cur+=NEUTRAL[pos%len(NEUTRAL)]
        pos+=1
    # Fill with complete neutral clauses when possible, allowing a 1-token proxy margin.
    while True:
        now=token_count(cur+after)
        if now>=target-1:break
        valid=[(token_count(cur+phrase+after),phrase) for phrase in FINISH
               if token_count(cur+phrase+after)<=target]
        if not valid:break
        best=max(valid,key=lambda x:x[0])
        if best[0]==now:break
        cur+=best[1]
    result=cur+after
    delta=target-token_count(result)
    if delta>1:raise RuntimeError(f"Proxy token balancing failed by {delta} for {case['id']}")
    return result
def prompt(case_id,arm):
    c=cases()[case_id]
    if arm=="baseline":return HEAD+task_section(c)
    if arm=="candidate":return candidate(c)
    if arm=="active_control":return control(c,token_count(candidate(c)))
    raise ValueError("Unknown arm")
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--case",required=True,choices=sorted(cases()))
    p.add_argument("--arm",required=True,choices=("baseline","active_control","candidate"))
    p.add_argument("--metrics",action="store_true")
    a=p.parse_args()
    src=prompt(a.case,a.arm)
    if a.metrics:
        print(json.dumps({"case":a.case,"arm":a.arm,"proxy_encoding":"o200k_base",
                          "proxy_tokens":token_count(src),"chars":len(src),
                          "sha256":hashlib.sha256(src.encode("utf-8")).hexdigest()}))
    else:print(src,end="")
if __name__=="__main__":main()
