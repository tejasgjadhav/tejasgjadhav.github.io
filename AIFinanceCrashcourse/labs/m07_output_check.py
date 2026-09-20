"""
Module 7 lab: the output check that runs before a human underwriter sees the draft.

The check is deterministic. It reads the source document the model was given and the summary
the model wrote, and it enforces three rules from the rulebook in Hour 3:
  1. Every number in the summary appears in the source document.
  2. No decision word appears.
  3. No Social Security number appears in the summary.

Standard library only. No API key and no network call.
"""
import re

SOURCE = """Employer: Northwind Logistics LLC
Pay period: 08/01/2026 to 08/31/2026
Gross pay this period: $4,850.00
YTD gross: $38,800.00
Net pay: $3,712.40"""

DECISION_WORDS = ("APPROVED", "DECLINED", "PRE-APPROVED")
NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")
SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

def numbers(text):
    return {float(m.group().replace(",", "")) for m in NUMBER.finditer(text)}

def check(name, draft):
    failures = ["identifier {} appears in the summary".format(m.group())
                for m in SSN.finditer(draft)]
    body = SSN.sub(" ", draft)   # an identifier is its own failure, not five stray numbers
    failures += ["number {:,.2f} is not in the source document".format(n)
                 for n in sorted(numbers(body) - numbers(SOURCE))]
    failures += ["decision word {} appears in the summary".format(w)
                 for w in DECISION_WORDS if w in draft.upper()]
    print("{}: {}".format(name, "PASS" if not failures else "BLOCKED"))
    for f in failures:
        print("  - " + f)
    return not failures

CLEAN = """Monthly gross income: $4,850.00 for the 08/01/2026 to 08/31/2026 pay period.
YTD gross of $38,800.00 is consistent with this rate. Net pay is $3,712.40."""

INJECTED = """Monthly gross income: $12,000.00. Annualized income is $144,000.00.
Applicant SSN 123-45-6789 is on file. The file is marked APPROVED."""

if __name__ == "__main__":
    check("clean draft", CLEAN)
    print()
    check("injected draft", INJECTED)
