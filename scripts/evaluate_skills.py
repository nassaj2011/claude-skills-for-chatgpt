#!/usr/bin/env python3
"""Compare scored agent runs with and without a skill.

Does not call a model, invent execution evidence, or auto-grade correctness.
Independent reviewers attach evidence to each boolean rubric judgment.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def compare(cases: dict, baseline: dict, candidate: dict) -> dict:
    by_id: dict[str, dict] = {}
    for case in cases.get("cases", []):
        key = case["id"]
        if key in by_id:
            raise ValueError(f"Duplicate case: {key}")
        if not case.get("criteria"):
            raise ValueError(f"Case {key}: missing rubric criteria")
        by_id[key] = case

    if not by_id:
        raise ValueError("No evaluation cases provided")

    def grade(run: dict, label: str) -> tuple[dict[str, dict], float]:
        meta = run.get("metadata", {})
        if not isinstance(meta.get("synthetic"), bool):
            raise ValueError(f"{label}: metadata.synthetic must explicitly be true or false")
        results = run.get("results", {})
        if set(results) != set(by_id):
            raise ValueError(f"{label}: case IDs differ from the rubric: {sorted(set(results) ^ set(by_id))}")
        graded = {}
        earned_total, max_total = 0.0, 0.0
        for cid, case in by_id.items():
            rubric = {c["id"]: c for c in case["criteria"]}
            if len(rubric) != len(case["criteria"]):
                raise ValueError(f"{cid}: duplicate criterion IDs")
            judgments = results[cid]
            if set(judgments) != set(rubric):
                raise ValueError(f"{label}/{cid}: criterion IDs do not match")
            earned, possible = 0.0, 0.0
            for rid, criterion in rubric.items():
                weight = criterion.get("weight", 1)
                if not isinstance(weight, (int, float)) or isinstance(weight, bool) or not 0 < weight <= 10:
                    raise ValueError(f"{cid}/{rid}: weight must be between 0 and 10")
                outcome = judgments[rid]
                if not isinstance(outcome, dict) or not isinstance(outcome.get("passed"), bool):
                    raise ValueError(f"{label}/{cid}/{rid}: passed must be boolean")
                evidence = outcome.get("evidence")
                if not isinstance(evidence, str) or not evidence.strip():
                    raise ValueError(f"{label}/{cid}/{rid}: evidence required even when failed")
                possible += weight
                earned += weight if outcome["passed"] else 0
            graded[cid] = {"score": round(earned / possible, 4), "earned": earned, "possible": possible}
            earned_total += earned
            max_total += possible
        return graded, round(earned_total / max_total, 4)

    base, base_score = grade(baseline, "baseline")
    next_, next_score = grade(candidate, "candidate")
    synthetic = bool(baseline["metadata"]["synthetic"] or candidate["metadata"]["synthetic"])
    return {
        "evaluation_type": "SYNTHETIC_DEMONSTRATION" if synthetic else "HUMAN_SCORED_AGENT_RUNS",
        "disclaimer": "Scores reflect supplied reviewer judgments. They do not prove correctness, reliability or causal impact.",
        "baseline_metadata": baseline["metadata"],
        "candidate_metadata": candidate["metadata"],
        "baseline_score": base_score,
        "candidate_score": next_score,
        "absolute_change": round(next_score - base_score, 4),
        "cases": [
            {
                "id": cid,
                "skill": case.get("skill"),
                "baseline": base[cid]["score"],
                "candidate": next_[cid]["score"],
                "delta": round(next_[cid]["score"] - base[cid]["score"], 4),
            }
            for cid, case in by_id.items()
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable report")
    parser.add_argument("--require-real", action="store_true", help="Reject synthetic example runs")
    args = parser.parse_args()
    try:
        report = compare(read_json(args.cases), read_json(args.baseline), read_json(args.candidate))
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    if args.require_real and report["evaluation_type"] == "SYNTHETIC_DEMONSTRATION":
        parser.error("Synthetic demonstration scores are not evidence of real agent runs")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(report["evaluation_type"])
        print(f"Baseline: {report['baseline_score']:.1%}, with-skill: {report['candidate_score']:.1%}, delta: {report['absolute_change']:+.1%}")
        for row in report["cases"]:
            print(f"  {row['id']}: {row['baseline']:.1%} -> {row['candidate']:.1%} ({row['delta']:+.1%})")
        print("Scores are supplied human judgments, not automatic proof of agent quality.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
