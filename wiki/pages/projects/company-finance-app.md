---
title: company-finance-app — Flask company lookup
type: project
tags: [python, flask, market-data, yfinance]
created: 2026-08-09
updated: 2026-08-09
sources: [~/files/company-finance-app]
---

A deliberately small Flask app built on 2026-08-09, living at `~/files/company-finance-app`
(`server.py` at about 5 KB, plus `static/` and `templates/`). You type a company name or a
ticker, it resolves the symbol with **yfinance**, and it shows four things: the latest market
price, the latest available revenue, the market cap, and the ticker and exchange it resolved
to. That is the whole product.

Run it with `python3 server.py` and open `http://127.0.0.1:5055`.

Two caveats come from the data source rather than the code. Values depend on Yahoo Finance
being available and on where the market is in its session. And for Indian equities the name
search often misses, so pass NSE-style tickers such as `RELIANCE.NS` when it does not resolve
the company you meant.

It sits inside [[files-repo]] but is untracked as of 2026-08-09. If it ever gets its own repo
it has to be gitignored in the root one — see the gitlink breakage recorded on [[files-repo]].
Unlike [[in-eq]], which is a multi-agent research pipeline, this is a single lookup screen and
is meant to stay that way.
