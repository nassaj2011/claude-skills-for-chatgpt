#!/usr/bin/env python3
"""Bounded HTTP test ONLY against an HTTP server created by this process.

Synthetic workload; no arbitrary URLs, auth, payments or third-party requests.
Request cap <=60, workers <=6, per-call timeout and explicit local shutdown.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import math
import threading
import time
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MAX_REQUESTS = 60
MAX_WORKERS = 6


class TinyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/synthetic-health":
            self.send_error(404)
            return
        time.sleep(.002)  # artificial service-time, not an app benchmark
        payload = b'{"ok":true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


def percentile(samples: list[float], percentile_value: float) -> float:
    if not samples or not 0 < percentile_value <= 100:
        raise ValueError("Invalid percentile input")
    ordered = sorted(samples)
    return ordered[math.ceil((percentile_value / 100) * len(ordered)) - 1]


def run(requests: int = 24, workers: int = 4, timeout: float = 1.0) -> dict:
    if (not isinstance(requests, int) or isinstance(requests, bool)
            or not 1 <= requests <= MAX_REQUESTS):
        raise ValueError("requests must be 1..60")
    if (not isinstance(workers, int) or isinstance(workers, bool)
            or not 1 <= workers <= MAX_WORKERS):
        raise ValueError("workers must be 1..6")
    if (not isinstance(timeout, (int, float)) or not 0.1 <= timeout <= 5.0):
        raise ValueError("timeout must be between 0.1 and 5 seconds")
    server = ThreadingHTTPServer(("127.0.0.1", 0), TinyHandler)
    background = threading.Thread(target=server.serve_forever, daemon=True)
    background.start()
    def call(_: int) -> tuple[float, int]:
        begin = time.perf_counter()
        client = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=timeout)
        try:
            client.request("GET", "/synthetic-health")
            response = client.getresponse()
            status = response.status
            if response.read() != b'{"ok":true}':
                status = 502
        except (TimeoutError, OSError, http.client.HTTPException):
            status = 599
        finally:
            client.close()
        return (time.perf_counter() - begin) * 1000, status

    try:
        started = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            outcomes = list(pool.map(call, range(requests)))
        elapsed = time.perf_counter() - started
    finally:
        server.shutdown()
        server.server_close()
        background.join(timeout=5)
    latencies = [duration for duration, _ in outcomes]
    error_count = sum(not 200 <= status < 400 for _, status in outcomes)
    result = {"mode": "isolated loopback synthetic HTTP fixture",
              "authorized_target": "127.0.0.1 allocated by this process",
              "requested": requests, "observed": len(outcomes), "workers": workers,
              "duration_seconds": round(elapsed, 4),
              "achieved_rps": round(len(outcomes) / elapsed, 2),
              "errors": error_count, "p50_ms": round(percentile(latencies, 50), 3),
              "p95_ms": round(percentile(latencies, 95), 3),
              "p99_ms": round(percentile(latencies, 99), 3),
              "status": "PASS" if error_count == 0 else "FAIL",
              "warning": "NOT evidence of a real application's capacity or production SLO."}
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requests", type=int, default=24)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=float, default=1.0)
    args = parser.parse_args()
    try:
        report = run(args.requests, args.workers, args.timeout)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
