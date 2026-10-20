---
name: project-bootstrap-environments
description: Bootstrap a reproducible software project with local, development, test, staging and production environment isolation, safe secrets, CI and onboarding.
---

# Reproducible project bootstrap

1. Determine whether this is a new repository or an existing product. Inspect README, AGENTS.md, lockfiles, project structure, and running processes; do not scaffold over existing code.
2. Select a stack from approved requirements and delivery constraints. Avoid imposing Docker, monorepos or framework rewrites unnecessarily.
3. Define dev/test/staging/production boundaries, disposable fixtures, a secret-free .env.example and credential provisioning policies.
4. Pin runtime and package versions where practical. Establish reproducible builds, safe migrations, lint/typecheck/test commands and small CI gates.
5. Use least-privilege CI access; protect real secrets and never commit .env files or credentials.
6. Document bootstrap, smoke and teardown commands for supported OSes with disk/resource requirements; do not delete user files as a cleanup shortcut.
7. Test from a fresh isolated checkout if authorized and feasible; disclose missing prerequisites and nondeterministic setup steps.

Output: repository layout, environment contract, onboarding commands, clean setup evidence, CI plan and remaining constraints.
Never claim fresh-machine reproducibility without testing it.
