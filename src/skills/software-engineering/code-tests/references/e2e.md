# E2E Testing Reference

Guidance for writing end-to-end tests with browser automation frameworks (Playwright, Cypress, WebdriverIO).

---

## Framework Detection

| Signal | Framework |
| --- | --- |
| `@playwright/test` in deps | Playwright |
| `cypress` in deps | Cypress |
| `webdriverio` / `wdio.conf.*` | WebdriverIO |

---

## Test Plan Format

When drafting the test plan in Phase 2, describe user flows step by step:

```text
Flow:         User completes checkout
Start URL:    /cart
Auth:         Logged-in user with items in cart

Steps:
  1. Navigate to /cart
  2. Verify items are listed with correct prices
  3. Click "Proceed to Checkout"
  4. Fill shipping address form
  5. Select payment method
  6. Submit order
  7. Assert: redirected to /order-confirmation
  8. Assert: order confirmation number displayed
  9. Assert: confirmation email triggered (check mock inbox or API)
```

---

## Selector Strategy

Prefer selectors in this order — stop at the first one available:

1. `data-testid` attribute — explicit test hook, immune to style/copy changes
2. ARIA role + accessible name — `getByRole('button', { name: 'Submit' })`
3. Label text — `getByLabel('Email address')`
4. Placeholder or visible text — `getByPlaceholder`, `getByText`
5. CSS class or XPath — last resort; document why no better option exists

Never select by element position (`nth-child`) or layout-dependent attributes.

---

## Page Object Model (POM)

Use POM when a page or component is referenced in more than one spec file. Keep POMs thin:

```typescript
// pages/CheckoutPage.ts
export class CheckoutPage {
  constructor(private page: Page) {}

  async fillShipping(address: Address) { ... }
  async submitOrder() { ... }
  async getConfirmationNumber(): Promise<string> { ... }
}
```

- One class per page or significant component
- POM methods describe user actions, not DOM operations
- No assertions inside POMs — keep them in spec files

---

## Fixtures and Auth

- Authenticate via API or storage state, not UI login flow, to keep tests fast
- Use Playwright `storageState` or Cypress `cy.session` to reuse auth across tests
- Parameterise fixtures for different user roles

```typescript
// Playwright: reuse auth state
test.use({ storageState: 'playwright/.auth/user.json' });
```

---

## Flakiness Prevention

- Wait for network idle or specific response, not arbitrary `sleep`/`waitForTimeout`
- Use `waitForURL`, `waitForSelector`, or `waitForResponse` with explicit conditions
- Avoid asserting on animation mid-state — wait for it to complete
- Intercept and stub non-deterministic third-party services (analytics, chat widgets) — see `references/mocking.md` for HTTP interceptor patterns

---

## P2 Checklist (E2E-specific)

- [ ] No `sleep` or fixed `waitForTimeout` — replaced with explicit wait conditions
- [ ] Auth set up via API or storage state, not UI login flow
- [ ] POM used for any page referenced in more than one spec
- [ ] Selectors use `data-testid` or ARIA roles — no fragile CSS path selectors
- [ ] Third-party services intercepted or stubbed to prevent flakiness
- [ ] Tests run headless in CI without browser-specific configuration
