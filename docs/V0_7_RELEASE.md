# v0.7.0 — Six additional quality-focused specialist upgrades

This release improves the **quality of six existing specialist skills**. The skill inventory remains 29, available both as native SKILL.md folders for compatible agents and as 29 complete copyable prompts in the independent ChatGPT Web Kit.

## Specialist content improved

1. **LLM API Integration** — typed JSON validation, prompt/tool trust boundary, explicit actor authorization, bounded provider retries/budget, offline failure matrix, privacy and evidence controls.
2. **MCP Integration Builder** — strict input contracts, scoped actor/tenant permissions, read/write separation, human approval, idempotency and safe mock-tool error handling.
3. **DevOps CI/CD** — least-privilege CI permissions, immutable artifact verification, migration compatibility, fail-closed release gates, rollback and human approval.
4. **Dependency Supply Chain Auditor** — source/provenance inventory, version pinning, install-time scripts, licenses, CVE reachability distinctions and minimal authorized remediation.
5. **Backup Disaster Recovery** — backup integrity versus real restorability, isolated restore, application consistency, RPO/RTO questions, corrupted/missing backup tests and no-overwrite policy.
6. **Performance Accessibility** — real-versus-proposed Core Web Vitals, RTL and 320 px reflow, focus management, accessible naming and actual browser evidence with manual WCAG limitations.

## Executable references and unit test counts

| New example | Local passing tests | Reality boundary |
| --- | ---: | --- |
| examples/llm-contract | 9 | Fake provider, no live model/API |
| examples/mcp-contract | 8 | Offline tool dispatcher, NOT a protocol-compliant MCP server |
| examples/release-policy | 7 | Fictional release evidence, no CI secrets or deploy |
| examples/supply-chain | 7 | Declared toy metadata, no lockfile parsing or live CVEs |
| examples/restore-drill | 6 | Disposable synthetic file restore, not database PITR/RTO evidence |
| examples/perf-budget | 6 | Static budgets + optional actual Edge browser run, not RUM/WCAG |
| **New executable suite total** | **43** | All fake/no real infrastructure changes |

The optional `examples/perf-budget/browser_budget.py` successfully ran against the local fictional Persian RTL page in Microsoft Edge with **27 DOM nodes, no observed horizontal overflow at 320/390 px, no JS error and no external requests**. These observations are local sample metrics, not production speed evidence.

## Real Codex model A/B evidence: archived but UNSCORED

Six fictional, non-sensitive specialist scenarios were designed in `evals/v07-quality-benchmarks.json` before the runs. Each was run twice with the same `gpt-5.6-terra` model and Codex CLI 0.147.0, once as baseline and once with the relevant full SKILL.md instructions prepended. All **12 independent sessions completed** and raw final answers are archived under `evals/runs/v07-*.txt`. SHA-256 and session IDs are in `evals/v07-run-manifest.json`. Verify with:

```bash
python scripts/verify_v07_runs.py
```

The archived outputs have **not been independently or blindly scored**. No numerical quality improvement, new average rating of 8.5/10, or causal effect is claimed. The runs were *in-context skill instruction* tests; Codex Code Mode host was unavailable and native auto-trigger, code editing, and automated web-app deployment were **not** evaluated.

## Web and repository compatibility

The canonical `skills/*/SKILL.md` revisions are deterministically exported via `scripts/build_web_kit.py --write` to `web-kit/CHATGPT_WEB_LIBRARY.txt`, Markdown and all 29 `web-kit/cards`. The offline selector is tested with existing browser smoke checks. Web instructions mark absent execution tools as **NOT RUN** and never assume access to private repositories.

## Explicit non-goals

No external load, private user code, real provider keys, payment transactions, production restoration or unapproved CI/deploy actions. Mock tests alone are not readiness certification. Further statistically meaningful evaluation requires replicated blinded A/B runs, actual representative code changes and scored acceptance evidence.

Full CI runs Python unit suites, source/security/catalogue validators, all six new examples, and the 12 saved-response hash checks. Browser smoke runs locally when a supported browser/Playwright is present; it is not a CI browser certification.
