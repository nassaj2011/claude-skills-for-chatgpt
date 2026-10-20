---
name: performance-accessibility
description: Assess and improve web performance and accessibility with measurable budgets, controlled profiling, and user-centered prioritization.
---

# Performance and accessibility
1. Establish audience, critical devices/network conditions, accessible interaction needs and baseline user journeys.
2. Measure first: profiling, bundle size, request waterfall, query timing, core web vitals where feasible; state tool and environment.
3. Find the real bottleneck before refactoring: expensive renders, waterfalls, slow queries, oversized assets or long tasks.
4. Define realistic performance budgets and verify key interactions with mobile throttling where possible.
5. Audit semantic markup, contrast, keyboard order, screen-reader labels, focus, dynamic announcements, touch targets and reduced motion.
6. Propose minimal incremental fixes that preserve behavior; run regression and a11y checks again.
7. State which items require human assistive-tech review and what was not tested.

Output: measured baseline, prioritized findings, affected routes/components, remediation, measured change and outstanding accessibility risks.
Do not claim WCAG conformity from automated scanning alone.

## Local accessibility/performance boundary

The `examples/frontend-rtl` specimen provides focus-visible, reduced-motion and semantic-label patterns, while `examples/observability-gate` provides an offline latency gate. Neither replaces axe/Lighthouse/browser measurements, WCAG audits or real field performance data. State the measured-versus-proposed boundary in all outcomes.
