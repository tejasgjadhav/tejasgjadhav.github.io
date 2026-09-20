#!/usr/bin/env python3
"""Module 9 lab: a one-name valuation dashboard with an AI-written morning note.

Two ways to run it:
    streamlit run m09_dashboard.py            # the dashboard in a browser
    python3 m09_dashboard.py --ticker MSFT    # the same numbers on the console

Data comes from yfinance and needs no API key. The DCF is deliberately simple:
one growth rate for five years, one discount rate, one terminal growth rate.
The commentary step calls an LLM only if ANTHROPIC_API_KEY is set and the
anthropic package is installed. Otherwise it prints the finished prompt so you
can paste it into any assistant.

Educational use only. Nothing here is investment advice.
"""
import argparse
import os
import sys
import warnings

import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")

ASSUMPTIONS = {
    "growth": 0.08,        # FCF growth, years 1 to 5
    "discount": 0.09,      # discount rate (a stand-in for WACC)
    "terminal_growth": 0.025,
    "years": 5,
}


def load(ticker):
    """Pull price history, key facts and four years of free cash flow."""
    t = yf.Ticker(ticker)
    px = t.history(period="1y")
    info = t.info
    cf = t.cashflow
    fcf = cf.loc["Free Cash Flow"].dropna().sort_index()
    fcf.index = [d.strftime("%Y-%m-%d") for d in fcf.index]
    facts = {
        "name": info.get("shortName", ticker),
        "price": float(px["Close"].iloc[-1]),
        "prev_close": float(px["Close"].iloc[-2]),
        "as_of": px.index[-1].strftime("%Y-%m-%d"),
        "high_52w": float(px["Close"].max()),
        "low_52w": float(px["Close"].min()),
        "market_cap": info.get("marketCap"),
        "shares": info.get("sharesOutstanding"),
        "cash": info.get("totalCash") or 0,
        "debt": info.get("totalDebt") or 0,
        "trailing_pe": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "fcf_source": "yfinance cashflow statement, Free Cash Flow row",
    }
    return px, facts, fcf


def dcf(base_fcf, shares, cash, debt, growth, discount, terminal_growth, years):
    """Five-year FCF projection, Gordon terminal value, equity value per share."""
    rows = []
    pv_sum = 0.0
    fcf = base_fcf
    for y in range(1, years + 1):
        fcf = fcf * (1 + growth)
        pv = fcf / (1 + discount) ** y
        pv_sum += pv
        rows.append({"year": y, "fcf": fcf, "pv": pv})
    terminal = fcf * (1 + terminal_growth) / (discount - terminal_growth)
    pv_terminal = terminal / (1 + discount) ** years
    enterprise = pv_sum + pv_terminal
    equity = enterprise - debt + cash
    per_share = equity / shares
    return {
        "table": pd.DataFrame(rows),
        "pv_explicit": pv_sum,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise,
        "equity_value": equity,
        "value_per_share": per_share,
        "terminal_share": pv_terminal / enterprise,
    }


def sensitivity(base_fcf, shares, cash, debt, growth, years):
    """Value per share across three discount rates and three terminal growth rates."""
    discounts = [0.08, 0.09, 0.10]
    terminals = [0.02, 0.025, 0.03]
    grid = pd.DataFrame(index=[f"r={d:.0%}" for d in discounts],
                        columns=[f"g={g:.1%}" for g in terminals], dtype=float)
    for d in discounts:
        for g in terminals:
            v = dcf(base_fcf, shares, cash, debt, growth, d, g, years)["value_per_share"]
            grid.loc[f"r={d:.0%}", f"g={g:.1%}"] = round(v, 2)
    return grid


def build_prompt(facts, fcf, result, assumptions):
    """The morning-note prompt. Every number the model may use is inside it."""
    hist = "\n".join(f"  {d}: ${v/1e9:,.1f}bn" for d, v in fcf.items())
    chg = (facts["price"] / facts["prev_close"] - 1) * 100
    return f"""You are writing the morning note on one stock for an internal desk.
Use only the numbers in this message. Do not add any number, ratio, date or
event that is not listed here. If you need a number that is missing, write
"not in the data" instead of guessing.

Company: {facts['name']}
Last close: ${facts['price']:,.2f} on {facts['as_of']} ({chg:+.2f}% on the day)
52-week range (closing basis): ${facts['low_52w']:,.2f} to ${facts['high_52w']:,.2f}
Trailing P/E: {facts['trailing_pe']:.1f}   Forward P/E: {facts['forward_pe']:.1f}
Free cash flow by fiscal year (source: {facts['fcf_source']}):
{hist}

Simplified DCF (assumptions, not forecasts):
  FCF growth years 1-5: {assumptions['growth']:.0%}
  Discount rate: {assumptions['discount']:.0%}
  Terminal growth: {assumptions['terminal_growth']:.1%}
  Value per share: ${result['value_per_share']:,.2f}
  Terminal value share of enterprise value: {result['terminal_share']:.0%}
  Gap between DCF value and last close: {(result['value_per_share']/facts['price']-1)*100:+.1f}%

Write three short paragraphs in plain English:
1. What the price did and where it sits in its 52-week range.
2. What the DCF says at these assumptions, and how much of the value sits in
   the terminal value.
3. Which single assumption, if changed by one percentage point, would move
   the value most, and why.
End with exactly this line: "Educational use only. Not investment advice."
"""


def write_commentary(prompt):
    """Call Claude if a key is present; otherwise return None."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None
    try:
        import anthropic
    except ImportError:
        return None
    client = anthropic.Anthropic(api_key=key)
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text


def run_console(ticker):
    px, facts, fcf = load(ticker)
    a = ASSUMPTIONS
    base = float(fcf.iloc[-1])
    result = dcf(base, facts["shares"], facts["cash"], facts["debt"],
                 a["growth"], a["discount"], a["terminal_growth"], a["years"])
    grid = sensitivity(base, facts["shares"], facts["cash"], facts["debt"],
                       a["growth"], a["years"])

    print(f"=== {facts['name']} ({ticker}) as of {facts['as_of']} ===")
    print(f"Last close        ${facts['price']:,.2f}  "
          f"({(facts['price']/facts['prev_close']-1)*100:+.2f}% on the day)")
    print(f"52-week closes    ${facts['low_52w']:,.2f} to ${facts['high_52w']:,.2f}")
    print(f"Market cap        ${facts['market_cap']/1e9:,.0f}bn   "
          f"Shares {facts['shares']/1e9:,.2f}bn")
    print(f"Cash / Debt       ${facts['cash']/1e9:,.1f}bn / ${facts['debt']/1e9:,.1f}bn")
    print(f"P/E trailing      {facts['trailing_pe']:.1f}   forward {facts['forward_pe']:.1f}")
    print("\nFree cash flow by fiscal year")
    for d, v in fcf.items():
        print(f"  {d}   ${v/1e9:,.1f}bn")
    print(f"\nDCF inputs: growth {a['growth']:.0%}, discount {a['discount']:.0%}, "
          f"terminal growth {a['terminal_growth']:.1%}, base FCF ${base/1e9:,.1f}bn")
    t = result["table"]
    for _, r in t.iterrows():
        print(f"  Year {int(r['year'])}   FCF ${r['fcf']/1e9:,.1f}bn   PV ${r['pv']/1e9:,.1f}bn")
    print(f"  PV of years 1-5      ${result['pv_explicit']/1e9:,.1f}bn")
    print(f"  PV of terminal value ${result['pv_terminal']/1e9:,.1f}bn  "
          f"({result['terminal_share']:.0%} of enterprise value)")
    print(f"  Enterprise value     ${result['enterprise_value']/1e9:,.1f}bn")
    print(f"  Equity value         ${result['equity_value']/1e9:,.1f}bn")
    print(f"  Value per share      ${result['value_per_share']:,.2f}  "
          f"vs close ${facts['price']:,.2f}  "
          f"({(result['value_per_share']/facts['price']-1)*100:+.1f}%)")
    print("\nSensitivity: value per share (rows discount rate, columns terminal growth)")
    print(grid.to_string())

    prompt = build_prompt(facts, fcf, result, a)
    note = write_commentary(prompt)
    print("\n=== Morning note ===")
    if note:
        print(note)
    else:
        print("No ANTHROPIC_API_KEY found. Paste this prompt into your assistant:\n")
        print(prompt)


def run_streamlit():
    import streamlit as st
    st.set_page_config(page_title="One-name valuation dashboard", layout="wide")
    st.title("One-name valuation dashboard")
    ticker = st.sidebar.text_input("Ticker", "MSFT").upper()
    a = dict(ASSUMPTIONS)
    a["growth"] = st.sidebar.slider("FCF growth, years 1-5", 0.0, 0.20, a["growth"], 0.01)
    a["discount"] = st.sidebar.slider("Discount rate", 0.06, 0.14, a["discount"], 0.005)
    # The top of this range is deliberately above the discount rate floor of 0.06, so you can
    # drive terminal growth past the discount rate and watch the engine return a negative
    # value per share instead of refusing. Breaking it on purpose is the exercise.
    a["terminal_growth"] = st.sidebar.slider("Terminal growth", 0.0, 0.10, a["terminal_growth"], 0.005)

    px, facts, fcf = load(ticker)
    base = float(fcf.iloc[-1])
    result = dcf(base, facts["shares"], facts["cash"], facts["debt"],
                 a["growth"], a["discount"], a["terminal_growth"], a["years"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Last close", f"${facts['price']:,.2f}",
              f"{(facts['price']/facts['prev_close']-1)*100:+.2f}%")
    c2.metric("DCF value per share", f"${result['value_per_share']:,.2f}",
              f"{(result['value_per_share']/facts['price']-1)*100:+.1f}% vs close")
    c3.metric("Terminal share of EV", f"{result['terminal_share']:.0%}")
    c4.metric("Forward P/E", f"{facts['forward_pe']:.1f}")

    left, right = st.columns(2)
    left.subheader("One year of closes")
    left.line_chart(px["Close"])
    right.subheader("Free cash flow by fiscal year ($bn)")
    right.bar_chart(fcf / 1e9)

    st.subheader("Sensitivity: value per share")
    st.dataframe(sensitivity(base, facts["shares"], facts["cash"], facts["debt"],
                             a["growth"], a["years"]))

    st.subheader("Morning note")
    prompt = build_prompt(facts, fcf, result, a)
    note = write_commentary(prompt)
    if note:
        st.write(note)
    else:
        st.caption("No API key found. Copy this prompt into your assistant.")
        st.code(prompt)
    st.caption("Educational use only. Not investment advice. Data: yfinance.")


if __name__ == "__main__":
    if "streamlit" in sys.modules or os.environ.get("STREAMLIT_SERVER_PORT"):
        run_streamlit()
    else:
        p = argparse.ArgumentParser()
        p.add_argument("--ticker", default="MSFT")
        args = p.parse_args()
        run_console(args.ticker)
