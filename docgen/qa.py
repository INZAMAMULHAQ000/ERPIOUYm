# -*- coding: utf-8 -*-
import argparse, re, sys
from docx import Document

ap = argparse.ArgumentParser()
ap.add_argument("docx", nargs="?",
                default=r"C:\xampp\htdocs\was\QASWA_ERP_Product_Feature_Compendium.docx")
P = ap.parse_args().docx
d = Document(P)

texts = [p.text for p in d.paragraphs]
for t in d.tables:
    for r in t.rows:
        for c in r.cells:
            texts.append(c.text)
blob = "\n".join(t for t in texts if t)

print("chars:", len(blob), "| paragraphs+cells:", len(texts), "| tables:", len(d.tables))
h1 = [p.text for p in d.paragraphs if p.style.name == "Heading 1"]
h2 = [p.text for p in d.paragraphs if p.style.name == "Heading 2"]
print("H1 count:", len(h1), "| H2 count:", len(h2))
print("TOC field present:", any("TOC" in str(p._p.xml) for p in d.paragraphs))
print("PAGE field present:", any("PAGE" in str(p._p.xml) for p in d.sections[-1].footer.paragraphs))
print("updateFields:", "updateFields" in d.settings.element.xml)

appA = [t for t in d.tables if t.rows and t.rows[0].cells[0].text.strip() == "#"]
if appA:
    print("Appendix A module rows:", len(appA[0].rows) - 1)
appG = [t for t in d.tables if t.rows and "Capability to evaluate" in t.rows[0].cells[0].text]
if appG:
    print("Appendix G checklist rows:", len(appG[0].rows) - 1)

bad = {
    "code artifacts": r"b\.(p|table|bul|callout|h[1-4])\(|self\.|\w+\.\w+\(",
    "python tokens": r"\bNone\b|\bTrue\b|\bFalse\b|_to_|not_to|theirselves|memorisefilter",
    "unverified tags": r"\[unverified\]|\[flag\]|TODO|XXX|Lorem",
    "mojibake": r"â€|Ã|\ufffd",
    "double spaces": r"[a-z]  +[a-z]",
    "stray markup": r"\*\*|__|##",
}
for name, rx in bad.items():
    hits = re.findall(rx, blob)
    print("%-16s -> %d" % (name, len(hits)), (hits[:6] if hits else ""))

# consistency of headline figures
for term in ["fifty-eight", "four hundred and sixty-nine", "one hundred and seven",
             "thirty-three hundred", "eleven exportable", "nineteen standard"]:
    print("phrase ok:", term, "->", blob.lower().count(term.lower()))
