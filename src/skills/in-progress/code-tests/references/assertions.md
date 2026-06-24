# Assertions Reference

Guidance for writing assertions that are meaningful, readable, and failure-informative.

---

## Core Principles

- Assert on **observable outcomes**, not on implementation details
- Every assertion must be **falsifiable** — it must be possible for it to fail
- Assertion failure messages must identify **what went wrong** without reading the source
- Prefer **specific matchers** over generic truthy/falsy checks

---

## Specificity Ladder

Prefer the most specific matcher available:

```typescript
// Worst — passes on any truthy value
expect(result).toBeTruthy();

// Better — asserts the type
expect(result).toBeDefined();

// Good — asserts the value
expect(result.status).toBe('pending');

// Best — asserts the full shape
expect(result).toMatchObject({
  status: 'pending',
  total: 9999,
  currency: 'USD',
});
```

---

## What NOT to Assert

- **Internal state**: private fields, internal counters, call counts (unless the side effect is the subject)
- **Implementation choices**: which method was called internally, which SQL query ran
- **Framework internals**: React component lifecycle, ORM internals
- **Irrelevant fields**: don't assert every field when only two are relevant to the scenario

```typescript
// Bad — asserts on implementation detail
expect(orderRepository.save).toHaveBeenCalledTimes(1);

// Good — asserts on observable outcome
const order = await db.orders.findById(result.id);
expect(order.status).toBe('pending');
```

---

## Error Assertions

Always assert on both the error type and the message/code:

```typescript
// Bad — only asserts something was thrown
await expect(service.createOrder(input)).rejects.toThrow();

// Good — asserts on error shape
await expect(service.createOrder(input)).rejects.toMatchObject({
  code: 'VALIDATION_ERROR',
  message: expect.stringContaining('items'),
});
```

For HTTP responses, assert on the full error body:

```typescript
expect(res.status).toBe(400);
expect(res.body).toMatchObject({
  code: 'VALIDATION_ERROR',
  fields: { items: expect.arrayContaining(['required']) },
});
```

---

## Async Assertions

Always `await` async assertions — un-awaited assertions always pass:

```typescript
// Bug — always passes
expect(asyncOperation()).resolves.toBe('done');

// Correct
await expect(asyncOperation()).resolves.toBe('done');
```

---

## Snapshot Assertions

Use snapshot assertions only for:

- Large, stable serialised outputs (CLI help text, generated SQL, report formats)
- UI component render output when reviewed and approved

Do not use snapshots for:

- API response bodies — assert on shape instead
- Database state — assert on specific fields
- Objects that include timestamps, UUIDs, or other non-deterministic values

When using snapshots, always review the generated snapshot before committing it.

---

## Readable Failure Messages

Add a message to assertions when the default failure output is ambiguous:

```typescript
// Jest / Vitest — second positional argument
expect(order.status, `order ${order.id} should be pending after creation`).toBe('pending');

// Playwright — options object, not positional argument
await expect(page.locator('[data-testid="status"]'), { message: 'order status should be pending after creation' }).toHaveText('pending');
```

Use `expect.soft` (Playwright) or equivalent to collect all failures in one run rather than stopping at the first:

```typescript
// Playwright
await expect.soft(page.locator('[data-testid="price"]')).toHaveText('$99.99');
await expect.soft(page.locator('[data-testid="stock"]')).toHaveText('In stock');
```

---

## Negative Assertions

Assert explicitly on absence — do not rely on the absence of a positive assertion:

```typescript
// Bad — does not verify the order was NOT created
const result = await service.createOrder(invalidInput);
expect(result).toBeUndefined();

// Good — verifies DB state directly
const orders = await db.orders.findByUserId(userId);
expect(orders).toHaveLength(0);
```
