# Development Rollout — To-Do List & Priority Plan

> **Date**: 2026-10-20
> **Purpose**: Survey-based priority to-do list for moving from planning to implementation.
> **Companion docs**: `resources/repo-alignment-audit.md` (full survey), `resources/agent-rules-proposal.md` (proposed rules).

---

## Scope of This Document

This file is the **working to-do list** for the transition from *design/planning* → *implementation*.
It is ordered first by **repo alignment** (making sure our docs and rules reflect reality and are consistent),
then by **information depth** (closing gaps before code), then by **implementation sequencing** (the actual build).

> **Priority legend**: 🔴 Blocking · 🟠 Should-do · 🟡 Nice-to-have · 🟢 Low

---

## Phase 0 — Repo Alignment (Do First)

> **Goal**: Get the repository, its rules, and its docs into one true state before building.

| # | Task | Priority | Why It Matters |
|---|---|---|---|
| 0.0 | **Run `.agents/scripts/init.sh`** and reconcile every `✅/⚠️` result with documented state | 🔴 | The init script claims `⚠️ Flask not installed` unless verified; first agent run should confirm the environment is real |
| 0.1 | **Enable the Todo/`todo.md` convention** — `resources/development-rollout-todo.md` becomes the tracking file | 🔴 | Single source of truth for what's done/next; prevents commit churn |
| 0.2 | **Draft proposed agent rules** (see `resources/agent-rules-proposal.md`) | 🔴 | **The #1 task** — governs quality of everything that follows; user-requested first item |
| 0.3 | **Reconcile `.agents/rules/` vs `AGENTS.md` vs memory bank** | 🔴 | Three places currently state slightly different things (e.g., `server.py:37` in tech-stack vs `server.py` not mentioned in AGENTS.md) |
| 0.4 | **Resolve README ambiguity** — README is 4Geeks template boilerplate, but repo is now a real project | 🟠 | Fresh agents/humans reading README get "HTML Hello" instead of "Influencer Dashboard" |
| 0.5 | **Pin the `requirements.txt`** (single `flask` entry) | 🟢 | Removes "pip3 install flask" guesswork; matches `tech-stack.md`'s dependency inventory |
| 0.6 | **Archive the scratchpads** (`generate-dashboard-guidelines.md`, `generate-profile-insights.md`) per maintenance rule 5 | 🟡 | They served their purpose; keep them in `memory-bank/archive/` per "archive, don't delete" |

---

## Phase 1 — Information Depth (Close Gaps Before Code)

> **Goal**: Ensure every interface, data shape, and design token is defined *before* `index.html` is written.

| # | Task | Priority | Why It Matters |
|---|---|---|---|
| 1.1 | **Define the mock data schema** (products, platforms, campaigns, KPI rollups) | 🔴 | The #1 missing artifact — everything renders from it; must live in one place and be reusable |
| 1.2 | **Decide theme** (dark vs light) as a hard requirement | 🟠 | `dashboard-design.md` keeps both as options; an implementation needs one |
| 1.3 | **Choose Chart CSS data model** — verify actual Chart CSS v1 API (`.column`, `.bar`, `.line` idiomatic markup) | 🟠 | Spec references Chart CSS but no real markup has been validated against the library; avoid "innovating" on the library's contract |
| 1.4 | **Define trend/alert/rules** (what anomaly counts as an alert, the threshold) | 🟡 | Alerts are "nice-to-have" but should be *defined*, not invented at render time |
| 1.5 | **Define empty/edge states** (no data, missing platform, NaN in engagement) | 🟡 | Prevents the dashboard from silently showing holes when mocks change |
| 1.6 | **Add `requirements.txt`** (Phase 0.5 covers) | 🟢 | (listed here for completeness) |

---

## Phase 2 — First Implementation Slice (The MVP That Proves The Pattern)

> **Goal**: Ship one complete, vertically-integrated feature end-to-end before scaling to all three blocks.

| # | Task | Priority | Why It Matters |
|---|---|---|---|
| 2.1 | **Scaffold `index.html`** with the three-block `<section>` shell, sticky nav, and `scroll-mt` offset | 🔴 | The atomic unit everything else fills in |
| 2.2 | **Implement ONE KPI card + ONE data table + ONE Chart CSS bar** with mock data | 🔴 | Proves the component pattern, data layer, and chart approach before building all of them |
| 2.3 | **Run the dev server** (`python3 server.py`) and view at 375/768/1024px | 🔴 | The verify-loop from best practices: screenshot → compare → fix |
| 2.4 | **Write a 3-line smoke check** (`server.py` returns `200` for `/`, `index.html` exists) | 🟠 | Gives the agent a pass/fail gate before each commit |

---

## Phase 3 — Complete the Three Blocks

> **Goal**: Full dashboard matching `resources/dashboard-design.md` + `resources/profile.md`.

| # | Task | Priority | Why It Matters |
|---|---|---|---|
| 3.1 | **KPI cards block** — 4 KPIs (commissions, top product, top platform, engagement) | 🔴 | Answers the 5 core questions at a glance |
| 3.2 | **Drivers block** — platform performance bars, product comparison, conversion funnel | 🟠 | Explains the outcomes |
| 3.3 | **Details block** — products/platforms/campaigns tables + alerts + top lists | 🟠 | Actionable operational view |
| 3.4 | **Responsive + a11y pass** (keyboard nav, focus order, `aria-label`, `alt`, 44px targets) | 🟠 | Part of Definition of Done |
| 3.5 | **API-ready data layer** — isolate mocks behind a single JS object | 🟡 | Future API swap touches one file (`profile.md`'s "future goal") |

---

## Phase 4 — Polish & Verification

> **Goal**: The definition-of-done items not yet covered by Phase 2–3.

| # | Task | Priority | Why It Matters |
|---|---|---|---|
| 4.1 | **Adversarial review** (fresh context, checklist = components/layout/a11y rules) | 🟠 | Independent check per best practices; catches self-bias |
| 4.2 | **README refresh** (or archive template README) | 🟡 | Finishes Phase 0.4, closes the repo-alignment loop |
| 4.3 | **First-pass review of memory bank** (record this session) | 🟡 | Keeps the amnesia-proof contract |
| 4.4 | **CI smoke check** (optional, low priority) | 🟢 | `current-status.md` already lists it as "not needed"; revisit only if humans rely on CI |

---

## Suggested Implementation Order (compressed)

1. **Phase 0.0–0.2** — run init, confirm environment, **draft agent rules** (the #1 priority).
2. **Phase 0.3–0.6** — reconcile rules/docs/README, pin deps, archive scratchpads.
3. **Phase 1.1–1.2** — define mock data schema and **pick the theme**.
4. **Phase 2.1–2.4** — scaffold + one vertical slice + verify loop.
5. **Phase 3** — complete blocks; check against the three-block design.
6. **Phase 4** — adversarial review, README/archive cleanup, memory bank update.

> *Details of what each section should contain, spec decisions to lock, and exact verification steps are in `resources/repo-alignment-audit.md`.*