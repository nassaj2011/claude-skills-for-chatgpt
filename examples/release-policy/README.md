# Offline CI/release evidence gate

The sample is deliberately **NO_GO**: skipped authorization, no staging smoke, migration not preflighted, no restore and no release authorization. This script has no GitHub, deployments, secrets, credentials, external requests or files to mutate.

Run: python -m unittest discover -s examples/release-policy -p "test_*.py" -v

Run fixture: python examples/release-policy/gate.py --file examples/release-policy/sample.json (expected exit 1 and NO_GO)

Even a complete synthetic PASS means only **ELIGIBLE_FOR_HUMAN_DECISION**. It is not actual CI verification, permission to deploy or final GO. Integrate only after verifying live CI evidence, exact SHA, environment ownership, migrations and approval policy.
