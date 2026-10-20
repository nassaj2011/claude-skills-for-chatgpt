# Provider-neutral LLM boundary — offline fixtures

A deterministic fake response adapter, typed schema validation, bounded transient retry/cost, and authorization guard before a mock read-only tool. It makes **zero external API calls** and neither stores nor requests credentials.

Run: python -m unittest discover -s examples/llm-contract -p "test_*.py" -v

This validates an application's response-validation concepts, NOT real model accuracy, current provider documentation, real token usage, actual costs or production tool permission. In ChatGPT Web, use the skill contract and user-run fixtures without claiming an API invocation occurred.
