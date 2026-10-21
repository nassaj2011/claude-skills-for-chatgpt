#!/usr/bin/env python3
"""Read-only verification of the 9 archived v0.8 pilot responses and scores.

Does NOT execute generated model code or contact any provider.
"""
from __future__ import annotations
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"evals/v08"
CASES=("H04-1","H14-1","H27-1")
ARMS=("baseline","active_control","candidate")
EXPECTED={("H04-1","baseline"):(10,10),("H04-1","active_control"):(10,10),
          ("H04-1","candidate"):(10,10),("H14-1","baseline"):(8,11),
          ("H14-1","active_control"):(11,11),("H14-1","candidate"):(11,11),
          ("H27-1","baseline"):(11,11),("H27-1","active_control"):(11,11),
          ("H27-1","candidate"):(11,11)}
def check():
    errors=[]
    bank=json.loads((BASE/"heldout_87.json").read_text(encoding="utf-8"))
    if len(bank["cases"])!=87 or len({c["skill"] for c in bank["cases"]})!=29:
        errors.append("Bad held-out bank coverage")
    entries=[json.loads(x) for x in (BASE/"pilot_journal.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    verified={}
    for item in entries:
        if item.get("state")!="COMPLETE":continue
        key=(item["case"],item["arm"])
        relative=item.get("output_path","")
        if relative!=f"evals/v08/runs/{key[0]}-{key[1]}.txt":
            errors.append("Unexpected evidence path for "+str(key));continue
        fn=ROOT/relative
        if not fn.is_file() or fn.is_symlink():
            errors.append("Missing original response "+relative);continue
        digest=hashlib.sha256(fn.read_bytes()).hexdigest()
        if digest!=item.get("output_sha256"):
            errors.append("Output tamper detected "+relative);continue
        if fn.stat().st_size<80:
            errors.append("Truncated output "+relative);continue
        verified[key]=item
    if set(verified)!=set(EXPECTED):
        errors.append("Incomplete verified 9-response coverage")
    scores=json.loads((BASE/"pilot_scores_v2.json").read_text(encoding="utf-8"))
    if scores["status"]!="ALL_NINE_SCORED" or len(scores["rows"])!=9:
        errors.append("Incomplete 9-arm test record")
    found={}
    for row in scores["rows"]:
        key=(row["case"],row["arm"])
        if key in found:errors.append("Duplicate score row "+str(key))
        found[key]=(row.get("passed"),row.get("total"))
        if row.get("state")!="TESTED":errors.append("Test not actually completed "+str(key))
        if key in verified and row.get("response_sha256")!=verified[key].get("output_sha256"):
            errors.append("Score-to-output checksum mismatch "+str(key))
    if found!=EXPECTED:errors.append("Recorded fixture scores differ from archived reviewed result")
    return errors

if __name__=="__main__":
    errors=check()
    if errors:
        for x in errors:print("ERROR:",x)
        raise SystemExit(1)
    print("PASS: 87 scenario bank; 9 archived A/B/control outputs with verified SHA-256; 9 recorded test rows; no code executed by verification.")
