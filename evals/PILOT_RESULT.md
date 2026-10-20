# First genuine-model A/B pilot — 2026-10-20

**Result: no measured improvement in one limited review case.** The baseline Codex run correctly declined to merge; adding `code-review-pr` instruction content did not improve the three rubric checks.

| | Baseline | With SKILL.md prepended |
| --- | --- | --- |
| Target | Fictional money-transfer PR, lacking authorization tests | Identical scenario |
| Agent/model | Codex CLI 0.147.0 / `gpt-5.6-terra` | Same |
| Environment | Read-only, ephemeral, no repository/network inspection instructed | Same |
| Rubric result | 7/7 = 100% | 7/7 = 100% |
| Reported tokens used (CLI) | 17,656 | 14,273 |
| Main conclusion | Do not merge; server-side ownership tests missing | NEEDS CHANGES; same concerns with a structured evidence table |

See [raw baseline response](runs/pilot-pr-baseline.txt), [raw candidate response](runs/pilot-pr-candidate.txt), [pilot rubric](pilot_cases.json) and [scored records](runs/).

**Caveats:** One fictional prompt only; the scorer was not blind or independent. Candidate included the content of the SKILL.md in the prompt rather than verifying Codex's native auto-trigger. Code Mode execution host was unavailable, so the run tested text reasoning, not tool-based repository inspection. Token counts reflect CLI reporting and are not controlled cost/latency benchmarks. Do **not** claim performance improvement from these data.

Repeat across the seven-case rubric, multiple runs, independent judges and tool-enabled environments before reporting gains.
