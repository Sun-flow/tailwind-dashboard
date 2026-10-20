# Project Overview

> **Date**: 2026-10-19
> **Status**: Design/planning phase — no implementation code written yet.

## What This Project Is

An **Influencer Dashboard** — a single-page, responsive Tailwind CSS dashboard for tracking income, revenue, and engagement metrics across an influencer's online platforms. Built as a static HTML/CSS/JS frontend served by a Flask development server.

### Goals

- Consolidate scattered analytics from 5 platforms (see `resources/profile.md` for full platform list) into one unified view.
- Answer 5 core questions at a glance:
  1. 💰 How much commission am I earning?
  2. 📦 Which products generate the most revenue?
  3. 📈 How well are my ads converting?
  4. 🏆 Which platforms generate the best return?
  5. ❤️ What is the engagement rate by platform/product?
- Provide a data-driven decision tool for content creation and ad spend allocation.
- Deliver a working prototype first; real API integration is a future goal.

## What This Project Isn't

- **Not a production-ready SaaS app** — no backend database, no auth, no real API integrations (yet).
- **Not multi-user** — a single influencer persona drives all data and UI decisions.
- **Not a heavy SPA** — vanilla JS only; no React, Vue, or framework.
- **Not using a paid charting library** — Chart CSS only, zero heavy dependencies.

## Scope & Boundaries

| In scope | Out of scope |
|---|---|
| Single-page responsive dashboard (`index.html`) | Multi-page routing |
| KPI summary cards (4 top-level metrics) | Real-time data / WebSockets |
| Product & platform breakdown tables | User authentication |
| Conversion funnel visualization | Database persistence |
| Static mock data in separate `data.js` module | External API integrations |
| Tailwind CSS v4 via CDN (no build step) | Custom CSS (beyond Tailwind utils) |
| Chart CSS for data visualization | Paid charting libraries (Chart.js, D3, etc.) |
| Flask dev server (`server.py`) | Production deployment config |

## Definition of Done (Initial Build)

- [ ] `index.html` exists with the full three-block dashboard layout
- [ ] All KPI cards, driver charts, and data tables render with mock data
- [ ] Responsive at mobile (375px), tablet (768px), and desktop (1024px+)
- [ ] Sticky navigation header with anchor links to the three blocks
- [ ] Mock data in separate `data.js` module (`resources/decisions.md`)
- [ ] Consistent component patterns (KPI cards, section blocks, tables, badges)
- [ ] Dark theme default (`slate-900`); light-toggle ready via `dark:` utilities (`resources/decisions.md`)
- [ ] No custom CSS beyond Tailwind utilities and Chart CSS

## Key Files

| Path | Purpose |
|---|---|
| `AGENTS.md` | Agent entry point — read first every session |
| `memory-bank/` | ✅ This directory — durable project memory for all agents |
| `.agents/rules/` | Agent behavioral rules, component/layout/a11y/semantic-html conventions |
| `resources/profile.md` | Client persona — multi-platform influencer, 3 products, 15% commission |
| `resources/dashboard-design.md` | Design plan — layout strategy, color palette, typography, component patterns |
| `resources/development-rollout-todo.md` | **NEW (2026-10-20)** — prioritized to-do list for implementation |
| `resources/repo-alignment-audit.md` | **NEW (2026-10-20)** — docs survey, repo alignment, guidelines audit |
| `resources/agent-rules-proposal.md` | **NEW (2026-10-20)** — draft agent rules proposal |
| `resources/decisions.md` | **NEW (2026-10-20)** — ADC log (theme, data.js, nav, verification) |
| `server.py` | Flask dev server (port 3000) — serves static files |
| `generate-dashboard-guidelines.md` | Scratchpad doc that produced `resources/dashboard-design.md` |
| `generate-profile-insights.md` | Scratchpad doc that produced `resources/profile.md` |
| `index.html` | *(to be created)* Main dashboard page |
| `learn.json` | 4Geeks Academy template metadata (not project-specific) |
| `prompt-memory-bank-generator.md` | Spec for initializing this memory bank |

## High-Level Architecture & Data Flow

```
┌──────────────────────────────────────────────────────────┐
│                    Flask Dev Server                       │
│                    server.py:3000                         │
│              (serves static files only)                   │
└──────────────┬───────────────────────────────────────────┘
               │ GET /
               ▼
┌──────────────────────────────────────────────────────────┐
│                   index.html                              │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  <header> — Sticky nav with anchor links            │  │
│  │  <main>                                             │  │
│  │    <section id="kpis">     — KPI outcome cards      │  │
│  │    <section id="drivers">  — Charts & breakdowns    │  │
│  │    <section id="details">  — Tables, alerts, lists  │  │
│  │  </main>                                            │  │
│  <script src="data.js"> — Mock data module          │  │
└─────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

Data flow: Mock data module (`data.js`) → vanilla JS renders into DOM using Tailwind/Chart CSS classes. A future API integration swaps the module contents only — renderers are unchanged.

## Agent Rules & Entry Points

See `document-plan.md` for the full file inventory. All agents start at `AGENTS.md`, which mandates reading:
1. `AGENTS.md` itself
2. All files in `.agents/rules/`
3. `resources/profile.md`
4. All files in `memory-bank/`

### See also

- `tech-stack.md` — language, framework, dependency versions
- `current-status.md` — what works, what's blocked, next steps
- `changelog.md` — change history