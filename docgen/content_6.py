"""content_6.py — Chapter 39 (marketing playbooks & business outcomes)."""


def render(b):
    b.pb = None
    b.pagebreak()
    b.title_heading("39.  Commercial Outcomes and Evaluation Playbook")
    b.lead("This chapter translates capability into outcomes. It is the section to hand to a board, a chief "
           "financial officer or an investor who needs to understand what QASWA ERP changes in the cost and "
           "risk profile of the organisation without reading every operating chapter.")

    b.h2("39.1  What changes in the finance function")
    b.p("The single biggest change is speed of information. In most organisations the controller is working "
        "with numbers that are between one week and one month old, because reconciling the ledger to the "
        "subledgers is a project. QASWA ERP keeps them in agreement continuously. The cost of producing a "
        "month-end report falls from several person-days to the time it takes to open the screen. The cost of "
        "producing a board pack with profit, cash, receivables, payables, tax and payroll position falls from "
        "a junior accountant's week to an hour of review.")
    b.p("The second change is audit defence. When an auditor or a tax authority asks how a number was produced, "
        "the answer is a drill-through path from the statement line to the individual journal to the document "
        "that originated it, with the user, timestamp and IP address attached to every step. That evidence "
        "already exists; nobody has to remember it.")
    b.callout("Month-end at the speed of review",
              "Compounded over a financial year, a four-day close across twelve months is six working months "
              "of accounting capacity returned to the business.",
              fill="E8F1FD", accent="0F62FE", label="FINANCE OUTCOME")

    b.h2("39.2  What changes in procurement")
    b.p("Procurement stops being the department where money leaks quietly. Every request that was raised "
        "verbally and every invoice that was paid against habit becomes a line that was approved by a named "
        "person against a known budget and a known approval level.")
    b.bullets([
        ("Traceability.   ", "The chain from a raised need to a supplier payment is one continuous "
                            "timestamped record. No orphan orders, no unbilled receipts, no bills paid at "
                            "the wrong amount."),
        ("Competition.   ", "Requests for quotation reach every supplier on the approved list at the same time, "
                            "with a deadline and a common specification, so prices are genuinely comparable."),
        ("Matching.   ", "Three-way matching between order, receipt and bill catches the three common leakage "
                         "patterns: paying for undelivered goods, paying the wrong quantity and paying the "
                         "wrong price."),
        ("Control.   ", "The approval matrix bends to the organisation, not to the enterprise software, so a "
                        "sensible limit for a department does not require an implementation project."),
    ])

    b.h2("39.3  What changes for people")
    b.p("Human resources in a growing organisation is usually two jobs at once:keeping records legal and "
        "keeping people paid. QASWA ERP separates them cleanly. Records, attendance, leave and documents stay "
        "current because the forms and reminders make inconsistency harder than consistency. Payroll is "
        "calculated inside the same system that holds the leave it depends on, so the same reconciliation "
        "that challenges every other number challenges payroll too.")
    b.p("The employee experience improves in the same move. A person can see their own balances, request leave, "
        "receive a pay slip and update a document without routing through an inbox. That self-service does not "
        "remove HR judgement; it removes the transcription between the person and the record.")

    b.h2("39.4  What changes in the organisation's risk register")
    b.table(["Risk register entry", "Control added by the platform"],
            [["Duplicate supplier payment", "Three-way matching against order and receipt, approval above every limit, audit log of the approval decision."],
             ["Expense outside budget", "Budget check at posting, encumbrance visible through the requisition, monthly variance reporting."],
             ["Paying for undelivered goods", "Receipt gate before payment, quantity and price tolerance rules on every match."],
             ["Unrecorded liability at close", "Accrual journals drafted with reversals, reconciliation gate before a period can close."],
             ["Unilateral master-data change", "Role-based permissions, audit trail on every change, four-eye roles possible on all master data."],
             ["Loss of evidence", "Attributed timestamps on every submission, approval, posting and change, exportable and tamper-evident in the database."],
             ["Data loss on interruption", "Incremental backups, point-in-time recovery, documented restore rehearsal, business continuity plan."]],
            widths=[6.0, 11.0], kind="feature", size=9.5)

    b.h2("39.5  The evaluation sequence recommended to a buyer")
    b.numbered([
        "Run a scripted demonstration against your own month-end: take one real month's transactions, post them through the system, and inspect the resulting trial balance against your own.",
        "Ask your auditor to attend the period-close demonstration, since the closing logic is the part auditors care about most and it is the hardest to fake.",
        "Compare your own chart of accounts against the import tool and time how long migration takes.",
        "Run a procurement scenario from requisition through to payment, including a deliberate price variance, and watch it be caught at matching.",
        "Ask for the data ownership terms in writing and test the export.",
        "Visit a live installation and speak to the controller there, off the script.",
    ])
    b.callout("A defensible decision",
              "An evaluation that measures these six things independently of the vendor's own slides will deliver a "
              "decision that the finance director can defend internally.",
              fill="FFF6E5", accent="B27A00", label="EVALUATION")
    b.p("The attached evaluation checklist (Appendix G) converts these points into thirty lines you can score on "
        "a five-point scale across competitors, so the comparison is recorded rather than argued at the end.", size=10.5)


    b.h2("39.6  Common objections, answered directly")
    b.bullets([
        ("It looks like accounting complexity dressed up.   ",
         "The interface is an IBM Carbon presentation of fairly standard controls, which is exactly why it is "
         "auditable: no clever behaviour, no hidden logic. Complexity lives in the data model, where auditors "
         "expect it."),
        ("We already own an accounting package.   ",
         "Most organisations do. The question is whether the GL agrees with the subledgers, whether the close "
         "is continuous, and whether procurement, HR and service answer to the same numbers. QASWA ERP is not "
         "a replacement of a GL; it is the reconciliation engine the existing stack never had."),
        ("Our data is messy.   ",
         "Migration is then the purpose, not the blocker. The import toolkit accepts partial data, flags gaps, "
         "and lets departments correct their own owners. A six-week migration with visible progress is normal."),
        ("Leadership wants a single vendor head.   ",
         "No professional services engagement is required to run the platform; the standard hosting arrangement "
         "and the documentation let an internal team operate it, and external support is available by the "
         "hour."),
        ("We are not ready for AI.   ",
         "Everything works without it. AI is an optional, policy-governed layer that produces drafts and "
         "suggestions a human approves, and it can be left switched off without disabling anything else."),
        ("Security and data sovereignty.   ",
         "The platform runs on the customer's own hosting, stores data in a MySQL database the customer "
         "controls, and exposes a documented structure. Nothing is held in a proprietary cloud and no "
         "subscription is required to reach the database."),
    ])

    b.h2("39.7  The first ninety days on the platform")
    b.numbered([
        "Week one: create the company, the ownership tree, currencies, document sequences and the chart of "
        "accounts. Import the opening balances from the previous system.",
        "Week two: load people, departments and designations; record the leave balances and opening attendance; "
        "configure the holiday calendar and leave types.",
        "Week three: load items, warehouses and current stock; set the reorder levels and supplier catalogue; "
        "raise the first test requisitions and purchase orders through to payment.",
        "Week four: switch live procurement on, issue the first customer invoices, and run the month-end close "
        "script. Capture what went well and what needs adjustment.",
        "Weeks five to eight: add budgets and tax registers, define SLAs and ticket categories, load the "
        "project portfolio and timesheets, and build the first scheduled reports.",
        "Weeks nine to twelve: turn on the approval matrix, the consolidation and multi-company flows, the AI "
        "draft tasks and the exportable board pack. Run the first quarterly close and hand it to the auditor.",
    ])
    b.callout("Adoption that compounds",
              "Most organisations are fluent in the routines by the end of the first quarter and run the second "
              "quarter close better than the first.",
              fill="E8F1FD", accent="0F62FE", label="ADOPTION")


    b.h2("39.8  Summary: cost, effort and timeline")
    b.p("A typical mid-sized deployment of QASWA ERP runs from initial agreement to a live month-end in twelve "
        "to sixteen weeks, spread over a project team of less than half a person each from finance, "
        "procurement, HR and IT. The pattern of effort is front-loaded into configuration and data load, and "
        "falls sharply once the first module is live, because the second module reuses the same security, "
        "numbering, currency and audit infrastructure. The annual recurring cost is a hosting footprint of "
        "modest size, since the stack is PHP and MySQL on standard web hosting, and the support burden is "
        "spent on the business rather than on the platform's internals. The payback is not a future-state "
        "diagram: it is the first month in which the close is run in days not weeks, the first quarter in "
        "which a duplicate payment does not occur, and the first audit in which every figure is "
        "traceable without preparation.")

