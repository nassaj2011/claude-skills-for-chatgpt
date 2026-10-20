---
name: agent-skill-security-auditor
description: Inspect Agent Skills for dangerous instructions, unexpected scripts, credential exfiltration, symlinks, scope escalation and third-party provenance before installation.
---

# Security audit for untrusted Agent Skills

A skill folder is executable guidance, not a sandbox: all third-party skills require source review before installing or running scripts.

1. Establish upstream repository, exact commit, license, maintainer and why the capability is needed; avoid installing unknown collections wholesale.
2. Inventory SKILL.md, scripts, embedded assets, nested references, symlinks and executable binaries. Note external URLs, shell commands, pip/npm install hooks and network calls.
3. Run `python scripts/audit_skills.py --root path/to/skills --json` to find **heuristic indicators** (unsafe shell pipelines, destructive actions, credential paths, instruction override, unexpected binaries/symlinks). Treat scanner results as leads, not a security guarantee.
4. Manually inspect suspicious code, transitive dependencies and whether apparent "do not run" examples are false positives. Never execute an untrusted audit target.
5. Compare declared scope and actual commands: filesystem reads, network destinations, GitHub permissions, browser automation, production mutation and secrets access.
6. Classify APPROVE / REVIEW / REJECT with documented provenance, findings, residual risk and owner permission. Any high-risk unresolved behavior blocks installation.
7. Prefer explicit user-scope, no-overwrite installation; pin revision and re-audit when upgrading.

Output: inventory, findings with file/line/reason, rights/provenance, tool permissions, mitigation and decision. A clean static scan **does not certify safety** or detect every prompt injection.

## Execution dependency

The static scanner is `scripts/audit_skills.py` in the **public source checkout**. Installing only this SKILL.md does not install the Python utility. Use a locally inspected copy of the repository or conduct manual source review when the helper is absent. Never fetch-and-execute an unknown scanner; absence of a scanner is not an approval to install untrusted skills.
