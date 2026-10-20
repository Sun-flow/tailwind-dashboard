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

---

### [2026-10-20] Global `window.DATA` load pattern (plain script, not an ES module)
- **Decision**: `data.js` assigns to a global `window.DATA` and is loaded with a plain `<script src="data.js">` before `app.js` — **not**`type="module"`.
- **Rationale**: Rule B5 requires one shared data module for API-readiness; a global object (mock-data-plan §7 "Load pattern" Option A) lets `app.js` load with a plain tag, keeping CDN + vanilla-JS constraints (no bundler, no `import` path resolution) and keeping the data layer trivially swappable. Approved by client ("option A").
- **Alternatives considered**: ES module `import` (rejected — requires `type="module"` on the app script and strict CORS/ordering for a local file; no bundler in the no-build-step stack).
- **Status**: Accepted (2026-10-20).

---

### [2026-10-20] Deterministic seeded Python generator for mock data
- **Decision**: Mock data is produced by `scripts/generate-data.py` (Python 3, `random.Random(seed)`) writing a **committed static `data.js`** — not generated at runtime, not JS.
- **Rationale**: A dev-time tool keeps the committed artifact byte-identical across runs (same seed → same file), enforces invariant checks before writing (never commit bad/leaky data), and does **not** violate the no-build-step rule (mock-data-plan §5.2 decision). Approved by client ("python").
- **Alternatives considered**: JS generator (rejected — Python is already in the toolchain for `server.py`, and the output is static regardless of language); runtime generation in `server.py` (rejected — breaks determinism and adds a build step).
- **Status**: Accepted (2026-10-20).

---

### [2026-10-20] Precomputed derived rollups in `data.js`
- **Decision**: KPI rollups (`derived.*`: total commission/revenue, per-platform/product revenue share, MoM deltas, top product/platform, avg ER, overall ROI, units sold, conversions) are **computed at generation time** and stored in `data.js`; renderers only read.
- **Rationale**: Matches "renderers consume only" from `dashboard-design.md` — the single data source answers the 5 core questions without duplicating business logic in `app.js` (mock-data-plan §7 "Derived-storage"). Approved by client ("precompute").
- **Alternatives considered**: computing in `app.js` (rejected — scatters business logic, two places to keep in sync).
- **Status**: Accepted (2026-10-20).

---

### [2026-10-20] 10 campaigns by default (2 per platform)
- **Decision**: The dataset ships exactly **10 campaigns** — 2 per platform (one pushed "tag push", one organic) — each tied to one product with its own budget/spend/ROI/funnel.
- **Rationale**: Gives the Details-block campaigns table enough rows to be meaningful without drowning a demo; 2 per platform keeps referral/funnel invariants (campaign revenue ≤ platform revenue) easy to guarantee. Approved by client ("seems fine" → 10).
- **Alternatives considered**: 8 (same structure, fewer rows); 12+ (rejected — clutter for a demo dataset).
- **Status**: Accepted (2026-10-20).

---

### [2026-10-20] Product categories (lifestyle / premium / starter)
- **Decision**: The 3 products carry a `category` label: **prod-a = lifestyle ($50)**, **prod-b = premium ($120)**, **prod-c = starter ($80)**.
- **Rationale**: Cheap cosmetic touch used by the product-comparison block (color/legend/grouping) and makes product mix readable; prices unchanged from `resources/profile.md`. Approved by client ("give them categories").
- **Alternatives considered**: generic A/B/C only (rejected — flat and no design hooks for comparison).
- **Status**: Accepted (2026-10-20).

---

### [2026-10-20] 10-month reporting span (2026-01 → 2026-10)
- **Decision**: `monthlySeries` covers **10 months**: `2026-01` → `2026-10`, anchor month 2026-10.
- **Rationale**: Long enough for meaningful trend arrows + MoM deltas + future sparklines without ballooning the file; end-of-period 2026-10 is a realistic "today" for a demo. Approved by client ("sounds good").
- **Alternatives considered**: 12 months (rejected — 2 extra rows of marginal value, larger diff); 3–6 months (rejected — too short for a trend story).
- **Status**: Accepted (2026-10-20).
---

### [2026-10-20] One binding design spec; superseded docs archived
- **Decision**: `resources/design-spec.md` is the single source for layout, colour, type, components, section content, and definition of done. `.agents/rules/` is trimmed to `core-rules.md`, `accessibility.md`, and `semantic-html.md`. Older planning docs, rules, and memory-bank files move to `archive/`.
- **Rationale**: The same decisions were written in five or six files that contradicted each other (card padding, breakpoints, the KPI set, "no navigation", the Charts.css URL, the no-inline-style rule). Each contradiction caused visual drift. Contradictions settled in the spec: base/`md:`/`lg:` breakpoints only; the KPI cards follow the brief's Revenue / Volume / Engagement / Performance categories; inline `style` is allowed only for Charts.css data values; the page renders from JS (no no-JS requirement); dark by default unless the user saved light; commissions only (no YouTube ad or Twitch subscription revenue yet); trends compare against last month.
- **Alternatives considered**: patching each conflicting file in place (rejected: the duplication would drift again); semantic `@theme` colour tokens instead of `dark:` pairs (deferred: the code already uses pairs consistently).
- **Status**: Accepted (2026-10-20). Supersedes the OS-preference first-load note in the archived accessibility rule.

---

### [2026-10-20] Drivers and Details build-out
- **Decision**: Build the rest of the Drivers and Details blocks (spec §8). Activity and engagement are normalised onto shared columns in the generator (`derived.activityByPlatform`, `derived.interactionsByPlatform`), with `null` for "doesn't apply". Top lists, ranked by commission, and improvement opportunities are also generated (`derived.rankings`, `derived.opportunities`). Alerts use a red / amber / gray severity pill, and ROI is shown as `2.8x`.
- **Rationale**: Platforms name content and interactions differently (X replies vs comments, Twitch chat), so mapping them in the generator keeps `app.js` free of business logic. Campaigns are ranked by commission rather than ROI because tiny Twitch tests ($33 spend) top any ROI ranking. Amber gives "medium" alerts a colour that isn't read as a trend direction.
- **Alternatives considered**: stacked multi-colour activity and engagement bars (rejected: breaks "one series colour per chart" and needs a legend); a sparse activity table (tried, rejected: mostly dashes and it scrolled in a half-width card).
- **Status**: Accepted (2026-10-20).

---

### [2026-10-20] Sales funnel drawn as linear bars, overall and per platform
- **Decision**: The funnel is a full-width card above the Drivers grid. It shows overall impressions → link clicks → conversions as linear Charts.css bars labelled with raw values and step rates, then one chart per step across platforms, then a table of each platform's step rates. Non-zero bars are at least 2px wide.
- **Rationale**: mae wants the size of each drop visible as a picture, even when the smallest step is a sliver, as long as the labels give the exact numbers. Per-step charts with their own scale keep every platform's bar readable, and the table gives the per-platform drop-off.
- **Alternatives considered**: a stage list with numbers only (first version; rejected by mae as too little visual information); a log scale (rejected: understates the drop); one mini funnel per platform on a shared scale (rejected: clicks and conversions would be slivers on every platform, so platforms couldn't be compared).
- **Status**: Superseded by [Sales funnel as 100% stacked bars].

---

### [2026-10-20] Sales funnel as 100% stacked bars
- **Decision**: Each platform (and "All platforms") gets one horizontal bar that is 100% of its impressions. The bar is split into bought, clicked but didn't buy, and saw but didn't click, using one indigo hue (darkest = furthest step) and neutral gray for "didn't click". `derived.funnelMix` holds the shares, which an invariant checks sum to 100. The step-rate table stays.
- **Rationale**: mae's reference was a 100% stacked bar chart. The funnel steps are nested (a buyer also clicked and saw), so the three buckets partition impressions and a part-to-whole bar is truthful. One hue keeps the steps reading as an order, not as unrelated categories.
- **Alternatives considered**: linear bars per step (the previous version; replaced at mae's request); a zoomed bar of clicks only (not built yet: it would make the bought/clicked split easier to see, but the whole-funnel framing is what mae asked for).
- **Status**: Accepted (2026-10-20).
