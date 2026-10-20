# Components & Structure

> **Last updated**: 2026-10-20

## Reusable Component Patterns

Build the dashboard using a consistent set of reusable components. Every use of the same pattern must share the same structure, spacing, and styling classes. **All card examples are light-first with `dark:` variants** (theme rule — see `layout.md`).

### KPI Card
```
┌──────────────────┐
│  📈 Metric Label  │
│   $12,450         │  ← large, bold value
│   ▲ +5.2% period │  ← trend indicator
└──────────────────┘
```
- Tailwind: `bg-white dark:bg-slate-800 rounded-xl shadow-sm p-6`
- Always: label, value, optional trend arrow/badge

### Section Block
```
┌──────────────────────────────────┐
│  Section Title            [↗️]   │  ← optional action link
├──────────────────────────────────┤
│  content (cards, chart, table)   │
└──────────────────────────────────┘
```
- Tailwind: `bg-white dark:bg-slate-800 rounded-xl shadow-sm p-6`
- Consistent heading hierarchy (`<h2>` in section, `<h3>` in cards)

### Data Table
- `<table>` with `<thead>` / `<tbody>`
- Tailwind: `divide-y divide-gray-200 dark:divide-slate-700`, header row `bg-gray-50 dark:bg-slate-700/50`
- Responsive: horizontal scroll on mobile (`overflow-x-auto`)

### Alert / Badge
- Use Tailwind color utilities: `bg-green-100 text-green-800` for positive, `bg-red-100 text-red-800` for negative. Add `dark:` counterparts so badges read correctly in dark mode.
- Keep sizes consistent (e.g., `px-2 py-1 text-xs rounded-full`)

---

## Section-Based Dashboard Structure

The dashboard is organized into three broad blocks (single page — no hamburger/sidebar/overlay navigation):

1. **Top block: Outcome KPIs** — row of KPI cards
2. **Middle block: Drivers** — charts and breakdowns explaining the outcomes
3. **Bottom block: Operational details** — tables, alerts, filtered lists

Each block is a `<section id="…">` with a consistent `<h2>` heading and internal padding.

### Sticky inline anchor navigation (Approach B)

- A sticky `<header>` holds a `<nav>` with anchor links to the three sections. **No overlay menus** — the "no navigation" rule means no hamburger/sidebars, not a veto on in-page anchors.
- Give each anchored section `scroll-mt-*` (`scroll-mt-20` ≈ sticky-header height) so headings don't hide under the sticky header.
- The nav link for the section in view should reflect state (e.g., `aria-current="true"`).

---

## Motion & Interaction State

- **Focus-visible rings**: interactive elements use a visible `focus-visible:` ring (e.g. `focus-visible:outline-2 outline-offset-2`), never `outline-none` alone.
- **Reduced motion**: respect `prefers-reduced-motion` — Tailwind v4 supports `motion-reduce:` (e.g., `motion-reduce:transition-none`). No animation that can't be disabled.
- Keep transitions short (`duration-200`) and subtle. Hover/static state changes are fine; flashy is not.

---

## Chart CSS for Visualizations

For KPI charts and driver visualizations, use **Chart CSS** (https://chartscss.org/):

- Add the Chart CSS stylesheet: `<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/chartscss/chart.css@v1/dist/chart.css">`
- Use Chart CSS column, bar, and line classes for data visualization
- Keep data simple — focus on clear hierarchy and readability over complex chart types
- **Responsive**: wrap each chart in a container; charts should not overflow the 375px viewport — prefer `overflow-x-auto` on the wrapper rather than letting the chart squish or clip. On wide screens a chart can span the full driver-section width.
- **Aspect**: use Chart CSS's `--color`/data attributes for series; don't hand-tune pixel heights — let the container define the footprint (`w-full h-64 md:h-80`).
- Wrap each chart in a consistent container: same `bg-white rounded-xl shadow-sm p-4 lg:p-6` as other components
- All chart containers should have a consistent aspect ratio (e.g., `aspect-[4/3]` or `aspect-[16/9]` on desktop)
- Do not mix in any other charting or CSS framework

## Consistent Pattern Rules

- All KPI cards share identical structure and Tailwind class sets
- All section blocks share the same container classes
- All data tables share the same header/row/cell styling
- All badges use the same size and shape
- All chart containers have consistent sizing and aspect ratio
- Do not deviate from the established pattern without updating this file