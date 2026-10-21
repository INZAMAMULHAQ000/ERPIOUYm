# -*- coding: utf-8 -*-
from build_docx import HEX_NAVY, HEX_BLUE, HEX_MIST, HEX_BAND, HEX_GOLD, HEX_KHAki, GREY, NAVY, BLUE, TEAL, WHITE


def render(b):
    # ---------------------------------------------------------------- A
    b.h1("Appendix A — Complete Module Index")
    b.lead("All fifty-eight business modules in the platform, in the order a new user meets them, with a "
           "plain description of what each one is for.")
    MODS = [
        ("Activity logs", "A chronological record of what people did across the system, filterable and exportable."),
        ("AI workspace", "The intelligence layer: assistant, copilot, documents, knowledge, agents, automations, governance and monitoring."),
        ("Analytics", "Cross-function dashboards with charts for people, projects, customers, finance and service over a selectable period."),
        ("Appearance", "Theme selection between the light and dark interfaces, remembered per person."),
        ("Asset assignments", "Issue assets to individuals with dates, expected return and full custody history."),
        ("Asset categories", "Define asset classes with their depreciation method, useful life and ledger accounts."),
        ("Asset returns", "Process returned assets with condition on arrival and damage notes."),
        ("Assets", "The operational fixed-asset register: identification, acquisition, condition and status."),
        ("Assets dashboard", "Totals by status and category, value, warranty and licence exposure, recent custody movements."),
        ("Attendance", "Daily marking, correction, monthly registers and status counts."),
        ("Audit logs", "The security-facing trail: who, what, which module, address and timestamp."),
        ("Authentication", "Sign-in, session issuance, live account validation and sign-out."),
        ("Companies", "The multi-entity master: identity, structure, ownership, accounting framework and statutory detail."),
        ("Contractors", "Non-employee engagement with compliance documents, contract lifecycle and rate history."),
        ("CRM dashboard", "Leads, pipeline, customers and follow-ups as a single commercial picture."),
        ("Customers", "The customer master of nearly a hundred attributes, with contacts, locations, notes and documents."),
        ("Deals", "The six-stage sales pipeline board with value, probability and expected close."),
        ("Departments", "Organisational units with codes, status and live headcount."),
        ("Designations", "Job titles tied to departments, with employee counts."),
        ("Employees", "The personnel file: personal, employment, immigration detail, documents and expiry surveillance."),
        ("Executive dashboard", "The owner's view: revenue, margin, headcount, projects, receivables, tickets and trend."),
        ("Expense categories", "Expense types with their ledger account mapping."),
        ("Expenses", "Direct company spend with approval, payment and reporting."),
        ("Finance", "The full accounting suite: ledger, banking, receivables, payables, expenses, budgets, tax, assets, payroll finance, reporting, closing and consolidation."),
        ("Helpdesk dashboard", "Ticket queues, SLA alerts, category mix and agent performance."),
        ("Holidays", "The year-by-year calendar of national, festival and optional holidays."),
        ("HRMS dashboard", "Workforce overview with headcount, attendance, leave and hiring charts."),
        ("Inventory", "The stock engine: ledger, balances, adjustments, transfers, reservations, counting and valuation."),
        ("Invoices", "The fast billing desk for raising customer invoices and recording payments."),
        ("Knowledge base", "Published articles and categories with search, versioning and a lifecycle."),
        ("Leads", "Prospect capture with source, value, priority, owner and status ladder."),
        ("Leave management", "Balance allocation and the annual entitlement grid."),
        ("Leave requests", "Application, live balance checking, approval and deduction."),
        ("Leave types", "Entitlement definitions with code, days, carry-forward and status."),
        ("Licences", "Software entitlements with seats, keys, expiry alerts and assignment."),
        ("Maintenance", "Asset upkeep records by type, cost, vendor and next due date."),
        ("Menu manager", "Administration of sidebar sections and items, each linked to a permission."),
        ("Payments", "Receipt and settlement records across customers and vendors."),
        ("People management", "The unified directory of every person, with structured onboarding and login control."),
        ("Permissions", "The individual action rights that access is granted on."),
        ("Procurement", "Requisitions, requests for quotation, comparisons, awards, orders, receipts, bills and matching."),
        ("Projects", "The project register with computed progress, members, tasks and milestones."),
        ("Projects dashboard", "Portfolio view of projects, tasks, hours, milestones and overdue work."),
        ("Reports", "The report centre: standard reports, filters, exports and saved reports."),
        ("Roles", "Named collections of permissions, with anti-lockout protection."),
        ("Scheduled reports", "Daily, weekly or monthly report delivery to recipient lists."),
        ("Settings", "The configuration console: global settings, currencies and rates, document numbering and lookup lists."),
        ("SLA policies", "Response and resolution targets by priority, with deletion protection."),
        ("System", "The administration landing page grouping users, roles, permissions and people."),
        ("Tasks", "Task lists and the drag-and-drop board, with sub-tasks, tags, assignees and discussion."),
        ("Tax settings", "Tax names, percentages and types."),
        ("Template designer", "Drag-and-drop design of printed documents with versioning and module mapping."),
        ("Ticket categories", "Service categories with codes, default priority and status."),
        ("Tickets", "The service desk queue with status, assignment, replies, internal notes and attachments."),
        ("Timesheets", "Hours logged per employee against project and task, with totals."),
        ("Users", "Accounts, role assignment, status and company access."),
        ("Vendors", "The supplier master with commercial, tax and ledger defaults, and a 360 position view."),
        ("Widgets", "The dashboard tile catalogue, sizes, permissions and layout reset."),
    ]
    rows = [[str(i + 1), n, d] for i, (n, d) in enumerate(MODS)]
    b.table(["#", "Module", "What it does for the business"], rows,
            widths=[0.7, 3.5, 12.8], size=8.6)

    # ---------------------------------------------------------------- B
    b.h1("Appendix B — Report and Statement Catalogue")
    b.lead("Every named report, statement and document the platform produces.")
    b.h2("B.1  Statutory and core financial statements")
    b.bullets([
        "Trial balance · Profit and loss · Balance sheet · Cash flow statement · General ledger report · "
        "Account ledger · Opening balances · Comparative period and comparative year statements · Budget "
        "against actual with variance.",
    ])
    b.h2("B.2  Reports by function")
    b.table(
        ["Function", "Reports"],
        [["Receivables", "AR ageing · Customer statement · Overdue invoices · Days sales outstanding · Invoice register · Revenue summary"],
         ["Payables", "AP ageing · Vendor statement · Overdue bills · Days payable outstanding · Bill register · Unbilled receipts · Match exceptions"],
         ["Expenses", "By category · By department · By project · By employee · Monthly · Yearly · Top categories · Budget against spend"],
         ["Budgets", "Budget summary · By department · By account · Utilisation · Budget against actual · Variance analysis"],
         ["Tax", "Tax summary · Output tax · Input tax · Tax period · Tax adjustments · Tax register export"],
         ["Fixed assets", "Asset register · Category summary · Depreciation schedule · Monthly depreciation · Net book value · Asset movement · Additions · Disposals · Gain and loss · Impairment"],
         ["Payroll", "Payroll summary · Payroll cost · Payroll detail · Monthly and yearly summary · Liability · Deduction · Department payroll · Employee payable · Employer contribution · Payment status · Salary expense · Payroll reconciliation"],
         ["Procurement", "Requisition register · Pending approval · Approved for sourcing · Rejected with reasons · Value by department, project and cost centre · RFQ dashboard · Quotation comparison · Award outcomes · Savings against estimate · PO register · PO dashboard · Receiving reports · Commitment and exposure"],
         ["Inventory", "Current stock · Movement ledger · Adjustment history · Transfer history · Stock valuation · Cost audit · Low and out-of-stock watchlist"],
         ["Closing", "Period closing · Year-end closing · Closing checklist · Opening balances · Closing journal · Unreconciled accounts · Year-over-year comparison"],
         ["Group", "Company trial balance · Group trial balance · Consolidated trial balance · Company and consolidated profit and loss · Company and consolidated balance sheet · Intercompany reconciliation · Intercompany exceptions · Eliminations · Ownership and non-controlling interest · Currency translation · Consolidation adjustments"],
         ["People", "Employee summary · Attendance report · Leave summary · Leave by employee, department and type · Detailed leave log · Timesheet summary · Asset allocation"],
         ["Projects", "Project progress · Task completion · Timesheet summary · Portfolio status"],
         ["CRM", "Leads conversion · Sales pipeline · Client growth · Revenue summary · Leads by source · Deal trend"],
         ["Service", "Ticket resolution · SLA performance · Support workload · Tickets by category and priority · Agent leaderboard"],
         ["Integrity", "Financial integrity check · Ratios pack · Report audit log"]],
        widths=[2.6, 14.4], kind="kv", size=9)
    b.h2("B.3  Output formats")
    b.p("On screen; print view with navigation removed; CSV suitable for Excel; and PDF via the export centre "
        "for eleven statement sets, rendered landscape A4 with the company name, report name, generation date "
        "and parameters stamped on the header. Every export writes an audit entry.")

    # ---------------------------------------------------------------- C
    b.h1("Appendix C — Controlled Documents and Numbering")
    b.lead("Every document the system issues, and how its number is formed. Prefixes, padding and counters "
           "are administrator-editable per company.")
    b.table(
        ["Document", "Purpose", "Typical number form"],
        [["Purchase requisition", "Internal request to buy", "PR-2026-000001"],
         ["Request for quotation", "Invitation to bid", "RFQ-2026-000001"],
         ["Vendor quotation", "A supplier's bid", "QUO-2026-000001"],
         ["Purchase order", "Formal commitment to a supplier", "PO-2026-000001"],
         ["Goods receipt note", "Physical receipt against an order", "GRN-2026-000001"],
         ["Vendor bill", "Supplier invoice for matching", "VB-2026-000001"],
         ["Journal voucher", "Manual or generated accounting entry", "By voucher type prefix"],
         ["Customer invoice", "Bill raised to a customer", "By company invoice sequence"],
         ["Customer receipt", "Money received from a customer", "By company receipt sequence"],
         ["Credit note", "Reduction of a customer's balance", "CN-YYYYMM-####"],
         ["Debit note", "Reduction of a supplier's balance", "By company debit sequence"],
         ["Stock movement", "Issue or receipt of inventory", "SM-2026-000001"],
         ["Stock adjustment", "Count correction with reason", "ADJ-2026-000001"],
         ["Stock transfer", "Warehouse to warehouse movement", "TRF-2026-000001"],
         ["Expense claim", "Employee reimbursement request", "Automatic claim number"],
         ["Company expense", "Direct company spend", "Automatic expense number"],
         ["Petty cash voucher", "Float issue, expense or top-up", "Automatic voucher number"],
         ["Asset code", "Unique asset identifier", "Automatically allocated"],
         ["Employee code", "Unique personnel identifier", "EMP-2026-0001"],
         ["Customer / vendor / contractor code", "Unique master identifier", "From company sequence"],
         ["Ticket number", "Service request identifier", "Automatically allocated"],
         ["Article address", "Knowledge article web name", "Auto-generated unique slug"],
         ["Category code", "Service category identifier", "CAT0001"]],
        widths=[4.4, 7.8, 4.8], size=9)
    b.p("Allocation is conflict-proof when two users save simultaneously, numbers are previewable without "
        "being consumed, and a backwards counter change warns visibly and writes an audit entry.")

    # ---------------------------------------------------------------- D
    b.h1("Appendix D — Access Model Reference")
    b.lead("How permissions are organised, with illustrative examples. There is no fixed screen count: any "
           "number of custom roles can be composed from the available rights.")
    b.h2("D.1  Illustrative role scopes")
    b.table(
        ["Role", "Typical grant"],
        [["Super administrator", "Every module, every company, every action — including sequence and configuration control. Protected against deletion and self-demotion."],
         ["Group finance manager", "All finance areas, closing, consolidation, intercompany, reports and exports across assigned companies."],
         ["Financial controller", "Ledger, budgets, tax, closing, integrity checks, period reopening, consolidated reporting."],
         ["Accountant", "Journals, receivables, payables, expenses, assets, tax register, budgets viewing, statements."],
         ["Accounts payable clerk", "Bill entry, receipts capture, matching exception review, vendor statements — no approval right."],
         ["Accounts receivable clerk", "Invoice raising, receipts allocation, statements, ageing — no credit-limit override."],
         ["Procurement officer", "Requisitions, RFQs, quotations, comparison, award recommendation, orders, receipts — no bill approval."],
         ["Approving manager", "Approval matrix rights by department and amount band; no master-data maintenance."],
         ["Warehouse supervisor", "Stock balances, receipts, adjustments, transfers, counting, low-stock watchlist."],
         ["HR administrator", "People records, attendance, leave, holidays, documents, contractors, directory maintenance."],
         ["Payroll officer", "Payroll finance: component mapping, postings, payment batches, reconciliation and reports."],
         ["Project manager", "Projects, tasks, milestones, timesheets and the projects dashboard."],
         ["Service agent", "Tickets, replies, internal notes, knowledge authoring; assignment rights limited."],
         ["Sales representative", "Leads, deals, follow-ups, customer creation within their own segment."],
         ["Auditor / reviewer", "Read and export across finance and operational registers, with the audit trail available; no create, edit or approve."],
         ["AI administrator", "Providers and models, governance rules, kill switches, observability and cost reporting."]],
        widths=[3.6, 13.4], kind="kv", size=9)
    b.h2("D.2  Action verbs used across modules")
    b.p("view · create · edit · delete · assign · approve · reject · post · cancel · close · reopen · "
        "reconcile · export · publish · manage sequences · manage currencies · manage lookups · manage credit "
        "· consolidate · operate kill switch. Each is tested independently, which is what allows segregation "
        "of duties to be real rather than nominal.")
    b.h2("D.3  Built-in safeguards")
    b.bullets([
        "A requester cannot approve their own requisition.",
        "Super-administrator role cannot be deleted.",
        "An administrator cannot remove their own super-admin status or deactivate themselves.",
        "The last active super administrator cannot be demoted.",
        "A user can only grant roles they already hold.",
        "Invalid role selections are filtered out before saving.",
        "Company access is re-validated on every switch.",
        "Every user is checked against a live account record on every page load.",
    ])

    # ---------------------------------------------------------------- E
    b.h1("Appendix E — Reference Data and Configuration Register")
    b.lead("The editable lists and switches an administrator can control without a development request.")
    b.table(
        ["Register", "Contents"],
        [["Company types", "LLC, sole proprietorship, partnership, free-zone establishment, branch, subsidiary, holding, non-government organisation, government body, trust."],
         ["Customer types", "Company, individual, partnership, sole proprietorship, government, trust."],
         ["Credit ratings", "AAA through to critical, supplied by typeahead from saved values."],
         ["Risk levels", "Graded classification carried on the customer record."],
         ["Know-your-customer status", "Not started, verified, rejected — with verifier and date."],
         ["Company size bands", "Micro through enterprise."],
         ["Tax categories", "Regular, composition, unregistered, special economic zone, export, deemed export, overseas."],
         ["Payment terms", "Text plus the day count that calculates invoice due dates."],
         ["Payment methods", "Cash, bank transfer, instant payment, card, wallet, cheque, online."],
         ["Billing cycles", "Per transaction through to annual, with consolidated billing."],
         ["Invoice delivery", "Email, print, portal, courier."],
         ["Price lists", "Named lists defaulting onto customers."],
         ["Shipping and Incoterms", "Conditions, Incoterms and locations."],
         ["Contact channels", "Recorded per customer contact."],
         ["Voucher types", "More than thirty books with prefix, auto-numbering and status."],
         ["Currencies", "Twelve in a standard installation, with symbol and decimal precision."],
         ["Exchange rates", "Dated, sourced, attributed and fully historiated."],
         ["Asset categories", "Depreciation method, useful life, residual value and three ledger accounts."],
         ["Expense categories", "Name, code and ledger mapping."],
         ["Leave types", "Code, annual entitlement, carry-forward switch and status."],
         ["Designations and departments", "Codes, descriptions, links and status."],
         ["Ticket categories", "Auto code, description, default priority, status."],
         ["SLA policies", "First-response and resolution targets by priority."],
         ["Approval matrix rules", "Company, department, priority, maximum amount, approver role, sequence, enabled."],
         ["Financial and tax settings", "Base currency, precision, prefixes, required ledger mappings, rounding rule, inclusive pricing."],
         ["Inventory settings", "Negative-stock permission, costing default, default location, adjustment and transfer approval switches."],
         ["Closing settings", "Checklist mandatory before period close and before year close."]],
        widths=[3.6, 13.4], kind="kv", size=9)

    # ---------------------------------------------------------------- F
    b.h1("Appendix F — Business Glossary")
    b.lead("Plain definitions of the terms used in this document, for readers outside finance.")
    b.table(
        ["Term", "Meaning in QASWA ERP"],
        [["Three-way match", "Comparing the purchase order, the goods receipt and the supplier bill before payment is allowed; differences become exceptions."],
         ["Tolerance", "The permitted variance — in quantity, price percentage or value — before a match is refused."],
         ["Immutable voucher", "A posted accounting entry that cannot be edited or deleted; corrected only by a linked reversal."],
         ["Reversal", "The mirror entry the system creates to cancel a posted voucher, with debits and credits swapped."],
         ["Period lock", "A closed month that refuses all postings, including reversals dated inside it."],
         ["Posting gateway", "The single controlled route by which any document writes to the general ledger."],
         ["Trial balance", "A list of every account's balance proving that total debits equal total credits."],
         ["Subledger", "A detail record — receivables, payables, tax, assets, payroll — that should agree with its control account."],
         ["Ageing", "Balances grouped by how overdue they are: current, one to thirty, thirty-one to sixty, sixty-one to ninety, over ninety days."],
         ["Days sales outstanding", "The average number of days taken to collect from customers."],
         ["Days payable outstanding", "The average number of days taken to pay suppliers."],
         ["Elimination", "Removal of intra-group revenue, expense, receivable and payable when consolidating, so a group does not book profit from trading with itself."],
         ["Non-controlling interest", "The share of a subsidiary the group does not own, shown separately in group equity."],
         ["Currency translation", "Converting a subsidiary's figures into the group currency at closing, average or historical rates."],
         ["Retained earnings", "Accumulated profit kept in the business; where the year-end close transfers the year's result."],
         ["Net book value", "An asset's cost less depreciation recorded so far, and less any impairment."],
         ["Impairment", "Writing an asset down when it is worth less than its recorded carrying value."],
         ["Capitalisation", "Recording an item as an asset with a depreciation life rather than expensing it immediately."],
         ["Weighted average cost", "A stock valuation method that blends each receipt into a new average cost."],
         ["Reservation", "Stock earmarked for a specific document so it is not promised twice."],
         ["Approval matrix", "Configured rules deciding who must approve a document, by company, department, priority and amount."],
         ["Service level agreement", "A committed response and resolution time applied to a ticket by priority."],
         ["Breach", "A ticket that has passed its SLA target; computed live in the queue."],
         ["Retrieval-augmented answer", "An AI answer built from your own documents, with citations rather than from general knowledge."],
         ["Confidence score", "How certain the system is about a field extracted from a document; low scores go to human review."],
         ["Kill switch", "An administrator control that stops a named AI capability — or everything — immediately and audibly."],
         ["Segregation of duties", "Splitting request, approval, receipt, billing and payment across different people, enforced by permission."],
         ["Soft delete", "Hiding a record rather than erasing it, so historical documents remain readable."]],
        widths=[3.2, 13.8], kind="kv", size=9)

    # ---------------------------------------------------------------- G
    b.h1("Appendix G — Evaluation Checklist")
    b.lead("Use this as the scoring sheet during selection. Each row corresponds to a chapter in this "
           "document.")
    rows = [
        ["Chart of accounts, journals, ledger and posting rules", "5", "", ""],
        ["Banking, cash, petty cash and reconciliation", "6", "", ""],
        ["Receivables, invoicing, receipts, statements, ageing", "7", "", ""],
        ["Payables, bill matching, payments, debit notes", "8", "", ""],
        ["Expenses and two-level employee claims", "9", "", ""],
        ["Budgets, versions, transfers, variance", "10", "", ""],
        ["Tax regimes, rates, groups, periods, register", "11", "", ""],
        ["Requisitions and approval matrix", "12", "", ""],
        ["RFQ, bid comparison, weighted award, savings", "13", "", ""],
        ["Orders, receipts, three-way match, returns", "14", "", ""],
        ["Vendor master and enforcement", "15", "", ""],
        ["Inventory ledger, valuation, counting", "16", "", ""],
        ["Assets, depreciation, disposal, licences", "17", "", ""],
        ["Payroll posting, batches, reconciliation", "18", "", ""],
        ["Employee records, attendance, leave, holidays", "19", "", ""],
        ["Contractors, onboarding, people directory", "20", "", ""],
        ["Leads, pipeline, customer master, 360 view", "21", "", ""],
        ["Billing, credit control, multi-currency", "22", "", ""],
        ["Projects, tasks, board, timesheets", "23", "", ""],
        ["Tickets, SLA breach management, knowledge", "24", "", ""],
        ["Multi-company, intercompany, consolidation", "25", "", ""],
        ["Period and year-end close", "26", "", ""],
        ["Assistant, copilot, navigation, voice", "27", "", ""],
        ["Documents, knowledge, agents, automations", "28", "", ""],
        ["AI governance, safety and cost control", "29", "", ""],
        ["Reporting, analytics, executive dashboard", "30", "", ""],
        ["Document design, print and distribution", "31", "", ""],
        ["Security, permissions, audit evidence", "32", "", ""],
        ["Configuration and reference data control", "33", "", ""],
        ["Backup, integrity and continuity", "34", "", ""],
    ]
    b.table(["Capability to evaluate", "Chapter", "Importance (H/M/L)", "Demonstrated (Y/N)"],
            rows, widths=[10.4, 1.7, 2.7, 2.2], size=9)

    # ---------------------------------------------------------------- H
    b.h1("Appendix H — Declaration")
    b.lead("About this document and the claims in it.")
    b.p("This compendium describes the QASWA ERP platform as presented for evaluation. Capability statements "
        "reflect the modules, screens, reports, controls and services present in the product. Items not yet "
        "delivered are collected in chapter 37 rather than mixed into the description of current "
        "functionality, so that commercial commitments can be made from an accurate baseline.")
    b.p("Figures quoted in this document — fifty-eight modules, four hundred and sixty-nine data domains, one "
        "hundred and seven AI services, more than thirty voucher books, twenty-six reference lists, twelve "
        "numbered document families, thirty-three hundred permission points, eleven exportable statement "
        "sets and nineteen standard reports in the report centre — describe the platform as configured for a "
        "full installation. A particular deployment may hold more or fewer entries in any list, because "
        "voucher books, currencies, lookup values, categories, roles and permissions are all maintainable by "
        "the operating organisation.")
    b.p("Nothing in this document constitutes a warranty of fitness for a particular business process. "
        "Process fit should be confirmed during evaluation using Appendix G, against your own documents and "
        "data. Legal, tax and statutory obligations remain the responsibility of the operating organisation "
        "and its advisers; the platform provides the controls, records and evidence that make compliance "
        "practical.")
    b.spacer(30)
    b.table(None, [["Prepared by", "QASWA Product Office"],
                   ["Document", "QASWA ERP — Product and Feature Compendium"],
                   ["Edition", "Release 2.0"],
                   ["Issued", "October 2026"],
                   ["Classification", "Commercial in confidence"],
                   ["Contact", "QASWA — available on request from your account lead"]],
            widths=[3.2, 13.8], kind="kv", zebra=True)
