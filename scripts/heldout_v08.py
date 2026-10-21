#!/usr/bin/env python3
"""Deterministic prompt construction for 87 held-out skill cases.

Three arms: baseline, generic length-matched active control, and canonical skill.
No model calls are made by this script, and no original skills are modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "evals/v08/heldout_87.json"

CONTROL_PARAS = [
    "Review the task request carefully and identify the requested deliverable, the context supplied, and any unresolved assumptions. Organize the response so that a future reader can distinguish the user's supplied facts from your proposed choices. Explain any constraints in plain language.",
    "State what information you can verify with the context available. When the request involves an external dependency, an uncertain environment, a policy interpretation, or a numerical estimate, describe the missing evidence without making up a completed inspection. Favor clear output artifacts.",
    "Before finalizing, inspect your response for internal contradictions, ambiguous terms, unjustified absolutes, overlooked edge cases and unqualified claims. If a claim is unverified, make that limitation visible. Separate your recommendations from facts.",
    "Keep recommendations feasible and proportionate to the scenario. Present steps in an order that another person could follow, indicate the owner of decisions, and avoid unexplained acronyms or reliance on unspecified resources. Match the requested output format.",
    "Use examples sparingly and make them fictional when no verified example is available. Mark proposed checks as proposed, explain the acceptance evidence that would be necessary and refrain from claiming any external work was completed. Prefer reversible actions.",
    "Respect access boundaries, confidentiality and the user's authority to decide. Do not request unnecessary sensitive data, add hidden actions, use external connections or overwrite original material. If necessary tools are absent, provide inspectable instructions rather than pretending to act.",
    "For recommendations and specifications, include a short record of relevant caveats and tradeoffs that affect the choice. Be concise but complete. Avoid repeating slogans, filler or generic best-practice lists that fail to answer the specific request.",
    "Check that proposed outcomes can be evaluated rather than relying on subjective enthusiasm. Name the expected artifacts and explain what can be measured later, while avoiding new requirements not justified by the request or available evidence.",
]
STANDARD = ("You are comparing a fictional, non-sensitive software engineering case. "
            "Do not use external tools, inspect private files, contact services or claim "
            "that any checks were executed. For code-production cases, output ONLY "
            "valid Python source for the requested function; otherwise explain evidence "
            "and concrete acceptance tests. No network, personal data or unapproved changes.\n")

def load_cases():
    cases = json.loads(BANK.read_text(encoding="utf-8"))["cases"]
    if len(cases) != 87 or len({x["id"] for x in cases}) != 87:
        raise ValueError("Bank should hold 87 unique cases")
    return cases

def skill_body(skill: str) -> str:
    f = ROOT / "skills" / skill / "SKILL.md"
    if f.is_symlink() or not f.is_file():
        raise ValueError("Invalid skill path")
    return f.read_text(encoding="utf-8-sig").replace("\r\n", "\n").strip()

def neutral_control(target_len: int) -> str:
    """Match character count only: semantic/token equivalence is NOT asserted."""
    prefix = "GENERAL WRITING AND REVIEW GUIDELINES (not specific to any domain):\n"
    parts = []
    idx = 0
    while len(prefix + "\n\n".join(parts)) < target_len:
        parts.append(CONTROL_PARAS[idx % len(CONTROL_PARAS)])
        idx += 1
    result = prefix + "\n\n".join(parts)
    # Exactly match length using a partial last paragraph (characters, not tokens).
    return result[:target_len]

def task_text(case: dict) -> str:
    return (f"HELD-OUT CASE ID: {case['id']}\n\nTASK:\n{case['task']}\n\n"
            + (f"CODE EVALUATION CONTRACT:\n{case['code_contract']['contract']}\n\n"
               if case["kind"] == "code-python" else
               "EXPECTED RESPONSE: scenario-specific practical artifact; include risk reasoning, "
               "acceptance/negative checks, honest evidence limits and explicit next steps.\n\n"))

def prompt(case_id: str, arm: str) -> str:
    case = next((x for x in load_cases() if x["id"] == case_id), None)
    if case is None or arm not in {"baseline", "active_control", "candidate"}:
        raise ValueError("Unknown case or arm")
    skill = skill_body(case["skill"])
    task = task_text(case)
    prefix = ""
    if arm == "candidate":
        prefix = "SPECIALIST GUIDELINES:\n" + skill
    elif arm == "active_control":
        prefix = neutral_control(len("SPECIALIST GUIDELINES:\n" + skill))
    return STANDARD + (prefix + "\n\n" if prefix else "") + task

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--case", required=True)
    p.add_argument("--arm", choices=["baseline", "active_control", "candidate"], required=True)
    p.add_argument("--digest-only", action="store_true")
    a = p.parse_args()
    result = prompt(a.case, a.arm)
    if a.digest_only:
        print(json.dumps({"id":a.case,"arm":a.arm,"chars":len(result),
                          "sha256":hashlib.sha256(result.encode("utf-8")).hexdigest()}))
    else:
        print(result, end="")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
