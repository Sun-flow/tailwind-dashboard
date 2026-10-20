# Session Log

> **Last updated**: 2026-10-20
> Newest first. One entry per session: date, where it ran, what changed (link the PR or commit), what was left open. Keep about 15 entries. When there are more, move the oldest to `archive/memory-bank/log-archive.md` (create it the first time). Entries before this file existed were rebuilt from git history.

### 2026-10-20 · Memory bank hardening (Claude Code, cloud)
- `scripts/check-memory.py` now checks `§` references against the spec and lists commits made after the last memory update. Added `scripts/screenshots.py` (+ `requirements-dev.txt`) and the Copilot pointer `.github/copilot-instructions.md`. "In progress" items now name branch, PR and environment. `AGENTS.md`'s file table lists only code, and the docs map lives in `context.md`. A cold read by a fresh agent found and fixed some duplicated instructions.
- Open: nothing.

### 2026-10-20 · Memory bank revived (Claude Code, cloud)
- Revived `memory-bank/` as five files (`README`, `context`, `status`, `log`, `notes`) and wrote a project-agnostic prompt to create and maintain one, `.agents/prompts/memory-bank.md`, which supersedes `archive/prompt-memory-bank-generator.md`. Moved the status file here from `resources/` as `status.md`. Added `CLAUDE.md` (points at `AGENTS.md`) and `scripts/check-memory.py`.
- Why: decision "Memory bank revived as lean agent memory" in `resources/decisions.md`.
- Open: nothing.

### 2026-10-20 · ROI on commission (Claude Code, cloud)
- ROI is now (commission − spend) ÷ spend; sales revenue is labelled "Sales Value". Commit `3587c7d`, in PR #3.
- Open: nothing.

### 2026-10-20 · Repo cleanup for presentation (Claude Code, cloud)
- New README with hero screenshots, 4Geeks template files removed, `requirements.txt` and `.gitignore` added, status file moved to `resources/`. PR #3.
- Open: nothing.

### 2026-10-20 · Drivers and Details (Claude Code, cloud)
- Built the Drivers and Details blocks; the funnel went from linear bars to 100% stacked bars at mae's request; added "Campaigns by return" with a median minimum spend. PR #2.
- Open: sparklines and a clicks-only funnel zoom are optional next steps (`status.md`).

### 2026-10-20 · One design spec (Claude Code, cloud)
- Unified the contradictory design docs and rules into `resources/design-spec.md`; moved the old docs, rules and the first memory bank to `archive/`. PR #1.
- Open: nothing.

### 2026-10-20 · First build (agent outside this environment)
- Finalised the agent rules, wrote the mock data plan and generator, generated `data.js`, and scaffolded `index.html` + `app.js`. Commits `a41a541` to `46da041`.

### 2026-10-19 · Planning and first memory bank (agent outside this environment)
- Added `AGENTS.md`, `.agents/rules/`, the client profile and the design plan; generated the first memory bank with two reviewer passes. Commits `50c438e` to `270997d`. All now in `archive/`.
