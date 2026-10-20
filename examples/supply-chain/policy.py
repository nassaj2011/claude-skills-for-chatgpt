"""Toy dependency-manifest provenance linter; not SBOM, npm parser or a CVE feed."""
from __future__ import annotations
import json,re
from pathlib import Path
VERSION=re.compile(r"^\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?$")
def review(data:dict)->dict:
 if not isinstance(data,dict) or not isinstance(data.get("packages"),list):raise ValueError("Expected packages list")
 if not data["packages"]:raise ValueError("No packages to review")
 findings=[]
 seen=set()
 for row in data["packages"]:
  if not isinstance(row,dict) or set(row)!={"name","version","source","integrity","license","install_scripts"}:raise ValueError("Incomplete metadata")
  name=row["name"]
  if not isinstance(name,str) or not re.fullmatch(r"[A-Za-z0-9@/_.-]{1,120}",name):raise ValueError("Invalid package name")
  if name in seen:findings.append({"name":name,"risk":"duplicate package metadata"})
  seen.add(name)
  if not isinstance(row["version"],str) or not VERSION.fullmatch(row["version"]):findings.append({"name":name,"risk":"floating/unpinned version"})
  if row["source"]!="approved-registry":findings.append({"name":name,"risk":"source provenance needs review"})
  if not isinstance(row["integrity"],str) or not re.fullmatch(r"sha256:[a-f0-9]{64}",row["integrity"]):findings.append({"name":name,"risk":"missing/invalid content integrity metadata"})
  if not isinstance(row["license"],str) or not row["license"].strip():findings.append({"name":name,"risk":"license unknown"})
  if row["install_scripts"] is not False:findings.append({"name":name,"risk":"install-time side effects require review"})
 return {"decision":"REVIEW" if findings else "PASS_STATIC_METADATA","findings":findings,
         "caveat":"Self-declared metadata; hashes not verified against downloads; no live registry/CVE/license check."}
def main()->int:
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("--input",type=Path,required=True);a=p.parse_args()
 result=review(json.loads(a.input.read_text(encoding="utf-8")))
 print(json.dumps(result,indent=2));return int(result["decision"]!="PASS_STATIC_METADATA")
if __name__=="__main__":raise SystemExit(main())
