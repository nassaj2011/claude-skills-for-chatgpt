# ChatGPT Web: skill-authoring-toolkit

Original: https://github.com/nassaj2011/claude-skills-for-chatgpt

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

## Specialist workflow

# Author reliable Agent Skills
1. Identify one specialized recurring task and examples where existing agent instructions underperform. Avoid a general-purpose catchall skill.
2. Write a concise frontmatter name (lowercase kebab-case) and description explaining *when* to use the skill, plus relevant exclusions.
3. Place essential decision rules, required evidence, safety boundaries and expected outputs in SKILL.md. Keep instructions short enough to be selectively loaded.
4. Add references/ only for substantial task-specific details and scripts/ only for deterministic repeatable work. No placeholder dependencies.
5. Separate planning from execution; never use a skill to expand user authorization or bypass platform restrictions.
6. Create example triggers and counterexamples to test routing; include a success/failure rubric and compare against a baseline without the skill.
7. Run the repository validator and tests; update documentation and examples. Review any third-party borrowed content and its specific license.

Output: installable folder, trigger cases, expected outputs, validation evidence and update notes.
A SKILL.md file cannot confer permissions, network access, native ChatGPT installation or tool availability.

## Your task

[Replace with your actual request and non-sensitive code/context.]

## Response

Provide actionable deliverables, evidence/assumptions, checks NOT EXECUTED and risks.
