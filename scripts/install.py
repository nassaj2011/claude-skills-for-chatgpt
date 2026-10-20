#!/usr/bin/env python3
"""Preview or safely copy original Agent Skills into a target directory.

No overwrite, no deletion, no network access and no third-party packages.
Use --apply to actually copy. The target is intentionally explicit.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from validate_skills import validate_all


def plan(skills_root: Path, destination: Path, selected: list[str] | None) -> list[tuple[str, Path, Path, str]]:
    count, errors = validate_all(skills_root)
    if errors or count == 0:
        raise ValueError("Invalid source skills:\n" + "\n".join(errors))
    available = {p.name: p for p in skills_root.iterdir() if p.is_dir()}
    names = sorted(available) if not selected else list(dict.fromkeys(selected))
    unknown = [name for name in names if name not in available]
    if unknown:
        raise ValueError("Unknown skill(s): " + ", ".join(unknown))
    result = []
    for name in names:
        dst = destination / name
        status = "SKIP (already exists)" if dst.exists() else "COPY"
        result.append((name, available[name], dst, status))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path, help="Explicit skills directory, e.g. ~/.agents/skills")
    parser.add_argument("--only", nargs="+", help="Optional skill folder names")
    parser.add_argument("--apply", action="store_true", help="Actually copy new skills (default: preview)")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1] / "skills"
    target = args.target.expanduser().resolve()
    try:
        operations = plan(root, target, args.only)
    except ValueError as exc:
        parser.error(str(exc))
    copied = 0
    for name, src, dst, status in operations:
        print(f"{status}: {name} -> {dst}")
        if args.apply and status == "COPY":
            # race-safe: copytree refuses to overwrite if destination appeared
            try:
                shutil.copytree(src, dst, dirs_exist_ok=False)
                copied += 1
            except FileExistsError:
                print(f"SKIP (appeared during install): {dst}")
    if args.apply:
        print(f"Installed {copied} new skill(s); existing paths left untouched.")
    else:
        print("Preview only. Run again with --apply to copy; existing skills will never be overwritten.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
