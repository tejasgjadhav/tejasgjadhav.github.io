---
title: KDP Dashboard — Amazon BSR tracker
type: project
tags: [kdp, amazon, dashboard, launchd, playwright]
created: 2026-07-03
updated: 2026-07-21
sources: [~/files/kdp-dashboard/README.md, ~/files/kdp-dashboard/HANDOFF.md]
---

Live dashboard tracking Amazon Best Seller Ranks for [[tejas-jadhav]]'s KDP catalog
(full catalog: [[kdp-books]]) across formats and countries, served with GitHub Pages.
Local repo `~/files/kdp-dashboard`, remote `github.com/tejasgjadhav/BSR`, live at
https://tejasgjadhav.github.io/BSR/. Structure: `index.html` dashboard, `scripts/` for the
rank scrape, `data/books.json` + `data/rankings.json` (current + 90-day history + audit_log),
`images/` for covers.

**Catalog = 8 books (as of 2026-07-20)** after adding Spanish + German editions and the Wealth
Code hardcover (7 real covers, updated README).

**Scraper moved off GitHub Actions → local launchd + Playwright (2026-07-21).** Amazon hardened
bot detection ~Jul 17: `curl_cffi` now hits the "Continue shopping" interstitial from both CI and
residential IPs. Fix: `scripts/scrape_bsr.py` fetches via **Playwright headless Chrome** (clicks
through the interstitial), run daily by launchd agent `com.tejasgjadhav.bsr-update` (8 AM +
RunAtLoad) → `daily_update.sh` does pull→scrape→commit→push; the disabled Actions cron was
fake-green (continue-on-error masked daily "Bot detection" failures). Manual fresh pull:
`python scripts/manual_update.py`.

**Honesty-first UI (2026-07-20, commit 917f7a1):** the dashboard shows the REAL age of each rank —
header "Ranks as of \<date\> · Nd ago" (from the newest actual rank, ⚠ when >7 days), country cards
carry "as of \<date\>" captions, ranks >7 days labeled **stale** and dimmed; the scraper reports
"Bot detection" (not "BSR not found") when blocked. Standing rule: never present stale ranks as
fresh, and don't bypass bot-detection or buy a paid proxy/API without laying out ToS tradeoffs
first. Feeds the ad-spend decisions in [[amazon-ads]].

Part of [[files-repo]].
