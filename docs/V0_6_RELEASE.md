# v0.6.0 — Specialist quality uplift (privacy, bounded load, visual assets)

**Scope:** 29 skills remain unchanged in number. Three underdeveloped skills were rewritten into evidence-first execution contracts while preserving portability to both Codex agents and ChatGPT Web users.

## 1. Privacy & data governance
- Detailed field-level map of purpose, processors, access roles, legal-basis questions, retention triggers, deletion and backup replay.
- PASS/FAIL/NOT RUN/NEEDS LEGAL REVIEW gates and explicitly prohibited declarations of legal compliance without evidence.
- New standard-library example: examples/privacy-inventory/. Fictional policy checks flag phone/user data in analytics, messaging overdisclosure, missing lifecycle or owner, and pending counsel review.
- The example is declarative and cannot prove how a running product actually handles personal data. A declared REVIEWED marker is not a real legal opinion.

## 2. Load and resilience
- Explicit ownership and written authorization before traffic. Without it, DESIGN ONLY.
- Workload arrival model, peak/recovery, request and concurrency caps, timeouts, abort triggers, invariant and queue checks, and comparison of configured to achieved load.
- New example examples/bounded-load/ runs a standard-library HTTP server on a locally allocated 127.0.0.1 port. Only this self-created fixture is exercised; no user URLs or accounts are allowed. At most 60 requests and six workers. The example shows observed throughput and p50/p95/p99 but **not** capacity of real apps.

## 3. Visual assets
- Structured creative brief, source vs export distinction, original/third-party rights inventory, print/responsive specifications, Persian typography and final-size QA.
- New examples/visual-asset/ contains an actual authored 1200×630 SVG and a rights manifest. The static quality gate checks geometry, description, safe SVG content, font contrast and declared license; optional local browser verification checks rendering geometry in Edge.
- No representation of copyright clearance, layered Figma files, human aesthetic approval, CMYK print accuracy or universal font shaping is claimed.

## Actual execution evidence

Python standard-library checks were run locally:
- Privacy inventory: 7 passed
- Local bounded HTTP: 7 passed
- SVG/asset metadata: 9 passed
- Real local SVG browser smoke: PASS_BROWSER_GEOMETRY; no external calls

All existing repo tests, manifest/provenance scans and regenerated web-kit files are checked in CI.

## A/B model evaluation state: NOT EXECUTED

Pre-registered prompts/rubrics: evals/prompts/v05-privacy.txt, v06-load.txt, v06-visual.txt, and evals/benchmarks/v06-*-criteria.json.
Six attempts to run independent Codex baseline-versus-updated-skill sessions failed at model transport with HTTP 404 from a Codex responses endpoint. No valid model outputs or A/B scores resulted. The rubric was not retrospectively rewritten to claim success.
See evals/V0_6_RESULTS.md.

**Do not claim the mean expert quality is now 8.5/10, or that tested infrastructure examples certify the skill instructions' overall impact.** Neither native auto-skill routing nor Web Projects integrated use was re-evaluated. Web kit prompts were deterministically rebuilt from the updated canonical SKILL.md files and unit-tested for parity.

## Repeatability and safety

    python scripts/validate_skills.py
    python scripts/audit_skills.py --root skills --fail-on review
    python scripts/provenance.py
    python scripts/build_web_kit.py
    python -m unittest discover -s tests -v
    python -m unittest discover -s examples/privacy-inventory -p "test_*.py" -v
    python -m unittest discover -s examples/bounded-load -p "test_*.py" -v
    python -m unittest discover -s examples/visual-asset -p "test_*.py" -v

No data tracking, hidden code access, destructive testing or outbound load is introduced.
