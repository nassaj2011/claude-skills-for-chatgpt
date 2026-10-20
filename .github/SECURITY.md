# Security policy

Do **not** include access tokens, user repositories, personal data or sensitive exploit details in public GitHub issues.

For security flaws in the skill kit, use the repository's private vulnerability reporting channel if the GitHub maintainer has enabled it:

https://github.com/nassaj2011/claude-skills-for-chatgpt/security/advisories/new

If this channel is unavailable, report only a non-sensitive request for a private contact method, without disclosing exploit details publicly.

## Supported release line

Current: v0.3.x. Earlier v0.1.x/v0.2.x distributions remain public, but users should check the latest reviewed release and manually review changed scripts.

## Scope and limitations

The scanner is heuristic and does not detect all malware, prompt injection or malicious dependencies. A clean CI run is not a security certification. Never test against third-party projects without authorization; do not add covert tracking or source exfiltration. See [provenance and privacy](../docs/PROVENANCE_AND_PRIVACY.md).
