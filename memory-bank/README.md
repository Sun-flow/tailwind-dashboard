# Memory Bank

> **Last updated**: 2026-10-20
> Built from the project-agnostic prompt in `.agents/prompts/memory-bank.md`. That file has the full rules and the reasoning behind them; this one is the short version for this repo.

Agents forget everything between sessions, and the next session may be a different agent or tool in a different environment. These files carry what would otherwise be lost. They are **memory, not standards**: the binding docs are listed below, and this folder points to them instead of copying them.

## Read at the start of every session

1. `context.md`: what the project is, how to run it, and where each kind of fact lives.
2. `status.md`: what works, what's next, open questions.
3. `log.md`: the top three or so entries, to see what the last sessions did and left open.
4. `notes.md`: before anything that touches mae's preferences, the screenshots, or the environment.

Then read the binding docs and code your task needs.

## The files

| File | For | Update when | Budget |
|---|---|---|---|
| `README.md` | This map and the maintenance rules. | A memory file is added, removed or repurposed. | ~120 lines |
| `context.md` | Orientation: purpose, stack, commands, data flow, where facts live. | Scope, stack, commands or doc layout change. | ~100 lines |
| `status.md` | Works / In progress / Next / Open questions / Known problems. | Any session that changes the state of the work. | ~80 lines |
| `log.md` | Session handoffs, newest first. | End of every session that changed something. | ~15 entries, then move the oldest to `archive/memory-bank/log-archive.md` |
| `notes.md` | mae's preferences, environment and tool gotchas, unwritten conventions. | As soon as you learn something the next session would rediscover. | ~100 lines |

## Sources of truth (higher wins)

1. The code: `index.html`, `app.js`, `scripts/generate-data.py` (and the `data.js` it writes), `server.py`.
2. `resources/design-spec.md`: the single binding spec for how the dashboard looks and is built.
3. `resources/decisions.md`: why each decision was made. New decisions go here, not in this folder.
4. `resources/profile.md`, `resources/brief.md`, `resources/mock-data-plan.md`: the client, the original brief, the data schema.
5. This folder.
6. `archive/`: history only, never instructions.

If something here disagrees with a higher source, fix this folder in the same session.

## What must stay in sync with the spec

The memory bank never restates spec values (colours, classes, type sizes, breakpoints, section contents). It refers to spec sections by number, such as "spec §8". So:

- When the spec's **section numbers or titles** change, update every `§` reference here (`grep -rn '§' memory-bank/ AGENTS.md`).
- When a spec change **finishes or adds work**, update `status.md` and add a `log.md` entry.
- When a change needs a **why**, write it in `resources/decisions.md`, and link that entry from the log rather than repeating it.

## How to maintain it

At the end of a session (or before handing work back):

1. Update `status.md`, add a `log.md` entry, and add anything learned to `notes.md`.
2. Update `context.md` if the stack, commands or doc layout changed.
3. Run `python3 scripts/check-memory.py` and fix what it reports.
4. Commit the memory changes with the work they describe.

Rules that keep it useful:

- **Point, don't copy.** Name the file and section that holds a fact. Use paths and sections, never line numbers.
- **Verify before writing.** Mark anything you couldn't check with ❓ and say what would confirm it.
- **Write the why**, date what changes, and stay inside the budgets.
- **No secrets** or private details. Don't repeat what git already records; link the commit or PR.

When mae says "update the memory bank", reconcile every file against the repo, not just the latest change.
