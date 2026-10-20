#!/usr/bin/env python3
"""Verify saved v0.7 Codex A/B output evidence without scoring it.

A digest validates file integrity only, not independent model authenticity.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def verify(root:Path=ROOT)->tuple[int,list[str]]:
    manifest=json.loads((root/"evals/v07-run-manifest.json").read_text(encoding="utf-8"))
    criteria=json.loads((root/"evals/v07-quality-benchmarks.json").read_text(encoding="utf-8"))
    faults=[]
    cases=manifest["cases"]
    expected={c["id"] for c in criteria["cases"]}
    if len(cases)!=6 or {x["id"] for x in cases}!=expected:
        faults.append("Incomplete case coverage or duplicates")
    if manifest.get("grading")!="NOT_SCORED" or any(c.get("score") is not None for c in criteria["cases"]):
        faults.append("Unsanctioned scoring claims")
    seen_sessions=set()
    for item in cases:
        b=item["baseline"];c=item["candidate"]
        if b["session_id"]==c["session_id"]:faults.append("Identical baseline/candidate session")
        for mode,run in (("baseline",b),("candidate",c)):
            session=run.get("session_id")
            if not isinstance(session,str) or not session or session in seen_sessions: faults.append("Missing/reused session ID")
            seen_sessions.add(session)
            path=run.get("path","")
            if (not isinstance(path,str) or not path.startswith("evals/runs/v07-")
                    or Path(path).is_absolute() or ".." in Path(path).parts
                    or Path(path).as_posix()!=f'evals/runs/{item["id"]}-{mode}.txt'):
                faults.append("Unsafe/wrong raw-output path "+str(path))
                continue
            target=root/path
            if not target.is_file() or target.is_symlink():
                faults.append("Raw file unavailable "+path)
                continue
            digest=hashlib.sha256(target.read_bytes()).hexdigest()
            if digest!=run.get("sha256"):faults.append("Raw output checksum changed: "+path)
            if len(target.read_bytes())<200:faults.append("Incomplete model response "+path)
    return len(cases),faults

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=ROOT)
    args=parser.parse_args()
    try:count,faults=verify(args.root)
    except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError) as ex:parser.error(str(ex))
    for f in faults:print("ERROR:",f)
    if faults:return 1
    print(f"PASS: {count} A/B cases, {count*2} independently recorded sessions and SHA-256 response digests; grades NOT SCORED.")
    return 0
if __name__=="__main__":raise SystemExit(main())
