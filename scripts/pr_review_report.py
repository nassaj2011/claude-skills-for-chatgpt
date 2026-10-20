#!/usr/bin/env python3
"""Produce a READ-ONLY GitHub PR review evidence report.

Requires authenticated GitHub CLI (gh). Does not modify or merge the PR.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess

REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def summarize(pr: dict, inline: list[dict], discussion: list[dict]) -> dict:
    checks = pr.get("statusCheckRollup") or []
    report_checks = []
    for c in checks:
        state = (c.get("conclusion") or c.get("state") or c.get("status") or "UNKNOWN").upper()
        report_checks.append({"name": c.get("name") or c.get("context") or "unnamed", "state": state})
    bad = {"FAILURE", "FAILED", "ERROR", "TIMED_OUT", "CANCELLED", "ACTION_REQUIRED"}
    pending = {"PENDING", "IN_PROGRESS", "QUEUED", "REQUESTED", "WAITING", "UNKNOWN", "EXPECTED"}
    status = (
        "CHECKS_FAILING" if any(c["state"] in bad for c in report_checks)
        else "CHECKS_INCOMPLETE" if not report_checks or any(c["state"] in pending for c in report_checks)
        else "CHECKS_REPORTED_COMPLETE"
    )
    return {
        "number": pr.get("number"),
        "title": pr.get("title"),
        "url": pr.get("url"),
        "head_sha": pr.get("headRefOid"),
        "base_sha": pr.get("baseRefOid"),
        "merge_state": pr.get("mergeStateStatus"),
        "review_decision": pr.get("reviewDecision") or "NOT_REPORTED",
        "check_summary": status,
        "checks": report_checks,
        "review_count": len(pr.get("reviews") or []),
        "general_comment_count": len(discussion),
        "inline_comment_count": len(inline),
        "inline_findings": [
            {"path": c.get("path"), "line": c.get("line") or c.get("original_line"), "url": c.get("html_url")}
            for c in inline
        ],
        "caveats": [
            "An API list of inline comments does not confirm which review threads are resolved.",
            "Check status alone is not a complete release/security review.",
            "The script does not inspect the actual diff; read the diff and code before a merge recommendation.",
        ],
    }


def gh_json(args: list[str]) -> object:
    call = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", timeout=60, check=False)
    if call.returncode:
        raise RuntimeError(f"gh command failed (exit {call.returncode}): {call.stderr.strip()[:500]}")
    return json.loads(call.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--pr", required=True, type=int, help="Pull request number")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not REPO.fullmatch(args.repo) or args.pr <= 0:
        parser.error("Use a valid owner/repo and positive PR number")
    try:
        fields = "number,title,url,headRefOid,baseRefOid,reviewDecision,mergeStateStatus,statusCheckRollup,reviews"
        pr = gh_json(["pr", "view", str(args.pr), "-R", args.repo, "--json", fields])
        comments = gh_json(["api", "--paginate", f"repos/{args.repo}/pulls/{args.pr}/comments"])
        discussion = gh_json(["api", "--paginate", f"repos/{args.repo}/issues/{args.pr}/comments"])
        if not isinstance(pr, dict) or not isinstance(comments, list) or not isinstance(discussion, list):
            raise ValueError("Unexpected GitHub CLI JSON response")
        report = summarize(pr, comments, discussion)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        parser.error(f"Cannot establish review evidence: {exc}")
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"PR #{report['number']} {report['title']}\n{report['url']}")
        print(f"SHA {report['head_sha']} | {report['check_summary']} | reviews: {report['review_decision']}")
        print(f"Comments: {report['inline_comment_count']} inline; {report['general_comment_count']} general")
        for c in report["checks"]:
            print(f"  {c['name']}: {c['state']}")
        for caveat in report["caveats"]:
            print("CAVEAT:", caveat)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
