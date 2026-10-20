"""Offline example: SLO gate on synthetic sanitized request records.

NOT live monitoring. Parses bounded JSONL and calculates request success / p95.
No network or external services; content must exclude personal data.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

BLOCKED_FIELDS = {"email", "password", "phone", "token", "access_token", "authorization", "user_id", "ip_address"}


def evaluate(events: list[dict], *, min_availability: float = 0.99,
             max_p95_ms: float = 500) -> dict:
    if not events:
        raise ValueError("Cannot approve on an empty dataset")
    if not 0 < min_availability <= 1 or max_p95_ms <= 0:
        raise ValueError("Invalid threshold")
    for idx, event in enumerate(events):
        if set(event) & BLOCKED_FIELDS:
            raise ValueError(f"Record {idx} contains a sensitive field")
        if set(event) != {"status", "latency_ms"}:
            raise ValueError(f"Record {idx} has missing or unexpected fields")
        status = event["status"]
        latency = event["latency_ms"]
        if not isinstance(status, int) or isinstance(status, bool) or not 100 <= status < 600:
            raise ValueError("Invalid HTTP status")
        if not isinstance(latency, (int, float)) or isinstance(latency, bool) or not math.isfinite(latency) or latency < 0:
            raise ValueError("Invalid latency")
    availability = sum(event["status"] < 500 for event in events) / len(events)
    sorted_latency = sorted(float(event["latency_ms"]) for event in events)
    p95_index = max(0, math.ceil(0.95 * len(sorted_latency)) - 1)
    p95_ms = sorted_latency[p95_index]
    return {
        "sample_size": len(events),
        "availability": round(availability, 6),
        "p95_ms": round(p95_ms, 2),
        "availability_met": availability >= min_availability,
        "latency_met": p95_ms <= max_p95_ms,
        "decision": "PASS" if availability >= min_availability and p95_ms <= max_p95_ms else "BLOCK",
        "note": "Offline synthetic/approved sanitized sample only. Not proof of production SLO or release readiness.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", type=Path, required=True)
    parser.add_argument("--min-availability", type=float, default=0.99)
    parser.add_argument("--max-p95-ms", type=float, default=500)
    args = parser.parse_args()
    try:
        events = [json.loads(line) for line in args.sample.read_text(encoding="utf-8").splitlines() if line.strip()]
        report = evaluate(events, min_availability=args.min_availability, max_p95_ms=args.max_p95_ms)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2))
    return int(report["decision"] != "PASS")


if __name__ == "__main__":
    raise SystemExit(main())
