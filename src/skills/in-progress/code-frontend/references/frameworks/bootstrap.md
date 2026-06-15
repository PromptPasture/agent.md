# Bootstrap

---

## Setup

```bash
npm install bootstrap
```

### React / Next.js — import in entry point

```ts
// src/main.tsx or app/layout.tsx
import 'bootstrap/dist/css/bootstrap.min.css';
```

### SvelteKit — import in global stylesheet

```css
/* src/app.css */
@import 'bootstrap/dist/css/bootstrap.min.css';
```

### Sass customisation — always override variables before importing

```scss
/* src/styles/bootstrap-custom.scss */
$primary:       #6366f1;
$font-size-base: 1rem;
$border-radius:  0.5rem;
$border-radius-lg: 0.75rem;

@import 'bootstrap/scss/bootstrap';
```

Import the custom file instead of the default CSS:

```ts
import './styles/bootstrap-custom.scss';
```

---

## Component Patterns

Use Bootstrap class names directly on HTML elements:

```html
<div class="card shadow-sm">
  <div class="card-body">
    <h5 class="card-title">Title</h5>
    <p class="card-text">Description text.</p>
    <button class="btn btn-primary">Action</button>
  </div>
</div>

<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container">
    <a class="navbar-brand" href="/">MyApp</a>
  </div>
</nav>

<div class="alert alert-danger" role="alert">
  Something went wrong.
</div>
```

---

## Never Use Bootstrap JavaScript in Reactive Frameworks

Bootstrap's JS plugins (Collapse, Dropdown, Modal, Tooltip) manipulate the DOM directly — this conflicts with React's and Svelte's virtual DOM and reactivity. Use framework state instead.

### Collapse

```html
<!-- Bad — Bootstrap JS -->
<button data-bs-toggle="collapse" data-bs-target="#menu">Toggle</button>
<div id="menu" class="collapse">Content</div>
```

**React:**

```tsx
const [isOpen, setIsOpen] = useState(false);
<button onClick={() => setIsOpen(p => !p)}>Toggle</button>
<div className={clsx('collapse', isOpen && 'show')}>Content</div>
```

**Svelte:**

```svelte
<script lang="ts">
  let isOpen = $state(false);
</script>
<button onclick={() => isOpen = !isOpen}>Toggle</button>
<div class="collapse" class:show={isOpen}>Content</div>
```

### Modal

Use a React or Svelte modal component rather than Bootstrap's JS Modal. Bootstrap CSS classes for modal structure are fine — only the JS plugin is problematic.

---

## Grid

```html
<div class="container">
  <div class="row g-4">
    <div class="col-12 col-md-6 col-lg-4">Card 1</div>
    <div class="col-12 col-md-6 col-lg-4">Card 2</div>
    <div class="col-12 col-md-6 col-lg-4">Card 3</div>
  </div>
</div>
```

---

## Utilities

Bootstrap ships a utility layer similar to Tailwind. Prefer Bootstrap utilities over writing custom CSS when already using Bootstrap:

```html
<!-- Spacing -->
<div class="mt-4 mb-2 px-3">

<!-- Display -->
<div class="d-flex align-items-center gap-2">

<!-- Text -->
<p class="text-muted fw-semibold text-truncate">

<!-- Colours -->
<span class="text-danger bg-light rounded p-1">
```
