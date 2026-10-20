# Accessibility (a11y)

> **Last updated**: 2026-10-20

Exact classes and the theme-toggle behaviour are in `resources/design-spec.md` (§3, §9, §10). These are the general rules:

- Use `aria-label` on interactive elements that have no visible text.
- Every `<img>` has descriptive `alt` text; use `alt=""` for decorative images.
- Decorative SVGs, icons and emoji get `aria-hidden="true"`.
- Keep the natural focus order; use `tabindex` only when necessary.
- Every interactive element has a visible focus indicator. Never use `outline-none` on its own.
- Respect reduced motion: `motion-reduce:transition-none` on anything that animates.
- Text meets WCAG AA contrast (4.5:1) in both themes.
