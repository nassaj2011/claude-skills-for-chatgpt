# ChatGPT Web: project-bootstrap-environments

Original: https://github.com/nassaj2011/claude-skills-for-chatgpt

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

## Specialist workflow

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

## Your task

[Replace with your actual request and non-sensitive code/context.]

## Response

Provide actionable deliverables, evidence/assumptions, checks NOT EXECUTED and risks.
