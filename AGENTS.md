# AGENTS.md — Agent Entry Point

> **For AI coding agents.** Start here every session, whatever tool or environment you run in.

## Project: Influencer Dashboard

A one-page Tailwind CSS dashboard showing an influencer's commissions, revenue, conversions, and engagement across 5 platforms and 3 products. Static HTML/CSS/JS, served by a small Flask dev server.

## Start of every session

Your memory doesn't carry over between sessions, so this repo keeps it for you in `memory-bank/`.

1. Open `memory-bank/README.md` and follow its start-of-session steps. They tell you what the project is, how to run it, where things stand and what the last session left open.
2. Read `resources/design-spec.md`, **the single, binding spec** for layout, colour, type, components, content, and definition of done, before any visual change.
3. Read `.agents/rules/core-rules.md`, which says how to work in this repo, including how to change the spec instead of inventing new standards.

Look up as needed: `resources/profile.md` (the client), `resources/decisions.md` (why decisions were made), `resources/mock-data-plan.md` (data schema), `resources/brief.md` (the original brief).

## End of every session

Before you finish or hand work back, update the memory bank as `memory-bank/README.md` describes: `status.md`, a new entry at the top of `log.md`, anything learned in `notes.md`. Then run `python3 scripts/check-memory.py` and commit the memory changes with the work. Write things down as you learn them; sessions can end without warning.

## Code

Commands are in `memory-bank/context.md`, and the docs map is its "Where facts live" table.

| Path | Purpose |
|---|---|
| `index.html` | The dashboard page: sticky nav and three `<section>` blocks (KPIs, Drivers, Details). |
| `app.js` | Renderers only. Consumes `window.DATA`; one render function per component. |
| `data.js` | Generated mock data (`window.DATA`). Don't hand-edit. |
| `scripts/generate-data.py` | Deterministic generator for `data.js`, with invariant checks. |
| `scripts/screenshots.py` | Retakes `resources/screenshots/` and checks for console errors and horizontal scroll. |
| `scripts/check-memory.py` | Checks the memory bank and lists commits it hasn't caught up with. |
| `server.py` | Flask dev server on port 3000. |

## Decision log format

Log decisions with lasting consequences in `resources/decisions.md`:

```
### [YYYY-MM-DD] Title
- **Decision**: one line
- **Rationale**: why
- **Alternatives considered**: what we didn't pick and why
- **Status**: Accepted / Superseded by [title]
```
