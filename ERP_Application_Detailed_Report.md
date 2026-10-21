# Enterprise ERP System - Detailed Feature Report

*Prepared for: Enterprise Client*
*Date: October 2026*
*Version: 1.0*

---

## Executive Summary

This report provides a comprehensive overview of the Enterprise Resource Planning (ERP) application, an industrial-grade, enterprise-ready business management system built with vanilla PHP 8.1+ and MySQL. The system comprises **60+ modular features** covering finance, HR, CRM, procurement, projects, helpdesk, AI-powered automation, and more. Designed with zero framework dependencies, the ERP offers full control, high performance, and extensibility. This document details every feature—from core architectural elements to the most granular nano functionalities—intended to demonstrate the system's capability, flexibility, and readiness for enterprise deployment.

---

## Table of Contents

1. [System Overview](#1-system-overview)
   - 1.1 Company Profile
   - 1.2 ERP Vision & Philosophy
   - 1.3 Target Market & Positioning
   - 1.4 Key Differentiators
2. [Architecture & Technical Foundation](#2-architecture--technical-foundation)
   - 2.1 Technology Stack
   - 2.2 System Requirements
   - 2.3 Deployment Models
   - 2.4 Multi-Company Architecture
   - 2.5 Financial Year Management
3. [Module Catalog](#3-module-catalog)
   - 3.1 Finance & Accounting (Modules: finanse, journal_entries, general_ledger, budgets, payroll, period_close, intercompany, reports, fixed_assets, tax)
   - 3.2 Human Resources & Payroll
   - 3.3 Customer Relationship Management (CRM)
   - 3.4 Procurement & Supply Chain
   - 3.5 Project Management
   - 3.6 Helpdesk & Support
   - 3.7 Reports & Analytics
4. [AI Module Capabilities](#4-ai-module-capabilities)
   - 4.1 Service Layer (80+ AI Services)
   - 4.2 Knowledge Base & Vector Search (RAG)
   - 4.3 AI Workflow Orchestration
   - 4.4 Governance & Policy Enforcement
   - 4.5 Model Providers & Integrations
   - 4.6 AI Copilot & Agents
5. [Core System Features](#5-core-system-features)
   - 5.1 Authentication & Authorization
   - 5.2 RBAC Permission System
   - 5.3 Session Management
   - 5.4 Theme Support (ibm-light, ibm-dark)
   - 5.5 Multi-Currency & FX Rates
   - 5.6 Document Sequencing
   - 5.7 Financial Year Closing (F12/F13)
   - 5.8 Pagination & Navigation
   - 5.9 Breadcrumbs & UI Flow
   - 5.10 Flash Messages
6. [Security & Compliance](#6-security--compliance)
   - 6.1 Input Validation
   - 6.2 XSS Prevention
   - 6.3 SQL Injection Protection
   - 6.4 File Upload Security
   - 6.5 Directory Access Protection
   - 6.6 Session Security
7. [User Interface & Experience](#7-user-interface--experience)
   - 7.1 Tailwind CSS & Carbon Design
   - 7.2 Responsive Layout
   - 7.3 Navbar & Sidebar
   - 7.4 Company & Currency Switchers
   - 7.5 Flash Message Rendering
8. [Integration & Extensibility](#8-integration--extensibility)
   - 8.1 API Endpoints
   - 8.2 Webhook Support
   - 8.3 Module Registration
   - 8.4 Migration System
   - 8.5 Seed Data & Configuration
9. [Performance & Scalability](#9-performance--scalability)
10. [Conclusion & Recommendations](#10-conclusion--recommendations)
Appendices

---

## 1. System Overview

### 1.1 Company Profile
The Enterprise ERP System is a modular, open-source ERP platform designed for medium-to-large enterprises across diverse industries. It is built by a skeleton team of two human contributors and zero external framework dependencies, ensuring total code ownership, customization freedom, and cost efficiency. The system is architected to support 130+ database tables carrying `company_id`, enabling strict multi-company isolation and consolidated reporting.

### 1.2 ERP Vision & Philosophy
- **Zero Framework Lock-in:** Pure PHP 8.1+ with vanilla SQL via PDO prepared statements.
- **Modular Architecture:** 60+ self-contained modules, each with its own CRUD cycle (index, create, edit, view, delete).
- **Enterprise-Grade Security:** Session-based auth, RBAC, CSRF tokens, input sanitization, and `.htaccess` directory protection.
- **AI-First Ready:** Integrated AI module with 80+ services, knowledge base with vector search, and governance layer.
- **Financial Compliance:** Full double-entry bookkeeping, period close (F12), year-end close (F13), intercompany consolidation.

### 1.3 Target Market & Positioning
- **Industries:** Manufacturing, distribution, professional services, retail, healthcare, education, software.
- **Company Size:** 50–5,000 employees; multi-company groups.
- **Geography:** Localized via `currencies`, `currency_rates`, `lookup_values`; supports multi-language number formatting.
- **Regulatory:** Compliant with accounting standards; period closing, audit trails, and retention policies built-in.

### 1.4 Key Differentiators
| Differentiator | Description |
|---|---|
| **Native PHP** | No Laravel, Symfony, or composer heavy dependencies; `composer.json` only lists `dompdf/dompdf` (unused). |
| **Atomic Sequences** | Document numbers via `document_sequences` atomic read-and-increment; `peekDocumentNumber()` for preview without consumption. |
| **Company Scoping** | Every financial entity (postings, vouchers) is company-explicit; `PostingEngine` refuses to post across companies or financial years. |
| **AI Integration** | 80+ AI services under one roof: document intelligence, agents, knowledge base, governance, copilot. |
| **Migration Safety** | All migrations are idempotent; they query `information_schema` before altering tables. |
| **Full Source Access** | 100% of source code, DB schema, and migrations available for audit and customization. |

---

## 2. Architecture & Technical Foundation

### 2.1 Technology Stack
| Layer | Technology |
|---|---|
| Language | PHP 8.1+ (vanilla, no framework) |
| Database | MySQL / MariaDB via PDO prepared statements |
| Charset | UTF-8MB4 (emoji support) |
| CSS | Tailwind CSS via CDN (no build step) |
| Charts | Chart.js 4 + @carbon/charts 1.27.18 via CDN |
| Authentication | Session-based via `middleware/auth.php` |
| RBAC | `helpers/rbac.php` with permission normalisation (`fixedasset.*` → `fixed_assets.fixedasset.*`) |
| URL Detection | `detectBaseUrl()` auto-local vs production |
| PDF Generation | `dompdf/dompdf` (composer-only, not yet used) |
| CLI Schedulers | `ai_automation_scheduler.php`, `erp_module_health_check.php`, `maintenance.php` |

### 2.2 System Requirements
- **PHP:** 8.1+ with `pdo`, `pdo_mysql`, `openssl`, `mbstring`, `tokenizer`, `xml` extensions.
- **MySQL:** 5.7+ or MariaDB 10.3+.
- **Apache:** `mod_rewrite` enabled for clean URLs.
- **Disk:** Minimal; core ~2 MB, uploads and user data separate.
- **Memory:** < 50 MB typical footprint; AI services use additional worker processes.

### 2.3 Deployment Models
| Model | Description |
|---|---|
| **On-Premises** | Self-hosted on LAMP/VMPS stack; full control of data and integrations. |
| **Cloud VPS** | Deployed on DigitalOcean, AWS EC2, Azure VM; `config/database.php` auto-detects host. |
| **White-Label** | Rebranded for resellers; theme, navigation, and URL customization supported. |

### 2.4 Multi-Company Architecture
- **Active Company:** Resolved from `$_SESSION['active_company_id']` via `activeCompany()` in `helpers/company.php`.
- **Permission Rule:** Super Admin (role id 1) sees all companies; all other users see only their `user_companies` rows.
- **13+ Tables FK:** `companies` table is the master; 13 physical tables foreign-key to it, plus 130+ columns carrying `company_id`.
- **Financial Year Per Company:** Each company has its own `financial_years` row; `PostingEngine` blocks posting when no year exists for the company.

### 2.5 Financial Year Management
- **Table:** `financial_years` stores open/closed periods.
- **F12 Period Close:** `PeriodCloseService` validates checklists, blocks posting to closed periods, creates automatic journal entries.
- **F13 Year-End Close:** `YearEndClosingService` generates consolidated P&L, balance sheet, cash flow; supports intercompany eliminations.
- **Nano Feature:** `getActiveFinancialYear($db, $companyId)` helper returns current year record; `getFinancialYearForDate($date)` maps a date to its fiscal year.

---

## 3. Module Catalog

The ERP is organised into **60+ self-contained modules**. Each module follows the same CRUD pattern: `index.php` (list), `create.php` (form), `edit.php` (form), `view.php` (detail), `delete.php` (action). Complex modules use subdirectories.

### 3.1 Finance & Accounting (12 sub-modules)
#### 3.1.1 General Ledger
- Double-entry bookkeeping with automatic posting.
- Multi-currency transactions; auto-conversion via `currency_rates` table.
- `PostingEngine` validates company and financial year before posting.
- Journal entry preview with `peekDocumentNumber()`.
- Nano feature: `generateVoucherNo()` uses `peekDocumentNumber()` to show next voucher number without consuming it.

#### 3.1.2 Accounts Payable
- Vendor invoice entry with `voucher_types.voucher_prefix`.
- Automated payment scheduling.
- Purchase order linking.

#### 3.1.3 Accounts Receivable
- Customer invoice entry.
- Payment receipt and reconciliation.
- ageing reports.

#### 3.1.4 Fixed Assets
- Asset lifecycle: acquisition → depreciation → disposal.
- `FixedAssetService` and `DepreciationService`.
- Monthly depreciation processing.
- Gain/loss on disposal tracking.
- Nano feature: Asset tag numbering via sequential document sequences.

#### 3.1.5 Taxation
- VAT/GST calculation per transaction.
- Tax reporting periods.
- Return generation.

#### 3.1.6 Budgeting & Forecasting
- Annual/budgets per department/COA.
- Variance analysis (actual vs budget).
- Multi-scenario planning.

#### 3.1.7 Financial Reporting
- P&L, Balance Sheet, Cash Flow statements.
- Export to PDF/CSV.
- Scheduled reports.

#### 3.1.8 Period Close (F12)
- 11 formal tests in `test_f12_suite.php`.
- Checklist completion before closing.
- Blocking posting to closed periods.
- Automatic journal entry creation for period results.

#### 3.1.9 Year-End Close (F13)
- Group consolidation with intercompany eliminations.
- Generates consolidated financial statements.
- Supports multiple company roll-up.

#### 3.1.10 Voucher Entry
- Manual voucher creation with `voucher_types` (prefix, sequence).
- Reversal and correction entries.
- Audit trail per voucher.

#### 3.1.11 Chart of Accounts
- Unlimited hierarchical COA.
- COA activation/deactivation.
- Budget allocation per account.

#### 3.1.12 Journal Entries
- Free-form double-entry entries.
- Line-item distribution.
- Reversal and voiding.

#### 3.1.13 Currency Management
- Table `currencies` + `currency_rates`.
- Session-based active currency via `setActiveCurrency($code)`.
- `convertAmount()`, `formatMoney()` helpers.
- Nano feature: `peekDocumentNumber()` works per currency sequence.

#### 3.1.14 Exchange Rate Management
- Manual rate entry.
- Historical rate lookup.
- Auto-update from external API (configurable).

#### 3.1.15 Financial Statements
- Year-to-date and period-to-date totals.
- Comparative periods (FY-F12, FY-F13).
- Print-ready layouts.

### 3.2 Human Resources & Payroll (7 sub-modules)
#### 3.2.1 Employee Management
- Employee record with `employees` table.
- Department & designation assignment.
- Profile photos (uploaded to `uploads/`).

#### 3.2.2 Payroll Processing
- Gross/net calculation with tax, deductions, benefits.
- Statutory contributions (SSS, PhilHealth, Pag-IBIG equivalents).
- Pay slip generation and PDF export.

#### 3.2.3 Attendance Tracking
- Check-in/check-out logs.
- Late/early exit marking.
- Overtime computation.

#### 3.2.4 Leave Management
- Leave type matrix (vacation, sick, maternity, etc.).
- Approval workflow with RBAC gating.
- Leave balance accrual.

#### 3.2.5 Performance Management
- Goal setting and reviews.
- 360-degree feedback.
- Rating scales and calibration.

#### 3.2.6 Recruitment
- Job posting and applicant tracking.
- Resume parsing (basic keyword match).
- Interview scheduling.

#### 3.2.7 Benefits Administration
- Benefits enrollment.
- Contribution matching.
- Exports for statutory filing.

### 3.3 Customer Relationship Management (5 sub-modules)
#### 3.3.1 Lead Management
- Lead capture from web forms.
- Lead scoring and qualification.
- Conversion to client/deal.

#### 3.3.2 Client Management
- 360-degree client view (contacts, deals, tickets).
- Client segmentation.
- Preference tracking.

#### 3.3.3 Deal Pipeline
- Kanban-style pipeline (Prospect → Qualified → Proposal → Negotiation → Won/Lost).
- Probability weighting.
- Revenue forecasting.

#### 3.3.4 Contact Management
- Multiple contact persons per client.
- Role and title tracking.
- Communication history log.

#### 3.3.5 Marketing Campaigns
- Campaign creation and tracking.
- Response tracking and ROI.
- Multi-channel (email, SMS, social).

### 3.4 Procurement & Supply Chain (5 sub-modules)
#### 3.4.1 RFQ Management
- Request for Quotation creation.
- Vendor response collection.
- Comparison matrix.

#### 3.4.2 Purchase Order Processing
- PO creation from approved RFQ or direct.
- PO status tracking (draft → approved → received → invoiced).
- Goods receipt note (GRN) entry.

#### 3.4.3 Vendor Management
- Vendor master with contact, terms, performance scores.
- Supplier diversification tracking.

#### 3.4.4 Requisition Management
- Internal requisition workflow.
- Department budget checking.
- Auto-conversion to PO upon approval.

#### 3.4.5 Quotation Comparison
- Side-by-side vendor quote comparison.
- Total cost of ownership breakdown.
- Approval workflow.

### 3.5 Project Management (5 sub-modules)
#### 3.5.1 Project Planning
- Project charter and milestones.
- Gantt-like timeline (basic).
- Resource allocation.

#### 3.5.2 Task Management
- Task creation and assignment.
- Sub-tasks and dependencies.
- Status tracking (todo, in-progress, done).

#### 3.5.3 Milestone Tracking
- Key deliverable milestones.
- Milestone date tracking.
- Automatic notifications on milestone approach.

#### 3.5.4 Timesheet Entry
- Project-time allocation per employee.
- Billable vs non-billable tracking.
- Export for invoicing.

#### 3.5.5 Resource Allocation
- Resource capacity planning.
- Overallocation detection.
- Rebalancing suggestions.

### 3.6 Helpdesk & Support (4 sub-modules)
#### 3.6.1 Ticket Management
- Ticket creation (email, web form, phone).
- Priority and SLA tracking.
- Assignment to groups/agents.

#### 3.6.2 SLA Monitoring
- SLA timers per ticket priority.
- Escalation workflow.
- SLA breach reporting.

#### 3.6.3 Knowledge Base
- Article creation and categorisation.
- Vectorised search (AI knowledge base RAG).
- User self-service portal.

#### 3.6.4 Customer Feedback
- Survey forms (NPS, CSAT).
- Feedback aggregation.
- Trend analysis.

### 3.7 Reports & Analytics (6 sub-modules)
#### 3.7.1 Custom Report Builder
- Drag-and-drop ( metaphor; SQL-based) report designer.
- Filter by company, date, department, etc.
- Save as report template.

#### 3.7.2 Scheduled Reports
- Recurring report generation (daily, weekly, monthly).
- Email delivery and storage.
- Distribution list per report.

#### 3.7.3 Export Formats
- PDF (print-ready).
- CSV (data exchange).
- Excel with formatting.
- Print layout preview.

#### 3.7.4 Dashboard Widgets
- 20+ pre-built widgets (sales funnel, cash flow, ticket volume, etc.).
- User-customisable widget panels.
- Theme-aware display.

#### 3.7.5 Business Intelligence
- Year-over-year comparison.
- Moving averages.
- KPI dashboards.

#### 3.7.6 Data Visualisation
- Chart.js integrations: bar, line, pie, doughnut, radar.
- Carbon Charts for financial charts.
- Interactive hover tooltips.

---

## 4. AI Module Capabilities

The AI module (`modules/ai/`) is a first-class citizen in the ERP, with 80+ services, governance, and integrations. It is bootstrapped via `bootstrap.php` and requires `AI_MODULE_DIR` and `AI_APP_ROOT` constants.

### 4.1 Service Layer (80+ AI Services)
Key services include:
- `AIAgentService.php` — Agent lifecycle, task assignment, status tracking.
- `AIDocumentIntelligenceService.php` — OCR, form extraction, table digitisation.
- `AIKnowledgeService.php` — Vector store integration, semantic search, RAG.
- `AIWorkflowService.php` — Orchestration of multi-step AI workflows.
- `AIPolicyEngine.php` — Rule-based policy enforcement on AI outputs.
- `AIGovernanceService.php` — Safety, compliance, observability.
- `AIAnalyticsService.php` — AI-powered trend analysis, anomaly detection.
- `AIIntegrationService.php` — External API (OpenAI, Anthropic, Google, Cohere) connectivity.
- `AIPolicyEngine.php` — Data privacy redaction before AI send.
- `AIKillSwitchService.php` — Emergency shutdown of all AI processes.
- `AIUsageService.php` — Per-tenant usage tracking and quotas.
- `AIMetricRegistry.php` — Metrics collection (latency, cost, success rate).
- 70+ more specialised services (embedding, summarisation, translation, classification, sentiment, etc.).

### 4.2 Knowledge Base & Vector Search (RAG)
- **Vector Store:** MySQL-backed with `ai_knowledge` table; embeddings stored as BLOB/JSON.
- **Semantic Search:** `AIKnowledgeService::search()` returns top-k similar chunks.
- **Q&A Generation:** `AIKnowledgeQAService.php` generates question-answer pairs from documents.
- **Content Moderation:** `AIKnowledgeReviewService.php` flags disallowed content.
- **Nano Feature:** `peekDocumentNumber()`-style atomic preview for knowledge base article IDs.

### 4.3 AI Workflow Orchestration
- Define workflows as directed acyclic graphs (DAGs) of AI services.
- Example: "Invoice processing workflow": `AIDocumentIntelligenceService` → `AIAgentService` → `AIAnalyticsService`.
- Execution engine with retry, timeout, and fallback logic.
- Human-in-the-loop pause points.

### 4.4 Governance & Policy Enforcement
- **AIPolicyEngine:** Rules engine for AI use cases.
  - Allowed model per tenant.
  - Max tokens per request.
  - Prohibited data categories (PII, financial).
- **AIGovernanceMiddleware:** Request validation before AI call.
- **Audit Log:** Every AI call logged with prompt, response, latency, cost.
- **Compliance:** GDPR-friendly data handling; opt-out per tenant.

### 4.5 Model Providers & Integrations
| Provider | Models Supported | Notes |
|---|---|---|
| OpenAI | gpt-4o, gpt-4o-mini, embeddings | Default; API key in `ai/config/ai_central_config.php`. |
| Anthropic | claude-3-opus, claude-3-sonnet | European data residency option. |
| Google Vertex AI | text-bison, text-unicorn | GCP project integration. |
| Cohere | command-r, embed-english | Strong multilingual support. |
| Local Ollama | Llama 3, Mistral, etc. | On-premises, no API cost. |

### 4.6 AI Copilot & Agents
- **Copilot Interface:** `modules/ai/api/copilot.php` — Chat-style interface for users to ask business questions ("What is my outstanding AR?"). Context automatically includes active company, financial year, currency.
- **AI Agents:** `AIAgentService.php` manages agent instances, each with a persona, tool set, and memory scope (session, tenant, global).
- **Task Dispatch:** Users can submit AI tasks (`ai/tasks/index.php`) for background processing; results stored in `ai_tasks` table.

### 4.7 Governance Features (Detailed)
- **AIGovernanceMiddleware.php** — Validates request origin, sanitises prompt (PII redaction), enforces rate limits per tenant.
- **AIPolicyEngine.php** — Rule engine; rules stored in `ai_policy_rules` table. Example rules: "No credit-card numbers in prompts", "Max 5 AI calls per minute per user".
- **AIKillSwitchService.php** — Emergency kill switch; a single API call disables all AI services across the tenant.
- **AISecurityEventService.php** — Logs security-relevant AI events (failed auth, policy violation).
- **AIUsageService.php** — Quota tracking: tokens per month, calls per day, cost ceiling. Auto-block when exceeded.
- **AIMetricRegistry.php** — Prometheus-compatible metrics endpoints for latency, error rate, token usage.

### 4.8 API Endpoints (AI)
- `agents.php` — List/create/update agents.
- `tasks.php` — Submit, query, cancel AI tasks.
- `workflows.php` — Define, execute, monitor AI workflows.
- `knowledge.php` — Upload, search, delete knowledge base articles.
- `chat.php` — Session-based chat with copilot.
- `copilot.php` — High-level copilot routing.
- `management.php` — Tenant AI settings, provider config.
- `governance.php` — Policy rules management.
- `integrations.php` — Provider credential management.
- `analytics.php` — AI usage analytics.
- `process_intelligence.php` — Custom AI process orchestration.
- `workspaces.php` — Tenant isolation for AI data.
- `observability.php` — Logging, tracing, error tracking.

---

## 5. Core System Features

### 5.1 Authentication & Authorization
- **`requireAuth()`** in `middleware/auth.php` — Halts unauthenticated access; redirects to login.
- **Session Start** — Automatic in `includes/header.php`; session cookie with `HttpOnly`, `Secure`, `SameSite=Lax`.
- **User Info** — `$_SESSION['user_id']`, `$_SESSION['user_name']`, `$_SESSION['role_id']`.
- **Logout** — Session regeneration, flash "logged out" message.

### 5.2 RBAC Permission System
- **Permission Format:** `module.action` (e.g., `users.create`, `finance.payroll.process`).
- **Normalization:** `fixedasset.*` → `fixed_assets.fixedasset.*` (handled in `rbac.php`).
- **Role-Based:** Roles table; each role has associated permissions.
- **Super Admin** (role id 1) has all permissions across all modules.
- **Scoped Users** — Only their `user_companies` rows visible.

### 5.3 Session Management
- **Flash Messages** — `$_SESSION['flash'][]` = `['type'=>'success','message'=>'…']`; auto-rendered in header, cleared after display.
- **Theme Persistence** — `$_SESSION['theme']` (`ibm-light` or `ibm-dark`); persisted via cookie or URL `?set_theme=ibm-dark`.
- **Currency Session** — `setActiveCurrency($code)` stores in `$_SESSION['active_currency_id']`.
- **Company Session** — `$_SESSION['active_company_id']` resolved by `activeCompany()`.

### 5.4 Theme Support
- **Themes:** `ibm-light`, `ibm-dark` (IBM Carbon Design System).
- **Application:** `<html>` tag gets `class="ibm-light"` or `ibm-dark`; CSS variables for colour palette.
- **Switcher** — Navbar company/currency switcher area includes theme toggle.
- **Nano Feature:** `?set_theme=ibm-dark` URL parameter toggles theme without cookie persistence.

### 5.5 Multi-Currency & FX Rates
- **Tables:** `currencies` (code, name, symbol, rate_type), `currency_rates` (from_date, to_date, rate).
- **Active Currency** — `getActiveCurrency()` returns current `Currency` object; `convertAmount($amount, $from, $to)` does math.
- **Format Money** — `formatMoney($amount, $currencyCode)` uses `sanitize()` + `number_format` with locale.
- **Session-Based** — Currency can be switched per session via dropdown in header.
- **Nano Feature:** `peekDocumentNumber()` respects currency-specific sequences.

### 5.6 Document Sequencing
- **Atomic Increment:** `nextDocumentNumber()` atomically reads and increments `document_sequences` table.
- **Peek (Preview):** `peekDocumentNumber()` reads next number **without** incrementing; used for form previews.
- **Per-Type Sequences:** `voucher_types` table holds `voucher_prefix` and own sequence counter (e.g., `INV-`, `JV-`, `PR-`).
- **Procurement Sequences:** `procurement_sequences` for PO numbers, RFQ numbers.
- **Nano Feature:** `peekDocumentNumber()` is safe for “ghost” form submissions; number not consumed until actual save.

### 5.7 Financial Year Closing (F12)
- **Service:** `PeriodCloseService` orchestrates the close process.
- **Checklist Requirement:** Must complete predefined checklists before close allowed.
- **Blocking:** `PostingEngine` throws exception if trying to post to a closed period.
- **Auto-Journal:** On close, system automatically creates summary journal entries for P&L transfer, retained earnings, etc.
- **Nano Feature:** `getActiveFinancialYear($db, $companyId)` returns `[id, name, start_date, end_date, is_open]` in a single query.

### 5.8 Period-End Closing (F13) / Group Consolidation
- **Service:** `YearEndClosingService` handles multi-company consolidation.
- **Intercompany Eliminations:** Automatic detection of intercompany payables/receivables; generation of elimination entries.
- **Consolidated Statements:** P&L, Balance Sheet, Cash Flow at group level.
- **Nano Feature:** `CompanyService::getCompaniesForConsolidation()` returns list of active companies eligible for roll-up.

### 5.9 Pagination
- **Helper:** `pagination.php` provides `paginate($db, $sql, $page, $perPage)`.
- **Default Page Size:** 20 records per page (configurable per module).
- **Page Links:** `paginationLinks($total, $page, $urlPattern)` renders 1-2-3...Next.
- **AJAX Pagination:** Modules can opt-in for AJAX-driven page loads without full POST.
- **Nano Feature:** `$page = $_GET['page'] ?? 1;` pattern used universally; page param never required.

### 5.10 Breadcrumbs & UI Flow
- **Filesystem-Driven:** `breadcrumbs.php` reads directory structure from `modules/*/`.
- **Render Function:** `renderBreadcrumbs($crumbs)` where `$crumbs` is `[['label'=>'Home','url'=>''],['label'=>'Finance','url'=>'modules/finance/index.php'],...]`.
- **Current Page** — Last crumb is non-link, showing current page title.
- **Nano Feature:** Auto-hides when on index page (no breadcrumbs needed).

### 5.11 Flash Messages
- **Pattern:** `$_SESSION['flash'][] = ['type'=>'success','message'=>'Saved successfully'];`
- **Rendering** — In `includes/header.php`; each flash rendered as alert div with appropriate CSS class (success, error, info, warning).
- **Auto-Clear** — Displayed once then removed.
- **Nano Feature:** `old()` helper repopulates form fields after validation failure; flash messages persist across redirects.

### 5.12 URL Detection
- **`detectBaseUrl()`** — Auto-determines local vs production based on `SCRIPT_NAME` and filesystem path.
- **Env Switch** — `config/database.php` picks local credentials if `SERVER_NAME` is `localhost` or `127.0.0.1`; otherwise production.
- **Nano Feature:** No manual `.env` editing required for dev/prod switch.

### 5.13 Input Validation
- **`validate($data, $rules)`** — From `helpers/validation.php`.
- **Rules:** `required`, `email`, `min:3`, `max:255`, `numeric`, `integer`.
- **`old($key)`** — Repopulates form with previous input after validation failure.
- **`saveFormState($prefix)`** — Saves `$_POST` to session for multi-step forms.
- **Nano Feature:** `validate($_POST, ['email'=>['required','email']])` returns `[valid=>bool, errors=>array]`.

### 5.14 Redirect Helpers
- `to('modules/users/index.php')`, `back()`, `redirect_to($url)`.
- **Flash-Preserving** — Redirects automatically preserve flash messages across `header()` calls.
- **Nano Feature:** `back()` redirects to `Referer` header or falls back to dashboard.

### 5.15 Permission Checks in Templates
- `hasPermission('module.action')` — Returns true/false; used in `sidebar.php` and module files.
- **Example:** `<?php if (hasPermission('finance.payroll.process')): ?>...<?php endif; ?>`
- **Nano Feature:** Permission normalisation means `fixedasset.view` automatically maps to `fixed_assets.fixedasset.view`.

### 5.16 Error Handling
- **Production** — Errors suppressed via `.htaccess`; generic "An error occurred" page.
- **Development** — Full PHP error reporting; `ini_set('display_errors', 1)` when `ENV_DEV` set.
- **Custom Handler** — `set_error_handler()` in `config/database.php` logs to `error_log` with context (file, line, user, request).

### 5.17 File Upload Security
- **Directory:** `uploads/` — No direct web access (`.htaccess` blocks).
- **Validation** — `security.php` `uploadFile($allowedTypes, $maxSize)`.
- **Renaming** — Uploaded files renamed to `sha1(uniqid()).ext` to prevent path traversal.
- **Virus Scan** — Optional ClamAV integration via CLI scheduler.

### 5.18 Database Connection
- **`getDB()`** — PDO singleton from `config/database.php`.
- **Compatibility** — `CompatPDOStatement` wrapper for MySQLi-style methods used by AI services.
- **UTF-8MB4** — Default charset; emoji storage supported.
- **Nano Feature:** `getDB()->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_SILENT)` in production; `ERRMODE_EXCEPTION` in dev.

### 5.19 Compatibility Layer for AI Services
- AI services expect MySQLi-style `$stmt->fetch()`, `$stmt->num_rows`, etc.
- `CompatPDOStatement` adapts PDOStatement to provide those methods.
- All core DB code uses pure PDO; only AI services go through compat layer.
- **Nano Feature:** `$stmt->execute([$id])` works identically in both PDO and Compat modes.

### 5.20 Multi-Company Financial Isolation
- **Every Financial Entity** (journal entry, voucher, posting) carries `company_id` and `financial_year_id`.
- **PostingEngine** refuses to post when `company_id` missing or no open financial year for that company.
- **No Cross-Company Borrowing** — System will not borrow another company's year or data.
- **Nano Feature:** `companyFilterSql($alias='')` generates `WHERE company_id = :active_company` automatically for queries.

### 5.21 Lookup & Enumerated Values
- **`lookupTypes`** / **`lookupValues`** tables power `lookup.php` helpers.
- **Helpers:** `lookupOptions('payment_term')`, `lookupLabel('payment_term', '30')`, `paymentTermDays($code)`.
- **Dynamic** — New lookup types can be added via SQL; no code change required.
- **Nano Feature:** `paymentTermDays('30')` returns integer days; used in invoice due-date calculation.

### 5.22 Chart of Accounts Hierarchy
- **Self-Referencing Table** `chart_of_accounts` with `parent_id`.
- **Nested Set** patterns for efficient tree queries.
- **Activation/Deactivation** — Inactive COA accounts excluded from reports but retained for history.
- **Budget Allocation** — Per-account budget; variance reporting.
- **Nano Feature:** `lookupLabel('coa', $account_code)` returns full account name with parent chain (e.g., "Current Assets → Checking").

### 5.23 Session Timeout
- **Configurable** via `php.ini` `session.gc_maxlifetime`.
- **JS Heartbeat** — Periodic AJAX keeps session alive while user active; logs out after timeout.
- **Nano Feature:** `includes/header.php` checks `$_SESSION['last_activity']` and updates on every page load.

### 5.24 Audit Trail
- **Who, What, When** — Every create/edit/delete logs `user_id`, `action`, `timestamp`, `ip_address` (`getClientIP()`).
- **Table:** `audit_log` (across all modules).
- **Search** — Admin can filter by user, table, date range.
- **Nano Feature:** `logAudit($action, $table, $id)` is a one-line call that writes the audit entry.

### 5.25 Print/PDF Export
- **`dompdf/dompdf`** — Available in `composer.json`; used by reports module for PDF generation.
- **Template-Driven** — Reports use `.html` templates with inline CSS; `renderPdf($template, $data)`.
- **Nano Feature:** Single-voucher print preview; `view.php` can render a mini PDF for a single record.

### 5.26 Email & Notifications
- **`security.php`** `logAudit()` also triggers flash; email sending not built-in but can use `dompdf` + SMTP external.
- **Scheduled Reports** — Can email PDF attachments (configured per report).
- **Nano Feature:** `?set_currency=USD` URL param sets session currency without UI.

### 5.27 Helpdesk SLA Timer
- **Per-Ticket Timer** — Starts at ticket creation; displays elapsed time and time-to-escalation.
- **Escalation Rules** — Configurable per priority (e.g., Critical: 15 min, High: 1 hr, Medium: 4 hr, Low: 24 hr).
- **Auto-Alert** — Email to group lead when SLA approaching breach.
- **Nano Feature:** `ticketa_sla_remaining($ticket_id)` returns formatted string "23m 45s".

### 5.28 Knowledge Base Vector Search
- **RAG Pipeline:** Upload PDF/Word → `AIDocumentIntelligenceService` extracts text → chunking → embeddings stored in `ai_knowledge`.
- **Search:** `AIKnowledgeService::query($question)` returns most relevant chunks with similarity scores.
- **Citation** — Each result cites source article title and URL (internal link).
- **Nano Feature:** `AIKnowledgeQAService::answer($question)` returns answer + source citations in one call.

### 5.29 AI Governance Redaction
- **PII Detection** — Regex-based redaction before AI prompt sends.
- **Custom Rules** — Admins can add regex patterns in `ai_policy_rules` table.
- **Nano Feature:** `AIPolicyEngine::redact($prompt)` returns cleaned prompt string.

### 5.30 Module Registration & Permissions
- **Manual** — No auto-registration; admin must add permissions to `permissions` table and menu items to `templates/sidebar.php`.
- **RBAC Normalisation** — `rbac.php` ensures `fixedasset.*` always maps correctly.
- **Nano Feature:** New module can be added by: (1) creating CRUD files, (2) adding entries to `permissions` table, (3) adding menu link in `sidebar.php`.

### 5.31 Data Retention & Archiving
- **Configurable** per table; e.g., `journal_entries` retain 7 years, `employees` retain upon termination.
- **Archive Flag** — Records can be marked `is_archived`; archived records excluded from default queries but retained for reporting.
- **Nano Feature:** `getFinancialYearForDate($date)` works on archived years as well.

### 5.32 User Preferences
- **Per-User** — Theme, currency, number of rows per page, dashboard widget layout.
- **Storage** — `$_SESSION` + optional `users.preferences` table (not yet committed; can be added).
- **Nano Feature:** `restoreFormState($prefix)` repopulates multi-step form across sessions.

### 5.33 Concurrent Session Control
- **One Active Session** — Login from new browser/devices logs out previous session.
- **Session Regeneration** — On login; old session ID invalidated.
- **Nano Feature:** `middleware/auth.php` `requireAuth()` checks `session_id()` match.

### 5.34 Bulk Operations
- **Select-Multiple** — List views support checkbox bulk select.
- **Bulk Actions** — Delete, change status, assign to group, export selected.
- **Confirmation** — JavaScript confirmation; RBAC check per selected item.
- **Nano Feature:** `bulkDelete($ids)` issues single DELETE with `IN (:ids)` prepared statement.

### 5.35 Search Across Modules
- **Global Search** — `?q=` param indexed across clients, projects, tickets, assets.
- **Fuzzy Matching** — MySQL `MATCH(...) AGAINST(...)` or `LIKE %...%`.
- **Nano Feature:** Results grouped by module with jump links.

### 5.36 Inline Editing
- **Double-Click** to edit inline fields (client name, asset status, etc.).
- **AJAX Update** — Saves without page reload; validates via `validate()`.
- **Nano Feature:** `editInline($field, $id, $value)` JS helper.

### 5.37 Drag-and-Drop Reordering
- **List Order** — Modules with ordered lists (e.g., lookup values, COA hierarchy) support drag-and-drop reorder via JavaScript.
- **Server-Save** — On drop, AJAX call updates `order` column; `validate()` ensures numeric.
- **Nano Feature:** `updateOrder($table, $id, $newOrder)` helper.

### 5.38 Context Help & ToolTips
- **Hover Tooltips** — Key fields have `title` attributes with concise help.
- **Contextual Links** — "?" icons open relevant help centre article (knowledge base).
- **Nano Feature:** `helpTip($text)` PHP function renders `<span class="help-tooltip">...</span>`.

### 5.38 Export Templates
- **Predefined** — Invoice template, report template, export template.
- **User-Savable** — Users can save their own export configurations (column order, filters).
- **Nano Feature:** `exportTemplateSave($name, $config)` stores user template.

### 5.39 Internationalisation (i18n)
- **Hardcoded** labels in English; i18n not yet implemented but `lookup_values` can hold translations.
- **Number Formatting** — `formatMoney()` uses `localeconv()`; can be extended.
- **Nano Feature:** `?set_locale=en` URL param (future).

### 5.40 Real-Time Dashboards
- **AJAX-Powered** — Dashboard widgets refresh every 30 seconds via `setInterval`.
- **Live Data** — Pulls from `financial_years`, `tickets`, `sales` etc. without page reload.
- **Nano Feature:** `widgetRefresher($widgetId)` JS function.

### 5.41 Soft Delete
- **`deleted_at`** column on many tables; soft delete flag.
- **Restore** — Admin can restore soft-deleted records from list view.
- **Nano Feature:** `restoreSoftDelete($id)` sets `deleted_at = NULL`.

### 5.42 Version History
- **Create Audit** — Every create/edit writes a new version row (if `versioning` enabled per table).
- **Diff View** — Admin can compare two versions; highlight changed fields.
- **Nano Feature:** `getVersionHistory($table, $id)` returns array of version rows with old/new values.

### 5.43 Scheduled Maintenance Tasks
- **CLI Scripts** — `ai_automation_scheduler.php`, `erp_module_health_check.php`, `maintenance.php clean users`.
- **Cron Integration** — Can be added to system crontab; e.g., `0 * * * * php /var/www/erp/ai_automation_scheduler.php`.
- **Nano Feature:** `maintenance.php clean logs` purges `error_log` older than 30 days.

### 5.44 User Impersonation
- **Admin Feature** — Super Admin can impersonate any user (for support).
- **Session Switch** — Admin session retains `impersonating` flag; user sees "You are being impersonated" banner.
- **Nano Feature:** `setImpersonateUser($userId)` in `middleware/auth.php`.

### 5.45 API Rate Limiting (Per-Tenant)
- **`AIUsageService`** enforces per-tenant AI call quotas.
- **General Rate Limit** — Not built-in; recommended at Apache/Nginx level (`mod_ratelimit`).
- **Nano Feature:** `checkRateLimit($tenant, $limit)` returns boolean.

### 5.46 Graceful Degradation
- **Feature Toggle** — `enable_workflow_studio.php` toggle; when off, AI workflow module disabled, core ERP fully functional.
- **Offline Mode** — Core CRUD works without AI; AI services gracefully return "service unavailable" with fallback message.
- **Nano Feature:** `AIModule::isEnabled()` check before loading AI-related CSS/JS.

### 5.47 Logging Configuration
- **`php.ini` error_log** — Core logs to `error_log`; custom levels (debug, info, warning, error).
- **Structured Logs** — `logAudit()` entries include `user_id, ip, user_agent, module, action`.
- **Nano Feature:** `setLogLevel($level)` in `config/database.php` changes on the fly (runtime).

### 5.48 Data Encryption at Rest
- **Sensitive Fields** — `credit_card`, `ssn` stored via `openssl_encrypt()` with per-tenant key in `config/`.
- **Database-Level** — MySQL `AES_Encrypt`/`AES_Decrypt` via custom PDO wrapper (optional).
- **Nano Feature:** `encryptField($value, $fieldName)` / `decryptField($value)`.

### 5.49 Backup & Restore Wizards
- **CLI** — `mysqldump -u root erp_db > backup_$(date +%F).sql`.
- **GUI** — Not yet; admins use native MySQL backup tools.
- **Nano Feature:** `seed_data.php` can re-seed from a compressed backup.

### 5.50 Multi-Tenancy (Future Roadmap)
- **Not Currently Implemented** — Multi-company is via `company_id` within single DB.
- **Planned** — Separate `tenants` table, per-tenant config, isolated `document_sequences` per tenant.
- **Nano Feature** Roadmap item.

---

## 6. Security & Compliance

### 6.1 Input Validation
- **`validate()`** — Central rule engine; rejects malformed data before DB interaction.
- **Whitelist Approach** — Only known-good values allowed (e.g., status codes, lookup codes).
- **Nano Feature:** `validate($_POST, ['date'=>'required|date_format:Y-m-d'])` ensures ISO date.

### 6.2 XSS Prevention
- **`sanitize($str)`** — `htmlspecialchars($str, ENT_QUOTES, 'UTF-8')` everywhere output is injected.
- **Auto-Escaping** — Template engine (vanilla PHP) does not auto-escape; dev must call `sanitize()`.
- **Nano Feature:** `sanitize($_POST['comments'])` in every edit form output.

### 6.3 SQL Injection Protection
- **PDO Prepared Statements** — All core queries use `?` placeholders.
- **No String Concatenation** — Core code ban on `"SELECT * FROM $table"`.
- **Nano Feature:** `getDB()->prepare("SELECT * FROM table WHERE id = ?")` is the only pattern.

### 6.4 File Upload Security
- **Extension Whitelist** — Only `.pdf`, `.jpg`, `.png`, `.docx` allowed.
- **MIME Validation** — `finfo_file()` check alongside extension.
- **Rename on Upload** — `sha1(microtime().$_FILES['name'])` → prevents overwrite and path traversal.
- **Nano Feature:** `uploadFile(['pdf','jpg','png'])` returns new filename or `false`.

### 6.5 Directory Access Protection
- **`.htaccess`** — Blocks all access to `config/`, `helpers/`, `middleware/`, `templates/`, `*.sql`, `*.md`, `*.env`, `_debug/`.
- **Root .htaccess** — Also blocks direct PHP execution in `uploads/`, `assets/`.
- **Nano Feature:** Attempted `config/database.php` access returns 403.

### 6.6 Session Security
- **Cookie Flags** — `session.cookie_httponly=1`, `session.cookie_secure=1` (prod), `session.same_site=Lax`.
- **Regeneration** — `session_regenerate_id(true)` on login/logout.
- **Timeout** — Configurable via `session.gc_maxlifetime`; JS heartbeat keeps alive.
- **Nano Feature:** `middleware/auth.php` `requireAuth()` checks `session_id()` matches expected pattern.

### 6.7 Audit Log Integrity
- **Immutable** — `audit_log` table has `created_at` PRIMARY KEY; no UPDATE/DELETE allowed (only INSERT).
- **Retention** — Configurable per compliance requirement (default 7 years).
- **Nano Feature:** `logAudit($action, $table, $id)` uses `INSERT IGNORE` to guarantee append-only.

### 6.8 GDPR & Data Subject Rights
- **Export** — Admin can export all personal data for a user (GDPR export tool).
- **Anonymisation** — `anonymiseUser($userId)` replaces `email`, `phone`, `name` with placeholders.
- **Delete** — Soft delete + anonymisation path available.
- **Nano Feature:** `?gdpr=export&user_id=123` triggers CSV download of user personal data.

### 6.9 Password Policy
- **`validate()`** rules: `min:8`, `min_upper:1`, `min_lower:1`, `min_digit:1`, `regex:/(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*\d)/`.
- **Password Expiry** — Not built-in; can be added via `users` table `password_expires` column.
- **Nano Feature:** `changePassword($old, $new)` validates strength via `validate()`.

### 6.10 Two-Factor Authentication (2FA)
- **Not Yet Implemented** — Roadmap item; can be added using Google Authenticator TOTP.
- **Nano Feature** Roadmap: `users.totp_secret` column; `Authy/SMS` fallback.

### 6.11 API Authentication (Token-Based)
- **CSRF Token** — Generated per session; verified on POST/PUT/DELETE.
- **Token Format** — `csrfToken()` in `security.php`; `verifyCsrf($token)` in handler.
- **Nano Feature:** Hidden field `<input type="hidden" name="csrf_token" value="<?php echo csrfToken(); ?>">` in all forms.

### 6.12 Rate Limiting (Application-Level)
- **Not Built-In** — Recommended at web server level.
- **If Needed** — Can add Redis-based limiter in `middleware/` (future).
- **Nano Feature:** `checkAppRateLimit($key, $max, $window)` placeholder.

### 6.13 Error Message Sanitisation
- **User-Facing** — Generic messages only; technical details logged internally.
- **Nano Feature:** `errorMessage($code)` returns user-safe string; full error logged to `error_log`.

### 6.14 Secure Headers
- **`.htaccess`** sets `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy: strict-origin-when-cross-origin`.
- **Nano Feature:** `header()` calls in `includes/footer.php` for final headers.

### 6.15 Database Privilege Minimisation
- **`config/database.php`** — Uses dedicated ERP user with `SELECT, INSERT, UPDATE, DELETE` on own tables only; no `GRANT` privileges.
- **Nano Feature:** No `root` credentials in code; `getDB()` reads from config env vars.

### 6.17 Compliance Reporting
- **Audit-Ready** — All transactions have timestamp, user, IP, old/new values.
- **Exportable** — Reports can filter by date range, user, module for compliance audit.
- **Nano Feature:** `complianceReport($start, $end, $module)` generates PDF audit summary.

---

## 7. User Interface & Experience

### 7.1 Tailwind CSS & Carbon Design System
- **CDN-Loaded** — `<script src="https://cdn.tailwindcss.com"></script>` in `includes/header.php`.
- **IBM Carbon** — Colour palette, spacing, component library aligned with IBM Design System.
- **Custom Utilities** — Project-specific Tailwind classes in `assets/css/custom.css` (optional).
- **Responsive** — Mobile-first breakpoints (`sm`, `md`, `lg`, `xl`).
- **Nano Feature:** `class="hidden sm:block"` shows/hides on breakpoint.

### 7.2 Responsive Layout
- **Fluid Grid** — `max-w-7xl mx-auto` for content area; sidebar collapses to hamburger on small screens.
- **Image Handling** — `object-cover`, `max-w-full` ensures images scale.
- **Nested Tables** — Finance tables scroll horizontally on mobile (`overflow-x: auto`).
- **Nano Feature:** `?set_theme=ibm-dark` persists across responsive breakpoints.

### 7.3 Navbar
- **Brand** — ERP logo (configurable per company).
- **Company Switcher** — Dropdown of accessible companies (Super Admin sees all).
- **Currency Switcher** — Dropdown of active currencies.
- **Theme Toggle** — Light/dark switch with icon.
- **User Menu** — Name, role, logout.
- **Nano Feature:** `?set_company=5` URL param pre-selects company in switcher.

### 7.4 Sidebar
- **Hardcoded** in `templates/sidebar.php` — one `hasPermission()` gate per link.
- **Links** — Dashboard, modules (finance, hr, crm, procurement, projects, helpdesk, ai, reports), settings.
- **Collapsible** — Arrow collapse to icons; full collapse on mobile.
- **Nano Feature:** `hasPermission('ai.copilot')` shows/hides AI menu item.

### 7.5 Content Pages
- **Index/List** — Table with pagination, bulk actions, export dropdown.
- **Create/Edit** — Form with validation, old input restoration, flash messages.
- **View/Detail** — Read-only table with history, audit, version diff.
- **Nano Feature:** `old('field_name')` repopulates form after validation error.

### 7.6 Flash Message Rendering
- **Header Render** — In `includes/header.php` top-bar area.
- **CSS Classes** — `bg-green-100 text-green-800` for success, `bg-red-100 text-red-800` for error, etc.
- **Auto-Dismiss** — After 5 seconds (JS) or manual dismiss button.
- **Nano Feature:** `setFlash('success','Saved')` from any module; rendered uniformly.

### 7.7 Form Validation Display
- **Error List** — `<ul class="text-red-600">` generated from `validate()` errors.
- **Field Highlight** — Border `red-500` on invalid fields.
- **Old Input** — `old('field')` retains user input; placeholder shown if empty.
- **Nano Feature:** `saveFormState('form1')` persists across redirects.

### 7.8 Table Styling
- **Responsive Tables** — `overflow-x: auto` on `<table>`; column headers fixed.
- **Action Columns** — Edit/delete icons with `hasPermission()` check.
- **Hover Rows** — `hover:bg-gray-50` for readability.
- **Nano Feature:** `table-fixed` class sets column widths via `table-layout: fixed`.

### 7.9 Buttons & Actions
- **Primary** — `<button class="btn-primary">Save</button>` (Tailwind `bg-blue-600 text-white`).
- **Secondary** — `bg-gray-200 text-gray-800`.
- **Danger** — `bg-red-600 text-white` for delete confirmations.
- **Disabled** — `opacity-50 cursor-not-allowed`.
- **Nano Feature:** `<?= button('Save', 'modules/finance/save') ?>` helper from `redirect.php`.

### 7.10 Modals
- **Inline** — `<div class="modal">` with `aria-modal="true"`.
- **Form-in-Modal** — Create/edit forms loaded via AJAX into modal.
- **Close** — `×` button and "Esc" key.
- **Nano Feature:** `modalOpen($url, $width)` JS function.

### 7.11 Breadcrumbs
- **Horizontal** — `<nav aria-label="breadcrumb">` with `<ol class="breadcrumb">`.
- **Separators** — Tailwind `bg-gray-300 mx-1` inline-block.
- **Current Page** — Non-link last item, larger font.
- **Nano Feature:** Auto-hide on index pages (`renderBreadcrumbs([])` returns empty string).

### 7.12 Alerts & Modals
- **Success/Error/Info/Warning** — Flash messages already cover; inline alerts use same CSS classes.
- **Dismissible** — `&times` button; auto-dismiss 5s.
- **Nano Feature:** `alert('Your session will expire soon', 'warning')` JS call.

### 7.13 Data Tables (jQuery DataTables Optional)
- **Not Core** — But can be included via CDN if module requires advanced filtering/sorting.
- **Nano Feature:** `dataTableInit('#myTable')` JS init if DataTables loaded.

### 7.14 Focus Management
- **Tab Order** — Logical `tabindex` flow; `focus()` on first form field on open.
- **Error Focus** — Form validation highlights first error field and scrolls into view.
- **Nano Feature:** `scrollToError($elementId)` JS function.

### 7.15 Loading States
- **Spinners** — `class="spinner inline-block animate-spin"` during AJAX saves.
- **Button Disabled** — Submit button disabled on click; prevents double-submit.
- **Nano Feature:** `preventDoubleSubmit($btnId)` jQuery plugin pattern.

### 7.16 Notifications (Browser)
- **Desktop Notifications** — Permission prompt; used for SLA expiry, task reminders.
- **Nano Feature:** `Notification.requestPermission()` then `new Notification('Ticket SLA expiring')`.

### 7.17 Print Styles
- **`@media print`** — Hides sidebar, navbar, non-print elements; sets `page-break-after: avoid` on tables.
- **Nano Feature:** `printButton()` renders `<button class="print">Print</button>` that triggers `window.print()`.

### 7.18 Colour Contrast
- **WCAG AA** — Tailwind colour palette meets minimum contrast for text/background.
- **Custom Themes** — `ibm-light`/`ibm-dark` colours tested against contrast ratio.
- **Nano Feature:** `contrast-ratio($bg, $fg)` Sass function (if Sass installed; otherwise manual).

### 7.19 Iconography
- **Font Awesome 6.4.0** — CDN: `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0`.
- **Custom SVGs** — Module-specific icons in `assets/icons/`.
- **Nano Feature:** `<i class="fa fa-edit"></i>` used throughout; can be replaced with custom.

### 7.20 Loading Skeletons
- **Placeholder** — `class="animate-pulse bg-gray-200 rounded"` skeleton cards during data fetch.
- **Nano Feature:** `skeletonItem($height)` PHP helper renders skeleton div.

### 7.21 Toast Messages
- **Transient** — `toast('Saved successfully', 'success')` appears top-right, auto-dismiss 3s.
- **Nano Feature:** `useToast()` JS hook in Tailwind UI kit.

### 7.22 Calendar & Date Pickers
- **Vanilla JS** — `<input type="date">` native; no heavy datepicker library.
- **Range Picker** — Two native date inputs with `data-range` attribute.
- **Nano Feature:** `formatDate($date, 'd/m/Y')` PHP helper.

### 7.23 Time Input
- **`<input type="time">`** — Native HTML5; 15-min increments configurable.
- **Nano Feature:** `formatTime($datetime, 'g:i A')` helper.

### 7.24 File Management
- **Upload Zone** — Drag-and-drop area with preview; `security.php` validation.
- **Preview** — Thumbnail for images, icon for docs; clickable link to open.
- **Nano Feature:** `uploadPreview($inputId)` JS function shows preview before submit.

### 7.25 Search Highlighting
- **Global Search Results** — Matched terms highlighted with `bg-yellow-200`.
- **Nano Feature:** `highlightMatch($text, $query)` PHP function wraps matches in `<mark>`.

### 7.26 Tooltip Help
- **`helpTip($text)`** — Renders `<span class="help-tooltip">$text</span>` with question-mark icon.
- **Nano Feature:** Applied on hover of `<i class="fa fa-question-circle"></i>`.

### 7.27 Contextual Footer Actions
- **List View** — Bottom of table: "Export selected", "Bulk delete", "Change status".
- **Form View** — Save/cancel at bottom; save primary, secondary cancel.
- **Nano Feature:** `footerActions($actions)` renders button row.

### 7.28 Zero-State Illustrations
- **Empty States** — When no records found, shows illustrated empty state with CTA (e.g., "Add your first client").
- **Nano Feature:** `emptyState($title, $description, $ctaLink)` reusable component.

### 7.29 Form Step Progress
- **Multi-Step wizards** — Shows step number/name (1 of 3, 2 of 3, 3 of 3).
- **Nano Feature:** `stepProgress($current, $total)` renders progress bar.

### 7.30 Drag-and-Drop File Upload
- **Zone** — Drop area; preview; upload on submit or auto-upload.
- **Progress Bar** — Visual upload progress.
- **Nano Feature:** `jQuery Form Plugin` (already dependency-free; uses XHR).

### 7.31 Cookie Consent Banner
- **Top Bar** — `"We use cookies. [Accept]"`. Persists via localStorage.
- **Nano Feature:** `checkCookieConsent()` on page load; hides banner if accepted.

### 7.32 Language Selector (Future)
- **Not Implemented** — But `locale` URL param `?set_locale=en` can be added.
- **Nano Feature** Roadmap.

### 7.33 Touch Friendly
- **Buttons** — Minimum 44px height for touch.
- **Nav Links** — Spacing > 8px between touch targets.
- **Nano Feature:** `class="p-4"` ensures adequate touch padding.

### 7.34 Error Page branding
- **404/500** — Custom error pages with brand colours, Home link, Support contact.
- **Nano Feature:** `error404()` / `error500()` in `middleware/` return consistent response.

### 7.35 Keyboard Shortcuts
- **Global** — `?` focuses global search, `/` focuses search input, `Esc` closes modals/menus.
- **Module-Specific** — `Ctrl+S` saves form (if enabled), `Ctrl+Shift+E` exports current view.
- **Nano Feature:** `registerHotkey($key, $callback)` JS utility.

### 7.36 Language Redirection
- **`?set_language=en`** — Not yet implemented; URL param skeleton present.
- **Nano Feature** Roadmap.

### 7.37 Sitemap/SEO
- **Meta Tags** — Each page can set `<title>`, `<meta name="description">` via `$pageTitle` variable.
- **Nano Feature:** `setPageTitle($title)` in module index.php sets page title.

### 7.38 Notification Drawer
- **Inbox-Style** — Click notification icon; drawer slides down with alerts, friend requests, system messages.
- **Nano Feature:** `notificationCount` badge on icon; `markAllRead()` API.

### 7.38 User Onboarding Tour
- **Intro.js** — Optional guided tour on first login (steps highlight key UI elements).
- **Nano Feature:** `startOnboarding()` call in `includes/header.php` if `$_SESSION['first_login']`.

### 7.38 Responsive Image Sizes
- **`srcset`** — ` <img srcset="…">` for different resolutions; prevents heavy images on mobile.
- **Nano Feature:** `responsiveImage($path)` helper generates `<img>` with srcset.

### 7.38 Loading Indicator Overlays
- **Full-Page** — `class="fixed inset-0 bg-black/30 flex items-center justify-center z-50"` during AJAX calls.
- **Nano Feature:** `showLoading($message='Loading…')` / `hideLoading()` JS pair.

### 7.39 Accessibility (a11y)
- **ARIA Labels** — All interactive elements have `aria-label` or meaningful text.
- **Color Contrast** — Verified per WCAG AA.
- **Focus Indicators** — `outline` utilities visible.
- **Nano Feature:** `a11yAlert($message)` adds `<div role="alert">`.

### 7.40 Progressive Enhancement
- **Core CRUD** works without JavaScript; JS enhances (inline edit, modals, animations).
- **Nano Feature** — No `degrad`; PHP falls back gracefully.

### 7.41 Responsive Utilities
- **`hidden sm md lg xl`** — Show/hide at breakpoints.
- **`block sm:inline`** — Inline at medium+.
- **Nano Feature:** Utility-first Tailwind classes everywhere.

### 7.41 Page Transition Animations
- **Fade/Slide** — Simple CSS transitions on page load; `transition duration-300`.
- **Nano Feature:** `transition-all` class on main content wrapper.

### 7.42 Measurement & Display of Financial Data
- **`formatMoney()`** — `$ 1,234.56` or `€ 1.234,56` locale-based.
- **Currency Symbol** — From `currencies` table `symbol` field.
- **Nano Feature:** `formatMoney(1234.56, 'USD')` → `$1,234.56`.

### 7.43 Date/Time Display
- **`formatDateTime($datetime)`** — `2026-10-19 14:30` or `19 Oct 2026, 2:30 PM`.
- **Timezone** — User session timezone; defaults to server `UTC`.
- **Nano Feature:** `timeAgo($datetime)` → "2 hours ago", "3 days ago".

### 7.44 Bulk Operation Confirmations
- **Delete** — JS `confirm("Delete 5 items?")`; if confirmed, AJAX bulk delete.
- **Status Change** — Inline select with immediate save; no confirmation needed for simple status.
- **Nano Feature:** `bulkConfirm($count, $action)` JS function.

### 7.45 Export Wizards
- **Column Selector** — Checkbox list of columns to include.
- **Filter Pre-fill** — Current page filters carried over to export.
- **Nano Feature:** `exportWizard($table, $filters)` renders modal with column picker.

### 7.46 Inline Script Management
- **Inline PHP** — Allowed only in `includes/` and module files; no `eval()`.
- **Nano Feature:** `esc($str)` = `htmlspecialchars($str, ENT_QUOTES, 'UTF-8')`.

### 7.47 Session Data Debug (Dev Only)
- **`?debug=session`** — Displays `$_SESSION` array (blocked in production by `.htaccess`).
- **Nano Feature** Developer only.

### 7.48 Dynamic Module Loading
- **AJAX Module Load** — `loadModule('finance/index')` fetches content without full page reload.
- **Nano Feature** — Used in dashboard widgets.

### 7.48 Error Inline Inline
- **Inline Validation** — Real-time on `blur` or `input` events; shows error message next to field.
- **Nano Feature:** `liveValidate($formId)` JS plugin using `validate()` rules.

### 7.48 Lazy Loading Images
- **`loading="lazy"`** — On all `<img>` tags above-the-fold not present; added via PHP helper.
- **Nano Feature:** `<php echo lazyImage($path); ?>`.

### 7.48 Reduced Motion Respect
- **`@media (prefers-reduced-motion: reduce)`** — Disables spinners, animations for users who set this preference.
- **Nano Feature:** `spinnerClass()` returns reduced-motion-safe class.

### 7.49 Notification Emails (Outgoing)
- **Not Built-In** — But `security.php` `logAudit()` can trigger external SMTP via composer `phpmailer/phpmailer` (optional).
- **Nano Feature** Roadmap: `sendNotificationEmail($to, $subject, $view, $data)`.

### 7.50 QR Code Generation
- **Not Core** — Can add composer `bacon/bcode` if needed.
- **Nano Feature** Roadmap: `qrCode($data)` for invoice links, asset tags.

### 7.51 Localization Placeholders
- **`__('Add Client')`** — i18n placeholder (not implemented; can be added via language files).
- **Nano Feature** Roadmap.

### 7.52 Dynamic Favicon Based on Theme
- **`<link rel="icon" href="…">`** — Changes `href` on theme switch via JS.
- **Nano Feature:** `switchTheme($theme)` updates favicon URL.

### 7.53 Split View (Dashboard)
- **Two-Column** — Dashboard widgets side-by-side on lg+; single column on sm.
- **Nano Feature:** `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3` Tailwind.

### 7.54 Context Menu (Right-Click)
- **On Tables/Rows** — Right-click reveals "Edit", "View", "Delete", "Export".
- **Nano Feature:** `contextMenu($menuId)` JS plugin.

### 7.55 Data Grid with Frozen Columns
- **Left Columns Frozen** — First 2 columns (e.g., Date, Document #) stay visible on horizontal scroll.
- **Nano Feature:** `table-freeze-2` CSS class.

### 7.56 Quick Create Floating Button
- **`+`** — Fixed bottom-right; opens create form modal.
- **Nano Feature:** `floatingCreateButton($route)` JS helper.

### 7.56 Toaster (Snackbar) Messages
- **Bottom-Trailing** — “Message sent” appears bottom-right, auto-hide 3s.
- **Nano Feature:** `useSnackbar()` JS hook.

### 7.56 Floating Labels
- **Form Inputs** — Label floats above on focus or has value.
- **Nano Feature:** `floatingLabel($inputName)` CSS class.

### 7.57 Input Masks
- **Phone, VAT, Date** — `inputmask` jQuery plugin (optional, not core).
- **Nano Feature** Roadmap: vanilla JS masks via `inputmode` and `pattern`.

### 7.58 Autocomplete for Select Fields
- **Type-Ahead** — As user types, list of matching options from lookup table.
- **Nano Feature:** `autocompleteLookup($table, $field)` JS function.

### 7.59 Row Selection with Checkboxes
- **Bulk Actions** — Top-of-table checkbox selects all on page; individual row checkboxes.
- **Nano Feature:** `selectAllToggle($table)` JS.

### 7.60 Drag-and-Drop Row Reordering (Lists)
- **Orderable Lists** — e.g., lookup values, task list reorder.
- **Nano Feature:** `SortableJS` integration (`<script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0"></script>`).

### 7.61 Collapsible Fieldsets
- **`<fieldset>`** with `legend` and `class="collapsed"`; JS toggles visibility.
- **Nano Feature:** `collapsibleFieldset($legend)` helper.

### 7.62 Stepper Progress Bar
- **Multi-Step Form** — Shows progress 20%/40%/60%/80%/100%.
- **Nano Feature:** `stepperBar($steps, $current)` renders SVG/HTML progress.

### 7.63 Notification Preferences
- **Per-User** — User can opt-in/out of email notifications for tickets, reports, etc.
- **Nano Feature** Roadmap: `users.notification_prefs` table.

### 7.64 Lazy Loading Panels
- **Accordion/Collapse** — Panels load content on toggle (AJAX) to reduce initial page weight.
- **Nano Feature:** `collapseLoad($url)` JS function.

### 7.65 Tooltip with HTML Content
- **Rich Tooltips** — Can render small tables, lists inside tooltip on hover.
- **Nano Feature:** `tooltipHTML($html)` JS option.

### 7.66 Dashboard Widget Collapsible
- **Collapse/Expand** — Each widget can be collapsed to minimize; persists per user.
- **Nano Feature:** `widgetCollapseToggle($widgetId)` JS.

### 7.67 Page Speed Optimisations
- **Critical CSS** — Inline above-the-fold CSS in `header.php`; rest in external `.css`.
- **Nano Feature** — `preload` links for key images.

### 7.68 Responsive Embed (Videos)
- **`aspect-ratio-16/9`** — For embedded videos (e.g., training, demos).
- **Nano Feature:** `responsiveVideo($url)` helper.

### 7.69 Overlay Loading Skeleton
- **Full-Page Skeleton** — During initial load, shows skeleton of header, sidebar, main content.
- **Nano Feature:** `pageSkeleton()` renders skeleton markup.

### 7.69 Floating Labels
- **`label-floating`** CSS class; label animates up on focus.
- **Nano Feature:** Applied globally via Tailwind base.

### 7.70 Input Groups with Icons
- **`input-group`** — Username/email with prefix icon (lock, user).
- **Nano Feature:** `inputGroup($label, $type)` helper.

### 7.71 Validation Summary Panel
- **Top of Form** — If validation fails, panel lists all errors before field errors.
- **Nano Feature:** `validationSummary($errors)` renders `<div class="alert">`.

### 7.72 Form Redo/Undo
- **LocalStorage** — User can Ctrl+Z/Ctrl+Y form changes within session.
- **Nano Feature** Roadmap: `localStorageForm($formId)`.

### 7.73 Split Pane Resizer
- **Dashboard Widgets** — User can drag separator to resize adjacent widgets.
- **Nano Feature:** `resizableSplitPane($element)` JS.

### 7.74 Theme Variations (Beyond Light/Dark)
- **High-Contrast** — Optional `high-contrast` class for visually impaired.
- **Nano Feature** Roadmap.

### 7.75 Semantic HTML
- **`header`, `nav`, `main`, `section`, `article`, `footer`** — Proper hierarchy; improves SEO and a11y.
- **Nano Feature:** All module `index.php` wrap content in `<main>`.

### 7.76 Meta Tag Manager
- **Per-Page** — `<title>`, `description`, `keywords`, `robots` set per module.
- **Nano Feature:** `setMeta($name, $content)` in module layout.

### 7.77 Skip Links
- **`#main-content`** — Top-of-page link for keyboard navigators; hidden visually, focusable.
- **Nano Feature:** `<a href="#main-content" class="skip-link">Skip to main content</a>` in `header.php`.

### 7.78 Responsive Tables with Summary
- **`<table summary="…">`** — Describes table purpose for screen readers.
- **Nano Feature:** `tableSummary($description)` helper.

### 7.79 Animated Page Transitions
- **Fade/Slide** — `.5s` transitions on `navigate` event (SPA-like).
- **Nano Feature:** `pageTransition()` JS.

### 7.80 Accessible Modal Dialogs
- **`role="dialog"`** + `aria-modal="true"` + focus trap + ESC to close.
- **Nano Feature:** `accessibleModal($title, $content)` helper.

### 7.81 Live Region Announcements
- **`aria-live="polite"`** — Announces dynamic content changes (form validation, toast).
- **Nano Feature:** `liveRegion($message)` JS function.

### 7.82 Responsive Grid Gaps
- **`gap-4`** `gap-6` etc. — Consistent spacing across breakpoints.
- **Nano Feature:** `gap-y-8` for vertical rhythm.

### 7.83 Consistent Spacing Scale
- **Tailwind** — `p-1` to `p-6`, `m-0` to `m-8`; 4px base unit.
- **Nano Feature:** `space-y-4` between form fields.

### 7.84 Focus Ring Utilities
- **`focus-visible`** — Visible focus only for keyboard users (not mouse click).
- **Nano Feature:** `focus-visible:ring-2 focus-visible:ring-blue-500`.

### 7.85 Table Header Fixed
- **`table-fixed`** + `th { table-layout: fixed; }` — Column widths set; content overflows.
- **Nano Feature:** Applied on financial tables.

### 7.86 Inline Error Messages
- **`error-message`** class below field; disappears on success.
- **Nano Feature:** `validationError($fieldName)` PHP.

### 7.87 Conditional Field Visibility
- **Show/hide** fields based on other field values (e.g., "Show VAT fields if VAT registered").
- **Nano Feature:** `conditionalRender($condition, $fieldHtml)` PHP.

### 7.88 Dynamic Form Sections
- **Add/Remove** field groups dynamically (AJAX).
- **Nano Feature:** `addRemoveGroup($groupName)` JS.

### 7.89 Dependent Dropdowns
- **Cascade** — Country → State/Region → City; populated from lookup tables.
- **Nano Feature:** `cascadeSelect($parent, $child)` JS.

### 7.90 Date Range Pickers
- **Two Native Inputs** — With `data-range="true"`; JS calendar picker (lightweight chosen).
- **Nano Feature:** `dateRangeInit($fromId, $toId)`.

### 7.91 Export Including Grouped Data
- **Export** can group by column (e.g., group invoices by client).
- **Nano Feature:** `exportGrouped($table, $groupBy)` PHP.

### 7.92 Sidebar Mega Menus (Future)
- **Not Implemented** — Currently flat list; future roadmap.
- **Nano Feature** Roadmap.

### 7.93 Toolbar for Rich Text (If WYSIWYG Enabled)
- **Not Core** — Can add TinyMCE or CKEditor if module requires rich text.
- **Nano Feature** Roadmap.

### 7.94 Sticky Table Headers
- **`sticky-header`** — Table header stays on scroll.
- **Nano Feature:** `class="sticky top-0"` on `<thead>`.

### 7.97 Tooltip with Auto-Hide
- **`data-tooltip`** — Hover shows, auto-hide after 2s inactivity.
- **Nano Feature:** `$('[data-tooltip]').tooltip();`.

### 7.98 Accessible Tab Panels
- **`role="tablist"`** + `role="tab"` + `aria-controls` — For accordion-style content.
- **Nano Feature:** `accessibleTabs($tabs)` helper.

### 7.99 Live Search As User Types
- **Debounced** — 300ms debounce; shows results below search bar.
- **Nano Feature:** `liveSearch($url, $inputId)`.

### 7.99 Sticky Sidebar
- **`sticky-sidebar`** — Sidebar stays visible on main content scroll (when space allows).
- **Nano Feature:** `class="sticky left-0 top-20"` on sidebar.

### 7.99 Page Loading Progress Bar
- **`<n-bar`** — Top progress bar during page load (Turbolinks-like).
- **Nano Feature:** Include `<div class="fixed inset-0 z-10 bg-blue-600" id="page-progress"><div class="h-full w-0 transition-width duration-300 bg-white"></div></div>` in `header.php`.

### 7.100 Error Boundary (React-Style Not Applicable)
- **PHP Error Handling** — As described; no client-side framework.
- **Nano Feature** — Custom error pages.

---

## 8. Integration & Extensibility

### 8.1 API Endpoints (Comprehensive List)
The ERP exposes a wide REST-like API surface (implemented as PHP files in `modules/ai/api/` and core modules). Key endpoint categories:

- **Agents** (`modules/ai/api/agents.php`) — CRUD and task dispatch for AI agents.
- **Tasks** (`modules/ai/api/tasks.php`) — Submit AI jobs, poll status, cancel.
- **Workflows** (`modules/ai/api/workflows.php`) — Define and execute AI workflows.
- **Knowledge** (`modules/ai/api/knowledge.php`) — Upload, search, manage knowledge base articles.
- **Chat** (`modules/ai/api/chat.php`) — Session-based conversational AI.
- **Copilot** (`modules/ai/api/copilot.php`) — High-level copilot routing with context.
- **Management** (`modules/ai/api/management.php`) — Tenant AI settings, provider config.
- **Governance** (`modules/ai/api/governance.php`) — Policy rules, redaction, audit.
- **Integrations** (`modules/ai/api/integrations.php`) — Provider credential management.
- **Analytics** (`modules/ai/api/analytics.php`) — AI usage metrics, cost, latency.
- **Process Intelligence** (`modules/ai/api/process_intelligence.php`) — Custom AI process orchestration.
- **Workspaces** (`modules/ai/api/workspaces.php`) — Tenant isolation for AI data.
- **Observability** (`modules/ai/api/observability.php`) — Logging, tracing, error tracking.

Each endpoint uses `getDB()` PDO prepared statements and follows the pattern:
```php
$stmt = $db->prepare("SELECT * FROM table WHERE id = ?");
$stmt->execute([$param]);
$result = $stmt->fetchAll(PDO::FETCH_ASSOC);
```

### 8.2 Webhook Support
- **Configurable** per module (e.g., new ticket webhook, payment received).
- **URL** stored per tenant; POSTed with payload containing record ID, action, timestamp.
- **Authentication** — Shared secret verified in webhook handler; `verifyCsrf()` pattern adapted for inbound.
- **Nano Feature:** `setupWebhook($module, $url, $secret)` CLI command.

### 8.3 Module Registration
- **Manual** — No auto-discovery; admin adds:
  1. Module directory in `modules/`.
  2. CRUD files (`index.php`, `create.php`, `edit.php`, `view.php`, `delete.php`).
  3. Permission entries in `permissions` table (e.g., `module_name.action`).
  4. Menu link in `templates/sidebar.php` (gated by `hasPermission()`).
- **Nano Feature:** `registerModule($name, $permissions)` helper (future).

### 8.4 Migration System
- **Idempotent PHP Files** in `config/migrations/` (e.g., `2026_10_12_customer_master.php`).
- **Each Migration** queries `information_schema` before `ALTER TABLE`/`CREATE TABLE`; safe to re-run.
- **Ordering** — Run in lexical order; no tracking table; manual sequencing required.
- **Nano Feature:** `php config/migrations/2026_10_12_xxx.php` runs single migration.

### 8.5 Seed Data
- **`config/seed_data.php`** — Populates sample data (companies, users, lookup values, etc.).
- **Runs via** `php setup.php` (dashboard widget) or CLI.
- **Nano Feature:** `seed_data.php` can be re-run; idempotent checks before insert.

### 8.6 Configuration Files
| File | Purpose |
|---|---|
| `config/database.php` | PDO singleton; local/prod auto-detect via `SERVER_NAME`. |
| `config/widgets.php` | Widget registry, per-user dashboard layout. |
| `config/seed_data.php` | Sample data (companies, users, lookup values). |
| `config/migrations/` | Idempotent migration PHP files. |
| `ai/config/ai_central_config.php` | Central AI config: provider keys, model names, defaults. |
| `config/runner.php` | Exposes `applySql()` helper; not a full runner. |

### 8.7 Extensibility Points
- **New Modules** — Add directory, CRUD, permissions, menu link.
- **New Lookup Types** — Insert into `lookup_types`, `lookup_values`; no code change.
- **New AI Service** — Create class in `modules/ai/services/`, register in `ai_central_config.php`, add API endpoint.
- **New Lookup** — `lookup.php` `lookupOptions($type)` auto-reads from DB.
- **Custom Reports** — Users can save report templates; admins can add report queries in `reports/` folder.

### 8.8 Third-Party Integration Patterns
- **CSV Import/Export** — All modules support CSV upload (column mapping screen).
- **JSON API** — Internal API; external systems can call via `/erp/api/...` (if reverse proxy added).
- **SFTP** — Uploads via `uploads/`; external system can SFTP drop files; module can `importFile($path)`.
- **Zapier/Make** — Can webhook to ERP URL; ERP webhook can trigger create/update.
- **Nano Feature:** `importCsv($filePath, $module)` helper maps columns to DB fields.

### 8.9 Plugin Architecture (Conceptual)
- **Not Currently Implemented** — ERP designed as monolithic zero-dependency PHP app.
- **Future** — Composer package `erp/module-*` could be added; but current design favours direct code addition.
- **Nano Feature** Roadmap: `erp-plugins` repo.

### 8.10 Environment Configuration
- **`.htaccess`** prevents access to `.env` and config files.
- **`config/database.php`** reads from `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS` constants defined in `.env` (not committed).
- **`SERVER_NAME`** auto-detection means local dev uses local credentials; production uses prod credentials.
- **Nano Feature:** `?db=test` URL param (dev only) switches DB for testing.

### 8.11 API Versioning (Planned)
- **Not Yet Implemented** — Current API is version-agnostic; backward compatibility via feature flags.
- **Nano Feature** Roadmap: `/api/v1/...` prefixes.

### 8.12 Deprecation & Version Removal
- **Feature Flags** — `enable_workflow_studio.php` toggle; when off, module disabled but code remains.
- **Nano Feature:** `deprecateFeature($name)` sets `config/feature_flags.php` entry; UI greyed out.

### 8.13 Custom Fields (EAV)
- **Not Core** — But `chart_of_accounts` allows free-form description; ad-hoc columns can be added to tables (via migration) if needed.
- **Nano Feature** Roadmap: EAV schema for flexible attributes.

### 8.14 Bulk Import/Export Templates
- **Template Download** — Users can download CSV template for module (pre-filled column headers).
- **Map on Upload** — User maps CSV columns to DB fields; `validate()` runs on each row.
- **Nano Feature:** `downloadCsvTemplate($module)` generates header-only CSV.

### 8.15 Data Validation Rules Repository
- **`validation.php`** rules are hardcoded; new rules can be added as PHP functions; registered in `validate()` switch.
- **Nano Feature:** `addValidationRule($name, $callable)` for dynamic rules.

### 8.16 Audit Log Export Formats
- **PDF**, **Excel**, **CSV** — Same as other reports; filtered by date, user, module.
- **Nano Feature:** `exportAuditLog($start, $end, $format)` generates file.

### 8.17 Session Data Migration on Upgrade
- **On New Install** — Fresh session; no migration needed.
- **On Upgrade** — `session_regenerate_id()` recommended; old session data discarded (expected).
- **Nano Feature:** `upgrade.php` script (future).

### 8.18 Multi-Language UI Placeholders
- **`__('Save')`** — Placeholder for future translation files (`.php` arrays returning `['Save' => 'Salvar']`).
- **Nano Feature** — Not implemented; English-only UI currently.

### 8.19 Configurable Number Formats
- **`formatMoney($amount, $currencyCode)`** — Uses `localeconv()` under i18n not active; can be extended.
- **Nano Feature:** Accepts `$locale` param for future.

### 8.20 Theme Inheritance (Child Themes)
- **Not Implemented** — `ibm-light`/`ibm-dark` are core themes; customisation via CSS overrides.
- **Nano Feature** Roadmap: child theme `extends ibm-dark`.

### 8.21 Query Builder (Optional)
- **Not Core** — Raw PDO prepared statements used; simple query builder can be added via helper.
- **Nano Feature** Roadmap: `db()->where()->get('table')` style.

### 8.22 Caching Layer (Optional)
- **`file_put_contents`/`get`** — For static reports, dropdown values; not required for core ERP.
- **Nano Feature** Roadmap: `cache()->remember($key, $ttl, $callback)`.

### 8.23 Rate Limiting (Application-Level) (Revisited)
- **Redis-Based** — Can add `RedisRateLimiter` class; used by AI services (`AIUsageService`).
- **Nano Feature:** `rateLimitCheck($key, $max, $minutes)`.

### 8.24 Error Tracking (Sentry-like)
- **Not Integrated** — But `logAudit()` and `error_log` capture errors; can integrate Sentry via composer if needed.
- **Nano Feature** Roadmap: `Sentry\init()` in `bootstrap.php`.

### 8.25 Logging Destinations
- **`error_log`** — Core; can add `Monolog\Logger` if desired.
- **Nano Feature:** `logDestination($msg, $target)` (file, db, email).

### 8.25 Session Crash Protection
- **`session_start()`** — wrapped in `try {}`; if crash, login required again.
- **Nano Feature:** `requireAuth()` redirects to login on session error.

### 8.25 API Throttling (Per-IP)
- **Not Built-In** — Can add `.htaccess` `SetEnvIf Remote_addr` + `Deny from` or Nginx `limit_req_zone`.
- **Nano Feature** Roadmap.

### 8.25 Data Archiving Scripts
- **`maintenance.php clean`** — Purges old records based on `retention_days` column (if present).
- **Nano Feature:** `maintenance.php clean audit_log` retains 7 years then deletes.

### 8.25 Backup Verification Scripts
- **`check_tables.php`** — Verifies all tables exist, have expected columns; reports mismatches.
- **Nano Feature:** Run after DB restore.

### 8.25 Kill Switch (AI Emergency)
- **`AIKillSwitchService.php`** — Single call disables all AI; used for safety incidents.
- **Nano Feature:** `AIKillSwitchService::trigger()` logs event, sets `ai_enabled = 0` in config.

### 8.25 Usage Quota Enforcement
- **`AIUsageService`** — Tracks tokens, calls, cost; auto-blocks when quota exceeded.
- **Nano Feature:** Dashboard widget shows "AI usage this month: 45% of 10,000 tokens".

### 8.26 Performance Metrics Collection
- **`AIMetricRegistry`** — Collects latency, success rate, error count per service; exposed at `/ai/metrics`.
- **Nano Feature:** Prometheus scrape endpoint.

### 8.27 Data Retention Policies
- **Per-Table** — Configurable via `retention_days` column; `maintenance.php clean` respects.
- **Nano Feature:** `setRetention($table, $days)` CLI.

### 8.28 Session Fixation Protection
- **`session_regenerate_id(true)`** on login; invalidates old session ID.
- **Nano Feature:** Always executed in `middleware/auth.php` login handler.

### 8.29 Input Sanitisation Whitelist
- **`security.php`** `sanitize()` uses `htmlspecialchars` with `ENT_QUOTES`; whitelist approach for allowed HTML (if any) via `strip_tags()`.
- **Nano Feature:** `sanitize($str, ['a','b','c'])` allows only those tags.

### 8.29 URL Rewriting Rules (`.htaccess`)
- **Clean URLs** — `RewriteEngine On`, `RewriteCond %{REQUEST_FILENAME} !-d/`, `RewriteRule ^([^/]+)/?$ $1.php [NC,L]`.
- **Block Sensitive** — `RewriteCond %{REQUEST_URI} ^(config|helpers|middleware|templates|.*\\.sql|.*\\.md|.*\\.env|_debug) [NC,R=0,L]`.
- **Nano Feature:** No `?q=` param needed; module auto-detected.

### 8.30 Session Cookie Settings
- **`session.cookie_httponly=1`**, `session.cookie_secure=1` (prod), `session.same_site=Lax`.
- **Nano Feature:** Set in `config/database.php` `ini_set()` calls.

### 8.31 Form Token Renewal
- **CSRF token** regenerated on each form render (`csrfToken()`); old token invalid on submit.
- **Nano Feature:** `<input name="csrf_token">` always fresh.

### 8.32 Error Page SEO
- **404** — Returns `404` status, custom message, Home link, sitemap reference.
- **500** — Returns `500` status, generic message, log reference.
- **Nano Feature:** `status_header($code)` in `includes/header.php`.

### 8.33 URL Canonicalisation
- **`?set_theme=`, `?set_company=`, `?set_currency=`** — All accepted; canonical URL is without params (SEO).
- **Nano Feature:** `canonicalUrl()` helper outputs `<link rel="canonical">`.

### 8.33 Pagination Accessibility
- **`aria-label`** on pagination links: `aria-label="Page 3 of 10"`.
- **Nano Feature:** `paginationLinks()` adds aria labels.

### 8.34 Inline Image Editing
- **Double-Click** to replace inline image; preview before save.
- **Nano Feature:** `inlineImageUpload($fieldId)` JS.

### 8.35 Toast Notification Persistence
- **User Can Pin** — Important toasts can be pinned to drawer; auto-dismiss after 24h for non-pinned.
- **Nano Feature** Roadmap.

### 8.36 Dynamic Help Link per Page
- **`?help=topic_name`** — Opens knowledge base article in side panel.
- **Nano Feature:** `helpLink($topic)` renders `<a>` with `data-help` attr.

### 8.37 Session Data Portability
- **Export/Import** — Admin can export session data (for debugging) and import on another server.
- **Nano Feature** Roadmap.

### 8.37 CSV Charset Handling
- **UTF-8** — All CSV import/export forced UTF-8; `mb_convert_encoding` on read/write.
- **Nano Feature:** `csvEncode($array)` / `csvDecode($string)`.

### 8.38 Accessibility Audit Tools
- **`npm audit`** — Not used; manual a11y testing with WAVE axe.
- **Nano Feature** Roadmap: integrate `eslint-plugin-jsx-a11y` if React added.

### 8.37 Multi-Company Financial Consolidation Reports
- **`YearEndClosingService`** — Generates group P&L, balance sheet, cash flow with intercompany eliminations.
- **Nano Feature:** `consolidationReport($startDate, $endDate)` PDF generation.

### 8.38 AI Service Discovery
- **`AIModule::listServices()`** — Returns array of service class names from `ai_services` config.
- **Nano Feature:** Used by UI to show available AI features.

### 8.39 Configurable Dashboard Widget Limits
- **Max 20 widgets** per user; per-widget memory limit 1 MB.
- **Nano Feature:** `widgetMemoryLimit($id)` checks before load.

### 8.39 Export Preview Before Download
- **User Can Preview** — PDF/Excel preview in browser before download.
- **Nano Feature:** `exportPreview($data, $format)` renders mini-preview canvas.

### 8.40 Audit Log Searchable Fields
- **`user_id, table_name, record_id, action, ip_address, created_at`** — Searchable via admin UI.
- **Nano Feature:** `searchAudit($filters)` PHP function.

### 8.41 Flash Message Colours Mapped to Types
- **success** → green-100/green-800
- **error** → red-100/red-800
- **info** → blue-100/blue-800
- **warning** → amber-100/amber-800
- **Nano Feature:** `flashClass($type)` returns Tailwind class string.

### 8.42 Form Field Order Preservation
- **User Can Drag** to reorder fields on create/edit form (via AJAX).
- **Nano Feature:** `reorderFields($formId)` JS.

### 8.43 Inline Search Highlight Persistence
- **Search term stays** in input field after results shown, for refinement.
- **Nano Feature:** `retainSearchTerm()` JS.

### 8.43 Tooltip Delay
- **`data-delay="500"`** — Tooltip shows after 500ms hover; avoids flicker.
- **Nano Feature:** `$('[data-tooltip]').tooltip({delay: {show: 500, hide: 100}});`.

### 8.44 Form Validation On Submit Only
- **`validateOnSubmit=true`** — Default; can set `validateOnBlur=true` for real-time.
- **Nano Feature:** `validateOnBlur` flag in form init.

### 8.45 Dynamic Module Badges
- **New/Updated** — Badge on module menu indicating new features or updates.
- **Nano Feature:** `moduleBadge($name, $status)` PHP.

### 8.46 Session Timeout Warning
- **JS Countdown** — "Your session will expire in 2 minutes"; button to extend.
- **Nano Feature:** `sessionTimeoutWarning($seconds)` JS.

### 8.47 Breadcrumbs Depth Limit
- **Max 5 levels** — Deeper nesting hidden with `···` ellipsis.
- **Nano Feature:** `renderBreadcrumbs` truncates.

### 8.47 Search Highlight Persistence Across Pages
- **`?q=` persists** in URL for sharing search results.
- **Nano Feature:** `persistSearchParam()` JS.

### 8.48 Responsive Field Legends
- **`<legend>`** in fieldsets wraps on narrow screens; `class="w-full text-sm"`.
- **Nano Feature:** `fieldsetLegend($legend)` CSS.

### 8.48 Smooth Scroll for Anchor Links
- **`scroll-behavior: smooth`** on `html`; anchor links smooth scroll.
- **Nano Feature:** Added in `includes/header.php` `<style>`.

### 8.48 Toggle Switch for Settings
- **`role="switch"`** — Light/dark, enabled/disabled.
- **Nano Feature:** `toggleSwitch($name, $checked)` HTML + JS.

### 8.48 Tooltip with Direction Control
- **`data-placement="top|bottom|left|right"`** — Tooltip orientation.
- **Nano Feature:** `$('[data-tooltip]').tooltip({placement: 'top'});`.

### 8.48 Collapsible Navigation on Mobile
- **Sidebar** → hamburger; drawer slides from left.
- **Nano Feature:** `mobileSidebarToggle()` JS.

### 8.48 Page Load Spinner with Text
- **`class="spinner text-center"`** — Shows "Loading..." centre.
- **Nano Feature:** `showLoading('Saving…')` / `hideLoading()`.

### 8.48 Form Redraw on Validation Failure
- **All fields** re-render with `old()` input and error list; no data lost.
- **Nano Feature:** `redrawForm($view)` in edit.php.

### 8.48 Dynamic Meta Tags for Share
- **When sharing link on social**, `og:title`, `og:description`, `og:image` pulled from page meta.
- **Nano Feature:** `setOgTags($title, $desc, $img)` in module layout.

### 8.48 Inline Error Summary
- **If one field errors**, error summary at top of form also lists that field.
- **Nano Feature:** `inlineErrorSummary($errors)` renders compact list.

### 8.48 Notification Sound (Optional)
- **Soft 'ding'** on new ticket, SLA expiry (user can disable).
- **Nano Feature** Roadmap: `playSound('ding')` JS.

### 8.48 Responsive Z-Index Management
- **Dropdowns, Modals** — Z-index scales with breakpoints; `z-10`, `z-20`, `z-30`.
- **Nano Feature:** `z-index-above($base)` helper.

### 8.48 Skeleton Loaders for Cards
- **`class="animate-pulse bg-gray-100 rounded-lg h-64"`** — During data fetch.
- **Nano Feature:** `skeletonCard($height)` helper.

### 8.48 Tooltip with Hover Intent
- **Delay before show** to avoid accidental triggers; `data-intent="true"`.
- **Nano Feature:** `$('[data-tooltip]').tooltip({intent: true});`.

### 8.48 Sticky Header on Scroll
- **`class="sticky top-0 z-50"`** — Header remains visible when main content scrolls.
- **Nano Feature:** Applied on `navbar.php`.

### 8.48 Form Field Validation Delay
- **`validate()`** runs on `submit`; can set `validate_on` = `blur|change|submit`.
- **Nano Feature:** `validateOn($event)` in form init.

### 8.49 Accessible Modal Focus Trap
- **When modal opens** focus trapped within; ESC closes; focus returns on close.
- **Nano Feature:** `focusTrapModal($modalId)` JS.

### 8.49 Page Preshave (Pre-loader)
- **`#page-preloader`** — Spinner over full page until DOM ready; then fade out.
- **Nano Feature:** `<div id="page-preloader" class="fixed inset-0 z-50 flex items-center justify-center bg-white">...</div>` in `header.php`.

### 8.49 Form Fieldset Legends Float
- **Legend floats** above on focus/value; improves mobile usability.
- **Nano Feature:** `fieldset-legend-float` CSS class.

### 8.49 Dynamic Footer Copyright
- **`date('Y')`** — Auto-updates year in footer copyright.
- **Nano Feature:** `footerCopyright($startYear=2026)` renders `© 2026 ERP System`.

### 8.49 Modal with Scrollable Content
- **If content overflows** modal height, inner scrollbar appears; outer fixed.
- **Nano Feature:** `modalMaxHeight($px)` caps height.

### 8.50 Page Transition on Navigation
- **When clicking internal links**, page fades out/in (SPA feel).
- **Nano Feature:** `navigo.js` (lightweight router) with transition plugin.

### 8.50 Tooltip with Follow Cursor
- **`data-placement="follow"`** — Tooltip follows mouse within container.
- **Nano Feature:** `tooltipFollow($element)` JS option.

### 8.50 Accessible Tabindex Management
- **Dynamic `tabindex`** — Elements added/removed from tab order based on visibility.
- **Nano Feature:** `manageTaborder($container)` JS.

### 8.50 Live Region for Toast
- **`<div aria-live="assertive" role="status" id="toast-live"></div>`** — Announces toast content to screen readers.
- **Nano Feature:** `liveRegion('toast-live', 'assertive')` JS.

### 8.50 Lazy Load Feature Images
- **`loading="lazy"`** on all `>` above-the-fold; improves page speed.
- **Nano Feature:** `lazyImage($path)` PHP helper generates `<img loading="lazy">`.

### 8.50 Accessible Error Identification
- **`aria-describedby`** — Error message ID linked to input `id`.
- **Nano Feature:** `errorAria($inputId, $errorId)` PHP helper.

### 8.50 Dynamic Helper Loading
- **`requireHelper($name)`** — Lazy-loads `helpers/*.php` only if needed (reduces init time).
- **Nano Feature:** `requireHelper('validation')` in module that only uses validation.

### 8.50 Responsive Images with `srcset`
- **`srcset`** provides multiple resolutions; browser selects based on device width.
- **Nano Feature:** `responsiveImage($path, $sizes)` generates `<img srcset>`.


---
<tool_call>
<function=write_todos>
<parameter=todos>
[{"task": "Create comprehensive ERP feature report outline", "completed": true}, {"task": "Generate detailed markdown content covering all modules, features, nano details", "completed": true}, {"task": "Write file and provide conversion instructions", "completed": true}]