#!/usr/bin/env python3
"""Create/verify backup-folder SHA-256 manifests without deleting or restoring.

This verifies file integrity only. It does NOT prove DB consistency, PITR or RTO.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


def snapshot(root: Path) -> dict:
    root = root.expanduser().absolute()
    if not root.is_dir() or root.is_symlink():
        raise ValueError("root must be a real directory, not a symlink")
    files: dict[str, dict] = {}
    for directory, dirs, names in os.walk(root, followlinks=False):
        parent = Path(directory)
        if any((parent / d).is_symlink() for d in dirs):
            raise ValueError("symlink directory in snapshot; refusing to follow or attest")
        for name in names:
            p = parent / name
            if p.is_symlink() or not p.is_file():
                raise ValueError(f"symlink or non-file: {p}")
            digest = hashlib.sha256()
            size = 0
            with p.open("rb") as source:
                while chunk := source.read(1024 * 1024):
                    digest.update(chunk)
                    size += len(chunk)
            rel = p.relative_to(root).as_posix()
            files[rel] = {"size": size, "sha256": digest.hexdigest()}
    return {"schema": 1, "algorithm": "sha256", "files": dict(sorted(files.items()))}


def verify(manifest: dict, current: dict) -> list[str]:
    if manifest.get("schema") != 1 or manifest.get("algorithm") != "sha256":
        raise ValueError("Unsupported manifest schema/algorithm")
    expected = manifest["files"]
    actual = current["files"]
    problems = []
    for path in sorted(set(expected) | set(actual)):
        if path not in expected:
            problems.append(f"ADDED: {path}")
        elif path not in actual:
            problems.append(f"MISSING: {path}")
        elif expected[path] != actual[path]:
            problems.append(f"MISMATCH: {path}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="An authorized backup snapshot directory")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", type=Path, help="Write a NEW manifest (never overwrite)")
    mode.add_argument("--verify", type=Path, help="Read an existing manifest and verify every file")
    args = parser.parse_args()
    root = args.root.expanduser().absolute()
    if root.is_symlink():
        parser.error("Refusing a symlink snapshot root")
    manifest_path = (args.write or args.verify).expanduser().resolve()
    if manifest_path == root or root in manifest_path.parents:
        parser.error("Store the manifest OUTSIDE the backed-up folder")
    try:
        current = snapshot(root)
        if args.write:
            with args.write.expanduser().open("x", encoding="utf-8") as out:
                json.dump(current, out, indent=2)
                out.write("\n")
            print(f"CREATED: {args.write} ({len(current['files'])} file(s)). Restore NOT tested.")
            return 0
        manifest = json.loads(args.verify.read_text(encoding="utf-8"))
        problems = verify(manifest, current)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    for p in problems:
        print(p)
    if problems:
        print(f"FAIL: {len(problems)} file-integrity mismatch(es), restore NOT tested.")
        return 2
    print(f"PASS: {len(current['files'])} file(s) match manifest SHA-256, restore NOT tested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
