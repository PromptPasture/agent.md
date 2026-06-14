# State Management

Choose the simplest state solution that covers the need. Add complexity only when a simpler tool genuinely cannot do the job.

---

## Decision Tree

```
Is the state used by only one component?
  └─ Yes → useState / useReducer

Is the state shared between a few nearby components?
  └─ Yes → Lift state to the nearest common ancestor

Is the state server data (fetched, cached, synchronised)?
  └─ Yes → React Query / SWR / framework loader (see references/data-fetching.md)

Is the state shared across distant components or the whole app?
  └─ Yes → Is it simple (a few values, infrequent updates)?
              └─ Yes → React Context
            Is it complex (many slices, frequent updates, devtools needed)?
              └─ Yes → Zustand / Jotai / Redux Toolkit
```

---

## Local State — useState

Default for component-scoped state. Prefer multiple focused `useState` calls over a single object state unless the values always change together.

```tsx
// Good — independent pieces of state
const [isOpen, setIsOpen] = useState(false);
const [selectedId, setSelectedId] = useState<string | null>(null);

// Good — values that always change together belong in one object
const [pagination, setPagination] = useState({ page: 1, pageSize: 20 });
```

### Functional updates for derived state

```ts
// When next state depends on previous — always use functional form
setCount(prev => prev + 1);
setItems(prev => [...prev, newItem]);
setItems(prev => prev.filter(item => item.id !== id));
```

---

## Local Complex State — useReducer

Use when state has multiple sub-values with defined transitions, or when `useState` logic is scattered across many handlers.

```ts
type State = {
  status: 'idle' | 'loading' | 'success' | 'error';
  data: User | null;
  error: string | null;
};

type Action =
  | { type: 'FETCH_START' }
  | { type: 'FETCH_SUCCESS'; payload: User }
  | { type: 'FETCH_ERROR'; payload: string }
  | { type: 'RESET' };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'FETCH_START':   return { ...state, status: 'loading', error: null };
    case 'FETCH_SUCCESS': return { status: 'success', data: action.payload, error: null };
    case 'FETCH_ERROR':   return { status: 'error', data: null, error: action.payload };
    case 'RESET':         return { status: 'idle', data: null, error: null };
    default:              return state;
  }
}

const [state, dispatch] = useReducer(reducer, { status: 'idle', data: null, error: null });
```

---

## Shared State — React Context

Use for low-frequency global values: theme, locale, authenticated user, feature flags.

**Do not use Context for high-frequency updates** (e.g. mouse position, scroll, form fields) — it re-renders every consumer on every change.

```tsx
// contexts/AuthContext.tsx
interface AuthContextValue {
  user: User | null;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const signOut = useCallback(async () => {
    await api.auth.signOut();
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

// Always export a typed hook — never expose the raw context
export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
```

### Split contexts by update frequency

```tsx
// Split static and dynamic values into separate contexts
// so reading user doesn't re-render on every dispatch
const AuthUserContext = createContext<User | null>(null);
const AuthActionsContext = createContext<{ signOut: () => void } | null>(null);
```

---

## Global State — Zustand

Prefer Zustand for app-wide state that is too complex for Context or updates too frequently for it to be performant.

```ts
// stores/useCartStore.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clear: () => void;
  total: () => number;
}

export const useCartStore = create<CartState>()(
  devtools(
    persist(
      (set, get) => ({
        items: [],

        addItem: (item) =>
          set(state => {
            const existing = state.items.find(i => i.id === item.id);
            if (existing) {
              return {
                items: state.items.map(i =>
                  i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i
                ),
              };
            }
            return { items: [...state.items, { ...item, quantity: 1 }] };
          }),

        removeItem: (id) =>
          set(state => ({ items: state.items.filter(i => i.id !== id) })),

        updateQuantity: (id, quantity) =>
          set(state => ({
            items: quantity <= 0
              ? state.items.filter(i => i.id !== id)
              : state.items.map(i => i.id === id ? { ...i, quantity } : i),
          })),

        clear: () => set({ items: [] }),

        total: () => get().items.reduce((sum, i) => sum + i.price * i.quantity, 0),
      }),
      { name: 'cart-storage' }
    )
  )
);
```

### Slice pattern for large stores

Split large stores into slices and compose:

```ts
// stores/slices/uiSlice.ts
interface UiSlice {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
}

export const createUiSlice = (set: SetState): UiSlice => ({
  sidebarOpen: false,
  toggleSidebar: () => set(state => ({ sidebarOpen: !state.sidebarOpen })),
});

// stores/useAppStore.ts
export const useAppStore = create<UiSlice & CartSlice>()((...args) => ({
  ...createUiSlice(...args),
  ...createCartSlice(...args),
}));
```

---

## Atomic State — Jotai

Prefer Jotai when state is naturally atomic and components subscribe to independent slices without a shared store structure.

```ts
import { atom, useAtom, useAtomValue, useSetAtom } from 'jotai';

// Primitive atoms
const countAtom = atom(0);
const userAtom = atom<User | null>(null);

// Derived atom — computed from other atoms
const doubleCountAtom = atom(get => get(countAtom) * 2);

// Async atom
const userProfileAtom = atom(async get => {
  const user = get(userAtom);
  if (!user) return null;
  return fetchUserProfile(user.id);
});

// Usage
function Counter() {
  const [count, setCount] = useAtom(countAtom);
  const double = useAtomValue(doubleCountAtom);

  return (
    <div>
      <p>{count} × 2 = {double}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
    </div>
  );
}
```

---

## URL State

Treat the URL as state for anything the user should be able to bookmark, share, or navigate back to: filters, search queries, pagination, selected tabs.

```ts
// Next.js App Router
import { useRouter, useSearchParams, usePathname } from 'next/navigation';

function useFilters() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const filters = {
    category: searchParams.get('category') ?? 'all',
    page: Number(searchParams.get('page') ?? '1'),
  };

  function setFilter(key: string, value: string) {
    const params = new URLSearchParams(searchParams.toString());
    params.set(key, value);
    params.set('page', '1'); // reset pagination on filter change
    router.push(`${pathname}?${params.toString()}`);
  }

  return { filters, setFilter };
}
```

---

## Framework-Specific Patterns

| Framework | Local | Shared | Server data |
| --- | --- | --- | --- |
| Next.js (React) | `useState` / `useReducer` | Context / Zustand / Jotai | React Query / `fetch` in Server Components |
| SvelteKit | Svelte stores / runes | Writable stores / context | `load` functions |
| Nuxt / Vue | `ref` / `reactive` | Pinia | `useFetch` / `useAsyncData` |
| Remix | `useState` | Context | `loader` / `useFetcher` |
| Astro | Nano Stores | Nano Stores | Frontmatter `fetch` / API routes |

---

## Common Mistakes

```ts
// ❌ Deriving state from props in useState — gets out of sync
const [name, setName] = useState(user.name); // won't update when user changes

// ✅ Derive directly in render; memoize if expensive
const displayName = user.displayName ?? user.name;

// ❌ Storing server data in useState — bypasses caching and sync
const [users, setUsers] = useState([]);
useEffect(() => { fetch('/api/users').then(r => r.json()).then(setUsers); }, []);

// ✅ Use React Query — handles caching, refetch, loading, error
const { data: users } = useQuery({ queryKey: ['users'], queryFn: fetchUsers });

// ❌ Context for high-frequency updates — re-renders every consumer
const MouseContext = createContext({ x: 0, y: 0 });

// ✅ Use a ref or a dedicated library (use-mouse, @use-gesture) for high-frequency values
```
