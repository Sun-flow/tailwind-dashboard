# Core Agent Rules

> **Last updated**: 2026-10-19

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

## Project-Specific Rules

1. This project is a **Tailwind CSS dashboard** for tracking an influencer's income, revenue, and engagement across online platforms.
2. All UI work uses **Tailwind CSS** (v4 via CDN or build step). Avoid custom CSS when Tailwind utilities suffice.
3. The Flask dev server (`server.py`) serves static files. Add a build step if Tailwind compilation is needed.
4. Keep `AGENTS.md` as the single entry point — all agents start here.
5. **Client profile lives in `resources/profile.md`** — the client is a multi-platform influencer (see `resources/profile.md` for full platform, product, and commission details). All dashboard data and UI decisions must align with this persona.