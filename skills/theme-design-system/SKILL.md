---
name: theme-design-system
description: Define and evolve a cohesive web or mobile design system with accessible tokens, typography, color, component variants and usage rules.
---

# Theme and design-system factory

1. Read brand identity, screenshots and the existing token/component stack. Preserve established brand rules unless redesign was requested.
2. Describe 2 viable visual directions with rationale rooted in audience and domain; choose one after considering accessibility and technical cost.
3. Specify semantic color tokens (surface, text, border, focus, danger, success), light/dark variants, typography scales, spacing, radius and motion preferences.
4. Map tokens to actual component primitives (buttons, inputs, nav, dialogs, tables, alerts) and their hover/focus/disabled/error/loading states.
5. Ensure minimum readable contrast, visible keyboard focus, reduced-motion support, RTL/localization and responsive breakpoints where relevant.
6. Provide a migration map for existing styles; avoid generating a parallel design system that conflicts with shipped components.
7. Validate representative screens at mobile, tablet and desktop widths and collect visual regression evidence.

Output: theme rationale, token table or CSS variables, component state matrix, sample usage and integration notes.
Do not claim WCAG compliance without measured checks.

## Token reference

Inspect `examples/frontend-rtl/tokens.css` for semantic light/dark tokens, logical layout properties, focus outlines and reduced-motion preference. This is a testable starting point rather than a general-purpose component library. Measure actual contrast and RTL behavior in a browser before certification.
