# Backfill manifest — remaining gaps

*Updated 2026-07-27 after the two IR-scrape workflows (see `audit_log.jsonl` actions `backfill-ir-scrape` / `-2`). Resolved and removed: by-line ADV & RPC quarterly 2016→2026Q2 (verified vs SEC filings); quarterly prices 2016→ (Yahoo closes R); GAAP opex 2025Q3–2026Q2 (10-Qs); adjusted expenses 2023Q1→ (release reconciliations); FY16–24 total-ADV [E] flags; Q1'26 revenue discrepancy (resolved: $1,880.1M per 10-Q); revenue breakdown + adjusted EPS 2016→ (42 qtrs); OI by class quarter-ends 2022Q4→.*

*2026-07-28, EDGAR XBRL backfill (actions `backfill-edgar-*`): performance bonds quarterly 2016Q1→2026Q2 (42 pts, replaces 3-pt series; the 2023Q4 ≈$90B [E] resolved to $90.2B R); opex breakdown 2016Q1→2026Q2 (P13 — comp/tech/prof/amort/depr R-tagged, licensing & other fees = exact residual vs total, every row cross-checked against `quarterly_fin.opex_g`; 2016Q4+2017Q4 flagged `lic-includes-other` for FY presentation drift, 2016Q4 XBRL total differs from the macrotrends backfill by $2.2M — XBRL kept).*

1. **OI by asset class, 2025Q2–Q4** — CME's releases for those periods carry ADV only; period-end OI not disclosed. Series runs 2022Q4→2026Q2 with that hole; monthly points append via `add-month --oi`.
2. **Adjusted expenses pre-2023** — CME published no adjusted-expenses subtotal before 2023; P3 approximates as GAAP less amortization/4 (D). By design, not fillable.
3. **Pre-2021 regular / pre-2020 variable dividend rates [E]** — verify against CME's dividend history page or old 10-Ks.
4. **FY25 buyback quarterly split** — full-year figure placed in Q4; refine if disclosed.
