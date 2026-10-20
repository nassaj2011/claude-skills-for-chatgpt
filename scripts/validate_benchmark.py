#!/usr/bin/env python3
"""Validate all 29 skill benchmark specifications, not agent success.

This file makes no model calls. A valid case is not a completed evaluation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def validate(skills: Path, manifest: Path) -> tuple[int, list[str]]:
    data = json.loads(manifest.read_text(encoding="utf-8"))
    problems: list[str] = []
    entries = data.get("cases")
    if not isinstance(entries, list):
        return 0, ["cases must be a list"]
    expected = {p.name for p in skills.iterdir() if p.is_dir()}
    seen = set()
    seen_ids = set()
    for index, case in enumerate(entries):
        if not isinstance(case, dict):
            problems.append(f"case #{index} not an object")
            continue
        name = case.get("skill")
        cid = case.get("id")
        if not isinstance(name, str) or not isinstance(cid, str):
            problems.append(f"case #{index} lacks skill/id")
            continue
        if name in seen or cid in seen_ids:
            problems.append(f"duplicate skill or case ID: {name}/{cid}")
        seen.add(name)
        seen_ids.add(cid)
        if case.get("execution_status") != "NOT_RUN" or case.get("score", "MISSING") is not None:
            problems.append(f"{cid}: unexecuted benchmark must have status NOT_RUN and score=null")
        for field in ("scenario", "task", "prompt", "negative_routing", "expected_artifact"):
            if not isinstance(case.get(field), str) or len(case[field].strip()) < 25:
                problems.append(f"{cid}: missing/short {field}")
        criteria = case.get("criteria", [])
        if not isinstance(criteria, list) or len(criteria) < 3:
            problems.append(f"{cid}: at least three acceptance criteria required")
            continue
        if len({x.get("id") for x in criteria if isinstance(x, dict)}) != len(criteria):
            problems.append(f"{cid}: duplicate criterion IDs")
        for criterion in criteria:
            if (not isinstance(criterion, dict)
                    or not isinstance(criterion.get("weight"), int)
                    or criterion["weight"] <= 0
                    or len(str(criterion.get("description", "")).strip()) < 15):
                problems.append(f"{cid}: invalid criterion")
    if seen != expected:
        problems.append(f"Skill catalog differs: missing={sorted(expected-seen)}, extra={sorted(seen-expected)}")
    if data.get("status") != "DESIGNED_NOT_EXECUTED":
        problems.append("manifest status must not claim executed results")
    return len(entries), problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    repo = Path(__file__).resolve().parents[1]
    parser.add_argument("--manifest", type=Path, default=repo / "evals/29-skill-benchmark.json")
    parser.add_argument("--skills", type=Path, default=repo / "skills")
    args = parser.parse_args()
    try:
        count, errors = validate(args.skills, args.manifest)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print(f"PASS: {count} scenario specifications cover every skill. Real runs NOT implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
