"""
m08_nav_engine.py  --  Chapter 8 lab: a small daily NAV engine with an exception list.

Usage:
    python3 m08_nav_engine.py            # price the fund, flag exceptions, print commentary template
    python3 m08_nav_engine.py --inject   # same, but blank one price and backdate one date to show the flags fire

The portfolio is a constructed example: five US holdings, a cash balance, an accrued expense
and a share count. Prices come from Yahoo Finance through yfinance. Nothing here is a real fund.
"""
import argparse, csv, os, sys, datetime as dt
import yfinance as yf

HERE = os.path.dirname(os.path.abspath(__file__))
HOLDINGS = os.path.join(HERE, "m08_holdings.csv")

# The constructed fund. Shares are round numbers chosen for the exercise.
FUND_ROWS = [
    ("SPY",  "SPDR S&P 500 ETF",       1200),
    ("QQQ",  "Invesco QQQ Trust",        900),
    ("AAPL", "Apple Inc.",              1500),
    ("MSFT", "Microsoft Corp.",          800),
    ("XOM",  "Exxon Mobil Corp.",       2500),
]
CASH = 250_000.00            # settled cash at the custodian
ACCRUED_EXPENSES = 4_200.00  # management fee and audit accrual
SHARES_OUTSTANDING = 100_000
MOVE_LIMIT = 0.05            # flag any holding that moved more than 5% on the day


def write_holdings_if_missing():
    if os.path.exists(HOLDINGS):
        return
    with open(HOLDINGS, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ticker", "name", "shares"])
        w.writerows(FUND_ROWS)


def read_holdings():
    with open(HOLDINGS) as f:
        return [(r["ticker"], r["name"], float(r["shares"])) for r in csv.DictReader(f)]


def fetch_prices(tickers):
    """Return {ticker: (last_close, prior_close, last_date)}; None fields where data is missing."""
    out = {}
    for t in tickers:
        try:
            h = yf.Ticker(t).history(period="10d", auto_adjust=False)
            closes = h["Close"].dropna()
            if len(closes) >= 2:
                out[t] = (float(closes.iloc[-1]), float(closes.iloc[-2]), closes.index[-1].date())
            elif len(closes) == 1:
                out[t] = (float(closes.iloc[-1]), None, closes.index[-1].date())
            else:
                out[t] = (None, None, None)
        except Exception:
            out[t] = (None, None, None)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inject", action="store_true", help="blank one price and backdate one date")
    args = ap.parse_args()

    write_holdings_if_missing()
    holdings = read_holdings()
    prices = fetch_prices([t for t, _, _ in holdings])

    if args.inject:
        # Two deliberate faults so the exception list has something to catch.
        last, prior, d = prices["XOM"]
        prices["XOM"] = (None, prior, d)                      # missing price
        last, prior, d = prices["MSFT"]
        prices["MSFT"] = (last, prior, d - dt.timedelta(days=3))  # stale date

    dates = [p[2] for p in prices.values() if p[2]]
    as_of = max(dates) if dates else None

    exceptions = []
    market_value = 0.0
    rows = []
    for t, name, sh in holdings:
        last, prior, d = prices[t]
        if last is None:
            exceptions.append(f"{t}: MISSING PRICE. Cannot value {sh:,.0f} shares. Hold the NAV.")
            rows.append((t, sh, None, None, None, d))
            continue
        if d != as_of:
            exceptions.append(f"{t}: STALE DATE. Price dated {d}, fund priced as of {as_of}.")
        move = (last / prior - 1) if prior else None
        if move is None:
            exceptions.append(f"{t}: NO PRIOR CLOSE. Day move cannot be checked.")
        elif abs(move) > MOVE_LIMIT:
            exceptions.append(f"{t}: LARGE MOVE. {move:+.2%} on the day, limit is {MOVE_LIMIT:.0%}.")
        mv = last * sh
        market_value += mv
        rows.append((t, sh, last, move, mv, d))

    total_assets = market_value + CASH
    net_assets = total_assets - ACCRUED_EXPENSES
    nav = net_assets / SHARES_OUTSTANDING

    print(f"DAILY NAV PACK  (constructed example)   priced as of {as_of}")
    print("-" * 78)
    print(f"{'Ticker':<7}{'Shares':>9}{'Close':>12}{'Day move':>11}{'Market value':>17}{'Price date':>13}")
    for t, sh, last, move, mv, d in rows:
        c = f"{last:,.2f}" if last is not None else "n/a"
        m = f"{move:+.2%}" if move is not None else "n/a"
        v = f"{mv:,.2f}" if mv is not None else "n/a"
        print(f"{t:<7}{sh:>9,.0f}{c:>12}{m:>11}{v:>17}{str(d):>13}")
    print("-" * 78)
    print(f"{'Securities at market':<40}{market_value:>20,.2f}")
    print(f"{'Cash':<40}{CASH:>20,.2f}")
    print(f"{'Total assets':<40}{total_assets:>20,.2f}")
    print(f"{'Less accrued expenses':<40}{ACCRUED_EXPENSES:>20,.2f}")
    print(f"{'Net assets':<40}{net_assets:>20,.2f}")
    print(f"{'Shares outstanding':<40}{SHARES_OUTSTANDING:>20,}")
    print(f"{'NAV per share':<40}{nav:>20,.4f}")
    print()
    print(f"EXCEPTIONS ({len(exceptions)})")
    if not exceptions:
        print("  none. NAV may be released after the four-eyes check.")
    for e in exceptions:
        print(f"  * {e}")
    if any("MISSING" in e for e in exceptions):
        print("  NAV STATUS: HELD. A missing price means the number above is incomplete.")
    else:
        print("  NAV STATUS: READY FOR REVIEW.")
    print()
    print("COMMENTARY TEMPLATE (fill only from the table above; every number must appear there)")
    print("  As of {as_of}, the fund's NAV per share was {nav}.")
    print("  The largest contributor to the day's move was {ticker}, which {rose/fell} {move}.")
    print("  {n} exception(s) were raised: {list them or write 'none'}.")
    print("  The NAV is {released / held} pending {reason}.")


if __name__ == "__main__":
    main()
