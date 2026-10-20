# Fictional privacy inventory, not a compliance certificate

The declared sample contains *field names only*, no names, phone numbers, session tokens or other real personal data. The policy rules are **illustrative project decisions**, not legal requirements. They reject analytics disclosure of direct identifiers, messaging overdisclosure, undefined retention, duplicate fields and incomplete access ownership.

Run: python examples/privacy-inventory/inventory_gate.py --input examples/privacy-inventory/sample.json

Tests: python -m unittest discover -s examples/privacy-inventory -p "test_*.py" -v

Caveats: This tool does not inspect running systems, automatically identify every sensitive field, decide legal bases or check vendor contracts; an invented REVIEWED status is not evidence of legal review. A real assessment requires data flows, retention/deletion tests, contracts and qualified jurisdictional review. In ChatGPT Web without local execution, generate the inventory table and mark checks NOT RUN.