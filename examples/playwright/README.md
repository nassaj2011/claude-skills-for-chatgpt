# Optional browser smoke example

Use only with an authorized **local/staging** web app and Playwright test runner already installed in that project's dependencies.

Place `smoke.spec.ts` in the target project's Playwright tests folder, or configure Playwright to include this path, then run:

```bash
# With an already-running authorized local app:
BASE_URL=http://127.0.0.1:3000 npx playwright test smoke.spec.ts
```

On PowerShell: `$env:BASE_URL="http://127.0.0.1:3000"; npx playwright test smoke.spec.ts`.

This is a **generic executable smoke template, not a complete end-to-end application test**. No Playwright dependency is installed automatically. Add domain-specific fixtures, critical journeys, selectors, negative cases, auth and payment isolation before relying on the suite as a release gate. Capture actual browser results; do not label template code PASS.
