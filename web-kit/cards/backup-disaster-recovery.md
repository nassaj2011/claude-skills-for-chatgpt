# ChatGPT Web: backup-disaster-recovery

Original: https://github.com/nassaj2011/claude-skills-for-chatgpt

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

## Specialist workflow

# Backup and disaster recovery

Use for backup policies, release/migration protection, ransomware resilience or availability-critical incidents; do not conduct a live restore without authorization.

1. Inventory data stores, object storage, configuration, secrets (tracked without exposing values), infrastructure state and external dependencies; identify a responsible owner.
2. Agree on **RPO** (maximum tolerated data loss) and **RTO** (maximum recovery time), legal retention and critical customer journeys. Do not invent targets.
3. Define backup methods consistent with application/database guarantees: PITR/WAL or equivalent, logical vs physical snapshots, encryption, immutable/offsite copy, retention and rotation.
4. Verify consistency across dependent stores and replay behavior, including pending background jobs and payment/provider state.
5. Inspect non-sensitive manifest/checksum evidence; use `python scripts/backup_manifest.py --root <backup-folder> --write <new-manifest.json>` and `--verify <manifest.json>` on authorized file backup snapshots. This checks file integrity, **not** database restore correctness.
6. Design an isolated, non-production restore drill that measures elapsed recovery, data invariants, application health and audit completeness; never overwrite live data.
7. Record drill failures, missing backups, responsible follow-ups and a rollback/emergency communication runbook.

Output: RPO/RTO, protection map, restore runbook, actual drill evidence versus planned checks, consistency risks and status. Never call a backup proven until an authorized restore test has passed.

## Execution dependency

The optional checksum utility `scripts/backup_manifest.py` is provided in the source repository. A standalone installed SKILL.md has no bundled backup binary and does not create real database backups. Use only authorized local tooling and never claim RPO/RTO or restore readiness from a hash check.

## Your task

[Replace with your actual request and non-sensitive code/context.]

## Response

Provide actionable deliverables, evidence/assumptions, checks NOT EXECUTED and risks.
