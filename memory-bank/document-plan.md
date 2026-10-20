# Document Plan — File Inventory & Maintenance Rules

> **Date**: 2026-10-19
> **Purpose**: Index/hub file — inventory of every memory-bank, docs, rules, and resource file.

---

## Memory Bank Core Files

| File | Purpose | Last Updated |
|---|---|---|
| `memory-bank/project-overview.md` | What this project is (goals, scope, boundaries, DoD, architecture, key files) | 2026-10-19 |
| `memory-bank/tech-stack.md` | Languages, frameworks, deps, tooling, CI, commands, constraints | 2026-10-19 |
| `memory-bank/current-status.md` | What works, gaps/blockers, next priorities, session history | 2026-10-19 |
| `memory-bank/document-plan.md` | **🔵 You are here** — file inventory and maintenance rules | 2026-10-19 |
| `memory-bank/changelog.md` | Human-readable change history (Keep-a-Changelog format) | 2026-10-19 |

## Root Files

| Path | Purpose | Referenced by |
|---|---|---|
| `AGENTS.md` | Agent entry point — read first every session | All agents |
| `server.py` | Flask dev server (port 3000) | `tech-stack.md` |
| `learn.json` | 4Geeks Academy template metadata (not project-specific) | — |
| `prompt-memory-bank-generator.md` | Spec for initializing this memory bank | `AGENTS.md` |
| `generate-dashboard-guidelines.md` | Scratchpad → produced `resources/dashboard-design.md` | `project-overview.md` |
| `generate-profile-insights.md` | Scratchpad → produced `resources/profile.md` | `project-overview.md` |
| `README.md` | Human-facing project boilerplate (4Geeks Academy template) | — |
| `README.cn.md` | Chinese translation of README | — |
| `README.es.md` | Spanish translation of README | — |

## Agent Rules

| Path | Purpose | Referenced by |
|---|---|---|
| `.agents/rules/core-rules.md` | General conduct, read-at-start mandate, project-specific rules | `AGENTS.md` |
| `.agents/rules/components.md` | Reusable component patterns, section structure, Chart CSS | `core-rules.md` |
| `.agents/rules/layout.md` | Tailwind CSS v4 CDN usage, mobile-first design, breakpoints | `core-rules.md` |
| `.agents/rules/semantic-html.md` | Semantic element usage rules | `core-rules.md` |
| `.agents/rules/accessibility.md` | a11y best practices (aria, alt text, keyboard nav) | `core-rules.md` |
| `.agents/scripts/init.sh` | Agent utility script | — |

## Resources

| Path | Purpose | Referenced by |
|---|---|---|
| `resources/profile.md` | Client persona — influencer, platforms, products, goals | `AGENTS.md`, `core-rules.md` |
| `resources/dashboard-design.md` | Design plan — layout, color palette, typography, components | `project-overview.md` |
| `resources/development-rollout-todo.md` | **NEW (2026-10-20)** — prioritized implementation to-do list | `current-status.md` |
| `resources/repo-alignment-audit.md` | **NEW (2026-10-20)** — docs survey, repo alignment, guidelines audit | `current-status.md` |
| `resources/agent-rules-proposal.md` | **NEW (2026-10-20)** — draft agent rules proposal | `current-status.md` |
| `resources/decisions.md` | **NEW (2026-10-20)** — ADC log (theme, data.js, nav, verification) | `current-status.md` |

## Review & Validation Files

*(Created during cross-validation passes)*

| Path | Purpose |
|---|---|
| `memory-bank/review-edits/fact-checker-review.md` | Fact-checker review findings (first validation pass) |
| `memory-bank/review-edits/consistency-checker-review.md` | Consistency-checker review findings (first validation pass) |
| `memory-bank/review-edits/project-overview--luna-review.md` | Luna review of project-overview.md (second pass) |
| `memory-bank/review-edits/project-overview--sol-review.md` | Sol review of project-overview.md (second pass) |
| `memory-bank/review-edits/tech-stack--luna-review.md` | Luna review of tech-stack.md (second pass) |
| `memory-bank/review-edits/tech-stack--sol-review.md` | Sol review of tech-stack.md (second pass) |
| `memory-bank/review-edits/current-status--luna-review.md` | Luna review of current-status.md (second pass) |
| `memory-bank/review-edits/current-status--sol-review.md` | Sol review of current-status.md (second pass) |
| `memory-bank/review-edits/document-plan--luna-review.md` | Luna review of document-plan.md (second pass) |
| `memory-bank/review-edits/document-plan--sol-review.md` | Sol review of document-plan.md (second pass) |
| `memory-bank/review-edits/changelog--luna-review.md` | Luna review of changelog.md (second pass) |
| `memory-bank/review-edits/changelog--sol-review.md` | Sol review of changelog.md (second pass) |
| `memory-bank/review-edits/changelog--luna-review.md` | Luna review of changelog.md (second pass) |
| `memory-bank/review-edits/changelog--sol-review.md` | Sol review of changelog.md (second pass) |

## Archive

*(Superseded content, never deleted)*

| Path | Original Location | Superseded By |
|---|---|---|
| *(none yet)* | | |

---

## Maintenance Rules

1. **Single source of truth**: Each fact lives in exactly one file. Other files link (→ `file.md`) rather than duplicating.
2. **Update on triggers**: After (a) new project patterns discovered, (b) significant changes implemented, (c) blocker/status change, (d) direction changes, (e) user says "update memory bank".
3. **Evidence-only**: Every claim traces to a real file, manifest, or command output. ❓ marks unverified claims.
4. **Date everything**: ISO-8601 date on every entry/snapshot.
5. **Archive, don't delete**: Superseded content → `memory-bank/archive/` with a linking note.
6. **One topic per file**: If a file straddles two concerns, split it and update this inventory.
7. **Keep it lint-able**: Valid cross-file links, canonical headings, no trailing duplicate headings.
8. **Agent-facing**: Memory bank files are for agents; keep them out of human README; keep agent operational noise out of human docs.
9. **Ten-second orientation**: Fresh agent reads `document-plan.md` → `project-overview.md` → `current-status.md` → `changelog.md` to know the project in seconds.

### When Adding a File

1. Add its row to the appropriate table above.
2. Update `project-overview.md` key files table if the file is significant.
3. If superseding an existing file, archive the old one and note the replacement.

### When Removing a File

1. Archive it (don't delete) — move to `memory-bank/archive/`.
2. Remove its row from the inventory table.
3. Add an archive entry noting the replacement.
4. Update `project-overview.md` if needed.