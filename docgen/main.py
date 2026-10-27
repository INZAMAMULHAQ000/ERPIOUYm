# -*- coding: utf-8 -*-
"""Build the QASWA ERP client compendium (Word .docx).

    python main.py                                   # default brand + client
    python main.py --client "Acme Trading LLC"        # addressed to one prospect
    python main.py --brand "NORTHSTAR ERP" --out "..\\Northstar_Feature_Compendium.docx"

Then refresh Word's fields and confirm the pagination:

    powershell -ExecutionPolicy Bypass -File finalize.ps1   # updates TOC, saves, exports PDF
    powershell -ExecutionPolicy Bypass -File pagefill.ps1   # words per page, flags light pages

Chapter text lives in content_1.py … content_5.py (chapters 1-9, 10-20, 21-29, 30-38, appendices).
Styling, tables, callouts and the cover live in build_docx.py.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

import build_docx as bd
from build_docx import Builder, field, set_run_font, para_border, GREY, NAVY, HEX_LINE
import content_1, content_2, content_3, content_4, content_5, content_6


def decorate_body_section(b):
    sec = b.doc.sections[-1]

    h = sec.header
    hp = h.paragraphs[0]
    hp.paragraph_format.tab_stops.add_tab_stop(Cm(17.0), WD_TAB_ALIGNMENT.RIGHT)
    hp.paragraph_format.space_after = Pt(2)
    r = hp.add_run(bd.BRAND); set_run_font(r)
    r.font.size = Pt(8.5); r.bold = True; r.font.color.rgb = NAVY
    r2 = hp.add_run("\tProduct & Feature Compendium  ·  " + bd.EDITION.split("—")[0].strip())
    set_run_font(r2)
    r2.font.size = Pt(8.5); r2.font.color.rgb = GREY
    para_border(hp, "bottom", sz=6, color=HEX_LINE, space=3)

    f = sec.footer
    fp = f.paragraphs[0]
    fp.paragraph_format.tab_stops.add_tab_stop(Cm(8.5), WD_TAB_ALIGNMENT.CENTER)
    fp.paragraph_format.tab_stops.add_tab_stop(Cm(17.0), WD_TAB_ALIGNMENT.RIGHT)
    r = fp.add_run("Commercial in confidence"); set_run_font(r)
    r.font.size = Pt(8); r.font.color.rgb = GREY
    r = fp.add_run("\t" + bd.BRAND + "\t"); set_run_font(r)
    r.font.size = Pt(8); r.bold = True; r.font.color.rgb = NAVY
    r = fp.add_run("Page "); set_run_font(r)
    r.font.size = Pt(8); r.font.color.rgb = GREY
    field(fp, "PAGE", placeholder="1", size=8, color=GREY)
    r = fp.add_run(" of "); set_run_font(r)
    r.font.size = Pt(8); r.font.color.rgb = GREY
    field(fp, "NUMPAGES", placeholder="1", size=8, color=GREY)


def rebrand(doc, old_token, new_token):
    """Swap the product word through body, tables and frames after rendering."""
    if old_token == new_token:
        return

    def fix(paras):
        for p in paras:
            for run in p.runs:
                if old_token in run.text:
                    run.text = run.text.replace(old_token, new_token)

    fix(doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                fix(cell.paragraphs)
                for nt in cell.tables:
                    for r2 in nt.rows:
                        for c2 in r2.cells:
                            fix(c2.paragraphs)
    for sec in doc.sections:
        fix(sec.header.paragraphs)
        fix(sec.footer.paragraphs)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--brand", default="QASWA ERP", help="product name on cover, header and footer")
    ap.add_argument("--client", default=bd.CLIENT, help='"Prepared for" line on the cover')
    ap.add_argument("--issued", default=bd.ISSUED, help="date of issue on the cover")
    ap.add_argument("--edition", default=bd.EDITION, help="edition line on the cover")
    ap.add_argument("--out", default=os.path.join(REPO, "QASWA_ERP_Product_Feature_Compendium.docx"))
    a = ap.parse_args()

    bd.BRAND, bd.CLIENT, bd.ISSUED, bd.EDITION = a.brand, a.client, a.issued, a.edition

    b = Builder()
    bd.build_cover(b)
    b.new_section_body()
    decorate_body_section(b)

    for mod in (content_1, content_2, content_3, content_4, content_6, content_5):
        mod.render(b)

    b.spacer(18)
    b.p("End of compendium.", size=9, italic=True, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER)

    token = a.brand.split()[0]
    rebrand(b.doc, "QASWA", token)

    settings = b.doc.settings.element
    uf = OxmlElement("w:updateFields"); uf.set(qn("w:val"), "true")
    settings.append(uf)

    cp = b.doc.core_properties
    cp.title = "%s — Product & Feature Compendium" % a.brand
    cp.subject = "Enterprise Resource Planning: complete functional and feature guide"
    cp.author = "%s Product Office" % token
    cp.category = "Commercial in confidence"
    cp.comments = "%s — %s. Non-technical feature compendium for client evaluation." % (a.edition, a.issued)
    cp.keywords = "ERP, %s, finance, procurement, HRMS, payroll, consolidation, AI, enterprise" % token

    b.doc.save(a.out)

    words = 0
    for p in b.doc.paragraphs:
        words += len(p.text.split())
    for t in b.doc.tables:
        for row in t.rows:
            for c in row.cells:
                words += len(c.text.split())
    print("saved:", a.out)
    print("brand:", a.brand, "| prepared for:", a.client)
    print("paragraphs:", len(b.doc.paragraphs), "tables:", len(b.doc.tables))
    print("approx words:", words)


if __name__ == "__main__":
    main()
