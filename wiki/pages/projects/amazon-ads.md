---
title: Amazon Ads — Sponsored Products for the flagship Claude-finance book
type: project
tags: [kdp, amazon, advertising, marketing]
created: 2026-07-20
updated: 2026-07-20
sources: [~/files/HANDOFF-amazon-ads.md]
---

Amazon Advertising (Sponsored Products) campaign on [[tejas-jadhav]]'s flagship KDP title
**"Claude AI for Finance Professionals"** (see [[kdp-books]]) — campaign
`A08827853M0646XUVFNUL`, entity `ENTITY2H0HGLW74CYKG`. Working state, bid table and watch-items
live in `~/files/HANDOFF-amazon-ads.md`. Rank feedback comes from the [[kdp-dashboard]].

**The recurring failure mode: underspend from bids set too low.** On 2026-07-20 the campaign spent
only ~$3.79/day (568 impressions) against a **$10/day budget** (~$7.48/day the prior week). Root
cause was low bids strangling volume, not the budget. **Through-line lesson: cutting bids to fix
ACOS quietly kills impressions and sales** — on profitable, low-ACOS keywords the right move is to
*raise* bids.

**Bids raised (2026-07-20)** on the winners: `claude ai for investment bankers` (drove a $93.96
sale) $0.90→$1.50; `claude ai made easy` (3.4% ACOS) and `claude ai manual` (4.2%) →$1.50;
`using claude for investing` (5.7%) →$1.50; `claude ai for finance professionals` →$1.20;
`claude ai`/`claude for finance` →$1.10; broad `claude` (discovery) →$1.00. Left at the floor
(at/above break-even): `claude finance`, `ai finance`, `ai finance books`.

**Deciding diagnostic:** recheck daily spend 3–4 days after a bid raise. If it climbs toward
$9–10/day, bids were the bottleneck. **If it stays stuck under ~$6/day despite much higher bids,
the block is the India account-balance alert throttling delivery** — a payment/settings matter only
the user can clear; no bid change fixes it.

Part of [[files-repo]].
