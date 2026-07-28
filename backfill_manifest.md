# Backfill manifest — gaps the updater is ready to fill
1. **By-line ADV & RPC quarterly, 2016–2025** — from CME quarterly earnings releases (RPC table). Unlocks the stacked by-line views in P1/P2. `add-quarter --period 2021Q1 --rpc rates=0.46,... --adv rates=12.1,...`
2. **Quarterly prices pre-2024** — fastest: Bloomberg `BDH CME US Equity PX_LAST` quarterly export, paste via `set`. Upgrades P6's yield line to quarterly.
3. **OI by asset class** — starts with the next monthly volume release (`add-month --oi ...`); no clean historical seed attempted.
4. **GAAP opex 2025Q3–2026Q2** — from 10-Qs as filed (Q2'26 10-Q ~Aug 6).
5. **Adjusted expenses quarterly pre-2026** — from release reconciliation tables.
6. **Verify flags**: FY16–20 & FY23–24 total ADV [E]; pre-2021 regular / pre-2020 variable dividend rates [E]; FY25 buyback quarterly split (placed Q4); **Q1'26 GAAP revenue: release-derived $1,754M vs aggregator $1,880M — resolve at 10-Q**.
