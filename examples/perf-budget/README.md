# Local UI budget and accessibility-adjacent browser evidence

The test uses a **local fictional Persian RTL page**, no internet and zero third-party services. Static budget tests run with Python stdlib. An optional actual Microsoft Edge/Chromium smoke checks measured DOM node count, resource entries, horizontal overflow at 320/390 px and JavaScript failures.

Unit: python -m unittest discover -s examples/perf-budget -p "test_*.py" -v

Browser (installed Playwright + browser needed): python examples/perf-budget/browser_budget.py

**Not a real Web Vitals or WCAG certificate.** DOM/resource budgets do not approximate actual field LCP/CLS/INP by themselves. Real projects need repeatable browser throttling, trace data, axe/Lighthouse (where allowed) and manual assistive technology checks. In ChatGPT Web without browser execution, the proper status is NOT RUN.
