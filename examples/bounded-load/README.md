# Safe, strictly local load-testing reference

The standard-library harness creates its own HTTP fixture on 127.0.0.1 using an ephemeral port. It is **not** capable of accepting an external URL, a real web app or production credentials. Hard limits: 60 requests and 6 workers, 0.1–5 second timeouts. Each request measures actual client-observed elapsed time and status; output includes p50/p95/p99 and achieved throughput.

Run: python examples/bounded-load/loopback_harness.py --requests 24 --workers 4

Tests: python -m unittest discover -s examples/bounded-load -p "test_*.py" -v

Do not use these tiny localhost timings for infrastructure sizing: they measure a deliberately artificial 2ms handler and local scheduling overhead. For a real target, first establish explicit authorization, an isolated environment, spend/rate/duration caps, metrics and a stop plan. A web-only ChatGPT user should request the test design and mark all execution NOT RUN.
