# The 120 Prompts — full CRAFT text

Every numbered prompt from *Claude AI for Finance Professionals*, written out in full CRAFT order — Context, Role, Action, Format, Tone — and ready to copy.

The book prints Role, Task and Output for each prompt. This page adds the Context and Tone layers explicitly, because those are the two you must adapt to your own desk. CRAFT is the framework used in this book. It is not Anthropic documentation.

## Chapter 2 — The Equity Research Desk

### PROMPT 1 — The Benjamin Graham Margin of Safety & Net-Net Screen

> **Finance context (from the book):** Benjamin Graham argued that every stock has an intrinsic value independent of its market price. When the market price falls significantly below that intrinsic value, a margin of safety exists. His net-net screen found companies so cheap that even shutting down the business and recovering only current assets still produced a profit for the investor.

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Senior value analyst applying Benjamin Graham's documented Security Analysis methodology.

ACTION:
Screen [N] stocks in [UNIVERSE] for deep value using Graham's documented criteria.
Graham Net-Net: Current Assets minus Total Liabilities vs Market Cap
Margin of Safety: minimum 33% discount to intrinsic value Financial strength: current ratio >2x, long-term debt limited Earnings stability: positive EPS in each of the last 10 years Dividend record: uninterrupted payments for at least 20 years P/E below 15x, P/Book below 1.5x, combined product <22.5 Graham Number = square root of (22.5 x EPS x Book Value Per Share)

FORMAT: Ranked list with Graham Number, margin of safety %, net-net value, one-line thesis.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The Peter Lynch PEG Ratio & GARP Discovery Framework

> **Finance context (from the book):** GARP means Growth At a Reasonable Price. Peter Lynch's PEG ratio divides P/E by the earnings growth rate. A PEG below 1.0 suggests the stock is priced below its growth rate. Lynch focused on fast growers with low institutional ownership before the market caught on.

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Growth-at-a-reasonable-price analyst applying Peter Lynch's documented GARP methodology.

ACTION:
Screen [UNIVERSE] for GARP opportunities using Lynch's documented framework.
PEG ratio: P/E divided by earnings growth rate. Target: PEG <1.0 Lynch categories: Stalwarts (8-12% growers), Fast Growers (20-25%), Turnarounds, Cyclicals Hidden gems: small/mid-cap with <30% institutional ownership Ten-bagger potential assessment: can this company grow 10x in 10 years?
Avoid: >60% institutional ownership (Lynch's 'overfollowed' warning) Insider ownership: management skin in the game preferred

FORMAT: Categorised GARP list with PEG ratios, Lynch categories, and ten-bagger assessments.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — The AQR Quality-Value-Momentum Multi-Factor Ranking

> **Finance context (from the book):** Academic research identifies three return factors: quality, value, and momentum. Names in the top quintile of all three at once are statistically uncommon. Each factor needs an economic rationale as well as statistical significance.

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Quantitative analyst applying publicly documented multi-factor investing research.

ACTION:
Apply AQR's documented QVM multi-factor model to rank [UNIVERSE]. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.
Quality factor (per AQR Asness et al. published research): Profitability: gross profits/assets, ROE, ROA, cash flow/assets Growth: 5yr growth in profitability measures
Safety: low beta, low leverage, high Altman Z-score Value factor: book-to-market, earnings yield, cash flow yield Momentum factor: 12-1 month return (excluding last month) Composite: equal-weight Quality + Value + Momentum z-scores Flag: stocks in top quintile of ALL three factors simultaneously

FORMAT: Factor scores, composite ranking, and triple-overlap identification.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — The Macro-Aware Earnings-Yield Spread & Valuation Framework

> **Finance context (from the book):** Two numbers are both called the equity risk premium. The forward ERP is what investors require over the risk-free rate. It is 5.20% for the US on Damodaran's 2026 estimate, and it is the CAPM and WACC input. The earnings-yield spread is the S&P 500 forward earnings yield minus the 10yr Treasury yield. It is 47bps now, against a twenty-year average of 3.2%. It gauges how richly equities sit against

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Senior strategist applying PIMCO's publicly documented macro-aware equity valuation approach.

ACTION:
Assess the earnings-yield spread and relative value of [MARKET/SECTOR/COMPANY]. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.
Earnings-yield spread: forward earnings yield minus risk-free rate Historical context: current spread vs 20-year average Forward ERP for cost of equity: state the source and date separately from the spread Real yield analysis: nominal yield minus inflation expectations Cross-asset relative value: equities vs credit vs bonds vs commodities

FORMAT: Spread analysis with cross-asset relative value and positioning context.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 7 — The Macro-Driven Sector Rotation & Cycle Positioning

> **Finance context (from the book):** Different sectors tend to perform differently at different stages of the economic cycle. Sector rotation involves adjusting weights in anticipation of cycle transitions, using EV/EBITDA vs historical averages and earnings growth estimates as the primary signals.

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Chief equity strategist with expertise in economic cycle analysis and sector allocation.

ACTION:
Optimal sector positioning for next 6-12 months given current macro environment.
Economic cycle stage: Early / Mid / Late expansion or Contraction For each of the 11 GICS sectors: Historical performance in current cycle stage Current EV/EBITDA vs 5yr historical average NTM EPS growth consensus estimate Specific macro catalyst with timing estimate Specific invalidating condition Conviction: HIGH / MEDIUM / LOW Recommend: 3 overweights, 2 underweights My macro view: [DESCRIBE IN 2-3 SENTENCES]

FORMAT: Sector rotation brief. Overweight/underweight table with conviction levels.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Buy-Side Full Due Diligence Research Note

> **Finance context (from the book):** A full due diligence note combines business quality, financial analysis, valuation, and risk assessment into a single document. The pre-mortem exercise, imagining the investment has already failed and working backwards, is the most practical way to find analytical blind spots before an IC presentation.

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Managing Director at a large sell-side firm preparing a full IC package for a new position. Apply the standard you would defend to the committee.

ACTION:
Full institutional due diligence on [COMPANY], [TICKER]. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.
Ask Claude: 'Using the latest publicly available financials for [COMPANY]:'
Business quality: revenue model, moat type, moat trajectory Financial quality: Revenue CAGR 3yr, EBITDA margin, FCF conversion, leverage Management: capital allocation track record, insider ownership, succession Valuation: DCF with WACC + TGR sensitivity, EV/EBITDA vs peers, P/FCF vs history Three 12-month catalysts with magnitude and probability each Two bear cases: specific mechanistic path to loss, probability, magnitude Position size: core 3-5%, standard 1-3%, watch <1% Pre-mortem: most credible path to being wrong

FORMAT: IC-ready research note. Assumption log required.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```


## Chapter 3 — The M&A Valuation Desk

### PROMPT 1 — The Institutional Buy-Side DCF Valuation Model

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Managing Director at a large sell-side firm building the M&A DCF, the number the board pack rests on. Apply the standard you would defend in that room.

ACTION:
Build a complete DCF for [COMPANY], [TICKER]. Five-year revenue projections by segment. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: Investment banking valuation memo. BCE only. Source every assumption.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The Institutional Cost of Capital Construction

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Senior financial analyst specialising in defensible WACC estimation.

ACTION:
Build a fully sourced WACC for [COMPANY] in [COUNTRY/MARKET]. RF rate with exact source and date. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: WACC table with every component sourced. Sensitivity analysis included.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 3 — The Institutional Peer Group Valuation Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Senior equity analyst building a sourced peer group valuation.

ACTION:
Comparable company analysis for [TARGET] vs [N]-company peer group. State peer inclusion/exclusion rationale. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: Comps table with implied valuation range and premium/discount analysis.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — The Private Equity Leveraged Buyout Returns Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Private equity analyst building sponsor acquisition returns analysis.

ACTION:
Complete LBO analysis for [COMPANY]. Entry EV/EBITDA: [X]-[X]x. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: 

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — The M&A Control Premium & Transaction Multiple Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Senior M&A banker analysing transaction multiples and control premiums.

ACTION:
Precedent transactions for [SECTOR], last [N] years, deal >[CUR][X]. For each: acquirer, target, date, EV, EV/EBITDA, EV/Revenue, control premium.

FORMAT: Transaction table with control premium analysis and implied target range.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 6 — The Conglomerate SOTP & Break-Up Value Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Managing Director at a large sell-side firm applying SOTP methodology. Value each segment as you would defend it to the board.

ACTION:
SOTP valuation for [COMPANY] with [N] business segments. Per segment: appropriate methodology and pure-play comparable. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: SOTP table with conglomerate discount and implied value vs current market cap.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Investment Banking Fairness Opinion Analytical Structure

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Managing Director at a large sell-side firm preparing the analytical structure for a board fairness opinion. Apply the standard you would defend in that room.

ACTION:
Fairness opinion analytical framework for [TARGET] at [CONSIDERATION]. Methods: DCF, comparable companies, precedent transactions, LBO floor, 52-week trading range. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: Football field with methodology ranges and majority fairness assessment.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```


## Chapter 4 — The Macro Risk Desk

### PROMPT 1 — The Ray Dalio All-Weather Portfolio Environment Assessment

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Senior risk analyst applying the Dalio All-Weather portfolio framework.

ACTION:
Assess current portfolio against Dalio's four economic environments: rising growth/rising inflation, rising growth/falling inflation, falling growth/rising inflation, falling growth/falling inflation. Map each major position to its environment sensitivity. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: All-Weather assessment with environment mapping and rebalancing recommendation.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The Macro Hedge Fund Risk Assessment

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Macro hedge fund risk analyst assessing systematic factor exposures.

ACTION:
Systematic risk assessment for [PORTFOLIO]. Factor exposures: growth, value, quality, momentum, duration, currency. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: Risk assessment with factor exposures and stress test results.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 3 — The Deep Portfolio Vulnerability & Assumption Challenge

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Portfolio manager applying radical transparency to stress-test core assumptions.

ACTION:
Challenge five key portfolio assumptions. For each: state the assumption, the evidence supporting it, the evidence against it, and what happens to the portfolio if the assumption is wrong.

FORMAT: Assumption challenge table with portfolio impact per assumption.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — The Multi-Scenario Historical & Hypothetical Stress Test

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Managing Director at a large sell-side firm running the stress scenarios the board will see. Apply the standard you would defend in that room.

ACTION:
Multi-scenario stress test for [PORTFOLIO]: 2022 Rate Shock (equities -18%, long bonds -31%), 2008 GFC (equities -38%, credit spread +300bps), 2020 COVID Crash (equities -34%, recovery V-shaped), custom scenario [DESCRIBE]. Portfolio P&L per position in each. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: Stress test results by position and scenario with comparison table.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — The Institutional Tail Risk Quantification & Hedging Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Institutional risk analyst quantifying tail risk and hedging costs.

ACTION:
Tail risk quantification for [PORTFOLIO]. CVaR at 95% and 99%. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: Tail risk metrics with hedging recommendations and cost analysis.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 6 — The Multi-Currency Portfolio FX Exposure & Hedging Strategy

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Portfolio strategist managing multi-currency FX exposure and hedge ratios.

ACTION:
FX exposure analysis for [PORTFOLIO]. Map all positions to underlying currency exposures including indirect (e.g.

FORMAT: FX exposure map with hedge ratio recommendation and instrument selection.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Portfolio Drawdown Attribution & Recovery Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Managing Director at a large sell-side firm attributing drawdown sources for the board. Separate factor losses from selection losses as you would defend them in that room.

ACTION:
Drawdown attribution for [PORTFOLIO] over [PERIOD]. Decompose total drawdown into: factor contributions (growth, value, quality, momentum), sector contributions, and idiosyncratic stock contributions. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: Drawdown attribution table with factor and stock decomposition.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```


## Chapter 5 — The Earnings Intelligence Desk

### PROMPT 1 — The Institutional Pre-Earnings Intelligence Brief

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Managing Director at a large sell-side firm signing off on the pre-earnings brief before the print. Apply the standard you would defend after the result is known.

ACTION:
Pre-earnings intelligence brief for [COMPANY], reporting in [N] days. Three thesis-critical KPIs with consensus estimate and your estimate.

FORMAT: Pre-earnings brief with decision matrix. Commit all actions before the print.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The Management Tone Trajectory Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Senior research analyst applying systematic management tone analysis.

ACTION:
Analyse last four earnings call transcripts for [COMPANY]. Per quarter: rate CONSTRUCTIVE/NEUTRAL/CAUTIOUS/MORE CAUTIOUS.

FORMAT: Tone trajectory table with keyword frequency shifts and synthesis.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 3 — The Management Guidance Reliability Scorecard

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Equity analyst building a guidance quality and credibility scorecard.

ACTION:
Guidance quality analysis for [COMPANY] over last 8 quarters. For each: guided metric, guided range, actual result, beat/miss, magnitude.

FORMAT: Guidance accuracy scorecard with credibility rating and bias assessment.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — The Institutional Segment-Level Revenue Intelligence Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Sector analyst decomposing segment-level revenue and mix dynamics.

ACTION:
Segment revenue intelligence for [COMPANY]. For each segment: revenue, growth rate, margin, management commentary. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: Segment decomposition with emphasis analysis and mix attribution.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — The Forensic Earnings Quality & Cash Conversion Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Forensic analyst assessing earnings quality and cash conversion.

ACTION:
Forensic earnings quality analysis for [COMPANY]. Sloan accruals ratio (should be near zero). Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: Earnings quality scorecard with red flags and cash conversion analysis.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 6 — The Consensus Estimate Positioning & Expectations Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Senior analyst mapping consensus positioning and sentiment extremes.

ACTION:
Consensus positioning analysis for [COMPANY] before [EVENT]. % of analysts with buy/hold/sell ratings.

FORMAT: Consensus positioning map with sentiment extremes identified.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 7 — The Institutional Post-Earnings Position Management

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Managing Director at a large sell-side firm executing the pre-committed post-earnings protocol. Apply the standard you would defend to the committee: the matrix decides, the record shows it.

ACTION:
Post-earnings position management protocol for [COMPANY] following [RESULT]. Assess: did KPIs meet pre-committed thresholds? Apply pre-committed decision matrix.

FORMAT: Post-earnings decision record with thesis update and position action.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Multi-Company Earnings Season Monitoring

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Research team lead managing multi-company earnings season monitoring.

ACTION:
Earnings season monitoring dashboard for [N] coverage names. Build a calendar with reporting dates, KPI thresholds, and pre-committed actions for each.

FORMAT: 

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```


## Chapter 6 — The Portfolio Strategy Desk

### PROMPT 1 — The Institutional Investment Policy Statement Construction

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Managing Director at a large sell-side firm constructing the Investment Policy Statement the client will sign. Apply the standard you would defend to the investment committee.

ACTION:
Build a complete Investment Policy Statement for [CLIENT/FUND].
RRTTLLU framework: Return objective (specific % or benchmark+X%), Risk tolerance (max drawdown, tracking error), Time horizon (years), Tax (jurisdiction and treatment), Liquidity (annual needs), Legal (mandate constraints), Unique (specific exclusions/requirements).

FORMAT: IPS policy document with all seven RRTTLLU dimensions documented.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The Strategic Asset Allocation & Risk Budgeting Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Senior portfolio manager building strategic asset allocation and risk budget.

ACTION:
Strategic Asset Allocation for [FUND]. Asset classes: global equity, fixed income, alternatives, real assets, cash. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: SAA with efficient frontier analysis and risk budget allocation.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 3 — The Tactical Asset Allocation & Factor Tilt Protocol

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Tactical strategist designing active tilts around the strategic allocation.

ACTION:
Tactical asset allocation overlay for [FUND] vs SAA. Current market conditions: [DESCRIBE BRIEFLY].

FORMAT: TAA overlay with specific tilts, rationale, and reversal conditions.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — The GIPS-Compliant Performance Reporting Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: GIPS-compliant performance reporting specialist.

ACTION:
GIPS-compliant performance reporting for [COMPOSITE] for period [DATES]. Time-weighted return calculation. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: GIPS-compliant performance report with all required disclosures.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — The Institutional Portfolio Rebalancing Policy & Execution

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Portfolio operations analyst managing rebalancing policy and execution.

ACTION:
Portfolio rebalancing analysis for [FUND]. Current weights vs SAA targets.

FORMAT: Rebalancing trade list with cost analysis and execution priority.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 6 — The Multi-Asset Portfolio Construction & Optimisation

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Multi-asset portfolio construction specialist.

ACTION:
Multi-asset portfolio construction for [MANDATE]. Asset class selection rationale.

FORMAT: Portfolio construction blueprint with diversification analysis.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 7 — The Client Portfolio Review & Communication Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Managing Director at a large sell-side firm presenting the portfolio review to the client's investment committee. Apply the standard you would defend in that room.

ACTION:
Client portfolio review for [CLIENT]. Performance vs IPS return objective.

FORMAT: 

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Institutional Risk-Adjusted Return Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Risk-adjusted performance analyst decomposing attribution by decision type.

ACTION:
Risk-adjusted return analysis for [PORTFOLIO] over [PERIOD]. Standing rule: after any multi-step numerical work, write and run a Python script recomputing every derived figure from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.
Sharpe ratio, Sortino ratio, Calmar ratio, Information ratio vs benchmark.

FORMAT: Risk-adjusted return report with full attribution decomposition.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```


## Chapter 7 — The Quant Trading Desk

### PROMPT 1 — The Statistical Edge Discovery & Pattern Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Quantitative researcher identifying statistically significant, economically-justified patterns.

ACTION:
Identify statistically significant patterns for [TICKER] over [TIME PERIOD]. Seasonal patterns: best/worst calendar months with p-value and sample size.

FORMAT: Pattern table with p-values, sample sizes, and economic rationale.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The Technical Analysis & Chart Pattern Recognition Protocol

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Technical analyst applying multi-timeframe trend and momentum analysis.

ACTION:
Technical analysis for [TICKER]. Trend identification: daily/weekly/monthly alignment.

FORMAT: Technical analysis brief with entry/stop/target and R:R flagged if below 2:1.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 3 — The Options Strategy & Derivatives Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Derivatives specialist analysing options strategies and Greeks.

ACTION:
Options strategy analysis for [UNDERLYING]. Current implied vol vs historical vol: is optionality cheap or expensive? Relevant strategies: covered call, protective put, collar, straddle/strangle.

FORMAT: Options strategy comparison with P&L profiles and Greeks.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — The Institutional Investment Strategy Backtesting Engine

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Quantitative strategist running systematic backtesting with walk-forward validation.

ACTION:
Backtest [STRATEGY] on [UNIVERSE] over [PERIOD]. Signal: [DESCRIBE LOGIC].

FORMAT: Backtest results with walk-forward validation. In-sample and out-of-sample reported separately.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — The High-Frequency Signal & Market Microstructure Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Market microstructure analyst assessing order flow and institutional positioning.

ACTION:
Market microstructure analysis for [TICKER]. Bid-ask spread: current vs historical average.

FORMAT: Microstructure signals with order flow and short interest analysis.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 6 — The Cross-Asset Momentum & Relative Value Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Cross-asset strategist building relative value and momentum frameworks.

ACTION:
Cross-asset relative value analysis. Compare [ASSET CLASS 1] vs [ASSET CLASS 2] on: yield/earnings yield, real yield, z-score vs 20yr history, current positioning (crowded or under-owned).

FORMAT: Cross-asset relative value table with positioning recommendation.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 7 — The Quantitative Portfolio Optimisation

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Portfolio optimisation specialist applying mean-variance with constraints.

ACTION:
Quantitative portfolio optimisation for [UNIVERSE]. Inputs: expected returns (factor model), covariance matrix (historical + shrinkage), constraints (max position [X]%, max sector [X]%, min diversification).

FORMAT: Optimal portfolio weights with efficient frontier and sensitivity analysis.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Institutional Trade Plan & Risk Management

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Head of trading at a multi-strategy fund, constructing the pre-committed trade plan to be defended before the risk committee.

ACTION:
Complete trade plan for [TICKER] before initiating any position.
Investment thesis: 2 sentences.

FORMAT: Complete pre-committed trade plan. All levels documented before any position is taken.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```


## Chapter 8 — The Strategy Consulting Desk

### PROMPT 1 — The Institutional Competitive Landscape & Market Structure

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Senior strategy analyst mapping competitive landscape and market structure.

ACTION:
Competitive landscape analysis for [SECTOR/INDUSTRY]. Top 5-7 companies by revenue/market cap.

FORMAT: Competitive landscape table with moat assessment and trajectory.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The Porter Five Forces Industry Attractiveness Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Industry analyst applying Porter's Five Forces framework.

ACTION:
Porter Five Forces analysis for [INDUSTRY]. Each force: rate intensity LOW/MEDIUM/HIGH with specific evidence.

FORMAT: Five Forces scorecard with attractiveness rating and investment implication.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 3 — The Competitive Advantage Period & Moat Width Assessment

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Equity analyst assessing competitive advantage period and moat durability.

ACTION:
Competitive advantage period (CAP) assessment for [COMPANY]. For each moat type present (brand, cost, network, switching): evidence, durability (years), trajectory.

FORMAT: Moat width assessment with CAP estimate and durability evidence.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — The Channel-Level Market Share & Competitive Dynamics Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Channel intelligence analyst tracking market share at the distribution level.

ACTION:
Channel-level market share analysis for [COMPANY] vs [COMPETITOR].
Distribution channels: [LIST].

FORMAT: Channel market share table with 8-quarter trend and divergence analysis.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — The Institutional SWOT & Strategic Position Assessment

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Strategic analyst building an evidence-backed SWOT assessment.

ACTION:
SWOT analysis for [COMPANY]. Each item must have specific evidence and a magnitude estimate, not a generic statement.

FORMAT: Evidence-backed SWOT with strategic priorities and threat mitigation plan.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 6 — The Technology Disruption & Business Model

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Technology disruption analyst evaluating competitive threat timelines.

ACTION:
Technology disruption assessment for [COMPANY]. Identify 3-4 technology threats: what technology, which competitor is deploying it, timeline, potential revenue impact.

FORMAT: Disruption threat assessment with timeline and response capability rating.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 7 — The Institutional Pricing Power & Revenue Quality Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Revenue quality analyst decomposing pricing power and margin flow-through.

ACTION:
Pricing power analysis for [COMPANY]. Revenue decomposition: price contribution vs volume contribution last 5 years.

FORMAT: 

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Single Best Investment Thesis Construction

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Managing Director at a large sell-side firm, constructing the single best investment thesis to be defended before the investment committee.

ACTION:
Single best investment thesis for [COMPANY]. What: one paragraph describing the business and why it is mispriced.

FORMAT: Investment thesis document with catalyst, KPIs, and invalidating condition.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```


## Chapter 9 — The Endowment Strategy Desk

### PROMPT 1 — The Yale/Harvard Endowment SAA Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: CIO of the endowment, applying the Yale/Harvard SAA framework and presenting the allocation to the investment committee.

ACTION:
Yale/Harvard endowment SAA framework for [INSTITUTION], [AUM].
Asset classes: public equity, fixed income, PE/VC, real assets, hedge funds, real estate.

FORMAT: Endowment SAA with spending policy sustainability analysis.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The Illiquidity Premium & Alternative Asset Allocation Protocol

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Alternative investments specialist quantifying illiquidity premium and budget.

ACTION:
Illiquidity premium analysis for [PORTFOLIO]. For each illiquid asset class (PE, VC, real estate, infrastructure): expected return premium over liquid equivalent, historical realised premium, time horizon required, governance requirements.

FORMAT: Illiquidity premium table with budget calculation and governance requirements.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 3 — The Private Equity & Venture Capital Allocation Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: PE and VC allocation specialist designing vintage diversification strategy.

ACTION:
PE and VC allocation framework for [ENDOWMENT/FUND]. Vintage year diversification: target number of commitments per year.

FORMAT: PE/VC allocation framework with vintage diversification and manager selection criteria.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — The Endowment Spending Policy & Perpetuity Assessment

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: CIO of the endowment, stress-testing spending policy sustainability for the investment committee.

ACTION:
Endowment spending policy analysis for [INSTITUTION]. Current spending rate vs long-run real return assumption.

FORMAT: Spending policy sustainability model with three scenarios and rule options.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — The Real Assets & Infrastructure Allocation Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Real assets allocation specialist mapping inflation linkage and income.

ACTION:
Real assets allocation analysis for [PORTFOLIO]. Asset classes: listed infrastructure, direct infrastructure, farmland, timber, commodities, TIPS.

FORMAT: Real assets allocation with inflation linkage and liquidity analysis.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 6 — The Manager Selection & Due Diligence Protocol

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Alternatives due diligence specialist scoring manager selection criteria.

ACTION:
Manager selection due diligence for [STRATEGY/ASSET CLASS].
Evaluation framework: track record (length, market cycles covered), team (tenure, key person risk), process (repeatable, documented), risk management (drawdown history, risk controls), fees (management fee, carry, hurdle).

FORMAT: Manager evaluation scorecard with weighted scores and selection recommendation.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 7 — The Endowment Rebalancing & Liquidity Management

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Endowment operations analyst managing rebalancing and liquidity.

ACTION:
Endowment rebalancing and liquidity management for [INSTITUTION].
Rebalancing triggers: which asset classes have drifted beyond bands? Cash generation: which illiquid positions have distributions pending? Capital calls: which commitments are due in next 12 months? Net liquidity position: surplus or deficit?

FORMAT: 

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Multi-Generational Wealth Preservation Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Family office or endowment strategist designing multi-generational framework.

ACTION:
Multi-generational wealth preservation framework for [FAMILY/INSTITUTION]. Objectives across three time horizons: current generation (10yr), next generation (30yr), perpetuity.

FORMAT: Multi-generational framework with time-horizon allocation and governance structure.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```


## Chapter 10 — The Sovereign Wealth Desk

### PROMPT 1 — The NBIM Norway GPFG Total Portfolio Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: CIO of the sovereign wealth fund, presenting the total portfolio framework to the board.

ACTION:
Total portfolio framework for [SOVEREIGN FUND], [$AUM]. SAA: equity/fixed income/real assets target weights with rationale.

FORMAT: Total portfolio framework document with geographic allocation and mandate rationale.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The Responsible Investment & ESG Integration Protocol

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Responsible investment officer designing ESG integration and engagement policy.

ACTION:
Responsible investment and ESG integration protocol for [INSTITUTION]. Exclusion criteria: define categories and specific tests.

FORMAT: Responsible investment policy with exclusion criteria, engagement protocol, and reporting framework.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 3 — The Geographic Diversification & Home Bias Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Global portfolio strategist quantifying geographic diversification and home bias.

ACTION:
Geographic diversification analysis for [PORTFOLIO]. Current geographic weights vs global market cap weights.

FORMAT: Geographic diversification table with home bias quantification and recommendation.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — The Long-Horizon Factor Allocation Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Long-horizon factor allocation specialist applying sovereign mandate design.

ACTION:
Long-horizon factor allocation framework for [SOVEREIGN FUND].
Factors: market, size, value, quality, low volatility, momentum.

FORMAT: Factor allocation framework with academic evidence and implementation guidance.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — The CPPIB Total Portfolio Approach

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Total portfolio approach specialist implementing the CPPIB framework.

ACTION:
CPPIB Total Portfolio Approach implementation for [INSTITUTION].
Reference portfolio: passive market cap-weighted equivalent.

FORMAT: Total Portfolio Approach framework with reference portfolio and active risk budget.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 6 — The Sovereign Credit & Fixed Income Allocation Protocol

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Fixed income strategist building sovereign credit and yield curve allocation.

ACTION:
Sovereign credit and fixed income allocation for [FUND]. Universe: developed market sovereigns, EM sovereigns, IG credit.

FORMAT: Fixed income allocation with duration analysis and yield curve positioning.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 7 — The Currency Overlay & FX Risk Management

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Currency overlay specialist managing multi-currency exposure and hedging.

ACTION:
Currency overlay framework for [PORTFOLIO]. Identify all currency exposures including indirect.

FORMAT: Currency overlay design with cost-benefit analysis per currency pair.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Governance & Accountability Reporting System

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Governance officer designing accountability and transparency reporting.

ACTION:
Governance and accountability reporting framework for [SOVEREIGN INSTITUTION]. Decision-making: investment committee structure, delegation authority, escalation path.

FORMAT: Governance framework with decision-making structure and reporting requirements.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```


## Chapter 11 — The ESG & Climate Desk

### PROMPT 1 — The TCFD Four-Pillar Climate Disclosure Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: ESG analyst applying the TCFD four-pillar climate risk framework.

ACTION:
TCFD four-pillar analysis for [COMPANY]. Pillar 1 Governance: board oversight, management roles, compensation links.

FORMAT: TCFD four-pillar disclosure table with scenario analysis and metrics.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The EU SFDR Article Classification Protocol

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Regulatory compliance analyst determining SFDR Article classification.

ACTION:
SFDR Article classification analysis for [FUND]. Determine whether the fund qualifies as Article 6 (no ESG integration), Article 8 (ESG characteristics), or Article 9 (ESG primary objective).

FORMAT: SFDR classification recommendation with evidence and disclosure obligations.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 3 — The Carbon Intensity & Net-Zero Pathway Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Climate investment specialist calculating WACI and net-zero pathway.

ACTION:
Carbon intensity and net-zero pathway analysis for [PORTFOLIO].
Calculate WACI (Weighted Average Carbon Intensity) for the portfolio.

FORMAT: WACI calculation with net-zero pathway and top contributor identification.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — The Physical Climate Risk & Stranded Asset Assessment

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Physical risk analyst mapping asset-level climate hazard exposure.

ACTION:
Physical climate risk assessment for [PORTFOLIO]. Asset locations: map each holding's key physical assets to climate hazard exposure.

FORMAT: Physical risk map with hazard exposure by asset and time horizon.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — The ESG Score Integration & Factor Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: ESG factor analyst integrating scores with financial attribution.

ACTION:
ESG score integration for [PORTFOLIO]. Data source: [PROVIDER].

FORMAT: ESG score integration with factor analysis and engagement priorities.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 6 — The Shareholder Engagement & Voting Policy Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Responsible investment officer designing engagement and voting policy.

ACTION:
Shareholder engagement and voting policy for [INSTITUTION].
Priority engagement issues: climate, executive compensation, board composition, human rights.

FORMAT: Engagement policy with voting stances and escalation framework.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 7 — The Impact Measurement & SDG Alignment Protocol

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Impact measurement specialist aligning portfolio to UN SDG goals.

ACTION:
Impact measurement framework for [FUND/PORTFOLIO]. Select 3-5 SDG goals most relevant to portfolio.

FORMAT: Impact measurement framework with SDG alignment and additionality assessment.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Climate Scenario Analysis & Portfolio Stress Test

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Head of responsible investment, presenting the climate stress test and positioning recommendation to the investment committee.

ACTION:
Climate scenario analysis and portfolio stress test for [PORTFOLIO]. Scenarios: Orderly transition (Net Zero 2050), Disorderly transition (Delayed action then sudden), Hot house world (No action, physical risk dominates).

FORMAT: Climate scenario portfolio stress test with sector analysis and positioning recommendation.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```


## Chapter 12 — The Fixed Income & Credit Desk

### PROMPT 1 — The Institutional Credit Analysis & Scoring Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Credit analyst applying institutional credit assessment and scorecard.

ACTION:
Credit analysis for [COMPANY] using institutional framework.
Scorecard: Net Debt/EBITDA, interest coverage, FCF/total debt, Altman Z-Score.

FORMAT: Credit scorecard with trend analysis and rating recommendation.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The Duration & Convexity Risk Management

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Fixed income portfolio manager managing duration and convexity risk.

ACTION:
Duration and convexity analysis for [FIXED INCOME PORTFOLIO]. DV01 per position.

FORMAT: Duration profile with key rate durations and liability matching analysis.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 3 — The Credit Spread Attribution & Curve Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Credit attribution specialist decomposing spread return components.

ACTION:
Credit spread attribution for [FIXED INCOME PORTFOLIO] over [PERIOD]. Total excess return vs duration-matched Treasuries.

FORMAT: Credit spread attribution by source, sector, and rating.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — The Covenant Analysis & Distressed Credit Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Distressed credit analyst mapping covenant headroom and breach scenarios.

ACTION:
Covenant analysis for [COMPANY/BOND ISSUE]. List all financial covenants: type (maintenance vs incurrence), metric, threshold, current level, headroom.

FORMAT: Covenant analysis with headroom calculation and breach scenario.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — The LDI & Liability-Matching Portfolio Construction

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Pension fund analyst applying liability-driven investing (LDI) framework.

ACTION:
LDI liability matching analysis for [PENSION FUND/INSTITUTION].
Liability profile: present value, duration, key rate exposures.

FORMAT: Liability matching analysis with duration gap and hedging instruments.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 6 — The Fixed Income Portfolio Construction & Optimisation

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Fixed income portfolio construction specialist applying credit mandate rules.

ACTION:
Fixed income portfolio construction for [MANDATE]. Credit quality minimum.

FORMAT: Fixed income portfolio blueprint with credit quality, duration, and concentration rules.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 7 — The Yield Curve Strategy & Positioning

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Managing Director on the rates desk at a large sell-side firm, recommending curve positioning to the investment committee.

ACTION:
Yield curve strategy for [FIXED INCOME PORTFOLIO]. Current curve shape: flat/steep/inverted/humped.

FORMAT: Yield curve positioning strategy with carry analysis and instrument selection.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Credit Default Probability & Recovery Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Credit risk analyst modelling default probability and recovery rates.

ACTION:
Credit default probability and recovery analysis for [ISSUER].
Default probability: Merton model (equity vol and leverage), market-implied (CDS spread / (1-Recovery)), rating agency historical default rates by rating.

FORMAT: 

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```


## Chapter 13 — Claude Model Family

### PROMPT 1 — Model Selection and Cost Optimisation

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Institutional AI deployment specialist, covering Claude model selection and cost optimisation.

ACTION:
Select the optimal Claude model for each task in your finance workflow. For bulk extraction (N>20 items): Haiku 4.5.

FORMAT: Model routing framework with cost analysis and team routing rules.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The High-Speed Universe Screening & Data Extraction Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Research operations lead, designing Haiku bulk extraction pipelines.

ACTION:
Design a Haiku 4.5 bulk screening pipeline. Input: [N] company annual reports or filings.

FORMAT: Bulk extraction pipeline design with quality validation and overnight scheduling.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 3 — Output Standards Configuration

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Compliance and AI standards officer, configuring institutional output standards.

ACTION:
Configure Sonnet 5 output standards for institutional finance use. System prompt elements: BCE-only language, assumption log required, risk caveats on forward-looking statements, compliance footer.

FORMAT: Configured output standard with compliance verification results.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — The Extended Multi-Layer Reasoning Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Managing Director at a large sell-side firm, reviewing this Opus 4.8 extended-reasoning memo before it goes to the investment committee.

ACTION:
Apply Opus 4.8 extended reasoning to a complex IC memo for [COMPANY]. Use extended thinking mode: the model shows its reasoning chain before the conclusion.

FORMAT: IC memo with extended reasoning chain and quality comparison vs Sonnet.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — The Claude Finance Agent Capability Assessment

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: AI workflow auditor, assessing Claude capability fit for finance use cases.

ACTION:
Assess Claude's capability for [SPECIFIC FINANCE WORKFLOW]. Test cases: 5 representative tasks from this workflow.

FORMAT: Capability assessment scorecard with hit rate and workflow fit evaluation.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 6 — The Institutional AI Cost Management & Budget Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Finance operations manager, building AI cost management and governance.

ACTION:
Design an AI cost management framework for [TEAM/INSTITUTION]. Map all AI tasks by volume and complexity. Standing rule: after the budget model is built, write and run a Python script recomputing every derived figure (monthly costs, savings, volume totals) from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: AI cost management framework with budget model and governance rules.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 7 — Multi-Model Pipeline Architecture

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: AI infrastructure architect, designing multi-model pipeline for finance teams.

ACTION:
Design a multi-model pipeline for [FINANCE WORKFLOW]. Stage 1 (Haiku): extraction and classification.

FORMAT: Multi-model pipeline architecture with data flow and quality gates.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Norway GPFG AI-at-Scale Institutional Deployment Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Institutional AI deployment lead, NBIM-inspired at-scale model architecture.

ACTION:
Design an AI-at-scale institutional deployment for [INSTITUTION] covering [N] portfolio companies. Three-stage architecture: Haiku for overnight bulk, Sonnet for escalation reports, Opus for complex analysis. Standing rule: write and run a Python script recomputing every cost figure (per-stage totals, saving versus single-model routing) from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: AI deployment architecture with governance, cost model, and efficiency analysis.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```


## Chapter 14 — Claude.ai Platform

### PROMPT 1 — The Institutional Claude Project Configuration Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Research team lead — configuring Claude Projects for coverage universe.

ACTION:
Configure a Claude Project for [YOUR COVERAGE UNIVERSE / FUND].
System prompt: fund mandate, benchmark, investment philosophy, BCE-only language rule, output format preferences, compliance footer.

FORMAT: Project configuration with system prompt and verification test results.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The Claude Deep Research Sector Initiation Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Senior analyst — using Deep Research for sector initiation.

ACTION:
Use Claude Deep Research for a sector initiation on [SECTOR].
Query: summarise the competitive landscape, key players, growth drivers, and main risks for this sector.

FORMAT: Sector initiation research output with source verification and gap analysis.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 3 — The Multi-Quarter Transcript Intelligence Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Equity analyst — multi-quarter transcript intelligence in a Project.

ACTION:
Load [N] earnings call transcripts for [COMPANY] into a Project.
Query: build a management credibility scorecard. Did management's language in each quarter predict the subsequent quarter's results?
Track specific language shifts vs subsequent guidance changes.

FORMAT: Multi-quarter transcript intelligence with management credibility scorecard.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — The Automated Prior Period vs Current Period Document Analysis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Research analyst — automated prior vs current period document comparison.

ACTION:
Upload [COMPANY]'s FY[X] and FY[Y] annual reports into a Project.
Query: what changed between the two years? Focus on: risk factor additions/removals, business description changes, forward-looking language shifts.

FORMAT: Prior period vs current period document comparison with financial significance flags.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — The Full Sector Initiation & Coverage Launch Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Managing Director at a large sell-side firm — signing off the sector initiation before coverage launches.

ACTION:
Launch full coverage on [SECTOR] using a Project with all available annual reports, recent earnings transcripts, and industry primers uploaded. Build: competitive landscape, financial comparison across [N] companies, sector risks, and a ranking of companies by investment attractiveness. Standing rule: after the financial comparison is built, write and run a Python script recomputing every derived figure (margins, medians, ranking inputs) from stated inputs; print PASS/FAIL per check; correct and rerun until all pass.

FORMAT: Full sector coverage launch pack with competitive analysis and company ranking.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 6 — The Long-Running Project Context Optimisation

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: AI workflow optimiser — auditing and improving Project context configuration.

ACTION:
Audit the context configuration of an existing Project. What is in the system prompt? What documents are loaded? Is context being used efficiently? Are any documents rarely queried? Propose optimisations: what to add, remove, or restructure to make each session more productive.

FORMAT: Project context audit with optimisation recommendations.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 7 — The Real-Time Portfolio Event & Signal Monitoring

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Portfolio monitoring lead — real-time event and signal monitoring workflow.

ACTION:
Configure a real-time portfolio monitoring workflow in a Project.
Daily trigger: new filings, news, or price moves for coverage universe.

FORMAT: Portfolio monitoring workflow with materiality filter and PM alert template.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Multi-Source Intelligence Aggregation & Synthesis

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Research synthesis specialist — multi-source intelligence aggregation.

ACTION:
Multi-source synthesis task: load [COMPANY]'s 10-K, last 4 earnings transcripts, and 3 recent sell-side research notes into a Project. Query: synthesise the bull and bear case from all sources.

FORMAT: Multi-source synthesis with agreement/disagreement analysis and coverage gaps.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```


## Chapter 15 — Claude Code for Quant Finance

### PROMPT 1 — The Institutional Monte Carlo Portfolio VaR Implementation

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Quantitative risk engineer — specifying and reviewing Monte Carlo VaR in Python.

ACTION:
Ask Claude Code to write a complete Monte Carlo VaR engine in Python. Specification: 10,000 simulations, 252-day horizon, Student-t distribution (dof=5), Cholesky decomposition for correlations, 2022 stress scenario (equity-bond correlation = +0.60). Validation lives in the repo's CLAUDE.md standing rule: every derived figure (VaR, CVaR, drawdowns) recomputed by a Python script from stated inputs, PASS/FAIL per check.

FORMAT: 

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The Python DCF Model

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Financial modeller — specifying and validating DCF automation in Python.

ACTION:
Ask Claude Code to build a complete Python DCF model for [COMPANY]. Specification: 5-year revenue projections by segment, WACC calculation with sourced inputs, terminal value via two methods (Gordon Growth + exit multiple), 3x3 sensitivity table (WACC x TGR), formatted Excel export. The repo's CLAUDE.md standing rule applies: every derived figure (WACC, terminal value, per-share bridge) recomputed by script, PASS/FAIL per check.

FORMAT: Claude Code builds the DCF scaffolding. Analyst verifies: revenue growth assumptions, WACC inputs, terminal value methodology, sensitivity table logic.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 3 — The Options Pricing & Greeks Calculator Framework

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Derivatives quant — specifying and reviewing Black-Scholes options pricer.

ACTION:
Ask Claude Code to build a Black-Scholes options pricer in Python.
Specification: European call and put pricing, all five Greeks (Delta, Gamma, Theta, Vega, Rho), implied volatility solver (Newton-Raphson), portfolio Greeks aggregation across multiple positions.

FORMAT: Claude Code implements the pricer. Analyst verifies: Black-Scholes assumptions match market conventions, IV solver convergence, Greeks calculation against textbook solutions.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — The Fama-French Multi-Factor Model

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Factor model specialist — specifying and validating Fama-French implementation.

ACTION:
Ask Claude Code to implement the Carhart four-factor model in Python (Fama-French three factors plus momentum). Specification: regress portfolio returns on Mkt-RF, SMB, HML and MOM.

FORMAT: Claude Code runs the regression. Analyst verifies: data period and source, factor definitions match Fama-French documentation, alpha is statistically meaningful.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — The Institutional Investment Strategy Backtesting Engine

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Quantitative strategist — specifying and reviewing backtesting engine.

ACTION:
Ask Claude Code to build an investment strategy backtesting engine in Python. Specification: signal generation from [DESCRIBE], position sizing (equal weight or [RULE]), transaction costs ([X]bps per trade), performance metrics (annualised return, Sharpe, Sortino, max drawdown, turnover, hit rate).

FORMAT: Claude Code builds the engine. Analyst verifies: no look-ahead bias in signal calculation, transaction costs realistic, walk-forward split discipline enforced.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 6 — The Python Portfolio Risk Attribution & Decomposition

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Risk attribution engineer — specifying and validating portfolio risk decomposition.

ACTION:
Ask Claude Code to build a portfolio risk attribution tool in Python. Specification: Marginal Contribution to Risk (MCTR) per position, systematic vs idiosyncratic decomposition using a factor model, concentration flags (top 5 positions % of total risk), tracking error vs benchmark.

FORMAT: 

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 7 — The Institutional Performance Analytics & Attribution

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Performance analytics engineer — specifying GIPS-compatible performance suite.

ACTION:
Ask Claude Code to build a GIPS-compatible performance analytics suite in Python. Specification: time-weighted return (TWR) calculation, money-weighted return (MWR/IRR), Brinson-Hood-Beebower (BHB) attribution (allocation + selection + interaction effects), formatted report output.

FORMAT: Claude Code builds the analytics suite. Analyst verifies: TWR methodology matches GIPS requirements, BHB attribution sums correctly to active return, data inputs are clean.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Financial Data Extraction & Processing Pipeline

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Data engineering lead — specifying financial data ingestion pipeline.

ACTION:
Ask Claude Code to build a financial data ingestion and processing pipeline in Python. Specification: ingest [DATA SOURCE FORMAT: CSV/Excel/JSON/API], validate schema, handle missing data, calculate derived metrics ([LIST]), export to structured Excel.

FORMAT: Claude Code builds the pipeline. Analyst verifies: data validation catches real errors, derived metrics match manual calculations on sample rows, Excel output is formatted correctly.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```


## Chapter 16 — Claude Cowork, Plugins & MCP

### PROMPT 1 — The Cowork Earnings Flash Note

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Research operations, configuring the Cowork earnings flash pipeline.

ACTION:
Configure a Cowork earnings flash note pipeline. Trigger: new PDF in /Earnings_Releases/ folder.

FORMAT: Earnings flash pipeline configuration with timing log and PM approval gate.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 2 — The Real-Time News Classification & Alert System

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Research operations, configuring the news classification and monitoring pipeline.

ACTION:
Configure a Cowork news classification pipeline. Trigger: scheduled run every [N] hours.

FORMAT: News classification pipeline with materiality filter and PM alert protocol.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 3 — The Automated Portfolio Risk Limit Breach Detection

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Risk operations, configuring automated portfolio risk limit monitoring.

ACTION:
Configure a Cowork daily risk limit monitoring pipeline. Trigger: daily at market open. Validation lives in the project CLAUDE.md standing rule: every dashboard figure recomputed by a Python script from position data, PASS/FAIL per check, before any alert is sent.

FORMAT: Risk limit monitoring pipeline with breach detection and CIO alert template.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 4 — Claude's Five Finance Plugins: Selection and Configuration

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Finance analyst, selecting and configuring the right Claude finance plugin.

ACTION:
Select the appropriate Claude finance plugin for [YOUR TASK]. Five options: Financial Analysis (DuPont, Altman Z, ratios), Investment Banking (LBO, accretion/dilution), Equity Research (research note format, sector KPIs), Private Equity (IC memo, IRR/MOIC), Wealth Management (IPS, RRTTLLU, client letters).

FORMAT: Plugin selection rationale and verification that domain conventions are applied.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 5 — HNI Client Advisory Using Claude Wealth Management

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Senior wealth advisor, reviewing the plugin-generated HNI package before it goes to the client and compliance.

ACTION:
Use the Claude Wealth Management Plugin for a complete HNI client advisory package. Client: [AGE], [RISK PROFILE], [AUM], [TIME HORIZON], [TAX JURISDICTION].

FORMAT: Complete HNI advisory package: RRTTLLU assessment, IPS draft, and compliant client letter.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 7 — The Investment Committee Presentation Preparation Pipeline

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Research team lead, automating IC deck preparation via Cowork.

ACTION:
Automate IC deck preparation using a Cowork weekly workflow. Step 1 (Haiku): pull current portfolio weights, compare to last IC, then calculate all position changes.

FORMAT: IC deck automation pipeline with position change analysis and PM review gate.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```

### PROMPT 8 — The Automated Client Communication & Quarterly Letter System

```
CONTEXT: [your firm, your universe, your data sources, the date, and any
house assumptions. The book supplies the finance context; you supply the desk.]

ROLE: Client relations manager, automating the quarterly client communication pipeline.

ACTION:
Build an automated quarterly client communication pipeline. Step 1 (Haiku): pull quarterly performance data, calculate TWR, benchmark, active return, top 3 contributors and detractors. The project CLAUDE.md standing rule applies: every performance figure recomputed by a Python script from holdings data, PASS/FAIL per check, before the draft reaches compliance.

FORMAT: Quarterly client letter pipeline with performance calculation and compliance check.

TONE: Institutional. Every forward-looking figure labelled
an estimate. No recommendation language.
```
