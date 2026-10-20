# Contributing

Thanks for improving an independent, open-source lifecycle skill kit.

## Contributions we welcome

- One well-scoped skill with a clear trigger and counterexample
- Better cross-skill handoffs and evidence gates
- Test fixtures or safe non-production examples
- Persian/English docs and reproducible quality checks

## New skill checklist

1. Place a `SKILL.md` under `skills/<lowercase-kebab-case-name>/`.
2. YAML frontmatter must include `name` (same as folder) and `description` that says *when* to use it; avoid generic "helps with coding".
3. Include concrete workflow, measurable output and boundaries for destructive actions, live systems and data privacy.
4. Prefer concise instruction files; use references/scripts only when materially needed.
5. Run `python scripts/validate_skills.py`, `python scripts/audit_skills.py --root skills`, and `python -m unittest discover -s tests -v`. Interpret scanner findings manually.
6. Update both READMEs/catalog and the workflow/mapping documents when necessary.
7. Explain at least one realistic invocation and one *not applicable* case in the PR description.
8. Confirm ownership and redistribution rights for all submitted material. Do not add copied proprietary Anthropic/OpenAI files or private project data.

## Contribution license

By contributing, you agree to license your original contribution under this repository's MIT license. Disclose third-party source and license before proposing copied content.

## Security

Do not post secrets, production PII, privileged access tokens, exploit paths with sensitive targets, or private client code in issues. See [docs/SECURITY.md](docs/SECURITY.md).

## Release policy

A passed manifest check means structural validity only. It does **not** imply measured improvement, runtime compatibility or production safety. Demonstrate runtime/evaluation evidence separately.
