# Accessibility (a11y)

- Add `role` attributes on landmark elements where semantic HTML is ambiguous.
- Use `aria-label` on interactive elements (nav, buttons, search, icons) lacking visible text.
- Every `<img>` must have descriptive `alt` text. Use `alt=""` for decorative images.
- Ensure keyboard-navigable focus order (`tabindex` only when necessary).
- Use `aria-hidden="true"` on purely decorative SVGs/icons.
