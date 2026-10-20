#!/usr/bin/env python3
"""Safely install new Agent Skills; preview-only by default.

- No network, telemetry, remote access, overwrite or deletion of user files.
- HIGH indicators always block; REVIEW indicators require explicit approval.
- Each skill is staged, rescanned and promoted in one directory rename.
- Partial staging directories are reported, NEVER silently removed.
The static scanner is heuristic and cannot guarantee that a skill is safe.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

from audit_skills import scan
from validate_skills import validate_all

PROJECT = "https://github.com/nassaj2011/claude-skills-for-chatgpt"


def _is_link(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())


def validate_target(target: Path) -> None:
    """Reject symlink/junction anywhere in destination ancestry."""
    if not target.is_absolute():
        raise ValueError("Destination must be an absolute path after expansion")
    for ancestor in (target, *target.parents):
        if _is_link(ancestor):
            raise ValueError(f"Symlink/junction destination path is not supported: {ancestor}")
        if ancestor.exists() and not ancestor.is_dir():
            raise ValueError(f"Destination ancestor is not a directory: {ancestor}")


def plan(skills_root: Path, destination: Path, selected: list[str] | None) -> list[tuple[str, Path, Path, str]]:
    count, errors = validate_all(skills_root)
    if errors or count == 0:
        raise ValueError("Invalid source skills:\n" + "\n".join(errors))
    available = {s.name: s for s in skills_root.iterdir() if s.is_dir() and not _is_link(s)}
    names = sorted(available) if not selected else list(dict.fromkeys(selected))
    unknown = [name for name in names if name not in available]
    if unknown:
        raise ValueError("Unknown or linked skill(s): " + ", ".join(unknown))
    validate_target(destination)
    result = []
    for name in names:
        dest = destination / name
        result.append((name, available[name], dest, "SKIP (already exists)" if dest.exists() or _is_link(dest) else "COPY"))
    return result


def audit_installable(operations: list[tuple[str, Path, Path, str]]) -> tuple[bool, int]:
    """Compatibility return: (has high finding, number of skills with any finding)."""
    blocked, reviewed = False, 0
    for name, src, _, status in operations:
        if status != "COPY":
            continue
        result = scan(src)
        for finding in result["findings"]:
            print(f"  {finding['severity']} {name}/{finding['path']}:{finding['line']} [{finding['rule']}] {finding['detail']}")
        if result["decision"] == "BLOCK":
            blocked = True
        if result["findings"]:
            reviewed += 1
    return blocked, reviewed


def install_one(src: Path, dest: Path) -> dict:
    """Stage without affecting existing skills; verify snapshot then rename."""
    if dest.exists() or _is_link(dest):
        return {"status": "SKIPPED", "skill": src.name}
    stage = dest.parent / f".install-pending-{src.name}-{uuid.uuid4().hex}"
    source_fingerprint = scan(src)
    if source_fingerprint["findings"]:
        # Reviewed indicators are handled by explicit CLI approval; HIGH never allowed.
        if source_fingerprint["decision"] == "BLOCK":
            raise RuntimeError(f"Source became unsafe: {src}")
    try:
        shutil.copytree(src, stage, symlinks=True, dirs_exist_ok=False)
        staged = scan(stage)
        if (staged["sha256"] != source_fingerprint["sha256"]
                or staged["findings"] != source_fingerprint["findings"]
                or staged["files_scanned"] != source_fingerprint["files_scanned"]):
            raise RuntimeError("Staged content differs from audited source")
        if dest.exists() or _is_link(dest):
            return {"status": "SKIPPED_DESTINATION_APPEARED", "skill": src.name, "staging_left": str(stage)}
        # Same-parent rename is atomic on supported local filesystems; Windows does not
        # replace an existing destination directory. See documented platform caveat.
        os.rename(stage, dest)
    except Exception as exc:
        raise RuntimeError(f"{exc}; staging, if created, was NOT deleted: {stage}") from exc
    return {"status": "INSTALLED", "skill": src.name, "file_count": staged["files_scanned"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True, help="Explicit destination e.g. ~/.agents/skills")
    parser.add_argument("--only", nargs="+", help="Selected skill names")
    parser.add_argument("--apply", action="store_true", help="Copy the audited skills; default is read-only preview")
    parser.add_argument("--accept-review", action="store_true", help="I have MANUALLY reviewed all REVIEW findings; HIGH still blocks")
    parser.add_argument("--receipt", type=Path, help="Optional NEW local JSON receipt, no upload; will not overwrite")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / "skills"
    target = args.target.expanduser().absolute()
    try:
        operations = plan(root, target, args.only)
    except ValueError as exc:
        parser.error(str(exc))
    blocked, reviewed = audit_installable(operations)
    for name, _, dest, status in operations:
        print(f"{status}: {name} -> {dest}")
    if blocked:
        print("BLOCKED: HIGH finding. Audit source; installation not allowed by this helper.")
        return 2
    if reviewed and not args.accept_review:
        print(f"REVIEW REQUIRED: {reviewed} skill(s) have suspicious/unsupported content.")
        print("Manual source review is required. Then explicitly use --accept-review to proceed.")
        if args.apply:
            return 3
    if not args.apply:
        print("Preview only; no installation occurred.")
        return 0

    installed = []
    errors = []
    if args.receipt:
        receipt = args.receipt.expanduser().absolute()
        if receipt.exists() or receipt.is_symlink():
            parser.error("Receipt file already exists; refusing to overwrite")
        if target == receipt or target in receipt.parents:
            parser.error("Receipt must be stored outside the destination skills folder")
    target.mkdir(parents=True, exist_ok=True)
    for name, src, dest, status in operations:
        if status != "COPY":
            continue
        try:
            out = install_one(src, dest)
            print(f"{out['status']}: {name}")
            installed.append(out)
        except (OSError, RuntimeError) as exc:
            print(f"ERROR installing {name}: {exc}")
            errors.append({"skill": name, "error_type": type(exc).__name__})
            break
    if args.receipt:
        data = {"schema": 1, "project": PROJECT, "created_utc": datetime.now(timezone.utc).isoformat(),
                "telemetry": False, "installed": installed, "errors": errors}
        with receipt.open("x", encoding="utf-8") as writer:
            json.dump(data, writer, indent=2)
            writer.write("\n")
        print(f"Local receipt written: {receipt} (no upload, no user identity collected)")
    print(f"Installed {sum(item['status'] == 'INSTALLED' for item in installed)} skill(s), {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
