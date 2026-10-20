# AGENTS.md — Agent Entry Point

> **For AI coding agents.** Start here every session.

## Project: Influencer Dashboard

A one-page Tailwind CSS dashboard showing an influencer's commissions, revenue, conversions, and engagement across 5 platforms and 3 products. Static HTML/CSS/JS, served by a small Flask dev server.

## Read first (in this order)

1. `resources/design-spec.md` — **the single, binding spec** for layout, colour, type, components, content, and definition of done.
2. `.agents/rules/core-rules.md` — how to work in this repo.
3. `resources/profile.md` — who the client is.
4. `resources/status.md` — what's built and what's next.

Look up as needed: `resources/brief.md` (the original section brief), `resources/decisions.md` (why decisions were made), `resources/mock-data-plan.md` (data schema).

**Don't invent new standards.** If the spec is missing something or seems wrong, propose a change to `resources/design-spec.md` and log it in `resources/decisions.md`. Don't add a rule elsewhere.

## Key files

| Path | Purpose |
|---|---|
| `index.html` | The dashboard page: sticky nav and three `<section>` blocks (KPIs, Drivers, Details). |
| `app.js` | Renderers only. Consumes `window.DATA`; one render function per component. |
| `data.js` | Generated mock data (`window.DATA`). Don't hand-edit. |
| `scripts/generate-data.py` | Deterministic generator for `data.js`, with invariant checks. |
| `server.py` | Flask dev server on port 3000. |
| `resources/screenshots/` | Full-page screenshots at 375/768/1024/1440 in both themes, plus the README hero images. Retake them after a visual change. |
| `archive/` | Superseded planning docs and rules. History only; not binding. |

## Quick start

```bash
pip3 install -r requirements.txt    # one-time (Flask)
python3 server.py                   # http://0.0.0.0:3000
python3 scripts/generate-data.py    # regenerate data.js after changing the generator
```

## Decision log format

Log decisions with lasting consequences in `resources/decisions.md`:

```
### [YYYY-MM-DD] Title
- **Decision**: one line
- **Rationale**: why
- **Alternatives considered**: what we didn't pick and why
- **Status**: Accepted / Superseded by [title]
```
