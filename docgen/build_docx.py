# -*- coding: utf-8 -*-
"""QASWA ERP - client-facing product & feature compendium generator."""
import sys, os
from docx import Document
from docx.shared import Pt, Cm, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY   = RGBColor(0x0A, 0x25, 0x4E)
BLUE   = RGBColor(0x0F, 0x62, 0xFE)
TEAL   = RGBColor(0x00, 0x6D, 0x7A)
GREY   = RGBColor(0x53, 0x59, 0x62)
DARK   = RGBColor(0x16, 0x16, 0x16)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
HEX_NAVY  = "0A254E"
HEX_BLUE  = "0F62FE"
HEX_MIST  = "F2F6FC"
HEX_LINE  = "D3DAE3"
HEX_BAND  = "E8F1FD"
HEX_GOLD  = "B27A00"
HEX_KHAki = "EEF3E9"
FONT = "Segoe UI"

# Overridden from the command line (see main.py) to reissue the compendium
# for a different brand or prospect without touching the chapter text.
BRAND = "QASWA ERP"
CLIENT = "The management team and prospective investing partners"
ISSUED = "October 2026"
EDITION = "Release 2.0 — Compendium of features and business capability"


def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn(k.replace("_", ":")), v)
    return e


def set_run_font(run, name=FONT):
    run.font.name = name
    rpr = run._r.get_or_add_rPr()
    for tag in ("w:rFonts",):
        el = rpr.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
            rpr.append(el)
        el.set(qn("w:ascii"), name)
        el.set(qn("w:hAnsi"), name)
        el.set(qn("w:cs"), name)


def field(paragraph, instr, placeholder="1", bold=False, size=None, color=None):
    r1 = paragraph.add_run(); set_run_font(r1)
    r1._r.append(_el("w:fldChar", w_fldCharType="begin"))
    r2 = paragraph.add_run(); set_run_font(r2)
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = instr
    r2._r.append(it)
    r3 = paragraph.add_run(); set_run_font(r3)
    r3._r.append(_el("w:fldChar", w_fldCharType="separate"))
    r4 = paragraph.add_run(placeholder); set_run_font(r4)
    r4.bold = bold
    if size: r4.font.size = Pt(size)
    if color: r4.font.color.rgb = color
    r5 = paragraph.add_run(); set_run_font(r5)
    r5._r.append(_el("w:fldChar", w_fldCharType="end"))
    for r in (r1, r2, r3, r5):
        r.font.size = Pt(size or 9)
    return paragraph


def shade_cell(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    for old in tcPr.findall(qn("w:shd")):
        tcPr.remove(old)
    tcPr.append(_el("w:shd", w_val="clear", w_color="auto", w_fill=hex_fill))


def cell_margins(table, top=60, bottom=60, left=110, right=110):
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for tag, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        mar.append(_el("w:" + tag, w_w=str(val), w_type="dxa"))
    tblPr.append(mar)


def table_borders(table, color=HEX_LINE, sz=4, inside=True, box=True):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    edges = []
    if box:
        edges += [("top", sz, color), ("left", sz, color), ("bottom", sz, color), ("right", sz, color)]
    if inside:
        edges += [("insideH", 2, color), ("insideV", 2, color)]
    for tag, s, c in edges:
        borders.append(_el("w:" + tag, w_val="single", w_sz=str(s), w_space="0", w_color=c))
    tblPr.append(borders)


def no_borders(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for tag in ("top", "left", "bottom", "right", "insideH", "insideV"):
        borders.append(_el("w:" + tag, w_val="none", w_sz="0", w_space="0"))
    tblPr.append(borders)


def fixed_layout(table):
    table._tbl.tblPr.append(_el("w:tblLayout", w_type="fixed"))


def repeat_header(row):
    row._tr.get_or_add_trPr().append(_el("w:tblHeader"))


def cant_split(row):
    row._tr.get_or_add_trPr().append(_el("w:cantSplit"))


def row_height(row, mm, exact=False):
    trPr = row._tr.get_or_add_trPr()
    h = OxmlElement("w:trHeight")
    h.set(qn("w:val"), str(int(mm * 56.7)))
    h.set(qn("w:hRule"), "exact" if exact else "atLeast")
    trPr.append(h)


def para_border(p, edge="bottom", sz=8, color=HEX_BLUE, space=6):
    pPr = p._p.get_or_add_pPr()
    pBdr = pPr.find(qn("w:pBdr"))
    if pBdr is None:
        pBdr = OxmlElement("w:pBdr"); pPr.append(pBdr)
    pBdr.append(_el("w:" + edge, w_val="single", w_sz=str(sz), w_space=str(space), w_color=color))


def para_shade(p, hex_fill):
    pPr = p._p.get_or_add_pPr()
    pPr.append(_el("w:shd", w_val="clear", w_color="auto", w_fill=hex_fill))


def write(cell, text, size=9.5, bold=False, italic=False, color=DARK, align=None,
          space_after=0, space_before=0, first=False):
    p = cell.paragraphs[0] if first and not cell.paragraphs[0].runs else cell.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = 1.06
    if align: p.alignment = align
    r = p.add_run(text); set_run_font(r)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic
    r.font.color.rgb = color
    return p


# ---------------------------------------------------------------- builder
class Builder:
    def __init__(self):
        self.doc = Document()
        self._styles()
        self._pages()

    def _styles(self):
        d = self.doc
        n = d.styles["Normal"]
        n.font.name = FONT; n.font.size = Pt(10.5); n.font.color.rgb = DARK
        n._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        pf = n.paragraph_format
        pf.space_after = Pt(6); pf.space_before = Pt(0); pf.line_spacing = 1.16

        specs = {
            "Heading 1": dict(size=17, color=NAVY, bold=True, before=18, after=10, pbb=False),
            "Heading 2": dict(size=12.5, color=BLUE, bold=True, before=13, after=5, pbb=False),
            "Heading 3": dict(size=11, color=TEAL, bold=True, before=10, after=3, pbb=False),
            "Heading 4": dict(size=10.5, color=GREY, bold=True, before=8, after=2, pbb=False),
        }
        for name, s in specs.items():
            st = d.styles[name]
            st.font.name = FONT; st.font.size = Pt(s["size"]); st.font.bold = s["bold"]
            st.font.color.rgb = s["color"]; st.font.all_caps = False
            st.paragraph_format.space_before = Pt(s["before"])
            st.paragraph_format.space_after = Pt(s["after"])
            st.paragraph_format.keep_with_next = True
            st.paragraph_format.line_spacing = 1.0
            st.paragraph_format.page_break_before = s["pbb"]
            pbdr = OxmlElement("w:pBdr")
            if name == "Heading 1":
                pbdr.append(_el("w:bottom", w_val="single", w_sz="10", w_space="4", w_color=HEX_BLUE))
                pbdr.append(_el("w:left", w_val="single", w_sz="18", w_space="8", w_color=HEX_NAVY))
            for edge in ("top", "right"):
                pbdr.append(_el("w:" + edge, w_val="none", w_sz="0", w_space="0"))
            st.element.get_or_add_pPr().append(pbdr)
            st.element.get_or_add_pPr().append(_el("w:keepLines"))
            rpr = st.element.get_or_add_rPr()
            rpr.append(_el("w:rFonts", w_ascii=FONT, w_hAnsi=FONT, w_cs=FONT))

        for lid in ("List Bullet", "List Number", "List Bullet 2", "List Paragraph"):
            try:
                st = d.styles[lid]
                st.font.name = FONT; st.font.size = Pt(10.5); st.font.color.rgb = DARK
                st.paragraph_format.space_after = Pt(3)
                st.paragraph_format.line_spacing = 1.12
            except KeyError:
                pass

    def _pages(self):
        s = self.doc.sections[0]
        s.page_width = Mm(210); s.page_height = Mm(297)
        s.left_margin = s.right_margin = Cm(2.0)
        s.top_margin = Cm(1.7); s.bottom_margin = Cm(1.7)
        s.header_distance = Cm(1.0); s.footer_distance = Cm(1.0)
        s.header.is_linked_to_previous = False
        s.footer.is_linked_to_previous = False

    def new_section_body(self):
        s = self.doc.add_section(WD_SECTION.NEW_PAGE)
        s.page_width = Mm(210); s.page_height = Mm(297)
        s.left_margin = s.right_margin = Cm(2.0)
        s.top_margin = Cm(2.1); s.bottom_margin = Cm(1.8)
        s.header_distance = Cm(1.0); s.footer_distance = Cm(1.0)
        s.header.is_linked_to_previous = False
        s.footer.is_linked_to_previous = False
        return s

    # -------------------------------------------------------------- blocks
    def title_heading(self, t):
        """Front-matter title that looks like a chapter heading but is excluded from the TOC."""
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(t); set_run_font(r)
        r.font.size = Pt(17); r.bold = True; r.font.color.rgb = NAVY
        pPr = p._p.get_or_add_pPr()
        pPr.append(_el("w:outlineLvl", w_val="9"))
        pbdr = OxmlElement("w:pBdr")
        pbdr.append(_el("w:bottom", w_val="single", w_sz="10", w_space="4", w_color=HEX_BLUE))
        pbdr.append(_el("w:left", w_val="single", w_sz="18", w_space="8", w_color=HEX_NAVY))
        for edge in ("top", "right"):
            pbdr.append(_el("w:" + edge, w_val="none", w_sz="0", w_space="0"))
        pPr.append(pbdr)
        return p

    def h1(self, t): self.doc.add_paragraph(t, style="Heading 1")
    def h2(self, t): self.doc.add_paragraph(t, style="Heading 2")
    def h3(self, t): self.doc.add_paragraph(t, style="Heading 3")
    def h4(self, t): self.doc.add_paragraph(t, style="Heading 4")

    def p(self, t, size=10.5, italic=False, color=None, align=None, after=6, bold=False):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(after)
        if align: p.alignment = align
        r = p.add_run(t); set_run_font(r)
        r.font.size = Pt(size); r.italic = italic; r.bold = bold
        if color: r.font.color.rgb = color
        return p

    def lead(self, t):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(9)
        p.paragraph_format.line_spacing = 1.22
        r = p.add_run(t); set_run_font(r)
        r.font.size = Pt(11.5); r.italic = True; r.font.color.rgb = GREY
        return p

    def bullets(self, items, level=1, size=10.5):
        for it in items:
            style = "List Bullet" if level == 1 else "List Bullet 2"
            try:
                p = self.doc.add_paragraph(style=style)
            except KeyError:
                p = self.doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(2.5)
            p.paragraph_format.left_indent = Cm(0.55 if level == 1 else 1.1)
            if level == 2:
                r0 = p.add_run("– "); set_run_font(r0); r0.font.size = Pt(size); r0.font.color.rgb = GREY
            bold_head = None
            text = it
            if isinstance(it, tuple):
                bold_head, text = it
            if bold_head:
                rb = p.add_run(bold_head + "  "); set_run_font(rb)
                rb.bold = True; rb.font.size = Pt(size); rb.font.color.rgb = NAVY
            r = p.add_run(text); set_run_font(r); r.font.size = Pt(size)

    def numbered(self, items, size=10.5):
        for i, it in enumerate(items, start=1):
            p = self.doc.add_paragraph()
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.left_indent = Cm(0.85)
            p.paragraph_format.first_line_indent = Cm(-0.85)
            p.paragraph_format.line_spacing = 1.14
            r = p.add_run("%d.  " % i); set_run_font(r)
            r.bold = True; r.font.size = Pt(size); r.font.color.rgb = BLUE
            r2 = p.add_run(it); set_run_font(r2); r2.font.size = Pt(size)

    num = numbered

    def stats(self, pairs, cols=4):
        rows = (len(pairs) + cols - 1) // cols
        t = self.doc.add_table(rows=rows * 2, cols=cols)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        fixed_layout(t); no_borders(t)
        cell_margins(t, top=70, bottom=70, left=80, right=80)
        i = 0
        for r in range(rows):
            for c in range(cols):
                big = t.cell(r * 2, c); lab = t.cell(r * 2 + 1, c)
                if i < len(pairs):
                    v, l = pairs[i]; i += 1
                    write(big, v, size=17, bold=True, color=BLUE,
                          align=WD_ALIGN_PARAGRAPH.CENTER, first=True)
                    for pp in big.paragraphs:
                        pp.paragraph_format.keep_with_next = True
                    write(lab, l.upper(), size=7.5, bold=True, color=GREY,
                          align=WD_ALIGN_PARAGRAPH.CENTER, first=True)
                for cell in (big, lab):
                    shade_cell(cell, HEX_MIST)
                for p in list(big.paragraphs) + list(lab.paragraphs):
                    p.paragraph_format.space_after = Pt(0)
            for rr in (t.rows[r * 2], t.rows[r * 2 + 1]):
                cant_split(rr)
        self.doc.add_paragraph().paragraph_format.space_after = Pt(3)
        return t

    def callout(self, title, body, fill=HEX_BAND, accent=HEX_BLUE, label="BUSINESS BENEFIT"):
        t = self.doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        fixed_layout(t); no_borders(t)
        cell_margins(t, top=110, bottom=110, left=170, right=150)
        c = t.cell(0, 0)
        shade_cell(c, fill)
        tcPr = c._tc.get_or_add_tcPr()
        bd = OxmlElement("w:tcBorders")
        bd.append(_el("w:left", w_val="single", w_sz="24", w_space="0", w_color=accent))
        tcPr.append(bd)
        cant_split(t.rows[0])
        p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(2)
        r = p.add_run(label + "  ·  " if label else ""); set_run_font(r)
        r.font.size = Pt(8); r.bold = True; r.font.color.rgb = RGBColor.from_string(accent)
        if title:
            rt = p.add_run(title); set_run_font(rt)
            rt.font.size = Pt(10.5); rt.bold = True; rt.font.color.rgb = NAVY
        p2 = c.add_paragraph(); p2.paragraph_format.space_after = Pt(0)
        p2.paragraph_format.line_spacing = 1.14
        r2 = p2.add_run(body); set_run_font(r2)
        r2.font.size = Pt(10); r2.font.color.rgb = DARK
        self.doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def table(self, header, rows, widths, kind="feature", size=9.5, zebra=True,
              align_center_cols=()):
        cols = len(widths)
        has_header = header is not None
        t = self.doc.add_table(rows=(1 if has_header else 0) + len(rows), cols=cols)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        fixed_layout(t)
        table_borders(t)
        cell_margins(t)
        total = sum(widths)
        usable = 17.0
        wcm = [w / total * usable for w in widths]

        start = 0
        if has_header:
            hr = t.rows[0]
            repeat_header(hr); cant_split(hr)
            for c, text in enumerate(header):
                cell = t.cell(0, c); shade_cell(cell, HEX_NAVY)
                write(cell, text, size=size - 0.3, bold=True, color=WHITE, first=True,
                      align=WD_ALIGN_PARAGRAPH.CENTER if c in align_center_cols else None)
            start = 1
        for i, row in enumerate(rows):
            tr = t.rows[i + start]; cant_split(tr)
            fill = None
            if zebra and i % 2 == 1:
                fill = HEX_MIST
            if kind == "kv" and i % 2 == 0:
                fill = "FAFBFD"
            for c, text in enumerate(row):
                cell = t.cell(i + start, c)
                if fill: shade_cell(cell, fill)
                bold = (kind == "kv" and c == 0)
                col = NAVY if bold else DARK
                write(cell, text, size=size, bold=bold, color=col, first=True,
                      align=WD_ALIGN_PARAGRAPH.CENTER if c in align_center_cols else None)
        for r in t.rows:
            for c in range(cols):
                r.cells[c].width = Cm(wcm[c])
        for c in range(cols):
            t.columns[c].width = Cm(wcm[c])
        self.doc.add_paragraph().paragraph_format.space_after = Pt(4)
        return t

    def caption(self, text):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(8)
        r = p.add_run(text); set_run_font(r)
        r.font.size = Pt(8.5); r.italic = True; r.font.color.rgb = GREY

    def rule(self):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(8)
        para_border(p, "bottom", sz=6, color=HEX_LINE)

    def spacer(self, pts=8):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(pts)
        r = p.add_run(""); set_run_font(r); r.font.size = Pt(2)

    def pagebreak(self):
        self.doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def build_cover(b):
    d = b.doc
    b.spacer(30)
    t = d.add_table(rows=1, cols=1)
    fixed_layout(t); no_borders(t)
    cell_margins(t, top=260, bottom=260, left=260, right=260)
    c = t.cell(0, 0); shade_cell(c, HEX_NAVY)
    row = t.rows[0]; row_height(row, 46)
    p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(2)
    r = p.add_run(" ".join(BRAND.split()[0])); set_run_font(r)
    r.font.size = Pt(30); r.bold = True; r.font.color.rgb = WHITE
    p2 = c.add_paragraph(); p2.paragraph_format.space_after = Pt(10)
    r2 = p2.add_run("E N T E R P R I S E   R E S O U R C E   P L A N N I N G"); set_run_font(r2)
    r2.font.size = Pt(11); r2.font.color.rgb = RGBColor(0x9F, 0xC8, 0xFF)
    p3 = c.add_paragraph(); p3.paragraph_format.space_after = Pt(0)
    r3 = p3.add_run("The complete operating platform for finance, procurement, people, "
                    "projects, service delivery and intelligent automation.")
    set_run_font(r3); r3.font.size = Pt(11.5); r3.italic = True
    r3.font.color.rgb = RGBColor(0xD8, 0xE5, 0xFA)
    b.spacer(26)

    b.p("Product & Feature Compendium", size=22, bold=True, color=NAVY, after=2)
    b.p("A complete, plain-language guide to everything %s does for your business" % BRAND,
        size=12.5, italic=True, color=GREY, after=22)

    b.table(
        ["Document details", ""],
        [["Edition", EDITION],
         ["Prepared for", CLIENT],
         ["Prepared by", "%s Product Office" % BRAND.split()[0]],
         ["Date of issue", ISSUED],
         ["Scope", "All 58 business modules, the finance close suite, the procurement lifecycle, "
                   "the people and payroll suite, group consolidation and the %s Intelligence layer"
                   % BRAND.split()[0]],
         ["Reading time", "Approximately 60 minutes; each chapter stands alone"],
         ["Classification", "Commercial in confidence — issued for evaluation purposes"]],
        widths=[3.2, 13.8], kind="kv", size=9.5)
    b.spacer(16)
    b.p("This document deliberately avoids technical jargon. Every chapter describes what a person "
        "in your organisation can actually do, what the system does automatically, and what that "
        "means for cost, control and speed.", size=10.5, italic=True, color=GREY)
