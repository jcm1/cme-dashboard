# CME KPI Dashboard
Self-contained `index.html` (open anywhere) rebuilt from `data/cme_kpi_data.json` by `update/update_dashboard.py`. Every datapoint carries a source tag (R reported / D derived / E estimate); every mutation logs to `data/audit_log.jsonl`; git history is the audit trail.

## GitHub Pages setup (once)
1. Create repo (e.g. `cme-dashboard`), copy this folder in, push.
2. Settings → Pages → Deploy from branch → `main` / root. Dashboard lives at `https://<user>.github.io/cme-dashboard/` — always current after each push.

## Monthly ritual (~5 min, ~2nd business day)
`python update/update_dashboard.py add-month --period 2026-07 --adv-total 30.4 --oi rates=xx,equity=xx` → commit & push.
Or in Claude: "update the CME dashboard with the July volume release" — I fetch, validate, run the command, hand back the folder. Cowork scheduled-task text: *"On the 2nd business day monthly: fetch CME's volume release, update cme-dashboard via update_dashboard.py, show me the diff before committing."*

## Quarterly ritual (earnings day + 10-Q)
`add-quarter --period 2026Q3 --rev ... --adj-opex ... --blend ... --rpc ... --buybacks ... --savings ... --perf-bonds ... --price 2026-09-30=...` → push. Tripwire chips update via `set --path tripwires...`.
