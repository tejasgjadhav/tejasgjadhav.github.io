---
title: Zerodha Kite Connect — broker API (historical-data attempt)
type: entity
tags: [broker, api, trading, nse, data]
created: 2026-07-03
updated: 2026-07-03
sources: [~/files/institutional-trader/.env (gitignored), ~/files/institutional-trader/CLAUDE.md]
---

Zerodha's **Kite Connect** API — set up during the real-data push for [[institutional-trader]] to try
to source real historical option premiums. Complements [[upstox]] (the live feed).

## App / setup (as of 2026-07)

- Kite Connect app registered by [[tejas-jadhav]]: app name *Institutional Trade*, redirect URL
  `https://127.0.0.1`.
- **Auth is a daily flow** (Kite access tokens expire each morning): open the login URL → approve →
  Kite redirects to `https://127.0.0.1/?...&request_token=…` → exchange the request_token +
  api_secret for an **access_token**, which is then used for the day.
- Instrument mapping quirk: **`instrument_token = exchange_token × 256`**.

## ⚠️ Credentials — NOT stored here

The **API key, API secret, and daily access token are NOT written into this wiki** (it is a git
repo — committing secrets leaks them into history permanently). They live only in
`institutional-trader/.env`, which is **gitignored and must never be committed**. The pasted-in-chat
API secret should be **regenerated** in the Kite developer console as a precaution. To store secrets
durably, use a password manager or the gitignored `.env`, never a tracked file.

## Why it didn't replace bhavcopy

Kite Connect has **no expired-instruments endpoint** — expired option contracts drop out, so it
cannot supply real premiums for closed contracts (the historical-candle API covers live instruments
only, and historical candles need the paid add-on). That gap is exactly why the pre-2024 real-premium
backtests used [[nse-bhavcopy]] instead (free, every expired contract, back to 2019). See
[[real-data-fade-validation]].
