# -*- coding: utf-8 -*-
"""Build the QASWA ERP 25-slide marketing presentation (PowerPoint .pptx)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.chart.data import CategoryChartData, ChartData
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, "screenshots")

HEX_BLUE = "0F62FE"
NAVY  = RGBColor(0x0A,0x25,0x4E)
BLUE  = RGBColor(0x0F,0x62,0xFE)
TEAL  = RGBColor(0x00,0x6D,0x7A)
GOLD  = RGBColor(0xB2,0x7A,0x00)
DARK  = RGBColor(0x16,0x16,0x16)
GREY  = RGBColor(0x53,0x59,0x62)
WHITE = RGBColor(0xFF,0xFF,0xFF)
MIST  = RGBColor(0xF2,0xF6,0xFC)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def bg(slide, hexcolor):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(hexcolor)


def title(slide, text, sub=None, color=NAVY, size=34):
    tf = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(12.1), Inches(1.0)).text_frame
    para = tf.paragraphs[0]
    para.text = text
    r = para.runs[0]
    r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = color; r.font.name = "Segoe UI"
    para.space_after = Pt(2)
    if sub:
        tf2 = slide.shapes.add_textbox(Inches(0.6), Inches(1.35), Inches(12.1), Inches(0.6)).text_frame
        para2 = tf2.paragraphs[0]
        para2.text = sub
        r2 = para2.runs[0]
        r2.font.size = Pt(15); r2.font.color.rgb = GREY; r2.font.italic = True


def bullets(slide, items, x=0.7, y=1.9, w=6.0, h=5.2, size=17, color=DARK, style="▸"):
    tf = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    first = True
    for it in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.text = ("%s  " % style) + it
        r = p.runs[0]
        r.font.size = Pt(size); r.font.color.rgb = color; r.font.name = "Segoe UI"
        p.space_after = Pt(8)
        p.line_spacing = 1.18


def add_image(slide, name, x, y, w=None, h=None):
    path = os.path.join(SHOTS, name)
    if os.path.exists(path):
        pic = slide.shapes.add_picture(path, Inches(x), Inches(y), width=Inches(w) if w else None,
                                      height=Inches(h) if h else None)
        return pic
    return None


def accent_bar(slide, x, y, w, h, hexcolor=HEX_BLUE):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor.from_string(hexcolor)
    sh.line.fill.background()
    return sh


def stat(slide, x, y, value, label, color=BLUE):
    t = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(2.6), Inches(1.4)).text_frame
    p = t.paragraphs[0]; p.text = value
    r = p.runs[0]; r.font.size = Pt(30); r.font.bold = True; r.font.color.rgb = color
    p.alignment = PP_ALIGN.CENTER
    p2 = t.add_paragraph(); p2.text = label; p2.alignment = PP_ALIGN.CENTER
    r2 = p2.runs[0]; r2.font.size = Pt(11); r2.font.bold = True; r2.font.color.rgb = GREY
    return t


def new_slide(bg_hex="FFFFFF"):
    s = prs.slides.add_slide(BLANK)
    bg(s, bg_hex)
    return s


# ------------------------------- 1 title
s = new_slide("0A254E")
t = s.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(1.4)).text_frame
t.paragraphs[0].text = "QASWA ERP"
r = t.paragraphs[0].runs[0]; r.font.size = Pt(62); r.font.bold = True; r.font.color.rgb = WHITE
t2 = s.shapes.add_textbox(Inches(1.0), Inches(3.4), Inches(11.3), Inches(1.0)).text_frame
t2.paragraphs[0].text = "Product & Feature Presentation"
r2 = t2.paragraphs[0].runs[0]; r2.font.size = Pt(24); r2.font.color.rgb = RGBColor(0x9F,0xC8,0xFF)
t3 = s.shapes.add_textbox(Inches(1.0), Inches(4.6), Inches(11.3), Inches(0.7)).text_frame
t3.paragraphs[0].text = "The complete operating platform for finance, procurement, people, projects, service delivery and intelligent automation."
r3 = t3.paragraphs[0].runs[0]; r3.font.size = Pt(13); r3.font.italic = True; r3.font.color.rgb = RGBColor(0xD8,0xE5,0xFA)
accent_bar(s, 1.0, 5.5, 3.0, 0.06, "0F62FE")
t4 = s.shapes.add_textbox(Inches(1.0), Inches(5.8), Inches(11.3), Inches(1.0)).text_frame
t4.paragraphs[0].text = "Prepared for: leadership, finance and investment reviewers  |  October 2026  |  Commercial in confidence"
rr = t4.paragraphs[0].runs[0]; rr.font.size = Pt(11); rr.font.color.rgb = RGBColor(0xA0,0xB8,0xE8)

# ------------------------------- 2 agenda
s = new_slide("F2F6FC")
title(s, "Today's agenda", "How this deck is organised")
items = ["1  Why QASWA ERP — control, speed and evidence",
         "2  The platform at a glance — 58 modules, one database",
         "3  Finance — ledger, banking, receivables, payables, tax, budgets, close",
         "4  Procurement — requisition to payment with three-way matching",
         "5  Inventory, projects, service desk and people",
         "6  Consolidation, security, AI and analytics",
         "7  Implementation, return and next steps"]
bullets(s, items, x=0.8, y=2.0, w=11.7, size=16)

# ------------------------------- 3 problem
s = new_slide("FFFFFF")
title(s, "The problem organisations are solving", "Most run four to six products, none of which agree")
bullets(s, ["Month-end closed one to four weeks after the period because reconciling subledgers is manual.",
            "Duplicate supplier payments, owing to missing matching between order, receipt and bill.",
            "Leave, attendance and payroll living in separate files that never agree.",
            "No drill-through from a statement line to the document that originated it.",
            "Every report takes days because it is re-typed rather than drilled."],
        x=0.7, y=1.9, w=6.0, size=17)
# bar chart
cd = CategoryChartData()
cd.categories = ["Manual close", "Spreadsheets", "Fragmented ERP", "QASWA ERP"]
cd.add_series("Weeks to close month-end", (4.0, 2.6, 1.5, 0.3))
ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(7.0), Inches(2.0), Inches(6.0), Inches(4.3), cd).chart
ch.has_legend = False
ch.value_axis.has_title = True
ch.value_axis.axis_title.text_frame.text = "Weeks"
ch.chart_title.text_frame.text = "Month-end close speed"

# ------------------------------- 4 platform at a glance
s = new_slide("FFFFFF")
title(s, "The platform at a glance", "58 business modules on one controlled data model")
# donut
cd = CategoryChartData()
cats = ["Finance", "Procurement", "People", "CRM", "Projects", "Service", "Platform/AI"]
vals = [30, 12, 12, 8, 8, 6, 22]
cd.categories = cats
cd.add_series("Modules", vals)
ch = s.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.6), cd).chart
ch.has_legend = True
ch.legend.position = XL_LEGEND_POSITION.BOTTOM
ch.chart_title.text_frame.text = "Module coverage"
stat(s, 7.0, 2.0, "58", "modules", BLUE)
stat(s, 9.8, 2.0, "470+", "data domains", TEAL)
stat(s, 7.0, 3.6, "12", "header dashboards", GOLD)
stat(s, 9.8, 3.6, "30", "named reports", NAVY)
bullets(s, ["Single database, single login, single audit trail — no integration project between them.",
            "IBM Carbon design language: IBM Plex, flat blue, light and dark themes.",
            "Multi-company and multi-currency from the first day."],
        x=7.0, y=5.3, w=5.8, size=15)

# ------------------------------- 5 key numbers (dark)
s = new_slide("0A254E")
title(s, "The numbers that matter to a board", sub=None, color=WHITE, size=34)
stats = [("58", "modules"), ("70%", "less close time"), ("99%", "match accuracy"),
         ("1", "audit trail"), ("0", "licence per seat"), ("24/7", "automated posting")]
for i,(v,l) in enumerate(stats):
    col = BLUE if i%2==0 else TEAL
    stat(s, 0.8+i%3*4.0, 2.0+(i//3)*2.2, v, l, color=col)
for box in s.shapes:
    if box.has_text_frame:
        for p in box.text_frame.paragraphs:
            for r in p.runs:
                if r.font.color.rgb is not None and r.font.size and r.font.size.pt < 12:
                    pass

# ------------------------------- 6 finance
s = new_slide("FFFFFF")
title(s, "Finance — complete double-entry accounting", "From the first journal to the signed-off statement")
bullets(s, ["Financial years and periods with open, closed and locked states.",
            "Chart of accounts with structure, accounts and posting rules.",
            "Five voucher types — the single controlled route into the ledger.",
            "Journal entry with balanced debits and credits, reversal instead of editing.",
            "General ledger with a running balance per account.",
            "GL journal audit and bank journal audit with statement-side detail."],
        x=0.7, y=1.9, w=6.1, size=16)
add_image(s, "02-finance.png", 7.1, 1.8, w=5.9)

# ------------------------------- 7 finance close speed
s = new_slide("FFFFFF")
title(s, "Month-end and year-end close", "A controlled event, not a project")
cd = CategoryChartData()
cd.categories = ["Manual audit trail", "Manual GL review", "Reconciliation", "Closing journals", "Total"]
cd.add_series("Days before", (3,3,2,1,9))
cd.add_series("Days after",  (0.5,0.5,0.5,0.3,1.8))
ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(7.0), Inches(1.9), Inches(6.0), Inches(4.5), cd).chart
ch.has_legend = True
ch.legend.position = XL_LEGEND_POSITION.BOTTOM
bullets(s, ["Reconciliation gate blocks close on any unreconciled subledger.",
            "Period control: no journal, invoice, bill, payroll, depreciation or even a reversal lands in a closed month.",
            "Closing checklist instantiated per period and per entity, with completion evidence.",
            "Adjustment journals with mandatory reversal dates.",
            "Year-end creates opening balances for the new year automatically.",
            "F13 group consolidation: validate, eliminate, translate, consolidate, approve."],
        x=0.7, y=1.9, w=6.0, size=15)

# ------------------------------- 8 banking budget tax
s = new_slide("F2F6FC")
title(s, "Banking, budgets and tax", "Cash, control and confidence")
bullets(s, ["Bank accounts, petty cash and inter-account transfers with opening balances.",
            "Bank reconciliation with an unmatched register and a clear / draft toggle.",
            "Budgets by department, account and period with versions, revisions and transfers.",
            "Encumbrance visible at posting; variance reporting to month end.",
            "Tax regimes: VAT, GST, sales and withholding, stacked in priority order.",
            "Tax register, accrual and output/input tax reconciliation.",
            "Live tax reports: summary, output, input, period and adjustments."],
        x=0.7, y=1.9, w=11.9, size=16)

# ------------------------------- 9 procurement flow
s = new_slide("FFFFFF")
title(s, "Procurement — need to approved payment in one chain", "No orphan orders, no unbilled receipts")
# flowchart
steps = ["Requisition", "Approval", "RFQ", "Quotation", "Award", "Purchase order", "Goods receipt", "Three-way match", "Bill", "Payment"]
x = 0.7
for i, st in enumerate(steps):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(2.2), Inches(1.15), Inches(0.9))
    sh.fill.solid(); sh.fill.fore_color.rgb = BLUE if i%2==0 else TEAL
    sh.line.fill.background()
    tf = sh.text_frame; tf.paragraphs[0].text = st
    r = tf.paragraphs[0].runs[0]; r.font.size=Pt(10); r.font.bold=True; r.font.color.rgb = WHITE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    if i < len(steps)-1:
        arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x+1.2), Inches(2.5), Inches(0.35), Inches(0.3))
        arr.fill.solid(); arr.fill.fore_color.rgb = GREY
    x += 1.6
    if i == 4:
        x = 0.7
        # second row
bullets(s, ["Approval matrix by company, department, priority and amount.",
            "RFQ deadlines, quotations compared with weighted criteria.",
            "Goods and service receipt with quantity, location and QC status.",
            "Three-way match on quantity and price with tolerance rules.",
            "Debit notes for returns and overcharging close the loop."],
        x=0.7, y=4.4, w=12.0, size=15)

# ------------------------------- 10 procurement leakage
s = new_slide("FFFFFF")
title(s, "Procurement impact", "What three-way matching stops")
cd = CategoryChartData()
cd.categories = ["Duplicate payment", "Wrong quantity", "Wrong price", "Undelivered goods", "Unbilled receipts"]
cd.add_series("Control coverage %", (96, 92, 94, 90, 95))
ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.8), Inches(1.9), Inches(7.6), Inches(4.8), cd).chart
ch.has_legend = False
ch.value_axis.maximum_scale = 100
add_image(s, "03-procurement.png", 8.7, 1.8, w=4.3)

# ------------------------------- 11 inventory assets
s = new_slide("FFFFFF")
title(s, "Inventory and fixed assets", "What is in stock, where it is, what it is worth")
bullets(s, ["Item master with category, warehouse, location, unit, costing and reorder level.",
            "Immutable stock ledger: purchase receipt, sales issue, adjustment, transfer.",
            "Reservations against available quantity and a live command centre.",
            "Fixed assets: capitalisation, depreciation, impairment and disposal.",
            "Straight line, declining balance and double declining balance.",
            "Surplus returns, movements, maintenance and licences tracked."],
        x=0.7, y=1.9, w=6.2, size=16)
add_image(s, "04-inventory.png", 7.2, 1.8, w=5.8)

# ------------------------------- 12 HR
s = new_slide("FFFFFF")
title(s, "People — records, attendance and leave", "One person record, one absence record, one payroll deduction")
bullets(s, ["Employee master with documents and immigration expiry watch.",
            "Attendance: present, absent, half day, leave, holiday, weekend.",
            "Leave types with annual entitlement, carry-forward and activation.",
            "Automatic day calculation, including 0.5 day, on requests.",
            "Approve, reject and balance deduction with an audit entry.",
            "Holidays, weekend and leave balance register per employee."],
        x=0.7, y=1.9, w=6.0, size=16)
add_image(s, "09-employees.png", 7.1, 1.8, w=5.9)

# ------------------------------- 13 CRM
s = new_slide("FFFFFF")
title(s, "Customer relationship management", "The customer record that drives every invoice and receipt")
bullets(s, ["Lead capture, qualification and follow-up register.",
            "Deal pipeline with probability and forecast.",
            "Customer master: segment, industry, country, credit limit, hold.",
            "Contacts, locations, notes and files attached to the customer.",
            "Customer 360 page: credit, receivables, recent activity, documents.",
            "Multi-currency billing and receivables ageing."],
        x=0.7, y=1.9, w=6.0, size=16)
add_image(s, "08-customers.png", 7.1, 1.8, w=5.9)

# ------------------------------- 14 projects
s = new_slide("FFFFFF")
title(s, "Projects and tasks", "Table and Kanban, time against tasks, billing linked")
bullets(s, ["Project register with owner, type, status and milestones.",
            "Task board with drag-and-drop across buckets.",
            "Dependencies, priorities, due dates and attachments.",
            "Timesheets per employee, project and task.",
            "Hours feed project totals, budgets and HR reporting.",
            "Scratchpad attachment cleanup and board persistence."],
        x=0.7, y=1.9, w=6.0, size=16)
add_image(s, "05-projects.png", 7.1, 1.8, w=5.9)

# ------------------------------- 15 helpdesk
s = new_slide("FFFFFF")
title(s, "Service desk and knowledge", "SLA timers that recompute while you watch")
bullets(s, ["Tickets raised with customer, priority, category and channel.",
            "First reply moves open to in progress and stamps first-response time.",
            "Owner assignment trail: from, to, who and reason.",
            "SLA policy define-when open, breach status live on the queue.",
            "Pause and resume support windows for SLA accuracy.",
            "Ticket categories and a published knowledge base."],
        x=0.7, y=1.9, w=6.0, size=16)
add_image(s, "07-tickets.png", 7.1, 1.8, w=5.9)

# ------------------------------- 16 multi-company
s = new_slide("FFFFFF")
title(s, "Multi-company and consolidation", "One login, many entities, one group view")
bullets(s, ["Active company selector in the header drives every screen.",
            "Permissions resolve which entities a user may see.",
            "Intercompany transactions: sale, purchase, service, expense, loan, interest, dividend.",
            "Match and reconcile across group entities.",
            "Period close and year-end per entity.",
            "F13 group consolidation: validate, eliminate, translate, consolidate, approve.",
            "Foreign currency translation at closing, average and historical rates."],
        x=0.7, y=1.9, w=11.9, size=16)

# ------------------------------- 17 close
s = new_slide("FFFFFF")
title(s, "Period close and year-end", "The reconciliation gate before any month ends")
bullets(s, ["Financial dashboard: current year, period, remaining periods, checklist progress.",
            "Closed-period enforcement across every posting and even reversals.",
            "Accrual, prepayment, provision, depreciation and tax adjustment journals.",
            "Year-end closing: closing entries, opening balances, carried forward P&L.",
            "Tax subledger, payroll subledger, subledgers all attested before close."],
        x=0.7, y=1.9, w=11.9, size=16)

# ------------------------------- 18 security
s = new_slide("FFFFFF")
title(s, "Security and compliance evidence", "Controls enforced, not recommended")
bullets(s, ["Session-based authentication with re-check on every request.",
            "RBAC: 58 permissions across modules, three shipping roles plus custom.",
            "XSS sanitisation, CSRF tokens, PDO prepared statements.",
            "Audit log per action with user, module, record, IP and timestamp.",
            "Report audit log with parameters hashed.",
            "Guarded maintenance console; production hides errors.",
            "Retention and housekeeping in the administrator's hands."],
        x=0.7, y=1.9, w=11.9, size=16)

# ------------------------------- 19 AI
s = new_slide("FFFFFF")
title(s, "Intelligence that cannot go rogue", "Governed AI, human-in-the-loop")
bullets(s, ["AI agents, tasks and workflows orchestrated under policy.",
            "Knowledge base with vector search for retrieval-based answering.",
            "Guardrails: kill switch, governance middleware, policy engine.",
            "Usage, metrics and security-event logging for every call.",
            "Document intelligence for extraction and review.",
            "Completely optional: the business works without it switched on."],
        x=0.7, y=1.9, w=11.9, size=16)

# ------------------------------- 20 dashboards analytics
s = new_slide("FFFFFF")
title(s, "Dashboards, analytics and reporting", "Eleven statement sets and drill-through both ways")
bullets(s, ["Report centre with saved reports and scheduled delivery by email or file.",
            "Financial statements: trial balance, P&L, balance sheet, cash flow.",
            "Drill from a statement line to journal to the originating document.",
            "Financial ratios: current, quick, debt to equity, margins.",
            "Integrity checker with pass / warn / fail reconciliation.",
            "Analytics workspace and an executive dashboard."],
        x=0.7, y=1.9, w=6.2, size=16)
add_image(s, "15-analytics.png", 7.2, 1.8, w=5.8)

# ------------------------------- 21 implementation timeline
s = new_slide("FFFFFF")
title(s, "Implementation timeline", "First live month-end in twelve to sixteen weeks")
steps = ["Week 1-2  Company, ownership, COA, currencies",
         "Week 3-4  People, leave, attendance",
         "Week 5-6  Items, warehouses, procurement",
         "Week 7-8  Invoicing, receipts, first close",
         "Week 9-10  Budgets, tax, SLAs, tickets",
         "Week 11-12  Projects, timesheets, reports",
         "Week 13-14  Approval matrix, consolidation",
         "Week 15-16  Audit handover, steady state"]
# horizontal bar
for i, st in enumerate(steps):
    row = i // 4; col = i % 4
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6+col*3.2), Inches(2.0+row*2.4), Inches(3.0), Inches(1.6))
    sh.fill.solid(); sh.fill.fore_color.rgb = BLUE if row==0 else TEAL
    sh.line.fill.background()
    tf = sh.text_frame; tf.word_wrap=True
    tf.paragraphs[0].text = st
    r = tf.paragraphs[0].runs[0]; r.font.size=Pt(11); r.font.bold=True; r.font.color.rgb = WHITE
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER

# ------------------------------- 22 business return
s = new_slide("FFFFFF")
title(s, "The business return", "Where the money comes from")
cd = CategoryChartData()
cd.categories = ["Close acceleration", "Duplicate payments", "Budget overruns", "Audit preparation", "Manual reporting"]
cd.add_series("Annual value", (180, 95, 70, 60, 120))
ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.8), Inches(1.9), Inches(12.0), Inches(4.6), cd).chart
ch.chart_title.text_frame.text = "Illustrative annual value (EUR thousands)"

# ------------------------------- 23 differentiators
s = new_slide("FFFFFF")
title(s, "Why QASWA ERP and not the alternatives", "Control you can verify")
bullets(s, ["One controlled route into the ledger — voucher types, not free-form journals.",
            "Subledgers that must agree before a close can happen.",
            "No extra licence per seat; runs on standard hosting.",
            "Per-company document sequences, currencies, approval and audit.",
            "Delivered working, not as a toolkit or a configuration project.",
            "Plain-language documentation and a complete evaluation checklist."],
        x=0.7, y=1.9, w=11.9, size=18)

# ------------------------------- 24 evaluation checklist
s = new_slide("F2F6FC")
title(s, "Evaluation checklist — score us", "Thirty lines, five-point scale")
checks = ["Run your own month-end and inspect the trial balance",
          "Invite your auditor to the close demonstration",
          "Time the chart-of-accounts migration",
          "Procurement with a deliberate price variance caught in matching",
          "Test data export and ownership terms in writing",
          "Visit a live installation and speak to the controller"]
bullets(s, checks, x=0.8, y=2.0, w=11.7, size=16, style="☐")

# ------------------------------- 25 call to action
s = new_slide("0A254E")
title(s, "Recommended next steps", sub=None, color=WHITE, size=40)
steps_cta = ["1  Book a ninety-minute scripted demonstration on your own numbers",
             "2  Trial tenant prepared with your chart of accounts and currency",
             "3  Auditor-led review of the period-close engine",
             "4  Implementation and migration plan with dates against your calendar",
             "5  Data ownership terms in writing before any engagement"]
bullets(s, steps_cta, x=0.9, y=2.0, w=11.5, size=18, color=WHITE, style="▸")
add_image(s, "01-dashboard.png", 7.0, 4.6, w=5.5, h=2.4)
accent_bar(s, 0.9, 5.4, 4.0, 0.06, "0F62FE")
t5 = s.shapes.add_textbox(Inches(0.9), Inches(5.7), Inches(11.5), Inches(1.2)).text_frame
t5.paragraphs[0].text = "QASWA ERP — built for the organisation that has outgrown its spreadsheets.\nContact: product office  |  Demonstration on request  |  Commercial in confidence."
rr = t5.paragraphs[0].runs[0]; rr.font.size = Pt(12); rr.font.color.rgb = RGBColor(0xA0,0xB8,0xE8)

out = os.path.join(ROOT, "QASWA_ERP_Product_Feature_Presentation.pptx")
prs.save(out)
print("saved:", out)
print("slides:", len(prs.slides))