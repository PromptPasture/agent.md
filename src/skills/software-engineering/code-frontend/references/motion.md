# Animation and Motion

Animation clarifies and provides feedback. Never block interaction, distract, or cause discomfort. Always respect user motion preferences.

---

## Reduced Motion — Non-Negotiable

Every animation must degrade gracefully when `prefers-reduced-motion: reduce` is set.

```css
/* Always pair animation with a reduced-motion override */
.card {
  transition: transform 0.2s ease, opacity 0.2s ease;
}

@media (prefers-reduced-motion: reduce) {
  .card {
    transition: none;
  }
}
```

Read the preference in JavaScript when controlling animation programmatically:

```ts
const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
```

---

## Choosing an Approach

|Use case|Preferred tool|
|---|---|
|Simple show/hide, hover, focus|CSS `transition`|
|Keyframe sequences|CSS `@keyframes`|
|Complex orchestration, gestures, shared layouts|Framework animation library|
|Page / route transitions|Framework router integration or View Transitions API|
|SVG animation|CSS `@keyframes`|
|Spring physics|Framework animation library|

**Default to CSS.** Reach for a library only when CSS cannot express the animation cleanly.

---

## CSS Transitions

Prefer `transform` and `opacity` — they run on the compositor thread and do not trigger layout recalculation.

```css
.button {
  transform: scale(1);
  opacity: 1;
  transition: transform 0.15s ease, opacity 0.15s ease;
}

.button:hover  { transform: scale(1.03); }
.button:active { transform: scale(0.97); }

/* Never animate layout properties — they trigger reflow */
/* Avoid: width, height, top, left, margin, padding */
```

### Timing guidelines

|Interaction|Duration|
|---|---|
|Micro (button press, toggle)|100–150ms|
|Element enter / exit|150–250ms|
|Page transition|250–400ms|
|Complex orchestration|300–500ms|

---

## View Transitions API

Native browser API for page and component transitions. No library required.

```css
/* Customise the transition */
::view-transition-old(root) { animation: fade-out 0.2s ease; }
::view-transition-new(root) { animation: fade-in  0.2s ease; }

@keyframes fade-out { to   { opacity: 0; } }
@keyframes fade-in  { from { opacity: 0; } }

@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root),
  ::view-transition-new(root) { animation: none; }
}
```

Always check for support and degrade silently — the state update must still happen:

```ts
function transition(update: () => void) {
  if ('startViewTransition' in document) {
    document.startViewTransition(update);
  } else {
    update();
  }
}
```

---

## What Not to Animate

- **Layout properties** (`width`, `height`, `top`, `left`, `margin`) — trigger reflow; use `transform` instead
- **Infinite loops without purpose**: spinners on loading states are acceptable; decorative infinite motion is not
- **Fast sequences on important content**: flashing or rapid motion can trigger vestibular disorders
- **Entrance animations on every element**: animate sparingly; not every component needs to slide in
