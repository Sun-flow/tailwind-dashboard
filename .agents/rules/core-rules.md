# Core Agent Rules

> **Last updated**: 2026-10-20

## Mandatory Read-at-Start

At the start of every task or session, the agent MUST read:

1. `AGENTS.md` — entry point, file map, and mandate
2. All files in `.agents/rules/` — behavioral and project rules
3. `resources/profile.md` — client persona, goals, products, and platforms
4. **All files in `memory-bank/`** — project overview, tech stack, current status, document plan, changelog

## General Conduct

- **Verify claims** against actual files, manifests, and git history. Cite `path/to/file:line` evidence. Never fabricate.
- **Single source of truth**: each fact lives in exactly one file; others link to it. No duplication.
- **Date everything** in ISO-8601 format.
- **Archive, don't delete** — superseded content goes to `memory-bank/archive/` with a linking note.
- **Write for the next amnesiac session** — always include the *why*, not just the *what*.
- **Memory bank is initialized** at `memory-bank/` (project overview, tech stack, current status, document plan, changelog). Read all files there before starting work.

## Workflow (Explore → Plan → Code → Verify)

For any task larger than a one-sentence diff, follow all four steps in order:

1. **Explore** — read the relevant design/profile/memory files before editing (`resources/dashboard-design.md`, `resources/profile.md`, `.agents/rules/*`, `memory-bank/*`).
2. **Plan** — state the approach (which files, which patterns) before coding.
3. **Code** — implement.
4. **Verify** — run the check defined for this task (see Verification Gate below) and report evidence.

Small tasks (typo, one-line change) skip straight to Code + Verify. If a task is not clear enough to plan, ask rather than guess.

## Verification Gate — Never Claim "Done" Without Evidence

**Before committing**, run at least one automated pass/fail check from this menu and include the output:

- **Endpoint smoke**: `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3000/` returns `200`.
- **HTML sanity check** (dependency-free): assert `index.html` exists; every referenced local asset resolves; exactly one `<h1>`; `<header>`, `<nav>`, `<main>` present; three `<section id="…">` blocks; interactive elements carry accessible labels and `<img>` tags carry `alt`. Implement as a shell/`node` one-liner — no external validator in the committed loop.
- **Screen-scale check**: screenshot at 375px, 768px, 1024px and compare against the three-block design (`resources/dashboard-design.md`).
- (When a test framework exists — none yet — the suite becomes the gate.)

It is **better to say "I could not verify this"** than to assert success without a check. If a check cannot run, say why and propose the check.

## Review (Writer/Reviewer)

After implementing anything of substance (a new section, a rewritten render path, a data schema), get a **fresh-context review** — a separate agent/pass (or human) sees only the diff + the rules checklist in `resources/agent-rules-proposal.md` §C, not the reasoning that produced it. The reviewer flags only correctness/requirement gaps, not style preferences.

## Project-Specific Rules

1. This project is a **Tailwind CSS dashboard** for tracking an influencer's income, revenue, and engagement across online platforms.
2. All UI work uses **Tailwind CSS v4 via CDN — no build step** (CDN `<script>` in `<head>`, no config/compilation). Avoid custom CSS when Tailwind utilities suffice.
3. The Flask dev server (`server.py`) serves static files. Running it is `python3 server.py` (see `AGENTS.md`); no other tooling is required to preview.
4. Keep `AGENTS.md` as the single entry point — all agents start here.
5. **Client profile lives in `resources/profile.md`** — the client is a multi-platform influencer (see `resources/profile.md` for full platform, product, and commission details). All dashboard data and UI decisions must align with this persona.
6. **Mock data lives in `data.js`** (single source, API-ready). Renderers consume the module; a future API swap changes one file. See `resources/agent-rules-proposal.md` §B5.