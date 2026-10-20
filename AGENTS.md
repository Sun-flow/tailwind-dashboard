# AGENTS.md — Agent Entry Point

> **For AI coding agents.** Read this file and every file it references at the start of every session.  
> The memory bank (`memory-bank/`) is initialized and active. **Read all files in `memory-bank/` before doing any work in the repo.**

## Project: Influencer Dashboard

A **Tailwind CSS dashboard** for tracking income, revenue, and engagement metrics across an influencer's online platforms. Built on a static HTML/CSS/JS frontend served by a Flask dev server.

**Key files:**

| Path | Purpose |
|---|---|
| `AGENTS.md` | You are here. Start here every session. |
| `.agents/rules/` | Agent behavioral & project rules — **read all files** in this directory. |
| `.agents/scripts/` | Agent utility scripts. |
| `resources/` | Repo resources — persona docs, images, temp files, website assets. |
| `resources/profile.md` | **Client profile** — who we're building for, their goals, products, platforms. |
| `generate-profile-insights.md` | Planning doc used to generate `resources/profile.md`. |
| `server.py` | Flask development server (port 3000). |
| `prompt-memory-bank-generator.md` | Spec for initializing the memory bank later. |
| `index.html` | *(to be created)* Main dashboard page. |

## Mandate

1. **Read-all-first**: at the start of every task or session, read:
   - `AGENTS.md` (you are here)
   - Every file in `.agents/rules/`
   - `resources/profile.md`
   - **Every file in `memory-bank/`** (project overview, tech stack, current status, document plan, changelog)
2. **Evidence-only**: every claim must be verified against the actual repository files. Cite `path/to/file:line`. Never fabricate.
3. **Memory bank is the source of truth**: project knowledge lives in `memory-bank/`. Agent behavioral rules live in `.agents/rules/`. Keep the separation — agent-facing vs human-facing, memory vs rules.
4. **Update on triggers**: update `memory-bank/` after discovering new patterns, implementing significant changes, status changes, or when told "update memory bank".

## Quick Start

```bash
pip3 install flask          # one-time
python3 server.py           # starts dev server at http://0.0.0.0:3000
```

For Tailwind CSS v4 via CDN (no build step), add to `<head>`:
```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```