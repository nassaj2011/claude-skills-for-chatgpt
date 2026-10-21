#!/usr/bin/env python3
"""Produce honest per-skill test-evidence coverage, not fabricated quality passes."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILLS=sorted(x.name for x in (ROOT/"skills").iterdir() if x.is_dir() and (x/"SKILL.md").is_file())
V04={"database-transaction-integrity","security-authorization-auditor"}
V07={"llm-api-integration","mcp-integration-builder","devops-ci-cd",
     "dependency-supply-chain-auditor","backup-disaster-recovery","performance-accessibility"}
V08={"database-transaction-integrity","llm-api-integration","dependency-supply-chain-auditor"}
V10={"database-transaction-integrity","security-authorization-auditor","backend-debugging"}
def main():
    if len(SKILLS)!=29:raise ValueError("Unexpected canonical skill count")
    rows=[]
    for skill in SKILLS:
        text=(ROOT/"skills"/skill/"SKILL.md").read_text(encoding="utf-8")
        rows.append({
            "skill":skill,"canonical_file_present":bool(text.strip()),
            "structural_validation":"PASS_BY_REPOSITORY_VALIDATOR",
            "privacy_static_scanner":"HEURISTIC_ONLY_NOT_SECURITY_CERTIFIED",
            "historic_in_context_AB":skill in V04 or skill in V07,
            "v08_three_arm_pure_code":skill in V08,
            "v10_multifile_generated_code":skill in V10,
            "fully_verified_real_world_skill":"NO",
            "native_host_autotrigger":"NOT_MEASURED",
            "web_app_project_effectiveness":"NOT_MEASURED"
        })
    report={"schema":1,"skills":rows,"total":len(rows),
            "site_package_basic_validity":"29/29 STRUCTURAL PASS",
            "all_skill_real_world_quality_pass":"NOT ESTABLISHED",
            "caution":"Different partial tests and model-only evaluations do not constitute 29 end-to-end passing skills."}
    path=ROOT/"evals/v10/skill_coverage_29.json"
    if path.exists():raise FileExistsError("No overwrite")
    path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("COVERAGE",len(rows),"structural PASS; no blanket functional certification")
if __name__=="__main__":main()
