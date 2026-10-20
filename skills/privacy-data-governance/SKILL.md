---
name: privacy-data-governance
description: Trace personal-data flows, minimization, user rights, retention, vendor transfers, deletion propagation and privacy release evidence for software platforms.
---

# Privacy and data governance — executable review contract

## Use when
The task involves personal data, logs/analytics, identity, marketing preferences, uploads, vendors, data exports or customer rights. Do not invoke for a purely static CSS change without user data.

## Evidence-first workflow
1. **Scope and authority.** Identify jurisdictions, controller/processor relationships, products, audiences, data subjects, environments and actual sources available. Label unknowns; do not assert GDPR or other legal compliance from generic guidance. Obtain qualified legal review for legal basis, cross-border transfers, sensitive classes and statutory timelines.
2. **Data map by field, not by feature name.** Record each field and purpose, source, processing system, recipient, access role, transmission/storage region, legal-basis question, retention trigger, deletion path and evidence reference. Include analytics, monitoring, test snapshots, exports, support tickets, message vendors and backups; distinguish operational logs from business records.
3. **Classify each disclosure.** Identify required vs optional fields, security/PII severity and whether user choice is required. Apply data minimization and pseudonymization at both collection and **each recipient boundary**; avoid raw phones, IDs or free-text payloads in analytics/traces.
4. **Map lifecycle.** Describe access/correction/export/deletion/withdrawal requests, system-of-record, processors, downstream copies, caches, archives, backups and restoration risk. Never promise instant erasure from immutable backups; state actual retention/restore quarantine controls and lawful exceptions as decisions.
5. **Tie risks to controls.** Specify owner, severity, exact remediation, source of verification, test case and blocker status. Prioritize unauthorized disclosures or unclear external sharing before cosmetic policy text.
6. **Verify on permitted environments.** Negative tests must cover role- and tenant-scope reads, analytics payload schema, CSV export permissions, deletion propagation, processor contracts, restored-backup deletion replay and incident logging without raw PII. Use synthetic records only.
7. **Decide and hand off.** Mark each gate PASS / FAIL / NOT RUN / NEEDS LEGAL REVIEW. Do not call legal compliance 'verified' solely because a checklist is complete.

## Required deliverable
- **Data-flow inventory:** field | source | purpose | recipient | basis to verify | region | retention trigger | deletion path | evidence.
- **Risk register:** severity | affected data | exploit/exposure pathway | owner | corrective action | acceptance test | status.
- **Lifecycle and user-rights map:** entrypoint, identity verification, response/exceptions, cascade, backup behavior.
- **Concrete acceptance tests** with an expected result; note tests not run and legal questions unresolved.
- **Executive decision** to proceed, block, or defer with explicit accountable sign-off, not a legal conclusion.

## Browser-only / ChatGPT web
If repository, storage, analytics configurations or tools are unavailable, ask for **redacted** schema/data-flow descriptions and produce an example matrix with NOT VERIFIED labels. Provide SQL or tests to run later rather than implying access. Never upload, store, echo or transmit real customer datasets unnecessarily.

## Verified local reference
An illustrative field-inventory validator and redacted sample live in examples/privacy-inventory/ in the public source checkout. They implement project-defined data policy checks, **not legal certification**. Run its tests only if a permitted local Python environment exists; otherwise use the checklist above.

## Safety constraints
No covert telemetry, hidden source-code collection, secret extraction or backdoor. Do not invent legal deadlines, consent grants, data-controller roles, contractual rights or privacy compliance. Never export real personal data into a public skill repository.
