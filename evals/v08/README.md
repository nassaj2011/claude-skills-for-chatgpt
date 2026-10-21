# Held-out, three-arm skill evaluation — v0.8 draft

87 new *fictional* prompts across all 29 skills (3 each). "Held-out" means new relative to the previous repository evaluation prompts, **not** guaranteed unseen during a foundation model's training.

The three arms are baseline, character-length-matched generic writing guidance, and the specialist SKILL.md. This is **not** a token-balanced control or a blinded within-model experiment.

First pilot: 3 actual code-generation tasks x 3 arms = 9 independent Codex text-only calls (H04-1, H14-1, H27-1). Model outputs must be checked by the deterministic guarded Python evaluator. Script does not touch production systems or use actual credentials.

```powershell
python scripts/heldout_v08.py --case H04-1 --arm baseline --digest-only
python scripts/run_v08_batch.py --max-new 9
python scripts/score_code_v08.py --case H04-1 --response evals/v08/runs/H04-1-baseline.txt
```

Safety: run only in a disposable development environment. The AST screen and temporary subprocess are **not a hardened security sandbox**. Do not run arbitrary unreviewed model code against a machine holding sensitive data. Failing or incomplete executions must be recorded and not inferred as success. The other 84 prompts are prepared, NOT EXECUTED, until experiments are deliberately scheduled.

Evaluation constraints: a 3-case pilot does not show general skill efficacy or prove 8.5/10. Do not merge or release solely based on prompt bank creation. Preserve raw responses, version, timestamps, SHA-256 and all failure outcomes.
