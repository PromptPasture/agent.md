---
status: "[DRAFT | FINAL | READY_FOR_DEV]"
documentType: DESIGN
phase: "[discovery | delivery | maintenance]"
version: "[1.0]"
createdAt: "[YYYY-MM-DD]"
updatedAt: "[YYYY-MM-DD]"
author: "[designer or team]"
tags:
  - "[design]"
  - "[ui]"
related:
  - "[PRD.md, SPEC.md, Figma URL, or related doc]"
---

# Design Specification: [Component / Feature Name]

## 1. Overview & Purpose

**Explain the UI element's role and usage context.**

[Brief description of what this UI element does and when it should be used.]

---

## 2. Visual Attributes & Tokens

**Map visible styling decisions to implementation-ready tokens.**

| Element | Property | Token / Value | Notes |
| ---------- | ---------- | ------------------------------- | ------------- |
| Background | Color | `var(--color-surface-elevated)` | |
| Border | Radius | `var(--radius-md)` (8px) | |
| Container | Padding | `var(--space-4)` (16px) | |
| Shadow | Box Shadow | `var(--shadow-sm)` | Only on hover |

---

## 3. States

**Document every user-visible component state and its behavior.**

- **Default:** [Description of the standard state]
- **Hover:** [e.g., "Cursor → pointer. Background → `--color-surface-hover`. Shadow → `--shadow-md`."]
- **Active / Pressed:** [e.g., "Scale: 0.98. Shadow → `--shadow-sm`."]
- **Focus:** [e.g., "2px solid `--color-focus-ring` with 2px offset."]
- **Disabled:** [e.g., "Opacity: 50%. Cursor → `not-allowed`. Hover effects disabled."]
- **Loading:** [e.g., "Text hidden; spinner centered. Component maintains resting dimensions."]
- **Error:** [e.g., "Border → `--color-error`. Error icon appears on right."]

---

## 4. Interaction & Motion

**Specify triggers, responses, and motion details that affect implementation.**

**Trigger:** [e.g., "Clicking 'Submit'"]
**Action:** [e.g., "Transitions to Loading state immediately."]
**Animation:**

- **Property:** [e.g., `background-color`, `transform`]
- **Duration:** [e.g., 200ms]
- **Easing:** [e.g., `ease-in-out`]

---

## 5. Responsive Behavior

**Define how the UI adapts across supported viewport ranges.**

| Breakpoint | Behavior |
| ----------------------- | ------------------------------------------- |
| **Mobile** (< 768px) | Elements stack. Width: 100%. Padding: 12px. |
| **Tablet** (768–1024px) | Side-by-side. Width: 50%. |
| **Desktop** (> 1024px) | Max width: 400px. |

---

## 6. Edge Cases & Content Scaling

**Capture content and data variations that can break layout or usability.**

- **Long text:** [e.g., "Truncate with ellipsis on a single line."]
- **Missing data:** [e.g., "Avatar fails → colored circle with initials."]
- **Localization:** [e.g., "Don't set fixed widths — German strings can be 50% longer."]
