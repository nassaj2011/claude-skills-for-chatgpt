#!/usr/bin/env python3
"""Preview or safely install new Agent Skills (no overwrite, no deletion).

A read-only heuristic security audit is mandatory for each selected new skill.
A clean audit cannot prove that a skill is safe; review third-party sources.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from audit_skills import scan
from validate_skills import validate_all


def plan(skills_root: Path, destination: Path, selected: list[str] | None) -> list[tuple[str, Path, Path, str]]:
    count, errors = validate_all(skills_root)
    if errors or count == 0:
        raise ValueError("Invalid source skills:\n" + "\n".join(errors))
    available = {p.name: p for p in skills_root.iterdir() if p.is_dir() and not p.is_symlink()}
    names = sorted(available) if not selected else list(dict.fromkeys(selected))
    unknown = [name for name in names if name not in available]
    if unknown:
        raise ValueError("Unknown or linked skill(s): " + ", ".join(unknown))
    result = []
    for name in names:
        dst = destination / name
        status = "SKIP (already exists)" if dst.exists() or dst.is_symlink() else "COPY"
        result.append((name, available[name], dst, status))
    return result


def audit_installable(operations: list[tuple[str, Path, Path, str]]) -> tuple[bool, int]:
    blocked = False
    reviewed = 0
    for name, src, _, status in operations:
        if status != "COPY":
            continue
        result = scan(src)
        for f in result["findings"]:
            print(f"  {f['severity']} {name}/{f['path']}:{f['line']} [{f['rule']}] {f['detail']}")
        if result["decision"] == "BLOCK":
            blocked = True
        if result["findings"]:
            reviewed += 1
    return blocked, reviewed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path, help="Explicit skill directory, e.g. ~/.agents/skills")
    parser.add_argument("--only", nargs="+", help="Optional skill names; unspecified means all")
    parser.add_argument("--apply", action="store_true", help="Copy new skills (default: preview only)")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / "skills"
    original_target = args.target.expanduser()
    if original_target.is_symlink():
        parser.error("Refusing to install into a symlink target")
    target = original_target.resolve()
    try:
        operations = plan(root, target, args.only)
    except ValueError as exc:
        parser.error(str(exc))
    blocked, reviewed = audit_installable(operations)
    for name, _, dst, status in operations:
        print(f"{status}: {name} -> {dst}")
    if blocked:
        print("BLOCKED: high-severity heuristic finding; investigate before installing.")
        return 2
    if reviewed:
        print(f"WARNING: {reviewed} skill(s) have review-level indicators; manual source review required.")
    if not args.apply:
        print("Preview only. Re-run with --apply to copy. Existing skill folders never overwritten.")
        return 0
    copied = 0
    for name, src, dst, status in operations:
        if status == "COPY":
            try:
                shutil.copytree(src, dst, dirs_exist_ok=False)
                copied += 1
            except FileExistsError:
                print(f"SKIP (appeared during install): {dst}")
            except OSError as exc:
                print(f"ERROR copying {name}: {type(exc).__name__}: {exc}")
                return 1
    print(f"Installed {copied} new skill(s); existing paths left untouched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
