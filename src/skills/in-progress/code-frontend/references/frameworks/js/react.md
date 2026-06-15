# React — Framework Adapter

Core React patterns that work in any React environment (Vite SPA, CRA, Remix, and as the base for Next.js). For Next.js-specific patterns see `references/frameworks/js/nextjs.md`.

---

## Conventions

### File extensions

- `.tsx` — React components
- `.ts` — hooks, utilities, types

### Hook naming

Prefix all custom hooks with `use`. One responsibility per hook.

```ts
export function useUserProfile(id: string) { ... }
export function useDebounce<T>(value: T, delay: number) { ... }
```

### Props — destructure at signature, optional props last

```tsx
function UserCard({ user, onSelect, className }: UserCardProps) { ... }
```

### Hooks rules

- Never call hooks conditionally or inside loops
- All hook calls at the top of the component function

```tsx
// Bad
if (isEnabled) { const [state] = useState(false); }

// Good
const [state, setState] = useState(false);
if (!isEnabled) return null;
```

### Return named objects from custom hooks

```tsx
// Good
const { data, isLoading, error } = useUserProfile(id);

// Exception — mirroring useState is acceptable
const [count, setCount] = useCounter(0);
```

---

## Error Handling

### react-error-boundary

```tsx
import { ErrorBoundary, type FallbackProps } from 'react-error-boundary';

function FeatureFallback({ error, resetErrorBoundary }: FallbackProps) {
  return (
    <section role="alert">
      <p>Failed to load: {error.message}</p>
      <button onClick={resetErrorBoundary}>Retry</button>
    </section>
  );
}

export function FeatureRoot() {
  return (
    <ErrorBoundary FallbackComponent={FeatureFallback}>
      <Feature />
    </ErrorBoundary>
  );
}
```

### Component error states

```tsx
function UserProfile({ id }: { id: string }) {
  const { data, isLoading, error } = useUserProfile(id);

  if (isLoading) return <UserProfileSkeleton />;
  if (error)     return <ErrorMessage error={error} onRetry={refetch} />;
  return <UserProfileView user={data} />;
}
```

### Reusable ErrorMessage

```tsx
export function ErrorMessage({ error, onRetry }: { error: Error | string; onRetry?: () => void }) {
  return (
    <div role="alert" aria-live="assertive">
      <p>{typeof error === 'string' ? error : error.message}</p>
      {onRetry && <button onClick={onRetry} type="button">Try again</button>}
    </div>
  );
}
```

---

## Motion — Framer Motion

### Reduced motion

```tsx
import { useReducedMotion, motion } from 'framer-motion';

function AnimatedCard({ children }: { children: React.ReactNode }) {
  const reduced = useReducedMotion();
  return (
    <motion.div
      initial={{ opacity: 0, y: reduced ? 0 : 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: reduced ? 0 : 0.2 }}
    >
      {children}
    </motion.div>
  );
}
```

### Fade and slide

```tsx
const fadeSlide = {
  hidden:  { opacity: 0, y: 12 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.2, ease: 'easeOut' } },
  exit:    { opacity: 0, y: -8, transition: { duration: 0.15 } },
};

export function Card({ children }: { children: React.ReactNode }) {
  return (
    <motion.div variants={fadeSlide} initial="hidden" animate="visible" exit="exit">
      {children}
    </motion.div>
  );
}
```

### Staggered list

```tsx
const list = { visible: { transition: { staggerChildren: 0.05 } } };
const item = { hidden: { opacity: 0, y: 8 }, visible: { opacity: 1, y: 0 } };

export function AnimatedList({ items }: { items: string[] }) {
  return (
    <motion.ul variants={list} initial="hidden" animate="visible">
      {items.map((text, i) => <motion.li key={i} variants={item}>{text}</motion.li>)}
    </motion.ul>
  );
}
```

### Shared layout + AnimatePresence

```tsx
import { AnimatePresence, motion } from 'framer-motion';

<motion.div layoutId={`card-${id}`} />

<AnimatePresence mode="wait">
  {isOpen && <Modal key="modal" />}
</AnimatePresence>
```

### View Transitions wiring

```tsx
import { flushSync } from 'react-dom';

function navigateWithTransition(update: () => void) {
  if ('startViewTransition' in document) {
    document.startViewTransition(() => flushSync(update));
  } else {
    update();
  }
}
```

---

## Accessibility

### Focus management

```tsx
function Dialog({ isOpen, onClose }: DialogProps) {
  const dialogRef  = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (isOpen) dialogRef.current?.focus();
    else        triggerRef.current?.focus();
  }, [isOpen]);

  return (
    <>
      <button ref={triggerRef} onClick={() => setOpen(true)}>Open</button>
      {isOpen && (
        <div ref={dialogRef} role="dialog" tabIndex={-1} aria-modal="true">
          {/* content */}
        </div>
      )}
    </>
  );
}
```

### Focus trap hook

```tsx
const FOCUSABLE = [
  'a[href]', 'button:not([disabled])', 'input:not([disabled])',
  'select:not([disabled])', 'textarea:not([disabled])',
  '[tabindex]:not([tabindex="-1"])',
].join(', ');

export function useFocusTrap(ref: React.RefObject<HTMLElement>, active: boolean) {
  useEffect(() => {
    if (!active || !ref.current) return;
    const els   = Array.from(ref.current.querySelectorAll<HTMLElement>(FOCUSABLE));
    const first = els[0];
    const last  = els[els.length - 1];

    function onKeyDown(e: KeyboardEvent) {
      if (e.key !== 'Tab') return;
      if (e.shiftKey) { if (document.activeElement === first) { e.preventDefault(); last.focus(); } }
      else            { if (document.activeElement === last)  { e.preventDefault(); first.focus(); } }
    }

    ref.current.addEventListener('keydown', onKeyDown);
    first?.focus();
    return () => ref.current?.removeEventListener('keydown', onKeyDown);
  }, [active, ref]);
}
```

---

## Performance

### Memoization

```tsx
const UserCard = memo(function UserCard({ user }: UserCardProps) {
  return <div>{user.name}</div>;
});

const handleSelect = useCallback((id: string) => setSelected(id), []);

const sorted = useMemo(
  () => [...items].sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);
```

### List virtualisation — @tanstack/react-virtual

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 56,
    overscan: 5,
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize(), position: 'relative' }}>
        {virtualizer.getVirtualItems().map(row => (
          <div key={row.key} style={{ position: 'absolute', top: row.start, width: '100%' }}>
            <ItemRow item={items[row.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Code splitting — lazy / Suspense (Vite)

```tsx
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
<Suspense fallback={<PageSkeleton />}><Dashboard /></Suspense>
```

### Debounce

```tsx
const debouncedSearch = useMemo(() => debounce((q: string) => fetchResults(q), 300), []);
<input onChange={e => debouncedSearch(e.target.value)} />
```

---

## Data Fetching

### React Query — useQuery

```ts
import { useQuery } from '@tanstack/react-query';

export function useUser(id: string) {
  return useQuery<User, Error>({
    queryKey: ['users', id],
    queryFn: () => fetchUser(id),
    staleTime: 1000 * 60 * 5,
  });
}
```

### React Query — useMutation with optimistic update

```ts
export function useUpdateUser() {
  const queryClient = useQueryClient();
  return useMutation<User, Error, UpdateUserInput>({
    mutationFn: updateUser,
    onMutate: async (input) => {
      await queryClient.cancelQueries({ queryKey: ['users', input.id] });
      const previous = queryClient.getQueryData<User>(['users', input.id]);
      queryClient.setQueryData(['users', input.id], { ...previous, ...input });
      return { previous };
    },
    onError: (_err, input, ctx) => {
      queryClient.setQueryData(['users', input.id], ctx?.previous);
    },
    onSuccess: (updated) => {
      queryClient.setQueryData(['users', updated.id], updated);
    },
  });
}
```

### SWR

```ts
import useSWR from 'swr';

export function useUser(id: string) {
  return useSWR<User>(`/api/users/${id}`, fetcher, { revalidateOnFocus: false });
}

export async function fetcher<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json() as Promise<T>;
}
```

### AbortController in useEffect

```tsx
useEffect(() => {
  const controller = new AbortController();
  async function load() {
    try {
      const data = await fetchUser(id, { signal: controller.signal });
      setUser(data);
    } catch (err) {
      if ((err as Error).name !== 'AbortError') setError(err as Error);
    }
  }
  load();
  return () => controller.abort();
}, [id]);
```

---

## Forms — React Hook Form + Zod

### Schema

```ts
import { z } from 'zod';

export const loginSchema = z.object({
  email:      z.string().min(1, 'Required').email('Enter a valid email'),
  password:   z.string().min(8, 'At least 8 characters'),
  rememberMe: z.boolean().optional().default(false),
});

export type LoginFormValues = z.infer<typeof loginSchema>;
```

### Form component

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

export function LoginForm({ onSubmit }: { onSubmit: (v: LoginFormValues) => Promise<void> }) {
  const { register, handleSubmit, formState: { errors, isSubmitting }, setError } =
    useForm<LoginFormValues>({
      resolver: zodResolver(loginSchema),
      mode: 'onBlur',
      reValidateMode: 'onChange',
    });

  async function submit(values: LoginFormValues) {
    try { await onSubmit(values); }
    catch { setError('root', { message: 'Something went wrong. Please try again.' }); }
  }

  return (
    <form onSubmit={handleSubmit(submit)} noValidate>
      <Field label="Email" error={errors.email?.message} required>
        <input {...register('email')} type="email" autoComplete="email" aria-invalid={!!errors.email} />
      </Field>
      <Field label="Password" error={errors.password?.message} required>
        <input {...register('password')} type="password" autoComplete="current-password" aria-invalid={!!errors.password} />
      </Field>
      {errors.root && <div role="alert">{errors.root.message}</div>}
      <button type="submit" disabled={isSubmitting} aria-busy={isSubmitting}>
        {isSubmitting ? 'Saving…' : 'Save'}
      </button>
    </form>
  );
}
```

### Field component

```tsx
import { useId, cloneElement } from 'react';

export function Field({ label, error, required, children }: FieldProps) {
  const id      = useId();
  const errorId = `${id}-error`;
  return (
    <div>
      <label htmlFor={id}>
        {label}
        {required && <span aria-hidden="true"> *</span>}
        {required && <span className="sr-only"> (required)</span>}
      </label>
      {cloneElement(children, { id, 'aria-describedby': error ? errorId : undefined })}
      {error && <p id={errorId} role="alert">{error}</p>}
    </div>
  );
}
```

---

## State

### useState

```tsx
const [isOpen,     setIsOpen]     = useState(false);
const [selectedId, setSelectedId] = useState<string | null>(null);

// Functional update when next state depends on previous
setItems(prev => prev.filter(item => item.id !== id));
```

### useReducer

```tsx
const [state, dispatch] = useReducer(reducer, { status: 'idle', data: null, error: null });
dispatch({ type: 'FETCH_START' });
dispatch({ type: 'FETCH_SUCCESS', payload: user });
```

### React Context

```tsx
const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const signOut = useCallback(async () => { await api.auth.signOut(); setUser(null); }, []);
  return <AuthContext.Provider value={{ user, signOut }}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
```

### Zustand

```ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

export const useCartStore = create<CartState>()(
  devtools(persist(
    (set, get) => ({
      items: [],
      addItem:    (item) => set(state => ({ items: [...state.items, item] })),
      removeItem: (id)   => set(state => ({ items: state.items.filter(i => i.id !== id) })),
      total:      ()     => get().items.reduce((sum, i) => sum + i.price * i.quantity, 0),
    }),
    { name: 'cart-storage' }
  ))
);
```

### Jotai

```ts
import { atom, useAtom, useAtomValue } from 'jotai';

const countAtom  = atom(0);
const doubleAtom = atom(get => get(countAtom) * 2);

function Counter() {
  const [count, setCount] = useAtom(countAtom);
  const double = useAtomValue(doubleAtom);
  return <button onClick={() => setCount(c => c + 1)}>{count} × 2 = {double}</button>;
}
```

### URL state (Vite / non-Next.js)

```ts
// Generic — works in any React app
function useQueryParam(key: string, defaultValue: string) {
  const params = new URLSearchParams(window.location.search);
  const value  = params.get(key) ?? defaultValue;

  function setValue(next: string) {
    const updated = new URLSearchParams(window.location.search);
    updated.set(key, next);
    window.history.pushState({}, '', `?${updated.toString()}`);
  }

  return [value, setValue] as const;
}
```

---

## PWA — Vite

```ts
// vite.config.ts
import { VitePWA } from 'vite-plugin-pwa';

VitePWA({
  registerType: 'autoUpdate',
  workbox: {
    globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
    navigateFallback: '/offline.html',
    runtimeCaching: [
      { urlPattern: /^https:\/\/api\./, handler: 'NetworkFirst',
        options: { cacheName: 'api-cache', expiration: { maxEntries: 100, maxAgeSeconds: 86400 }, networkTimeoutSeconds: 10 } },
      { urlPattern: /\.(?:png|jpg|jpeg|svg|webp)$/, handler: 'CacheFirst',
        options: { cacheName: 'image-cache', expiration: { maxEntries: 60, maxAgeSeconds: 2592000 } } },
    ],
  },
  manifest: {
    name: 'MyApp', short_name: 'MyApp', theme_color: '#6366f1',
    icons: [
      { src: '/icons/icon-192.png', sizes: '192x192', type: 'image/png' },
      { src: '/icons/icon-512.png', sizes: '512x512', type: 'image/png' },
    ],
  },
})
```

### Online status hook

```tsx
import { useSyncExternalStore } from 'react';

function subscribe(cb: () => void) {
  window.addEventListener('online',  cb);
  window.addEventListener('offline', cb);
  return () => { window.removeEventListener('online', cb); window.removeEventListener('offline', cb); };
}

export function useOnlineStatus(): boolean {
  return useSyncExternalStore(subscribe, () => navigator.onLine, () => true);
}
```

### Install prompt hook

```tsx
export function useInstallPrompt() {
  const [prompt, setPrompt]       = useState<BeforeInstallPromptEvent | null>(null);
  const [isInstalled, setInstalled] = useState(false);

  useEffect(() => {
    const onPrompt    = (e: Event) => { e.preventDefault(); setPrompt(e as BeforeInstallPromptEvent); };
    const onInstalled = () => { setInstalled(true); setPrompt(null); };
    window.addEventListener('beforeinstallprompt', onPrompt);
    window.addEventListener('appinstalled', onInstalled);
    return () => {
      window.removeEventListener('beforeinstallprompt', onPrompt);
      window.removeEventListener('appinstalled', onInstalled);
    };
  }, []);

  async function triggerInstall() {
    if (!prompt) return;
    await prompt.prompt();
    const { outcome } = await prompt.userChoice;
    if (outcome === 'accepted') setPrompt(null);
  }

  return { canInstall: !!prompt && !isInstalled, triggerInstall };
}
```

---

## i18n — react-i18next (Vite)

```ts
// lib/i18n.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import Backend from 'i18next-http-backend';

i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    ns: ['common', 'product', 'errors'],
    defaultNS: 'common',
    interpolation: { escapeValue: false },
    detection: { order: ['querystring', 'localStorage', 'navigator'], caches: ['localStorage'] },
    saveMissing: process.env.NODE_ENV === 'development',
    missingKeyHandler: (lng, ns, key) => console.warn(`Missing: ${lng}/${ns}/${key}`),
  });
```

```tsx
import { useTranslation, Trans } from 'react-i18next';

const { t } = useTranslation('product');
<Trans i18nKey="product:inStock" count={count}><strong>{{ count }}</strong> items left</Trans>
<span>{t('price', { price: product.price })}</span>
```
