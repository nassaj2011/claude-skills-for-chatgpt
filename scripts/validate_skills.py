#!/usr/bin/env python3
"""Validate this project's subset of the Agent Skills SKILL.md convention.

Dependency-free by design: we accept only simple, scalar YAML frontmatter
containing name and description (not an arbitrary YAML parser).
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
KEYS = {"name", "description"}


def validate_one(skill_dir: Path) -> list[str]:
    problems: list[str] = []
    path = skill_dir / "SKILL.md"
    if not path.is_file():
        return [f"{path}: missing SKILL.md"]
    content = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    match = FRONTMATTER.match(content)
    if match is None:
        return [f"{path}: missing or malformed frontmatter"]
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            problems.append(f"{path}: not a key: value line: {line!r}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in fields:
            problems.append(f"{path}: duplicate field {key}")
        if key not in KEYS:
            problems.append(f"{path}: unsupported field {key}")
        fields[key] = value
    name = fields.get("name", "")
    description = fields.get("description", "")
    if not NAME.fullmatch(name) or len(name) > 64:
        problems.append(f"{path}: name must be <=64 chars and kebab-case")
    if name != skill_dir.name:
        problems.append(f"{path}: name does not match folder")
    if not (25 <= len(description) <= 1024):
        problems.append(f"{path}: description must be 25..1024 chars")
    if "<" in description or ">" in description:
        problems.append(f"{path}: description contains angle brackets")
    body = content[match.end():].strip()
    if len(body) < 300:
        problems.append(f"{path}: body is too short")
    if "[TODO:" in body:
        problems.append(f"{path}: unresolved TODO placeholder")
    if not body.startswith("# "):
        problems.append(f"{path}: body should start with one heading")
    return problems


def validate_all(skills_root: Path) -> tuple[int, list[str]]:
    if not skills_root.is_dir():
        return 0, [f"{skills_root}: missing skills directory"]
    children = sorted(p for p in skills_root.iterdir() if p.is_dir())
    if not children:
        return 0, [f"{skills_root}: no skills"]
    errors = [error for path in children for error in validate_one(path)]
    return len(children), errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills", type=Path, default=Path(__file__).resolve().parents[1] / "skills")
    args = parser.parse_args()
    count, problems = validate_all(args.skills)
    for problem in problems:
        print("ERROR:", problem)
    if problems:
        print(f"FAIL: checked {count} skill(s), found {len(problems)} problem(s)")
        return 1
    print(f"PASS: validated {count} skill(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
