# Agent Rules — Proposal Draft

> **Date**: 2026-10-20
> **Status**: **FINALIZED** — open questions resolved 2026-10-20; decisions below are binding.
> **Purpose**: Rules for our agent that ensure a high-quality output application, shaped by the guidelines audit in `resources/repo-alignment-audit.md` and by the existing `.agents/rules/` files.
> **Where this lands**: these rules are split into additions/amendments to the existing `.agents/rules/*.md` files and/or `AGENTS.md` — see §D.

---

## Why These Rules

The audit surfaced two gaps that most affect output quality:

1. **No verification-before-commit contract** — best practices say "give Claude a way to verify its work"; we currently have no pass/fail gate defined.
2. **No Writer/Reviewer standard** — an independent second pass (fresh context) catches self-bias.

Plus several alignment fixes (components.md says "no navigation" while the design plan decided on sticky nav; theme undecided; mock data schema undefined).

The proposed rules below are grouped into **behavioral** (how we work) and **engineering** (what "done & good" means). Each is tagged with its source (existing repo rule, best-practice audit, or new).

---

## A. Behavioral Rules (How We Work)

### A1. Read-all-first & Single Source of Truth (existing)
**Rule**: At session start, read `AGENTS.md` → `.agents/rules/` → `resources/profile.md` → all `memory-bank/` files, per `AGENTS.md` mandate. Each fact lives in exactly one file; other files link (→ `resources/profile.md`, `memory-bank/*`), never duplicate.
**Why**: Prevents drift like the theme / nav conflicts we currently have.

### A2. Explore → Plan → Code → Verify (new, from best-practices audit)
**Rule**: For any task larger than a one-sentence diff:
1. **Explore** — read the relevant design/profile/memory files before editing.
2. **Plan** — state the approach (which files, which patterns) before coding.
3. **Code** — implement.
4. **Verify** — run the check defined for this task (see B4).
Small tasks (typo, one-line change) skip straight to Code + Verify.
**Why**: "Optimize for the outcome, not the detour" — planning before implementation avoids solving the wrong problem.

### A3. Never claim "done" without evidence (new, from best-practices audit)
**Rule**: Every "✅ done" must be backed by an output the agent can read — test output, `curl` status, screenshot — not a guess. If a check can't run, say so explicitly and propose the check.
**Why**: "Without a check, 'looks done' is the only signal" (Claude Code best practices). This is the single highest-leverage rule we can adopt.

### A4. Writer/Reviewer for non-trivial work (new)
**Rule**: After implementing anything of substance (a new section, a rewritten render path, a data schema), get a **fresh-context review** — a separate agent/pass (or human) sees only the diff + the rules checklist, not the reasoning that produced it. The reviewer flags only correctness/requirement gaps, not style preferences.
**Why**: "A reviewer that sees the result, not the reasoning, evaluates on its own terms" (Claude Code best practices; Writer/Reviewer pattern).

### A5. Small, atomic diffs + clean tree (new)
**Rule**: Prefer small focused commits (Conventional Commits, Keep a Changelog entry). Never leave the tree dirty at end of session. If you must make a multi-file change, split with clear commit boundaries.
**Why**: Matches the `changelog.md` (Keep a Changelog) & SemVer conventions; makes adversarial review and rollback possible.

### A6. Respect the memory bank update triggers (existing)
**Rule**: Update `memory-bank/` on: new patterns discovered, significant changes implemented, blocker/status change, direction change, or when the user says "update memory bank". Always date entries (ISO-8601). Archive, don't delete.
**Why**: Amnesia-proof contract — the next agent must reconstruct our state from the files alone.

---

## B. Engineering Rules (What "Done & Good" Means)

### B1. Components & consistency (existing — keep, add active-section note)
**Rule**: Use exactly the patterns in `.agents/rules/components.md` — KPI card, section block, data table, alert/badge. Do **not** mix structures; if a pattern is wrong, update the rule file rather than deviating silently.
**Amendment (conciliation)**:
- Replace the now-wrong "no navigation — single page" line in `components.md:29` with the decided **sticky inline anchor nav** (Approach B from `dashboard-design.md`).
- Note the `scroll-mt` offset so the sticky header never hides a section title on hash-jump.

### B2. Layout & mobile-first (existing — keep)
**Rule**: Mobile-first; base = <640px, then `sm:`, `md:`, `lg:`. No pixel-based sizes. All interactive elements ≥44×44px. Tailwind v4 CDN only; Chart CSS is the sole visualization exception; no custom CSS beyond Tailwind utilities.
**Amendment (chart behavior)**: charts keep a defined aspect ratio (`aspect-[4/3]` desktop, allow `overflow-x-auto` only where unavoidable) — add this to `components.md`.
**Amendment (theme — RESOLVED 2026-10-20)**: **Dark theme is the default** (`slate-900` bg). A **light-mode toggle is allowed** (sun/moon button in sticky header, `prefers-color-scheme` OS-aware via Tailwind v4 `dark:` variant, persisted to `localStorage`). Build light-first with `dark:` utilities so both states work; add the toggle as a future implementation item — not required for the first vertical slice.

### B3. Semantic + accessible (existing — keep)
**Rule**: Per `.agents/rules/semantic-html.md` and `accessibility.md` — one `<h1>`, landmark roles, `aria-label`, `alt`, keyboard order, `aria-hidden` on decorative icons.
**Proposed addition**: focus-visible rings + reduced-motion respect for micro-interactions, plus a documented accessible theme-toggle pattern (`aria-pressed`, visible label) — fills the "motion & states" gap.

### B4. Verification gate (new — the headline engineering rule)
**Rule**: Before committing, run at least one **automated** pass/fail check from this menu:
- Endpoint smoke: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3000/` returns `200`.
- HTML lint / structure: file exists, contains `<main>`, `<header>`, `<nav>`, three `<section>`s (or whatever the block structure requires).
- Screen-scale check: screenshot at 375px, 768px, 1024px and compare against the three-block design.
- (When a test framework exists — none yet — the suite becomes the gate.)
**Why**: This is the "give Claude a way to verify its work" rule made concrete for a static-dashboard repo.

### B4.5 HTML sanity check (new — lightweight validator, RESOLVED 2026-10-20)
**Rule**: The HTML structure check is the committed "lightweight validator". It is a dependency-free shell/`node` one-liner asserting:
1. `index.html` exists and every local asset it references resolves (`data.js`, CSS).
2. Required landmarks present: exactly one `<h1>`; `<header>`, `<nav>`, `<main>`; three `<section id="…">` blocks.
3. No unclosed tags / stray `<` in text content (regex sanity, not a full parser).
4. Interactive elements carry `aria-label` and `<img>` tags carry `alt` (grep-based) when no visible label exists.
An external validator (e.g. `npx html-validate`) is **optional** and only after the build stabilizes — keep it out of the committed gate to avoid a dependency.
**Why**: A pass/fail signal for document structure and a11y basics without adding a toolchain.

### B5. Data layer must be single-source & API-ready (existing concept — make it a rule)
**Rule**: Mock data lives in exactly one `data.js` module (RESOLVED 2026-10-20 — separate file, not inline `<script>`). Renderers consume the module only; a future API swap changes one file. Define the schema (products, platforms, campaigns, KPI rollups) before writing renderers.
**Why**: `dashboard-design.md` already says "data layer isolated"; current repo has no data artifact yet. A separate file keeps the API-ready rule honest and keeps `index.html` diffable.

### B6. Section/feature = one module pattern (new, mild)
**Rule**: Each of the three blocks (KPIs, Drivers, Details) is one `<section>` with a clear `id`; renderer functions are named by section and co-located. Keeps the diff map predictable ("KPIs block here") for the reviewer.
**Why**: Predictability; consistent with the component-pattern rule.

---

## C. Standard "Definition of Done" Checklist (for each feature)

A task is **done** when all of these hold:

- [ ] Meets the design intent in `resources/dashboard-design.md` + `resources/profile.md` (client persona and 5 core questions).
- [ ] Matches the patterns in `.agents/rules/components.md` / `layout.md` (no silent deviation).
- [ ] Semantic HTML + a11y per rules (roles, alt, keyboard, focus, ≥44px targets).
- [ ] Responsive: renders correctly at 375px, 768px, 1024px+.
- [ ] Mock data consumed from the single data source (no inline magic numbers).
- [ ] Verification check (B4) ran and passed; evidence attached.
- [ ] Fresh-context review (A4) done for non-trivial work; findings addressed or explicitly deferred.
- [ ] `memory-bank/` updated if facts/patterns/status changed (A6).
- [ ] `changelog.md` entry added (Keep a Changelog format).

---

## D. Proposed File Changes to Land These Rules

| Target file | Change |
|---|---|
| `.agents/rules/components.md` | Clarify "no navigation" (keep — no hamburger/sidebar; add sticky inline anchor nav via Approach B); add Chart CSS responsive/aspect note; add motion/state note |
| `.agents/rules/core-rules.md` | Add A2 (explore→plan→code→verify), A3 (evidence for done), A4 (writer/reviewer), B4 (verification gate) + B4.5 (HTML sanity check), C (DoD checklist) |
| `.agents/rules/layout.md` | Add theme default (dark) + toggle; add chart-breakpoint guidance; confirm no-build-step |
| `.agents/rules/accessibility.md` | Add focus-visible + reduced-motion + accessible theme-toggle pattern |
| `AGENTS.md` | Add a short "Verification" section (run server, curl 200/HTML sanity, 3-screen visual check); keep it brief |
| `resources/dashboard-design.md` | Resolve theme (dark default + light toggle); separate `data.js`; keep as single design source of truth |
| `memory-bank/current-status.md` | Record this finalized session + next steps |

---

## E. Open Questions for the Human

> **RESOLVED 2026-10-20** — decisions below are binding and reflected in §B. Kept here for traceability.

1. **Theme choice** — dark default with a light-mode toggle (OS-aware via Tailwind v4 `dark:` variant, persisted). Toggle button is a future implementation item; dark default is the rule. *(Recommendation accepted.)* Where the toggle lives: sticky header, sun/moon icon, `aria-pressed` + visible label.
2. **Data location** — **separate `data.js`** module (not inline `<script>`). B5 now mandates it.
3. **Nav behavior** — the "no navigation" line in `components.md` is **kept** as the no-hamburger/no-sidebar rule; the page remains a single scrolling page. Sticky inline anchor nav (Approach B) is added alongside, not in place of, that rule.
4. **Verification depth** — yes, a lightweight validator is added, but as the **B4.5 HTML sanity check** (dependency-free one-liner) rather than an external tool. Optional `npx html-validate` deferred until build stabilizes.

---

## F. Summary

These rules convert the **best-practice findings** (verify work, explore→plan→code, writer/reviewer, keep instruction files concise, small atomic diffs, single source of truth) into **enforceable local conventions** for this repo, layered on top of the already-strong `.agents/rules/` and memory-bank system. **Open questions are resolved (2026-10-20):** dark default + light toggle, separate `data.js`, keep the no-hamburger rule, and add the B4.5 HTML sanity check. Per §D, we now land the edits into `.agents/rules/`, `AGENTS.md`, and `resources/dashboard-design.md`, then begin Phase 1/2 of `resources/development-rollout-todo.md`.