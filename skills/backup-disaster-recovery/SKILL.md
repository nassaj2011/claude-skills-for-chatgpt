---
name: backup-disaster-recovery
description: Plan and verify backup integrity, isolated restore drills, RPO/RTO objectives, application consistency, provenance and incident recovery with explicit authorization.
---

# Backup and disaster recovery — restore evidence over backup status

## Trigger and safe boundary
Use for backups, migrations, data-loss resilience, disaster recovery, ransomware recovery and continuity plans. Nothing here authorizes restoring onto production or deleting retained backups. In ChatGPT Web with no filesystem tools, produce a runbook and label all verification NOT RUN.

## Specialist recovery protocol
1. Inventory critical data and *dependencies*: relational databases, files/object storage, key material (names only), WAL/PITR, worker queues, idempotency/payment state, DNS, runtime environment and third-party data. Identify system owners and blast radius.
2. Agree RPO (acceptable data loss), RTO (acceptable downtime), testing cadence, retention/jurisdiction and incident priorities with accountable stakeholders. Missing targets are OPEN DECISIONS, not inferred numbers.
3. Map backup type to consistency requirements: database-consistent dumps/snapshots, transaction logs, offsite/immutable copies, encrypted storage, key recovery, rotation and independent credentials. A list of backed-up files is not a database-consistent snapshot.
4. Check file-level checksum/catalogue manifests for tamper evidence, but separate **integrity** from **restorability**. Review metadata, last success timestamp, storage reachability, encryption key access and coverage of tenant/application tables.
5. Specify authorized **isolated restore** into a disposable environment, validate actor/tenant isolation, referential/financial integrity, queued job replay, payment side effects (disabled), health smoke and partial-failure recovery. Measure achieved restore time and point-in-time actual loss from controlled test markers.
6. Perform negative fault drills only inside a disposable test: missing object, corrupted archive, stale key, incomplete WAL and restored backup with pending deletion requests. Record fail-closed decisions and protected originals.
7. Release readiness requires actual restore evidence, responsible approval, measured RPO/RTO and known caveats. A backup dashboard showing green does not establish recovery.

## Deliverables
Protection matrix | backup schedule/retention/key owner | restore checklist | measured vs target RTO/RPO | consistency and access tests | failures and remediation owner | declared readiness GO/NO-GO/NOT TESTED.

## Executable reference
The repository provides `scripts/backup_manifest.py` for authorized backup-folder SHA-256 verification. A new `examples/restore-drill/` synthetic source-to-isolated-destination drill tests exact content recovery, corruption detection and no-overwrite, but **does not verify database consistency or production RTO**. All tests create temporary data.

## Hard limits
Never run an unapproved restore, expose backups with real personal data, claim encryption keys are recoverable without proof or automatically clean up user-owned originals.
