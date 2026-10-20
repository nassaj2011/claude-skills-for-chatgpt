# Persian/RTL accessible booking prototype

**Scope:** A completely local, educational HTML/CSS/ES module UI for validating theme tokens, RTL layout, keyboard focus, semantic form controls, status announcements, state ownership, loading/error/retry and the visible separation between a demo and a production booking system.

It **does not** authenticate anyone, reserve a real slot, persist information or handle money. It makes **zero outbound network calls** and has no third-party dependencies.

## How to run

Open `index.html` locally in a browser that supports ES modules, or serve this folder with an existing authorized static development server. If local file security blocks module imports, use a loopback-only static server. No package install is required.

## How to test

```bash
node --test examples/frontend-rtl/ui.test.mjs
node --check examples/frontend-rtl/ui.mjs
```

The node test verifies only the **pure state machine** and safe text rendering, not actual visual layout or WCAG conformance. Inspect the browser UI manually with keyboard navigation and screen reader. Future Playwright integration must be run in an authorized local browser environment.

## Skills applied

`frontend-design-direction`, `theme-design-system`, `react-artifacts-builder` (state-management concepts only; this specimen is deliberately **not** React), `performance-accessibility`, and `qa-test-strategy`.
