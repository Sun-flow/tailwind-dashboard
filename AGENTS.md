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

## Project Story

**Why this exists**: Our client — a multi-platform influencer — has income/engagement data scattered across Instagram, YouTube, TikTok, Twitter/X, and Twitch, plus spreadsheets and manual notes. They can't see at a glance how much commission they earn, which products and platforms pay off, or how ads convert.

**Who we're building for**: One influencer persona (see `resources/profile.md`), 3 products (A $50, B $120, C $80), 15% commission. A single reporting dashboard that consolidates it all.

**What success looks like**: A single scrolling page answering 5 core questions — How much am I earning? Which products? How are ads converting? Which platforms return best? What's engagement per platform/product? — readable in ~10 seconds, zero-training, shareable with a manager or sponsor.

**Most important rule** (read first in `.agents/rules/`): **verify your work before claiming "done"** — see `core-rules.md`.

## There Is No Such Thing As A Free Launch

Real work has a cost in effort, context, and time. If a task can be done with less churn — fewer rewrites, fewer throwaway commits, less re-reading — do that. Concretely:

- **Try the simplest correct thing first.** Before reaching for "API-ready", "configurable", "themed", or any future-proofing, ask: does the current task need it? If not, defer it and note the decision.
- **The rules are a floor, not a ceiling.** Reads are cheap; guessing is expensive. Prefer reading the actual file/spec/rule over inventing from memory.
- **A wrong approach abandoned early is success.** If a path isn't working after two attempts, stop and reassess — don't paper over it.
- **Small, focused diffs beat one giant rewrite.** Every commit should be reviewable in a glance.

## Architecture Decision Context (ADC) — Log Format

When a decision has lasting consequences (tech choice, data shape, nav/theme, verification approach), log it as a short entry in `resources/decisions.md`:

```
### [YYYY-MM-DD] Title
- **Decision**: one line
- **Rationale**: why (evidence: file:line where useful)
- **Alternatives considered**: what we didn't pick and why
- **Status**: Accepted / Superseded by [title] / Deferred
```

- One entry per decision. Keep it short — a paragraph of rationale, not an essay.
- Update the entry's `Status` when a decision is superseded. Never delete an entry (archive path: `resources/decisions.md`).