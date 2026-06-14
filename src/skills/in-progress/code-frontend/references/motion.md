# Animation and Motion

Animation enhances clarity and feedback. It must never block interaction, distract, or cause discomfort. Always respect the user's motion preference.

---

## Reduced Motion — Non-Negotiable

Every animation must degrade gracefully when `prefers-reduced-motion: reduce` is set.

```css
/* CSS — always pair animation with a reduced-motion override */
.card {
  transition: transform 0.2s ease, opacity 0.2s ease;
}

@media (prefers-reduced-motion: reduce) {
  .card {
    transition: none;
  }
}
```

```ts
// React — read the preference in JS when controlling animation programmatically
const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
```

In Framer Motion, use the built-in hook:

```tsx
import { useReducedMotion } from 'framer-motion';

function AnimatedCard() {
  const reduced = useReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0, y: reduced ? 0 : 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: reduced ? 0 : 0.2 }}
    />
  );
}
```

---

## Choosing an Approach

| Use case | Preferred tool |
| --- | --- |
| Simple show/hide, hover, focus | CSS `transition` |
| Keyframe sequences | CSS `@keyframes` |
| Complex orchestration, gestures, shared layouts | Framer Motion |
| Page / route transitions | Framer Motion or View Transitions API |
| SVG animation | CSS or Framer Motion |
| Spring physics | Framer Motion |

Default to CSS. Reach for Framer Motion only when CSS cannot express the animation cleanly.

---

## CSS Transitions

```css
/* Prefer transform and opacity — these are compositor-only and do not trigger layout */
.button {
  transform: scale(1);
  opacity: 1;
  transition: transform 0.15s ease, opacity 0.15s ease;
}

.button:hover {
  transform: scale(1.03);
}

.button:active {
  transform: scale(0.97);
}

/* Avoid animating layout properties — they trigger reflow */
/* Bad: width, height, top, left, margin, padding */
```

### Timing guidelines

| Interaction | Duration |
| --- | --- |
| Micro (button press, toggle) | 100–150ms |
| Element enter / exit | 150–250ms |
| Page transition | 250–400ms |
| Complex orchestration | 300–500ms |

---

## Framer Motion

### Fade and slide in

```tsx
import { motion } from 'framer-motion';

const fadeSlide = {
  hidden: { opacity: 0, y: 12 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.2, ease: 'easeOut' } },
  exit:   { opacity: 0, y: -8, transition: { duration: 0.15 } },
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
const list = {
  visible: { transition: { staggerChildren: 0.05 } },
};

const item = {
  hidden:  { opacity: 0, y: 8 },
  visible: { opacity: 1, y: 0 },
};

export function AnimatedList({ items }: { items: string[] }) {
  return (
    <motion.ul variants={list} initial="hidden" animate="visible">
      {items.map((text, i) => (
        <motion.li key={i} variants={item}>
          {text}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

### Layout animation (shared element)

```tsx
// Framer Motion tracks the element by layoutId and animates between positions
<motion.div layoutId={`card-${id}`} />
```

Wrap the tree in `<AnimatePresence>` when elements enter or exit the DOM:

```tsx
import { AnimatePresence } from 'framer-motion';

<AnimatePresence mode="wait">
  {isOpen && <Modal key="modal" />}
</AnimatePresence>
```

---

## View Transitions API

Native browser API for page and component transitions. No library needed.

```ts
// Wrap the state change that triggers a DOM update
document.startViewTransition(() => {
  flushSync(() => setPage(nextPage));
});
```

```css
/* Customise the transition */
::view-transition-old(root) {
  animation: fade-out 0.2s ease;
}
::view-transition-new(root) {
  animation: fade-in 0.2s ease;
}

@keyframes fade-out { to { opacity: 0; } }
@keyframes fade-in  { from { opacity: 0; } }

@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root),
  ::view-transition-new(root) {
    animation: none;
  }
}
```

Check support before use — degrade silently:

```ts
if ('startViewTransition' in document) {
  document.startViewTransition(() => update());
} else {
  update();
}
```

---

## What Not to Animate

- **Layout properties** (`width`, `height`, `top`, `left`, `margin`) — trigger reflow, use `transform` instead
- **Infinite loops without purpose** — spinning loaders are acceptable; decorative infinite motion is not
- **Fast sequences on important content** — flashing or rapid motion can trigger vestibular disorders
- **Entrance animations on every element** — animate sparingly; not every component needs to slide in
