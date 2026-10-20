#!/usr/bin/env python3
"""Generate a repeatable baseline or skill-instructed prompt for one case.

The generator does not run the model, install skills, contact networks or
grade responses. Candidate mode prepends a trusted local SKILL.md verbatim.
The resulting file is created NEW and never overwrites user data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

BANNER = ("The following is a **fictional, non-sensitive benchmark**. "
          "Do not inspect private files, run production actions or invent completed "
          "tests. Only use explicitly authorized tools and record uncertainty.\n")


def prepare(data: dict, skills: Path, case_id: str, mode: str) -> str:
    matches = [case for case in data["cases"] if case["id"] == case_id]
    if len(matches) != 1:
        raise ValueError("Unknown or duplicated case ID")
    case = matches[0]
    name = case["skill"]
    skill_path = skills / name / "SKILL.md"
    if not skill_path.is_file() or skill_path.is_symlink():
        raise ValueError("Missing or linked skill")
    if mode not in {"baseline", "candidate"}:
        raise ValueError("Unsupported benchmark mode")
    task = case["prompt"]
    if not isinstance(task, str) or not task.strip():
        raise ValueError("Missing prompt")
    if mode == "baseline":
        return BANNER + "\n" + task.strip() + "\n"
    instruction = skill_path.read_text(encoding="utf-8-sig").strip()
    # Intentional, documented "in-context instruction" treatment, not native skill trigger.
    return BANNER + "\n" + "BENCHMARK SKILL INSTRUCTIONS (from local source):\n" + instruction + (
        "\n\nBENCHMARK TASK (identical text to baseline):\n" + task.strip() + "\n")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True, help="Case ID in evals/29-skill-benchmark.json")
    parser.add_argument("--mode", required=True, choices=["baseline", "candidate"])
    parser.add_argument("--output", type=Path, required=True, help="A NEW path, not an existing file")
    args = parser.parse_args()
    try:
        source = root / "evals/29-skill-benchmark.json"
        manifest = json.loads(source.read_text(encoding="utf-8"))
        task = prepare(manifest, root / "skills", args.case, args.mode)
        out = args.output.expanduser().absolute()
        if out.is_symlink():
            raise ValueError("Output is a symlink")
        with out.open("x", encoding="utf-8") as writer:
            writer.write(task)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    print(f"CREATED {out} ({args.case}, {args.mode}); sha256={hashlib.sha256(task.encode('utf-8')).hexdigest()}")
    print("No model was run, and native skill auto-trigger was NOT tested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
