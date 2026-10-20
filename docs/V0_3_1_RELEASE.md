# v0.3.1 — Cross-platform provenance checksum fix

Fixes a Windows portability defect found during post-release validation of v0.3.0.

- `scripts/provenance.py` now normalizes textual CRLF line endings to LF before SHA-256 hashing of `SKILL.md` files.
- The canonical `CATALOG.json` explicitly declares `hash_normalization: CRLF-to-LF`, and every of the 29 skill hashes was regenerated accordingly.
- The regression suite verifies that identical SKILL.md text with LF or CRLF produces the same hash.
- The release/version and attribution documentation were updated. No telemetry, hidden tracking, source-code upload or remote access were added.

The SHA-256 catalog is an integrity aid, not a publisher identity signature. This hotfix does not independently validate all Agent Skills at runtime.
