---
name: skill-authoring-toolkit
description: Create and maintain reusable Agent Skills in SKILL.md format, with precise triggers, testable workflows, safe tool permissions and validation.
---

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
