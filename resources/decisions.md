# Architecture Decision Context (ADC) Log

> **Date created**: 2026-10-20
> **Purpose**: Record decisions that have lasting consequences — tech choice, data shape, nav, theme, verification approach. Maintained per the "Architecture Decision Context (ADC) — Log Format" section in `AGENTS.md`.
> **Rule**: one entry per decision; keep it short; update `Status` when superseded; never delete an entry.

---

### [2026-10-20] Dark theme default with light-mode toggle
- **Decision**: Dashboard ships **dark-first** (`slate-900` bg) as the default; a light-mode toggle is allowed (sun/moon button in sticky header, OS-aware via Tailwind v4 `dark:` variant, persisted to `localStorage`).
- **Rationale**: `resources/dashboard-design.md` brainstormed both directions; "professional dark" was the creative direction, and Tailwind v4's `dark:` variant makes both states cheap. Light-first markup with `dark:` utilities means the toggle is a single class flip on `<html>`. (src: `resources/dashboard-design.md` "Color Palette Brainstorm"; `resources/agent-rules-proposal.md` §B2)
- **Alternatives considered**: light-only default (rejected — darker aesthetic fits dashboard, and the brainstorm direction); dark-only (rejected — misses OS-preference users).
- **Status**: Accepted (2026-10-20). Toggle is a **future implementation item**; default dark is binding for the build.

---

### [2026-10-20] Mock data lives in a separate `data.js` module
- **Decision**: Mock data is a single `data.js` JS module (not inline `<script>` in `index.html`). Renderers consume the module only.
- **Rationale**: Keeps the API-ready rule honest (a future API swap changes one file); keeps `index.html` diffable; matches `dashboard-design.md` "API-ready architecture". (src: `resources/agent-rules-proposal.md` §B5)
- **Alternatives considered**: inline `<script>` (rejected — contaminates the markup diff and couples data to the page).
- **Status**: Accepted (2026-10-20).

---

### [2026-10-20] Single scrolling page with sticky inline anchor nav (no hamburger/sidebar)
- **Decision**: The dashboard is one scrolling page. Sticky header with inline anchor links to the three blocks (KPIs, Drivers, Details). **No hamburger/sidebar menus.**
- **Rationale**: `resources/dashboard-design.md` evaluated hamburger vs inline links and chose Approach B (inline). The "no navigation" line in `components.md` is retained and interpreted as "no overlay menus / no multi-page routing" — not a veto on anchor links. (src: `resources/dashboard-design.md` "Navigation & Header Strategy"; `resources/agent-rules-proposal.md` §E3)
- **Alternatives considered**: hamburger sidebar (rejected — indirection for a 3-section page, hides structure).
- **Status**: Accepted (2026-10-20).

---

### [2026-10-20] Verification gate with a lightweight HTML sanity check
- **Decision**: Before committing, run an automated pass/fail check: (1) `curl` returns 200 on `/`; (2) HTML sanity check (one `<h1>`, landmarks, three `<section>`, referenced assets resolve, a11y basics); (3) 3-breakpoint screenshots (375/768/1024) compared against the design.
- **Rationale**: Aligns with the "give the agent a way to verify its work" best practice. The HTML sanity check is a dependency-free shell/`node` one-liner — no external validator in the committed loop. (src: `resources/agent-rules-proposal.md` §B4, §B4.5)
- **Alternatives considered**: `npx html-validate` (deferred until the build stabilizes — keeps the gate dependency-free).
- **Status**: Accepted (2026-10-20).