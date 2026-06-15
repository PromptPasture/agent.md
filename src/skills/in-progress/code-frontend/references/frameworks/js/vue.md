# Vue 3 — Framework Adapter

Vue 3 with the Composition API. For Nuxt.js (Vue meta-framework) see `references/frameworks/nuxt.md`. This adapter covers Vite + Vue SPA and shared patterns used by Nuxt.

---

## Conventions

### File extensions

- `.vue` — Single File Components (SFC)
- `.ts` — composables, utilities, types
- `.d.ts` — type declarations

### SFC structure — always use `<script setup>`

```vue
<script setup lang="ts">
// 1. Imports
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import UserAvatar from '@/components/UserAvatar.vue';
import type { User } from '@/types/user';

// 2. Props and emits
interface Props {
  user: User;
  featured?: boolean;
}
const props = withDefaults(defineProps<Props>(), { featured: false });
const emit  = defineEmits<{ select: [id: string] }>();

// 3. Composables
const store = useUserStore();

// 4. State
const isExpanded = ref(false);

// 5. Computed
const displayName = computed(() => props.user.displayName ?? props.user.name);

// 6. Functions
function handleSelect() {
  emit('select', props.user.id);
}
</script>

<template>
  <article class="user-card" :class="{ featured }" @click="handleSelect">
    <UserAvatar :src="user.avatar" :alt="displayName" />
    <span class="name">{{ displayName }}</span>
  </article>
</template>

<style scoped>
.user-card { display: flex; gap: 1rem; }
.featured  { border: 2px solid var(--color-brand); }
</style>
```

---

## Error Handling

### Global error handler

```ts
// main.ts
const app = createApp(App);

app.config.errorHandler = (err, instance, info) => {
  console.error('Vue error:', err, info);
  // Send to error reporting service
};
```

### Error boundary component

```vue
<!-- components/ErrorBoundary.vue -->
<script setup lang="ts">
import { onErrorCaptured, ref } from 'vue';

const error = ref<Error | null>(null);

onErrorCaptured((err) => {
  error.value = err instanceof Error ? err : new Error(String(err));
  return false; // stop propagation
});

function retry() { error.value = null; }
</script>

<template>
  <div v-if="error" role="alert">
    <p>{{ error.message }}</p>
    <button @click="retry">Retry</button>
  </div>
  <slot v-else />
</template>
```

### Async component with error state

```vue
<script setup lang="ts">
const { data: user, error, status } = useUser(userId);
</script>

<template>
  <AppSkeleton v-if="status === 'pending'" />
  <AppError v-else-if="error" :error="error" @retry="refresh()" />
  <UserProfile v-else :user="user!" />
</template>
```

---

## Motion

Vue ships `<Transition>` and `<TransitionGroup>` for enter/leave animations.

```vue
<template>
  <Transition name="fade" appear>
    <div v-if="visible">Content</div>
  </Transition>

  <TransitionGroup name="list" tag="ul">
    <li v-for="item in items" :key="item.id">{{ item.name }}</li>
  </TransitionGroup>
</template>

<style>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to       { opacity: 0; }

.list-enter-active { transition: all 0.2s ease; }
.list-leave-active { transition: all 0.15s ease; }
.list-enter-from, .list-leave-to { opacity: 0; transform: translateY(8px); }
.list-move         { transition: transform 0.2s ease; }

@media (prefers-reduced-motion: reduce) {
  .fade-enter-active, .fade-leave-active,
  .list-enter-active, .list-leave-active,
  .list-move { transition: none; }
}
</style>
```

For complex animations use **@vueuse/motion** or GSAP.

---

## Accessibility

```vue
<script setup lang="ts">
import { ref, nextTick, onUnmounted } from 'vue';

const dialogRef = ref<HTMLElement | null>(null);
const triggerRef = ref<HTMLButtonElement | null>(null);
const isOpen = ref(false);

async function open() {
  isOpen.value = true;
  await nextTick();
  dialogRef.value?.focus();
}

async function close() {
  isOpen.value = false;
  await nextTick();
  triggerRef.value?.focus();
}
</script>

<template>
  <button ref="triggerRef" @click="open">Open dialog</button>
  <div v-if="isOpen" ref="dialogRef" role="dialog" :aria-modal="true" tabindex="-1">
    <button @click="close">Close</button>
    <slot />
  </div>
</template>
```

Use **@vueuse/core** `useFocusTrap` for focus trapping.

---

## Performance

### Computed over methods for derived values

```ts
// Good — cached until dependencies change
const sortedItems = computed(() => [...items.value].sort((a, b) => a.name.localeCompare(b.name)));

// Bad — recalculates on every render
function getSortedItems() { return [...items.value].sort(...); }
```

### v-memo for expensive list rows

```html
<!-- Only re-renders when item.id or selected changes -->
<div v-for="item in list" :key="item.id" v-memo="[item.id, selected === item.id]">
  <ExpensiveRow :item="item" :selected="selected === item.id" />
</div>
```

### Lazy-load routes and components

```ts
// router/index.ts
const routes = [
  { path: '/dashboard', component: () => import('@/views/Dashboard.vue') },
];

// Async component with loading state
const HeavyChart = defineAsyncComponent({
  loader: () => import('@/components/HeavyChart.vue'),
  loadingComponent: ChartSkeleton,
  errorComponent: ErrorDisplay,
  delay: 200,
});
```

### shallowRef for large objects

```ts
// Avoid deep reactivity for large, infrequently updated structures
const tableData = shallowRef<Row[]>([]);
```

---

## Data Fetching — TanStack Query for Vue

```ts
// composables/useUser.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { fetchUser, updateUser } from '@/api/users';

export function useUser(id: Ref<string>) {
  return useQuery({
    queryKey: ['users', id],
    queryFn: () => fetchUser(id.value),
    staleTime: 1000 * 60 * 5,
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateUser,
    onSuccess: (updated) => queryClient.setQueryData(['users', updated.id], updated),
  });
}
```

### Native fetch composable — @vueuse/core useFetch

```ts
import { useFetch } from '@vueuse/core';

const { data, error, isFetching } = useFetch(`/api/users/${userId}`).json<User>();
```

---

## Forms — VeeValidate + Zod

```ts
// schemas/login.ts
import { z } from 'zod';
export const loginSchema = z.object({
  email:    z.string().min(1, 'Required').email('Invalid email'),
  password: z.string().min(8, 'At least 8 characters'),
});
```

```vue
<script setup lang="ts">
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import { loginSchema } from '@/schemas/login';

const { defineField, handleSubmit, errors, isSubmitting } = useForm({
  validationSchema: toTypedSchema(loginSchema),
});

const [email, emailAttrs]       = defineField('email');
const [password, passwordAttrs] = defineField('password');

const onSubmit = handleSubmit(async (values) => {
  await authService.login(values);
});
</script>

<template>
  <form @submit="onSubmit" novalidate>
    <label for="email">Email</label>
    <input id="email" v-model="email" v-bind="emailAttrs" type="email"
      :aria-invalid="!!errors.email" :aria-describedby="errors.email ? 'email-error' : undefined" />
    <p v-if="errors.email" id="email-error" role="alert">{{ errors.email }}</p>

    <button type="submit" :disabled="isSubmitting" :aria-busy="isSubmitting">
      {{ isSubmitting ? 'Logging in…' : 'Log in' }}
    </button>
  </form>
</template>
```

---

## State — Pinia

```ts
// stores/cart.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([]);

  const total = computed(() =>
    items.value.reduce((sum, i) => sum + i.price * i.quantity, 0)
  );

  function addItem(item: CartItem) {
    const existing = items.value.find(i => i.id === item.id);
    if (existing) existing.quantity++;
    else items.value.push({ ...item, quantity: 1 });
  }

  function removeItem(id: string) {
    items.value = items.value.filter(i => i.id !== id);
  }

  return { items, total, addItem, removeItem };
}, { persist: true }); // pinia-plugin-persistedstate
```

```vue
<script setup lang="ts">
import { useCartStore } from '@/stores/cart';
const cart = useCartStore();
</script>

<template>
  <p>Total: {{ cart.total }}</p>
  <button @click="cart.addItem(product)">Add to cart</button>
</template>
```

### URL state — Vue Router

```ts
import { useRoute, useRouter } from 'vue-router';
import { computed } from 'vue';

export function useFilters() {
  const route  = useRoute();
  const router = useRouter();

  const category = computed(() => route.query.category as string ?? 'all');
  const page     = computed(() => Number(route.query.page ?? 1));

  function setFilter(key: string, value: string) {
    router.push({ query: { ...route.query, [key]: value, page: 1 } });
  }

  return { category, page, setFilter };
}
```

---

## SEO — Vite SPA

For a Vite SPA, use **@vueuse/head** or **unhead**:

```ts
import { useHead } from '@unhead/vue';

useHead({
  title: computed(() => `${product.value?.name} — MyApp`),
  meta: [
    { name: 'description', content: computed(() => product.value?.description) },
    { property: 'og:image', content: computed(() => product.value?.imageUrl) },
  ],
});
```

For SSR/SSG, use Nuxt — see `references/frameworks/nuxt.md`.

---

## PWA — Vite PWA

```ts
// vite.config.ts
import { VitePWA } from 'vite-plugin-pwa';

VitePWA({
  registerType: 'autoUpdate',
  manifest: { name: 'MyApp', theme_color: '#6366f1' },
  workbox: { globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'] },
})
```

---

## i18n — vue-i18n

```ts
// plugins/i18n.ts
import { createI18n } from 'vue-i18n';
import en from '@/locales/en.json';
import fr from '@/locales/fr.json';

export const i18n = createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: { en, fr },
});
```

```vue
<script setup lang="ts">
import { useI18n } from 'vue-i18n';
const { t, locale } = useI18n();
</script>

<template>
  <p>{{ t('product.addToCart') }}</p>
  <p>{{ t('cart.items', { count: cartCount }) }}</p>
  <select v-model="locale">
    <option value="en">English</option>
    <option value="fr">Français</option>
  </select>
</template>
```
