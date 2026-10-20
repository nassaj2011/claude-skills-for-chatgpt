#!/usr/bin/env python3
"""Offline privacy data-flow inventory lint for a fictional app.

No user data, network, external dependencies or claim of legal certification.
Produces actionable findings from a declared project-specific JSON contract.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SENSITIVE = {"name", "phone", "email", "address", "free_text", "user_id", "booking_id"}
PUBLIC_PSEUDONYMOUS = {"daily_count", "total_revenue_bucket", "event_type", "anonymous_session"}
MESSAGING_ALLOW = {"phone", "message_template"}
REQUIRED = {
    "field", "classification", "purpose", "source", "retention_trigger",
    "deletion_path", "access_roles", "recipients", "legal_basis_review",
}


def validate(data: dict) -> dict:
    if not isinstance(data, dict) or not isinstance(data.get("fields"), list) or not data["fields"]:
        raise ValueError("Inventory must contain a nonempty fields array")
    findings: list[dict] = []
    seen = set()

    def fail(rule: str, field: str, details: str, severity="HIGH") -> None:
        findings.append({"rule": rule, "field": field, "severity": severity, "details": details})

    for i, item in enumerate(data["fields"]):
        if not isinstance(item, dict) or not REQUIRED.issubset(item):
            fail("incomplete-record", f"row:{i}", "Inventory record missing required fields")
            continue
        name = item["field"]
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z_0-9]{0,63}", name):
            fail("invalid-field", str(name), "Use field identifiers rather than values")
            continue
        if name in seen:
            fail("duplicate", name, "Field appears more than once")
        seen.add(name)
        for key in ("classification", "purpose", "source", "retention_trigger", "deletion_path"):
            if not isinstance(item[key], str) or not item[key].strip() or item[key].strip().lower() in {"unknown", "tbd", "none"}:
                fail("missing-governance", name, f"Missing/undecided {key}")
        if not isinstance(item["access_roles"], list) or not item["access_roles"] or any(
            not isinstance(x, str) or not x.strip() for x in item["access_roles"]
        ):
            fail("access-scope", name, "Non-empty, explicit access roles required")
        if item["legal_basis_review"] not in {"REVIEWED", "PENDING"}:
            fail("legal-review", name, "Record REVIEWED or PENDING; do not infer legal compliance", "REVIEW")
        elif item["legal_basis_review"] == "PENDING":
            fail("legal-review-pending", name, "Qualified review remains outstanding", "REVIEW")
        recipients = item["recipients"]
        if not isinstance(recipients, list):
            fail("invalid-recipients", name, "Recipients must be a list")
            continue
        for recipient in recipients:
            if not isinstance(recipient, dict) or not isinstance(recipient.get("name"), str):
                fail("invalid-recipient", name, "Recipient must have a declared system name")
                continue
            destination = recipient["name"].lower()
            if destination == "analytics" and name not in PUBLIC_PSEUDONYMOUS:
                fail("analytics-pii", name, "Do not send direct or linkable personal fields to analytics")
            if destination == "messaging" and name not in MESSAGING_ALLOW:
                fail("overdisclosure", name, "Messaging vendor should receive only destination and template")
            if destination in {"public", "public_export"} and name in SENSITIVE:
                fail("public-personal-data", name, "Cannot publish identifiable fields")
            if destination not in {"analytics", "messaging", "primary_db", "support", "public", "public_export"}:
                fail("undocumented-recipient", name, f"Recipient {destination} needs documented policy", "REVIEW")

    high = sum(x["severity"] == "HIGH" for x in findings)
    return {"decision": "BLOCK" if high else ("REVIEW" if findings else "PASS"),
            "fields_reviewed": len(data["fields"]), "high_findings": high,
            "findings": findings,
            "disclaimer": "Declared inventory only; cannot prove a live app follows it or meets any law."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    try:
        out = validate(json.loads(args.input.read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
