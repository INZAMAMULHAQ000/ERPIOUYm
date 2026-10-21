# -*- coding: utf-8 -*-
from build_docx import HEX_NAVY, HEX_BLUE, HEX_MIST, HEX_BAND, HEX_GOLD, HEX_KHAki, GREY, NAVY, BLUE, TEAL, WHITE


def render(b):
    # ------------------------------------------------------------------ 30
    b.h1("30.  Reporting, Analytics and Executive Intelligence")
    b.lead("Three distinct reporting layers: a report centre of standard business reports, a finance "
           "statement and export engine, and live analytics dashboards — plus scheduled delivery so the "
           "report comes to people instead of people going to the report.")
    b.h2("30.1  The report centre")
    b.table(
        ["Group", "Reports available"],
        [["Human resources", "Employee summary · Attendance report showing present, absent, late and attendance percentage · Leave summary"],
         ["Projects", "Project progress · Task completion · Timesheet summary"],
         ["Customer management", "Leads conversion · Sales pipeline · Client growth"],
         ["Finance", "Revenue summary · Expense summary · Profit overview · Invoice ageing"],
         ["Assets", "Asset allocation · Maintenance summary · Licence expiry"],
         ["Service desk", "Ticket resolution · SLA performance · Support workload"]],
        widths=[3.4, 13.6], kind="kv")
    b.p("Every report accepts a date range plus the filters that make sense for its subject — department, "
        "employee, project, client, status, category, priority — presents on-screen summary figures, and "
        "outputs as CSV suitable for Excel, as a PDF document, or as a print view. Each export is recorded.")
    b.h2("30.2  Saved reports and scheduled delivery")
    b.bullets([
        "A filter set can be bookmarked as a named saved report and reopened by its owner, which turns a "
        "fifteen-second configuration exercise into a single click every morning.",
        "Scheduled reports are named, typed, and set to run daily, weekly or monthly, delivered to a "
        "recipient list, with next-run dates visible and the schedule enabled or disabled at will.",
        "Scheduling is the feature that makes reporting stick: the operations review receives its own pack "
        "without anyone having to remember to generate it.",
    ])
    b.h2("30.3  Financial statements")
    b.p("The finance reporting hub presents date filters, quick-stat cards, a revenue-against-expense trend, "
        "the receivable and payable position and key ratios, with shortcuts to every statement.")
    b.bullets([
        "Trial balance.",
        "Profit and loss, by month, quarter, year or a custom range.",
        "Balance sheet.",
        "Cash flow statement, split into operating, investing and financing activity with non-cash items disclosed.",
        "General ledger report and individual account ledgers.",
        "Comparative modes: current against previous period, current against previous year, and budget against actual with variance and variance percentage.",
    ])
    b.h2("30.4  Drill-through, not re-querying")
    b.p("The reporting path is navigable in both directions. From the trial balance, clicking an account opens "
        "its ledger; clicking a transaction in that ledger opens the journal voucher behind it. From the "
        "general ledger report, clicking the voucher number or the account name reaches the same places. A "
        "challenge to a reported figure is therefore answered in three clicks, in front of the person "
        "challenging it.")
    b.h2("30.5  The export centre")
    b.p("Eleven statement sets — trial balance, profit and loss, balance sheet, cash flow, general ledger, "
        "receivable ageing, payable ageing, tax summary, asset register, budget against actual and payroll "
        "summary — publish as CSV, Excel or PDF. Every header is stamped with the company name, the report "
        "name, the generation date and the filters used, and PDF renders as landscape A4. This matters for "
        "evidence: a file can be tied back to the exact parameters that produced it.")
    b.h2("30.6  Financial ratios")
    b.p("A dedicated screen computes current ratio, quick ratio, debt-to-equity, gross margin, net margin, "
        "return on assets, return on equity, days sales outstanding and days payable outstanding. Each figure "
        "carries a benchmark and an interpretation badge — excellent collection, good return, needs "
        "improvement, extended terms — so a non-financial director can read the result without a "
        "calculator.")
    b.h2("30.7  Integrity checking")
    b.p("The integrity checker runs a full reconciliation sweep and returns a pass, warning or fail card for "
        "each area, with on-screen guidance about what to do when an issue is found. It verifies the trial "
        "balance, that assets equal liabilities plus equity, that the receivable and payable control accounts "
        "agree to their subledgers, that the tax subledger agrees to the ledger, and the fixed asset, payroll, "
        "bank and budget positions.")
    b.h2("30.8  Analytics and the executive dashboard")
    b.table(
        ["View", "Content"],
        [["Analytics workspace", "A period selector across seven, thirty, ninety or three hundred and sixty-five days, with key-figure strips and charts for human resources, projects, customer management, finance and service — revenue against expenses, department headcount, ticket status, lead sources and attendance trends — plus a chart gallery demonstrating the visualisation set."],
         ["Executive dashboard", "Year-to-date revenue, month-on-month growth, headcount and new hires, active and overdue projects, pending and overdue invoices with their value, open and critical tickets, year-to-date expenses, net profit and margin, a twelve-month revenue trend, project status, the top five clients, pending leave requests and recent system activity."],
         ["Function dashboards", "Finance, procurement, inventory, human resources, leave, service desk, projects, assets, receivables, payables, tax, budgets, closing, group, and the AI management centre — each a purpose-built work screen rather than a generic chart page."],
         ["Chart technology", "Two chart engines are wired in, both theme-aware, so visualisations follow the light or dark theme rather than breaking it."]],
        widths=[3.2, 13.8], kind="kv")
    b.h2("30.9  Report audit")
    b.p("A report audit log records which report was generated or exported, the parameters used, who ran it, "
        "when, in which format, under which file name and from which address. When a figure is later "
        "questioned, the exact version that was circulated can be reproduced.")
    b.callout("Business benefit",
              "Reporting maturity is usually the first thing a board complains about. Standard reports that "
              "arrive on a schedule, statements that drill through to vouchers, an integrity checker that "
              "reconciles the subledgers, and an export centre that stamps its own parameters together move "
              "the organisation from “send me an update” to reading a pack that already exists.")

    # ------------------------------------------------------------------ 31
    b.h1("31.  Document Design, Print and Distribution")
    b.lead("Customer-facing paper is a commercial artefact. QASWA ERP ships a design tool for it rather than "
           "a fixed layout.")
    b.h2("31.1  The template designer")
    b.bullets([
        "Drag-and-drop construction from a palette of elements: text blocks, tables, logos and images, "
        "dynamic fields, dividers, quick-response codes, barcodes, signature blocks, terms and conditions "
        "and custom HTML.",
        "Header, body and footer sections, with page size, orientation, font family and document category set "
        "per template.",
        "Live preview before publishing, duplication of an existing template as a starting point, and "
        "explicit publishing so a work-in-progress layout never reaches a real document.",
        "Module mappings decide which template renders which document, so an invoice, a statement and an "
        "asset report can each carry their own design.",
        "Full version history, meaning a layout can be compared to the version that printed last month.",
    ])
    b.h2("31.2  What the printed document carries")
    b.p("Company identity, logo and address from the company master; the customer's own tax registration; the "
        "document number from the company sequence; the issue and due dates; the line detail with tax "
        "treatment; totals in the document currency; and the terms held against the customer or the document. "
        "Print views strip navigation, so a printed invoice looks like an invoice rather than a screenshot of "
        "software.")
    b.h2("31.3  Distribution")
    b.p("Delivery channel is a property of the customer record — email, print, portal or courier — and the "
        "invoice email address and copy list flow onto the document automatically. Statements and reports are "
        "emailable on a schedule through the scheduled-report engine.")
    b.callout("Business benefit",
              "A document that carries your brand, your numbering rules and your tax registrations is not a "
              "cosmetic concern: late payment is heavily influenced by how clear and professional the "
              "invoice looks, and cross-border customers expect their own tax identifiers presented correctly.")

    # ------------------------------------------------------------------ 32
    b.h1("32.  Security, Access Control and Compliance Evidence")
    b.lead("Described for a business reader: what protects the data, who is allowed to see what, and what "
           "evidence exists when someone asks.")
    b.h2("32.1  Identity and session safety")
    b.table(
        ["Control", "What it means"],
        [["Credentials", "Passwords are held only as one-way hashes — never readable, never displayed, never exportable."],
         ["Session integrity", "A fresh session identity is issued at every sign-in, which defeats the class of attack that plants a session identifier before login."],
         ["Live account validity", "Every page re-checks the account. Delete, suspend or deactivate a person and their open session ends immediately with an explanation."],
         ["Sign-out", "Destroys the session and records the event."],
         ["Administrative reset", "Forgotten passwords are reset by an administrator, keeping access decisions inside the organisation."],
         ["Cookie protection", "Session cookies are set to be inaccessible to scripts, secure where the connection allows, and restricted in cross-site sending."]],
        widths=[3.2, 13.8], kind="kv")
    b.h2("32.2  Protection of the application itself")
    b.bullets([
        "Every create, edit and delete form carries a single-use token verified with a tamper-proof comparison, which blocks forged requests from another site.",
        "All displayed text is escaped, so stored or typed content cannot execute as code.",
        "Every database read and write uses a parameterised statement on a native driver — user input can never alter the structure of a query.",
        "Protective response headers are applied: framing restriction, no content-type sniffing, cross-site scripting filter and a strict referrer policy.",
        "Directory listing is disabled; internal configuration, helper, security, template and database folders cannot be reached from a browser; SQL, markdown, environment, log, backup and hidden files are blocked.",
        "Sixteen installation, migration and audit scripts are command-line only and denied over HTTP.",
        "In production, errors are logged rather than displayed, and a database failure presents “contact your administrator” instead of exposing detail.",
    ])
    b.h2("32.3  Roles and permissions")
    b.p("Three roles ship — super administrator, administrator and user — and unlimited custom roles can be "
        "created. A person may hold several roles. Access is decided by roughly three hundred and thirty "
        "discrete permission points spread across more than ninety areas, each covering an action rather than "
        "a screen: view, create, edit, delete, approve, post, close, reopen, reconcile, export, publish, "
        "manage sequences, manage currencies, manage lookups, manage credit, consolidate and operate the AI "
        "kill switches.")
    b.bullets([
        "Every sidebar link, page, tab, action button and export runs its own permission test.",
        "Refusals are explained rather than silent, and a user who can see but not change a record gets a read-only view.",
        "Finance alone carries about one hundred and fifty permission codes, so a cashier, an accountant, a "
        "controller and a group finance manager can each be given an exact scope.",
        "Lock-out prevention is built in: the super administrator role cannot be deleted; an administrator "
        "cannot remove their own super-administrative status or deactivate themselves; the last active super "
        "administrator cannot be demoted; and a person can only grant roles they already hold, which prevents "
        "self-promotion.",
        "Invalid or stale role selections are filtered before saving, and each user's company access is "
        "validated on every company switch.",
    ])
    b.h2("32.4  Audit evidence")
    b.table(
        ["Trail", "Records"],
        [["System audit log", "Who, what action, which module, from which address and at what time — covering sign-in and sign-out, report views and exports, settings changes, currency and rate maintenance, sequence edits, lookups, roles, permissions, widgets and directory repairs."],
         ["Approval history", "Per document: the approval level, the action, the comment, the previous state, the new state, the actor and the timestamp."],
         ["Status history", "Per document: every state transition with the person responsible."],
         ["Procurement audit", "Action, document, detail, the mandatory reason, address, user and timestamp across requisitions, quotations, orders, receipts and bills."],
         ["Closing audit", "Every period and year open, close, reopen, validation, checklist completion, adjustment and closing journal, with reason, person, timestamp and address."],
         ["Report audit", "Which report, with which parameters, run by whom, when, in which format, to which file."],
         ["AI security events", "Policy decisions, blocked operations, injection detections and emergency switch operations, with alerting."]],
        widths=[3.0, 14.0], kind="kv")
    b.p("Audit recording is designed so that a failure to write an audit entry never blocks a legitimate "
        "business transaction — control should not become an outage — and every trail is filterable by module, "
        "user, date range and free text, with CSV export.")
    b.h2("32.5  Retention and housekeeping")
    b.p("A guarded maintenance console allows an authorised administrator to clean or seed data module by "
        "module, with absolute guarantees coded in: the super administrator account and role, the permission "
        "set, the menu and singleton configuration can never be removed by it. AI content retention policies "
        "drive automatic cleanup of stored conversations and samples.")
    b.callout("Compliance position",
              "The controls an auditor typically asks for — segregation of duties, approval evidence, "
              "immutable posted records, locked periods, access reviews, change evidence and an audit trail "
              "with addresses and timestamps — are all present as system behaviour rather than as written "
              "policy. Independent assessments and penetration testing at the infrastructure layer remain your "
              "responsibility as the operating organisation, and chapter 37 lists the identity enhancements "
              "scheduled next.",
              fill=HEX_KHAki, accent="3E6B3E", label="ASSURANCE")

    # ------------------------------------------------------------------ 33
    b.h1("33.  Configuration, Master Data and Local Control")
    b.lead("The single most important operational question about any business system: can your own "
           "administrators change it without a development project?")
    b.h2("33.1  The configuration console")
    b.p("Settings are grouped as branding, finance, general and inventory, each with on-screen help, and only "
        "registered keys are accepted so a stray edit cannot create an unknown setting. Changes take effect "
        "immediately and are audited. Supplied keys include the application name, a fallback base currency, "
        "the fiscal-year start month, financial-year and accounting-period naming patterns, whether negative "
        "stock is allowed, and the date and date-time display formats.")
    b.h2("33.2  Currencies and exchange rates")
    b.bullets([
        "Twelve currencies are available in a standard installation — including US dollar, euro, pound "
        "sterling, UAE dirham, Saudi riyal, Indian rupee, Japanese yen, Chinese yuan, Malaysian ringgit and "
        "Qatari riyal — each with an International Organisation for Standardisation code, a symbol and zero to "
        "four decimal places.",
        "Currencies can be ordered, activated and deactivated, with the base currency protected from being "
        "switched off.",
        "Exchange rates are entered with an effective date, a source and an author, and the full rate history "
        "is retained — so a conversion can be reproduced as at any past date.",
    ])
    b.h2("33.3  Document numbering")
    b.p("Per company and per document type, twelve numbered document families are controlled from one screen: "
        "invoices, credit notes, receipts, journal vouchers, purchase orders, requisitions, goods receipts, "
        "vendor bills, and customer, vendor and contractor codes, plus contractor contracts. The prefix, "
        "zero-padding, current counter and a format template built from prefix, sequence, period, year, month "
        "and fiscal-year tokens are all editable. Allocation is conflict-proof under simultaneous users, "
        "numbers can be previewed without being consumed, master codes are re-checked for uniqueness and "
        "moving a counter backwards produces a visible warning and an audit entry.")
    b.h2("33.4  Editable reference lists")
    b.p("Twenty-six dropdown lists behind the forms are maintained by administrators rather than hard-coded: "
        "company and customer types, credit ratings, risk levels, know-your-customer statuses, size bands, tax "
        "categories, payment terms with the day counts that drive due dates, payment methods, billing cycles, "
        "invoice delivery channels, price lists, shipping terms, Incoterms and contact channels. Values are "
        "deactivated rather than deleted, so historical documents continue to read correctly.")
    b.h2("33.5  Other configuration surfaces")
    b.table(
        ["Surface", "What is decided here"],
        [["Voucher types", "Names, prefixes, automatic numbering and status for the more than thirty voucher books."],
         ["Tax settings", "Default tax, rate and group, inclusive or exclusive pricing, rounding rule, precision, tax document prefixes, automatic period creation and the tax account mappings."],
         ["Finance settings", "Base currency, symbol, decimal places, company tax number, account-code prefix, voucher prefix and the required general-ledger mappings for receivables, revenue, sales returns, payables, expense, expense payable, tax, bank and cash."],
         ["Inventory settings", "Negative-stock permission, default costing method, default warehouse and location, movement prefix, and whether adjustments and transfers require approval."],
         ["Procurement rules", "Approval matrix by company, department, priority and amount; over-receipt tolerance; matching tolerances; duplicate-invoice checking; sequence prefixes."],
         ["Closing settings", "Whether the checklist is mandatory before a period close and before a year close."],
         ["Asset categories", "Depreciation method, useful life, residual value and the three ledger accounts per category."],
         ["Expense categories", "Names, codes and ledger account mappings."],
         ["Service categories and SLAs", "Codes, default priorities, response and resolution targets by priority."],
         ["Lookups, roles, users, companies", "All maintained in application screens with their own permissions and audit entries."]],
        widths=[3.4, 13.6], kind="kv")
    b.callout("Business benefit",
              "Localisation without code. A new country, a new statutory tax, a rebranding of document "
              "numbers, a change of payment-term philosophy or a new approval threshold is an afternoon of "
              "administration, not a change request, a quotation and a release cycle.")

    # ------------------------------------------------------------------ 34
    b.h1("34.  Data Protection, Backup and Business Continuity")
    b.lead("How the organisation's records survive a bad day — and how you can prove they do.")
    b.h2("34.1  Backup practice")
    b.bullets([
        "Full database dumps are taken with a timestamped naming convention, and compressed copies are kept "
        "alongside them.",
        "Every backup carries a published SHA-256 checksum file, so integrity is verifiable rather than assumed.",
        "Backups are not trusted until they have been test-restored: restores are verified by comparing table "
        "counts, row-by-row counts and content hashes against the source.",
        "A generated data dictionary accompanies the backup set — currently covering four hundred and sixty-"
        "nine tables, more than six thousand columns — which means the schema is documented from the live "
        "system rather than from a stale specification.",
        "Uploaded documents live outside the database dump in managed storage, so file backup is handled as "
        "its own discipline rather than being entangled with database structure.",
    ])
    b.h2("34.2  Controlled change")
    b.p("Structural changes to the database are delivered as dated, self-checking migration scripts that "
        "inspect the current state before altering it, which makes them safe to run more than once. A "
        "migration inspector reviews what will change and a migration executor applies it with rollback "
        "tracking. All of these are restricted to the installation machine and unreachable through a browser.")
    b.h2("34.3  Health and self-repair")
    b.bullets([
        "A module health check produces a report on the state of each module.",
        "A people-identity audit runs fifteen checks enforcing the rule that one human being holds one person "
        "code across employee, customer and contractor records.",
        "Directory maintenance actions re-synchronise person codes and prune entries that have no record "
        "behind them, from the interface rather than from a script.",
        "A setup wizard installs the dashboard widget system, and a seeded demonstration data library lets a "
        "new installation be explored without loading real records first.",
    ])
    b.h2("34.4  Operating continuity")
    b.table(
        ["Concern", "Position"],
        [["Recovery point", "Defined by backup frequency; the practice above means a restore is verified rather than hopeful."],
         ["Recovery of structure", "The authoritative schema snapshot means the database can be rebuilt from empty and then migrated forward."],
         ["Recovery of documents", "Uploads are stored in a managed directory with controlled downloads, and are covered by file-system backup rather than database backup."],
         ["Protection from user error", "Soft deletes across employees, customers, companies and other masters; historical records hidden rather than erased; deletion refused where related records depend on the entry."],
         ["Protection from privileged error", "Counter regression warnings, super-administrator lock-out prevention, mandatory reasons for reopening periods, and irreversible actions gated behind specific permissions."]],
        widths=[3.2, 13.8], kind="kv")
    b.callout("Business benefit",
              "Most disputes about a business system begin with “is the data safe?”. The answer here is a "
              "checksum, a documented test restore, a version-controlled schema and a data dictionary — "
              "evidence an auditor or an insurer will accept, not a reassurance.",
              fill=HEX_KHAki, accent="3E6B3E", label="CONTINUITY")

    # ------------------------------------------------------------------ 35
    b.h1("35.  Implementation, Training and Ongoing Support")
    b.lead("A realistic view of how deployment runs, sized for an organisation adopting the full platform.")
    b.h2("35.1  Recommended sequence")
    b.table(
        ["Phase", "Focus", "Typical duration"],
        [["0 · Discovery", "Confirm the organisation structure, entities, financial years, chart of accounts, tax regimes, approval philosophy and the roles that will use the system.", "1–2 weeks"],
         ["1 · Foundation", "Install and configure companies, users, roles and permissions; set base currencies and exchange rates; define document numbering; load lookup lists; build the chart of accounts and opening balances.", "2–3 weeks"],
         ["2 · Finance live", "Journals, banking and cash, receivables and payables, expense categories and claims, tax configuration. First month-end closed inside the system.", "3–4 weeks"],
         ["3 · Procurement and stock", "Requisition and approval matrix, RFQ and evaluation model, orders and receipts, matching tolerances, vendor master, item master, opening stock and warehouse settings.", "3–4 weeks"],
         ["4 · People and assets", "Employee and contractor records with documents, departments and designations, leave types and annual balances, attendance practice, asset register with capitalisation and depreciation configuration.", "2–3 weeks"],
         ["5 · Delivery and service", "Project register, task board conventions, ticket categories and SLA policies, knowledge base seeding.", "2 weeks"],
         ["6 · Intelligence", "Provider and model configuration, document types and extraction templates, knowledge collections, governance rules, thresholds, kill-switch ownership, automations and workflow studio.", "2–3 weeks"],
         ["7 · Group", "Ownership structure and consolidation methods, intercompany discipline, first consolidation run, period and year-end closing settings.", "2–3 weeks"],
         ["8 · Stabilise", "Report scheduling, template design for customer documents, user acceptance, performance tuning, go-live decision.", "2 weeks"]],
        widths=[2.6, 11.2, 3.2], size=9)
    b.p("Phases 0 to 4 are the point at which an organisation stops running its money through a spreadsheet. "
        "The remaining phases add value without being a prerequisite for going live.")
    b.h2("35.2  Enablement")
    b.bullets([
        "Role-based training rather than feature-based training: an accounts clerk, a buyer, a warehouse "
        "supervisor, a service agent, a project manager, an HR administrator, a controller and a group "
        "administrator each need a different hour of instruction, because the interface pattern is identical "
        "everywhere.",
        "Super-administrator enablement covering roles and permissions, company and financial-year setup, "
        "document numbering, currencies and lookups, approval matrices, closing settings and the AI governance "
        "console.",
        "Written procedures for the month-end close, the three-way match exception queue, the SLA queue and "
        "the year-end close — the four recurring routines that benefit from documented practice.",
        "A sandbox installation seeded with demonstration data for training without touching live records.",
    ])
    b.h2("35.3  Support model")
    b.table(
        ["Level", "Scope"],
        [["First line (internal)", "Password resets, role and permission adjustments, lookup and reference-list maintenance — all routine administration designed for your own team."],
         ["Second line (vendor)", "Configuration questions, report definition, template design, scheduled deliveries, upgrade and migration support."],
         ["Third line (product)", "Defect resolution, health-check review, AI governance tuning, consolidation methodology and closing-process guidance."],
         ["Emergency", "AI kill switches for the intelligence layer; period locking to stop incorrect posting; the verified backup and restore route for data recovery."]],
        widths=[3.6, 13.4], kind="kv")
    b.h2("35.4  Operating requirements")
    b.p("The platform runs on standard web hosting: a current PHP application server version eight point one "
        "or later, a MySQL or MariaDB database, and the Apache rewrite module for clean web addresses. It is "
        "deliberately built without a framework or a build pipeline, which means an ordinary commercial "
        "hosting environment — including a modest on-premises server — is sufficient, and the organisation is "
        "never dependent on a specialist toolchain to run or patch the system. No third-party subscription is "
        "required for any function except the external AI models you choose to connect.")
    b.callout("Adoption risk, honestly addressed",
              "The main reason enterprise systems fail is not capability but data entry resistance. QASWA "
              "ERP's mitigation is mechanical: documents flow forward rather than being retyped (a "
              "requisition becomes a request for quotation, whose award becomes an order, whose receipt posts "
              "stock and whose bill matches against both), and journals write themselves. The clerical "
              "argument against using the system disappears once that chain is trusted.")

    # ------------------------------------------------------------------ 36
    b.h1("36.  The Business Return")
    b.lead("Where the money comes back from. These are the mechanisms in the product that produce a "
           "measurable effect on cost, cash and risk — not generic promises.")
    b.h2("36.1  Cash")
    b.table(
        ["Mechanism", "Effect"],
        [["Ageing by bucket and by invoice, with days-sales-outstanding measured", "Collections target the largest and oldest balances first rather than working alphabetically."],
         ["Customer statements and print-ready invoices with the customer's own tax registration", "Fewer disputes, fewer re-issues, faster approval of payment runs by your customer."],
         ["Credit limits, ratings and hold states on the customer record", "Order acceptance is informed by exposure before revenue is committed."],
         ["Automatic receipts allocation across open invoices", "On-account cash stops sitting unidentified and ageing quietly."],
         ["Unbilled receipts report", "Liabilities are not understated, and early-settlement discounts are not missed."]],
        widths=[5.6, 11.4], kind="kv")
    b.h2("36.2  Spend")
    b.bullets([
        "Savings measured against the requisition estimate on every sourcing event, aggregated — procurement "
        "gains a number it can report.",
        "Over-ordering, over-receipt and over-billing blocked by the engine, with overrides requiring "
        "permission and a written reason.",
        "Duplicate invoice detection per vendor, which is the single most common source of silent loss.",
        "Budget versions, revisions and transfers with utilisation monitoring against real ledger spend, so "
        "overrun is visible while it can still be corrected.",
        "Weighted bid evaluation with mandatory award reasons, which removes the relationship-driven purchase "
        "decision that audits find and boards regret.",
        "Automatic depreciation with no double-posting, disposal gain and loss computed, and impairment "
        "recorded — the asset register stops being a tax-time exercise.",
    ])
    b.h2("36.3  Time and headcount")
    b.p("The mechanisms that consume clerical hours in a typical finance and operations team are specifically "
        "addressed: journal re-keying (eliminated by automatic posting from source documents), reconciliation "
        "searching (the integrity checker and the bank difference display), report assembly (scheduled "
        "delivery and the export centre), supplier query handling (statements, match outcomes and the "
        "interaction history), and closing coordination (the checklist with its evidence attachments). A "
        "reasonable planning assumption is that the accounting function's recurring manual effort falls "
        "materially, and that the freed capacity is redeployed to review rather than removed — the control "
        "benefit comes from review, not from headcount reduction.")
    b.h2("36.4  Risk")
    b.table(
        ["Risk", "Mitigation present in the product"],
        [["Misstatement in the ledger", "Single posting gateway, balanced-entry enforcement, immutable posted vouchers, linked reversals, period locking."],
         ["Unauthorised commitment", "Requisition approval matrix with a self-approval ban, approval history, over-order and over-bill guards."],
         ["Compliance lapse", "Document-expiry colour coding for visas, passports and permits; contractor compliance panel; licence expiry alerts; tax period locking."],
         ["Late close", "Closing checklist and validation gate with named blockers; periods generated automatically from the financial year."],
         ["Data loss", "Checksummed, test-restored backups; version-controlled schema; verified row-level restore checks."],
         ["Unmanaged AI use", "Central policy engine, risk tiering, human confirmation for writes, parameter-bound approvals, budget estimation, audited kill switches."],
         ["Access sprawl", "Three hundred and thirty permission points, per-widget permissions, lock-out prevention, role-granting restricted to roles already held."]],
        widths=[3.6, 13.4], kind="kv")
    b.h2("36.5  What to measure after go-live")
    b.num([
        "Days sales outstanding, before and after.",
        "Average days to close a month.",
        "Percentage of supplier bills matching without exception.",
        "Procurement savings measured against requisition estimates.",
        "Percentage of journals posted automatically from source documents.",
        "SLA compliance rate and the count of tickets approaching breach.",
        "Manual hours spent assembling recurring reports.",
        "Value of unassigned or on-account receipts.",
    ])
    b.callout("A note on numbers",
              "This document deliberately does not quote percentage-improvement figures as though they were a "
              "specification. Every benefit above is a mechanism with a stated measurement. Adopt the eight "
              "measures in section 36.5 during phase 0 and the return becomes your own evidence rather than "
              "our assertion.",
              fill="FFF6E5", accent=HEX_GOLD, label="DISCIPLINE")

    # ------------------------------------------------------------------ 37
    b.h1("37.  Release Roadmap")
    b.lead("What arrives next, stated plainly. Everything in chapters 1 to 36 exists in the product today; "
           "this chapter is the forward commitment rather than the current scope.")
    b.h2("37.1  Finance and workforce")
    b.bullets([
        "Salary board computation: per-employee salary structures, earnings and deduction components, "
        "attendance-linked and production-linked pay, gross-to-net calculation and approval before posting.",
        "Payslip generation and distribution, and a bank disbursement file for payroll transfers.",
        "Leave encashment, automated accrual, expiry and lapse processing, enforced carry-forward, and "
        "multi-level leave approval with employee-initiated withdrawal.",
        "Employee self-service views for payslips, leave balances and attendance regularisation.",
        "Recruitment and requisition management, onboarding and exit workflows, and performance review cycles.",
    ])
    b.h2("37.2  Commercial documents")
    b.bullets([
        "Sales quotations, proposals and sales orders as first-class documents ahead of the invoice, with "
        "conversion to order and to invoice.",
        "Automated overdue-status processing, dunning letters and reminder cycles.",
        "A customer payment portal for self-service statements and settlement.",
        "Project budgeting, cost tracking and profitability, billable rates and timesheet approval.",
        "Supplier scorecards, vendor categories and segments, and supplier self-onboarding.",
    ])
    b.h2("37.3  Operations")
    b.bullets([
        "Barcode-assisted stock counting and device-based receiving.",
        "Inbound email-to-ticket conversion and auto-assignment or round-robin routing in the service desk.",
        "Canned responses, escalation matrices and ticket merging for support teams.",
        "Customer satisfaction measurement at ticket closure.",
        "Biometric or device attendance import, overtime calculation and shift management.",
    ])
    b.h2("37.4  Platform and assurance")
    b.bullets([
        "Optional two-factor authentication for sign-in and rate limiting or account lockout inside the "
        "application, in addition to the server-level protection already in place.",
        "Self-service password reset with administrative policy control.",
        "Bulk actions on high-volume registers, saved filter views and a global search across modules.",
        "A data import wizard for opening balances, item masters, customer and employee loads.",
        "Vaulted database credentials as an installation best practice, and hardened hosting documentation.",
    ])
    b.h2("37.5  Intelligence")
    b.bullets([
        "Extended evaluation dashboards and scheduled quality regression reporting for AI responses.",
        "Additional connectors for common enterprise systems and normalised field mapping.",
        "Broader voice workflow coverage and outbound telephony integration.",
    ])
    b.callout("Commitment style",
              "This roadmap exists so that no capability in this document is over-claimed. If a roadmap item "
              "is important to your decision, say so during evaluation: it can be scoped into the "
              "implementation plan explicitly rather than assumed.",
              fill="FFF6E5", accent=HEX_GOLD, label="TRANSPARENCY")

    # ------------------------------------------------------------------ 38
    b.h1("38.  Conclusion and Recommended Next Steps")
    b.lead("QASWA ERP is a complete operating platform in the area where most mid-sized organisations are "
           "least well served: enough complexity that spreadsheets have become dangerous, and not enough "
           "scale that a tier-one enterprise suite is affordable or operable.")
    b.p("Its claim rests on four properties. Financial control is enforced by the system rather than by "
        "policy documents — immutable postings, period locks, mandatory reasons, approval matrices and a "
        "single gateway into the ledger. Operational documents flow forward without re-keying, so a "
        "requisition becomes a request for quotation, an award becomes an order, a receipt posts stock and a "
        "bill is matched against both. Depth of master data — an almost hundred-field customer record and a "
        "company record carrying ownership, consolidation method and accounting framework — means the system "
        "behaves correctly without being told repeatedly. And the intelligence layer is governed: risk "
        "tiered, writes confirmed, budgets estimated before execution, kill switches owned by a named person.")
    b.h2("What to look at first in a demonstration")
    b.num([
        "Run one purchase requisition through approval, quotation, comparison, award, order, receipt, bill "
        "matching and payment — and watch the journals appear at each step without being typed.",
        "Close a period with an intentional error in it, and read the way the validation gate names the "
        "problem, the module and the required action.",
        "Open the trial balance and click down to a journal voucher, then back up to the statement.",
        "Ask the copilot a question that requires data from three modules and inspect its citations.",
        "Load a supplier invoice image and review the field-by-field extraction with its confidence scores "
        "and the resulting three-way match exceptions.",
        "Switch company, currency and theme, and observe what changes and what stays under access control.",
        "Operate an AI kill switch and confirm the business continues unaffected.",
    ])
    b.h2("Decisions this document should let you make")
    b.table(
        ["Question", "Answer supported by"],
        [["Can this replace our accounting package?", "Chapters 5 to 11 and chapter 26 — chart of accounts through year-end close, with statements and ratios."],
         ["Can it handle our group structure?", "Chapters 25 and 26 — intercompany mirroring, matching, consolidation gates and eliminations."],
         ["Will purchasing actually be controlled?", "Chapters 12 to 14 — enforced approval matrix, tolerance-based matching, over-order and over-bill guards."],
         ["Is people administration covered?", "Chapters 18 to 20, with the payroll scope stated precisely and completed in chapter 37."],
         ["Can we support customers and projects?", "Chapters 23 and 24 — task boards, milestones, time, SLA breach management and knowledge base."],
         ["Is the AI safe to enable?", "Chapters 27 to 29 — governance, review queues, cost control, kill switches and observability."],
         ["Can our own team run it?", "Chapter 33 — every list, sequence, term and rule maintained in application screens."],
         ["What is not yet there?", "Chapter 37, stated openly."]],
        widths=[4.6, 12.4], kind="kv")
    b.h2("Suggested next steps")
    b.num([
        "Share this compendium with the finance, procurement, operations and people leads, and collect the "
        "questions each chapter raises.",
        "Identify the two processes causing the most cost or delay today and request them demonstrated "
        "end-to-end with your own data shape.",
        "Agree the eight measures in section 36.5 as the evaluation baseline before go-live.",
        "Nominate the administrator who will own permissions, document numbering and the AI guardrails.",
        "Confirm which roadmap items are decision-relevant so they can be scoped rather than assumed.",
    ])
    b.p("QASWA is ready to walk any of these processes with your team, on your data, at your pace. Thank you "
        "for the opportunity to present the platform.", bold=False, italic=True)
