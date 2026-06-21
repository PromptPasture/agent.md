# Progressive Web App (PWA)

A PWA must be useful offline or in poor network conditions — not just installable. Start with a solid manifest and service worker caching strategy before adding the install prompt.

---

## Checklist Before Shipping

- [ ] `manifest.json` linked in `<head>` with all required fields
- [ ] Service worker registered and active
- [ ] App works on a slow 3G connection (test in DevTools → Network throttling)
- [ ] App shows meaningful UI when fully offline
- [ ] Icons provided at 192×192 and 512×512 (maskable variants included)
- [ ] `theme-color` matches the app's primary colour
- [ ] HTTPS in production (required for service workers)

---

## Web App Manifest

```json
// public/manifest.json
{
  "name": "MyApp — Full Application Name",
  "short_name": "MyApp",
  "description": "One sentence describing what the app does.",
  "start_url": "/",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#ffffff",
  "theme_color": "#6366f1",
  "icons": [
    { "src": "/icons/icon-192.png",          "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-512.png",          "sizes": "512x512", "type": "image/png" },
    { "src": "/icons/icon-512-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ],
  "screenshots": [
    { "src": "/screenshots/desktop.png", "sizes": "1280x800", "type": "image/png", "form_factor": "wide",   "label": "Dashboard view" },
    { "src": "/screenshots/mobile.png",  "sizes": "390x844",  "type": "image/png", "form_factor": "narrow", "label": "Mobile home screen" }
  ]
}
```

Link in `<head>`:

```html
<link rel="manifest" href="/manifest.json" />
<meta name="theme-color" content="#6366f1" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="default" />
<link rel="apple-touch-icon" href="/icons/icon-192.png" />
```

---

## Service Worker

Use **Workbox** — it handles cache versioning, precaching, and runtime strategies. Never write service workers by hand for production use.

Register the service worker as early as possible:

```ts
// Framework-agnostic registration
if ('serviceWorker' in navigator) {
  window.addEventListener('load', async () => {
    try {
      const reg = await navigator.serviceWorker.register('/sw.js');
      console.log('SW registered:', reg.scope);
    } catch (err) {
      console.error('SW registration failed:', err);
    }
  });
}
```

---

## Caching Strategies

| Strategy | Behaviour | Use for |
| --- | --- | --- |
| `CacheFirst` | Serve from cache; update in background | Static assets, fonts, images |
| `NetworkFirst` | Try network; fall back to cache on failure | API responses, dynamic pages |
| `StaleWhileRevalidate` | Serve cache immediately; refresh in background | Non-critical data, avatars |
| `NetworkOnly` | Always network — no cache | Auth, payments, writes |
| `CacheOnly` | Always cache — no network | Offline-only content |

**Never cache `POST`, `PUT`, `PATCH`, or `DELETE` requests.**

Recommended runtime caching rules:

```
API responses    → NetworkFirst,          TTL 24h, max 100 entries
Images           → CacheFirst,            TTL 30d, max 60 entries
Fonts            → CacheFirst,            TTL 365d, max 10 entries
Static assets    → StaleWhileRevalidate,  TTL 30d
Navigation       → NetworkFirst with offline fallback page
Auth endpoints   → NetworkOnly
```

---

## Offline UI

Always show meaningful UI when the app is offline — never a blank screen.

### Detect online status

```ts
// Plain JS — framework-agnostic
function getOnlineStatus(): boolean {
  return navigator.onLine;
}

function onOnlineStatusChange(callback: (isOnline: boolean) => void): () => void {
  const handleOnline  = () => callback(true);
  const handleOffline = () => callback(false);

  window.addEventListener('online',  handleOnline);
  window.addEventListener('offline', handleOffline);

  // Return cleanup function
  return () => {
    window.removeEventListener('online',  handleOnline);
    window.removeEventListener('offline', handleOffline);
  };
}
```

Wire into the framework's reactive system in the framework adapter.

### Offline banner

```html
<!-- Always in DOM — toggle visibility via JS, not DOM insertion -->
<div id="offline-banner" role="status" aria-live="polite" hidden>
  You are offline. Some features may be unavailable.
</div>
```

```ts
const banner = document.getElementById('offline-banner')!;
const cleanup = onOnlineStatusChange(isOnline => {
  banner.hidden = isOnline;
});
```

### Offline fallback page

Serve a static `offline.html` for navigation requests that fail when offline. Configure Workbox to use it as the navigation fallback:

```html
<!-- public/offline.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Offline — MyApp</title>
</head>
<body>
  <main>
    <h1>You are offline</h1>
    <p>Check your connection and try again.</p>
    <button onclick="window.location.reload()">Retry</button>
  </main>
</body>
</html>
```

---

## Install Prompt

The browser controls when `beforeinstallprompt` fires. Capture it, defer display until the user has seen value from the app, then trigger on explicit user action.

```ts
interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

class InstallPromptManager {
  private prompt: BeforeInstallPromptEvent | null = null;
  private installed = false;

  constructor() {
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      this.prompt = e as BeforeInstallPromptEvent;
      this.onPromptAvailable?.();
    });

    window.addEventListener('appinstalled', () => {
      this.installed = true;
      this.prompt = null;
      this.onInstalled?.();
    });
  }

  get canInstall(): boolean {
    return !!this.prompt && !this.installed;
  }

  async triggerInstall(): Promise<'accepted' | 'dismissed' | 'unavailable'> {
    if (!this.prompt) return 'unavailable';
    await this.prompt.prompt();
    const { outcome } = await this.prompt.userChoice;
    if (outcome === 'accepted') this.prompt = null;
    return outcome;
  }

  onPromptAvailable?: () => void;
  onInstalled?: () => void;
}

export const installPrompt = new InstallPromptManager();
```

---

## Background Sync

Queue failed writes and replay them when connectivity is restored:

```ts
// Main thread — queue on failure, register sync tag
async function saveOffline(key: string, data: unknown): Promise<void> {
  // Store pending data in IndexedDB (see references/storage.md)
  await db.set('pending', key, data);

  if ('serviceWorker' in navigator && 'SyncManager' in window) {
    const reg = await navigator.serviceWorker.ready;
    await reg.sync.register(`sync-${key}`);
  }
}

// Service worker — replay on reconnect
self.addEventListener('sync', (event: SyncEvent) => {
  if (event.tag.startsWith('sync-')) {
    event.waitUntil(replayPending(event.tag));
  }
});
```

Background Sync has limited browser support — always provide a **manual retry path** as a fallback for browsers that do not support it.

---

## Testing

| Tool | What to check |
| --- | --- |
| DevTools → Application → Manifest | Manifest parsed correctly, all icons load |
| DevTools → Application → Service Workers | SW registered, active, no console errors |
| DevTools → Network → Offline | App loads from cache when offline |
| DevTools → Network → Slow 3G | App is usable under poor network |
| Lighthouse → PWA audit | Installability, offline readiness, splash screen |
| Workbox logging (dev) | Cache hits, misses, and strategy decisions |
