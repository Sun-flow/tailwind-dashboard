# Layout & CSS

> **Last updated**: 2026-10-19

## Tailwind CSS

- Use **Tailwind CSS v4 CDN** via a single external stylesheet — `<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>` in `<head>`.
- No inline `<style>` blocks; apply all styling through Tailwind utility classes in HTML markup.
- **Never** mix in other CSS frameworks. Chart CSS (https://chartscss.org/) is the **only** allowed CSS visualization library — and only for KPI charts and driver visualizations where a semantic chart structure adds clarity.
- **Never** use `float` or `display: inline-block` for page structure. Use Flexbox (`flex`) for layout and component alignment.
- Extend with CSS custom properties (`--var`) in the Tailwind config or a minimal global CSS block for consistent spacing, colors, and breakpoints — only where Tailwind utilities are insufficient.

## Mobile-First Design

This is a **mobile-first** dashboard. All layout work starts from the smallest screen and expands outward.

### Rules

1. **Start from the smallest screen.** Design the single-column layout first. Everything must be readable and usable on a 375px-wide viewport before adding wider breakpoints.
2. **Adapt with Tailwind breakpoints only.** Use the built-in responsive prefixes in this order:
   - No prefix = mobile base (default, < 640px)
   - `sm:` = tablet portrait (640px–768px)
   - `md:` = tablet landscape / small desktop (768px–1024px)
   - `lg:` = desktop (1024px+)
3. **Same components, all screens.** A KPI card, a table, a chart container must work on mobile, tablet, and desktop without structural changes — only grid column count and spacing adapt.
4. **Avoid pixel-based sizes.** Never use `w-[...]` or `h-[...]` fixed-size utilities. Use relative units: `w-full`, `w-1/2`, `max-w-screen-xl`, `min-h-screen`, Tailwind spacing (`p-4`, `gap-4`, `space-y-4`).
5. **Use Tailwind spacing utilities.** Gutter between blocks: `space-y-6` or `space-y-8`. Padding: `p-4` mobile, `lg:p-6` desktop. Gap in grids: `gap-4` or `gap-6`.
6. **Touch targets.** All interactive elements (buttons, links, sortable headers) must be at least 44×44px — use `min-h-[44px]` or ensure padding/clip yields that size.
