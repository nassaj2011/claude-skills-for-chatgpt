---
name: frontend-design-direction
description: Create deliberate, distinctive, accessible frontend visual direction and interface composition grounded in the product's users and brand.
---

# Frontend design direction

1. Establish audience, primary task, brand, information hierarchy, target devices and emotional tone. Explore references only when authorized/available.
2. Choose a clear visual concept justified by product context, rather than adding gradients or illustrations by default.
3. Plan hierarchy: navigation, primary action, content density, typography, spacing, rhythm, imagery and meaningful empty states.
4. Sketch interactions and account for loading, error, partial data, zero results, disabled actions, destructive confirmation and permission denial.
5. Design mobile-first; consider touch targets, keyboard navigation, readable contrast, screen readers, RTL and localization.
6. Implement against the project's current design system/components; avoid unrelated framework changes or broad refactors.
7. Use screenshots and browser testing when a UI execution environment exists; correct broken layouts before calling it done.

Output: visual rationale, key screen/state inventory, responsive rules, implementation details, visual verification and limitations.
Do not substitute a static mockup for functioning behavior when the user requested an application.

## Local RTL example

Review `examples/frontend-rtl/index.html` and `tokens.css` for a Persian RTL accessible-form prototype. The `node --test examples/frontend-rtl/ui.test.mjs` check covers state logic only. Perform real browser layout, keyboard and screen-reader checks before asserting visual/accessibility quality.
