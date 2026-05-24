# E2E Test Generation

Use this reference for browser-driven workflows and user journeys.

## Framework Selection

**Use the browser test framework the repository already trusts.**

Prefer the framework already present in the repository. Detect it from config files and dependencies:

| Signal | Framework |
| --- | --- |
| `playwright.config.*`, `@playwright/test` | Playwright |
| `cypress.config.*`, `cypress/` | Cypress |
| Selenium/WebDriver imports or Grid config | Selenium |

If there is no existing framework and the user did not choose one, prefer Playwright for new web E2E code because it has first-class fixtures, tracing, retries, and multi-browser support.

## Implementation Pattern

**Make browser tests stable, isolated, and readable.**

- **Location:** Put tests in the existing E2E directory, commonly `tests/e2e/`, `e2e/`, `cypress/e2e/`, or the repo's configured test directory.
- **Page objects:** Use them only when a flow has repeated behavior or multiple tests share the same screen actions. Avoid page objects for one-off checks.
- **Selectors:** Use stable selectors in this order: accessible role/name, label text, explicit test id, semantic text. Avoid brittle CSS paths.
- **Waiting:** Replace arbitrary waits with assertions on visible UI state, URL changes, network responses, or domain-specific readiness signals.
- **Test data:** Isolate data per run. Create data through public APIs, fixtures, factories, or seeded test helpers already present in the repo.
- **Authentication:** Capture auth through existing storage-state/session helpers when available; otherwise log in through the UI only for one setup path, not every test.

## Coverage Shape

**Keep suites compact and focused on user-visible risk.**

Generate a compact suite with:

- **Smoke:** One test for the critical happy path.
- **Failure:** One validation or permission failure path.
- **Persistence:** One persistence or reload check when the flow changes state.
- **Accessibility:** Optional smoke check only if the project already uses an accessibility test helper.

## Playwright Defaults

**Prefer role-based actions and assertions close to the behavior.**

```ts
import { expect, test } from '@playwright/test';

test('user completes the critical flow', async ({ page }) => {
  await page.goto('/target');
  await page.getByRole('button', { name: /continue/i }).click();
  await expect(page.getByRole('heading', { name: /success/i })).toBeVisible();
});
```

Use `test.step` for long workflows, `test.describe` for a single feature area, and fixtures for shared setup. Keep assertions close to actions.

## Cypress Defaults

**Use deterministic Cypress flows and Testing Library commands when available.**

```ts
describe('critical flow', () => {
  it('lets a user complete the flow', () => {
    cy.visit('/target');
    cy.findByRole('button', { name: /continue/i }).click();
    cy.findByRole('heading', { name: /success/i }).should('be.visible');
  });
});
```

Prefer Testing Library commands when installed. Use `cy.intercept` for deterministic network behavior only when the test is intentionally stubbing dependencies.

## Selenium Defaults

**Keep Selenium lifecycle and selector patterns consistent with the project.**

Use explicit waits, page objects for repeated screens, and driver lifecycle hooks that match the existing framework. Keep selectors centralized when the suite already follows that pattern.
