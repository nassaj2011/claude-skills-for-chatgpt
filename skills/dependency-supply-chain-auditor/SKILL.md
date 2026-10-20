---
name: dependency-supply-chain-auditor
description: Review package dependencies, vulnerable versions, licenses, lockfiles, build provenance and CI security for web and backend repositories.
---

# Software supply-chain auditing

1. Read ecosystem manifests and lockfiles (npm/pnpm/yarn, pip/uv/poetry, containers, infrastructure) from the current commit; avoid hallucinating dependency versions.
2. Create a dependency inventory by direct/transitive path, runtime vs development scope, update cadence and source provenance.
3. Run available **read-only** vulnerability/license/SBOM tools against approved manifests; capture exact commands, scanner DB timestamp and warnings about false positives.
4. For relevant advisories assess reachability, exposure, exploit preconditions and available patched ranges. Do not rate severity from CVSS alone.
5. Review install scripts, CI actions, third-party binaries, GitHub token permissions, pinned artifacts and provenance/signature verification where warranted.
6. Propose the smallest compatible remediation; model lockfile churn, API breakage, rollback and regression suite. Never auto-upgrade or install dependencies without scope approval.
7. Track accepted risk, ownership and retest date; do not present a scanner pass as an exhaustive security guarantee.

Output: inventory, evidence-backed vulnerabilities and licenses, prioritized upgrade plan, supply-chain controls, CI gate and unassessed components.
