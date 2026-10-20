# Consistency-Checker Review

**Verdict**: FAIL ⚠️
**Date**: 2026-10-19

## Summary

7 issues found (3 🔴 blocking, 3 🟡 should-fix, 1 🟢 nit). The memory bank is structurally sound but contains several stale references and one superseded claim that must be resolved before it can be considered fully consistent.

---

## Findings

| Issue | Location | Description | Severity |
|---|---|---|---|
| 1 | `.agents/rules/core-rules.md:20` | **Superseded claim**: States "Memory bank not yet initialized" — but `memory-bank/` now exists with all 5 core files. Also references file `memory-bank-generator-prompt.md` which does not exist on disk (actual name: `prompt-memory-bank-generator.md`). This contradicts `AGENTS.md:3` ("The memory bank is initialized and active"). | 🔴 |
| 2 | `memory-bank/tech-stack.md:22` | **Stale line reference**: Cites `.agents/rules/layout.md:5` for Tailwind CSS v4 CDN, but `layout.md:5` is the heading `## Tailwind CSS`, not the CDN statement (which is at `layout.md:7`). | 🔴 |
| 3 | `memory-bank/tech-stack.md:23` | **Stale line reference**: Cites `.agents/rules/components.md:25` for Chart CSS v1 CDN, but `components.md:25` is ASCII art (`│  content (cards, chart, table)   │`), not the Chart CSS reference (which is at `components.md:58`). | 🔴 |
| 4 | `memory-bank/tech-stack.md:32` | **Stale line reference**: Cites `server.py:48` for `app.run(...)`, but `server.py` has only 37 lines. The actual `app.run()` is at `server.py:37`. | 🔴 |
| 5 | `memory-bank/tech-stack.md:41` | **Stale line reference**: Cites `AGENTS.md:28` for `pip3 install flask` and `AGENTS.md:29` for `python3 server.py`, but the actual commands are at `AGENTS.md:38` and `AGENTS.md:39`. | 🟡 |
| 6 | `AGENTS.md:21` | **Dangling file reference**: Lists `memory-bank-generator-prompt.md` in the key files table, but the actual file on disk is `prompt-memory-bank-generator.md`. The same wrong filename is also referenced in `.agents/rules/core-rules.md:20`. | 🔴 |
| 7 | `.agents/rules/core-rules.md:18` vs `memory-bank/document-plan.md:63` | **Contradictory archive rules**: `core-rules.md:18` says superseded content goes to `.agents/rules/archive/`, but `document-plan.md:63` (maintenance rule #5) says it goes to `memory-bank/archive/`. These conflict. `.agents/rules/archive/` does not exist on disk. | 🔴 |
| 8 | `memory-bank/document-plan.md:45` | **Stale inventory**: States "(none yet — first validation pass in progress)" for review/validation files, but `memory-bank/review-edits/fact-checker-review.md` already exists on disk. | 🟡 |
| 9 | `memory-bank/project-overview.md:9` vs single-source-of-truth rule | **Minor duplication**: `project-overview.md` lists all 5 platform names inline ("Instagram, YouTube, TikTok, Twitter/X, Twitch") rather than linking to `resources/profile.md` where the platforms definition lives. The same list also appears verbatim in `.agents/rules/core-rules.md:28`. Maintenance rule #1 in `document-plan.md` says "each fact lives in exactly one file; others link." | 🟡 |
| 10 | `memory-bank/current-status.md:35` | **Fact references `project-overview.md` which itself duplicates platforms**: The cross-file links to `project-overview.md` and `resources/profile.md` are otherwise valid, but the chain of platform-fact references ultimately traces back to three separate locations. | 🟢 |

---

## Detailed Breakdown by Check Type

### 1. Cross-File Agreement ✅ (mostly)

Core numeric claims ("5 platforms", "3 products", "15% commission") are consistent across all files that mention them:

| Claim | Files Agree? |
|---|---|
| 5 platforms (Instagram, YouTube, TikTok, Twitter/X, Twitch) | ✅ Consistent across `project-overview.md`, `profile.md`, `dashboard-design.md`, `core-rules.md` |
| 3 products (A: $50, B: $120, C: $80) | ✅ Consistent across `project-overview.md`, `profile.md`, `dashboard-design.md`, `core-rules.md` |
| 15% commission | ✅ Consistent across `project-overview.md`, `profile.md`, `dashboard-design.md`, `core-rules.md` |

Date stamps (2026-10-19) are present and plausible on all files. ✅

### 2. Dangling References ❌

- **`memory-bank-generator-prompt.md`** referenced in `AGENTS.md:21` and `.agents/rules/core-rules.md:20` does **not exist**. The actual file is `prompt-memory-bank-generator.md`. (🔴)
- All other relative paths (`AGENTS.md`, `.agents/rules/`, `resources/profile.md`, `server.py`, etc.) resolve correctly. ✅

### 3. Freshness ❌

- **`.agents/rules/core-rules.md:20`** contains the superseded claim "Memory bank not yet initialized" that is contradicted by `AGENTS.md:3` ("is initialized and active"). (🔴)
- **`memory-bank/tech-stack.md` line references** are stale — they point to wrong line numbers in `layout.md`, `components.md`, `server.py`, and `AGENTS.md`. (🔴/🟡)

### 4. Document-Plan Accuracy ❌

| Item | Status |
|---|---|
| Lists all 5 core memory-bank files | ✅ |
| Lists root files (AGENTS.md, server.py, etc.) | ✅ |
| Lists agent rules files (5 `.agents/rules/*.md`) | ✅ |
| Lists `.agents/scripts/init.sh` | ✅ (file exists on disk) |
| Lists review files as empty ("none yet") | ❌ — `fact-checker-review.md` already exists in `review-edits/` (🟡) |

### 5. AGENTS.md Alignment ⚠️

- `AGENTS.md` correctly states "The memory bank (`memory-bank/`) is initialized and active." ✅
- `AGENTS.md` correctly instructs agents to read all files in `memory-bank/`. ✅
- **But** `AGENTS.md` references the generator prompt file by the wrong filename (`memory-bank-generator-prompt.md` instead of `prompt-memory-bank-generator.md`). (🔴)

### 6. Duplicate Facts ⚠️

- The list of 5 platforms appears inline in **three** separate files: `project-overview.md:9`, `.agents/rules/core-rules.md:28`, and `resources/profile.md`. Per single-source-of-truth rules, this should live in `resources/profile.md` alone with other files linking to it. (🟡)

### 7. Link Validity ❌

| Link | Cited In | Actual Location | Valid? |
|---|---|---|---|
| `.agents/rules/layout.md:5` | `tech-stack.md:22` | `layout.md:7` (line 5 is a heading) | ❌ |
| `.agents/rules/components.md:25` | `tech-stack.md:23` | `components.md:58` (line 25 is ASCII art) | ❌ |
| `server.py:48` | `tech-stack.md:32` | File has only 37 lines; app.run at line 37 | ❌ |
| `AGENTS.md:28` | `tech-stack.md:41` | Commands at lines 38–39 | ❌ |
| `AGENTS.md:29` | `tech-stack.md:41` | Commands at lines 38–39 | ❌ |
| `server.py:2-3` | `tech-stack.md:14` | Lines 2–3 are `from flask import Flask` / `from flask import send_from_directory` | ✅ |
| `.vscode/settings.json` | `tech-stack.md:37` | File exists | ✅ |

---

## Verdict Notes

The most critical issues are: (1) the superseded "not yet initialized" claim in `core-rules.md`, (2) five stale/stale line references in `tech-stack.md`, and (3) the dangling reference to a non-existent filename (`memory-bank-generator-prompt.md`). Until these are resolved, agents reading the memory bank will encounter conflicting signals about the project state and may be unable to verify claims against the correct source lines.