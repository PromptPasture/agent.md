# Browser Storage

Pick the storage mechanism that matches data scope, lifetime, size, and sensitivity. Never store sensitive data client-side without understanding security trade-offs.

---

## Decision Guide

```
Does the data need to be sent to the server on every request (e.g. auth)?
  └─ Yes → Cookie (HttpOnly for tokens)

Does the data need to be readable on the server during SSR?
  └─ Yes → Cookie

Does the data need to survive closing the browser tab but not the browser?
  └─ Yes → sessionStorage

Does the data need to survive closing the browser entirely?
  └─ Yes → Is it small and simple (< 5 MB, string values)?
              └─ Yes → localStorage
            Is it large, structured, or queried?
              └─ Yes → IndexedDB

Does the data need to be available offline (PWA)?
  └─ Yes → IndexedDB (data) + Cache API (responses)
```

---

## Cookies

**Use for:** authentication tokens, session IDs, locale preference, consent flags, A/B test assignments — anything the server needs to read on every request.

### Security attributes — always set all three

```ts
// Server-set cookie (preferred for auth tokens)
Set-Cookie: session=abc123;
  HttpOnly;          // JS cannot read — protects against XSS
  Secure;            // HTTPS only
  SameSite=Strict;   // no cross-site send (use Lax for OAuth flows)
  Path=/;
  Max-Age=86400      // 1 day in seconds
```

```ts
// Client-set cookie (for non-sensitive preferences only)
function setCookie(name: string, value: string, days: number): void {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`;
}

function getCookie(name: string): string | null {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith(`${name}=`))
    ?.split('=')[1]
    .then(decodeURIComponent) ?? null;
}

function deleteCookie(name: string): void {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
}
```

### Rules

- **Never store auth tokens in `localStorage`**: use `HttpOnly` cookies; JS cannot read them, making them immune to XSS
- Use `SameSite=Strict` for auth; `SameSite=Lax` for OAuth redirect flows; never `SameSite=None` without `Secure`
- Max cookie size is ~4 KB per cookie — store IDs, not payloads
- Cookies are sent on every matching request — keep them small

---

## localStorage

**Use for:** non-sensitive user preferences (theme, language, UI state), cached non-critical data, feature flag overrides, draft content.

```ts
// Typed localStorage wrapper
const storage = {
  get<T>(key: string): T | null {
    try {
      const item = localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : null;
    } catch {
      return null;
    }
  },

  set<T>(key: string, value: T): void {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (err) {
      // Quota exceeded or private browsing mode
      console.warn(`localStorage.set failed for key "${key}":`, err);
    }
  },

  remove(key: string): void {
    localStorage.removeItem(key);
  },
};
```

### Rules

- **Synchronous**: large reads/writes block the main thread; keep values small
- **Not available during SSR**: always guard with `typeof window !== 'undefined'`
- **Shared across all tabs** of the same origin — changes are visible immediately
- **Persists until cleared**: no expiry mechanism; implement your own if needed
- **5–10 MB limit** depending on browser — not for large datasets
- **Never store tokens, passwords, PII, or payment data**: XSS can read everything in `localStorage`

```ts
// SSR guard
function getTheme(): 'light' | 'dark' {
  if (typeof window === 'undefined') return 'light'; // SSR default
  return storage.get<'light' | 'dark'>('theme') ?? 'light';
}
```

---

## sessionStorage

**Use for:** form state across a multi-step flow within a single tab, temporary UI state that should reset when the tab closes.

```ts
// Same API as localStorage — scoped to the current tab and session
sessionStorage.setItem('step', JSON.stringify({ index: 2, answers: [] }));
const step = JSON.parse(sessionStorage.getItem('step') ?? 'null');
```

### Rules

- **Tab-scoped**: not shared between tabs, even same origin
- **Cleared on tab close**: survives page reload within the tab
- **Not available during SSR**: same guard as `localStorage`
- Same 5–10 MB limit as `localStorage`

---

## IndexedDB

**Use for:** large datasets, structured/queryable data, offline-first apps (PWA), client-side caching of API responses, binary data (files, images, blobs).

Use a wrapper library — the native API is verbose. `idb` is the standard lightweight wrapper.

```ts
import { openDB, type DBSchema } from 'idb';

interface AppDB extends DBSchema {
  products: {
    key: string;
    value: {
      id: string;
      name: string;
      price: number;
      updatedAt: number;
    };
    indexes: { 'by-updated': number };
  };
}

const dbPromise = openDB<AppDB>('app-db', 1, {
  upgrade(db) {
    const store = db.createObjectStore('products', { keyPath: 'id' });
    store.createIndex('by-updated', 'updatedAt');
  },
});

// Read
async function getProduct(id: string) {
  return (await dbPromise).get('products', id);
}

// Write
async function saveProduct(product: AppDB['products']['value']) {
  return (await dbPromise).put('products', product);
}

// Query by index
async function getRecentProducts(since: number) {
  return (await dbPromise).getAllFromIndex('products', 'by-updated', IDBKeyRange.lowerBound(since));
}

// Delete
async function deleteProduct(id: string) {
  return (await dbPromise).delete('products', id);
}
```

### Rules

- **Asynchronous**: all operations return Promises; never blocks the main thread
- **Large capacity**: typically 50–80% of available disk space
- **Available offline**: works without a network connection; core to PWA offline strategy
- **Persists until cleared**: implement expiry with a `updatedAt` timestamp and periodic cleanup
- **Not shared across origins**: same-origin isolation like other storage
- See `references/pwa.md` for IndexedDB + Cache API offline patterns

---

## Comparison

||Cookie|localStorage|sessionStorage|IndexedDB|
|---|---|---|---|---|
|Capacity|~4 KB|5–10 MB|5–10 MB|50–80% disk|
|Lifetime|Configurable|Until cleared|Tab session|Until cleared|
|Server-readable|✓|✗|✗|✗|
|SSR-safe|✓|✗|✗|✗|
|Cross-tab|✓|✓|✗|✓|
|Async|✗|✗|✗|✓|
|Offline (PWA)|Partial|✓|✗|✓|
|Auth tokens|✓ (HttpOnly)|✗|✗|✗|

---

## Security Rules

- **Never store in `localStorage` or `sessionStorage`:** auth tokens, JWTs, session IDs, passwords, payment details, PII — XSS can exfiltrate everything
- **Auth tokens belong in `HttpOnly` cookies**: the browser sends them automatically, JS cannot read them
- **Encrypt sensitive data** before writing to IndexedDB if it must be stored client-side
- **Sanitise on read**: always validate and parse storage values; treat them as untrusted input
- **Clear on sign-out**: explicitly remove all storage entries on logout; do not rely on expiry alone

---

## Storage Events (Cross-Tab Sync)

`localStorage` fires a `storage` event in other tabs when a value changes:

```ts
window.addEventListener('storage', (event) => {
  if (event.key === 'theme') {
    applyTheme(event.newValue as 'light' | 'dark');
  }
});
```

Use this to sync preferences or session state across open tabs without a server round-trip.
