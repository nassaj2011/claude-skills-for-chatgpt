# مهارت‌های کلاد برای چت‌جی‌پی‌تی
## Claude Skills for ChatGPT — Idea → Production

[فارسی](README.fa.md) · [Workflow](docs/WORKFLOW.md) · [v0.3 improvements](docs/V0_3_RELEASE.md) · [Privacy & provenance](docs/PROVENANCE_AND_PRIVACY.md) · [Evaluation rubric](evals/README.md) · [Anthropic comparison](docs/ANTHROPIC_COMPARISON.md) · [Contribute](CONTRIBUTING.md)

> **Independent community project.** Inspired by the *Agent Skills* approach and the public [Anthropic Skills](https://github.com/anthropics/skills) examples, but **not affiliated with, endorsed by, or maintained by Anthropic or OpenAI**. The skill instructions in this repository are newly authored, not verbatim copies or an official Claude-to-ChatGPT conversion.

**29 original, portable Agent Skills** covering the entire software-platform lifecycle: discovery, architecture, UI/UX, application development, API integrations, security, debugging, tests, CI/CD, observability, release and handover.

This is **a workflow kit, not a new AI model, a SaaS platform or a deployment engine**. An installed skill guides an agent; tools, permissions, coding environment and testing still determine what it can actually execute.

### What makes this different?
Instead of collecting hundreds of unrelated prompts, this project combines a curated lifecycle, explicit handoffs, evidence-based release gates, reproducible skill validation, and honest capability boundaries. It works best with **OpenAI Codex** and other Agent Skills-compatible execution environments. ChatGPT web support varies by product surface and plan.

### Skill catalog

| Lifecycle | Skills |
| --- | --- |
| 01 · Discover and plan | [product-business-analyst](skills/product-business-analyst/SKILL.md), [technical-project-orchestrator](skills/technical-project-orchestrator/SKILL.md) |
| 02 · Architect and govern | [software-architect](skills/software-architect/SKILL.md), [database-transaction-integrity](skills/database-transaction-integrity/SKILL.md), [security-authorization-auditor](skills/security-authorization-auditor/SKILL.md), [privacy-data-governance](skills/privacy-data-governance/SKILL.md) |
| 03 · Design | [frontend-design-direction](skills/frontend-design-direction/SKILL.md), [theme-design-system](skills/theme-design-system/SKILL.md), [visual-assets-design](skills/visual-assets-design/SKILL.md), [performance-accessibility](skills/performance-accessibility/SKILL.md) |
| 04 · Build | [react-artifacts-builder](skills/react-artifacts-builder/SKILL.md), [backend-api-engineer](skills/backend-api-engineer/SKILL.md), [mcp-integration-builder](skills/mcp-integration-builder/SKILL.md), [llm-api-integration](skills/llm-api-integration/SKILL.md) |
| 05 · Debug and test | [backend-debugging](skills/backend-debugging/SKILL.md), [playwright-webapp-testing](skills/playwright-webapp-testing/SKILL.md), [qa-test-strategy](skills/qa-test-strategy/SKILL.md) |
| 06 · Ship and operate | [devops-ci-cd](skills/devops-ci-cd/SKILL.md), [qa-release-gatekeeper](skills/qa-release-gatekeeper/SKILL.md), [observability-monitoring](skills/observability-monitoring/SKILL.md), [documentation-handover](skills/documentation-handover/SKILL.md) |
| 07 · Extend and evaluate | [skill-authoring-toolkit](skills/skill-authoring-toolkit/SKILL.md), [skill-evaluation-benchmark](skills/skill-evaluation-benchmark/SKILL.md) |
| 08 · Review and secure delivery | [code-review-pr](skills/code-review-pr/SKILL.md), [agent-skill-security-auditor](skills/agent-skill-security-auditor/SKILL.md), [dependency-supply-chain-auditor](skills/dependency-supply-chain-auditor/SKILL.md) |
| 09 · Recover, scale and bootstrap | [backup-disaster-recovery](skills/backup-disaster-recovery/SKILL.md), [load-resilience-testing](skills/load-resilience-testing/SKILL.md), [project-bootstrap-environments](skills/project-bootstrap-environments/SKILL.md) |

### Install for Codex

1. Clone the public repository:

   ```bash
   git clone https://github.com/nassaj2011/claude-skills-for-chatgpt.git
   cd claude-skills-for-chatgpt
   ```

2. Preview what the installer would copy:

   ```bash
   python scripts/install.py --target ~/.agents/skills
   ```

3. Apply for your **user** or **project** scope:

   ```bash
   python scripts/install.py --target ~/.agents/skills --apply
   # Or: python scripts/install.py --target /path/to/project/.agents/skills --apply
   ```

On Windows PowerShell, you may specify a Windows path or an existing custom Codex home:

```powershell
python .\scripts\install.py --target "$env:USERPROFILE\.agents\skills" --apply
# With CODEX_HOME configured:
python .\scripts\install.py --target "$env:CODEX_HOME\skills" --apply
```

The installer **does not overwrite** existing skills, never deletes files, performs read-only heuristic skill auditing before installation, and runs in preview mode unless `--apply` is passed. A clean static scan is not proof of safety. It uses only Python's standard library. You can install selected skills with `--only frontend-design-direction qa-release-gatekeeper`.

Restart or refresh your coding agent to discover new skills. A skill may be selected automatically based on its description or explicitly by name, depending on the host.

### ChatGPT and OpenAI API

- **ChatGPT web/app:** cloning a GitHub repository **does not automatically install skills in your ChatGPT account**. Where supported, use your workspace's skill-upload mechanism; otherwise add the relevant SKILL.md content as project instructions/knowledge or use it with a connected execution environment. Capabilities vary.
- **Codex / Agent Skills hosts:** install the SKILL.md folders into your configured skills directory.
- **OpenAI API:** skills can be packaged as folders/ZIPs and attached in supported tool/runtime configurations. See the [official API documentation](https://developers.openai.com/api/docs/guides/tools-skills).
- **Claude Code:** these original instructions also follow the open Agent Skills folder convention; compatibility depends on the host and available tools.

### Example: build a sports booking platform

Use [the fictional end-to-end worked example](examples/from-idea-to-production.md): product hypothesis → PRD → booking invariants → architecture → UI → backend → race-condition tests → release gate → live metrics. No proprietary project materials are included.

### Validate and contribute

```bash
python scripts/validate_skills.py
python scripts/audit_skills.py --root skills --fail-on review
python scripts/provenance.py
python -m unittest discover -s tests -v
```

Each `skills/<name>/SKILL.md` needs a frontmatter `name` and useful `description`, workflow steps, real safety boundaries and evidence-based outputs. See [CONTRIBUTING.md](CONTRIBUTING.md). Every new skill should say **when to use it** and **when not to**.

### Licensing and attribution

Original material in **this** repository is available under the [MIT License](LICENSE). No Anthropic skill source files are redistributed. Existing upstream skill names and concepts are referenced descriptively with links in [docs/ANTHROPIC_COMPARISON.md](docs/ANTHROPIC_COMPARISON.md). Third-party skills may have **different per-skill licenses**; check before copying or modifying any upstream content. “Claude”, “ChatGPT” and “Codex” are trademarks of their respective owners.

**Status: v0.3.1 community hardening release.** Manifest checks, heuristic pre-install security scanning, fixture-based evaluator tests and CI are automated. End-to-end benchmark gains, production deployments and security certification are *not* claimed.

### v0.2: safety tooling and measured pilot

The seven new risk-oriented skills ship with an install-time heuristic safety scan, real read-only PR evidence CLI, file-backup checksum verifier, and a transparent A/B scoring framework. See [release notes](docs/V0_2_RELEASE.md), [benchmark protocol](evals/README.md), and the [first genuine-model pilot](evals/PILOT_RESULT.md). The single review-case pilot showed **no measured improvement** (baseline 100%, skill-instructed 100%). This is not an end-to-end assessment of all 29 skills.

### v0.3: provenance, privacy and fail-closed installation

Read the [security and privacy policy](docs/PROVENANCE_AND_PRIVACY.md) and [release notes](docs/V0_3_RELEASE.md). A new [CATALOG.json](CATALOG.json) contains SHA-256 hashes for all 29 public SKILL.md files and identifies the official source. **These hashes detect divergence but do not authenticate the publisher without a trusted Git revision or signature.**

```bash
python scripts/provenance.py
python scripts/audit_skills.py --root skills --fail-on review
# Review any flagged source files manually before installation:
python scripts/install.py --target ~/.agents/skills --only code-review-pr
python scripts/install.py --target ~/.agents/skills --only code-review-pr --apply
# Only after MANUALLY verifying any REVIEW findings:
# python scripts/install.py --target ~/.agents/skills --only SKILL --apply --accept-review
```

Optional on-device receipt: `--receipt /path/to/new/receipt.json` (never uploaded, no user ID). Existing installations are **not overwritten** and are **not silently upgraded**. Tools such as `pr_review_report.py` stay in this source checkout; a standalone installed SKILL.md does not bundle them. No hidden tracking, covert access to user code or automatic source uploads are implemented.
