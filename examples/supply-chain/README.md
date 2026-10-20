# Synthetic dependency inventory — not live CVE scanning

This offline example checks a **declared** package list for pinned version strings, approved source class, syntactically valid SHA-256 metadata, license presence and install-time script declarations.

Run: python -m unittest discover -s examples/supply-chain -p "test_*.py" -v

No package installation, public registry calls, lockfile mutation, dependency vulnerability database or license assurance is performed. An attacker who controls the declaration may fabricate values. Real attestations and scan evidence require an authorized source checkout and trusted scanners with pinned advisory database dates.
