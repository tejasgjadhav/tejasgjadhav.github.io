# Handoff — Amazon Ads optimization ("claude Campaign")
_Updated: 2026-07-31 by Claude Code_

## 🚨 2026-07-31 — SALES COLLAPSE DIAGNOSED + KEYWORD REVERT + SPAIN CAMPAIGN
**Symptom:** Jul 30 royalties $5.82 / 1 order (was ~$22/day avg). Orders healthy 8-16/day
through Jul 23, slid from Jul 25, cratered Jul 30-31.

**Findings (verified in console):**
1. Ads Jul 30: ALL campaigns combined spent $5.55, 7 clicks, 0 purchases, $0 ad sales.
2. Flagship Jul 24-31: $66.22 spend, 79 clicks, 2 purchases, $29.98 sales = **220% ACOS**;
   conversion 2.5% vs 11.8% historical. CTR 0.40% vs 0.55% lifetime.
3. **India insufficient-balance banner STILL up** (user must clear in payment settings —
   flagged since Jul 21, remains the #1 suspected throttle).
4. Timing correlation: my long 21-keyword KDP set went live ~Jul 24 (published Jul 21 + 72h)
   — exactly when organic slide began. User challenged the long keywords; user was right.
5. Flagship manuscript was re-uploaded Jul 28 (v7.epub) — another review cycle mid-window.

**Actions taken 2026-07-31 (all verified):**
- **KDP keywords REVERTED to short head terms** (user-style search-bar terms + proven ad
  converters), 21 distinct per book, all 3 formats republished (~72h review each):
  - Flagship Kindle: claude ai · claude ai book · claude books · claude for finance ·
    ai finance book · claude ai for beginners · how to use claude ai
  - Flagship PB: claude ai manual · claude book · claude ai for finance ·
    claude ai for investment bankers · ai finance · claude code · ai trading
  - Flagship HC: using claude for investing · claude ai guide · ai for investing ·
    generative ai finance · ai investing book · quantitative finance ai · anthropic
  - AI Prompts K: ai prompts · ai prompts book · finance prompts · prompt engineering ·
    claude prompts · prompts for financial analysts · ai for finance
  - AI Prompts PB: ai prompts for finance · financial modeling ai · ai finance prompts ·
    prompt engineering finance · prompt book · financial analyst ai · dcf valuation ai
  - AI Prompts HC: prompt engineering handbook · ai financial analysis book · investment
    banking ai · ai valuation · fp&a ai prompts · ai for analysts · generative ai prompts
  - Cowork K: ai agents · ai agents book · ai automation · build ai agents · claude agents ·
    ai for finance teams · no code ai
  - Cowork PB: claude cowork · anthropic cowork · ai workflow automation · ai agents for
    finance · claude ai agents · finance automation · claude code book
  - Cowork HC: ai finance book · ai agents handbook · ai in banking · finance automation
    book · agentic ai · artificial intelligence finance · claude agent sdk
  - Spanish edition (all 3 formats): already short head terms — left UNTOUCHED, no republish.
- **US ES campaign A023886336CS4J1OOSKJ paused then ARCHIVED** (user ordered deletion).
- **NEW Spain-marketplace campaign LAUNCHED**: "Claude AI para profesionales - Spain",
  id A0260804YDGTTVW6LT4S, entity ENTITY3991WBI12IAGA (advertising.amazon.es), €2.00/day,
  manual targeting, dynamic bids DOWN ONLY, 3 products (B0H57YSP56/B0H9B6HXK2/B0H99G7KFX,
  all in stock on .es), 8 exact kw @ €0.60 (claude ia · claude ia finanzas · claude ai
  finanzas · ia para finanzas · inteligencia artificial finanzas · prompts ia finanzas ·
  claude ia libro · analisis financiero ia), 4 phrase negatives (gratis·pdf·curso·descargar).

**✅ INDIA BALANCE ALERT = FALSE ALARM (verified 2026-07-31 in Billing overview):**
India ads profile has ₹0 billed EVER, no overdue anywhere, US/DE/ES all Active with $0
overdue, zero unpaid invoices. The red banner comes from an unused India prepaid wallet and
does NOT block US/DE/ES delivery. DO NOT add balance. US ads were serving all along
($66 spent Jul 24-31) — the sales collapse was the keyword/conversion issue, not payment.

**✅ BUDGET CUTS 2026-07-31 (user directive: cap ~$300/month spend). All verified:**
- Flagship $10 → **$6.00/day**
- German auto €2.43 → **€1.75/day** (⚠️ gotcha: typing "1,75" saved as €175 — the field
  treats comma as thousands sep; caught and fixed immediately. ALWAYS use a dot.)
- German manual €2.00 → **€1.00/day**
Committed total now ≈ $13.3/day ≈ $400/mo ceiling; actual spend is consumption-based
(charged per click only, budget = daily cap not a charge) and historically runs 50-60% of
cap → ~$200-250/mo expected. Billing = CPC consumption, charged to card monthly/threshold.

**⬜ WATCH / NEXT:**
2. Keyword reviews clear ~Aug 2-3; judge sales recovery Aug 4-7.
3. If flagship ACOS still >100% after revert: cut the Jul 23 bid raises back down
   (claude $1.00→$0.75, claude ai $1.10→$0.90, exacts $1.50→~$1.10).
4. German hardcover draft GF2HWVXH40X ("Claude AI für Finanzprofis") sits unpublished with
   short keywords — untouched, decide separately.

> Separate from `HANDOFF.md` in this directory, which covers the LinkedIn/Naukri job drive
> and the German book build. Do not merge the two.

## Goal
Optimize the Amazon Sponsored Products campaign for "Claude AI for Finance Professionals"
to be **profitable within a fixed $12/day budget**. User has stated the budget will NOT be
raised — income from the book funds living expenses, so profit per dollar matters more than growth.

## Account coordinates
- Campaign: `claude Campaign - 5/31/2026 20:00:35.122` — id `A08827853M0646XUVFNUL`
- Ad group: `Ad Group - 5/31/2026 20:01:10.550` — id `A06090321R3RU1KRZXPPB`
- Entity: `ENTITY2H0HGLW74CYKG`
- Console: https://advertising.amazon.com/cm/sp/campaigns/A08827853M0646XUVFNUL/ad-groups?entityId=ENTITY2H0HGLW74CYKG
- Access via `mcp__claude-in-chrome__*` (user's logged-in Chrome). Sonsored Products, US, manual targeting.

## Baseline (lifetime, as of 2026-07-20)
$334.82 spend → $576.17 sales, 30 purchases, **58.08% ACOS**, 46,514 impressions, 255 clicks.
43 keywords total: 13 enabled, 30 paused.

### Cost per purchase by placement (the decisive table)
| Placement | Cost | Purchases | Cost/purchase |
|---|---|---|---|
| Rest of search | $132.21 | 19 | **$6.96** |
| Product pages | $157.90 | 10 | $15.79 |
| Top of search | $48.55 | 1 | **$48.55** |

## Current state

**Done and verified (2026-07-20):**
1. **6 negative phrase keywords added** (ad group had ZERO before):
   `prompt engineering`, `make money`, `network engineers`, `financial planning`,
   `trading books`, `system design interview`
2. **Rest of search bid adjustment → +50%.** Top of search deliberately left at 0%.
3. **6 exact-match keywords added at $1.60**, all Delivering:
   `claude ai for investment bankers`, `claude ai for finance professionals`,
   `claude for finance`, `claude ai made easy`, `claude ai manual`, `using claude for investing`

**Bid restructure COMPLETE 2026-07-20 (planned by Fable 5, executed by Opus 4.8).**

Final enabled set — 12 keywords, all verified Delivering:

| Keyword | Match | Bid |
|---|---|---|
| claude ai made easy | Exact | $1.25 |
| claude ai manual | Exact | $1.25 |
| using claude for investing | Exact | $1.15 |
| claude | Broad | $0.90 |
| claude ai for investment bankers | Exact | $0.90 |
| claude for finance | Exact | $0.85 |
| claude ai finance | Broad | $0.83 |
| claude finance | Broad | $0.83 |
| claude ai for finance professionals | Exact | $0.80 |
| claude ai | Broad | $0.73 |
| ai finance books | Broad | $0.70 |
| ai finance | Broad | $0.60 |

Paused: `ai prompt`, `ai trading`, `claude code`, `trading`, `gen ai books`, `investing book`,
`generative ai system design interview`.

All placement bid adjustments reverted to **0%** (Top of search / Rest of search / Product pages).

**KEYWORD-LEVEL ACOS discovered during execution** (was not available when planning — the earlier
figures were per-search-term, which understated some keywords badly):
`claude` 40.4% (16 of 28 purchases — the engine) · `claude ai` 21.7% ✓ · `ai finance` 32.1% ·
`claude finance` 59.9% · `claude ai finance` 71.7% · `ai trading` 86.7% · **`claude code` 310.8%**
(search-term view had shown 30.5% — this is why it was paused rather than bid down).

**Account quirk: minimum bid is $0.60.** A $0.55 bid on `ai finance` was silently rounded up to $0.60.

**Open / unresolved:** the break-even question below. Nothing else should be tuned until it's answered.

## ✅ RESOLVED 2026-07-20 — the campaign is running at a LOSS

Source: `~/Downloads/KDP_Royalties_Estimator-d3acf617-4aca-452f-b5b8-44f214b2392a.xlsx`
(sheets: eBook / Paperback / Hardcover Royalty). Filtered to title
"Claude AI for Finance Professionals", Marketplace = Amazon.com, Currency = USD.

**Actual US royalties (real data, 479 units):**
| Format | Price | Royalty/unit | % of sale | Print cost |
|---|---|---|---|---|
| Paperback | $24.99 | $6.76 | **27.1%** | $8.23 |
| eBook | $5.99 | $3.85 | 64.2% | — |
| Hardcover | ~$44 | $9.94 | 21.1% | $20.05 |

**Break-even ACOS ≈ 27%** (ad sales are overwhelmingly the $24.99 paperback —
ads report shows $24.99/$23.99/$21.99 order values). Campaign is at **58.08%**.

Lifetime: $576.17 sales × ~27% = ~$156 royalty vs $334.82 spend → **roughly −$180**.
Even at a generous 50/50 paperback/ebook mix (45.7% blended) it is still ≈ −$72.

**THE binding constraint: max sustainable CPC ≈ $0.70.** Actual CPC is $1.33.
(Conversion 11.8% = 30 purchases / 255 clicks; ~$5.76 royalty per ad-driven sale;
$5.76 × 0.118 ≈ $0.68.) The campaign pays about 2x what a click can be worth.

**This invalidated part of the earlier same-day work:** the 6 exact keywords were added at
$1.60 and Rest of search was boosted +50% — both push CPC UP. Those were correct for moving
ACOS off 58%, but 58% was never the right target. 27% is.

### Strategic notes beyond the ads
- eBook pays 64%, paperback 27%. Ads driving ebook sales are viable at 58% ACOS; ads driving
  paperback sales are not. Paperback print cost ($8.23) eats a third of list.
- Hardcover (21%, $20.05 print cost) is the weakest format by a wide margin.

## 🚨 BLOCKER discovered 2026-07-20 — CAMPAIGN IS NOT RUNNING (payment failure)
All keywords show status **"Payment failure"**. Two account alerts:
1. *"Your credit card couldn't be charged — You don't have enough credit to make a payment in United States."*
2. *"Your campaigns have stopped delivering due to insufficient balance. Please add balance to your account in India to resume advertising."*

**The user must fix this themselves in Amazon payment settings — Claude must never enter card or
payment details.** Until it is resolved, every optimization below is inert: no impressions, no spend,
no sales. Nothing can be measured and the day-14 / day-30 checkpoints cannot start counting.

## OPEN QUESTION (asked 2026-07-20, in progress)
User wants keyword + budget strategy across all books/formats, and asks whether the $12/day
should back one book or be split across three.

**Full US royalty-per-unit table (offer-price basis, from the KDP file):**
| Title | eBook | Paperback | Hardcover |
|---|---|---|---|
| Claude AI for Finance Professionals | $3.78 (63.2%, $5.98) | $6.77 (27.1%, $24.99) | $9.49 (21.1%, $44.98) |
| AI Prompts for Financial Analysis | $3.18 (63.8%, $4.98) | $6.55 (31.4%, $20.87) | $8.93 (20.4%, $43.83) |
| Claude Cowork for Finance | $2.86 (63.6%, $4.49) | $6.06 (40.2%, $15.09) | $9.87 (28.2%, $34.99) |

US unit volume: Claude AI Finance 233 pb / 231 eb / 15 hc · AI Prompts 35 pb / 151 eb / 5 hc ·
Claude Cowork 14 pb / 63 eb / 4 hc.

⚠️ **KEY REFRAME:** ACOS% is misleading across formats. What ads actually need is *royalty per unit*
(max CPA). Hardcover pays the MOST per sale ($9.49) despite the worst ACOS%; ebook pays the least
($3.78) despite the best ACOS%. Max CPC = royalty/unit × conversion rate (11.8%):
hardcover $1.12 · paperback $0.80 · ebook $0.45.

⚠️ **There is no book called "Claude Code."** The user said "claude code" — the actual titles are
*Claude Cowork for Finance* and *AI Prompts for Financial Analysis*. `claude code` is also an
existing (now paused, 310% ACOS) KEYWORD. Confirm which they meant before acting.

## KEYWORD SETS — all three books (Fable-planned, 2026-07-20)

Bid rule: max CPC = royalty-per-unit × conversion rate (11.8%). Account minimum bid is **$0.60**.
Book 3 confirmed by user as **Claude Cowork for Finance** (there is no "Claude Code" book).

### BOOK 1 — Claude AI for Finance Professionals — gets the FULL $12/day
All 3 format ASINs in ONE ad group. Blended break-even bid ≈ $0.73 (≈$0.95 if paperback repriced).

| Keyword | Match | Bid | Status |
|---|---|---|---|
| claude ai made easy | Exact | $1.25 | ✅ live |
| claude ai manual | Exact | $1.25 | ✅ live |
| using claude for investing | Exact | $1.15 | ✅ live |
| claude ai for investment bankers | Exact | $0.90 | ✅ live |
| claude for finance | Exact | $0.85 | ✅ live |
| claude finance | Broad | $0.83 → cut to $0.60 | ⬜ TODO |
| claude ai for finance professionals | Exact | $0.80 | ✅ live |
| claude ai | Broad $0.73 → **Exact $0.90** | | ⬜ TODO (match-type change = new kw) |
| claude ai for cfo | Exact | $0.70 | ✅ live |
| claude ai for investing | Exact | $0.70 | ✅ live |
| claude for financial analysts | Exact | $0.70 | ✅ live |
| ai finance books | Broad | $0.70 | ✅ live |
| ai finance | Broad $0.60 → **Phrase $0.70** | | ⬜ TODO |
| claude | Broad | $0.90 → cut to $0.75 | ⬜ TODO |
| how to use claude ai | Exact | $0.60 | ✅ live |
| claude ai for beginners | Phrase | $0.65 | ⬜ TODO |

Negative exact (live): claude code · claude coding · claude api · claude pricing · anthropic careers ·
claude monet · claude ai login · claude vs chatgpt · ai trading bot
Negative phrase (live): prompt engineering · make money · network engineers · financial planning ·
trading books · system design interview

### BOOK 2 — Claude Cowork for Finance — SHELVED until day 30 ($2/day when live)
Note: its paperback is the **most ad-tolerant in the catalogue** — $15.09 list, $6.06 royalty,
**40.2% break-even ACOS** vs the flagship's 27.1%. Worth remembering if the flagship stalls.
All Exact, all $0.60: claude cowork · anthropic cowork · claude cowork finance ·
claude agents for finance · ai agents for finance teams

### BOOK 3 — AI Prompts for Financial Analysis — SHELVED until day 30 ($2/day when live)
Ebook-dominant (151 eb vs 35 pb) → blended royalty ~$3.90 → break-even bid ~$0.46, which is
**BELOW the $0.60 account minimum.** This book only works at minimum bid AND only if it converts
≥15%. Treat as a short-leash experiment, judged at 100 clicks, hard stop.
All Exact, all $0.60: ai prompts for financial analysis · chatgpt prompts for finance ·
prompts for financial analysts · claude prompts finance · prompt engineering for finance
⚠️ Caution: generic prompt/AI terms already lost money on the flagship.

## ✅ FINAL USER DECISION 2026-07-20 (supersedes the split below): "do what fable thinks is right"
= **ONE BOOK. All $12/day on Claude AI for Finance Professionals. Do NOT build campaigns B and C.**
This also resolves the $14-vs-$12 arithmetic problem — it no longer applies.
Books 2 and 3 stay shelved until the day-30 trigger (flagship ACOS ≤45% AND cost/purchase <$7).

### Flagship edits applied in this final pass
- `claude` broad $0.90 → **$0.75** ✅
- `claude finance` broad $0.83 → **$0.60** ✅
- `claude ai for investing` $1.49 → **$0.70** ✅ (an earlier correction had silently failed)

### ⬜ STILL OUTSTANDING — 3 match-type changes (not applied; ran out of session context)
These need a fresh session. Each is add-new + pause-old, since Amazon cannot change a keyword's
match type in place:
1. Add `claude ai` **Exact @ $0.90** → then pause the existing `claude ai` Broad ($0.73)
2. Add `ai finance` **Phrase @ $0.70** → then pause the existing `ai finance` Broad ($0.60)
3. Add `claude ai for beginners` **Phrase @ $0.65** (no existing keyword to pause)

⚠️ **UI GOTCHA that ate two attempts:** after clicking "Add keywords" in the Enter-list dialog, a
sub-dialog appears — *"N of M keywords don't have a suggested bid. Choose an alternate bid: $0.30"*.
It must be filled in and confirmed with its own "Add keywords" button. Clicking elsewhere dismisses
the WHOLE dialog and silently discards everything. Also: keywords that DO have a suggested bid
ignore the custom bid and take the suggestion — check every row's bid in the right-hand panel
before pressing Save.

## SUPERSEDED — earlier three-way split request (user reverted to Fable's plan, see above)
User wants to split budget three ways: **Claude AI $10 + AI Prompts $2 + Claude Cowork $2**.

⚠️ **ARITHMETIC PROBLEM: that totals $14/day, not $12.** User previously stated $12 is a hard
ceiling tied to living expenses. MUST confirm before building: either $14/day total, or
$8 + $2 + $2 to hold the $12 line. Do not assume.

⚠️ Fable's analysis argued against splitting (each $2/day book gets ~2.4 clicks/day ≈ 0.28
orders/day, so ~1.3 orders per keyword per month — below the level at which a bid decision can be
made, and Amazon's algorithm never exits learning mode). User has chosen to split anyway; that is
their call. Build it, but keep the day-30 kill trigger: any $2/day campaign with 100 clicks and
<2 orders gets paused and its budget returned to the flagship.

⚠️ AI Prompts specifically: break-even bid ~$0.46 is BELOW the $0.60 account minimum. It is
structurally unprofitable at any bid Amazon will accept unless conversion exceeds ~15%.

### TO BUILD (two new Sponsored Products campaigns, US, manual targeting)
Campaign B — "AI Prompts for Financial Analysis" — $2/day, all formats one ad group, all Exact $0.60:
ai prompts for financial analysis · chatgpt prompts for finance · prompts for financial analysts ·
claude prompts finance · prompt engineering for finance
Negatives (phrase): free · pdf download · course · certification

Campaign C — "Claude Cowork for Finance" — $2/day, all formats one ad group, all Exact $0.60:
claude cowork · anthropic cowork · claude cowork finance · claude agents for finance ·
ai agents for finance teams
Negatives (phrase): claude code · coworking · office space · free

Then reduce Campaign A (flagship) daily budget from $12 to $10 (or $8 — see arithmetic above).

## 🇪🇸 SPANISH EDITION — new €2/day campaign requested 2026-07-20 (NOT YET BUILT)
**Claude AI para profesionales de las finanzas: Prompts, plugins y flujos de trabajo —
18 mesas financieras institucionales, 130+ prompts originales** · TEJAS JADHAV · KDP Select enrolled
- Kindle eBook — ASIN **B0H57YSP56** — $6.99
- Paperback — ASIN **B0H9B6HXK2** — $34.99
- Hardcover — ASIN **B0H99G7KFX** — $59.99
All three went live 2026-07-17.

✅ **CORRECTED 2026-07-20 by user: primary marketplace is Amazon.com, NOT Amazon.es.** The author
advertises foreign-language editions on the US marketplace — same approach already used for the
German edition (*Claude AI für Finanzprofis*, which shows US ebook sales in the royalty report,
confirming the pattern works).

So this is a **new campaign in the EXISTING US ad account**: Amazon.com, **USD**, $2/day,
same $0.60 minimum bid, same billing. No new marketplace access needed. Spanish-language keywords
target Spanish-speaking buyers searching on Amazon.com.

### Estimated unit economics (BETTER than the US edition — higher price vs the same fixed print cost)
| Format | Price | Est. royalty | Est. break-even ACOS |
|---|---|---|---|
| eBook $6.99 | 70% | ~$4.89 | ~70% |
| Paperback $34.99 | 60% − ~$8.23 print | **~$12.76** | **~36.5%** |
| Hardcover $59.99 | 60% − ~$20 print | ~$16.00 | ~26.7% |

Compare the US edition: paperback 27.1%, hardcover 21.1%. The Spanish edition is materially more
ad-tolerant purely because list price is higher against the same fixed manufacturing cost.
**These are ESTIMATES** — pull the real figures from the KDP royalty report once ES sales exist.

⚠️ **Zero sales history, zero reviews, listing is 3 days old.** Conversion rate is unknown, so the
11.8% used for US bid math does NOT transfer. Start at the floor and let data accumulate.

### Spanish keyword set (all Exact, start at €0.60 / marketplace minimum)
Spanish searchers use both "IA" and "AI" — cover both.
claude ia · claude ia finanzas · claude ai finanzas · ia para finanzas ·
inteligencia artificial finanzas · prompts ia finanzas · claude ia libro ·
analisis financiero ia · ia para analistas financieros · prompts inteligencia artificial finanzas

Negative phrase: gratis · pdf · curso · descargar · chatgpt

### Day-30 kill trigger
100 clicks with <2 orders → pause and return the budget to the US flagship.

## ⏳ IN PROGRESS 2026-07-20 — applying the 7 keywords below to the LIVE KDP listing
User explicitly authorised editing + republishing. Three formats, each has its own 7 keyword slots:
Kindle **B0GSX73KF6** ($5.99) · Paperback **B0GV2SS77G** ($24.99) · Hardcover **B0GVJPXVP8** ($49.99)
Republishing metadata triggers an Amazon review (~72h); the book normally stays live during it.
Priority order if time/context is short: Kindle (231 US units) → Paperback (233) → Hardcover (15).

## ✅ CARD FIXED 2026-07-21 — campaigns spend live. Reprice DECLINED (drop it). Subagent FAILED (stalled).

## ⚠️ UNDERSPEND DIAGNOSIS 2026-07-23 (user caught it): account spent only $5.71 on Jul 21 vs ~$18
budget. Root cause: bids were cut TOO aggressively (~$0.60-1.25, near floor) to fix the 58% ACOS →
now loses auctions → can't consume the $10 flagship budget → low volume, low sales. This is the
opposite of the earlier "out of budget" problem (that flag is now STALE). Fix in progress: a
subagent is RAISING bids on the proven low-ACOS converters (claude ai, investment bankers, made
easy, manual, using-for-investing, etc.) toward suggested bids to win more profitable volume, while
leaving the money-losers low. ✅ DONE 2026-07-23: verified underspend (~$7.48/day last 7d; Jul 21 only
$3.79 on 568 impr), then RAISED 8 bids (each verified after save): claude $0.75→$1.00 · claude ai
$0.90→$1.10 · claude ai for finance professionals $0.80→$1.20 · claude ai for investment bankers
$0.90→$1.50 · claude ai made easy $1.25→$1.50 · claude ai manual $1.25→$1.50 · claude for finance
$0.85→$1.10 · using claude for investing $1.15→$1.50. Left low: claude finance $0.83, ai finance
$0.70, ai finance books $0.70. (Earlier match-type backlog was applied: claude ai now Exact, ai
finance now Phrase.) ⬜ WATCH: recheck daily spend in 3-4 days — if ~$9-10/day, fixed. If STILL
under ~$6/day, the India balance alert is likely throttling delivery → user must clear it.
Daily budget = hard ceiling, no runaway risk. LESSON: aggressive bid-cutting fixes ACOS% but starves volume; the right equilibrium
bids high enough to spend budget on sub-breakeven terms. Also note: month-to-date sales ARE happening
($492.73 Jul 1-22, all 5 campaigns Delivering, India-balance issue RESOLVED — no payment banner).
New ES/AI-Prompts campaigns created Jul 20 are only 2-3 days old → too young to judge (need ~14d).

## 🗺️ ACTUAL LIVE STATE verified 2026-07-21 (this is ground truth):
| Campaign | Country | Budget | Status | Notes |
|---|---|---|---|---|
| claude Campaign (A) A08827853M0646XUVFNUL | US | **$8.00/day** ✅ | Delivering | agent DID reduce 12→8 before failing |
| german autotargetting Campaign - 1.6.2026 | Germany | €2.43 (~$2.78) | Delivering | **PRE-EXISTING**, not from this session |
| Campaign - 31.5.2026 20:20:43.149 | Germany | €2.00 (~$2.29) | Delivering | **PRE-EXISTING**, not from this session |

**German edition is ALREADY advertised (2 campaigns, ~$5/day). Do NOT build a new German campaign.**
Current committed spend ≈ **$13.07/day** BEFORE adding anything.
The broken multi-country draft the subagent left was discarded (was $0 budget, never launched).

## ⚠️ BUDGET CONFLICT — user chose "skip new German, add AI Prompts $2 + Spanish $2"
That = $8 + $5.07 German + $2 + $2 = **~$17/day, breaks the $14 cap by ~$3.**
✅ RESOLVED 2026-07-21 (v2): user re-weighted → **flagship UP to $10, remaining ~$8 split $2 each.**
TARGET ALLOCATION (~$18/day total):
- US "claude Campaign" (flagship, proven earner): **$8 → $10** (RAISE)
- German auto (€2.43): trim toward ~$2 (≈€1.75) — NOTE: bills in EUR, "$2" is approximate
- German manual (€2.00 ≈ $2.29): already ~$2, leave or nudge to ~€1.75
- Campaign B (AI Prompts): $2
- Campaign D (Spanish): $2
Rationale: puts most weight on the only proven earner (Fable-aligned), equal small test budgets on
the other four; kill-trigger still applies (100 clicks <2 orders → pause, money to flagship).
⚠️ German campaigns are EUR — cannot set an exact USD figure; get them approximately $2-equivalent.

## ✅ 2nd build subagent COMPLETED 2026-07-21 — campaigns built & launched. Final state:
| Campaign | id | Country | Budget | Status |
|---|---|---|---|---|
| claude Campaign (flagship) | A08827853M0646XUVFNUL | US | **$10.00** ✅ raised | Delivering |
| AI Prompts for Financial Analysis (NEW) | A09636231W6B3M6SPV2O0 | US | $2.00 | Launched |
| Claude AI para profesionales ES (NEW) | A023886336CS4J1OOSKJ | US | $2.00 | Launched |
| german autotargetting | (pre-existing) | DE | €2.43 | Delivering |
| Campaign - 31.5.2026 | (pre-existing) | DE | €2.00 | Delivering |
Total ≈ **$19.07/day** (→ ~$18.29 once German-auto trimmed).

Campaign B products: Kindle B0GS5RL6XS, Paperback 9357823662, Hardcover B0GSBV7QX9 (4th pb
B0GS6FS186 was out-of-stock, skipped). 7 exact kw @ $0.60 + 6 phrase negatives — all verified.
Campaign D products: B0H57YSP56 / B0H9B6HXK2 / B0H99G7KFX. 8 exact kw @ $0.60 + 4 phrase negs.

## ✅ 2026-07-21: KDP keywords APPLIED to all 4 books × 3 formats (12/12 entered & verified).
##   - 4 Kindle/eBook editions: PUBLISHED ("Updates in review", ~72h): Claude AI B0GSX73KF6,
##     AI Prompts B0GS5RL6XS, Cowork B0H1R2GZX9, Spanish B0H57YSP56.
##   - 8 PRINT editions (paperback+hardcover): keywords SAVED server-side but NOT published —
##     agent hit an Amazon PASSWORD re-auth wall at the print pricing step (entering a password is
##     prohibited, so it correctly stopped). Status "With unpublished changes / Continue setup".
##   ⬜ USER MUST FINISH THE 8 PRINT FORMATS: Bookshelf → each "Continue setup" → Content → Pricing
##      → Publish (sign in once when prompted). NO keyword re-entry needed — values already saved.
##      Print ASINs: ClaudeAI PB B0GV2SS77G / HC B0GVJPXVP8 · AIPrompts PB 9357823662 / HC B0GSBV7QX9
##      · Cowork PB B0H2CZKK2W / HC B0H2CWS6K7 · Spanish PB B0H9B6HXK2 / HC B0H99G7KFX
##   (Only the Keywords field was touched anywhere; price/title/desc/cover/manuscript untouched.)

## ⬜ TWO OUTSTANDING ITEMS (user must do — Claude blocked)
1. **Trim german autotargetting €2.43 → €1.75.** Agent couldn't: the inline spinner only steps in
   whole euros (€1.43 or €3.43) and the classifier blocked typing an exact value. Set manually.
2. **PAYMENT/BALANCE WARNING is BACK:** *"Your campaigns have stopped delivering due to insufficient
   balance. Please add balance to your account in India."* User said the card was fixed, but this
   India-account-balance alert (a SEPARATE alert from the US card) appears to still be open.
   Campaigns show "Delivering" but may not actually serve until balance is added. USER MUST RESOLVE
   in payment settings — Claude must never touch payment details.

## 💰 $14/DAY ALLOCATION ACROSS 4 CAMPAIGNS (user directive 2026-07-21) — BUILDING NOW
All on **Amazon.com**, USD, $0.60 min bid. All formats of a title in ONE ad group per campaign.

| Campaign | Budget | Basis |
|---|---|---|
| A · Claude AI for Finance Professionals (EN) — EXISTS, A08827853M0646XUVFNUL | **$8** | 30 purchases, $576 sales — only proven earner |
| B · AI Prompts for Financial Analysis | **$2** | 151 ebook + 35 pb US units |
| C · Claude AI für Finanzprofis (DE) | **$2** | 8 US ebook units — .com pattern proven |
| D · Claude AI para profesionales (ES) | **$2** | 0 units, brand new — pure test |
| **TOTAL** | **$14** | |

Step 1: reduce Campaign A daily budget $12 → **$8**. Then create B, C, D at $2 each.
Kill trigger on B/C/D: 100 clicks with <2 orders → pause, return budget to A.

**Campaign C — GERMAN ad keywords** (Exact, $0.60): claude ki finanzen · claude ai finanzen ·
ki für finanzprofis · ki prompts finanzen · künstliche intelligenz finanzen · claude ki buch ·
finanzanalyse ki · ki für analysten — Negatives: kostenlos · pdf · kurs · gratis

**Campaign D — SPANISH ad keywords** (Exact, $0.60): claude ia · claude ia finanzas ·
claude ai finanzas · ia para finanzas · inteligencia artificial finanzas · prompts ia finanzas ·
claude ia libro · analisis financiero ia — Negatives: gratis · pdf · curso · descargar

**Campaign B — AI PROMPTS ad keywords** (Exact, $0.60): ai prompts for financial analysis ·
ai prompts for finance · financial analyst prompts · prompt engineering finance · ai prompt book ·
prompts for equity research · ai prompt library — Negatives: free · pdf · course · art ·
midjourney · entrepreneurs
⚠️ KEY INSIGHT: `ai prompt` had **9,494 impressions** but converted badly for the CLAUDE book —
that was a product/query MISMATCH, not weak demand. For the AI Prompts book it is the core term.

## 📚 KDP KEYWORDS — 3 BOOKS, DATA-GROUNDED (final, 2026-07-21) — use these
Grounded in the flagship's 162-query Search Terms report; same audience → terms transfer across all
3 books. PROVEN anchors (must be included) flagged ⭐. Simple head terms, ≤50 chars, 7 per format.
Rule: `chatgpt`/`gpt`/`openai`/`gemini`/`midjourney` NEVER (suppression). `claude`/`anthropic`/`cowork` OK.

### CLAUDE COWORK FOR FINANCE
Kindle: claude ai book · ai for finance · ai agents for beginners · learn ai automation · generative
ai book · ai for finance professionals · no code ai
Paperback: ⭐claude cowork (PROVEN $21.99 sale) · ai agents book · ai automation finance · claude ai
guide · build ai agents · ai trading bot book · ⭐claude code (2,935 impr+sale)
Hardcover: ⭐ai finance book · ai agents handbook · ai in banking · finance automation book · ai
workflow automation · artificial intelligence finance · claude agent sdk

### AI PROMPTS FOR FINANCIAL ANALYSIS
Kindle: ⭐ai prompts book · prompt engineering book · finance prompts · learn prompt engineering · ai
prompts for beginners · generative ai prompts · ai for financial analysis
Paperback: ⭐ai prompts for finance (the 9,494-impr core term) · financial modeling ai · ai investing
book · prompt engineering finance · ⭐claude prompts · financial analyst ai · dcf valuation ai
Hardcover: prompt engineering handbook · ai financial analysis book · investment banking ai · ai
valuation · fp&a ai prompts · ai for analysts · financial analysis handbook

### CLAUDE AI PARA PROFESIONALES (SPANISH)
Kindle: ia para principiantes · libro ia finanzas · ⭐claude ia · aprender ia · ⭐ia finanzas · libro
de inteligencia artificial · ai finanzas
Paperback: ⭐inteligencia artificial finanzas · claude ai libro · ia para inversiones · prompts ia ·
ia banca · analisis financiero ia · libro claude
Hardcover: inteligencia artificial libro · ia para profesionales · ai para finanzas · ia para
invertir · libro inteligencia artificial finanzas · prompts para finanzas · ia trading
(Accents dropped intentionally — Amazon matches unaccented and buyers rarely type them.)

⚠️ These are domain+proxy grounded. Once each book runs its OWN ads for ~2 weeks, revisit with its
real Search Terms report — same method used on the flagship.

## SUPERSEDED — AI Prompts-only KDP set below (use the 3-book block above instead)
## 📚 KDP KEYWORDS — AI Prompts for Financial Analysis (21, 7 per edition)
Title already indexes: ai, prompts, financial, analysis, practical, sample, outputs, equity,
research, valuation, investment, banking, risk, management → don't waste slots on these.

**PAPERBACK ($20.87, $6.55/u):** `ai prompt library for bankers` · `financial modeling prompt
templates` · `dcf lbo comps prompt guide` · `m&a deal analysis ai prompts` · `credit risk
portfolio prompt book` · `fp&a treasury prompt playbook` · `prompt engineering for analysts`

**KINDLE ($4.98, $3.18/u):** `ai prompt engineering guide beginners` · `100 prompts for financial
analysts` · `generative ai prompt handbook` · `llm prompts for business finance` · `ai copilot
prompts for excel` · `prompt templates for consultants` · `ai prompt book for professionals`

**HARDCOVER ($43.83, $8.93/u):** `institutional finance prompt desk` · `quantitative analysis
prompt guide` · `hedge fund private equity prompts` · `ai automation prompts for finance` ·
`capital markets prompt reference` · `agentic ai prompts for finance` · `equity valuation
prompt workflows`

⚠️ Excluded: `chatgpt`, `gpt`, `openai`, `midjourney` — competitor trademarks, suppression risk.
Avoid `CFA`/`FRM` in metadata too (credential-body trademarks).

## ⭐ FINAL — 21 DISTINCT KDP KEYWORDS (7 per format, max coverage) — USE THIS SET
Each format has its OWN 7 slots → 21 distinct strings, not the same 7 repeated. All ≤50 chars.
Allocation is weighted by unit volume + royalty: strongest evidence on Paperback (233u, $6.77/u),
learning/discovery on Kindle (231u, $3.78/u), adjacent/premium on Hardcover (15u, $9.49/u).

### PAPERBACK B0GV2SS77G — highest-value format, strongest-evidence terms
1. `claude ai for investment bankers`
2. `claude ai for cfo and finance directors`
3. `equity research valuation dcf modeling`
4. `investment banking private equity hedge fund`
5. `financial modeling excel automation tools`
6. `ai for financial analysts and advisors`
7. `corporate finance fpa treasury risk`

### KINDLE B0GSX73KF6 — learning / beginner / broad discovery
8. `claude ai made easy manual playbook`
9. `claude ai for beginners bible guide`
10. `learning claude ai step by step`
11. `ai engineering prompt engineering guide`
12. `ai productivity tools for professionals`
13. `artificial intelligence business books`
14. `machine learning for finance practitioners`

### HARDCOVER B0GVJPXVP8 — adjacent / senior / premium
15. `using claude for investing and markets`
16. `quantitative finance ai data analysis`
17. `generative ai finance handbook reference`
18. `agentic ai agents for finance workflows`
19. `capital markets portfolio management ai`
20. `fintech innovation digital transformation`
21. ~~`ai automation for accountants auditors`~~ → **REPLACED with `claude code for finance automation`**

### ⚠️ CORRECTIONS 2026-07-21 (user challenged, user was right)
**(a) `accountants auditors` DROPPED.** Wrong audience — this book is institutional finance
(IB / equity research / PE / capital markets desks), not accounting or audit.

**(b) `claude code` was WRONGLY excluded.** Two errors in the original reasoning:
  1. It was filed under "author's other books" — it is NOT. Claude Code is Anthropic's product.
     The author's other books are Claude Cowork and AI Prompts. That exclusion was a category error.
  2. Ads ACOS logic was applied to a FREE slot. KDP backend keywords cost nothing per impression —
     there is no CPC. A term at 310% ACOS is a *paid-bidding* verdict, NOT an organic-relevance
     verdict. Terms that lose money in ads can be perfectly good free KDP keywords.
  `claude code` converted a real sale → **include it.**

**(c) Same logic re-admits `ai trading`** — 3 purchases / $34.97 at keyword level, and the book
covers trading desks. Money-losing in paid ads, free and relevant as a KDP keyword. → include.

**(d) STILL excluded: `chatgpt` / `openai`** — trademark/suppression risk is independent of cost.
And `claude cowork` — that genuinely IS the author's other book; would cannibalise.

**(e-REVISED) VOLUME DATA DOES EXIST — impressions from the ads report are a demand proxy.**
Lifetime impressions per keyword (higher = more search demand):
claude 16,646 · ai prompt 9,494 · ai trading 3,054 · **claude code 2,935** · ai finance 1,310 ·
claude finance 1,266 · claude ai 1,008 · trading 991 · claude ai finance 608 · ai book 302 ·
agentic ai book 285 · ai investment 180 · agentic 127 · agentic ai 113 · ai agent 79 ·
gen ai books 64 · ai engineering 63 · ai finance books 53 · investing book 47 · ai beginners 20 ·
ai agents book 8
→ Rank KDP keywords by IMPRESSIONS (demand) × CONVERSION (relevance). Drop sub-100-impression
terms; they are not worth a slot. Caveat: impressions are bid-dependent, so this is directional.
Also: all 162 rows in the Search Terms report are PROVEN real customer queries.

**(e-OLD, superseded) SEARCH VOLUME IS UNKNOWN.** These 21 are built from CONVERSION evidence in the ads
Search Terms report, not from search-volume data. Amazon gives KDP authors no volume figures.
Nothing here is verified as "high search". To get real volume, use Publisher Rocket / Helium 10,
or Amazon's own search-bar autocomplete as a free proxy. Treat the broad discovery terms
(artificial intelligence business books, machine learning for finance practitioners, fintech
innovation) as UNVERIFIED GUESSES — they carry no conversion evidence at all.



### DELIBERATELY EXCLUDED (this is the "full scope" answer)
- `chatgpt` / `openai` — competitor trademarks; KDP metadata violation, suppression risk.
  (Note: "open ai for finance" DID convert 1 sale in ads — still not safe as a KDP keyword.)
- `claude code` / `claude cowork` — those are the author's OTHER books; would cannibalise.
- `ai trading` / trading bots — 86.7–193% ACOS in ads, money-losing and off-positioning.
- `prompt engineering for generative ai`, `ai prompts to help you make money` — zero conversions.
- `network engineers`, `system design interview` — irrelevant traffic, already ad negatives.

## SUPERSEDED — earlier single 7-keyword set (use the 21 above instead)
Built from ACTUAL converting search terms in the ads Search Terms report, not guesswork.
Rule applied: do NOT spend slots on words already in the title/subtitle — Amazon already indexes
those (claude, ai, finance, professionals, institutional, prompts, financial, analysis, valuation,
investment, research, sample, outputs, plugins, workflows).

1. `claude ai for investment bankers cfo analyst`
2. `generative ai finance handbook manual playbook`
3. `equity research valuation dcf financial modeling`
4. `ai for beginners guide learning made easy`
5. `quantitative finance data analysis automation`
6. `prompt engineering guide llm assistant`
7. `banking private equity hedge fund fintech`

Evidence behind these — converting search terms (purchases / sales):
claude ai for investment bankers (2 / $93.96 — best in account) · claude ai for finance
professionals (2 / $26.98) · claude for finance (2 / $29.98) · claude ai made easy · claude ai
manual · book claude ai pro · using claude for investing · quantitative finance ai · open ai for
finance · claude ai for beginners bible · claude playbook data analysis · learning claude ·
claude ai for cfo

⚠️ **Do NOT put `chatgpt` in KDP keywords.** Using a competitor's trademark to divert search
traffic breaches Amazon's metadata guidelines and risks listing suppression. (It is fine as an
ad NEGATIVE keyword, which is where it already sits.) `claude`/`anthropic` are defensible because
the book genuinely is about that product and the name is already in the title — but that is the
author's risk call, not a guarantee.

## KEYWORD SETS — remaining backlist titles (not yet advertised)
Both are consumer/personal-finance, NOT institutional — different buyer, cheaper clicks.

**Stop Losing Money** (ebook $2.99, royalty $1.50/u @ ~64% → break-even bid ~$0.18, far below the
$0.60 floor). **Do not advertise at current price.** Ebook must be repriced to $4.99+ before ads
are arithmetically possible. If repriced, Exact @ $0.60: investing mistakes book ·
why investors lose money · personal finance mistakes · stop losing money investing

**The Wealth Code of Chhatrapati Shivaji Maharaj** (ebook $2.99, royalty $2.07/u @ 69%
→ break-even bid ~$0.24, also below floor). Same conclusion — reprice before advertising.
If repriced, Exact @ $0.60: shivaji maharaj book · maratha history book ·
indian history wealth · money lessons from history

**Claude AI für Finanzprofis** (German) — advertise on Amazon.de, NOT .com. Needs a separate
DE-marketplace campaign; economics not yet pulled. Exact: claude ai buch · ki für finanzen ·
claude ai finanzen · ki prompts finanzen

## Next steps
1. Get the actual per-format royalty from KDP (Reports → Royalties). Compute break-even ACOS.
2. If break-even < 58%, the target is ACOS reduction, not volume: keep concentrating spend on
   the `claude`-family keywords and the 6 new exacts; pause anything above break-even.
3. Re-evaluate after 7–10 days. Three changes landed simultaneously on 2026-07-20, so attribution
   before then is unreliable.
4. Consider pausing `ai trading` broad (193% ACOS) if it stays above break-even.

## Decisions & gotchas
- **Amazon's UI recommends +5% on Top of search — ignore it.** That placement converts at
  $48.55/purchase, the worst of the three, despite a 7.38% CTR. High clicks, near-zero conversion.
- Placement bid adjustments are **increase-only** (0–900%). Product pages cannot be reduced
  directly; boosting Rest of search crowds it out indirectly because the campaign is budget-capped.
- `ai tools` was deliberately NOT added as a negative — that keyword is already paused so the
  spend cannot recur, and the phrase is too broad. `system design interview` was added instead.
- **Known config conflict:** the enabled keyword `generative ai system design interview` is now
  permanently blocked by the `system design interview` negative. Harmless ($0.30 bid, 0 impressions)
  but should be paused.
- Campaign ran out-of-budget 24 of 28 days at the old $7.71 budget. Now $12/day. **Do not raise it** —
  the user has explicitly ruled this out.
- The winning pattern in search terms is `claude` + a specific role/use case
  (investment bankers, CFO, finance professionals, investing). Generic AI/prompt/trading terms lose money.
- Search Terms report only retains terms with clicks in the last 65 days — pull it before it ages out.

## How to resume
Open the campaign URL above in the user's Chrome, go to Targeting (filter Active status = Enabled)
and Search terms (sort by Purchases, then by Total cost) with the date range set to Lifetime.
Then start at step 1 — do not tune bids further until the royalty rate is known.
