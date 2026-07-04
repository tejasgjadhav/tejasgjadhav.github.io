---
title: BUY strategies tested on real 5-min data 2019→date (Zerodha Kite)
type: synthesis
tags: [trading, intraday, backtest, out-of-sample, zerodha, real-data]
created: 2026-07-04
updated: 2026-07-04
sources: [~/files/institutional-trader/studies/BUY_STRATEGIES_2019_REALTEST.md]
---

The multi-year, all-regime test of the two **intraday BUY** strategies in [[institutional-trader]]
(see [[trading-strategies]]). The fades reached 2019 on daily bhavcopy closes; the BUY strategies are
intraday, and Upstox only holds 5-min data ~1–2 years. **[[zerodha-kite]]'s historical API returns
5-min bars back to 2019** — so this is the first real-data test of the BUY edges across every regime.

**What's measurable.** Kite gives real 5-min *underlying* bars 2019→date. Intraday *option premiums*
for expired contracts exist nowhere historically, so — like the 365-day underlying study — this
measures the real **directional edge on the underlying** (signal→close move), NOT option P&L.

## 3-Family — FULL gate stack (driven by the actual production code)
Ran `compute_all_families` + `is_orb_confirmed` on the Kite bars with the real gates: Gate 1
(alpha-z > 0.55 + ≥2 families), Gate 2 (ORB break + 1.2× volume surge), Gate 3 (market alignment).
100/100 stocks, 19,454 signals:

| Year | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | ALL |
|---|---|---|---|---|---|---|---|---|---|
| Hit% | 53.3 | 51.3 | 46.2 | 52.6 | 49.3 | 48.5 | 53.4 | 49.9 | **50.6** |
| Avg move% | +.236 | +.117 | +.017 | +.135 | +.140 | +.056 | +.079 | +.033 | **+.107** |

**The gates are real, and this is fairer than "overfit."** A no-gate proxy (ORB+trend+alignment) is
a 48% coin flip; adding the real alpha-z + volume-surge gates lifts it to **50.6% hit, +0.107%/trade,
positive in EVERY year 2019→2026** — a small but genuinely durable directional edge (matches the
365-day study's +0.13% and extends it to 8 years). **But a direction edge ≠ a profitable strategy:**
+0.107% is the underlying move; options leverage it ~10× yet theta/IV/bid-ask/−15% stops/Gate-6
liquidity eat it → the engine's real-option 1-year test was **−1.0% net (55% win)**.

## ORB+VWAP — real signal on Kite 5-min, trend-ride on the underlying
2,303 signals: **NIFTY 42% hit / +0.031%/trade, BANKNIFTY 36% / +0.049%, BOTH 39% / +0.040%.**
Negative in ~2 of 8 years per index (NIFTY 2020/2026; BANKNIFTY 2023/2025). Thin and inconsistent —
weaker than the +0.9%/18mo window implied; options leverage it but costs eat it ("+0.8% gross → ~0%
net").

## Bottom line
| | Signals | Hit | Avg move | Consistency | Net (option-buying) |
|---|---|---|---|---|---|
| 3-Family (full gates) | 19,454 | 50.6% | +0.107% | +ve every year | −1.0% (real-option yr) |
| ORB+VWAP | 2,303 | 39% | +0.040% | −ve ~2/8 yrs | ~0% net |

Neither BUY strategy is "overfit noise" — 3-Family's direction edge is durable and beats ORB+VWAP's
— but **neither survives option-buying costs net.** Both remain paper forward-tests. Contrast with
the credit-spread verdicts in [[real-data-fade-validation]] (gated stock fade = the one net edge).
