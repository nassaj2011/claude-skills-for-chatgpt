# مهارت‌های کلاد برای چت‌جی‌پی‌تی
## Claude Skills for ChatGPT — Idea → Production

[فارسی](README.fa.md) · [Workflow](docs/WORKFLOW.md) · [Anthropic comparison](docs/ANTHROPIC_COMPARISON.md) · [Contribute](CONTRIBUTING.md)

> **Independent community project.** Inspired by the *Agent Skills* approach and the public [Anthropic Skills](https://github.com/anthropics/skills) examples, but **not affiliated with, endorsed by, or maintained by Anthropic or OpenAI**. The skill instructions in this repository are newly authored, not verbatim copies or an official Claude-to-ChatGPT conversion.

**22 original, portable Agent Skills** covering the entire software-platform lifecycle: discovery, architecture, UI/UX, application development, API integrations, security, debugging, tests, CI/CD, observability, release and handover.

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
| 07 · Extend the kit | [skill-authoring-toolkit](skills/skill-authoring-toolkit/SKILL.md) |

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

The installer **does not overwrite** existing skills, never deletes files, and runs in preview mode unless `--apply` is passed. It uses only Python's standard library. You can install selected skills with `--only frontend-design-direction qa-release-gatekeeper`.

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
python -m unittest discover -s tests -v
```

Each `skills/<name>/SKILL.md` needs a frontmatter `name` and useful `description`, workflow steps, real safety boundaries and evidence-based outputs. See [CONTRIBUTING.md](CONTRIBUTING.md). Every new skill should say **when to use it** and **when not to**.

### Licensing and attribution

Original material in **this** repository is available under the [MIT License](LICENSE). No Anthropic skill source files are redistributed. Existing upstream skill names and concepts are referenced descriptively with links in [docs/ANTHROPIC_COMPARISON.md](docs/ANTHROPIC_COMPARISON.md). Third-party skills may have **different per-skill licenses**; check before copying or modifying any upstream content. “Claude”, “ChatGPT” and “Codex” are trademarks of their respective owners.

**Status: v0.1 community foundation.** Skill-format checks are automated; end-to-end agent evaluations, integration deployments and production certification are *not* claimed.
