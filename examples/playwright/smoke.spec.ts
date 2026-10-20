// Optional Playwright smoke suite for an authorized local/staging app.
// Requires @playwright/test to be installed in the target test project.
// Do not run against external sites or production without explicit permission.
import { test, expect } from '@playwright/test';

const baseURL = process.env.BASE_URL ?? 'http://127.0.0.1:3000';

test('entry page responds and has an accessible document title', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', error => errors.push(error.message));
  const response = await page.goto(baseURL, { waitUntil: 'domcontentloaded' });
  expect(response, 'No response from target app').not.toBeNull();
  expect(response!.status()).toBeLessThan(500);
  await expect(page.locator('body')).toBeVisible();
  await expect(page).toHaveTitle(/\S+/);
  expect(errors, 'Browser exceptions').toEqual([]);
});

test('page remains usable at a narrow viewport', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(baseURL, { waitUntil: 'domcontentloaded' });
  await expect(page.locator('body')).toBeVisible();
});
