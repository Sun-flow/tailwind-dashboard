# Dashboard Design Plan

> **Date**: 2026-10-19  
> **Status**: Design development — creative direction established; implementation proposals to be filled in future steps

---

## Client Needs & Goals

From `resources/profile.md` — a **multi-platform influencer** promotes 3 products across 5 platforms (Instagram, YouTube, TikTok, Twitter/X, Twitch) and needs a **single reporting dashboard** to consolidate scattered data.

### Core Questions the Dashboard Must Answer

| # | Question | How We Measure It |
|---|---|---|
| 1 | 💰 **How much commission am I earning?** | Total commissions = units sold × price × 15%, broken out by product and platform |
| 2 | 📦 **Which products generate the most revenue?** | Product-level revenue ranking (units sold × price) |
| 3 | 📈 **How well are my ads converting?** | Conversion rate = conversions ÷ reach, per platform and per product |
| 4 | 🏆 **Which platforms generate the best return?** | ROI = (revenue − costs) per platform; which platform earns the most per dollar spent |
| 5 | ❤️ **What is the engagement rate by platform/product?** | (likes + comments + shares) ÷ impressions, split by platform and product post |

### Underlying Needs

- **Time savings**: stop jumping between 5 different analytics dashboards, spreadsheets, and manual notes
- **Data-driven decisions**: know where to focus content creation and ad spend
- **Clear priorities**: see at a glance what's working and what's not
- **Accountability**: track performance of promoted products against commission goals

---

## Functionality Expectations

| Feature | Priority | Description |
|---|---|---|
| **Single-page dashboard** | 🔴 Must-have | All key info at a glance, one scrolling page, no pagination |
| **Sticky navigation header** | 🔴 Must-have | Inline anchor links to jump between the three dashboard blocks; no hamburger/sidebar |
| **Responsive layout** | 🔴 Must-have | Works on mobile (portrait), tablet, and desktop without horizontal scroll |
| **KPI summary cards** | 🔴 Must-have | Top row showing total commissions, top product, top platform, overall engagement rate |
| **Driver charts/breakdowns** | 🟠 Should-have | Platform performance bars, product comparison, conversion funnels |
| **Operational data tables** | 🟠 Should-have | Products table, platforms table, campaigns table — sortable columns |
| **Alert indicators** | 🟡 Nice-to-have | Visual flags for anomalies (sharp conversion drops, unexpected spikes) |
| **Filtered "top" lists** | 🟡 Nice-to-have | "Top products", "top platforms", "improvement opportunities" |
| **Static mock data** | 🔴 Must-have | Embedded JSON or JS data to drive all visuals initially |
| **API-ready architecture** | 🟢 Future | Data layer isolated so real API integration can replace mocks later |

---

## ❓ Proposed Implementation Methods

> **Reserved for future research.** This section will be filled after reviewing implementation options — Chart.js vs Chart CSS, data architecture (JSON vs JS module), layout grid strategy, and color scheme decisions.  
> *The guidelines recommend Chart CSS (https://chartscss.org/) for KPIs and drivers to keep the stack lightweight — this will be evaluated against other options.*

### Layout Approach

*— to be decided —*

### Charting Approach

*— to be decided —*

### Data Architecture

*— to be decided —*

### Color Palette & Theme

*— to be decided —*

---

## 🎨 Creative Design Choices

> **Brainstorming notes.** Layout patterns, color schemes, element organization, typography, and visual hierarchy.

### Three-Block Dashboard Structure (from guidelines)

```
┌─────────────────────────────────────────────┐
│  🔝 TOP BLOCK: Outcome KPIs                 │
│  [KPI Card] [KPI Card] [KPI Card] [KPI Card]│
│  Volume │ Revenue │ Engagement │ Performance │
├─────────────────────────────────────────────┤
│  📊 MIDDLE BLOCK: Drivers                   │
│  ┌─ Platform Performance ─┐ ┌─ Product ─┐   │
│  │  Bar charts by platform │ │  Comparison│  │
│  └─────────────────────────┘ └───────────┘   │
│  ┌─ Conversion Funnel ─────┐ ┌─ Activity ─┐  │
│  │  Stage-by-stage dropoff │ │  Posts/pub │  │
│  └─────────────────────────┘ └───────────┘   │
├─────────────────────────────────────────────┤
│  📋 BOTTOM BLOCK: Operational Details        │
│  ┌─ Products Table ─┐ ┌─ Platforms Table ─┐  │
│  └──────────────────┘ └───────────────────┘   │
│  ┌─ Alerts ──────────────┐ ┌─ Top Lists ─┐   │
│  └───────────────────────┘ └─────────────┘   │
└─────────────────────────────────────────────┘
```

### Grid Layout Strategy Brainstorm

**Desktop layout (>1024px, `lg:` breakpoint):**
- Top block: 4-column grid of KPI cards in a single row
- Middle block: 2-column grid — left (platform bars) | right (product comparison); second row: 2-column — left (funnel) | right (activity)
- Bottom block: 2-column grid — left (tables stack) | right (alerts + lists stack)

**Tablet layout (768-1024px, `md:` breakpoint):**
- Top block: 2×2 grid of KPI cards
- Middle block: Single column, cards stack vertically
- Bottom block: Single column, sections stack vertically

**Mobile layout (<768px, `sm:` breakpoint):**
- Top block: 1-column stack of KPI cards (scrollable)
- Middle block: Single column
- Bottom block: Single column with horizontal-scroll tables

### Color Palette Brainstorm

**Theme direction: "Professional dark" (dashboard-appropriate)**
- Background: `slate-900` or `gray-900` dark mode with a `gray-50` / `white` light mode option
- Cards: `white` / `gray-50` with `shadow-sm` / `shadow-md` depth
- Accent colors for KPI categories:
  - Volume / Scale → `blue-500` / `blue-600`
  - Revenue / Money → `green-500` / `emerald-500`
  - Engagement → `purple-500` / `violet-500`
  - Retention → `teal-500`
  - Performance → `indigo-500`
  - Satisfaction → `amber-500`
  - Efficiency → `cyan-500`
- Trend indicators: `green-500` ▲ for positive, `red-500` ▼ for negative
- Data visualization bars: use the accent color of the metric being shown
- Text hierarchy: `gray-900` headings, `gray-600` body, `gray-400` secondary labels

**Alternative: "Clean white" (light mode)**
- Background: `gray-50`
- Cards: `white` with `border border-gray-200`
- Same accent color scheme, with darker text

### Typography Approach
- Tailwind default font stack (system sans-serif) — no custom fonts to keep it lightweight
- Heading hierarchy:
  - Page title: `text-2xl` or `text-3xl font-bold`
  - Section headings: `text-xl font-semibold`
  - Card titles: `text-sm font-semibold uppercase tracking-wide text-gray-500`
  - KPI values: `text-3xl font-bold` or `text-4xl font-bold`
  - Table headers: `text-xs font-medium uppercase tracking-wide`
  - Body/table cells: `text-sm`

### Card Design Pattern (consistent across all blocks)
```
┌──────────────────────────────┐
│  LABEL (text-xs uppercase)   │
│  VALUE (text-3xl bold)       │  ← KPI cards
│  ▲ TREND (text-xs)           │
├──────────────────────────────┤
│  or                          │
├──────────────────────────────┤
│  SECTION TITLE        [↗️]   │  ← Driver/table blocks
│  ┌─ content ─┐               │
│  └───────────┘               │
└──────────────────────────────┘
```
- `bg-white rounded-xl shadow-sm p-4 lg:p-6` — consistent container
- Inner padding adapts: `p-4` on mobile, `lg:p-6` on desktop

### Data Visualization Approach (placeholder)
- Bar charts: Chart CSS column/bar classes or Tailwind-driven `div` bars
- Progress/comparison: inline bar fills using Tailwin d widths
- Funnel: stepped horizontal bars decreasing in width
- Keep chart containers at consistent aspect ratio (e.g., `aspect-[4/3]`)

### Element Organization Principles
- **Left-to-right priority**: most important metric in top-left KPI card
- **Vertical rhythm**: consistent gutter between blocks (`space-y-6` or `space-y-8`)
- **Scroll behavior**: only the page scrolls; no individual component scrolls (except maybe tables with `overflow-x-auto`)
- **Touch targets**: all interactive elements minimum 44×44px (Tailwind `min-h-[44px]` if needed)

### Navigation & Header Strategy

> **Goal**: Provide a fixed or sticky header/navbar that lets the user jump directly to any of the three dashboard blocks (KPIs, Drivers, Operational Details), plus a quick "scroll to top" affordance.

#### Why Add Navigation?

The original brief called for a "single-page dashboard — all key info at a glance, no navigation required." However, as the dashboard grows in data, scrolling from the top KPI cards all the way down to the alerts table becomes friction. Navigation serves two purposes:

| Purpose | Benefit |
|---|---|
| **🧭 Orientation** | The user always knows which block they're viewing — the active section is highlighted in the nav |
| **⏩ Quick jumps** | Power users skip straight to the table or chart they need without manual scrolling |

A navigation header also **anchors the brand**: a place for the dashboard title, a subtle platform-selector (future), and visual consistency across views.

#### Approach A: Hamburger Menu → Sidebar

```
┌───┬───────────────────────────┐
│ ☰ │  Influencer Dashboard     │  ← sticky top bar
├───┴───────────────────────────┤
│                               │
│  ┌───────────────────────┐    │
│  │ ✕ KPI Outcomes        │    │  ← sidebar overlay / push
│  │   Drivers             │    │
│  │   Operational Details │    │
│  │   ─────────────       │    │
│  │   ↑ Back to Top       │    │
│  └───────────────────────┘    │
│                               │
│  (page content)               │
└───────────────────────────────┘
```

| 👍 Pros | 👎 Cons |
|---|---|
| Maximizes content area — no horizontal nav stealing space | Adds a tap/clicks step to reach any section |
| Familiar pattern (mobile users know the hamburger) | The sidebar overlay hides the page, making orientation *harder* — you lose sight of where you are |
| Sidebar can hold future items (settings, platform switcher, date range) without cluttering the header | On mobile, the animation/overlay adds complexity and potential performance cost |
| Clean, minimal header | Sidebar content is hidden by default — the user must discover it; contradicts "zero-training" goal |
| Fits the "professional dashboard" visual language | Inconsistent with the single-page scroll rhythm — nav competes with the scroll-to-section flow |

**Verdict**: A hamburger sidebar works well for **settings-heavy dashboards** with many navigation destinations. For a three-section single-page dashboard, it adds unnecessary indirection.

#### Approach B: Landing Header with Inline Section Links

```
┌──────────────────────────────────────────┐
│  📊 Influencer Dashboard                 │  ← sticky top bar
│  [KPIs] · [Drivers] · [Details]  [↑Top] │  ← inline horizontal nav
├──────────────────────────────────────────┤
│                                          │
│  🔝 KPI Outcomes    ← highlighted active │
│  ...                                     │
│  📊 Drivers          ← smooth scroll     │
│  ...                                     │
│  📋 Operational Details                  │
│  ...                                     │
└──────────────────────────────────────────┘
```

| 👍 Pros | 👎 Cons |
|---|---|
| **Zero clicks** to navigate — all destinations visible at all times | Takes permanent horizontal space in the header; on very narrow phones (375px) the links may need to wrap or condense to icons |
| Direct visual **orientation**: the active link is highlighted, so the user knows exactly which block they're viewing | With more than ~5 items the bar becomes crowded; we have exactly 3 sections which is ideal |
| **Smooth scroll anchors** (`<a href="#kpi-block">`) require zero JavaScript — works with pure HTML | Harder to extend with many future nav items without redesign |
| **Consistent** with the single-page scroll paradigm — nav reinforces the three-block structure | — |
| **Faster** — no overlay, no animation, no click to reveal | — |
| Aligns with "zero-training" goal: the links *are* the three dashboard blocks; the user learns the structure just by looking at the nav | — |

**Verdict**: For this dashboard's scope (3 sections, single page, content-forward), inline section links are the **clear winner**. They make the three-block structure visible at all times, require zero interaction to use, and reinforce the dashboard's mental model on every scroll.

#### Recommendation

**Use Approach B: a sticky header with inline anchor links** for the three dashboard blocks.

| Decision | Rationale |
|---|---|
| **Sticky top bar** | `sticky top-0 z-50` — always accessible, never lost during scroll |
| **Text links, not icons** | Clear labels ("KPIs", "Drivers", "Details") over ambiguous icons; icons may be added *alongside* text on desktop |
| **Current-section highlighting** | JavaScript `scrollSpy` (or simple `section:target` CSS) marks the active nav item — gives orientation |
| **Smooth-scroll behavior** | CSS `scroll-behavior: smooth` on `<html>` — no JS needed for the scroll animation itself |
| **"Back to top" link** | A small link in the nav or a floating button after scrolling past the first viewport |
| **Mobile adaptation** | On `sm:` screens, nav links can shrink to abbreviated labels or single-word pills if the title truncates; worst case, wrap to two rows in the sticky bar |
| **No hamburger** | Avoid the sidebar pattern for this project — it's an unnecessary layer of indirection for a three-section page |

This decision may be revisited if a future iteration adds many more sections (e.g., per-platform dashboards, campaign manager, settings). In that case, a hamburger sidebar becomes justified — but we cross that bridge when we come to it.

---

## 🧭 Design Goals & Overarching Theme

> **Design language, mood, and user experience philosophy.**

### Core Design Principles

| Principle | What It Means in Practice |
|---|---|
| **🔢 Clarity first** | Numbers are the star. Plenty of whitespace, generous padding, muted backgrounds. The data should be readable from 3 feet away. |
| **📐 Progressive disclosure** | Top block = summary (what should I know?). Middle block = drivers (why is it happening?). Bottom block = details (what can I act on?). Each layer reveals more. |
| **🎵 Consistent rhythm** | Every card, every section follows the same structural pattern. Once you learn one, you've learned all of them. Predictable = fast to scan. |
| **🧭 Visible navigation** | A sticky header with inline section links keeps the three-block structure always in view. Users jump directly to KPIs, Drivers, or Details with one tap. No hamburger/sidebar — avoid indirection for a three-section page. |
| **📱 Mobile-first, not mobile-last** | Start with a single-column layout for the smallest screen, then expand using Tailwind `sm:`, `md:`, `lg:` breakpoints. Never use fixed pixel widths. |
| **🎨 Data-driven color** | Color is functional first — it groups related metrics and signals direction (green=good, red=attention). Decorative color is secondary. |
| **⚡ Performance-aware** | No heavy libraries. No custom CSS where Tailwind utilities suffice. Chart CSS or lightweight CSS-only charting. Fast load on any connection. |

### Visual Mood & Personality
- **Tone**: Professional, trustworthy, data-forward
- **Vibe**: Clean like a Bloomberg terminal, approachable like a modern SaaS dashboard
- **Inspiration references**:
  - Linear.app — minimal, airy, generous whitespace
  - Stripe dashboard — clean data tables, subtle color coding
  - GitHub Insights — clear time-series, trend sparklines
- **What we avoid**: Dense "wall of widgets" dashboards, 3D charts, heavy gradients, busy backgrounds

### User Experience Goals
1. **10-second orientation**: A glance tells the influencer their total commissions, top product, best platform, and overall trend — without reading a word.
2. **Zero-training required**: The layout is so intuitive they don't need onboarding. The three-block structure mirrors how they think: outcomes → what drives them → what to do next.
3. **Confidence through clarity**: Clean numbers, clear labels, and consistent formatting build trust. The influencer can share this dashboard with a manager or sponsor without embarrassment.
4. **Actionable alerts**: Anomalies aren't just shown — they're flagged in context. A sudden spike in conversions appears next to the relevant platform/product, not in a separate "alerts" section alone.
5. **Delight in the details**: Micro-interactions (hover states on cards, subtle transitions on sort) make the dashboard feel polished without adding complexity.

### Constraints That Shape Design
| Constraint | Design Response |
|---|---|
| Tailwind CSS v4 only (no custom CSS except Chart CSS) | Use Tailwind utility classes exclusively; no `style.css` file; keep Chart CSS as the only allowed exception |
| No JavaScript charting library | Chart CSS or pure-HTML/CSS bars/fills for all visualization |
| Static mock data (no API) | Design the data layer as a clean JS object so swapping in real API data later touches one file |
| Single scrolling page with sticky nav | Three logical blocks in vertical scroll; sticky header with inline anchor links for jumping; scrollSpy for active-section highlighting |
| Must work without JS (progressive) | KPIs, tables, and anchor-link nav render with HTML/CSS alone; smooth-scroll JS is enhancement, not requirement |
| Sticky header must not overlap content | Use `scroll-mt-16` (or appropriate offset) on section anchors so the fixed header doesn't hide the section title when jumping via hash links |

### Visual Hierarchy Map

```
                    VISUAL WEIGHT
                        ↓
    ┌────────────────────────────────────┐
    │  � Sticky Nav Bar                 │  ← ALWAYS VISIBLE
    │  [KPIs] [Drivers] [Details] [↑Top] │     thin, unobtrusive
    ├────────────────────────────────────┤
    │  �🔝 KPI Cards (largest type,       │  ← HIGHEST
    │     color accent, trend arrows)     │     VISUAL
    ├────────────────────────────────────┤     WEIGHT
    │  📊 Driver Charts (bars + labels)   │
    │     balanced visual weight          │
    ├────────────────────────────────────┤
    │  📋 Data Tables (smaller type,      │  ← LOWER
    │     monochrome, horizontal scroll)  │     WEIGHT
    ├────────────────────────────────────┤
    │  ⚠️ Alerts (color-tagged, compact)  │  ← CONTEXTUAL
    └────────────────────────────────────┘
```

---

## 📋 Appendix: Rules Coverage Checklist

> Rules from `generate-dashboad-guidelines.md` mapped to `.agents/rules/`

| Guideline Rule | Covered In | Notes |
|---|---|---|
| Build reusable components (cards, widgets, boxes, tables) | `components.md` | Sections & component patterns defined |
| Design mobile-first (breakpoints, no pixels) | → needs `layout.md` update or new `mobile-first.md` | Tailwind breakpoint strategy not yet codified |
| Use semantic HTML | `semantic-html.md` | Complete |
| Tailwind CSS v4 only, no other frameworks | `layout.md` | Mentions v4 CDN |
| Chart CSS allowed for KPIs/drivers | → needs addition | Not yet mentioned in rules |
| Consistent patterns for similar elements | `components.md` | Complete |

### Rules That Still Need Coverage (from `generate-dashboad-guidelines.md`)

~~**Mobile-first rule** — ✅ NOW COVERED in `.agents/rules/layout.md` (added 2026-10-19):~~
- ~~Start from the smallest screen~~
- ~~Adapt with Tailwind breakpoints (`sm:`, `md:`, `lg:`)~~
- ~~Ensure same components work on tablet and desktop~~
- ~~Avoid pixel-based sizes~~
- ~~Use Tailwind spacing and sizing utilities~~

~~**Chart CSS rule** — ✅ NOW COVERED in `.agents/rules/components.md` (added 2026-10-19):~~
- ~~Chart CSS (https://chartscss.org/) is the approved visualization library~~
- ~~Data can be simple; focus on clear hierarchy and readability~~
- ~~Do not mix in other CSS frameworks or custom CSS except Chart CSS~~