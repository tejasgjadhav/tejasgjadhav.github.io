"""
Module 6 lab: pull a US G-SIB's public capital figures and check them before any AI writes a word.

Two public sources, both free and both machine-readable:
  1. SEC XBRL APIs (data.sec.gov). Every 10-K and 10-Q fact, tagged, as JSON.
  2. The regulatory capital table inside the bank's own 10-Q on EDGAR.

The capital-table figures below were copied by hand from JPMorgan Chase's Form 10-Q for the
quarter ended June 30, 2026 (EDGAR accession 0001628280-26-054343, filed August 6, 2026),
"Capital Risk Management" section, Standardized approach column. Copying them is step one.
Checking that they agree with each other is step two, and that is the point of this script.
Provenance: every figure is tagged deterministic (read from the source) or derived (computed here).
"""
import json
import urllib.request

UA = {"User-Agent": "AI in Finance reader example@example.com"}   # the SEC asks for a contact
CIK = "0000019617"                                              # JPMorgan Chase & Co.

def sec(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA)))

# ---- Step 1: one XBRL fact, straight from the SEC ----
d = sec(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{CIK}/us-gaap/StockholdersEquity.json")
facts = [f for f in d["units"]["USD"] if f["form"] in ("10-Q", "10-K")]
facts = {f["end"]: f for f in sorted(facts, key=lambda f: f["filed"], reverse=True)}  # first filing wins
print(f"{d['entityName']}  |  {d['tag']}  |  source: SEC companyconcept API")
for end in sorted(facts)[-3:]:
    f = facts[end]
    print(f"  {end}  ${f['val']/1e9:,.1f} billion   {f['form']}  filed {f['filed']}   [deterministic]")
print()

# ---- Step 2: the capital table, copied from the 10-Q, in $ millions ----
q = {
    "CET1 capital": 302_619, "Tier 1 capital": 322_720, "Total capital": 362_723,
    "Risk-weighted assets": 2_132_428, "Total leverage exposure": 5_844_422,
}
reported = {"CET1 capital ratio": 14.2, "Tier 1 capital ratio": 15.1,
            "Total capital ratio": 17.0, "Supplementary leverage ratio": 5.5}
minimums = {"CET1 capital ratio": 11.5, "Tier 1 capital ratio": 13.0, "Total capital ratio": 15.0}
print("JPMorgan Chase, June 30, 2026, Standardized approach, $ millions  [deterministic]")
for k, v in q.items():
    print(f"  {k:26s} {v:>12,}")
print()

# ---- Step 3: recompute every ratio and compare with the reported one ----
print("Reconciliation  [derived]")
calc = {
    "CET1 capital ratio": q["CET1 capital"] / q["Risk-weighted assets"] * 100,
    "Tier 1 capital ratio": q["Tier 1 capital"] / q["Risk-weighted assets"] * 100,
    "Total capital ratio": q["Total capital"] / q["Risk-weighted assets"] * 100,
    "Supplementary leverage ratio": q["Tier 1 capital"] / q["Total leverage exposure"] * 100,
}
for k, c in calc.items():
    r = reported[k]
    ok = "PASS" if abs(c - r) <= 0.05 else "FAIL"
    line = f"  {k:30s} computed {c:6.2f}%   reported {r:5.1f}%   {ok}"
    if k in minimums:
        line += f"   headroom over {minimums[k]:.1f}% requirement: {r - minimums[k]:.1f} points"
    print(line)
print()
print("Nothing above was written by a language model. That is deliberate.")
