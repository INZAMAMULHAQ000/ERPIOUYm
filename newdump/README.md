# newdump/ — production database backup and schema reference

Taken **2026-10-16 10:56** local from `erp_db`, after the login-access and role controls: a person
who has no login can be given one from their own profile (or linked to an account that already
exists), a Super Admin can be changed back to Admin or User, both are CSRF-protected and audited, and
neither can leave the organisation without a Super Admin who can actually sign in.

| File | Size | Purpose |
|---|---|---|
| `erp_db_production_20261016_105654.sql` | 2,596 KB | **Use this.** Full schema + all data: 467 tables, 12,746 rows, 6,090 columns |
| `erp_db_production_20261016_105654.sql.gz` | 289 KB | Same content compressed — use if the upload limit blocks the `.sql` |
| `DATABASE_STRUCTURE.md` | 558 KB | Full data dictionary: every table, every column, keys, defaults, FK targets, row counts |
| `generate_structure.php` | | Regenerates `DATABASE_STRUCTURE.md` from the live database |
| `SHA256SUMS.txt` | | checksums for the current dump, its `.gz`, this README, the dictionary and the generator |
| `erp_db_production_20261016_101924.sql` (+`.gz`) | | Superseded — taken before the login-access controls, 37 minutes earlier |
| `erp_db_production_20261015_125554.sql` (+`.gz`) | | Superseded — before the login-role controls |
| `erp_db_production_20261015_123434.sql` (+`.gz`) | | Superseded — before the adaptive-credentials fix |
| `erp_db_production_20261015_122907.sql` (+`.gz`) | | Superseded — identical content, taken minutes earlier |
| `erp_db_production_20261015_121454.sql` (+`.gz`) | | Superseded — before the profile photo was shown |
| `erp_db_production_20261015_110152.sql` (+`.gz`) | | Superseded — before the drift-repair buttons |
| `erp_db_production_20261015_085453.sql` (+`.gz`) | | Superseded — before the Person Code backfill |
| `erp_db_production_20261014_165508.sql` (+`.gz`) | | Superseded — multi-role schema, before the Admin grants |
| `erp_db_production_20261014_150855.sql` (+`.gz`) | | Superseded — taken before the multi-role work |
| `erp_db_production_20261014_100252.sql` (+`.gz`) | | Superseded — taken before the contract-terms work |
| `erp_db_production_20261013_163751.sql` (+`.gz`) | | Superseded — before the contractor module |
| `erp_db_production_20261013_110452.sql` (+`.gz`) | | Superseded — before the employee identification work |

## The identity rule this snapshot satisfies

> Every human in the system has exactly one directory entry — one **Person Code** — and one code per
> category they belong to: **Employee Code**, **Contractor Code**, **Customer Code**, all linked to
> that one entry.

`people` already held four independent nullable links, so the model needed no new columns for this;
what it needed was coverage and visibility. Before this snapshot **12 of 14 employees and the one
individual customer had no Person Code at all**, because records created inside HRMS, Contracts or
the Customer Master never touched the directory. Three things close that:

1. **Backfill** — `config/migrations/2026_10_15_person_code_coverage.php` minted the 13 missing
   entries, merging on email so one human with an employee row and a customer row becomes one person
   holding both codes. Organisations are deliberately not minted: a `clients` row is a person only
   when `customer_type = 'individual'`, so the directory does not become a mirror of the customer
   master. Dry-run by default, `--apply` to write, idempotent, and its own closing check exits 1 if
   any record is still uncovered.
2. **Auto-mint on save** — `peopleEnsurePersonForRecord()` in `helpers/people_onboarding.php`: an
   employee, contractor or individual customer created directly in its own module now issues or
   reuses a Person Code, and a later wizard run for that email reuses the person instead of forking
   one.
3. **One numbering rule** — `peopleNextPersonCode()` and `nextUniqueDocumentNumber()`. Person and
   Employee codes are read past their prefix instead of as a fixed last four characters (the old read
   would have truncated the series at 9,999), and every allocated number is re-checked against the
   column it is going into. That matters because `clients.client_code` and `contractors.contractor_code`
   are unique database-wide while `document_sequences` counts per company, so a second company could
   previously hand out a code that already existed and the insert died in front of the user.

`people_identity_audit.php` (CLI, blocked over HTTP by `.htaccess`) is the standing proof: 15 checks,
exit 0 while the rule holds, exit 1 naming the offending records when it does not.

**Drift goes both ways, and the list page now fixes both.** Deleting an employee, contractor or
individual customer calls `peopleForfeitRecord()`: the person type is reopened rather than left
claiming a record that is gone, and a directory entry whose last record has gone is removed with it
(anything with a second category or a login account is kept). A record that exists with no directory
entry — a restored dump, hand-edited SQL, or a person deleted from the directory — is shown on the
People Management list with **Add them & repair stale rows**, and entries left with nothing behind
them are shown with **Remove the empty entries**. Both are POST + CSRF, permission-gated, logged, and
refuse to touch a row that still holds a record or a login.

## What this dump carries

Schema, from `config/migrations/2026_10_14_people_multi_role.php` (additive, idempotent, nothing
removed):

- **`person_roles`** (8 columns, 2 rows) — one row per role a person holds: `role`
  (`employee` / `customer` / `contractor`), `status` (`pending` / `complete` / `declined`),
  `record_id` and `completed_at`. `UNIQUE (person_id, role)` makes a double role association
  impossible at the database level, and the FK to `people` is `ON DELETE CASCADE`, so removing a
  directory entry cannot leave orphan role rows. These rows **are** the onboarding workflow state:
  a refresh, an abandoned step, a failed save or a module record deleted elsewhere is answered by
  reading them, not by remembering anything in the session.
- **`people.uq_people_email`** — `people.email` was only indexed, so the directory's "one person
  per email" rule existed in application code alone and two concurrent creations could fork a
  person. The index is now UNIQUE; email stays nullable, so several people recorded without an
  address remain legal. The migration refuses to add it if duplicate emails already exist and
  prints the offending addresses instead of deleting or merging anyone.
- **Backfill**: every existing person got exactly one role row, derived from `category` and the
  populated link columns, marked `complete` where a record already sits behind the link. In this
  snapshot the directory holds **3 people and 5 role rows** (`PER20260015` a customer,
  `PER20260016` an employee with a login, `PER20260017` an employee with an HRMS record), each
  appearing finished rather than half-onboarded because their records already exist.
- `people.category` is **unchanged** and keeps its old meaning as the *primary* role (the first
  selected one), so every existing reader of it — the list filter, the statistics, the profile
  badge — still works. `database/schema.sql` in the repo was regenerated from the same database
  (469 tables).

Data, from `config/migrations/2026_10_15_people_directory_admin_access.php`:

- **Admin (role 2) now holds `people_management.view`, `.create` and `.edit`** — three rows in
  `role_permissions`. `people_management.delete` stays Super Admin only. Without this, an Admin held
  `employees.create` / `customers.create` / `contractors.create` yet could not open the screen that
  starts an onboarding.

Code changes that carry no DDL but ship with this snapshot: People Management no longer inserts into
`employees` or `contractors` itself; `middleware/auth.php` re-validates the session against the
`users` table; `modules/people_management/delete.php` and `modules/employees/delete.php` require POST
plus a CSRF token; and `config/database.php` gained an **optional** `config/db.local.php` override.

## Logins: giving one to a person, and changing the role it holds (no DDL)

A person's **person types** (Employee / Customer / Contractor) and their **login roles**
(Super Admin / Admin / User) are different things and live in different tables — `person_roles`
versus `user_roles`.

**Giving a login to a person who does not have one** was not possible before this snapshot.
`people.user_id` was written only by `modules/people_management/create.php`, at the moment the
directory entry was made, so anyone created without ticking "Create login credentials" — or created
from HRMS / Contracts / the Customer Master, which never touch it — sat on their profile reading
*"This person cannot log in to the ERP system"* with no control anywhere that could change that. A
person's profile now offers, depending on state:

| State | What the profile offers | Needs |
|---|---|---|
| No login, no matching account | **Create login & attach** — a form pre-filled with the person's name and email | `users.create` **and** `people_management.edit` |
| No login, but an unclaimed account with that email exists | **Link the existing account** | `users.edit` **and** `people_management.edit` |
| Login attached | **Change this login's role**, **View User Record**, **Unlink this login from the person** | `users.edit` (+ the same pair for unlinking) |

All three post to `modules/people_management/login.php`, which is POST-only, CSRF-checked and
permission-gated, and delegates the actual account work to `helpers/account.php` — the same code
`modules/users/create.php` now runs, so an account minted from a profile cannot be shaped differently
from one minted in the Users module. `people.user_id` is indexed but **not unique**, so the helper is
the only thing standing between one login serving two directory entries; it refuses that, refuses a
second login for a person who already has one, and refuses to duplicate an email that is already in
use (including by a soft-deleted account, because `users.email` is UNIQUE across every row). Creating
an account in the Users module for an email that matches a person with no login now attaches it,
rather than leaving the profile and the account unaware of each other.

Three defects were fixed on the role path, all of them privilege-related:

- **No CSRF token.** Both `modules/users/edit.php` and `modules/users/create.php` accepted a
  cross-site POST that rewrote `user_roles`, so any logged-in Super Admin visiting a crafted page
  could have a user's roles silently replaced. Both forms now carry `csrf_token` and are refused
  without it.
- **`$_POST['roles']` was not validated.** A stale or hand-crafted id reached `user_roles` after the
  user row had already been written, so the save died in front of the user with a foreign-key error
  on a half-updated account. `assignableRoleIds()` now filters the submission against the live
  `roles` table; `status` is likewise checked against `active|inactive|suspended`.
- **Admin could mint a Super Admin.** `users.create` and `users.edit` are both granted to **Admin**,
  and nothing compared the roles being handed out against the roles the actor holds: an Admin could
  create themselves a Super Admin account, or promote a colleague past their own reach.
  `accountGrantableRoleIds()` now allows a Super Admin to grant anything and anyone else only roles
  they already hold — on the person's profile, on Users → Create, and on Users → Edit alike.
- **Nothing prevented lockout.** `roleChangeBlocked()` now refuses two changes: removing your own
  Super Admin role or deactivating your own account, and stripping Super Admin from (or deactivating)
  **the last Super Admin that can actually sign in** — an inactive, soft-deleted or non-crypt-password
  account does not count as a fallback.
  Every accepted change is written to `audit_logs` as
  `Updated user: <email> — roles [Super Admin] -> [Admin], status active`.

Verified end to end over HTTP (55 assertions: the form's absence on a profile that already has a
login, refusal without a token, refusal on a GET, create → attach → **sign in with the new
credentials**, role boundaries in both directions, conflict refusal leaving nothing half-applied,
detach → link → no-duplicate, an Admin refused a Super Admin grant and allowed an Admin grant, and the
audit lines), after which the test people, accounts and audit rows were deleted and re-checked for
orphans. The suite found two real bugs on the way: `login.php` called `peopleLoad()` without
requiring `helpers/people_onboarding.php` (fatal on first use), and `helpers/account.php` filtered
`people` on a `deleted_at` column that does not exist.

No row in this dump was produced by the guards: the test accounts they were exercised on were
created and deleted inside the same run, and `users`, `user_roles` and `audit_logs` were re-checked
afterwards.

**Credential resolution is adaptive, and must stay that way.** The same code runs on the XAMPP
machine and on `application.kmsdigitechs.com` with no file to create: a web request is judged by the
host it arrived on, and a command-line run by the machine it is on (so production cron no longer
mistakes itself for development). `config/db.local.php` is an opt-in override for a machine that
wants to keep its password out of version control — nothing depends on it. An earlier revision of
this README described it as required, and that wording shipped a broken production site: the file is
gitignored, so a deploy never carried it, and the app died at startup with "Application is not
configured". Do not make that file a precondition again.

No employee, customer or contractor table changed shape. `contractors` (39 columns),
`contractor_contracts` (47), `contractor_rate_schedules` (11), `contractor_documents` (12) and
`people.contractor_id` are exactly as in the earlier dumps.

## DATABASE_STRUCTURE.md — the tracking document

469 tables listed by domain (Contractor, Employee & HR, Finance & GL, Procurement & Vendors,
Sales & CRM, Projects, Inventory, Helpdesk, AI, Configuration, System, Other), each with a column
table: position, name, type, nullability, key flags (`PK`/`UQ`/`IDX`/`FK`), default and
foreign-key target, plus live row counts and an anchored table index.

Regenerate it any time — it reads `information_schema` only and writes nothing to the database:

```bash
php newdump/generate_structure.php
```

The dictionary describes the **live** database (469 tables, 6,119 columns, 12,755 rows) while the
dump carries **467 / 6,090 / 12,746**. The difference is exactly the two local scratch tables below
(29 columns, 9 rows), so the two documents reconcile rather than contradict. Re-run the generator
after every migration and diff the output.

## Why the scratch tables are excluded

`clients_pre_customer_master_20261012` and `companies_pre_company_master_20261012` are local
pre-migration safety nets, not business data. Zero references to them appear in the dump.
Everything else is identical to the live database.

## Command used

```
mysqldump -u root --single-transaction --quick --routines --triggers \
  --add-drop-table --default-character-set=utf8mb4 --comments \
  --ignore-table=erp_db.clients_pre_customer_master_20261012 \
  --ignore-table=erp_db.companies_pre_company_master_20261012 erp_db
```

`--single-transaction` gives a consistent InnoDB snapshot without locking the running app.

## Verification actually performed (2026-10-16 10:56, 13 harness assertions + 15 identity checks, 0 failures)

Not just written — restored into a scratch database (`erp_db_verify_20261016_105654`) and compared
with the live one by a harness that is designed not to be able to pass vacuously: it prints how many
pairs it actually counted and **fails if that number is below the table count**, and it finishes with
a self-test that damages a copy and asserts the damage is noticed.

Two failure modes of the harness itself were found and fixed while producing this snapshot, and both
are the reason the guards exist:

- a ~45 KB 469-way `UNION ALL` was being passed with `-e`, which exceeds the Windows command-line
  argument limit, so MySQL never saw the query; the statements now go in on **stdin**, one per table.
- `mysql.exe` on Windows writes **CRLF**; redirected to a file every line carried a trailing `\r`, so
  a table-name diff reported all 469 tables as "new". All client output is now passed through
  `tr -d '\r'`. (An earlier generation of this harness reported "0 compared, 0 mismatched" and looked
  like a clean pass for a different reason entirely — `'-u root'` handed over as one argument.)

What was asserted, all against this exact file:

| # | Check | Result |
|---|---|---|
| 0 | the `.sql` starts with a dump banner and ends with its `Dump completed` marker (not truncated) | 2,658,410 bytes |
| 1 | tables = live 469 − 2 excluded | **467** |
| 1 | columns vs live minus the scratch tables | **6,090** identical |
| 1 | indexes vs live minus the scratch tables | **2,193** identical |
| 1 | routines + triggers carried | 0 = 0 (the source has none) |
| 2 | the restored table set equals the intended set, **in both directions** | exact, no surprises |
| 3 | **467 row-count pairs compared individually** | 0 mismatched, **12,746 rows** |
| 4 | the `.gz` imports and yields the same 467 tables | ok |
| 5 | `php people_identity_audit.php` **run against the restored copy** | exit 0, 15 checks clean |
| 6 | self-test: a table dropped from the comparison is noticed | ok |
| 6 | self-test: the pair-count guard trips on a truncated comparison | ok (466 vs 467) |
| 6 | self-test: an excluded scratch table never appears in the restore | ok |
| 6 | self-test: a deleted row is noticed (a copy with `roles` id 3 removed differs) | ok |

Step 5 is the part that matters most for this project: the restored copy is not merely row-equivalent,
it re-passes the identity rule on its own data — every employee and every individual customer has a
Person Code, no Person Code is blank or duplicated, no `complete` role points at a record that is
missing, and no directory entry is claimed by an organisation customer.

**The restored copy was also booted as the application**, not just queried. With a temporary
`config/db.local.php` pointing at it, login (HTTP 302 to the dashboard) and then Dashboard, People
Management list, the profile of a person with **no** login, Users, Employees, Contractors and Customers
all rendered — 56 KB to 101 KB each, with **zero** occurrences of `Fatal error`, `Parse error`,
`Warning:`, `Deprecated:`, `Undefined variable`, `Access Denied` or `DB Error`. Provenance was
established with a marker account inserted **only** in the restored copy: the Users list served from
it returned 4 occurrences of the marker name (the result row plus the search box echoing the term), and
the same request after deleting the override returned 1 — the calibration for an empty result set,
confirmed by searching for a term that matches nothing at all. `SELECT COUNT(*)` against `erp_db` for
the marker returned 0, so no test row was ever written to the live database.

Both scratch databases (`erp_db_verify_20261016_105654`, `erp_db_proof_20261016_105654`,
`erp_db_gzcheck`) and the temporary override were removed afterwards; `information_schema` lists only
`erp_db`, and `config/db.local.php` does not exist — which is the state production needs, because
nothing depends on it.

The source has no stored procedures, functions, triggers, views or events, so their absence in the dump
is accuracy rather than loss.

## IMPORTANT — uploaded files are not in this dump

`employees.photo_path`, `contractors.photo_path` and both `*_documents.file_path` columns store
paths only; the bytes live on disk under `uploads/`. Importing the SQL alone leaves every scan and
photo broken.

Currently on disk (3.2 MB, all belonging to employee #34):

```
uploads/employees/34/photo_34_68453e6b.jpg             1,993,870
uploads/employees/34/passport_copy_34_b581069b.pdf        760,255
uploads/employees/34/emirates_id_copy_34_c007d789.pdf     383,747
uploads/employees/34/visa_copy_34_eabae5c8.jpg            121,860
```

`uploads/contractors/` is empty — the register has no rows yet, because every record created during
testing was deleted before this dump. Confirm with `ls -R uploads` after importing.

Copy the tree to the production app root (the folder holding `modules/`), preserving names exactly —
the database references them verbatim, and `uploads/` is gitignored so a git deploy will not carry it:

```bash
scp -r uploads/ <user>@<prod>:/path/to/app/uploads/
```

People Management shows that photo as the person's avatar on its list, profile and onboarding
screens — it reads `employees.photo_path` or `contractors.photo_path` rather than keeping a second
copy, so **the directory inherits the same breakage**: without this folder the avatar falls back to
initials, with a tooltip saying a photo is recorded but the file is not on this server. That is
deliberate — a broken image tag on every row of a people list is worse than an initial.

## Importing to production

The dump has no `CREATE DATABASE` / `USE` statement, so it imports into whichever database you
select — it does not have to be named `erp_db`.

```bash
cd newdump && sha256sum -c SHA256SUMS.txt          # verify the transfer first

# 1. back up production first so you can roll back
mysqldump -h localhost -u <prod_user> -p <prod_db> > prod_before_import.sql

# 2. import (this DROPS and recreates every table in <prod_db>)
mysql -h localhost -u <prod_user> -p <prod_db> < erp_db_production_20261016_100953.sql
```

In phpMyAdmin: select the production database → Import → choose the `.sql` (or `.gz`) → Go.

**If you deploy code instead of importing this dump**, the schema change is
`config/migrations/2026_10_14_people_multi_role.php` — run it before the new People screens, which
read `person_roles` unconditionally and will fatal without it.

## After importing — do these six things

1. **Nothing to configure for the database.** `config/database.php` resolves the production
   credentials from the host the request arrived on, exactly as it did before. Optionally, to stop
   the password living in version control, create `config/db.local.php` (copy
   `config/db.local.example.php`, fill in the real values, `'production' => true`) — it is gitignored,
   so it must be created on the server itself, and it takes precedence when present. It is never
   required.
2. **Change the admin password, and delete the leftover test accounts.** The imported `users` table
   carries **15 accounts**, and two groups of them must not go live:
   - `admin@erp.com` / `admin123` (id 1, Super Admin) — the local demo login. Change it from
     Users → Edit user, immediately, before the site is indexed.
   - ids **168–174**: `Audit Tenant 42`, `Audit Tenant 43` (three repeated runs) and `Doc Test`.
     These are leftovers from automated audit/AI testing on 2026-09-03, not your data. Their
     `password` column holds the literal `x` — not a bcrypt hash — so `password_verify()` can never
     succeed and **none of them can sign in**, which is why the boot proof above could rely on them.
     But `Doc Test` (id 174) is granted **Super Admin**, so `roleChangeBlocked()` deliberately ignores
     accounts whose password is not a crypt hash when it counts how many Super Admins would be left —
     otherwise a login that can never be used would look like a safety net. Delete the seven rows
     anyway; a directory of accounts that can never sign in is noise in every user list.
   The login screen used to print `Demo: admin@erp.com / admin123` on every host; it now prints that
   only when `IS_PRODUCTION` is false, so the hint survives locally and never reaches the live site.
   Verified both ways: the rendered page contains 0 occurrences of `admin123` / `admin@erp.com` with
   `'production' => true`, and still shows the hint once the override is removed.
3. **Copy `uploads/`** as described above, or document viewers show broken images and blank PDFs.
4. **Make `uploads/` writable** by the web-server user. The modules create
   `uploads/employees/<id>/` and `uploads/contractors/<id>/` on first upload and report a clear
   error if the directory cannot be made.
5. **Assign companies.** Non-Super-Admin users need `user_companies` rows or they see no company
   at all; role id 1 bypasses that check, everyone else does not. Contractor contracts are stamped
   with the active company and numbering (`CTR…`, `CTRT-…`) is per company — check the counters
   under Configuration → Document Numbering before the first live entry. Admins hold
   `people_management.view/create/edit` in this dump.

   Deploying code instead of importing? Apply the migrations in order, then let the auditor tell you
   whether the identity rule holds:

   ```bash
   php config/migrations/2026_10_14_people_multi_role.php
   php config/migrations/2026_10_15_people_directory_admin_access.php
   php config/migrations/2026_10_15_person_code_coverage.php            # read-only preview
   php config/migrations/2026_10_15_person_code_coverage.php --apply    # after you approve the list
   php people_identity_audit.php                                        # exit 0 means the rule holds
   ```

   The preview prints every record that would receive a Person Code. On a production database that
   list is the data you are signing off, so read it first — locally it is what surfaced ten seed
   employees that nobody had ever put in the directory.
6. **Rotate the database password that is still in git history.** `config/database.php` carried the
   production password in plaintext up to this change; the file is clean now, but the old value is
   reachable in past commits. Change it in the hosting panel and put only the new one in
   `config/db.local.php`.
6. **Decide who may use People Management.** All four `people_management.*` permissions are granted
   to Super Admin only, while `employees.create`, `customers.create` and `contractors.create` also
   sit with Admin. The onboarding coordinator handles that gracefully — a user who lacks a module's
   permission sees "Needs employees.create" instead of a link that dies on Access Denied — but if
   Admins are meant to create people, grant `people_management.view/create/edit` to that role.

## Sensitivity — read this before you push

This folder holds live personal data: password hashes for 8 of the 15 accounts (the other 7 are the
test leftovers described above, with a non-hash placeholder), one employee record carrying real
passport and Emirates ID numbers, 3 directory entries, 7 customer records, all company, invoice,
journal and audit records (2,623 audit rows), and the `ai_*` tables with encrypted provider API keys —
effectively readable by anyone holding the file, because the repo's encryption key is hardcoded in
`modules/ai/includes/ai_credential.php`.

`DATABASE_STRUCTURE.md` is the schema only — no rows — but it does disclose table and column
naming across the whole ERP.

**Status of the repository, checked in this working copy:** `.gitignore` now excludes
`newdump/*.sql`, `newdump/*.sql.gz` and `config/db.local.php`, and the eight previously committed
dump files have been removed from the index (`git rm --cached`), so the next commit stops shipping
them. The files stay on disk. `git ls-files newdump` now lists only `DATABASE_STRUCTURE.md`,
`README.md`, `SHA256SUMS.txt` and `generate_structure.php`.

**What is still exposed:** history. Commits `731a219` and `eea63cd` (both labelled "Backup
completely") carry full dumps — the 10:02 dump alone is a 2,620,110-byte object reachable from
`HEAD` — and this repository has a remote (`origin` → `github.com/INZAMAMULHAQ000/ERPOUIVB`), so
whoever can read that remote can already read the passport numbers, the bcrypt hashes and the AI
provider keys. `config/database.php` likewise carried the production database password in earlier
revisions. Untracking does not undo that, and neither does deleting the files.

Treat these credentials and records as published until history is dealt with. The steps, least to
most invasive — the third one rewrites every commit hash and needs your explicit decision, so it
has not been run:

1. Rotate what is exposed: the admin password, the database password in the hosting panel, and every
   AI provider key held in `ai_*`.
2. Commit the untracking above, and confirm `git ls-files` never re-lists a `.sql`.
3. Purge the blobs from history with `git filter-repo --invert-paths --path-glob 'newdump/*.sql*'`
   (or BFG), then force-push `main` and every branch that carries them
   (`codebase-indexing-0baac`, `erp-module-system`). Everyone else must re-clone; anyone with an old
   clone keeps the data locally regardless.

`DATABASE_STRUCTURE.md` is the schema only — no rows — but it does disclose table and column naming
across the whole ERP.

The companion `uploads/employees/34/` tree is worse still: actual passport and visa images of a
named person. That one *is* gitignored, so it lives only on this disk and on any machine it is
copied to.

Store the folder encrypted, delete it from any shared machine once deployed, and never email it.
