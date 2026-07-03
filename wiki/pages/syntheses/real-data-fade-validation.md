---
title: Real-premium validation of the fade credit spreads (bhavcopy + Upstox OOS)
type: synthesis
tags: [trading, options, backtest, out-of-sample, real-data]
created: 2026-07-03
updated: 2026-07-03
sources: [~/files/institutional-trader/studies/STOCK_OPTIONS_NO_EDGE.md (Parts 10–11), ~/files/institutional-trader/CLAUDE.md]
---

The decisive real-data test of the two fade credit-spread strategies in [[institutional-trader]]
(see [[trading-strategies]]). Question: are the fade edges — validated only on the recent
Oct'24→date window — durable, or regime artifacts? Answered by pulling **real** option premiums
back to 2019 from [[nse-bhavcopy]] (the source no broker API exposes) and re-running the deployed
geometry with a clean method (OI filter, expiry settled via underlying intrinsic, 2× stop, P&L as
net % of width — lot-independent).

## Result 1 — Stock fade credit spread: durable edge CONFIRMED (but modest)

Real bhavcopy, cleaned, 2019→Sep'24:

| Config | Trades | Win% | Net % of width |
|---|---|---|---|
| Index fade (NIFTY, no gate) | 181 | 54% | −1.4% |
| Stock fade — **ungated** | 6,844 | 56% | −1.1% |
| Stock fade — **GATED** (credit/width ≥ 0.40, prem ≥ ₹50) | 718 | 54% | **+5.3%** |

Gated stock fade by year: 2019 +22.7 · 2020 +0.4 · 2021 +3.0 · 2022 +13.4 · 2023 −4.5 · 2024 +1.1.
**The credit/width gate IS the edge and it survives out-of-time** (positive 5 of 6 years). Strip
it and stocks lose like everything else. Real edge is **~⅓–½ of the optimistic recent-window
backtest** (+16–25% → +5.3% of width; 65% → 54% win) — durable but modest, high variance.

## Result 2 — Index fade: NOT durable; a gate salvage FAILED out-of-sample

Real bhavcopy NIFTY index fade is **net −1.4%** over 2019→Sep'24, positive only in 2019 & 2024
(favorable regimes). A winner/loser analysis found two gates that looked like a fix **in-sample**:

- **Direction:** CE (fade UP-breaks) lost −5.0% (48% win); PE (fade DOWN-breaks) won +6.6% (65%).
  Attributed to the index's "upward drift."
- **Flush:** among down-breaks, requiring close ≥0.5% beyond the band → **PE+flush = +15.1% net,
  78% win, positive all 6 years, bootstrap p5 +4.1%.** Looked robust.

**The out-of-sample test broke it.** Re-run on real Upstox premiums Oct'24→date (116 trades), the
direction asymmetry **reversed**: CE won +7.8%, PE lost −8.7%, and the deployed gate came in
**−2.8%** (FINNIFTY −17.7%). NIFTY topped Sept 2024 and corrected into 2025 → the drift was DOWN,
so down-breaks continued (fading them lost). The "upward drift" was just the 2019–24 bull regime.
**Gates reverted** (`SWING_FADE_DOWN_ONLY=False`, `SWING_MIN_BREAKOUT_PCT=0.0`).

## The durable lessons

1. **No durable directional edge on the index fade** — pooled across regimes it cancels. Index fade
   is regime timing, run only as a small forward-test.
2. **6 positive years in ONE secular regime ≠ out-of-sample.** The gate passed a 6/6-year check and
   a positive bootstrap p5, then failed the first genuinely different regime. Only a different
   *regime* is a real holdout — bootstrap/per-year checks inside one regime do not protect you.
3. **Real pre-2024 option data exists** via [[nse-bhavcopy]]; it overturned a "validated" strategy.
   Get the real data before trusting a short-window backtest.

Method note: the same rigor that rejected the index gate *confirmed* the stock gate — both judged
on real premiums with identical clean settlement, not estimates.
