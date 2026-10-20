# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
(via informal convention — no version tag exists yet).

## [Unreleased]

### Added

- **Rules proposal FINALIZED + landed** (2026-10-20):
  - `resources/agent-rules-proposal.md` — status set to **FINALIZED**; all §E open questions resolved and binding (theme: dark default + light toggle; data: `data.js` module; nav: keep inline anchor nav; verification: B4 gate + new B4.5 HTML sanity check)
  - `resources/decisions.md` — **NEW** ADC (Architecture Decision Context) log with 4 accepted entries (dark theme + toggle, `data.js` module, sticky inline anchor nav, verification gate)
  - `.agents/rules/core-rules.md` — added Explore→Plan→Code→Verify workflow, Verification Gate (curl 200 / HTML sanity / 3-breakpoint screens), Writer/Reviewer pattern, DoD language; confirmed mock data in `data.js`
  - `.agents/rules/components.md` — clarified "no navigation" → no overlay menus, documented sticky inline anchor nav (Approach B) + `scroll-mt`; added Motion & Interaction State (focus-visible, reduced-motion) and Chart CSS responsive/aspect notes
  - `.agents/rules/layout.md` — confirmed **no build step**; added Theme section (dark default `slate-900`, light toggle via `dark:` variant, build light-first); added chart breakpoint guidance
  - `.agents/rules/accessibility.md` — added Focus & Motion section and the accessible theme-toggle pattern (`aria-pressed`, visible label, localStorage + `prefers-color-scheme`)
  - `AGENTS.md` — added **Project Story**, **TANSTAAFL** (there is no such thing as a free lunch — do the simple correct thing), and **ADC log format** sections
  - `resources/dashboard-design.md` — theme resolved (dark default + light toggle) in Color Palette Brainstorm + Proposed Implementation Methods; static mock data row updated to `data.js` module
- **Pre-development survey & resources** (2026-10-20):
  - `resources/development-rollout-todo.md` — prioritized to-do list (repo alignment → information depth → implementation)
  - `resources/repo-alignment-audit.md` — full docs survey, repo alignment findings, guidelines audit (AGENTS.md standard, Claude Code best practices, real-world AGENTS.md examples)
  - `resources/agent-rules-proposal.md` — draft rules (behavioral + engineering) + Definition-of-Done checklist for a high-quality build
  - `project-overview.md` — project scope, goals, architecture, key files
  - `tech-stack.md` — verified tech stack, commands, dependencies, constraints
  - `current-status.md` — status ledger with what works, gaps, next priorities
  - `document-plan.md` — inventory/hub file with maintenance rules
  - `changelog.md` — this file
- **Cross-validation review infrastructure** — `memory-bank/review-edits/` directory created; fact-checker and consistency-checker reviews completed for first validation pass
- **Second revision pass (dual-reviewer, Luna + Sol)** — independent reviews completed for all 5 memory-bank core files (`project-overview`, `tech-stack`, `current-status`, `document-plan`, `changelog`); 10 review files in `memory-bank/review-edits/`

### Fixed

- `tech-stack.md` — corrected 6 stale line-number references across 5 files (`server.py:48`→`:37`, `AGENTS.md:28`→`:38`, `AGENTS.md:29`→`:39`, `components.md:25`→`:58`, `layout.md:5`→`:7`, `layout.md:29`→`:28`) and repaired broken Dependency Inventory table (missing `Type` column)
- `changelog.md` — corrected commit count from "7 commits on main" to "5 commits on main"
- `.agents/rules/core-rules.md` — updated superseded "memory bank not yet initialized" language; fixed archive path from `.agents/rules/archive/` to `memory-bank/archive/`; removed duplicate platform/product inline list (now links to `resources/profile.md`)
- `AGENTS.md` — fixed dangling reference to `memory-bank-generator-prompt.md` (actual name: `prompt-memory-bank-generator.md`)
- `document-plan.md` — updated review/validation files inventory to reflect existing review files (first + second pass)
- `project-overview.md` — removed duplicate inline platform list (now links to `resources/profile.md`)
- `current-status.md` — corrected commit count from "7 commits" to "5 commits on `main` (7 commits total in repository)"

### Changed

- `AGENTS.md` updated to point to `memory-bank/` (read-all-at-start mandate) — see `AGENTS.md` line references.

---

## [0.1.0] — 2026-10-19

### Added

- Repository initialized with 4Geeks Academy HTML Hello template (`server.py`, `README.md`, `learn.json`)
- `AGENTS.md` — agent entry point with file map and mandate
- `.agents/` workspace directory:
  - `.agents/rules/core-rules.md` — general conduct, project-specific rules
  - `.agents/rules/components.md` — reusable component patterns, Chart CSS
  - `.agents/rules/layout.md` — Tailwind v4 CDN, mobile-first design, breakpoints
  - `.agents/rules/semantic-html.md` — semantic HTML conventions
  - `.agents/rules/accessibility.md` — a11y best practices
  - `.agents/scripts/init.sh` — utility script
- `resources/profile.md` — client persona (multi-platform influencer, 3 products, 15% commission)
- `resources/dashboard-design.md` — design plan (three-block layout, color palette, typography, grid strategy)
- `generate-profile-insights.md` — scratchpad for profile generation
- `generate-dashboard-guidelines.md` — scratchpad for dashboard design plan
- `prompt-memory-bank-generator.md` — spec for memory bank initialization workflow
- `README.cn.md`, `README.es.md` — Chinese and Spanish translations
- Git history with 5 commits on `main` branch (7 commits total in repository); remote `origin` configured on GitHub