# v0.6 — Three specialist skill upgrades: evidence register

## Experiment plan registered before execution
| Area | Baseline prompt | Updated-skill rubric | State |
|---|---|---|---|
| privacy-data-governance | evals/prompts/v05-privacy.txt | evals/benchmarks/v06-privacy-criteria.json | MODEL RUN FAILED |
| load-resilience-testing | evals/prompts/v06-load.txt | evals/benchmarks/v06-load-criteria.json | MODEL RUN FAILED |
| visual-assets-design | evals/prompts/v06-visual.txt | evals/benchmarks/v06-visual-criteria.json | MODEL RUN FAILED |

Attempts: six independent Codex CLI starts with model gpt-5.6-terra (`--ephemeral --ignore-user-config -s read-only`), on fictional non-sensitive prompts. All failed before generation because the ChatGPT Codex service returned HTTP 404 at the model endpoint. No complete output was generated; no comparisons or numerical rubric grades exist.

**Data integrity rule:** Do not treat these attempts as 0%-score runs; they are missing/blocked observations. Historical v0.4 comparisons of other skills are unaffected. Re-execute once model service access works and preserve complete raw artifacts and independent session IDs.

## Successful domain implementation evidence
| Area | Executed test | Verified outcome | Limit |
|---|---|---|---|
| Privacy | Seven tests, including prohibited analytics, vendor over-disclosure and retention uncertainty | PASS | Defined inventory controls only, not deployed traffic/legal compliance |
| Load | Seven tests; actual local HTTP requests with bounded counters | PASS | Synthetic loopback handler, not public or staging capacity |
| Visual | Nine XML/contrast/rights lint tests + browser geometry smoke | PASS | No human print/typeface/aesthetics certification |
| ChatGPT Web | Deterministic regeneration and parity of all 29 skill cards | PASS when CI is green | No guarantee of native tool routing or host capabilities |

## Quality interpretation
The reviewed skills now contain clearer triggers, non-triggers, decision criteria, negative tests, materialized examples, and web-only fallbacks. This is **structural/operational improvement**, not verified causal model performance. A new 0–10 scoring round should be performed after blinded, repeated A/B tests and human review of resulting code/artifacts.
