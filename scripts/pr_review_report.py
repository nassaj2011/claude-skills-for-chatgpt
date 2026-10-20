#!/usr/bin/env python3
"""Produce a read-only evidence snapshot of a GitHub Pull Request.

Uses authenticated gh CLI. All API calls read data; never comments/merges.
Not a substitute for code review or release approval.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess

REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
SUCCESS = {"SUCCESS", "PASSED"}
FAILURE = {"FAILURE", "FAILED", "ERROR", "TIMED_OUT", "CANCELLED", "ACTION_REQUIRED"}
PENDING = {"PENDING", "IN_PROGRESS", "QUEUED", "REQUESTED", "WAITING", "EXPECTED"}
NEUTRAL = {"NEUTRAL", "SKIPPED", "STALE", "UNKNOWN", "NOT_APPLICABLE"}
THREAD_QUERY = """query($owner:String!,$name:String!,$number:Int!,$cursor:String) {
 repository(owner:$owner,name:$name) {
  pullRequest(number:$number) {
   reviewThreads(first:100,after:$cursor) {
    pageInfo { hasNextPage endCursor }
    nodes { isResolved isOutdated }
   }
  }
 }
}"""


def flatten_pages(parsed: object) -> list[dict]:
    """gh api --paginate --slurp returns list of response pages."""
    if not isinstance(parsed, list):
        raise ValueError("Expected a list of paginated responses")
    result = []
    for page in parsed:
        if not isinstance(page, list):
            raise ValueError("Unexpected paginated response shape")
        for item in page:
            if not isinstance(item, dict):
                raise ValueError("Unexpected PR comment payload")
            result.append(item)
    return result


def summarize(pr: dict, inline: list[dict], discussion: list[dict], threads: dict | None = None) -> dict:
    checks = pr.get("statusCheckRollup") or []
    report_checks = []
    for c in checks:
        if not isinstance(c, dict):
            continue
        raw = c.get("conclusion") or c.get("state") or c.get("status") or "UNKNOWN"
        state = str(raw).upper()
        report_checks.append({"name": c.get("name") or c.get("context") or "unnamed", "state": state})
    states = {c["state"] for c in report_checks}
    if states & FAILURE:
        check_summary = "CHECKS_FAILING"
    elif not report_checks or any(state not in SUCCESS for state in states):
        # Skipped/neutral/unknown are NOT evidence that required checks passed.
        check_summary = "CHECKS_INCOMPLETE"
    else:
        check_summary = "CHECKS_REPORTED_COMPLETE"

    info = threads or {"status": "NOT_CHECKED", "total": None, "unresolved": None}
    if info.get("status") != "COMPLETE":
        info = {"status": "NOT_CHECKED", "total": None, "unresolved": None}
    decision = pr.get("reviewDecision") or "NOT_REPORTED"
    caveats = [
        "Successful reported checks may omit required branch-protection rules: check actual repository policy.",
        "Review decision and resolved threads do not replace inspecting the code diff and authorization.",
        "An API list of inline comments does not confirm whether review threads are resolved.",
        "Missing or incomplete thread data must not be treated as resolved.",
    ]
    return {
        "number": pr.get("number"),
        "title": pr.get("title"),
        "url": pr.get("url"),
        "head_sha": pr.get("headRefOid"),
        "base_sha": pr.get("baseRefOid"),
        "merge_state": pr.get("mergeStateStatus"),
        "review_decision": decision,
        "check_summary": check_summary,
        "checks": report_checks,
        "review_count": len(pr.get("reviews") or []),
        "general_comment_count": len(discussion),
        "inline_comment_count": len(inline),
        "inline_findings": [
            {"path": c.get("path"), "line": c.get("line") or c.get("original_line"), "url": c.get("html_url")}
            for c in inline
        ],
        "review_threads": info,
        "evidence_ready": bool(
            check_summary == "CHECKS_REPORTED_COMPLETE"
            and decision == "APPROVED"
            and info.get("status") == "COMPLETE"
            and info.get("unresolved") == 0
        ),
        "caveats": caveats,
    }


def gh_json(args: list[str]) -> object:
    call = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", timeout=90, check=False)
    if call.returncode:
        # Avoid accidentally surfacing tokens or user data from full stdout.
        raise RuntimeError(f"gh failed (exit {call.returncode}); check authentication/API permissions")
    return json.loads(call.stdout)


def gh_comments(repo: str, pr: int, endpoint: str) -> list[dict]:
    response = gh_json(["api", "--paginate", "--slurp", f"repos/{repo}/{endpoint}/{pr}/comments?per_page=100"])
    return flatten_pages(response)


def gh_review_threads(repo: str, number: int) -> dict:
    owner, name = repo.split("/", 1)
    cursor: str | None = None
    total, unresolved = 0, 0
    for _ in range(30):  # 3000 thread cap, no silent truncation
        args = ["api", "graphql", "-f", f"query={THREAD_QUERY}", "-f", f"owner={owner}",
                "-f", f"name={name}", "-F", f"number={number}"]
        if cursor is not None:
            args += ["-f", f"cursor={cursor}"]
        response = gh_json(args)
        connection = response["data"]["repository"]["pullRequest"]["reviewThreads"]
        nodes = connection["nodes"]
        total += len(nodes)
        unresolved += sum(not n["isResolved"] for n in nodes)
        page = connection["pageInfo"]
        if not page["hasNextPage"]:
            return {"status": "COMPLETE", "total": total, "unresolved": unresolved}
        cursor = page.get("endCursor")
        if not cursor or not nodes:
            break
    return {"status": "NOT_CHECKED", "total": None, "unresolved": None}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not REPO.fullmatch(args.repo) or args.pr <= 0:
        parser.error("Use valid owner/repo and positive PR number")
    try:
        fields = "number,title,url,headRefOid,baseRefOid,reviewDecision,mergeStateStatus,statusCheckRollup,reviews"
        pr = gh_json(["pr", "view", str(args.pr), "-R", args.repo, "--json", fields])
        inline = gh_comments(args.repo, args.pr, "pulls")
        discussion = gh_comments(args.repo, args.pr, "issues")
        if not isinstance(pr, dict):
            raise ValueError("Unexpected PR payload")
        try:
            threads = gh_review_threads(args.repo, args.pr)
        except (KeyError, TypeError, ValueError, RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError):
            threads = {"status": "NOT_CHECKED"}
        report = summarize(pr, inline, discussion, threads)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        parser.error(f"Cannot establish PR review evidence: {type(exc).__name__}: {exc}")
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"PR #{report['number']}: {report['title']}\n{report['url']}")
        print(f"SHA {report['head_sha']} | {report['check_summary']} | reviewer decision: {report['review_decision']}")
        print(f"Comments: {report['inline_comment_count']} inline; {report['general_comment_count']} general")
        print(f"Threads: {report['review_threads']}")
        print(f"Evidence-ready for further manual review: {report['evidence_ready']}")
        for check in report["checks"]:
            print(f"  {check['name']}: {check['state']}")
        for caveat in report["caveats"]:
            print("CAVEAT:", caveat)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
