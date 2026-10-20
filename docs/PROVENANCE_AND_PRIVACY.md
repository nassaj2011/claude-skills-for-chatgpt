# Provenance, privacy and responsible distribution

This is an independent community skill kit, not an Anthropic or OpenAI product.

## Publisher and origin

- Project: **Claude Skills for ChatGPT — Idea → Production**
- Canonical source: https://github.com/nassaj2011/claude-skills-for-chatgpt
- Publisher account: **nassaj2011** (repository maintainer, **not** the identity of any user)
- Release: **v0.7.0**
- License: MIT (original contents only; upstream marks belong to their owners)
- Machine-readable per-skill file hashes: [CATALOG.json](../CATALOG.json) (textual CRLF line endings normalized to LF before hashing for Windows/Linux portability)

These details establish where this public distribution claims to come from. **A plain SHA-256 catalog is not an identity signature**: someone who modifies the catalog and skill files together can still produce matching checksums. To establish provenance, compare against a trusted Git commit/tag and, where available, signed release verification. Never treat a filename or unverified metadata as proof.

## Privacy and operational boundaries

- **No hidden telemetry**: SKILL.md files are instructions; this project's `install.py` does not access the network, contact this maintainer, or transmit user code.
- **No user tracking or hidden access**: the project contains no backdoor, automatic source-code upload, persistent agent credential, covert user-ID collection or remote-admin interface.
- **Optional local installation receipt**: a user can pass `--receipt /path/to/new/local-receipt.json`. The file is written locally, contains the public source URL, install time, installed skill names and status, but no user ID and is **never uploaded** by this tool.
- **Read-only security scanning**: `scripts/audit_skills.py` checks selected risk indicators. Unknown executable formats and links are flagged; clean results do not prove harmlessness.
- **PR review tool**: `pr_review_report.py` contacts GitHub through authenticated `gh` **only when explicitly executed by the user/agent**. It is read-only, but GitHub receives API requests as it normally would. The installer makes no such requests.
- **Generated code belongs to its user**, subject to the actual project's agreements and applicable law. Skill authors are not entitled to inspect it.
- **No use surveillance**: cloning a public repository does not give the publisher visibility into the user's private repository, tool calls or generated files. GitHub itself may collect access information under its own privacy terms, separate from these scripts.

## Sharing with friends or organizations

You may share the public GitHub URL. Installing from source is optional and users should inspect scripts before executing them. For managed/enterprise distribution, use an explicit consent/permissions model for any future integrations or compliance reports; user activity collection must be off by default and transparently disclosed before opt-in.

Security concerns about these tools should follow [responsible disclosure guidance](SECURITY.md). Do not publish someone else's credentials, private code or identifying data.

## Security limitations

Nothing in text-only Agent Skills guarantees that downstream generated websites are safe. Tool scopes, user authorization, content restrictions and application security controls must be enforced by actual execution environments. No open-source skill collection can reliably identify all future users or prevent someone from writing unsafe code using a different tool.
