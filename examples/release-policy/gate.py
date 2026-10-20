"""Synthetic release evidence classifier. Never deploys, invokes CI, or reads secrets."""
from __future__ import annotations
import json
from pathlib import Path

REQUIRED={"sha","environment","checks","migration","restore_drill","approved"}
CRITICAL={"unit","authorization","integration","staging_smoke"}

def decide(evidence:dict) -> dict:
    if not isinstance(evidence,dict) or set(evidence)!=REQUIRED:raise ValueError("Invalid evidence schema")
    if not isinstance(evidence["sha"],str) or len(evidence["sha"])<7:raise ValueError("Missing commit SHA")
    if evidence["environment"] not in {"staging","production"}:raise ValueError("Bad environment")
    checks=evidence["checks"]
    if not isinstance(checks,dict) or not CRITICAL.issubset(checks):raise ValueError("Incomplete check inventory")
    if any(v not in {"PASS","FAIL","SKIPPED","NOT_RUN"} for v in checks.values()):raise ValueError("Unknown check status")
    blockers=[f"{k}:{checks[k]}" for k in sorted(CRITICAL) if checks[k]!="PASS"]
    if evidence["migration"]!="PREFLIGHT_PASS":blockers.append("MIGRATION_NOT_VERIFIED")
    if evidence["restore_drill"] is not True:blockers.append("RESTORE_NOT_PROVEN")
    if evidence["approved"] is not True:blockers.append("NO_ACCOUNTABLE_APPROVAL")
    return {"verdict":"NO_GO" if blockers else "ELIGIBLE_FOR_HUMAN_DECISION",
            "sha":evidence["sha"],"blockers":blockers,
            "caveat":"Offline illustration; not actual CI or deployment evidence. Eligible != deployed."}

def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--file",type=Path,required=True)
    args=p.parse_args()
    output=decide(json.loads(args.file.read_text(encoding="utf-8")))
    print(json.dumps(output,indent=2))
    return int(output["verdict"]=="NO_GO")
if __name__=="__main__":raise SystemExit(main())
