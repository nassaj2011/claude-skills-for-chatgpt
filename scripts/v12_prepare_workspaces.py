#!/usr/bin/env python3
"""Rebuild archived v0.10 fictional two-file patches; does not execute model code.

Read-only archived response SHA verification, strict path allowlist, Python syntax
verification, and no overwrite. Use a disposable environment before separate
post-hoc scoring, which does execute previously generated Python.
"""
from __future__ import annotations
import ast
import hashlib
import json
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"evals/v10"
OUT=BASE/"patch_workspaces"
EXPECTED={
    "BOOK":{"booking/service.py","booking/queries.py"},
    "AUTH":{"portal/policy.py","portal/handlers.py"},
    "QUEUE":{"notifier/worker.py","notifier/metrics.py"},
}
ARMS=("baseline","active_control","candidate")

def digest(content:bytes)->str:
    return hashlib.sha256(content).hexdigest()

def main():
    if OUT.exists() or OUT.is_symlink():
        raise FileExistsError(f"Refusing to replace any existing workspaces: {OUT}")
    raw=[json.loads(line) for line in (BASE/"patch_journal.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    valid={}
    for row in raw:
        if row.get("status")!="COMPLETE":
            continue
        k=(row["case"],row["arm"])
        if k in valid:
            raise ValueError("Duplicate model response record")
        p=ROOT/row["file"]
        if not p.is_file() or p.is_symlink() or digest(p.read_bytes())!=row["response_sha256"]:
            raise ValueError("Archived model output missing or tampered: "+str(k))
        valid[k]=p
    expected={(task,arm) for task in EXPECTED for arm in ARMS}
    if set(valid)!=expected:
        raise ValueError("Archived evidence coverage does not contain exactly nine cases")
    changes={}
    for (task,arm),file in valid.items():
        source=file.read_text(encoding="utf-8-sig").strip()
        fence=chr(96)*3
        if source.startswith(fence):
            lines=source.splitlines()
            if lines[-1].strip()==fence:
                source="\n".join(lines[1:-1])
        document=json.loads(source)
        if not isinstance(document,dict) or set(document)!={"files"}:
            raise ValueError("Unexpected result object")
        changed=document["files"]
        if not isinstance(changed,dict) or set(changed)!=EXPECTED[task]:
            raise ValueError("Unexpected replacement target")
        for rel,content in changed.items():
            if not isinstance(content,str) or not content.strip() or len(content)>25000:
                raise ValueError("Invalid replacement source")
            ast.parse(content)
        changes[(task,arm)]=changed
    OUT.mkdir(parents=True)
    for (task,arm),changed in changes.items():
        target=OUT/f"{task}-{arm}"
        template=BASE/"templates"/task
        if template.is_symlink() or not template.is_dir():
            raise ValueError("Invalid source template")
        shutil.copytree(template,target)
        for rel,content in changed.items():
            f=target/rel
            if not f.is_file() or f.is_symlink():
                raise ValueError("Unexpected target: "+rel)
            f.write_text(content,encoding="utf-8")
    print(f"PASS: reconstructed {len(changes)} fictional model-code workspaces, no code executed, all raw hashes verified.")
if __name__=="__main__":
    main()
