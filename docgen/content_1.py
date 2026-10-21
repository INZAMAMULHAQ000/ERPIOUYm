# -*- coding: utf-8 -*-
from build_docx import Builder, write, HEX_NAVY, HEX_BLUE, HEX_MIST, HEX_BAND, HEX_GOLD, HEX_KHAki, GREY, NAVY, BLUE, TEAL, WHITE
from docx.enum.text import WD_ALIGN_PARAGRAPH


def toc_page(b):
    d = b.doc
    b.title_heading("Contents")
    b.p("Right-click anywhere in this list once the document is open in Microsoft Word and choose "
        "“Update Field” to refresh the page numbers.", size=9, italic=True, color=GREY, after=10)
    from build_docx import field
    para = d.add_paragraph()
    field(para, r'TOC \o "1-1" \h \z \u', placeholder="Table of contents will appear here after Word updates the field.")


def how_to_read(b):
    d = b.doc
    b.pagebreak()
    d.add_paragraph("How to read this document", style="Heading 1")
    d.paragraphs[-1].paragraph_format.page_break_before = False
    b.lead("Every chapter answers three questions in plain business language: what can a person do, "
           "what does the system do on its own, and what does that change for the business. Nothing in "
           "these pages requires technical knowledge to follow.")
    b.table(
        ["Element", "What it tells you"],
        [["Capability tables", "A named feature, exactly how it behaves in day-to-day use, and the value it delivers."],
         ["Business benefit panels", "The commercial consequence — time saved, risk removed, cash recovered, audit avoided."],
         ["At-a-glance counters", "Verified scale of the platform: modules, reports, permissions, documents."],
         ["Chapter on its own page", "Each of the 38 chapters begins on a fresh page so you can extract and circulate it."],
         ["Appendices", "The complete index of modules, reports, documents, configuration lists and a glossary."],
         ["Release roadmap", "What arrives in the next phase, stated openly so commitments are never over-claimed."]],
        widths=[3.6, 13.4], kind="kv")
    b.callout("One platform, one version of the truth",
              "QASWA ERP was built as a single connected product rather than a collection of purchased "
              "modules stitched together. A purchase requisition, a goods receipt, a supplier bill, a "
              "journal entry, a budget line and a consolidated group balance sheet all sit in the same "
              "database, under the same approval rules, and carry the same audit trail. That is why the "
              "system can tell you — today, not next quarter — what a decision will cost.")


def render(b):
    toc_page(b)
    how_to_read(b)

    # ------------------------------------------------------------------ 1
    b.h1("1.  Executive Summary")
    b.lead("QASWA ERP is a complete enterprise operating platform for a mid-sized to large "
           "organisation that wants finance, procurement, people, projects, customer-facing "
           "operations and an artificial-intelligence layer running on one system, under one set "
           "of controls, with one audit trail.")
    b.p("Most organisations buy four or five separate products to cover this ground — an accounting "
        "package, a procurement tool, an HR system, a helpdesk and, increasingly, a separate AI "
        "assistant — and then pay consultants for years to keep the interfaces between them alive. "
        "QASWA ERP removes that architecture. Everything described in this document runs natively "
        "inside the same application, on the same permission model, against the same master data, "
        "and is visible on the same dashboards.")
    b.stats([("58", "Business modules"), ("469", "Data domains"), ("100+", "Reports & statements"),
             ("300+", "Permission points"), ("107", "AI services"), ("12", "Document sequences")])
    b.h2("What the platform delivers")
    b.bullets([
        ("Accounting that closes itself.", "Every operational document — an invoice, a supplier bill, "
         "an expense claim, a depreciation run, a payroll posting, a stock movement, an intercompany "
         "transfer — generates its own double-entry journal through a single controlled posting gateway. "
         "Nobody re-keys figures, and nothing reaches the ledger without passing the same validation."),
        ("Procurement you can defend.", "The full requisition-to-payment chain is enforced rather than "
         "advised: requisitions, approval matrices, requests for quotation, weighted bid comparison, "
         "purchase orders, goods receipt with inspection, three-way matching with tolerances, and payment "
         "allocation. Over-ordering, over-receipt and over-billing are blocked by the system."),
        ("People operations without spreadsheets.", "Personnel records with document-expiry surveillance, "
         "attendance registers, leave entitlements and balances, contractor engagement and rate history, "
         "timesheets, and the workforce cost posted into finance."),
        ("Group-level financial control.", "Multi-company trading with per-company financial years, an "
         "intercompany engine that books the mirror entry in the partner company automatically, matching "
         "and reconciliation, and a consolidation workspace that produces group statements with eliminations "
         "and currency translation."),
        ("A disciplined month-end and year-end.", "A template-driven closing checklist, a validation gate "
         "that refuses to close a period until the numbers actually reconcile, controlled reopening with a "
         "mandatory written reason, and a year-end close that carries balances forward exactly once."),
        ("AI that is permitted, not unleashed.", "One hundred and seven AI services sit behind a central "
         "policy engine: risk tiers, mandatory human confirmation for writes, budget estimation before "
         "execution, roughly forty individual kill switches and six one-command emergency shutdowns."),
    ])
    b.h2("Who it is for")
    b.table(
        ["If you are…", "The platform gives you…"],
        [["A group CFO or financial controller",
          "Locked periods, immutable posted vouchers, an integrity checker that reconciles subledgers to the "
          "general ledger, and consolidation that validates before it is allowed to post."],
         ["A head of procurement or operations",
          "Savings measured against the requisition estimate, auditable award decisions with override reasons, "
          "and a supplier performance picture built from actual quote-and-win behaviour."],
         ["An HR leader",
          "One directory of every person your organisation deals with, expiring-visa and contract alerts, live "
          "leave balances, and workforce cost that lands in the ledger without manual effort."],
         ["A service or project manager",
          "Drag-and-drop task boards, milestones, logged hours, a ticket queue with live SLA breach detection, "
          "and a knowledge base your customers and staff can both search."],
         ["A business owner or investor",
          "An executive dashboard with year-to-date revenue, margin, headcount, overdue invoices, open critical "
          "tickets and the twelve-month trend — all from live data, refreshed on every screen visit."],
         ["An IT or compliance lead",
          "Role-based access on every button, an audit trail carrying user, action, module, IP address and "
          "timestamp, hardened hosting rules, and checksummed, test-restored backups."]],
        widths=[4.2, 12.8], kind="kv")
    b.callout("Bottom line",
              "QASWA ERP replaces the accounting package, the purchasing spreadsheet, the HR file cabinet, "
              "the helpdesk inbox and the standalone AI assistant with one licensed, one-team-operated "
              "platform — and it does that without giving up the financial controls an auditor expects.",
              label="THE PROPOSITION")

    # ------------------------------------------------------------------ 2
    b.h1("2.  The Platform at a Glance")
    b.lead("A single page you can keep on your desk. Every figure below describes capability that is "
           "present in the product today.")
    b.table(
        ["Area", "What is included", "Scale"],
        [["Finance and accounting",
          "Chart of accounts, vouchers and journals, general ledger, opening balances, banking, cash, petty cash, "
          "transfers, reconciliation, accounts receivable, accounts payable, expenses, budgets, tax, fixed assets, "
          "period and year-end close, consolidation",
          "52 finance work areas"],
         ["Procurement and supply chain",
          "Requisitions, approval matrix, RFQ, vendor quotations, weighted comparison, purchase orders with formal "
          "revisioning, goods and service receipts with inspection, vendor bills with three-way match, payments, "
          "debit notes",
          "10-stage lifecycle"],
         ["Inventory and assets",
          "Item master, immutable stock ledger, multi-warehouse balances, reservations, adjustments, transfers, "
          "physical count, valuation and cost audit; asset register, capitalisation, depreciation, assignment, "
          "return, maintenance, licences",
          "5 costing methods"],
         ["People and payroll",
          "Employee master, departments, designations, attendance, leave types and balances, holidays, timesheets, "
          "contractors and contracts, unified people directory, payroll posting, payment batches, reconciliation",
          "11 workforce modules"],
         ["Customers and service",
          "Leads with seven sources, six-stage pipeline board, a customer master of unusual depth, contacts, "
          "locations, credit control, invoices, receipts, credit notes, statements, ageing, tickets, SLA policies, "
          "knowledge base",
          "~98-field customer record"],
         ["Projects",
          "Project register, milestones, tasks with sub-task checklists, tags, multi-assignee ownership, "
          "drag-and-drop board, discussion, activity trail, timesheet capture, project-billed invoices",
          "6 statuses, 4 priorities"],
         ["QASWA Intelligence (AI)",
          "Assistant chat, universal copilot, natural-language navigation, voice, document intelligence with OCR, "
          "retrieval-augmented knowledge, correspondence drafting, analytics and forecasting, process intelligence, "
          "agents, workflow studio, automations, workspaces, insights and monitors",
          "107 services, 30+ screens"],
         ["Reporting",
          "Report centre, an export centre producing eleven statement sets in three formats, template designer, "
          "saved reports, scheduled delivery, analytics dashboards, executive dashboard, financial ratios",
          "100+ named reports"],
         ["Control and administration",
          "Roles and granular permissions, company master with ownership hierarchy, configuration console, "
          "currency and FX maintenance, document numbering, editable lookup lists, audit and activity logs, "
          "menu and widget administration",
          "300+ permission points"]],
        widths=[3.1, 10.1, 3.8], size=8.8)
    b.h2("Coverage by business function")
    b.table(
        ["Function", "Covered end to end", "Partially covered"],
        [["Accounting and ledger", "Yes — setup to year-end close", "—"],
         ["Statutory reporting", "Trial balance, P&L, balance sheet, cash flow, GL", "Consolidated statements"],
         ["Purchasing", "Requisition to payment with matching", "Supplier scorecards"],
         ["Stock control", "Ledger, valuation, transfers, counting", "Bar-code scanning"],
         ["Sales order processing", "Invoicing and receipts", "Quotation and order books (see roadmap)"],
         ["Payroll calculation", "Posting, payable, batch, reconciliation", "Salary-board computation (see roadmap)"],
         ["Human resources", "Records, attendance, leave, onboarding", "Recruitment, appraisal, exit"],
         ["Customer relationship", "Leads, pipeline, master, service", "Campaign management"],
         ["Service desk", "Tickets, SLA, knowledge base", "Customer self-service portal"],
         ["Project delivery", "Tasks, milestones, time", "Budget and profitability"],
         ["Intelligent automation", "Documents, knowledge, agents, governance", "—"]],
        widths=[5.0, 8.0, 4.0], size=9, align_center_cols=())
    b.callout("Read this honestly",
              "Where a function is marked “partially covered”, the surrounding business process still works "
              "today — the note identifies the specific convenience layer that arrives in the next release. "
              "Chapter 37 sets these out precisely so that nothing in this document surprises you later.",
              fill="FFF6E5", accent=HEX_GOLD, label="NOTE")

    # ------------------------------------------------------------------ 3
    b.h1("3.  Why Organisations Choose QASWA ERP")
    b.lead("Six differentiators that change day-to-day outcomes rather than merely appearing on a feature list.")
    b.h2("3.1  One posting gateway for every document")
    b.p("There is exactly one route into the general ledger. Whether the source is an approved invoice, a "
        "reimbursed expense claim, a depreciation run, an asset disposal, a bank transfer, a tax adjustment, "
        "a payroll posting, a closing journal or an intercompany counterpart, the entry passes the same "
        "checks: it must have lines, debits must equal credits, the accounts must exist and be active, the "
        "date must fall inside the company's own financial year, the period must not be locked, and the "
        "company must be identified. Reports never write balances; dashboards never create entries. That is "
        "why the numbers on the executive dashboard and the numbers in the trial balance always agree.")
    b.h2("3.2  Controls that are enforced, not recommended")
    b.bullets([
        "A posted voucher cannot be edited or deleted. It is corrected by a reversal that creates the mirror entry, swaps debits and credits, links the two documents and stamps the original as reversed.",
        "A requester can never approve their own requisition, however the approval matrix is configured.",
        "A goods receipt must be completed before the matching bill can post, and billed quantities and values cannot exceed what the order and receipt actually allow.",
        "A closed period refuses journals, invoices, bills, receipts, payments, expenses, payroll, depreciation, tax postings — and even the reversal that would land inside it.",
        "Reopening a period or a financial year requires a written reason and records the person, timestamp and IP address. Silent reopening is impossible.",
        "A year closes once. The operation is repeat-safe, so opening balances can never be duplicated by an accidental second run.",
        "A claim cannot be reimbursed twice, and a concurrent second approval is rejected with a message that the record changed under the user.",
    ])
    b.h2("3.3  Depth where it matters: master data")
    b.p("Most systems store a name and a phone number for a customer and a code for an account. QASWA ERP "
        "carries a customer record of nearly a hundred attributes — identity and grouping, contacts and "
        "channel preferences, structured addressing, commercial terms, credit limit, rating and hold, "
        "delivery and Incoterms, banking, tax registration and exemption detail, industry and size bands, "
        "assigned account, sales and support representatives, and consent flags. The company master is "
        "equally deep, carrying entity type, parent and subsidiary links with ownership percentages, "
        "consolidation method, accounting framework, statutory registrations, e-invoicing regime, fiscal "
        "year start and default ledger accounts. This depth is what lets the system behave correctly without "
        "being told repeatedly.")
    b.h2("3.4  Intelligence that cannot go rogue")
    b.p("The AI layer was designed with the assumption that it will eventually be asked to do something "
        "wrong. Every AI operation passes a central policy engine. Risk is tiered low, medium, high and "
        "critical; high-risk work is diverted into a human review queue; writes always require confirmation "
        "and pending actions expire; approvals are cryptographically bound to the exact parameters, so "
        "changing one number in a proposed action voids the approval. The AI is never given credentials, "
        "cannot run arbitrary database queries, cannot execute files, and cannot reach routes that have not "
        "been registered for it. Roughly forty individual kill switches and six one-click emergency "
        "shutdowns are operated by a named administrator and audited. Chapter 29 is dedicated to this.")
    b.h2("3.5  A closing process a controller can sign")
    b.p("Period and year-end close are treated as controlled events rather than a month's worth of "
        "spreadsheets. The checklist is instantiated per period from a template, each item can be marked "
        "pending, in progress, completed or exception with comments and supporting attachments, and a "
        "validation gate runs a battery of tests before the close is allowed to proceed. When a test fails, "
        "the system names the problem, the module and the required action. A period is never left half closed.")
    b.h2("3.6  Delivered as a working product, not a toolkit")
    b.p("Nothing in this document requires a development project before it can be used. Modules are already "
        "built, screens already exist, reports already run. Configuration — chart of accounts, tax regimes, "
        "approval rules, document formats, currencies, lookup lists and permission sets — is done in "
        "application screens by your own administrators. The implementation chapter in this document sets out "
        "a realistic sequence for a live deployment.")
    b.callout("The commercial consequence",
              "Fewer interfaces means fewer licences, fewer reconciliation breaks, fewer consultant hours and "
              "far fewer questions that end with “that is in a different system”. Controls being enforced "
              "rather than documented means audit findings move from recurring exceptions to evidence trails.",
              fill=HEX_KHAki, accent="3E6B3E", label="WHY IT MATTERS")

    # ------------------------------------------------------------------ 4
    b.h1("4.  The Everyday Working Experience")
    b.lead("Before any module, the shell: what a person sees when they sign in, and the interface "
           "conventions that stay identical everywhere in the product.")
    b.h2("4.1  Sign-in and identity")
    b.p("Users sign in with an email address and password on a clean branded screen. The session is issued "
        "fresh at each sign-in, and every page the user opens re-checks that the account is still live. If an "
        "administrator deletes, suspends or deactivates an account while the person is working, the open "
        "session ends immediately with an explanation rather than continuing quietly. Signing out destroys "
        "the session and records the event.")
    b.h2("4.2  The home dashboard")
    b.bullets([
        ("Personal layout.", "Each user arranges their own dashboard. A Customize mode exposes a widget "
         "catalogue, lets the person drag widgets into order, add or remove them, resize them, and save; "
         "a restore-default action is always available."),
        ("Separate layouts.", "Home, Executive, Helpdesk, Finance, Leave, Analytics and Assets each hold "
         "their own arrangement, so switching context does not scramble the previous one."),
        ("Permission-aware widgets.", "Individual tiles carry their own permission, so an executive KPI can "
         "be withheld from a broader audience without hiding the whole dashboard."),
        ("Remembered position.", "Finance list screens remember where the user had scrolled and restore it "
         "when they return from a detail page."),
    ])
    b.h2("4.3  Navigation")
    b.table(
        ["Element", "Behaviour"],
        [["Sidebar", "Grouped sections that auto-expand around the page you are on and mark the active link; "
                     "collapses on desktop and becomes a slide-over with a backdrop on phones."],
         ["Permission gating", "Every link, tab, button, export and card is individually gated. Users do not see "
                               "what they cannot use, and direct attempts to reach a forbidden screen return an "
                               "access-denied explanation."],
         ["Breadcrumbs", "Generated automatically from where the page sits, so a person can always step back a level."],
         ["Company picker", "Appears in the top bar as soon as two or more companies exist; each switch is "
                            "re-validated against the user's access."],
         ["Currency picker", "Lists every active currency; displayed amounts convert using the latest effective rate."],
         ["Theme toggle", "One click to IBM-style light or dark, available on every screen including sign-in."],
         ["Menu management", "Administrators can add, reorder, indent, rename, icon-set, route and enable or "
                             "disable sidebar sections and items, each tied to a permission."]],
        widths=[3.4, 13.6], kind="kv")
    b.h2("4.4  The list-screen pattern")
    b.p("Every register in the product follows the same shape, which is why people learn it once. Above the "
        "table sit count tiles that summarise the current filter. A search box matches across the obvious "
        "fields. Column filters cover status, department, owner, date range and category. Column headings "
        "sort ascending and descending. Pagination states “showing x to y of n” and preserves every active "
        "filter in its links. Status and priority are shown as colour-coded chips rather than words alone. "
        "A clear-filters action resets the view, and empty states explain what to do next rather than simply "
        "being blank. Row actions are view, edit and — where the permission allows — delete, and deletions go "
        "through a confirmation panel that closes with Escape.")
    b.h2("4.5  Forms and data safety")
    b.bullets([
        "Required fields, formats and ranges are checked as the person types, with the message appearing beside the field.",
        "If a save fails validation, the data entered is preserved and the error list is restored — nobody retypes a long form.",
        "Document numbers are offered as a preview while the user types, and only consumed when the record is actually saved.",
        "Money fields recalculate on the server; totals shown in the browser are never trusted as the posted figure.",
        "Attachments accept the file types each screen defines, record size and uploader, and are served through a controlled download rather than a public path.",
        "Duplicate protection is built in at the places that matter: employee and vendor codes, account codes, bank account numbers, invoice numbers per vendor, asset serials, financial year names, budget names and lines, expense category names and voucher prefixes.",
    ])
    b.h2("4.6  Appearance")
    b.p("The interface follows the IBM Carbon design language: IBM Plex typography, flat blue accents, "
        "square geometry, restrained motion. Two themes ship — a light working theme and a full dark theme in "
        "which tables, badges, tabs and charts all restyle rather than merely inverting. The choice is "
        "remembered in the browser, in the session and against the user record, so it survives sign-out and "
        "follows the person between tabs. Reduced-motion preferences are honoured. Layouts reflow at three "
        "breakpoints, and wide tables become scrollable rather than crushing on a phone.")
    b.h2("4.7  Print and reading")
    b.p("Statements, registers, invoices, asset reports and closing documents can be produced as dedicated "
        "print views that strip navigation, keep the company identity and header block, and carry totals "
        "rows. The export centre additionally renders landscape A4 documents for eleven statement sets.")
    b.callout("Why the shell matters",
              "A platform only gets used if people can find things and the screens behave predictably. "
              "Because the pattern repeats across fifty-eight modules, training time collapses: a person who "
              "learns the vendor register already knows the stock ledger, the ticket queue and the asset list.")

    # ------------------------------------------------------------------ 5
    b.h1("5.  Finance I — Core Accounting and the General Ledger")
    b.lead("The foundation everything else posts into: the chart of accounts, voucher design, journal "
           "entry, the ledger itself, and the rules that protect it.")
    b.h2("5.1  Financial years and accounting periods")
    b.bullets([
        "Create, edit, activate and archive financial years per company, each with its own name, start and end dates and display format; duplicate year names within a company are refused.",
        "One action generates the full monthly period calendar for a year, so period-level control exists from day one rather than being retrofitted mid-year.",
        "Periods progress Open → Closing → Closed → Archived, and the status is visible wherever a date could be entered.",
        "The finance dashboard header states the active year and its date range so nobody posts into the wrong period by accident.",
    ])
    b.h2("5.2  Chart of accounts")
    b.p("Accounts are maintained with a code, name, account group, account type, nature (asset, liability, "
        "equity, income or expense), a parent-group hierarchy presented as a tree, an opening balance with "
        "its debit or credit direction, a display order, an active flag, and a switch that decides whether "
        "manual journals may touch the account at all. Code uniqueness is enforced with a configurable "
        "prefix, and a live search plus filters make an established chart easy to navigate. Account groups "
        "and account types are themselves maintainable, with their own parent relationships, statement "
        "nature and normal direction — which is what allows new accounts to be created safely without "
        "breaking reporting.")
    b.h2("5.3  Voucher design")
    b.table(
        ["Attribute", "What it controls"],
        [["Voucher type name", "The human label used on journals, reports and printed documents."],
         ["Prefix", "The leading characters of the automatically assigned document number."],
         ["Auto-numbering switch", "Turn automatic numbering on or off per voucher type; more than thirty voucher books are configured in a typical installation."],
         ["Status", "Retire a voucher type without deleting history or orphaning posted journals."],
         ["Company scope", "Each company maintains its own voucher books and numbering, with no borrowing from another entity."]],
        widths=[4.0, 13.0], kind="kv")
    b.h2("5.4  Journal entry")
    b.p("A journal is captured with a voucher date, voucher type, description and reference, and an "
        "unlimited line grid. Lines are added and removed freely, and the screen shows running debit and "
        "credit totals with a balanced indicator, so the person preparing the entry always knows whether it "
        "can post. Entries are saved as drafts, reviewed, and then posted. Drafts remain editable; posted "
        "vouchers do not.")
    b.h2("5.5  The posting rules")
    b.p("No entry reaches the ledger unless it satisfies the same controlled checks. Each is stated here "
        "because together they are the reason the ledger can be trusted.")
    b.bullets([
        "The entry must be a draft at the moment of posting, and must be the current version of that draft.",
        "There must be at least one line, and total debits must exactly equal total credits.",
        "Every account referenced must exist, be active, and be permitted to receive manual entries.",
        "The voucher date must fall inside the financial year of the company on the journal.",
        "The accounting period containing the date must not be closed or locked.",
        "The journal must carry a company; the engine will not default to another entity's year or fall back to a hard-coded company.",
    ])
    b.h2("5.6  Reversal instead of editing")
    b.p("Correcting a posted entry raises a reversal. The system creates a mirror journal with the debits and "
        "credits swapped, numbers it with a reversal suffix, stamps the original as reversed and links the two. "
        "The history stays intact, which is what an auditor and a tax authority expect, and the correction is "
        "traceable from either end.")
    b.h2("5.7  The ledger")
    b.p("Every posting writes to the general ledger with a running balance per account. The ledger can be "
        "browsed by account and date range; opening balances are held per financial year and can be verified "
        "against the prior year's closing. From the ledger the user can step directly to the journal voucher "
        "behind any line, and from an account ledger step back to the journal — the drill path is two clicks "
        "in either direction.")
    b.callout("What this prevents",
              "Unbalanced ledgers, silent edits to posted history, accounts that quietly stop reporting "
              "correctly because the wrong nature was chosen, and the classic audit finding of a transaction "
              "changed after the fact. In their place: an immutable record, linked corrections, and a chart "
              "that stays structurally sound as it grows.")

    # ------------------------------------------------------------------ 6
    b.h1("6.  Finance II — Banking, Cash and Reconciliation")
    b.lead("Money movement outside the sales and purchase cycle: bank and cash accounts, transfers, petty "
           "cash, and the reconciliation discipline that makes month-end provable.")
    b.h2("6.1  Account maintenance")
    b.p("Bank accounts and cash accounts are maintained with their identifiers, opening balances and the "
        "ledger account they control. Duplicate account numbers are refused, so two screens can never end up "
        "reconciling different versions of the same bank.")
    b.h2("6.2  Deposits, withdrawals and transfers")
    b.bullets([
        "Bank transactions are recorded as deposits or withdrawals with a method, reference, offset account and amount; the system posts the journal automatically.",
        "Cash transactions behave the same way for physical cash holdings, with the same offset-account control — an offset into the same account is blocked.",
        "Money transfers move funds between any bank or cash pairing and generate their own voucher, so a transfer is never a manual pair of journals that might not balance.",
    ])
    b.h2("6.3  Petty cash")
    b.p("Floats are maintained with a custodian and running balance. Issue, top-up and expense are each "
        "recorded with a category and offset account, producing a fund position and an activity log. Because "
        "each movement posts through the same gateway, the float balance on screen and the balance in the "
        "ledger are the same number.")
    b.h2("6.4  Bank reconciliation")
    b.table(
        ["Step", "What happens"],
        [["Start", "Enter the statement date and the statement closing balance. The system pulls the book balance from the ledger."],
        ["See the gap", "The difference is displayed and highlighted in red until it reaches nil, so the size of the problem is always visible."],
        ["Match", "Each unreconciled ledger line is ticked against the statement. Running matched and unmatched totals update as the user works."],
        ["Note", "Remarks can be recorded against the reconciliation for the reviewer who comes after."],
        ["Complete", "Completing writes the reconciliation state; reconciliations already completed or cancelled are protected from being silently altered."],
        ["Escalate", "The finance dashboard shows in-progress reconciliations as an alert with a jump link, so an open reconciliation cannot be forgotten."]],
        widths=[2.4, 14.6], kind="kv")
    b.h2("6.5  Cash visibility")
    b.p("The finance home shows total bank balance, total cash balance, today's deposits and withdrawals, "
        "today's posted journals with debit and credit totals, and pending drafts. A treasurer therefore "
        "sees the day's position without opening a single report.")
    b.callout("Business benefit",
              "Reconciliation stops being an end-of-month scramble. Because the difference is displayed on "
              "screen and an incomplete reconciliation raises an alert, the average time to detect a bank "
              "discrepancy falls from weeks to the same day — and closing cannot proceed until it is resolved.")

    # ------------------------------------------------------------------ 7
    b.h1("7.  Finance III — Accounts Receivable and Customer Billing")
    b.lead("From the invoice you raise to the cash you collect, including credit notes, statements, ageing "
           "and the customer's own view of their account.")
    b.h2("7.1  The receivable dashboard")
    b.bullets([
        "Total receivables, invoices raised this month, payments received and an ageing summary at the top of the screen.",
        "Average collection days and the top outstanding customers, so attention goes where the money is.",
        "An invoice trend that separates one-off spikes from a genuine deterioration.",
        "Every tile links through to the filtered list behind it.",
    ])
    b.h2("7.2  Raising an invoice")
    b.table(
        ["Part of the invoice", "What the system does"],
        [["Number", "Assigned from the company's invoice sequence; prefix, padding and counter are administrator-editable and the next number is previewable without consuming it."],
         ["Customer and defaults", "Trading currency, tax-inclusive behaviour, price list, payment terms, delivery channel, invoice email and copy list flow from the customer master."],
         ["Due date", "Derived from payment terms written as “Net N days”, defaulting to thirty days when nothing is specified."],
         ["Lines", "Add or remove freely: item, description, quantity, unit, price, line discount percentage, and per-line tax treatment with taxable, zero-rated, exempt or out-of-scope status and an exemption reference."],
         ["Totals", "Subtotal, header discount by percentage or amount, tax, grand total, paid and outstanding — recalculated on the server, never trusted from the browser."],
         ["Project", "An optional project link, so invoicing can be traced to delivery work."],
         ["Notes and terms", "Free-text notes and standing terms and conditions appear on the printed document."]],
        widths=[4.0, 13.0], kind="kv")
    b.h2("7.3  The invoice lifecycle")
    b.p("Draft → approved → sent → partially paid → paid, with overdue and cancelled states. Approval posts "
        "the double entry automatically: receivable debited, revenue credited, output tax credited. A "
        "status-change history records the previous state, the new state, who made the change and the note "
        "they added. An invoice can be duplicated into a new draft — useful for recurring billing — and the "
        "duplication is itself audited.")
    b.h2("7.4  Printing and presenting to the customer")
    b.p("A dedicated print view produces a customer-facing invoice showing the customer's own VAT or GST "
        "number, the company identity from the company master, and the document header. Rendering passes "
        "through the template designer, so the layout is yours rather than a vendor default.")
    b.h2("7.5  Receipts and allocation")
    b.p("A customer receipt carries a system receipt number, date, customer, payment method, reference or "
        "cheque number, and the bank or cash account that received it — the account fields appear only for "
        "the methods that need them. The receipt can then be allocated across open invoices on a dedicated "
        "allocation screen; over-allocation is blocked, invoice balances and paid status update immediately, "
        "and the receipt's unallocated balance remains on account for later application. Each payment leg "
        "generates its own journal.")
    b.h2("7.6  Credit notes")
    b.p("A credit note is raised against an invoice, typed as price correction, return, discount adjustment "
        "or cancellation, with reason, tax treatment and totals. It moves draft → issued → applied → "
        "cancelled and posts the reversing revenue, tax and receivable entries with the journal linked. "
        "Numbering follows the CN plus year-month plus sequence pattern.")
    b.h2("7.7  Statements and ageing")
    b.bullets([
        ("Customer statement.", "Any from-and-to period, with the opening balance computed from pre-period activity, then invoices, receipts and credit notes interleaved with a running balance and period totals. One-click print produces a clean statement with navigation removed."),
        ("Ageing.", "Current, 1–30, 31–60, 61–90 and over-90-day buckets as at a chosen date, colour-coded, "
         "with the individual overdue invoices listed inside each bucket and days overdue shown per invoice."),
        ("Collection focus.", "Overdue balances render in red wherever they appear, including the customer master and the 360 view."),
    ])
    b.callout("Business benefit",
              "Receivables stop being a monthly surprise. With ageing visible per customer and per invoice, "
              "average collection days reported on the dashboard, and credit limits and hold states carried "
              "on the customer record, collections becomes a daily routine rather than a quarterly "
              "conversation.")

    # ------------------------------------------------------------------ 8
    b.h1("8.  Finance IV — Accounts Payable and the Vendor Ledger")
    b.lead("Everything that leaves the organisation: bills, matching, approval, payment, debit notes and the "
           "vendor's own account view.")
    b.h2("8.1  Payable dashboard")
    b.p("Outstanding payables, bills raised this month, payments made this month and ageing sit on the same "
        "screen as unbilled receipts and open matching exceptions. The dashboard is therefore a work list: "
        "it shows what is owed, what has been received but not yet billed, and what the matching engine has "
        "refused to accept.")
    b.h2("8.2  Vendor bills")
    b.table(
        ["Control", "Behaviour"],
        [["Identity", "Vendor, bill date, due date, currency and the vendor's own invoice number."],
         ["Links", "Optional purchase order and goods receipt links; a bill can reference a service receipt as well as a goods receipt."],
         ["Duplicate watch", "The vendor's own invoice number is checked for uniqueness per vendor and company, and can be switched on or off where a vendor legitimately reuses references."],
         ["Lines", "Per-line tax type, rate, group and status — taxable, exempt, zero-rated or out of scope — with exemption reference, and a ledger expense account on every line."],
         ["Matching", "Billed quantity and value cannot exceed the remaining unbilled order or receipt value unless an authorised override is recorded."],
         ["States", "Draft, pending approval, matched, exception, approved, posted, rejected, cancelled."],
         ["Posting", "Approval creates the purchase voucher: expense debited by account, input tax debited, total credited to accounts payable, tax-return data recorded, and the bill marked posted with the journal linked."],
         ["Order effect", "The purchase order automatically moves to partially or fully billed and remaining billable quantities are recomputed."]],
        widths=[2.8, 14.2], kind="kv")
    b.h2("8.3  Payments")
    b.p("Vendor payments carry an automatic payment number, date, method, the bank or cash account funding "
        "them, a reference and the amount. Open bills load on the screen so the payment can be allocated "
        "across them; bills move to partially paid or paid with a status-history line, and the payment journal "
        "is generated by the system.")
    b.h2("8.4  Debit notes")
    b.p("Debit notes reduce payable balances and reverse expense and input tax. They are typed as return, "
        "price correction, discount adjustment or cancellation, carry a reason and tax treatment, and move "
        "draft → issued → applied → cancelled with an automatic reversing journal.")
    b.h2("8.5  Vendor statements and days payable")
    b.bullets([
        "Vendor statements for any period, in the same running-balance format used for customers.",
        "Accounts payable ageing with overdue bills identified individually and days-payable-outstanding computed rather than eyeballed.",
        "The vendor 360 view shows total billed, paid, outstanding and overdue, purchase order count, recent bills, recent payments and recent orders on one page.",
    ])
    b.callout("Business benefit",
              "Duplicate payment and billing above the order are the two most common causes of leaked margin "
              "in purchasing. Both are blocked by the engine rather than by policy, and every override "
              "requires a permission and a written reason that is stored in the audit log.")

    # ------------------------------------------------------------------ 9
    b.h1("9.  Finance V — Expenses and Employee Claims")
    b.lead("Two distinct expense flows — money the company spends directly, and money an employee spends and "
           "claims back — each with its own approval path.")
    b.h2("9.1  The expense dashboard")
    b.p("Today's spend, items pending approval, claims awaiting reimbursement, budget against spend and the "
        "expense trend are on one screen, split between company expenses and employee claims so a finance "
        "officer can see both queues without filtering.")
    b.h2("9.2  Categories and account mapping")
    b.p("Expense categories are maintained with their ledger account mapping and a case-insensitive guard "
        "against duplicate names. Mapping at the category level is what allows an approved expense to post "
        "itself without an accountant deciding where it belongs.")
    b.h2("9.3  Company expenses")
    b.table(
        ["Stage", "What happens"],
        [["Capture", "Expense number, date, category, department, project and vendor allocation, amount, tax fields, payment method and funding account, description and receipt."],
         ["Submit", "Draft becomes pending approval."],
         ["Decide", "Approve, reject with a captured reason, or cancel."],
         ["Post", "Approval raises the payable in the ledger."],
         ["Pay", "Marking as paid clears the payable through the chosen bank or cash account and creates the payment journal."],
         ["Review", "Consolidated expense approvals screen presents every pending item across expense types in one worklist."]],
        widths=[1.8, 15.2], kind="kv")
    b.h2("9.4  Employee claims — two-level approval")
    b.p("A claim is captured with an automatic claim number, employee, date, category, project, description, "
        "amount, tax and total, and supports multiple receipt attachments in PDF and image formats. It then "
        "follows a genuine two-stage route: the employee submits, the manager approves the business case, and "
        "finance approval posts the payable to the ledger and returns the voucher number. Reimbursement pays "
        "the employee from a chosen bank or cash account with a reference and its own journal. Rejection "
        "captures a reason, cancellation is a distinct state, and an approval history records the level, "
        "action, comment, person and timestamp for every stage.")
    b.bullets([
        "Concurrent approval is detected: a second approver is told the record has already been approved or changed.",
        "A claim cannot be reimbursed twice.",
        "The system will not allow a claim to skip finance approval on the way to payment.",
    ])
    b.h2("9.5  Reporting")
    b.p("Expense reporting slices spend by category, department, project, employee and month, and the "
        "monthly and yearly reports carry the same filters. Top-category analysis sits on the dashboard so "
        "concentration is obvious.")
    b.callout("Business benefit",
              "Two-level approval with a stored history is the control auditors ask for first on travel and "
              "entertainment spend. Because approval itself posts the payable and payment clears it, the "
              "expense subledger reconciles to the general ledger by construction rather than by month-end "
              "effort.")
