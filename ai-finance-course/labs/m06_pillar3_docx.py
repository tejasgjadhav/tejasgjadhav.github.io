"""
Module 6 lab, last step: assemble the checked figures into a Word document with python-docx.
Every row carries its provenance tag. The narrative paragraph is pasted in from the chat step
after a human has checked each figure in it against the table.
"""
from docx import Document

rows = [
    ("CET1 capital", "$302,619 million", "deterministic"),
    ("Tier 1 capital", "$322,720 million", "deterministic"),
    ("Total capital", "$362,723 million", "deterministic"),
    ("Risk-weighted assets (Standardized)", "$2,132,428 million", "deterministic"),
    ("Total leverage exposure", "$5,844,422 million", "deterministic"),
    ("CET1 capital ratio (computed)", "14.19%", "derived"),
    ("Tier 1 capital ratio (computed)", "15.13%", "derived"),
    ("Total capital ratio (computed)", "17.01%", "derived"),
    ("Supplementary leverage ratio (computed)", "5.52%", "derived"),
    ("CET1 headroom over 11.5% requirement", "2.7 points", "derived"),
]
doc = Document()
doc.add_heading("Regulatory Capital Summary, JPMorgan Chase & Co., June 30, 2026", level=1)
doc.add_paragraph("Source: Form 10-Q for the quarter ended June 30, 2026, EDGAR accession "
                  "0001628280-26-054343, Capital Risk Management section, Standardized approach. "
                  "Figures tagged deterministic were read from the filing. Figures tagged derived "
                  "were computed from them and reconciled to the reported ratios within 0.05 points.")
t = doc.add_table(rows=1, cols=3)
t.style = "Light Grid Accent 1"
for i, h in enumerate(["Metric", "Value", "Provenance"]):
    t.rows[0].cells[i].text = h
for r in rows:
    c = t.add_row().cells
    for i, v in enumerate(r):
        c[i].text = v
doc.add_heading("Narrative", level=2)
doc.add_paragraph("[Paste the checked narrative here. Tag: llm, human-checked.]")
doc.save("pillar3_summary_jpm_2q26.docx")
print("Wrote pillar3_summary_jpm_2q26.docx")
print(f"  1 heading, 1 source paragraph, 1 table with {len(rows)} rows, 1 narrative placeholder")
for r in rows:
    print(f"  {r[0]:42s} {r[1]:>20s}   [{r[2]}]")
