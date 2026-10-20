# Repo Alignment Survey & Audit

> **Date**: 2026-10-20
> **Purpose**: Full survey of our documentation state, repo alignment, and areas where depth could improve before beginning implementation.
> **Feeds into**: `resources/development-rollout-todo.md` (prioritized to-do list).
> **Method**: Read every file in the workspace; verified claims against `git log`, filesystem, and `server.py`. Guidelines audit performed against external sources (see last section).

---

## 1. What We Have (Inventory)

### Foundational
| Artifact | Status |
|---|---|
| `AGENTS.md` — agent entry point, read-all-first mandate | ✅ Strong |
| `.agents/rules/` — 5 files (core, components, layout, semantic-html, accessibility) | ✅ Strong, but see gaps |
| `resources/profile.md` — client persona (5 platforms, 3 products, 15% commission) | ✅ Strong |
| `resources/dashboard-design.md` — design plan (three-block, palette, typography, nav) | ✅ Strong |
| `memory-bank/` — 5 core files + 12 review files | ✅ Solid & well-reviewed |
| `server.py` — Flask dev server (port 3000) | ✅ Working |
| Git — `main`, 5 commits, clean tree, remote `origin` | ✅ Healthy |

### Verified Facts (cross-checked against filesystem/git)
- **Commits**: 5 on `main` (`git rev-list --count main`); 2 detached agent-host checkpoints not on any branch (total 7). `current-status.md` + `changelog.md` already corrected to say "5 on main" ✅.
- **Line references**: `tech-stack.md` was fixed from 6 stale refs during second-pass review (server.py:37, AGENTS.md:38/39, components.md:58, layout.md:7/28) — current state is accurate ✅.
- **Tailwind/Chart CSS**: both CDN URLs match rule files exactly ✅.
- **`index.html`**: does **not** exist (verified). All implementation remains in planning docs.
- **`server.py`** at 37 lines, serves static from repo root, `debug=True`, `extra_files=['./']` (hot-reload).

---

## 2. Repo Alignment — What's Inconsistent or Under-defined

The docs are in good shape, but several alignment issues would trip up an agent or a human walking in cold:

### 2.1 Rule/docs/persona drift
| Issue | Evidence | Severity |
|---|---|---|
| `components.md` says "no navigation — single page" while `dashboard-design.md` **decided** on a sticky nav with inline anchor links | `.agents/rules/components.md:29` vs `resources/dashboard-design.md` "Recommendation: Approach B" | 🔴 |
| `core-rules.md` says "add a build step if Tailwind compilation is needed", but `tech-stack.md` and `layout.md` firmly enforce **no build step** (CDN only) | `.agents/rules/core-rules.md:26` vs `.agents/rules/layout.md:5-7` | 🟡 |
| `dashboard-design.md` still lists **theme as undecided** (dark vs light both brainstormed) while an implementation needs one | `resources/dashboard-design.md` "Color Palette Brainstorm" | 🟠 |
| `AGENTS.md` names `learn.json` as a "not project-specific" template file; README is still the 4Geeks "HTML Hello" boilerplate | `AGENTS.md:16`, `README.md:1` | 🟡 |
| `.vscode/settings.json` opens all `*.md` in Markdown preview; fine, but section links like `resources/dashboard-design.md` "Recommendation" aren't anchored | — | 🟢 |

### 2.2 Missing artifacts that block comprehension
| Missing | Why It Blocks |
|---|---|
| **No mock data schema or file** — the single most-used input doesn't exist | Everything renders from it; `dashboard-design.md` says "embedded JSON/JS" but that's a decision, not data |
| **No `requirements.txt`** — Flask version unpinned | `tech-stack.md` dependency inventory says "no lockfiles" but notes it as a gap to close |
| No CI / no smoke test | Listed as "not needed" in `current-status.md`; for an agent build, a 3-line `curl`-based check closes the verify-loop |

### 2.3 Scratchpad residue
- `generate-dashboard-guidelines.md`, `generate-profile-insights.md`, and `prompt-memory-bank-generator.md` are **spec/scratchpad** documents that produced artifacts but are still present in the root, and `AGENTS.md`/`project-overview.md` reference `generate-*.md` as "key files". Per `document-plan.md` maintenance rule 5 (archive, don't delete) these could move to `memory-bank/archive/` once they've served their purpose.
- **Archiving these has a ripple effect**: `project-overview.md`, `document-plan.md`, `tech-stack.md`, `AGENTS.md`, and even `current-status.md` reference them as key files — so if we archive them, we must update all referencing files.

---

## 3. Areas Where Depth Is Thin (Improve Before Beginning)

These aren't blockers, but they'd harden the repo before Phase 2/3.

### 3.1 Interaction & motion conventions
- **Missing**: what happens on hover/click for cards, tables, "back to top", nav active-state? `dashboard-design.md` calls for "micro-interactions (hover states, subtle transitions)" but no rule file defines them.
- **Suggest**: a compact `motion-and-states.md` or a section in `components.md` specifying focus-visible rings, hover lift, transition durations, and reduced-motion respect.

### 3.2 Responsive *chart* behavior
- **Missing**: how charts adapt at 375px vs 1024px. `layout.md` handles grids, but Chart CSS charts (bars/columns) on small viewports aren't covered.
- **Suggest**: add a note in `layout.md` or `components.md` — "chart containers keep `aspect-[4/3]` until mobile; allow horizontal scroll on the driver block only when unavoidable."

### 3.3 Formatted number/currency/date conventions
- **Missing**: `$50.00` vs `$50` vs `$7.50`; how to display percents, large numbers, abbreviations. `dashboard-design.md` shows `$12,450` but no rule.
- **Suggest**: a `data-formatting.md` rule — currency with 2 decimals, thousands separators, percents to 1 decimal, "12.4K" abbreviation policy.

### 3.4 Table column/priority definitions
- **Missing**: which columns each table has (products: price, commissions, conversions, ROI per `generate-dashboard-guidelines.md`; platforms: reach, engagement, conversions) and sort semantics.
- **Suggest**: define the three tables' columns + sorting in `components.md` or a `tables.md`.

### 3.5 "How to run the app" is under-specified
- `AGENTS.md` quick-start says `python3 server.py`; nothing documents the run + verify loop, what "the dashboard looks right" means, or screenshot-comparison.
- **Suggest**: add a "Verification" section to `AGENTS.md` (or a `verification.md` rule) — run server, `curl localhost:3000` returns 200, view at 3 breakpoints.

### 3.6 The `.agents/scripts/init.sh` is stale
- Verified: the script still prints `⚠️ Flask not installed` unless Flask is present, and says "memory bank not yet initialized" — it was written before the memory bank existed. It validates a workspace, not the current repo. Needs a refresh to reflect the initialized state.

---

## 4. The Checklist-Recommended Statements (Claim Parity)

| Statement | In Repo? |
|---|---|
| Client persona: multi-platform influencer, 3 products, 15% commission, 5 platforms | ✅ `resources/profile.md` |
| Component: consistent card pattern `bg-white rounded-xl shadow-sm p-4 lg:p-6` | ✅ `resources/dashboard-design.md`, `components.md` |
| Three-block structure: KPIs → Drivers → Details | ✅ `generate-dashboard-guidelines.md` → `dashboard-design.md` |
| Chart CSS only heavy dependency; Tailwind v4 CDN | ✅ `.agents/rules/` |
| Sticky single-page nav with inline anchor links (Approach B) | ✅ Decided in `dashboard-design.md` — **but conflicting text remains in `components.md:29`** |
| Static mock data as embedded JSON/JS; API-ready future | ✅ `dashboard-design.md` "API-ready architecture" 🟢 |
| 5 core questions mirrored in project-overview, profile, dashboard-design | ✅ Consistent |

---

## 5. Guidelines Audit (External Sources)

An audit of industry-standard guidance on agent instruction files and agentic coding workflows, run 2026-10-20.

### 5.1 `AGENTS.md` open standard (agents.md, Agentic AI Foundation / LF)
- AGENTS.md is a **README for agents**: predictable place for build steps, tests, and conventions that would clutter a human README.
- **Keep it short**; every line must earn its place. Over-specified instruction files cause agents to ignore rules.
- Commands the agent can run automatically (test/build/lint) belong in AGENTS.md; verify-loop is a first-class citizen.
- Nested AGENTS.md files are supported; "closest wins" — but we're a single-package project, so one root file is right.

### 5.2 Claude Code best practices (code.claude.com/docs/en/best-practices)
- **"Give Claude a way to verify its work"** — tests, build exit code, linter, or screenshot-comparison. Without a check, "looks done" is the only signal. This is the single highest-leverage practice we can adopt.
- **"Explore first, then plan, then code"** — separate research/planning (plan mode) from implementation. For this repo, that means: maintain the compose-first approach (docs → then implementation), but keep small direct tasks direct.
- **"Provide specific context"** — reference files, mention constraints, point to example patterns.
- **Context is the constraint** — clean sessions between tasks; use subagents for heavy investigation; compact aggressively.
- **Test/lint gate before commit** — every change should pass the check you defined.
- **Adversarial review** — a fresh subagent (or reviewer) that sees only the diff + criteria finds gaps the implementer's bias hides. Writer/Reviewer pattern is recommended.
- **Keep CLAUDE.md concise** — exactly our rule file concern.

### 5.3 Real-world AGENTS.md examples (temporalio/sdk-java, anthropics/claude-code)
- Temporal's AGENTS.md: small, concrete — repo layout, build/test commands, commit message style, **review checklist** ("add new tests", "update docs", "all tests pass"). Exactly the right density.
- Claude Code's own CLAUDE.md: enforces security hardening **as deterministic rules** (allow-list, permission modes) — rules that must always hold.

### 5.4 Synthesis → Instructions for our repo
1. **Add verification-before-commit** to agent rules (the #1 gap vs best practices).
2. **Keep rule files short and concrete** — the 5 current files are already the right size; add only what earns a place.
3. **Require exploring before coding** — read the design docs, confirm with the user before Principle #3, then implement.
4. **Adopt a Writer/Reviewer pattern** — one pass to implement, one fresh-context pass to review against the rules checklist.
5. **Keep context clean** — fresh session per task, use the todo tracking file as the single source of truth.

---

## 6. Summary of Highest-Priority Items

1. **Draft proposed agent rules** (the #1 user-requested item) → `resources/agent-rules-proposal.md`
2. **Reconcile drift** between `.agents/rules/*.md`, `AGENTS.md`, and memory bank.
3. **Define the mock data schema** — the missing backbone.
4. **Decide theme** (or explicitly defer with a default).
5. **Add `requirements.txt`** + a smoke-check command.
6. **Refresh `init.sh`** to reflect the initialized repo.
7. **Define verification loop** (server up, `curl` 200, screenshot at 3 breakpoints).

*All unblocked work is captured in `resources/development-rollout-todo.md`.*