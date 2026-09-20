#!/usr/bin/env python3
"""Module 3 lab: three agents write a one-page investment memo on one S&P 500 company.

Research Agent  -> pulls the facts from SEC EDGAR companyfacts (XBRL) and yfinance. No key.
Analysis Agent  -> computes revenue growth, net margin and debt to equity in plain Python.
Writing Agent   -> drafts the memo. Calls the `claude` CLI if it is on the PATH; otherwise
                   it prints the prompt so you can paste it into any free AI chat.
Reviewer        -> you. The script also runs one mechanical check: every number in the memo
                   must appear in the fact sheet or the analysis.

Usage:  python3 m03_three_agent_memo.py AAPL
        python3 m03_three_agent_memo.py MSFT --no-llm
"""
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from datetime import date, datetime

UA = {"User-Agent": "ai-finance-master-guide lab (reader@example.com)"}

# XBRL tags, tried in order. The first tag that carries two fiscal years wins.
TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
                "SalesRevenueNet"],
    "net_income": ["NetIncomeLoss"],
    "total_debt": ["LongTermDebt", "DebtInstrumentCarryingAmount", "LongTermDebtNoncurrent"],
    "equity": ["StockholdersEquity"],
}
DURATION = {"revenue", "net_income"}  # flow items; balance items are instants


def get_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.load(r)


def cik_for(ticker):
    table = get_json("https://www.sec.gov/files/company_tickers.json")
    for row in table.values():
        if row["ticker"].upper() == ticker.upper():
            return f"{row['cik_str']:010d}", row["title"]
    sys.exit(f"{ticker} is not in the SEC ticker table")


def last_two_fiscal_years(facts, tag, duration):
    """Return [(end_date, value), (end_date, value)] for the two latest fiscal years."""
    rows = facts.get(tag, {}).get("units", {}).get("USD", [])
    by_end = {}
    for r in rows:
        if r.get("form") != "10-K" or r.get("fp") != "FY":
            continue
        if duration:
            days = (datetime.fromisoformat(r["end"]) - datetime.fromisoformat(r["start"])).days
            if not 350 <= days <= 380:
                continue  # skip quarterly and cumulative rows
        # keep the most recently filed value for each period end
        if r["end"] not in by_end or r["filed"] > by_end[r["end"]][0]:
            by_end[r["end"]] = (r["filed"], r["val"])
    ends = sorted(by_end)[-2:]
    return [(e, by_end[e][1]) for e in ends] if len(ends) == 2 else None


def research_agent(ticker):
    cik, name = cik_for(ticker)
    facts = get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json")["facts"]["us-gaap"]
    out = {"company": name, "ticker": ticker.upper(), "cik": cik, "tags_used": {}}
    for item, tags in TAGS.items():
        for tag in tags:
            got = last_two_fiscal_years(facts, tag, item in DURATION)
            if got:
                out[item] = got
                out["tags_used"][item] = tag
                break
        else:
            sys.exit(f"no two-year series for {item}; tags tried: {tags}")
    try:
        import yfinance as yf
        info = yf.Ticker(ticker).fast_info
        out["price"] = round(float(info["last_price"]), 2)
        out["market_cap"] = float(info["market_cap"])
    except Exception as e:  # the memo still works without a live price
        out["price"], out["market_cap"] = None, None
        out["price_note"] = f"yfinance unavailable: {e}"
    return out


def bn(x):
    return f"${x / 1e9:,.1f} billion"


def fact_sheet(f):
    (e0, rev0), (e1, rev1) = f["revenue"]
    (_, ni0), (_, ni1) = f["net_income"]
    (_, debt), (_, eq) = f["total_debt"][1], f["equity"][1]
    lines = [
        f"Company: {f['company']} ({f['ticker']}), SEC CIK {f['cik']}",
        f"Fiscal year ended {e1}: revenue {bn(rev1)}",
        f"Fiscal year ended {e0}: revenue {bn(rev0)}",
        f"Net income, fiscal year ended {e1}: {bn(ni1)}",
        f"Net income, fiscal year ended {e0}: {bn(ni0)}",
        f"Total debt at {f['total_debt'][1][0]}: {bn(debt)}",
        f"Shareholders' equity at {f['equity'][1][0]}: {bn(eq)}",
    ]
    if f["price"]:
        lines.append(f"Share price on {date.today()}: ${f['price']:,.2f} (market cap {bn(f['market_cap'])})")
    lines.append("Source: SEC EDGAR companyfacts API, 10-K filings, XBRL tags "
                 + ", ".join(f"{k}={v}" for k, v in f["tags_used"].items())
                 + ("; price from Yahoo Finance via yfinance" if f["price"] else ""))
    return "\n".join(lines)


def analysis_agent(f):
    (_, rev0), (_, rev1) = f["revenue"]
    ni1 = f["net_income"][1][1]
    debt, eq = f["total_debt"][1][1], f["equity"][1][1]
    growth = (rev1 / rev0 - 1) * 100
    margin = ni1 / rev1 * 100
    de = debt / eq
    return "\n".join([
        f"Revenue growth: {bn(rev1)} / {bn(rev0)} - 1 = {growth:.1f}%",
        f"Net margin: {bn(ni1)} / {bn(rev1)} = {margin:.1f}%",
        f"Debt to equity: {bn(debt)} / {bn(eq)} = {de:.2f}x",
        f"Reading: revenue {'grew' if growth >= 0 else 'fell'} {abs(growth):.1f}% year on year. "
        f"The company kept {margin:.1f} cents of every revenue dollar as profit. "
        f"It carries {de:.2f} dollars of debt for every dollar of equity.",
    ])


CLOSING = "This memo is a classroom exercise. It is not investment advice."

WRITER_PROMPT = """You are the Writing Agent in a three-agent research crew. Below are a fact sheet
from the Research Agent and an analysis from the Analysis Agent. Write a one-page investment memo
with four sections: The numbers, The reading, The view, Sources. Keep every sentence short. Every
number must appear in the material below; do not introduce a new one. In The view, give a clear
two-sentence position a reader could disagree with. End the memo with this line exactly:
"{closing}"

FACT SHEET
{facts}

ANALYSIS
{analysis}
"""


def writing_agent(prompt, use_llm):
    if use_llm and shutil.which("claude"):
        try:
            r = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True, timeout=240)
            if r.returncode == 0 and CLOSING in r.stdout:
                # the memo ends at the required closing line; anything after it is chatter
                return r.stdout.split(CLOSING)[0].strip() + "\n" + CLOSING, "claude CLI"
        except Exception:
            pass
    return None, "prompt only"


def reviewer(memo, facts, analysis):
    """Every number in the memo must exist in the source material."""
    nums = lambda s: set(re.findall(r"\d[\d,]*(?:\.\d+)?", s))
    allowed = nums(facts) | nums(analysis)
    missing = sorted(n for n in nums(memo) if n not in allowed and not re.fullmatch(r"\d{1,2}", n))
    return missing


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ticker = args[0] if args else "AAPL"
    use_llm = "--no-llm" not in sys.argv
    f = research_agent(ticker)
    facts = fact_sheet(f)
    print("=== RESEARCH AGENT: fact sheet ===\n" + facts)
    analysis = analysis_agent(f)
    print("\n=== ANALYSIS AGENT ===\n" + analysis)
    prompt = WRITER_PROMPT.format(facts=facts, analysis=analysis, closing=CLOSING)
    memo, how = writing_agent(prompt, use_llm)
    if memo is None:
        print("\n=== WRITING AGENT: paste this prompt into any AI chat ===\n" + prompt)
    else:
        print(f"\n=== WRITING AGENT ({how}) ===\n" + memo)
        missing = reviewer(memo, facts, analysis)
        print("\n=== REVIEWER (mechanical check) ===")
        print("PASS: every number in the memo traces to the fact sheet or the analysis."
              if not missing else f"FAIL: numbers with no source: {missing}")
