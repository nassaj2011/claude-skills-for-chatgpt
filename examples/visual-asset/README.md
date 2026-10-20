# SVG visual-asset reference — editable vector source

This fictional Persian-language social card is a **real SVG source**, not an AI-generated preview or a layered Photoshop/Figma file. Source: booking-social.svg (1200 × 630 px) with title/description, self-contained geometry, and no external scripts, fonts, linked images or telemetry.

Run: python examples/visual-asset/asset_gate.py

Tests: python -m unittest discover -s examples/visual-asset -p "test_*.py" -v

The tests validate XML structure, accessibility markup, geometry, some risky references, rights declaration and approximate contrast. They **do not validate** Persian shaping in every browser, true source licensing, composition quality, final image rasterization, physical bleed, CMYK correctness or printer proofs. Rights metadata are self-declared and do not confer ownership of external assets. Visual inspection and licensed print preparation remain a manual gate.

The source is compatible with the ChatGPT Web workflow: users can request a design brief, SVG modifications, review criteria and a handoff without a terminal; only genuinely executed tooling can certify files or rendering.

Optional real-browser check: python examples/visual-asset/browser_smoke.py --screenshot path/to/new/local.png

A local Microsoft Edge run confirmed the SVG has 1200x630 rendered geometry, three text nodes and no external requests or JavaScript errors. This is **not** a human visual or print approval.
