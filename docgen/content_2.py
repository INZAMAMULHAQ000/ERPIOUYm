# -*- coding: utf-8 -*-
from build_docx import HEX_NAVY, HEX_BLUE, HEX_MIST, HEX_BAND, HEX_GOLD, HEX_KHAki, GREY, NAVY, BLUE, TEAL, WHITE


def render(b):
    # ------------------------------------------------------------------ 10
    b.h1("10.  Finance VI — Budget Control, Versions and Variance")
    b.lead("Budgets in QASWA ERP are live objects with a lifecycle, not a spreadsheet column that is "
           "compared to actuals by hand each month.")
    b.h2("10.1  Building a budget")
    b.table(
        ["Choice", "Options and controls"],
        [["Period basis", "Annual, quarterly or monthly budgets."],
         ["Construction basis", "By department, by project or by account — or any combination of the three on one budget."],
         ["Line grid", "Each line carries department, project, account, period and amount. A duplicate line for the same department, project, account and month is detected and refused."],
         ["Monthly allocation matrix", "A dedicated grid screen spreads an amount across the twelve months, so seasonality is entered as a shape rather than twelve separate records."],
         ["Naming", "Budget names must be unique within their year."],
         ["Lifecycle", "Create → submit → approve → activate → close, with deletion permitted only on drafts."]],
        widths=[3.6, 13.4], kind="kv")
    b.h2("10.2  Versions, revisions and transfers")
    b.bullets([
        ("Versions.", "Several scenarios can exist against the same year — a base plan, a stretch case, a "
         "constrained case — with exactly one activated at a time, so reporting always knows which plan is real."),
        ("Revisions.", "An approved budget can be increased, decreased or adjusted against specific lines. "
         "Each revision records what changed and produces a version history, so the movement from original "
         "plan to current plan is a documented trail rather than a new file."),
        ("Transfers.", "Funds move from one budget line to another with a stated reason and an approve or "
         "reject decision. Transfers cannot create money: the source line reduces by exactly what the "
         "destination line gains."),
    ])
    b.h2("10.3  Monitoring and variance")
    b.p("Budget monitoring compares each budget line to the actual spend recorded in the general ledger. "
        "The comparison can be refreshed on demand and snapshotted so a controller can show what the "
        "position looked like on a particular date. Variance analysis is available by account, by "
        "department and by project, showing the variance amount and utilisation percentage, and the budget "
        "dashboard summarises total budget, actual spent, utilisation and alert count.")
    b.h2("10.4  Budget reports")
    b.bullets([
        "Budget summary across the whole plan.",
        "Budget by department, showing allocation against actual.",
        "Budget by account, for cost-line control.",
        "Utilisation report, ranking the lines closest to or past their limit.",
        "Budget versus actual, and variance analysis, both available through the finance report hub and exportable.",
    ])
    b.p("Because budgets are checked against real ledger postings, a department cannot spend itself over "
        "approval limits unnoticed — the utilisation figure moves the moment the expense posts.")
    b.callout("Business benefit",
              "Budget overrun becomes a same-day conversation instead of a quarter-end discovery. Versioning "
              "means a revised plan can be produced in an afternoon without losing the original number that "
              "the board approved.")

    # ------------------------------------------------------------------ 11
    b.h1("11.  Finance VII — Tax Management")
    b.lead("A configurable indirect-tax engine: regimes, rates, groups, registrations, exemptions, "
           "periods, the register itself, adjustments and reporting.")
    b.h2("11.1  Regimes and rates")
    b.p("Tax regimes for VAT, GST, sales tax and withholding are defined as named tax types with an output "
        "or input direction, a default flag and effective dates. Rates carry their own effective date "
        "ranges, so a change in the statutory rate is a dated record rather than a backdated edit that "
        "silently changes historical documents.")
    b.h2("11.2  Tax groups")
    b.p("Several rates can be stacked onto a single transaction line through a tax group in priority order — "
        "for example output VAT at five percent together with withholding at three percent. Groups are "
        "reusable across sales and purchase documents and are selected per line.")
    b.h2("11.3  Registrations and exemptions")
    b.bullets([
        "Tax registrations are maintained per jurisdiction and country, which is what allows a multi-entity group to file correctly in each territory.",
        "Exemptions are recorded with a code, a reason, an amount and a validity period, and an exemption reference can be cited on an individual invoice or bill line.",
        "Customer and company records carry withholding rates, tax category (regular, composition, unregistered, special economic zone, export, deemed export, overseas), exemption references and VAT return frequency.",
    ])
    b.h2("11.4  Tax periods and the register")
    b.table(
        ["Function", "Behaviour"],
        [["Period lifecycle", "Create → submit → close. Periods can be created manually or, when automatic creation is enabled, opened on the first posting of a new month."],
         ["Locking", "Closing a period locks the tax register: ordinary transactions for that month are refused with a message directing the user to raise an adjustment or a reversal."],
         ["Register", "One searchable list of output, input and adjustment postings, filterable by date, type, direction and status, with a detail view on each line."],
         ["Export", "The register exports to CSV for submission to an accountant or portal."],
         ["Adjustments", "An adjustment is raised, approved or rejected with a full audit trail; an approved adjustment posts its own voucher."],
         ["Settings", "Default type, rate and group; tax-inclusive or tax-exclusive pricing; rounding rule from five methods; decimal precision; tax invoice and tax credit note prefixes; automatic period switch; and the output-tax, input-tax and clearing account mappings."],
         ["Dashboard", "Open filing periods, output against input tax across six months, register breakdown, recent tax transactions, and an explicit warning when a ledger mapping is missing."]],
        widths=[2.4, 14.6], kind="kv")
    b.h2("11.5  Tax reporting")
    b.p("Five tax reports are provided — summary, output tax, input tax, period and adjustments — alongside "
        "the register export. Because every tax posting originates from an approved source document, the "
        "return figures can be drilled back to the invoice or bill that produced them.")
    b.callout("Business benefit",
              "Indirect-tax exposure is visible continuously rather than at filing. Rate changes take effect "
              "on a date instead of corrupting history, closed periods refuse edits, and adjustments are the "
              "only route into a locked month — with an approval and a reason attached.",
              fill="FFF6E5", accent=HEX_GOLD, label="COMPLIANCE")

    # ------------------------------------------------------------------ 12
    b.h1("12.  Procurement I — Requisition and Approval")
    b.lead("The purchasing chain begins with a controlled internal request, not an email to a buyer.")
    b.h2("12.1  The purchase requisition")
    b.table(
        ["Section", "What is captured"],
        [["Header", "Number from the yearly requisition sequence with an editable prefix; company, department, branch, project and cost centre; requester, request date and need-by date; purpose statement; currency; priority from Low to Urgent."],
         ["Lines", "Each line is typed Stock, Non-stock, Service, Asset or Expense, and carries quantity, unit, estimated price, discount, tax percentage, its own need-by date, a preferred vendor, and its own department, project and cost centre."],
         ["Totals", "Recalculated by the server on every change; browser-side arithmetic is never used as the authoritative figure."],
         ["Attachments", "Supporting documents can be attached to the requisition."]],
        widths=[2.4, 14.6], kind="kv")
    b.h2("12.2  States and editability")
    b.p("Draft, submitted, pending approval, approved, rejected, cancelled and closed. Only drafts and "
        "rejected requisitions can be edited, which prevents a document being quietly changed while it is "
        "sitting in someone's approval queue. A rejected requisition can be corrected and resubmitted rather "
        "than restarted.")
    b.h2("12.3  The approval matrix")
    b.p("Approval rules are configured by administrators and matched on company, department, priority and a "
        "maximum amount. Matching rules run in sequence and every matching rule must approve before the "
        "document is approved; each rule points at an approver role rather than an individual, so a change of "
        "post-holder does not require a rule change. Rules can be enabled or disabled without deleting them, "
        "and if no rule matches, any holder of the approval right may act.")
    b.bullets([
        "A requester can never approve their own requisition — enforced by the engine, not by the rule set.",
        "Rejection and cancellation both require a written reason, which is retained with the document.",
        "Every approval action writes to a per-document approval history showing the actor, the comment, the previous state and the new state, plus a procurement audit entry carrying the IP address and timestamp.",
    ])
    b.h2("12.4  Visibility before commitment")
    b.p("The procurement command centre shows requisition value trend, status mix, spend by department, the "
        "open pipeline, outstanding requisitions by priority, current approval queues and the most requested "
        "items. A buyer therefore sees total demand — and can consolidate it — before committing anything.")
    b.h2("12.5  Requisition reporting")
    b.bullets([
        "Requisition register with full filtering.",
        "Pending approval, for chasing approvers.",
        "Approved and ready to source.",
        "Rejected with reasons, to identify recurring blockages.",
        "Committed value by department, project and cost centre.",
    ])
    b.callout("Business benefit",
              "Unauthorised purchasing is closed off at the start of the chain. Because a requisition line "
              "carries its own project and cost centre, spend is attributed correctly from the moment it is "
              "requested — which is the data a project or department margin report depends on.")

    # ------------------------------------------------------------------ 13
    b.h1("13.  Procurement II — Sourcing, Quotation and Award")
    b.lead("The competitive part of purchasing: inviting suppliers, capturing bids, comparing them on a "
           "weighted basis and awarding with a documented reason.")
    b.h2("13.1  Creating the request for quotation")
    b.p("Only an approved requisition can become a request for quotation, and its lines carry across "
        "automatically — nothing is retyped. The RFQ carries a number from its own sequence and moves through "
        "draft, open, sent, partially responded, fully responded, evaluation, awarded, cancelled and closed. "
        "Invitations can only be issued to active vendors; an inactive vendor is skipped with a stated reason. "
        "Each send writes a per-vendor communication record: method, recipient, status, sender and date.")
    b.h2("13.2  Deadline discipline")
    b.bullets([
        "A response deadline and a quote-validity date are tracked per invitation.",
        "Stale invitations expire automatically rather than lingering on a buyer's screen.",
        "RFQs more than thirty days overdue close themselves, so the pipeline reflects reality.",
    ])
    b.h2("13.3  Capturing vendor quotations")
    b.p("Each supplier submits its own quotation document with a number of its own. The system supports "
        "partial quoting against the RFQ, alternative or substitute lines, other charges such as freight and "
        "handling, Incoterms, warranty terms, the vendor's reference, lead time, validity date, per-line "
        "delivery days and warranty months. Quotations move draft → received → under evaluation → shortlisted "
        "→ rejected, selected or expired.")
    b.h2("13.4  Comparison and weighted evaluation")
    b.table(
        ["Mechanism", "How it works"],
        [["Line-by-line grid", "Every vendor is compared against the same RFQ line, with a grand-total row across the quotation."],
         ["Evaluation criteria", "Named criteria with weights that must sum to exactly one hundred percent, scored nought to ten."],
         ["Automatic ranking", "Weighted score is calculated by the system; ties break on the lower price."],
         ["Savings measurement", "Saving against the requisition estimate is computed per RFQ and summed, so sourcing value is measured rather than claimed."],
         ["Award", "Award the whole RFQ to one supplier, or split the award line by line across suppliers."],
         ["Override control", "Selecting a vendor that did not rank first forces an override reason, and an award reason is always mandatory."]],
        widths=[3.4, 13.6], kind="kv")
    b.h2("13.5  Quote dashboard")
    b.p("Open RFQs, responses pending, quotations received, evaluations in progress, awards awaiting "
        "selection, expired items, estimated value and measured savings are presented as count tiles, each "
        "linking into the filtered list. Vendor quote-versus-win performance is reported on the same screen "
        "and on the procurement command centre, which is the beginning of supplier performance management.")
    b.callout("Business benefit",
              "The two failure modes in sourcing — awarding to a friend and losing the rationale for an award "
              "— are both closed. The weighted grid makes the cheapest compliant answer obvious, the mandatory "
              "reason and override note make the decision defensible, and the savings calculation turns "
              "procurement into a function that can show a number.")

    # ------------------------------------------------------------------ 14
    b.h1("14.  Procurement III — Orders, Receipts, Matching and Returns")
    b.lead("Commitment, delivery and settlement: purchase orders with formal amendment, receipts with "
           "inspection, three-way matching, and the debit note that corrects it.")
    b.h2("14.1  Purchase orders")
    b.image("screenshots/03-procurement.png",
            caption="Figure 3 - The procurement workspace: requisitions, sourcing, orders, receipts, matching and returns "
                    "in one connected chain.")
    b.p("A purchase order is created from the award and retains the complete requisition → RFQ → quotation → "
        "award → order chain on every line, which is what makes the document self-explaining years later. "
        "The header carries buyer, requester, payment and delivery terms, delivery location, Incoterms, "
        "warranty terms, shipping method, special instructions, separate vendor-facing and internal notes, "
        "and its own other charges. States run draft, pending approval, approved, rejected, sent, "
        "acknowledged, partially received, fully received, partially billed, fully billed, closed and cancelled.")
    b.bullets([
        ("Over-order guard.", "Ordered quantity cannot exceed the awarded quantity."),
        ("Formal revisioning.", "An amendment requires a reason, receives a revision number, snapshots the previous lines and produces an automatic before-and-after change list; the document returns to draft for re-approval."),
        ("Acknowledgement.", "Sending the order and the vendor's acknowledgement — their reference, confirmed date and comments — are both logged."),
        ("Commitment tracking.", "Reports show committed, cancelled and remaining value so exposure is measurable before goods arrive."),
    ])
    b.h2("14.2  Goods and service receipt")
    b.table(
        ["Feature", "Detail"],
        [["Receipt basis", "Receiving is allowed only against an order that is approved, sent, acknowledged or partially received."],
         ["Per-line arithmetic", "Ordered, previously received, remaining, received, accepted, rejected, damaged, short and backorder quantities are all tracked."],
         ["Integrity rule", "Accepted, rejected and damaged quantities can never exceed the quantity actually received."],
         ["Tolerance", "An over-receipt tolerance percentage is configurable, so a genuine delivery variance does not stall the warehouse."],
         ["Line detail", "Batch number, serial number, expiry and manufacturing date, warehouse, bin location, and rejection or damage reason and type."],
         ["Inspection", "A workflow of pending, passed, partially passed, failed or not required, recording the inspector, quantities, comments and supporting documents."],
         ["Automatic effects", "Finalising updates the order's received quantities, moves the order to partially or fully received, maintains a per-line receiving summary with remaining, outstanding and last-receipt dates, and posts accepted stock lines into the inventory ledger — repeat-proof, so a double save cannot double the stock."],
         ["Liability position", "A receipt records a physical event only. It never creates a supplier liability; that happens on the bill."],
         ["Returns", "Rejections and returns are recorded on their own screen with reason, inspection result and evidence."]],
        widths=[3.0, 14.0], kind="kv")
    b.h2("14.3  Three-way matching")
    b.p("The match engine compares the order, the receipt and the bill line by line using quantity "
        "tolerance, price percentage tolerance and total-value tolerance — a five percent default that can be "
        "edited per bill. The output states matched or exception, gives the variance amount and percentage, "
        "and reports the quantity and price status per line. Exceptions are itemised by type: quantity "
        "mismatch, price mismatch, missing receipt, or overall variance, each with the required action. An "
        "exception can be overridden by someone holding the permission, with a reason, or rejected; every "
        "outcome is stored.")
    b.h2("14.4  Returns, debit notes and the closing of the loop")
    b.p("Where goods are returned or the supplier has overcharged, a debit note is raised against the bill "
        "and the payable and input tax are reversed with their own journal. Payment allocation then settles "
        "what genuinely remains owed, and the vendor statement reflects the corrected position.")
    b.h2("14.5  Procurement reporting")
    b.bullets([
        "Order register with total, approved, pending and open-value tiles.",
        "Receipt reports by date, status and order showing received against accepted, rejected and damaged.",
        "Unbilled receipts — the classic source of understated liabilities.",
        "Matching exceptions, presented as a work queue.",
        "Supplier bill register, statements and accounts-payable ageing.",
        "Outstanding procurement value across orders and receipts.",
    ])
    b.callout("Business benefit",
              "Three-way matching is where purchasing leakage is normally found and normally tolerated. "
              "Making it automatic converts it into an exception queue with named owners: the only bills that "
              "reach the ledger are the ones that reconcile to what was ordered and what actually arrived.")

    # ------------------------------------------------------------------ 15
    b.h1("15.  Vendor and Supplier Management")
    b.lead("The supplier record is the control point for the whole purchasing chain.")
    b.h2("15.1  The vendor master")
    b.table(
        ["Attribute group", "Included"],
        [["Identity", "Unique vendor code, legal name, contact person, email, phone, address, website, notes, active or inactive."],
         ["Commercial", "Payment terms, trading currency, default expense account and default payable account."],
         ["Tax", "VAT or tax number with length validation, and tax category carried on the record."],
         ["Position", "Total billed, total paid, outstanding and overdue value, order count, recent bills, recent payments and recent orders."]],
        widths=[3.2, 13.8], kind="kv")
    b.h2("15.2  Search, filters and summary tiles")
    b.p("The register searches across name, code, email and contact person, filters by status, pages the "
        "result, and shows tiles for total vendors, active vendors and outstanding value. The vendor profile "
        "is the 360 view described above.")
    b.h2("15.3  Enforcement through the chain")
    b.bullets([
        "An inactive vendor cannot be nominated on a requisition.",
        "An inactive vendor cannot be invited to a quotation request.",
        "An inactive vendor cannot be issued a purchase order.",
        "An inactive vendor cannot receive a goods receipt or raise a bill.",
        "Quote-versus-win performance is reported from real bid data rather than an opinion.",
    ])
    b.h2("15.4  Interaction history")
    b.p("Every RFQ invitation with its method, recipient and status, and every purchase order transmission "
        "with the vendor's acknowledgement, sits against the supplier relationship. That record is the "
        "evidence base when a commercial conversation goes badly.")
    b.callout("Coming next",
              "Formal supplier scorecards, vendor categories and segments, bank-account detail capture, a "
              "blacklist flag and supplier self-onboarding are scheduled for the next release — see chapter "
              "37. Everything listed above is available now.",
              fill="FFF6E5", accent=HEX_GOLD, label="ROADMAP")

    # ------------------------------------------------------------------ 16
    b.h1("16.  Inventory and Warehouse Control")
    b.lead("A single, controlled stock engine. Every quantity change in the organisation passes through it, "
           "which is what makes the stock figure trustworthy.")
    b.h2("16.1  The item master")
    b.p("Items carry a code, name, category, default warehouse and location, unit of measure, costing "
        "method (FIFO, LIFO, weighted average, standard or moving average), reorder point, minimum quantity, "
        "unit price, default vendor, flags for batch-controlled and serial-controlled items, and an active "
        "status.")
    b.h2("16.2  The stock ledger")
    b.p("Stock movement is written as immutable ledger rows: purchase receipt, sales issue, adjustment in and "
        "out, transfer in and out, opening stock and reversal. Each row carries company, item, warehouse, bin, "
        "batch, serial, quantity in and out, unit cost, value, before-and-after cost and value, the source "
        "document reference and a status. Negative stock is blocked unless deliberately switched on. Moving "
        "average cost recalculates on every receipt, and when inventory, cost of goods sold and adjustment "
        "accounts are configured, movements post to the general ledger automatically.")
    b.h2("16.3  Balances, reservations and movements")
    b.table(
        ["Capability", "What it does for you"],
        [["Multi-warehouse balances", "On-hand, reserved, available, average cost and stock value per item, warehouse and bin."],
         ["Opening stock", "Captured once at go-live and dated, so the ledger starts from a provable position."],
         ["Adjustments", "System quantity against counted quantity with variance and value, a mandatory reason, attachments and an optional approval gate before posting."],
         ["Transfers", "Warehouse to warehouse as a single atomic movement that posts the out and the in together, with its own approval switch."],
         ["Reservations", "Stock reserved against a document, then released, cancelled, or consumed — consumption converts the reservation into an issue."],
         ["Physical count", "Load ledger balances, enter counted quantities, see the discrepancy quantity and value automatically, and let completion generate the gain and loss adjustments."],
         ["Numbering", "Stock movements, adjustments and transfers each draw from their own document sequence."],
         ["Settings", "Allow negative stock, default costing method, default warehouse and location, movement prefix, require adjustment approval, require transfer approval."]],
        widths=[3.4, 13.6], kind="kv")
    b.h2("16.4  The inventory command centre")
    b.image("screenshots/04-inventory.png",
            caption="Figure 4 - The inventory command centre: balances, reservations, movements and stock risk "
                    "visualised at a glance.")
    b.bullets([
        "Stock value, active items, and on-hand, reserved and available totals.",
        "Pending approvals, so a stalled adjustment does not quietly misstate stock.",
        "Six-month movement value trend and a ninety-day movement mix.",
        "Stock value by warehouse and a workflow status funnel.",
        "Top items by value and recent movements.",
        "A low and out-of-stock watchlist of items at or below their minimum — the working list for replenishment.",
    ])
    b.h2("16.5  Inventory reporting")
    b.p("Current stock, the full movement ledger with seven filters, adjustment history, transfer history, a "
        "valuation report with a grand total, and a cost audit that shows the valuation history behind every "
        "movement. Fast lookups return stock and location figures as the user types.")
    b.callout("Business benefit",
              "Because the ledger is immutable and repeat-proof, stock accuracy becomes a counting problem "
              "rather than a record-keeping problem. The cost audit answers the question finance always asks "
              "at valuation: not what the stock is worth now, but how it came to be worth that.")

    # ------------------------------------------------------------------ 17
    b.h1("17.  Fixed Assets, Licences and Infrastructure")
    b.lead("Two layers on one asset record: the operational register that tells you who has what and what "
           "condition it is in, and the accounting layer that depreciates, impairs and disposes of it.")
    b.h2("17.1  The operational register")
    b.table(
        ["Detail", "Captured"],
        [["Identification", "Automatically unique asset code, name, category, unique serial number with duplicate rejection, brand and model."],
         ["Acquisition", "Purchase date, cost, purchasing vendor, warranty expiry with a counter for warranties expiring within thirty days."],
         ["Condition", "New, good, fair or damaged."],
         ["Status", "Available, assigned, in maintenance, damaged, lost or retired."],
         ["Notes", "Free text with a full change history."]],
        widths=[3.0, 14.0], kind="kv")
    b.h2("17.2  Custody, movement and upkeep")
    b.bullets([
        ("Assignment.", "Issue an asset to an employee with an assigned date, expected return date and notes; the complete assignment history stays on the asset."),
        ("Return.", "Process returns with a return date, condition on arrival and damage notes."),
        ("Transfer.", "Move assets between departments, projects, locations and companies with financial history preserved."),
        ("Maintenance.", "Log repairs, upgrades, cleaning, replacements and inspections with date, vendor, cost, description, status and next due date, and see month-to-date and total maintenance cost as key figures."),
        ("Licences.", "Software records hold the key, seat count, purchase and expiry dates, vendor, expired and expiring-soon alerts, and assignment to individuals."),
    ])
    b.h2("17.3  The financial layer")
    b.p("Asset categories are configured through a setup that defines the depreciation method, useful life, "
        "default residual value and the three ledger accounts the category needs: cost, accumulated "
        "depreciation and depreciation expense. Capitalisation records acquisition cost, capitalised cost, "
        "capitalisation and in-service dates, useful life in months, residual value and method; a second "
        "capitalisation of the same asset is refused.")
    b.h2("17.4  Depreciation")
    b.p("Straight-line, declining balance and double-declining balance are supported. The system generates "
        "the month-by-month schedule, skips periods that have already been posted, lets the user preview the "
        "charge before running it, and posts the depreciation journal in the same action. Net book value is "
        "available on demand, and the asset's complete financial history is held in one place.")
    b.h2("17.5  Impairment and disposal")
    b.bullets([
        "Impairment is recorded by comparing carrying value to recoverable value; the impairment loss journal is produced automatically.",
        "Disposal is handled as sale, scrap or donation, with gain or loss computed automatically and full derecognition journals written.",
        "Both appear on the asset's history, so a reviewer can reconstruct the whole financial life of the item without leaving the record.",
    ])
    b.h2("17.6  The asset dashboard")
    b.p("Asset cost, accumulated depreciation and net book value at the top; monthly depreciation trend; "
        "cost by category; the count of assets ready for depreciation; ledger account mappings; totals by "
        "status and category; warranty position; licence expiry; recent assignments; and low-stock alerts on "
        "the operational side. A pending-schedule queue on the module home tells the accountant exactly which "
        "assets still need this month's charge.")
    b.h2("17.7  Asset reporting")
    b.p("Nine reports cover the register, category summary, depreciation schedule, monthly depreciation "
        "summary, net book value, asset movement, additions, disposals, gain and loss and impairment. "
        "Several are print-ready and the register and depreciation schedules also export as CSV.")
    b.callout("Business benefit",
              "The two chronic asset problems are unrecorded disposals and depreciation that is done from a "
              "spreadsheet. Here depreciation runs from the category's own method and life, posts itself, "
              "cannot double-post a month, and computes the gain or loss on disposal — which also means the "
              "fixed-asset subledger reconciles to the control account without a manual schedule.")

    # ------------------------------------------------------------------ 18
    b.h1("18.  Payroll and Workforce Cost")
    b.lead("QASWA ERP carries workforce cost from an approved pay run into the ledger, tracks what is owed "
           "to staff, manages salary payment batches and reconciles payroll against finance against the bank.")
    b.h2("18.1  The payroll record")
    b.p("Each run carries a run code, period start and end, pay date, basic salary, allowances, overtime, "
        "employer contributions, employee deductions, gross and net pay, and moves through draft, approved, "
        "posted and paid with the approver's name and timestamp recorded. The finance view of payroll starts "
        "where an approved run becomes eligible for posting.")
    b.h2("18.2  Component-to-account mapping")
    b.p("Every payroll component name is mapped to a chart-of-accounts line and classified as an expense, a "
        "liability or an asset. Mappings are added, edited, viewed and processed from a single screen and can "
        "be set active or inactive and searched. This mapping is what allows a salary posting to hit the "
        "right accounts without an accountant interpreting the pay structure each month.")
    b.h2("18.3  Posting a payroll run")
    b.bullets([
        "The system builds the journal automatically: salary expense debited, salary payable credited.",
        "Gross, deductions and net are recorded against the posting.",
        "The run is stamped posted and the reconciliation position updates.",
        "Posting goes through the same gateway and the same period-lock checks as every other document, so a run cannot be posted into a closed month.",
    ])
    b.h2("18.4  Salary payment batches")
    b.table(
        ["Stage", "Behaviour"],
        [["Create", "A batch is raised against the unpaid balance of a posted run, with a name, the funding bank account, a date, a method — bank transfer, cheque or cash — and a reference."],
         ["Check", "A partial-payment warning appears if the batch does not cover the balance."],
         ["Post", "The system writes the debit to salary payable and the credit to the bank account."],
         ["Track", "Batches move pending → approved → paid, with a failed state for exceptions, and the run advances toward paid."],
         ["Reconcile", "A dedicated screen compares payroll total, posted total and bank-paid total with a difference column and a status of reconciled, unreconciled or investigation."]],
        widths=[1.8, 15.2], kind="kv")
    b.h2("18.5  Payables and deductions")
    b.p("Separate screens hold salary payables and deduction payables, so the money owed to staff and the "
        "money withheld on their behalf — taxes, contributions, deductions — are tracked as distinct "
        "liabilities rather than one net figure. Employer contributions are reported alongside.")
    b.h2("18.6  Payroll reporting")
    b.bullets([
        "Payroll cost and salary expense.",
        "Department payroll and monthly summary.",
        "Yearly summary and employee payable.",
        "Deduction report and employer contribution report.",
        "Payment status report and payroll reconciliation.",
        "The payroll report hub in finance adds summary, cost, detail, monthly and liability views with date-range and department filters and print styling.",
    ])
    b.callout("Being precise about scope",
              "The posting, payable, disbursement, reconciliation and reporting side of payroll is fully "
              "implemented and audited inside the product. The salary-board computation screen — gross-to-net "
              "arithmetic from an employee salary structure, payslip PDFs and a bank disbursement file — is "
              "delivered in the next release (chapter 37). Today, approved run totals enter the system and "
              "everything downstream of them happens inside QASWA ERP.",
              fill="FFF6E5", accent=HEX_GOLD, label="HONEST SCOPE")

    # ------------------------------------------------------------------ 19
    b.h1("19.  Human Resources I — People, Attendance and Leave")
    b.lead("The personnel file, the daily attendance register, the leave engine and the calendar — with "
           "expiry surveillance built in.")
    b.h2("19.1  The employee record")
    b.image("screenshots/09-employees.png",
            caption="Figure 17 - The employee register: personal data, departments, documents and balances on "
                    "one record.")
    b.table(
        ["Group", "Fields and behaviour"],
        [["Personal", "Name, gender, date of birth, marital status, phone, email, address and photograph."],
         ["Employment", "Department, designation, joining date, employment type (full time, part time, contract, intern), reporting manager, work location and status (active, inactive, terminated, resigned)."],
         ["Identity and immigration", "Nationality, passport number and expiry, visa type from nine options, visa number and expiry, Emirates ID number and expiry, contract number with start and end dates."],
         ["Code", "The next employee code is allocated automatically in an EMP-plus-year-plus-sequence format, with gaps retried and duplicate email addresses blocked."],
         ["Search", "A number typed with or without dashes finds the same record, so a partially entered Emirates ID still matches."]],
        widths=[3.2, 13.8], kind="kv")
    b.h2("19.2  Document vault and expiry watch")
    b.p("Fixed document slots hold the passport copy, visa copy, Emirates ID copy and employment contract "
        "copy, plus named additional documents in PDF and image or Word formats. Each file records who "
        "uploaded it and when, and offers view and download. Scans are colour-coded by expiry: amber within "
        "sixty days, red once expired. Compliance status is therefore visible on the record rather than being "
        "discovered at an audit or a visa renewal deadline.")
    b.h2("19.3  Departments and designations")
    b.bullets([
        "Departments hold a name, a unique code, a description and an active flag, show a live count of active employees on each row, and refuse deletion while staff are attached.",
        "Designations are tied to a department and show their own employee counts.",
        "Reporting lines are held on each employee record, giving a practical management chain for approvals and escalation.",
    ])
    b.h2("19.4  Attendance")
    b.image("screenshots/10-attendance.png",
            caption="Figure 5 - Daily attendance captured and corrected by status chip, with today's present, absent "
                    "and on-leave counts feeding the HR home page.")
    b.table(
        ["Capability", "Detail"],
        [["Daily marking", "Check-in and check-out times, status, late minutes and remarks, per employee per day."],
         ["Status set", "Present, absent, half day, leave, holiday and weekend, each shown as a colour chip."],
         ["Guards", "A second record for the same employee and date is refused with a clear message; a check-out earlier than the check-in is prevented by the form."],
         ["Correction", "Any record can be amended later, with the change audited — the practical regularisation route when a mark is wrong."],
         ["Monthly register", "Filtered by employee, month, year and status, with day-count tiles for present, absent and half day, a late-minutes column and pagination."],
         ["Dashboard", "Today's present, absent and on-leave counts feed the HR home page."]],
        widths=[3.0, 14.0], kind="kv")
    b.h2("19.5  Leave types and entitlement")
    b.image("screenshots/11-leave.png",
            caption="Figure 6 - Leave application and live balance checking, with the allocation grid behind every "
                    "entitlement.")
    b.p("Leave types are defined with a unique code, annual days entitlement, a carry-forward switch and an "
        "active flag. Annual balances are allocated to every employee for every leave type from a single "
        "pre-filled grid, so a year's entitlement is issued in one action rather than one record at a time.")
    b.h2("19.6  Applying and approving leave")
    b.bullets([
        "A request is raised by leave type and date range; the number of days is computed automatically and a half day can be taken as 0.5.",
        "Before submission the screen shows allocated, used, pending and remaining days, and states whether the request is fully covered, partly loss of pay with the number of loss-of-pay days, or wholly loss of pay.",
        "Requests move pending → approved or rejected, with the approver's identity and remarks recorded.",
        "On approval, days are deducted from the current year's balance, and a balance record is created automatically from the type default if none exists.",
        "Loss-of-pay approvals are recorded without deducting from an earned balance.",
        "The approve and reject actions are available inline on the list with confirmation, and the register filters by employee, department, status and date.",
    ])
    b.h2("19.7  Holiday calendar")
    b.p("Holidays are maintained year by year with a name, date, type — national, festival or optional — and "
        "a description. An upcoming-holidays strip and colour-coded type badges keep the calendar readable, "
        "and the same data feeds the HR dashboard.")
    b.h2("19.8  Time tracking")
    b.p("Timesheets log hours per employee against a project and an optional task, with the work date and a "
        "description. The register filters by employee, project, month and year and totals the month and the "
        "current week, feeding the hours figures on the project and HR dashboards.")
    b.h2("19.9  HR dashboards and reports")
    b.bullets([
        ("HRMS home.", "Tiles for employees, contractors, departments, designations, attendance and leave; today's present, absent and on-leave; pending and approved leave; upcoming holidays; new hires this month; and six charts covering employees by department, attendance today, leave by type, monthly hires, gender split and employment type. Permission-aware quick actions offer new employee, mark attendance, request leave and new department."),
        ("Leave dashboard.", "Active headcount, pending approvals with a review-now prompt, approvals this month, remaining balance per employee and an allocated-versus-used chart."),
        ("Leave reports.", "By employee, by department, by leave type and a detailed leave log, all filtered by date range, employee, department, type and status, printable and downloadable."),
        ("Report centre.", "Employee summary, an attendance report showing present, absent, late and attendance percentage, and a leave summary — each exportable to CSV, PDF or print, saveable as a named report and schedulable."),
        ("Audit.", "Marking attendance, uploading a document, approving or rejecting leave, posting payroll and exporting a report each write an audit entry with the user, module, IP address and timestamp."),
    ])
    b.callout("Business benefit",
              "HR administration stops living in folders. Immigration document expiry is surfaced by colour "
              "before it becomes a legal problem, leave balances are calculated rather than remembered, and "
              "attendance and leave figures are available on the same screen as headcount — which is what "
              "makes workforce planning discussions possible at all.")

    # ------------------------------------------------------------------ 20
    b.h1("20.  Human Resources II — Contractors, Onboarding and the People Directory")
    b.lead("A contractor is not an employee, and a person may be both a customer contact and a supplier "
           "contact. QASWA ERP models this properly instead of forcing everyone into one table.")
    b.h2("20.1  The unified people directory")
    b.p("One directory covers every person your organisation deals with, across three record categories: "
        "employee, customer and contractor. Each entry shows the categories that person exists in, which "
        "steps of their setup remain unfinished, and links to the underlying records. Search runs across the "
        "directory, with category and status filters and category chips so a single page answers the question "
        "“do we already have this person?”.")
    b.h2("20.2  Structured onboarding")
    b.table(
        ["Onboarding step", "Behaviour"],
        [["Checklist", "One checklist per person covering each category they should exist in, with an overall progress bar."],
         ["Complete details", "Create the missing record directly from the checklist."],
         ["Link existing", "Attach a record that already exists; duplicate prevention runs on email address."],
         ["Decline", "Mark a category as not applicable, with the option to reopen the step later."],
         ["Login and role", "Grant, link or detach a system login and role directly from the person's profile."],
         ["Consistency", "Maintenance actions re-synchronise the directory and prune entries that no longer have a record behind any category; deleting one category forfeits or reopens the affected steps rather than orphaning the person."]],
        widths=[3.0, 14.0], kind="kv")
    b.h2("20.3  Why this matters operationally")
    b.p("Without a directory, the same individual appears as an employee, a vendor contact and a customer "
        "representative, and nobody knows the real headcount of relationships. With it, identity is "
        "reconciled: one person, one person code, and every role they play visible on one page. The platform "
        "ships an identity audit that enforces exactly this rule across fifteen checks.")
    b.h2("20.4  Contractor management")
    b.bullets([
        "Registration with engagement type, source and status.",
        "A compliance panel holding Emirates ID, visa type, visa number and expiry, work permit number and expiry.",
        "Slot documents with a valid-until date, displayed as expiry chips: expired, expires in N days, or all documents valid.",
        "A formal contract lifecycle — draft, approve, activate, extend up to a configured limit, complete or terminate — with a designated current contract and deletion permitted only on drafts, so an approved or activated engagement can never be quietly removed.",
        "A dated rate schedule recording basis, amount and the reason for each change, with a monthly-equivalent calculation and a not-to-exceed ceiling.",
        "A sortable, filterable register with key-figure tiles and pagination.",
    ])
    b.h2("20.5  Access to the system for people and partners")
    b.p("Staff, contractors and client contacts receive ordinary logins and see only the modules their role "
        "permits. Because permission checks run on every screen, tab, button and export, external access can "
        "be granted narrowly — a supplier's project manager can see the task board without seeing your margin.")
    b.callout("Business benefit",
              "Contractor spend is usually the least visible part of the workforce budget. Rate history, "
              "engagement ceilings, contract lifecycle states and document compliance for contractors sit in "
              "the same place as employees, which means a single report can answer a question that normally "
              "takes three spreadsheets.")
