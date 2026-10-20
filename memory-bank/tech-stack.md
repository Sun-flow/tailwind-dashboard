# Tech Stack

> **Date**: 2026-10-19
> **Verified against**: `server.py`, `AGENTS.md`, `learn.json`, `resources/dashboard-design.md`, `.agents/rules/layout.md`

## Languages & Frameworks

| Component | Technology | Version / Source | Notes |
|---|---|---|---|
| Frontend markup | HTML5 | — | Semantic HTML (`<header>`, `<main>`, `<section>`, etc.) |
| Frontend styling | Tailwind CSS v4 | CDN via `<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4">` | No build step; no custom CSS beyond Tailwind utilities |
| Frontend logic | Vanilla JavaScript | ES6+ | No frameworks (React, Vue, etc.) |
| Charting | Chart CSS | CDN via `<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/chartscss/chart.css@v1/dist/chart.css">` | CSS-only charts; column, bar, line classes |
| Backend server | Python / Flask | Flask (latest PyPI) | Dev server only; serves static files |

**Pinned dependencies**: None beyond Flask (see `server.py:1-4`). No `requirements.txt` or `package.json` exists.

## Tooling & Configuration

| Tool | Purpose | Verified location |
|---|---|---|
| Flask | Development web server (port 3000) | `server.py:37` — `app.run(host='0.0.0.0',port=3000, debug=True)` |
| Tailwind CSS v4 CDN | Utility-first CSS framework | `.agents/rules/layout.md:7` |
| Chart CSS v1 CDN | CSS-based chart visualizations | `.agents/rules/components.md:58` |
| VS Code | Primary editor | `.vscode/settings.json` exists |

## CI / Workflows

No CI configuration exists yet. No GitHub Actions workflows, no Dockerfiles.

## Environment & Configuration

No environment variables or `.env` files exist. The Flask server runs with `debug=True` on `0.0.0.0:3000` (`server.py:37`).

## Canonical Commands

| Command | Purpose | Verified |
|---|---|---|
| `pip3 install flask` | One-time dependency install | `AGENTS.md:38` |
| `python3 server.py` | Start dev server at http://0.0.0.0:3000 | `AGENTS.md:39` |

## Dependency Inventory

| Dependency | Type | Evidence |
|---|---|---|
| Flask | Runtime (Python) | `server.py:2-3` — `from flask import Flask` |
| Tailwind CSS v4 CDN | Frontend (CDN) | `.agents/rules/layout.md:7` |
| Chart CSS v1 CDN | Frontend (CDN) | `.agents/rules/components.md:58` |

No lockfiles (`package-lock.json`, `yarn.lock`, `Pipfile.lock`) exist. No `requirements.txt` exists.

## Tech Constraints

- **No build step**: Tailwind v4 is used via CDN/browser script, not the CLI/postcss pipeline.
- **No other CSS frameworks**: Chart CSS is the only allowed exception (`.agents/rules/layout.md:8`).
- **No pixel-based sizes**: Relative units only (`w-full`, `w-1/2`, Tailwind spacing) — `.agents/rules/layout.md:26`.
- **Touch targets**: All interactive elements ≥44×44px — `.agents/rules/layout.md:28`.