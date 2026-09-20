"""Module 1 lab: pull Apple's income statement from its FY2025 10-K on SEC EDGAR.

The numbers come from the SEC's XBRL "company facts" API. It is free and needs
no API key. The SEC only asks that you identify yourself in the User-Agent
header, so put your own name and email on the line below.

Run it:
    python3 m01_edgar_pnl.py            # Apple
    python3 m01_edgar_pnl.py 789019     # Microsoft (its CIK)
"""

import json
import sys
import urllib.request

# The SEC asks every script to say who is calling. Use your own name and email.
USER_AGENT = "Tejas Jadhav tejasipsjadhav@gmail.com"

# Every SEC registrant has a Central Index Key. Apple is 320193, Microsoft is 789019.
CIK = int(sys.argv[1]) if len(sys.argv) > 1 else 320193

# The income statement lines we want, in the order a P&L prints them.
# Left: the XBRL tag Apple uses. Right: the label we print.
LINES = [
    ("RevenueFromContractWithCustomerExcludingAssessedTax", "Net sales"),
    ("CostOfGoodsAndServicesSold", "Cost of sales"),
    ("GrossProfit", "Gross margin"),
    ("ResearchAndDevelopmentExpense", "Research and development"),
    ("SellingGeneralAndAdministrativeExpense", "Selling, general and administrative"),
    ("OperatingExpenses", "Total operating expenses"),
    ("OperatingIncomeLoss", "Operating income"),
    ("IncomeTaxExpenseBenefit", "Provision for income taxes"),
    ("NetIncomeLoss", "Net income"),
]

# 1. Download every fact the company has ever tagged. One JSON file, about 4 MB.
url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK:010d}.json"
req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
with urllib.request.urlopen(req, timeout=60) as resp:
    facts = json.load(resp)

name = facts["entityName"]
gaap = facts["facts"]["us-gaap"]


def annual_values(tag):
    """Return {period_end: value} for full-year figures reported in a 10-K.

    The API's "fy" field is the year of the FILING, not of the period, so a 10-K
    that shows three years of history tags all three with the same fy. We key by
    the period end date instead, which is unambiguous.
    """
    out = {}
    if tag not in gaap:
        return out
    for row in gaap[tag]["units"].get("USD", []):
        # form == "10-K": it came from an annual report. fp == "FY": it is a full-year figure.
        # A frame like "CY2025" with no "Q" in it marks a clean twelve-month duration.
        frame = row.get("frame", "")
        if row.get("form") == "10-K" and row.get("fp") == "FY" and frame.startswith("CY") and "Q" not in frame:
            out[row["end"]] = row["val"]
    return out


# 2. Pick the three most recent fiscal year ends that carry a revenue figure.
revenue = annual_values(LINES[0][0])
periods = sorted(revenue)[-3:]

# 3. Print the statement. Values are in whole dollars in the file; we show millions.
print(f"{name}  (CIK {CIK})")
print("Source: SEC EDGAR XBRL company facts, Form 10-K, full fiscal year")
print("Figures in USD millions")
print()
print(f"{'Fiscal year ended':<38}" + "".join(f"{p:>14}" for p in periods))
table = {}
for tag, label in LINES:
    vals = annual_values(tag)
    table[tag] = vals
    row = "".join(f"{vals[p] / 1e6:>14,.0f}" if p in vals else f"{'not tagged':>14}" for p in periods)
    print(f"{label:<38}{row}")

# 4. Recompute two subtotals in Python. If a check fails, do not use the table.
print()
for p in periods:
    try:
        sales = table["RevenueFromContractWithCustomerExcludingAssessedTax"][p]
        cogs = table["CostOfGoodsAndServicesSold"][p]
        gm = table["GrossProfit"][p]
        ok1 = "PASS" if sales - cogs == gm else "FAIL"
    except KeyError:
        ok1 = "SKIPPED (a line is not tagged)"
    try:
        opex = table["OperatingExpenses"][p]
        opinc = table["OperatingIncomeLoss"][p]
        ok2 = "PASS" if gm - opex == opinc else "FAIL"
    except KeyError:
        ok2 = "SKIPPED (a line is not tagged)"
    print(f"{p}  sales - cost of sales = gross margin: {ok1}")
    print(f"{p}  gross margin - operating expenses = operating income: {ok2}")

print()
print("Now open the 10-K on sec.gov and match one line against the printed statement.")
