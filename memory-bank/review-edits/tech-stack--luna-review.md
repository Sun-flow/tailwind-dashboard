# Review: tech-stack.md (GPT-6 Luna)

**Verdict**: PASS ✅ (with 🟢 nits)
**Date**: 2026-10-19

## Inaccuracies Found

| Claim | Line | Evidence | Severity |
|---|---|---|---|
| None — all factual claims verified | — | See below | ✅ |

## Verified Accurate Claims

| Claim | Evidence | Verdict |
|---|---|---|
| "Frontend markup: HTML5" — semantic HTML | `.agents/rules/semantic-html.md` — explicitly mandates `<header>`, `<main>`, `<section>`, etc. | ✅ |
| "Tailwind CSS v4 CDN: `<script src=\"https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4\">`" | `.agents/rules/layout.md:7` — exact URL match | ✅ |
| No build step | `.agents/rules/layout.md:5-7` — CDN only, no CLI/postcss | ✅ |
| "Chart CSS: CDN via `<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/gh/chartscss/chart.css@v1/dist/chart.css\">`" | `.agents/rules/components.md:58` — exact URL match | ✅ |
| "Backend server: Python / Flask" | `server.py:2-4` — `from flask import Flask` | ✅ |
| "No `requirements.txt` or `package.json`" | `test -f requirements.txt` → MISSING; `test -f package.json` → MISSING | ✅ |
| Flask at `server.py:37` | `sed -n '37p' server.py` → `app.run(host='0.0.0.0',port=3000, debug=True, extra_files=['./',])` | ✅ |
| Tailwind CSS v4 CDN at `.agents/rules/layout.md:7` | `sed -n '7p' .agents/rules/layout.md` → Tailwind v4 CDN script tag | ✅ |
| Chart CSS v1 CDN at `.agents/rules/components.md:58` | `sed -n '58p' .agents/rules/components.md` → Chart CSS stylesheet URL | ✅ |
| VS Code at `.vscode/settings.json` | `test -f .vscode/settings.json` → EXISTS | ✅ |
| No CI, no GitHub Actions workflows, no Dockerfiles | `ls .github/workflows/ 2>&1` → not found; `test -f Dockerfile` → MISSING | ✅ |
| No `.env` file | `test -f .env` → MISSING | ✅ |
| `pip3 install flask` at `AGENTS.md:38` | `sed -n '38p' AGENTS.md` → `pip3 install flask          # one-time` | ✅ |
| `python3 server.py` at `AGENTS.md:39` | `sed -n '39p' AGENTS.md` → `python3 server.py           # starts dev server at http://0.0.0.0:3000` | ✅ |
| No lockfiles (package-lock.json, yarn.lock, Pipfile.lock) | All three `ls` → "No such file or directory" | ✅ |
| "No build step" constraint | `.agents/rules/layout.md:5-7` — CDN only; no CLI config | ✅ |
| Chart CSS is only allowed exception at `layout.md:8` | `sed -n '8p' .agents/rules/layout.md` → "Chart CSS is the only allowed CSS visualization library" | ✅ |
| No pixel-based sizes at `layout.md:26` | `sed -n '26p' .agents/rules/layout.md` → "Avoid pixel-based sizes" | ✅ |
| Touch targets at `layout.md:28` | `sed -n '28p' .agents/rules/layout.md` → "≥44×44px" rule | ✅ |

## Summary

All substantive claims in `tech-stack.md` are verified accurate. Every file-path evidence citation points to the correct line in the actual file. The CDN URLs match exactly. The dependency, lockfile, and CI claims are correct.

**Recommendations**: No blocking or should-fix issues found. Two 🟢 observations for consideration:
- The Dependency Inventory table has a missing `Type` column for two rows (Tailwind, Chart CSS) — cosmetic.
- `resources/dashboard-design.md` is listed in the "Verified against" header but never cited in the body — consider removing from header or adding a citation.