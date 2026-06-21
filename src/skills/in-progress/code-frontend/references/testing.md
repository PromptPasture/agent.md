# Testing

Tests verify behavior from the user's perspective — not implementation details. Write tests that would still pass after a refactor that changes no observable behavior.

---

## Scope

| Level | What it covers | Tools |
| --- | --- | --- |
| Unit | Pure functions, utilities, custom hooks in isolation | Vitest |
| Component | A single component — render output, interactions, async states | Vitest + Testing Library |
| Integration | A feature composed of multiple components wired together | Vitest + Testing Library |

E2E (Playwright, Cypress) is outside this reference — it targets a running app, not co-located test files.

---

## Co-location Convention

Place test files next to the file they test. Never use a top-level `__tests__/` directory.

```
src/components/UserCard/
  UserCard.tsx
  UserCard.test.tsx        # component tests
  UserCard.types.ts
  index.ts

src/hooks/
  useDebounce.ts
  useDebounce.test.ts      # unit tests
```

---

## What to Test vs. What to Skip

### Test

- User-visible behavior: what renders, what the user sees after an action
- Interaction flows: click, type, submit, keyboard navigation
- Async states: loading, error, success — all three explicitly
- Edge cases that are part of the contract: empty list, disabled state, missing optional prop
- Custom hooks: input/output, not internal state shape

### Skip

- Implementation details: which `useState` variable holds a value, internal method calls
- Framework internals: whether `useEffect` ran, how many times a setter was called
- Snapshot tests as a primary strategy — they break on any markup change and assert nothing meaningful
- Styling: class names, CSS values — test behavior, not presentation

---

## Test Structure

One concept per test. Name tests as sentences: `renders a disabled button when loading is true`.

```ts
describe('UserCard', () => {
  it('renders the user name and avatar', () => {
    // Arrange
    render(<UserCard user={mockUser} />);

    // Act — none needed for render tests

    // Assert
    expect(screen.getByRole('heading', { name: mockUser.name })).toBeInTheDocument();
    expect(screen.getByRole('img', { name: mockUser.name })).toBeInTheDocument();
  });
});
```

---

## Query Priority

Prefer queries in this order — they reflect how users perceive the UI:

1. `getByRole` — most resilient, tests accessibility too
2. `getByLabelText` — for form inputs
3. `getByPlaceholderText` — last resort for inputs without labels
4. `getByText` — for visible copy
5. `getByTestId` — only when no semantic query is possible; add `data-testid` sparingly

Never query by class name or internal component structure.

---

## Component Tests

### Props and render output

```ts
it('renders a link when href is provided', () => {
  render(<UserCard user={mockUser} href="/profile/1" />);
  expect(screen.getByRole('link', { name: mockUser.name })).toHaveAttribute('href', '/profile/1');
});

it('renders a button when no href is provided', () => {
  render(<UserCard user={mockUser} onSelect={vi.fn()} />);
  expect(screen.getByRole('button', { name: mockUser.name })).toBeInTheDocument();
});
```

### User interactions

Use `userEvent` over `fireEvent` — it simulates real browser behavior including focus, pointer events, and keyboard sequences.

```ts
import userEvent from '@testing-library/user-event';

it('calls onSelect when the card is clicked', async () => {
  const user = userEvent.setup();
  const onSelect = vi.fn();

  render(<UserCard user={mockUser} onSelect={onSelect} />);
  await user.click(screen.getByRole('button', { name: mockUser.name }));

  expect(onSelect).toHaveBeenCalledOnce();
});

it('calls onSelect on Enter keypress', async () => {
  const user = userEvent.setup();
  const onSelect = vi.fn();

  render(<UserCard user={mockUser} onSelect={onSelect} />);
  screen.getByRole('button', { name: mockUser.name }).focus();
  await user.keyboard('{Enter}');

  expect(onSelect).toHaveBeenCalledOnce();
});
```

### Async states — all three, explicitly

```ts
it('shows a loading skeleton while data is fetching', () => {
  server.use(http.get('/api/users/:id', () => new Promise(() => {})));
  render(<UserProfile id="1" />);
  expect(screen.getByRole('status', { name: /loading/i })).toBeInTheDocument();
});

it('shows an error message when the fetch fails', async () => {
  server.use(http.get('/api/users/:id', () => HttpResponse.error()));
  render(<UserProfile id="1" />);
  expect(await screen.findByRole('alert')).toHaveTextContent(/failed to load/i);
});

it('renders the user profile on success', async () => {
  render(<UserProfile id="1" />);
  expect(await screen.findByRole('heading', { name: mockUser.name })).toBeInTheDocument();
});
```

---

## Unit Tests — Hooks

Test hooks via `renderHook`. Test the input/output contract, not internal implementation.

```ts
import { renderHook, act } from '@testing-library/react';
import { useDebounce } from './useDebounce';

it('returns the initial value immediately', () => {
  const { result } = renderHook(() => useDebounce('hello', 300));
  expect(result.current).toBe('hello');
});

it('updates the value after the delay', async () => {
  vi.useFakeTimers();
  const { result, rerender } = renderHook(({ value }) => useDebounce(value, 300), {
    initialProps: { value: 'hello' },
  });

  rerender({ value: 'world' });
  expect(result.current).toBe('hello');

  act(() => vi.advanceTimersByTime(300));
  expect(result.current).toBe('world');

  vi.useRealTimers();
});
```

---

## Unit Tests — Pure Functions

No render needed. Test inputs, outputs, and edge cases directly.

```ts
import { formatCurrency } from './formatCurrency';

it('formats a positive amount with the currency symbol', () => {
  expect(formatCurrency(1234.5, 'USD')).toBe('$1,234.50');
});

it('handles zero', () => {
  expect(formatCurrency(0, 'USD')).toBe('$0.00');
});

it('handles negative amounts', () => {
  expect(formatCurrency(-50, 'USD')).toBe('-$50.00');
});
```

---

## Integration Tests

Test a complete user flow through a feature — multiple components wired together, including real state and side effects. Mock only at the network boundary (MSW).

```ts
it('submits a contact form and shows a success confirmation', async () => {
  const user = userEvent.setup();

  render(<ContactPage />);

  await user.type(screen.getByLabelText(/name/i), 'Ada Lovelace');
  await user.type(screen.getByLabelText(/email/i), 'ada@example.com');
  await user.type(screen.getByLabelText(/message/i), 'Hello there');
  await user.click(screen.getByRole('button', { name: /send/i }));

  expect(await screen.findByRole('status')).toHaveTextContent(/message sent/i);
});

it('shows field errors when submitting an empty form', async () => {
  const user = userEvent.setup();

  render(<ContactPage />);
  await user.click(screen.getByRole('button', { name: /send/i }));

  expect(await screen.findByText(/name is required/i)).toBeInTheDocument();
  expect(screen.getByText(/email is required/i)).toBeInTheDocument();
});
```

---

## Mocking

### Network — use MSW

Mock at the network layer with Mock Service Worker, not by mocking `fetch` or `axios` directly. This tests the full data-fetching path.

```ts
// test-setup/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({ id: params.id, name: 'Ada Lovelace' });
  }),
];
```

### Modules and dependencies

Mock a module only when it has side effects that cannot run in a test environment (file system, device API, third-party SDK). Never mock a module just to avoid testing it.

```ts
// Good — mocking a browser API unavailable in jsdom
vi.mock('./useGeolocation', () => ({
  useGeolocation: () => ({ lat: 51.5, lng: -0.1 }),
}));

// Bad — mocking a utility to avoid testing it
vi.mock('./formatDate', () => ({ formatDate: vi.fn(() => '2024-01-01') }));
```

---

## Accessibility in Tests

`getByRole` queries validate semantic structure implicitly. Add explicit a11y assertions for critical paths:

```ts
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

it('has no accessibility violations', async () => {
  const { container } = render(<UserCard user={mockUser} />);
  expect(await axe(container)).toHaveNoViolations();
});
```

Run axe checks on forms, dialogs, and any component with custom ARIA usage.
