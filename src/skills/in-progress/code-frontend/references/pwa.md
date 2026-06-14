# Progressive Web App (PWA)

A PWA must be useful offline or in poor network conditions — not just installable. Start with a solid manifest and service worker caching strategy before adding the install prompt.

---

## Checklist Before Shipping

- [ ] `manifest.json` linked in `<head>` with all required fields
- [ ] Service worker registered and active
- [ ] App works on a slow 3G connection (test in DevTools)
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
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512-maskable.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ],
  "screenshots": [
    {
      "src": "/screenshots/desktop.png",
      "sizes": "1280x800",
      "type": "image/png",
      "form_factor": "wide",
      "label": "Dashboard view"
    },
    {
      "src": "/screenshots/mobile.png",
      "sizes": "390x844",
      "type": "image/png",
      "form_factor": "narrow",
      "label": "Mobile home screen"
    }
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

### Using Workbox (recommended)

Workbox handles cache versioning, precaching, and runtime strategies. Use it via the framework plugin rather than writing service workers by hand.

#### Vite — vite-plugin-pwa

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
        runtimeCaching: [
          {
            // Cache API responses — network first, fall back to cache
            urlPattern: /^https:\/\/api\.myapp\.com\/.*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: { maxEntries: 100, maxAgeSeconds: 60 * 60 * 24 }, // 24h
              networkTimeoutSeconds: 10,
            },
          },
          {
            // Cache images — cache first
            urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
            handler: 'CacheFirst',
            options: {
              cacheName: 'image-cache',
              expiration: { maxEntries: 60, maxAgeSeconds: 60 * 60 * 24 * 30 }, // 30d
            },
          },
        ],
      },
      manifest: {
        name: 'MyApp',
        short_name: 'MyApp',
        theme_color: '#6366f1',
        icons: [
          { src: '/icons/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: '/icons/icon-512.png', sizes: '512x512', type: 'image/png' },
        ],
      },
    }),
  ],
});
```

#### Next.js — next-pwa

```ts
// next.config.ts
import withPWA from 'next-pwa';

export default withPWA({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development',
  runtimeCaching: [
    {
      urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
      handler: 'CacheFirst',
      options: { cacheName: 'google-fonts', expiration: { maxEntries: 4, maxAgeSeconds: 365 * 24 * 60 * 60 } },
    },
  ],
})({
  // ...your next config
});
```

---

## Caching Strategies

| Strategy | Behaviour | Use for |
| --- | --- | --- |
| `CacheFirst` | Serve from cache; update in background | Static assets, fonts, images |
| `NetworkFirst` | Try network; fall back to cache | API responses, dynamic pages |
| `StaleWhileRevalidate` | Serve cache immediately; refresh in background | Non-critical data, avatars |
| `NetworkOnly` | Always network — no cache | Authentication, payments, writes |
| `CacheOnly` | Always cache — no network | Offline-only content |

Never cache `POST`, `PUT`, `PATCH`, or `DELETE` requests.

---

## Offline UI

Always show meaningful UI when the app is offline — never a blank screen.

```tsx
// hooks/useOnlineStatus.ts
import { useSyncExternalStore } from 'react';

function subscribe(callback: () => void) {
  window.addEventListener('online', callback);
  window.addEventListener('offline', callback);
  return () => {
    window.removeEventListener('online', callback);
    window.removeEventListener('offline', callback);
  };
}

export function useOnlineStatus(): boolean {
  return useSyncExternalStore(
    subscribe,
    () => navigator.onLine,
    () => true // server snapshot — assume online
  );
}
```

```tsx
// components/OfflineBanner/OfflineBanner.tsx
export function OfflineBanner() {
  const isOnline = useOnlineStatus();

  if (isOnline) return null;

  return (
    <div role="status" aria-live="polite">
      You are offline. Some features may be unavailable.
    </div>
  );
}
```

For pages that cannot function offline, show a dedicated fallback:

```tsx
// app/offline/page.tsx (Next.js) or public/offline.html (Vite)
export default function OfflinePage() {
  return (
    <main>
      <h1>You are offline</h1>
      <p>Check your connection and try again.</p>
      <button onClick={() => window.location.reload()}>Retry</button>
    </main>
  );
}
```

Configure Workbox to serve the offline page for navigation requests that fail:

```ts
// In workbox runtimeCaching
{
  urlPattern: ({ request }) => request.mode === 'navigate',
  handler: 'NetworkOnly',
  options: {
    plugins: [
      new WorkboxWindow.NavigationRoute(
        new WorkboxWindow.NetworkFirst(),
        { blacklist: [/^\/_/] }
      ),
    ],
    fetchOptions: { redirect: 'follow' },
  },
}
```

---

## Install Prompt

The browser controls when the install prompt is shown. Capture the event and defer it until a meaningful moment — not immediately on load.

```tsx
// hooks/useInstallPrompt.ts
import { useEffect, useState } from 'react';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export function useInstallPrompt() {
  const [prompt, setPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [isInstalled, setIsInstalled] = useState(false);

  useEffect(() => {
    function handlePrompt(e: Event) {
      e.preventDefault();
      setPrompt(e as BeforeInstallPromptEvent);
    }

    function handleInstalled() {
      setIsInstalled(true);
      setPrompt(null);
    }

    window.addEventListener('beforeinstallprompt', handlePrompt);
    window.addEventListener('appinstalled', handleInstalled);

    return () => {
      window.removeEventListener('beforeinstallprompt', handlePrompt);
      window.removeEventListener('appinstalled', handleInstalled);
    };
  }, []);

  async function triggerInstall() {
    if (!prompt) return;
    await prompt.prompt();
    const { outcome } = await prompt.userChoice;
    if (outcome === 'accepted') setPrompt(null);
  }

  return { canInstall: !!prompt && !isInstalled, triggerInstall, isInstalled };
}
```

```tsx
// Show only after the user has demonstrated value from the app
function InstallButton() {
  const { canInstall, triggerInstall } = useInstallPrompt();

  if (!canInstall) return null;

  return (
    <button onClick={triggerInstall} type="button">
      Add to home screen
    </button>
  );
}
```

---

## Background Sync

Queue failed writes and replay them when connectivity is restored:

```ts
// Register a sync tag when a write fails
async function saveOffline(data: FormData) {
  await localforage.setItem('pending-save', data);

  if ('serviceWorker' in navigator && 'SyncManager' in window) {
    const registration = await navigator.serviceWorker.ready;
    await registration.sync.register('sync-save');
  }
}

// In the service worker — listen for the sync event
self.addEventListener('sync', (event: SyncEvent) => {
  if (event.tag === 'sync-save') {
    event.waitUntil(replaySave());
  }
});
```

Background Sync has limited browser support — always provide a manual retry path as a fallback.

---

## Testing PWA Behaviour

| Tool | What to check |
| --- | --- |
| Chrome DevTools → Application → Manifest | Manifest parsed correctly, icons load |
| Chrome DevTools → Application → Service Workers | SW registered, active, no errors |
| Chrome DevTools → Network → Offline | App loads from cache when offline |
| Lighthouse PWA audit | Installability, offline, splash screen |
| `workbox-window` logging | Cache hits/misses in development |
