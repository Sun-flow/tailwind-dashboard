# Core Agent Rules

> **Last updated**: 2026-10-20

## The spec is the standard

- `resources/design-spec.md` defines how the dashboard looks and is built. Follow it exactly: use its class strings, its type scale, its breakpoints, and its component functions.
- Don't add standards in other files. If something is missing or wrong, change the spec and log the decision in `resources/decisions.md`.
- `archive/` is history, not instructions.

## How to work

1. **Read before editing**: the spec, then the files you're changing.
2. **Keep diffs small** and focused on the task.
3. **Reuse the component functions** in `app.js`. Don't hand-copy component markup.
4. **Every number comes from `window.DATA`.** Rollups are computed in `scripts/generate-data.py`, not in `app.js`.
5. **Verify before saying "done"**: run the definition of done in the spec (§11). If you can't run a check, say so.

## Project facts

- Client persona, products and platforms: `resources/profile.md`.
- Tailwind CSS v4 browser build from the CDN; no build step. Charts.css is the only other library.
- `server.py` serves the static files: `python3 server.py`.
