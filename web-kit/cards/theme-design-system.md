# ChatGPT Web: theme-design-system

Original: https://github.com/nassaj2011/claude-skills-for-chatgpt

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

## Specialist workflow

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

## Your task

[Replace with your actual request and non-sensitive code/context.]

## Response

Provide actionable deliverables, evidence/assumptions, checks NOT EXECUTED and risks.
