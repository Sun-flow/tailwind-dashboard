# Core Agent Rules

> **Last updated**: 2026-10-19

## Mandatory Read-at-Start

At the start of every task or session, the agent MUST read:

1. `AGENTS.md` — entry point, file map, and mandate
2. All files in `.agents/rules/` — behavioral and project rules
3. `resources/profile.md` — client persona, goals, products, and platforms

## General Conduct

- **Verify claims** against actual files, manifests, and git history. Cite `path/to/file:line` evidence. Never fabricate.
- **Single source of truth**: each fact lives in exactly one file; others link to it. No duplication.
- **Date everything** in ISO-8601 format.
- **Archive, don't delete** — superseded content goes to `.agents/rules/archive/` with a linking note.
- **Write for the next amnesiac session** — always include the *why*, not just the *what*.
- **Memory bank not yet initialized**. The bank (`memory-bank/`) will be generated when directed, following the spec in `memory-bank-generator-prompt.md`. Until then, all project knowledge lives in `.agents/rules/`.

## Project-Specific Rules

1. This project is a **Tailwind CSS dashboard** for tracking an influencer's income, revenue, and engagement across online platforms.
2. All UI work uses **Tailwind CSS** (v4 via CDN or build step). Avoid custom CSS when Tailwind utilities suffice.
3. The Flask dev server (`server.py`) serves static files. Add a build step if Tailwind compilation is needed.
4. Keep `AGENTS.md` as the single entry point — all agents start here.
5. **Client profile lives in `resources/profile.md`** — the client is a multi-platform influencer (Instagram, YouTube, TikTok, Twitter, Twitch) promoting 3 products (A: $50, B: $120, C: $80) at 15% commission. All dashboard data and UI decisions must align with this persona.