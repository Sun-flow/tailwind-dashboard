# Notes

> **Last updated**: 2026-10-20
> Things learned the hard way. Add to this as soon as you learn something the next session would otherwise rediscover. Keep each note to a line or two, and remove notes that stop being true.

## Working with mae

- mae makes the design calls. When a choice changes what the page shows, offer two or three options with a recommendation instead of picking silently, then log the outcome in `resources/decisions.md`.
- mae wants information shown visually when it can be, with labels carrying the exact numbers. A numbers-only funnel was rejected; reference charts mae shares are the target to match.
- mae often keeps the old view alongside a new one (the per-step funnel charts stayed under the stacked bars). Ask before removing a view mae has seen.
- mae works in more than one environment (Claude Code in the cloud, and GitHub Copilot with DeepSeek in a Codespace). Nothing outside the repo carries over between them, so anything worth keeping goes in this folder or `resources/`.
- Commit messages are plain sentences in the imperative ("Show the sales funnel as 100% stacked bars"), with a short body explaining what and why.

## Domain

- "Revenue" for the creator means **commission**. Sales revenue is what buyers paid the brand and is labelled "Sales Value". ROI is computed on commission.
- Tiny campaigns (Twitch tests with a few dollars of spend) top any raw ROI ranking, so ROI rankings use a minimum spend (`derived.roiMinSpend`).

## Gotchas

- Charts.css: the `cdn.jsdelivr.net/gh/chartscss/...` URL in the archived rules returns 404. Use the npm URL pinned in spec §2.
- Tailwind v4's `dark:` variant only follows the `dark` class because of the `@custom-variant` line in spec §2. Without it, `dark:` follows the OS setting.
- `data.js` is generated: edit `scripts/generate-data.py` and rerun it. The generator is seeded, so the output is identical across runs unless the generator changes.
- After any visual change, run `python3 scripts/screenshots.py` and look at the results before committing them. On 2026-10-20 its output was pixel-identical to the committed screenshots, so a diff in the images means the page changed.
- Claude Code cloud sessions can block `cdn.jsdelivr.net`. `scripts/screenshots.py` then loads the same package versions from the npm registry; if Chromium won't start there, set `PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium`.
- In Claude Code cloud sessions there is no `gh` CLI; GitHub goes through the GitHub MCP tools.
