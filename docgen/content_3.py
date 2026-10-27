# -*- coding: utf-8 -*-
from build_docx import HEX_NAVY, HEX_BLUE, HEX_MIST, HEX_BAND, HEX_GOLD, HEX_KHAki, GREY, NAVY, BLUE, TEAL, WHITE


def render(b):
    # ------------------------------------------------------------------ 21
    b.h1("21.  Customer Relationship Management")
    b.lead("Leads, a visual pipeline, and one of the most complete customer masters available in this class "
           "of software.")
    b.h2("21.1  Lead capture")
    b.table(
        ["What is recorded", "Detail"],
        [["Identity", "Automatic lead code, company name, contact person, email, phone and country."],
         ["Value", "Expected deal value, so pipeline is measured from the first contact."],
         ["Ownership and urgency", "Owning salesperson and a priority of low, medium, high or critical."],
         ["Source", "Website, referral, social media, trade show, cold call, advertisement or other — the basis of channel analysis."],
         ["Notes", "Free-text narrative captured at the moment of contact."],
         ["Status ladder", "New → contacted → qualified → proposal sent → negotiation → won or lost, each with its own colour."]],
        widths=[4.4, 12.6], kind="kv")
    b.p("The lead register carries four count tiles — total, new, qualified and won — searches on company, "
        "contact or email, filters by status, priority and owner, and pages fifteen at a time. Live "
        "validation prevents an incomplete or malformed record from being saved in the first place.")
    b.h2("21.2  Follow-ups")
    b.p("A follow-up register holds the date, the type of contact — call, email, meeting, messaging or demo — "
        "notes, the next follow-up date and a status of completed, pending or cancelled. The CRM home page "
        "surfaces the next six pending follow-ups with a type-specific icon, which turns the day's sales "
        "rhythm into a visible queue rather than a memory test.")
    b.h2("21.3  The deal pipeline")
    b.bullets([
        "Deals carry a six-stage pipeline: inquiry, qualified, proposal, negotiation, closed won, closed lost.",
        "Each deal holds a value, a win probability percentage (validated to a number capped at one hundred), an expected closing date, the originating lead, the customer, an owner and notes.",
        "The pipeline is presented as a board: one column per stage, each headed with a count bubble and colour-coded, ordered by expected close date.",
        "A totals strip above the board shows total pipeline value, won value and win rate.",
        "The deal detail sheet repeats the stage badge, value, probability, expected close and creation date.",
    ])
    b.h2("21.4  The customer master")
    b.p("The customer record is deliberately deeper than a contact card, because customer data drives "
        "invoicing, credit, delivery, tax and reporting. Its roughly ninety-eight attributes are organised as "
        "follows.")
    b.table(
        ["Group", "Examples"],
        [["Identity and grouping", "Customer code, legal and trade name, customer type across company, individual, partnership, sole proprietorship, government and trust, account group, segment, parent-company link for group structures, one-time-customer flag, customer-since date, lead source."],
         ["Contact and preference", "Email, phone, alternate phone, messaging number, website, professional network profile, preferred language, time zone and preferred contact method."],
         ["Address", "Structured line one and two, city, state, postal code and country, plus multiple labelled locations."],
         ["Commercial terms", "Trading currency, payment terms text and derived day count, payment method, price list, tax-inclusive flag, credit limit, credit rating, credit hold as none, manual or automatic, collection priority, interest rate, cash discount percentage and discount days, default discount, commission rate, billing cycle from per-transaction to annual, consolidated billing and a partial-payment switch."],
         ["Delivery", "Shipping condition, Incoterms and location, delivery lead time, invoice delivery channel of email, print, portal or courier, invoice email and copy list."],
         ["Banking", "Bank, account name, account number, branch and bank identifier."],
         ["Tax and registration", "GST or VAT number, primary and secondary tax identifiers, tax category, jurisdiction, state code, registration date, exemption reference and expiry, withholding rate and import-export code."],
         ["Organisation", "Industry, registration number, company size from micro to enterprise, employee count, annual revenue and year established."],
         ["Relationships", "Assigned account manager, sales representative and support representative, sales region, distribution channel, contract start and end dates."],
         ["Compliance", "Status across active, inactive, prospect, blocked and archived; a know-your-customer workflow of not started, verified or rejected with verifier and date; risk level; marketing-consent and data-processing-consent switches; internal notes."]],
        widths=[3.0, 14.0], kind="kv")
    b.p("Typeahead on segment, industry across fifteen sectors, country across eighteen markets and credit "
        "rating is drawn from values already saved, which keeps the data clean without anyone having to "
        "maintain a separate reference list.")
    b.h2("21.5  Contacts, locations, notes and files")
    b.bullets([
        "Multiple named contacts per customer with designation, email, phone and a primary flag.",
        "Multiple labelled locations typed bill-to, ship-to, remittance or other, with a default marker.",
        "Timestamped notes with the author recorded.",
        "Uploaded documents classified by type with uploader and file size.",
    ])
    b.h2("21.6  The customer 360 view")
    b.image("screenshots/08-customers.png",
            caption="Figure 8 - The customer master and 360 view: credit, limits, contacts, locations, notes and files "
                    "on one business record.")
    b.p("One page answers the four questions a relationship owner actually asks. Credit: limit, rating, "
        "available credit and a utilisation bar. Money: invoice count, outstanding, overdue, and a "
        "twelve-month chart of billed versus collected. Activity: recent invoices, open deals and open "
        "support tickets. Action: a new-invoice shortcut. Seeing support load next to revenue is what turns a "
        "renewal conversation from a guess into a judgement.")
    b.h2("21.7  The customer register")
    b.p("Filters cover customer type, status, credit-hold state and segment. Column headings sort, twenty-five "
        "rows show per page, and tiles report total, active, prospect and on-credit-hold counts. Deletion is "
        "protected: the system lists the related records that block removal, and removal is a recoverable hide "
        "rather than an erasure, so historical documents stay readable.")
    b.h2("21.8  CRM dashboards and reports")
    b.bullets([
        "Six key figures: total leads with new-this-month, active customers, active deals with created-this-month, pipeline value, won value and lead conversion rate.",
        "Four charts: leads by status, deals by stage, leads by source across the top eight, and a six-month deal trend.",
        "A pipeline summary panel with per-stage value bars in stage colours, a top active deals table, a recent leads feed and an upcoming follow-ups feed.",
        "Four quick actions: new lead, new customer, new deal, new follow-up.",
        "Standard reports: leads conversion, sales pipeline, client growth and revenue summary — each exportable to CSV or PDF, saveable with its filters, printable standalone and schedulable for delivery.",
    ])
    b.callout("Business benefit",
              "Revenue forecasting depends on data hygiene more than on methodology. A customer record that "
              "already holds currency, terms, tax registration, credit behaviour and contacts means the sales "
              "team types less, the invoice is right first time, and the pipeline figure can actually be "
              "trusted.")

    # ------------------------------------------------------------------ 22
    b.h1("22.  Sales Billing, Collections and Customer Credit")
    b.lead("Billing is available in two forms: a fast billing desk for high-volume invoicing, and the full "
           "finance receivable suite described in chapter 7. Both sit on the same customer master and the "
           "same ledger.")
    b.h2("22.1  The billing desk")
    b.p("The lighter billing screen raises an invoice with the same line mechanics as the finance suite — "
        "dynamic line grid, per-line discount and tax, header discount, subtotal, tax and grand total — and "
        "tracks paid and balance on the face of the document. It is designed for a commercial team that needs "
        "to invoice quickly without wanting the whole accounting workspace.")
    b.h2("22.2  Payment capture")
    b.table(
        ["Element", "Behaviour"],
        [["Methods", "Cash, bank transfer, instant payment, card, online wallet, cheque or online payment."],
         ["Reference", "A reference or cheque number with character and uniqueness checks."],
         ["Effect", "A part payment automatically moves the invoice to partially paid; full settlement moves it to paid."],
         ["Receiver", "Who received the money is recorded on the payment."],
         ["Ledger", "Each receipt posts through the same controlled gateway, with the bank or cash account credited or debited as appropriate."]],
        widths=[2.6, 14.4], kind="kv")
    b.h2("22.3  Credit control")
    b.bullets([
        "Credit limit, credit rating and a credit-utilisation bar are held on the customer and shown on the 360 view.",
        "A credit-hold state of none, manual or automatic travels with the record and is filterable on the register, so a blocked customer is obvious before an order is accepted.",
        "Collection priority and interest rate support a differentiated approach to slow payers.",
        "Ageing buckets and overdue flags identify who to call today.",
    ])
    b.h2("22.4  Multi-currency billing")
    b.p("Currencies, symbols, decimal precision and dated exchange rates are maintained against the company's "
        "base currency. Both the customer and the invoice carry a currency, and displayed amounts across the "
        "application convert to the viewer's chosen currency using the latest effective rate — where no rate "
        "exists, the stored figure is shown rather than a wrong conversion.")
    b.h2("22.5  Document numbering as a control")
    b.p("Invoice, credit-note and receipt numbers come from per-company sequences in the configuration "
        "console, where the prefix, padding, counter and format template can be changed. Number allocation is "
        "conflict-proof when two users save at the same moment, and moving a counter backwards raises a "
        "visible warning and writes an audit entry — the gap an auditor asks about is therefore a documented, "
        "authorised decision.")
    b.h2("22.6  Receivable dashboards and reports")
    b.bullets([
        "Billing register tiles for total, outstanding and overdue with colour-coded status chips and filters on status, customer, dates and search.",
        "Payment register tiles for total received, this month and pending balance, with method-coloured badges and search by invoice or reference.",
        "Standard reports: revenue summary, invoice ageing, profit overview and expense summary.",
        "Finance receivable dashboard: total receivables, overdue amount, average collection days, ageing chart and top outstanding customers.",
        "The executive home page rolls collected revenue this month against last month, the twelve-month revenue trend, top customers by revenue, and pending and overdue invoice counts.",
    ])
    b.callout("Coming next",
              "Sales-side documents — quotations, proposals and sales orders ahead of the invoice — automated "
              "overdue-status runs, dunning letters and reminder cycles, and a customer payment portal are "
              "scheduled in the next release (chapter 37). Invoicing, receipts, credit notes, statements, "
              "ageing and credit data are all live today.",
              fill="FFF6E5", accent=HEX_GOLD, label="ROADMAP")

    # ------------------------------------------------------------------ 23
    b.h1("23.  Projects, Tasks and Time")
    b.lead("Delivery work: a project register, milestones, a genuinely interactive task board, shared "
           "ownership, and the hours that make it all measurable.")
    b.h2("23.1  The project register")
    b.image("screenshots/05-projects.png",
            caption="Figure 9 - The project register with milestones, tasks and time tracked against every engagement.")
    b.table(
        ["Field or behaviour", "Detail"],
        [["Core record", "Unique project code, name, client, description, start and end dates, estimated hours, project manager, status and priority."],
         ["Validation", "An end date earlier than the start date is refused."],
         ["Status", "Planning, active, on hold, completed or cancelled, each with its own colour chip."],
         ["Priority", "Low through critical."],
         ["Progress", "A progress bar computed from completed tasks divided by total tasks — it moves on its own as work is finished."],
         ["On the list", "Member count and task count per project, tiles for total, active, planning and completed, search and status filter, fifteen per page."]],
        widths=[4.0, 13.0], kind="kv")
    b.h2("23.2  Milestones")
    b.p("Each project holds milestones with a name, description, due date and a status of pending, in "
        "progress, completed or cancelled, ordered by due date so the critical path is readable at a glance.")
    b.h2("23.3  Tasks")
    b.image("screenshots/06-tasks.png",
            caption="Figure 10 - The task board: table and drag-and-drop Kanban view with bucket columns and "
                    "attachment trash.")
    b.bullets([
        "Task records carry title, description, start and due dates, estimated hours, one of six statuses — to do, in progress, review, testing, completed, blocked — one of four priorities, and a manual progress percentage.",
        "Multiple people can be assigned to one task, each added or removed individually, alongside a single primary owner.",
        "Colour-labelled tags are applied inline, with duplicate tag names blocked and a colour chosen per label.",
        "A sub-task checklist sits under each task with a completed-versus-total counter, an auto-computed bar that turns green when everything is done, ordered positions and a reordering interface.",
        "Discussion comments record author and timestamp; an activity trail shows who changed which field from what to what.",
        "Cross-project views filter by project, assignee and priority with free-text search.",
    ])
    b.h2("23.4  Two working views")
    b.p("A tab switches between the table and the board. The board is a real drag-and-drop interface: "
        "dropping a card into another column saves the new status immediately without a page reload, with "
        "ghost highlighting while dragging. Overdue tasks are counted inside each column so a slippage "
        "pattern is visible per status. In the table view, rows are click-through, filters apply on change and "
        "pressing Enter in the search box runs the filter.")
    b.h2("23.5  Time and billing linkage")
    b.p("Hours are logged per employee against a project and an optional task, feeding project totals, the "
        "dashboard and the timesheet summary report. Both invoice engines can stamp a project on an invoice, "
        "so billed revenue can be traced back to delivery work and the effort behind it.")
    b.h2("23.6  Project dashboards and reports")
    b.bullets([
        "Tiles for total and active projects, total and in-progress tasks, hours logged in total and this month, and overdue projects.",
        "Charts for projects by status, tasks by status, tasks by priority and hours by project for the current month.",
        "Panels for upcoming milestones and overdue tasks, with quick actions to create a project, a task or a time entry.",
        "Standard reports: project progress, task completion and timesheet summary, all exportable and schedulable.",
    ])
    b.callout("Coming next",
              "Project budget, cost and profitability tracking, task dependencies and a Gantt view, project "
              "templates, billable rates and timesheet approval are on the release roadmap (chapter 37). "
              "Planning, execution, board management and time capture are live today.",
              fill="FFF6E5", accent=HEX_GOLD, label="ROADMAP")

    # ------------------------------------------------------------------ 24
    b.h1("24.  Service Desk, SLAs and Knowledge")
    b.lead("Support intake, agent workflow, live breach management and a knowledge base — the four things a "
           "service organisation is measured on.")
    b.h2("24.1  Raising a ticket")
    b.table(
        ["Element", "Behaviour"],
        [["Core fields", "Automatic ticket number, customer, requesting employee, category, SLA policy, subject, description, priority, source channel, assignee and due date."],
         ["Channels", "Web, email, phone or internal, recorded on the ticket for channel analysis."],
         ["Smart defaults", "Selecting a category pre-sets its default priority; selecting an SLA policy automatically computes the due date from that policy's resolution hours."],
         ["Status", "Open, in progress, waiting on client, resolved, closed or reopened — with reopening a distinct state rather than a re-open of the same status."],
         ["Priority", "Low, medium, high and critical, colour-coded throughout."]],
        widths=[3.2, 13.8], kind="kv")
    b.h2("24.2  Agent workflow")
    b.p("The first public reply on an open ticket automatically moves it to in progress and stamps the first "
        "response time; resolution and closure timestamps are held on the record. Public replies and internal "
        "notes are kept separate so a customer never sees the deliberation. Internal notes support "
        "mentioning colleagues by name, stored as a mention list and displayed inline. Attachments can be "
        "uploaded in bulk onto a reply — images, PDF, archives, text, CSV and generic files up to ten "
        "megabytes each — with size and type recorded, and served through a controlled download screen.")
    b.h2("24.3  Ownership trail")
    b.p("Every reassignment records the agent it moved from, the agent it moved to, who reassigned it and a "
        "written reason, and appears as an assignment history on the ticket. This is the record that settles "
        "“nobody was ever responsible for this”.")
    b.h2("24.4  SLA policy definition")
    b.bullets([
        "Policies hold a name, a first-response target in hours, a resolution target in hours, the priority they apply to, a description and an active flag.",
        "A policy cannot be deleted while tickets reference it, which protects historical reporting.",
        "The policy selected at intake determines the ticket's due date automatically.",
    ])
    b.h2("24.5  Live breach management")
    b.p("Breach status is not a nightly job. The ticket list recomputes breach flags for open tickets past "
        "their SLA due date every time it loads, and clears them again if the ticket recovers. A breached row "
        "is painted red with a warning icon; the ticket sheet shows the remaining SLA hours and whether the "
        "target has been blown; and the queue panel highlights tickets that have consumed eighty percent of "
        "their target, with hours elapsed against target listed, so an agent can act before the breach rather "
        "than after it.")
    b.h2("24.6  The ticket queue")
    b.image("screenshots/07-tickets.png",
            caption="Figure 11 - The service-desk queue: live breach flags, ownership trail, SLA timers and ticket "
                    "detail.")
    b.bullets([
        "Tiles for open, in progress, resolved and SLA-breached tickets.",
        "Filters on status, priority, category, assigned agent and date range, with all active filters preserved through pagination.",
        "Colour-coded status and priority badges, overdue due dates in bold red, and unassigned tickets explicitly flagged.",
    ])
    b.h2("24.7  Categories and the knowledge base")
    b.p("Ticket categories are maintained with an automatic code, description, default priority and active "
        "flag. Knowledge articles carry a title, an auto-generated unique web address, a rich body, a "
        "category, comma-separated tags and a lifecycle of draft, published or archived. Categories hold a "
        "unique name and address, a description, an icon and an active flag. Search spans title, content and "
        "tags; filters cover category and status; a view counter increments on every read; and tiles show "
        "published and draft counts.")
    b.h2("24.8  Dashboards and reports")
    b.image("screenshots/17-helpdesk-dash.png",
            caption="Figure 12 - The helpdesk workspace: open, in-progress and breached tickets, SLA timers "
                    "and queue management.")
    b.bullets([
        "Service home page with open, in-progress, resolved and breached tiles, a tickets-by-priority chart and a tickets-by-category chart.",
        "An SLA alerts panel listing tickets approaching breach with hours elapsed against target.",
        "A top support agents leaderboard for the last thirty days, showing tickets assigned and resolved per agent.",
        "Standard reports: ticket resolution with timings, SLA performance comparing target against actual with a verdict per ticket, and support workload of open and resolved counts by agent.",
        "The customer 360 view embeds open ticket count and recent tickets, so account managers see service load beside revenue.",
    ])
    b.callout("Business benefit",
              "Support commitments become measurable. Because SLA targets are applied at intake and breach is "
              "computed live, an organisation can quote a response time it can actually evidence — and the "
              "SLA performance report is the document to put in front of a client when they claim otherwise.")

    # ------------------------------------------------------------------ 25
    b.h1("25.  Multi-Company, Intercompany and Group Consolidation")
    b.lead("Several legal entities are not the same thing as one company with a filter. QASWA ERP treats "
           "entities as first-class objects with their own years, sequences, currencies, ledgers and rules.")
    b.h2("25.1  The company master")
    b.image("screenshots/12-companies.png",
            caption="Figure 7 - The multi-entity company master: companies, groups, brands and the active entity "
                    "switcher that drives every screen.")
    b.table(
        ["Group", "Attributes held"],
        [["Identity", "Code, legal and trade name, entity type across LLC, sole proprietorship, partnership, free-zone establishment, branch, subsidiary, holding, non-government organisation, government body and trust, business category and group."],
         ["Structure", "Parent and subsidiary links with ownership percentages and the consolidation method — full, proportionate, equity or none."],
         ["Accounting", "Base currency, accounting framework (IFRS, IFRS for SMEs, local GAAP, US GAAP), fiscal-year start month, year and period naming patterns and default ledger accounts."],
         ["Statutory", "Registration number, tax and VAT numbers, tax authority and office, VAT return frequency and due day, and the applicable e-invoicing regime."],
         ["Operations", "Country, time zone, languages, branch codes, bank accounts with a primary flag, warehouses and cost centres."],
         ["Status", "Active, inactive, dormant or archived."]],
        widths=[2.6, 14.4], kind="kv")
    b.p("The company list searches eight fields, filters by type, status and group, sorts, shows derived "
        "counts — users with access, subsidiaries, journals and financial years — and displays a warning "
        "banner against any company without a fiscal-year start, because such a company cannot post.")
    b.h2("25.2  Working across entities")
    b.bullets([
        "A switcher in the top bar appears as soon as two or more companies exist, showing the name, code and currency; each switch is re-validated against the user's access rights.",
        "Super administrators see every company; every other person sees only the companies they are assigned to.",
        "All data reads are restricted to the active company, with genuinely shared group-level records available where intended.",
        "The chosen company's identity, tax number, logo and address feed printed documents automatically.",
        "Financial years, voucher books and document sequences are each maintained per company; the posting engine will not borrow another entity's year and has no default-company fallback.",
    ])
    b.h2("25.3  Intercompany transactions")
    b.p("A transaction between two group companies — sale, purchase, service, expense, loan, interest or "
        "transfer — is entered once. The system then generates the mirrored transaction and the posted journal "
        "in the partner company's books automatically, and cross-links both sides through a shared root "
        "reference. One-sided balances, the defect that makes consolidation projects late, are structurally "
        "impossible.")
    b.h2("25.4  Matching and reconciliation")
    b.bullets([
        "An automatic match engine pairs entries using an amount tolerance and a date window.",
        "Match states are tracked as matched, partially matched, unmatched, exception and resolved.",
        "Partner-pair reconciliation shows company A's receivable against company B's payable with the difference and the difference as a percentage.",
        "Exceptions surface first on the dashboard with a resolve action, so the work list is ordered by problem rather than by date.",
    ])
    b.h2("25.5  Consolidation runs")
    b.table(
        ["Stage", "Gate applied"],
        [["Draft", "The run is created for a group, a period and a set of companies."],
         ["In progress", "Company data is drawn in."],
         ["Validated", "Each company must have a financial year, a balanced trial balance, closed periods, a configured exchange rate and a clean intercompany reconciliation. Failures are listed."],
         ["Approved", "Available only once validation has passed."],
         ["Posted", "Available only once approved, and a run posts exactly once."],
         ["Cancelled", "An alternative terminal state, audited."]],
        widths=[2.2, 14.8], kind="kv")
    b.p("The consolidation workspace walks the controller through validate, eliminate, statements, approve and "
        "post on one screen, with a live balance-sheet check alongside. Eliminations for intercompany "
        "receivable against payable and intercompany revenue against expense are created in the consolidation "
        "layer only — individual company ledgers are never altered — and manual reclassification and "
        "adjustment journals can be added to the same run.")
    b.h2("25.6  Currency translation")
    b.p("Each run translates at closing, average or historical rates, and the resulting foreign-currency "
        "translation adjustment is surfaced within group equity rather than buried in a residual.")
    b.h2("25.7  Group reporting")
    b.bullets([
        "Consolidated trial balance with one column per company, an eliminations column and the consolidated figure.",
        "Consolidated profit and loss and consolidated balance sheet.",
        "Elimination, ownership and non-controlling interest reports, intercompany reconciliation and exception reports, currency translation and consolidation adjustment reports.",
        "Company, group, standalone and consolidated views are available as report filters on the same statement definitions.",
        "The group dashboard shows legal entities, groups, companies in scope, group revenue, expenses and profit, intercompany gross balance, eliminations, currency adjustment and last run status.",
    ])
    b.callout("Business benefit",
              "Groups of three to twenty entities are the awkward size: too complex for manual consolidation, "
              "too small for a tier-one suite. Because the counterpart entry is created automatically and a "
              "run must validate before it can be approved, a consolidation cycle that normally takes weeks "
              "becomes a matter of clearing an exception list.")

    # ------------------------------------------------------------------ 26
    b.h1("26.  Period Close and Year-End Closing")
    b.lead("The closing process is where most accounting systems reveal their weakness. Here it is a designed "
           "workflow with a gate, a checklist, a preview and an audit trail.")
    b.h2("26.1  The closing dashboard")
    b.p("Current year, current period, periods closed against remaining, checklist progress, pending "
        "adjustments, unreconciled modules, current net profit or loss and the overall closing status appear "
        "on one screen. A controller knows the state of the close without asking anyone.")
    b.h2("26.2  Period control")
    b.bullets([
        "Monthly periods are generated from the financial year and can be closed, locked and reopened.",
        "Reopening is controlled: it refuses to proceed without a written reason and records the user, timestamp and IP address.",
        "Once closed, a period refuses journals, invoices, bills, receipts, payments, expenses, payroll postings, depreciation runs, tax postings — and even a reversal whose date would land inside it.",
    ])
    b.h2("26.3  The reconciliation gate")
    b.p("Before a month can close, a battery of tests runs. Every failure blocks the close and names the "
        "problem, the module and the required action; a period is never left partially closed.")
    b.table(
        ["Test group", "What must be true"],
        [["Journals", "No unposted or draft journals remain in the period."],
         ["Balance", "Total debits equal total credits."],
         ["Adjustments", "No pending or unposted closing adjustments remain."],
         ["Checklist", "The closing checklist is complete with zero unresolved exceptions."],
         ["Subledgers", "Bank, accounts receivable, accounts payable, tax and payroll reconciliations are attested."],
         ["Configuration", "The company has a financial year and the required ledger mappings exist."]],
        widths=[3.0, 14.0], kind="kv")
    b.h2("26.4  The closing checklist")
    b.p("The checklist is instantiated per period and per year from a template, and covers bank reconciliation "
        "completed; accounts receivable, accounts payable, tax, payroll, fixed asset and inventory "
        "reconciliations; accruals and prepayments reviewed; suspense accounts reviewed; trial balance "
        "reviewed; profit and loss and balance sheet reviewed; and management approval received. Each item can "
        "be marked pending, in progress, completed or exception, with comments and supporting attachments — so "
        "the evidence sits with the control rather than in an email.")
    b.h2("26.5  Closing adjustments")
    b.p("Accrual, prepayment, provision, correction, depreciation and tax adjustment journals are drafted "
        "inside the close, approved or rejected, and posted only through the standard gateway. There is no "
        "route into the ledger that bypasses the checks, closing or otherwise.")
    b.h2("26.6  Year-end closing")
    b.num([
        "Run the year validation: all periods closed, trial balance balanced, no unposted journals, required adjustments posted, retained-earnings and income-summary accounts configured, checklist complete, no unresolved exceptions and subledger reconciliations in order.",
        "Review the what-will-happen preview, which states the outcome before anything is written.",
        "Execute the close. The system computes net profit or loss, closes the temporary accounts into the configured retained-earnings account, writes the closing journal, carries permanent balances into the next financial year and creates that year if it does not yet exist.",
        "Verify on the opening-balance carry-forward screen that the new year's opening equals the prior year's closing, in debit and in credit.",
    ])
    b.p("The operation is repeat-safe: a closed year cannot be closed a second time and opening balances are "
        "never duplicated. Reopening the year and reversing the closing journal are both available, both "
        "audited, and neither deletes history.")
    b.h2("26.7  Closing history and reports")
    b.bullets([
        "A closing audit trail lists every period opened, closed and reopened, every validation run, checklist completion, adjustment, year closure and opening-balance generation, with person, timestamp, reason and IP address.",
        "Seven closing reports: period closing, year-end closing, closing checklist, opening balance, closing journal, unreconciled accounts and year-over-year comparison.",
        "Closing settings let the controller decide whether the checklist is mandatory before a period close, before a year close, both, or neither.",
    ])
    b.callout("Business benefit",
              "The audit question “who changed the closed month and why” has an evidenced answer. The "
              "management question “when will we have the numbers” has a schedule rather than a hope. And "
              "because reopening costs a written reason and an audit entry, the practice of quietly adjusting "
              "a closed period stops being available.",
              fill=HEX_KHAki, accent="3E6B3E", label="AUDIT")

    # ------------------------------------------------------------------ 27
    b.h1("27.  QASWA Intelligence I — Assistant, Copilot and Voice")
    b.lead("One hundred and seven AI services across more than thirty screens. This chapter covers how people "
           "talk to the system; chapter 28 covers what the system reads and does; chapter 29 covers how it is "
           "controlled.")
    b.h2("27.1  The assistant")
    b.p("A conversational assistant answers questions using your own operational data. Conversation history "
        "is retained across the thread, messages are substantial enough to paste a document into, responses "
        "stream as they are produced, and the screen opens with suggested questions so nobody stares at an "
        "empty box.")
    b.h2("27.2  The universal copilot")
    b.table(
        ["Stage", "What happens"],
        [["Understand", "The request is classified into an intent and routed to the capabilities that can answer it."],
         ["Retrieve", "Relevant ERP records and knowledge sources are pulled, within the permissions of the person asking."],
         ["Reason and act", "The answer is composed, or an action is planned for approval."],
         ["Verify", "The result is checked against the data it claims to describe."],
         ["Explain", "The answer is written in plain language with citations back to the underlying records or documents."],
         ["Offer", "A “do it for me” mode carries a suggestion straight into execution, subject to approval."]],
        widths=[2.0, 15.0], kind="kv")
    b.p("Session history and recent sessions are available, a capability list states what the copilot can do "
        "in the current context, and quick commands cover the common asks. Because it is a single box, the "
        "user does not need to know which module owns the answer.")
    b.h2("27.3  Natural-language navigation and the command centre")
    b.p("Typing “open pending requisitions” reaches the screen. The command centre maintains a registered "
        "directory of every screen in the product, filters it by the user's permissions, and matches requests "
        "on keywords and synonyms. The matching runs server-side on ordinary logic, so routine navigation "
        "costs no AI credits at all.")
    b.h2("27.4  Voice")
    b.bullets([
        "Push-to-talk input, speech-to-text transcription, spoken replies, dictation into form fields and spoken commands — each with its own switch, so an organisation can enable dictation without enabling outbound speech.",
        "Authorisation is never inherited from a voice conversation: a spoken request does not carry permissions the user does not hold.",
        "A high-risk spoken action requires explicit confirmation bound to the user, the company, the exact action and an expiry time.",
    ])
    b.h2("27.5  Proactive briefings")
    b.p("A daily briefing is generated per role — finance, procurement, inventory, management — and every "
        "figure in it is traced to actual data rather than composed. The point is that a manager starts the "
        "day with the exceptions already summarised.")
    b.h2("27.6  Intelligence events, watchlists and monitors")
    b.table(
        ["Mechanism", "Behaviour"],
        [["Detection", "Business situations are identified using rule, threshold, trend and anomaly logic. The AI writes the explanation; it does not decide the detection, which keeps the trigger deterministic and reviewable."],
         ["Events", "Duplicate events are merged, evidence is attached, statuses are tracked, and any event can be turned into a task with one action."],
         ["Watchlists", "A user follows a specific supplier, document or record and receives events about it."],
         ["Monitors", "An administrator publishes a reusable detection rule that everyone can benefit from."],
         ["Insights", "Recommendations appear proactively on the dashboard, are deduplicated, and carry helpful or not-helpful feedback, per-user preferences and ninety-day retention."]],
        widths=[2.4, 14.6], kind="kv")
    b.p("Feedback is collected across the copilot, correspondence, knowledge answers, intelligence events and "
        "observability review, which is how the quality of the answers becomes something you can report on "
        "rather than argue about.")
    b.callout("Business benefit",
              "The value is not conversation; it is that the exceptions find the person. A supplier invoice "
              "that no longer matches an order, a bid about to expire, a customer approaching a credit limit, "
              "a ticket drifting toward breach — these are detected from your data and explained in language a "
              "non-specialist can act on.")

    # ------------------------------------------------------------------ 28
    b.h1("28.  QASWA Intelligence II — Documents, Knowledge, Automation and Agents")
    b.lead("The working half of the AI layer: reading documents, answering from your own policies, and doing "
           "the routine work on a schedule.")
    b.h2("28.1  Document intelligence")
    b.table(
        ["Capability", "What it means in practice"],
        [["Registration", "Upload or link a document; it is auto-classified, checked for duplicates, tracked for expiry and retention, and related to other documents."],
         ["Extraction", "Optical character recognition turns images, PDFs and scans into structured business fields, with a confidence score and page reference for every field."],
         ["Review queue", "Low-confidence fields route automatically to a human, and every correction is recorded field by field — which is how accuracy improves rather than degrades."],
         ["Templates", "Extraction templates carry validation rules and version history; document types are configured by an administrator with changes audited."],
         ["Three-way reconciliation", "An invoice is compared against the purchase order and the goods receipt — supplier, items, quantities, prices, tax, totals and references — with discrepancies flagged and explained. It never approves a payment."],
         ["Master-data matching", "Extracted names and codes are matched to existing vendor and customer records to prevent duplicate masters."],
         ["Document questions", "Ask a question about a specific document and get an answer grounded in it."],
         ["Comparison", "Compare two quotations, invoices or contracts and see what changed."],
         ["Action proposals", "A contract can produce a draft purchase requisition; an inbound message can produce a document-aware reply."],
         ["Search", "Search by keyword, by meaning and by metadata. Restricted documents never appear in results or in AI answers."]],
        widths=[3.4, 13.6], kind="kv")
    b.h2("28.2  The knowledge base")
    b.bullets([
        "Collections are created and sources added as pasted text or as files — PDF, Word, Markdown, HTML, CSV or plain text, up to ten megabytes.",
        "Content is chunked, indexed and retrieved semantically, with a keyword fallback when meaning alone is not enough.",
        "Answers are grounded and cited. When the knowledge base does not hold the answer, the system says so rather than inventing one, and flags a conflict when two sources disagree.",
        "Versions carry effective dates and supersession, freshness is tracked, quality is scored, and a review queue supports the full lifecycle from draft to review to published to retired.",
        "Gap detection shows what staff asked that the knowledge base could not answer — the most practical way to improve documentation.",
        "AI-drafted articles go to a human who approves, edits or rejects them.",
        "Knowledge is surfaced in context: inside the record a person is looking at, on the page they are working on, and during agent execution for process-compliance lookups.",
    ])
    b.h2("28.3  Correspondence")
    b.p("Emails and letters are drafted from verified ERP facts, with the source records listed and "
        "alternative suggestions offered. Drafts can be regenerated, edited and deleted. Threads about a "
        "supplier, customer, employee, invoice or ticket can be summarised, their action items extracted, and "
        "a chronological timeline built. Inbound correspondence is classified and prioritised, a user can "
        "correct a classification, and the system detects when a message needs a follow-up. Translation "
        "between business languages protects amounts, dates and references explicitly. Templates are "
        "AI-assisted with controlled variables, versions, activation and rollback.")
    b.p("Sending is treated as a safety event: recipient validation, attachment checks, sensitive-data "
        "screening, and a hard distinction between saving a draft and sending — with an explicit confirmation "
        "before anything leaves the organisation. Batch preparation tasks and suggested outbound messages can "
        "be triggered by intelligence events.")
    b.h2("28.4  Analytics and forecasting")
    b.bullets([
        "Analysis runs only over approved data sources, and each metric has one registered definition, so the same key figure cannot be calculated two different ways. Arbitrary database queries are refused.",
        "Dimensions, role-specific metric sets, supporting evidence and an AI-written explanation accompany each result.",
        "Forecasting and what-if scenarios run on simulations only and cannot write to live data.",
        "Analyses can be saved and scheduled to recur.",
    ])
    b.h2("28.5  Process intelligence")
    b.p("The system builds end-to-end process maps for procurement and other lifecycles, detects bottlenecks, "
        "summarises cycle time against SLA and rework, compares departments with each other, and produces "
        "prioritised improvement recommendations that can be simulated before being adopted. A recommendation "
        "converts into a task or a formal change proposal. Analysis runs on an allowlist of lifecycle tables, "
        "on a schedule.")
    b.h2("28.6  Agents, skills, workflows and automations")
    b.table(
        ["Feature", "What you can do"],
        [["Agents", "Give an objective and receive a structured plan you can preview or dry-run before anything happens. Execution is step by step, with pause, resume and cancel, durable checkpoints that allow a safe restart after an interruption, and produced artefacts such as reports, drafts and summaries."],
         ["Approvals", "Each action that changes data requires an approval cryptographically bound to its exact parameters. Change one number and the approval is void."],
         ["Skills", "A named catalogue of repeatable expert procedures — raise a purchase requisition, draft a quotation, add a supplier, create a user, investigate an issue, prepare a monthly review."],
         ["Automations", "Create, edit, enable, disable and run on demand. Time-based schedules fire from a minute-level scheduler with database locking, concurrency caps, retries with backoff and failure notification. Event triggers come from a registered catalogue of business events with twenty-four-hour duplicate suppression."],
         ["Workflow studio", "A visual builder with versioning, validation and dry-run testing. Steps include reading data, AI analysis, field and threshold conditions, approval requests, task creation, notifications, and manual or event triggers."],
         ["Workspaces", "Shared team rooms with members and roles, shared conversations, findings carrying evidence and review status, research sessions with notes and summaries, pinned context, standing instructions, goals, knowledge references, an activity timeline, notifications and workspace analytics."]],
        widths=[2.4, 14.6], kind="kv")
    b.h2("28.7  Integration and administration")
    b.p("Providers and models are administered in application: add, edit and delete providers, discover and "
        "import the models each offers live, set defaults, enable or disable, and test the connection. A "
        "generic REST connector, outbound webhooks, a calendar connector and field-mapping synchronisation "
        "with preview-before-apply are provided, with credentials held in a vault and revocable, and "
        "connection health and activity logged. Procurement, finance, human resources, customer management "
        "and service are already wired into the AI layer.")
    b.callout("Business benefit",
              "Document intelligence is where the payback usually appears first: supplier invoices read and "
              "structured with confidence scores, reconciled against orders and receipts, with a human "
              "reviewing only what is uncertain. That removes the data-entry step from accounts payable and "
              "the rework step from procurement disputes.")

    # ------------------------------------------------------------------ 29
    b.h1("29.  AI Governance, Safety and Cost Control")
    b.lead("The reason an organisation can switch the AI layer on without accepting unmanaged risk.")
    b.h2("29.1  The policy engine")
    b.p("Every AI operation passes one central policy engine, applied from the screen down to the database — "
        "defence in depth rather than a single checkpoint. Risk is tiered low, medium, high and critical, and "
        "high-risk work is diverted into a human review queue rather than executed.")
    b.h2("29.2  Hard rules the assistant cannot work around")
    b.bullets([
        "Any write requires confirmation, and pending actions expire after thirty minutes with a maximum of fifty outstanding.",
        "Monetary thresholds and bulk-action ceilings trigger additional permissions and review.",
        "Approvals are bound to exact parameters; changing a value invalidates the approval.",
        "The AI is never given credentials, API keys or tokens, and tools execute server-side.",
        "Arbitrary database queries, file execution, unregistered routes and unregistered functions are refused.",
        "Prompt-injection is detected and the output of external tools is sanitised before it can influence behaviour.",
        "Data classification and masking rules are applied before content reaches a model.",
        "Financial actions, external communications, bulk operations, loops and navigation are each covered by a dedicated protective service.",
    ])
    b.h2("29.3  Cost discipline")
    b.table(
        ["Control", "Behaviour"],
        [["Pre-execution estimate", "The cost of an operation is estimated before it runs."],
         ["Provider lock", "Switching provider to evade a budget block is prevented."],
         ["Rate limits", "Per-feature limits apply, with a default of thirty requests per minute."],
         ["Usage reporting", "Consumption and cost are reported by feature and over time."],
         ["Retention", "Retention policies drive automated cleanup of stored content."]],
        widths=[3.2, 13.8], kind="kv")
    b.h2("29.4  Kill switches and emergency controls")
    b.p("Roughly forty individual switches govern workflow execution, agents, document processing, voice, "
        "knowledge retrieval, webhooks, external writes, evaluations, feedback collection and content "
        "sampling. Six one-command emergency shutdowns, including a disable-everything control, each require a "
        "reason and are audited. A named administrator can stop the AI layer in one click without stopping the "
        "business.")
    b.h2("29.5  Observability and quality")
    b.bullets([
        "Per-request traces with detail, so an answer can be reconstructed.",
        "Quality datasets and evaluation cases, regression runs, controlled experiments and benchmarks.",
        "Prompt version management with activation, so a prompt change is a release rather than an edit.",
        "Findings, anomaly and failure detection, report generation and masked content sampling.",
        "A security event log with alerting, and a management centre showing the health of every AI component, diagnostics, feature validation, switch states, cost and rate rules, masking and retention policies, usage dashboards, audit logs and retry or resolution of failed operations from one screen.",
    ])
    b.callout("Business benefit",
              "Most AI features fail to reach production because nobody can answer “what happens if it is "
              "wrong”. Here the answer is specific: risk tiers, mandatory human confirmation for writes, "
              "parameter-bound approvals, a review queue, budget checks before execution, an audited kill "
              "switch, and a trace for every response.",
              fill=HEX_KHAki, accent="3E6B3E", label="RISK")
