# Status

> **Last updated**: 2026-10-20

## Works

- The whole page, complete against `resources/design-spec.md` §8: sticky nav with a dark/light toggle, four KPI cards, the Drivers block (sales funnel as 100% stacked bars with per-step charts and a step-rate table, commission share by platform, performance by product, activity and engagement by platform) and the Details block (alerts, improvement opportunities, platform / product / campaign tables with alert markers, top performers by commission and by return).
- `data.js` from `scripts/generate-data.py` (seed 20261020, schema v1.0); all invariant checks pass. ROI is (commission − spend) ÷ spend.
- Checked at 375, 768, 1024 and 1440px in both themes: no console errors, no horizontal page scroll. axe-core (WCAG 2 A/AA and best practice) reports no violations at 375 and 1440px in both themes; keyboard focus is visible throughout.
- Repo presentable: project README with hero screenshots, template leftovers removed, `requirements.txt` added.
- Memory bank revived as this folder, with a project-agnostic prompt in `.agents/prompts/memory-bank.md`.

## In progress

- Nothing.

## Next

1. Optional: monthly trend sparklines from `monthlySeries` (the data exists; nothing renders it yet).
2. Optional: a zoomed bar of clicks only in the funnel, so the bought / clicked split is easier to see (see the "Sales funnel as 100% stacked bars" decision).

## Open questions

- None.

## Known problems

- None known. The page needs an internet connection because both libraries load from the CDN.
