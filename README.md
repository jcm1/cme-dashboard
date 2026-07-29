# CME KPI Dashboard
Self-contained `index.html` (open anywhere) rebuilt from `data/cme_kpi_data.json` by `update/update_dashboard.py`. Every datapoint carries a source tag (R reported / D derived / E estimate); every mutation logs to `data/audit_log.jsonl`; git history is the audit trail.

## Panel map
Panels run in reading order — number = position, and the canvas/chips ids match (`P7` ↔ `c7` ↔ `chips7`). Renumber only via a full pass over `template.html` (labels, ids, JS block comments, cross-references) or the mapping silently rots.

| § | | |
|---|---|---|
| **1 · The engine** | P1 volume · P2 pricing (RPC) | P3 fee mix · P4 non-transaction revenue |
| **2 · The P&L** | P5 revenue vs expenses vs margin | P6 cost breakdown |
| **3 · The moat** | P7 open interest · P8 rates ADV vs UST issuance | P9 margin savings & customer deposits |
| **4 · The owner's take** | P10 capital returns · P11 price & shareholder yield | P12 valuation (TTM adj P/E) |
| **5 · What would break it** | P13 tripwire strip | |

P11 and P12 each carry a thin dashed *implied-at-last-close* line — yield and multiple recomputed from the banner price (daily close, or live quote when reachable), so they move with the market between quarter-ends.

## Price banner
Three layers, best available wins: embedded last quarterly close → `data/price_live.json` (refreshed each weekday ~5:45pm ET by `.github/workflows/daily-price.yml`, committed by github-actions bot) → true live quote fetched client-side when the page can reach one. Quarter-end closes in `price[]` are reported (Yahoo).

## GitHub Pages setup (once)
1. Create repo (e.g. `cme-dashboard`), copy this folder in, push.
2. Settings → Pages → Deploy from branch → `main` / root. Dashboard lives at `https://<user>.github.io/cme-dashboard/` — always current after each push.

## Monthly ritual (~5 min, ~2nd business day)
`python update/update_dashboard.py add-month --period 2026-07 --adv-total 30.4 --oi rates=xx,equity=xx` → commit & push.
Or in Claude: "update the CME dashboard with the July volume release" — I fetch, validate, run the command, hand back the folder. Cowork scheduled-task text: *"On the 2nd business day monthly: fetch CME's volume release, update cme-dashboard via update_dashboard.py, show me the diff before committing."*

## Quarterly ritual (earnings day + 10-Q)
`add-quarter --period 2026Q3 --rev ... --adj-opex ... --blend ... --rpc ... --buybacks ... --savings ... --perf-bonds ... --opex comp=..,tech=..,prof=..,amort=..,depr=..,other=.. --price 2026-09-30=...` → push. Tripwire chips update via `set --path tripwires...`. (`--opex` feeds P6; licensing & other fees is stored as the exact residual vs `--opex-g`.)
