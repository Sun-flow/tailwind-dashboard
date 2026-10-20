# Accessibility (a11y)

> **Last updated**: 2026-10-20

- Add `role` attributes on landmark elements where semantic HTML is ambiguous.
- Use `aria-label` on interactive elements (nav, buttons, search, icons) lacking visible text.
- Every `<img>` must have descriptive `alt` text. Use `alt=""` for decorative images.
- Ensure keyboard-navigable focus order (`tabindex` only when necessary).
- Use `aria-hidden="true"` on purely decorative SVGs/icons.

## Focus & Motion

- **Visible focus**: every interactive element gets a visible focus indicator — Tailwind `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-400` (or a high-contrast equivalent). Never rely on `outline:none` alone.
- **Reduced motion**: respect `prefers-reduced-motion` for micro-interactions (transitions, animations, hover states). Tailwind's `motion-reduce:` variant covers this (e.g., `motion-reduce:transition-none`). No animation may be un-disableable.

## Accessible theme toggle (when implemented)

- A `<button>` carrying the sun/moon icon with a **visible text label** (e.g., "Toggle theme") — don't rely on the icon alone.
- Use `aria-pressed="true"/"false"` to expose the current state, and reflect it in the icon and label.
- Persist choice to `localStorage` but respect OS preference on first load (`prefers-color-scheme`) when no stored choice exists — so the page never fights the user's default.
- Keyboard accessible by default (native button), in the tab order, and includable in the sticky header next to the nav.
