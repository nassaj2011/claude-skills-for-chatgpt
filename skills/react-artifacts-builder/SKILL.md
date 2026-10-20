---
name: react-artifacts-builder
description: Build multi-component interactive web interfaces using a compatible React stack, routing, state and UI primitives where appropriate.
---

# Multi-component web app builder

1. Confirm requested deliverable: mockup, reusable component, interactive local demo, or production feature. Never imply a demo is a deployed system.
2. Inspect package versions, React framework (Next.js/Vite/etc.), existing routes, UI components and build/test commands.
3. Choose a minimal component hierarchy, state ownership, data loading and routing model. Use actual project libraries; do not assume Tailwind or shadcn is installed.
4. Separate view state, server state and derived state; validate form inputs and handle loading, empty, error, retry and offline states.
5. Include accessible semantics and keyboard/focus behavior for overlays, menus and forms.
6. Keep API contracts typed where feasible; never embed tokens/secrets in client bundles.
7. Run formatting, typecheck, tests and build where available; if unable to execute, identify that explicitly.
8. For complex interaction, verify through playwright-webapp-testing and capture reproducible evidence.

Output: files changed, architecture sketch, interaction states, test commands/results and remaining caveats.
Prefer working features to ornamental complexity.
