#!/usr/bin/env python3
"""Reproducible local checksum catalog for published Agent Skills.

A Git revision/tag or verified signature is needed for authenticity.
Checksums alone detect accidental divergence from THIS repo's checked-in catalog.
No network access, user identifiers or tracking.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

PROJECT = "Claude Skills for ChatGPT"
SOURCE = "https://github.com/nassaj2011/claude-skills-for-chatgpt"
VERSION = "v0.5.0"


def build(skills_dir: Path) -> dict:
    if not skills_dir.is_dir():
        raise ValueError("Missing skills directory")
    entries = []
    for folder in sorted(skills_dir.iterdir()):
        if not folder.is_dir() or folder.is_symlink():
            raise ValueError(f"Unexpected skill entry: {folder.name}")
        skill = folder / "SKILL.md"
        if not skill.is_file() or skill.is_symlink():
            raise ValueError(f"Missing or linked SKILL.md: {folder.name}")
        content = skill.read_bytes().replace(b"\r\n", b"\n")
        entries.append({"name": folder.name, "path": "skills/" + folder.name + "/SKILL.md",
                        "sha256": hashlib.sha256(content).hexdigest()})
    return {"schema": 1, "project": PROJECT, "source": SOURCE, "version": VERSION,
            "hash_normalization": "CRLF-to-LF",
            "tracking": False, "contains_user_identity": False, "skills": entries}


def verify(catalog: dict, current: dict) -> list[str]:
    errors = []
    for key in ("schema", "project", "source", "version", "hash_normalization", "tracking", "contains_user_identity"):
        if catalog.get(key) != current[key]:
            errors.append(f"Catalog metadata mismatch: {key}")
    expected = {e["name"]: e for e in catalog.get("skills", [])}
    actual = {e["name"]: e for e in current["skills"]}
    if len(expected) != len(catalog.get("skills", [])):
        errors.append("Duplicate names in catalog")
    if set(actual) != set(expected):
        errors.append("Skill inventory differs")
    for name in sorted(set(actual) & set(expected)):
        if actual[name] != expected[name]:
            errors.append(f"Content mismatch: {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills", type=Path, default=Path(__file__).resolve().parents[1] / "skills")
    parser.add_argument("--catalog", type=Path, default=Path(__file__).resolve().parents[1] / "CATALOG.json")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true", help="Create a NEW catalog; never overwrite existing one")
    group.add_argument("--refresh", action="store_true", help="Explicitly regenerate this repository\u2019s existing CATALOG.json")
    args = parser.parse_args()
    try:
        current = build(args.skills)
        if args.write:
            with args.catalog.open("x", encoding="utf-8") as output:
                json.dump(current, output, indent=2, ensure_ascii=False)
                output.write("\n")
            print(f"CREATED: {args.catalog} ({len(current['skills'])} skills)")
            return 0
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
        if args.refresh:
            if catalog.get("source") != SOURCE:
                raise ValueError("Refusing to refresh an unrelated source catalog")
            with args.catalog.open("w", encoding="utf-8") as output:
                json.dump(current, output, indent=2, ensure_ascii=False)
                output.write("\n")
            print("REFRESHED: {} ({} skills)".format(args.catalog, len(current["skills"])))
            return 0
        errors = verify(catalog, current)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    for issue in errors:
        print("ERROR:", issue)
    if errors:
        return 2
    print(f"PASS: {len(current['skills'])} skill SHA-256 entries match CATALOG.json. Authenticity NOT certified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
