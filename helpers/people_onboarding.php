<?php
/**
 * People onboarding — the single place that knows what a person's business
 * roles are and how a role gets fulfilled.
 *
 * People Management is the entry point: it creates the shared person record
 * and the list of roles that person was selected for. It never collects
 * employee, customer or contractor data itself. Each module owns its own form,
 * validation and numbering; this helper only (a) tells a module "you are
 * finishing onboarding for person N", (b) prefills that module's form with the
 * shared identity, and (c) writes the relationship back once the module has
 * saved successfully.
 *
 * Why the progress lives in the database rather than the session:
 * `person_roles.status` is the workflow state. A user who closes the tab,
 * refreshes mid-step, loses a role save, or has a module record deleted under
 * them (contractors/delete.php nulls people.contractor_id) still gets the
 * correct next step, because the answer is read from the rows, not remembered
 * in memory. Nothing here opens a transaction that spans two screens: each
 * module save commits on its own, and the link is a second short transaction.
 *
 * Conventions worth knowing before editing this file:
 *  - to() exits, so a caller that has already decided where to go cannot run
 *    code after it. Every function here returns a value and lets the page
 *    redirect.
 *  - flash() is keyed and the layout consumes every pending key on the next
 *    render, so wizard messages use 'wiz_*' keys and never 'success'/'error'.
 *  - $_SESSION['_old_input'] is one global slot shared by every form in the
 *    app. It is how prefilling a module form without touching its markup is
 *    possible at all — and why leaving the wizard must clear it.
 */

/**
 * The role registry, in the order onboarding steps are presented.
 *
 * Deliberately the only copy of these names, tables, link columns and URLs:
 * the coordinator, the list, the profile and the three module forms all read
 * it from here so they cannot drift apart.
 */
function peopleRoleDefinitions()
{
    return [
        'employee' => [
            'label'          => 'Employee',
            'module'         => 'HRMS — Employees',
            'table'          => 'employees',
            'code_column'    => 'employee_code',
            'link_column'    => 'employee_id',
            'create_perm'    => 'employees.create',
            'view_perm'      => 'employees.view',
            'create_url'     => 'modules/employees/create.php',
            'view_url'       => 'modules/employees/view.php?id=',
            'hint'           => 'Department, designation, joining date, contract terms and right-to-work scans.',
            'identity_mode'  => 'split_name',
            'deleted_column' => null,
        ],
        'customer' => [
            'label'          => 'Customer',
            'module'         => 'Customer Master',
            'table'          => 'clients',
            'code_column'    => 'client_code',
            'link_column'    => 'customer_id',
            'create_perm'    => 'customers.create',
            'view_perm'      => 'customers.view',
            'create_url'     => 'modules/customers/form.php',
            'view_url'       => 'modules/customers/view.php?id=',
            'hint'           => 'Billing profile, credit terms, TRN and addresses as an individual customer.',
            // The customer master stores one trading name, not a first and last
            // name, and only natural persons belong in the directory at all.
            'identity_mode'  => 'single_name',
            'deleted_column' => 'deleted_at',
            'person_only'    => true,
        ],
        'contractor' => [
            'label'          => 'Contractor',
            'module'         => 'Contracts — Contractor Register',
            'table'          => 'contractors',
            'code_column'    => 'contractor_code',
            'link_column'    => 'contractor_id',
            'create_perm'    => 'contractors.create',
            'view_perm'      => 'contractors.view',
            'create_url'     => 'modules/contractors/form.php',
            'view_url'       => 'modules/contractors/view.php?id=',
            'hint'           => 'Register entry with work-permit documents, then engagement contracts and rates.',
            'identity_mode'  => 'split_name',
            'deleted_column' => 'deleted_at',
        ],
    ];
}

function peopleRoleDefinition($role)
{
    $defs = peopleRoleDefinitions();
    return $defs[$role] ?? null;
}

/** The first role in canonical order — that is what people.category records. */
function peoplePrimaryRole(array $roles)
{
    foreach (array_keys(peopleRoleDefinitions()) as $role) {
        if (in_array($role, $roles, true)) {
            return $role;
        }
    }
    return null;
}

/**
 * Re-order selected roles into the canonical onboarding sequence and drop
 * anything that is not a real role. Input comes straight from the request.
 */
function peopleNormaliseRoles($roles)
{
    $roles = is_array($roles) ? $roles : [];
    $clean = [];
    foreach (array_keys(peopleRoleDefinitions()) as $role) {
        if (in_array($role, $roles, true)) {
            $clean[] = $role;
        }
    }
    return $clean;
}

/**
 * One query for the list page: person_id => [role => status].
 *
 * The joins exist to keep the list honest. `person_roles` can claim a role is
 * complete while the record behind it has been deleted from its own module —
 * the FK nulls people.employee_id and the CLI auditor reports it, but a table of
 * people must not display a relationship that no longer exists. So a claimed
 * complete row whose record is gone is shown as pending, which is the truth and
 * also what makes the row's "Continue onboarding" link meaningful.
 */
function peopleRoleSummary($db, array $personIds)
{
    if (!$personIds) {
        return [];
    }
    $in = implode(',', array_fill(0, count($personIds), '?'));
    $stmt = $db->prepare("
        SELECT pr.person_id, pr.role,
               CASE
                 WHEN pr.status <> 'complete' THEN pr.status
                 WHEN pr.role = 'employee'   AND e.id IS NULL THEN 'pending'
                 WHEN pr.role = 'customer'   AND cl.id IS NULL THEN 'pending'
                 WHEN pr.role = 'contractor' AND ct.id IS NULL THEN 'pending'
                 ELSE 'complete'
               END AS status
        FROM person_roles pr
        LEFT JOIN employees e       ON pr.role = 'employee'   AND e.id  = pr.record_id
        LEFT JOIN clients cl        ON pr.role = 'customer'   AND cl.id = pr.record_id AND cl.deleted_at IS NULL
        LEFT JOIN contractors ct    ON pr.role = 'contractor' AND ct.id = pr.record_id AND ct.deleted_at IS NULL
        WHERE pr.person_id IN ($in)");
    $stmt->execute(array_values($personIds));
    $summary = [];
    foreach ($stmt->fetchAll() as $row) {
        $summary[(int) $row['person_id']][$row['role']] = $row['status'];
    }
    return $summary;
}

/**
 * Load a person with their roles, repairing rows whose module record vanished.
 *
 * A complete role whose link column is NULL, or whose record no longer exists,
 * is put back to pending. That is what makes deletion outside this workflow
 * (a contractor removed from the register) reopen the step instead of leaving
 * the directory claiming a relationship that is gone.
 */
function peopleLoad($db, $personId)
{
    $stmt = $db->prepare("SELECT * FROM people WHERE id = ? LIMIT 1");
    $stmt->execute([(int) $personId]);
    $person = $stmt->fetch();
    if (!$person) {
        return null;
    }

    $roles = [];
    $rs = $db->prepare("SELECT role, status, record_id FROM person_roles WHERE person_id = ?");
    $rs->execute([(int) $person['id']]);
    foreach ($rs->fetchAll() as $row) {
        $roles[$row['role']] = ['status' => $row['status'], 'record_id' => $row['record_id'] !== null ? (int) $row['record_id'] : null];
    }

    $repair = $db->prepare("UPDATE person_roles SET status = 'pending', record_id = NULL, completed_at = NULL
                            WHERE person_id = ? AND role = ?");
    foreach (peopleRoleDefinitions() as $role => $def) {
        if (($roles[$role] ?? ['status' => null])['status'] !== 'complete') {
            continue;
        }
        $linked = $person[$def['link_column']] !== null ? (int) $person[$def['link_column']] : 0;
        $exists = false;
        if ($linked > 0) {
            // A soft-deleted customer is not a live record: leaving the role
            // "complete" would advertise a link whose page redirects to a list.
            $gone = !empty($def['deleted_column']) ? " AND `{$def['deleted_column']}` IS NULL" : '';
            $check = $db->prepare("SELECT 1 FROM `{$def['table']}` WHERE id = ?$gone LIMIT 1");
            $check->execute([$linked]);
            $exists = (bool) $check->fetch();
        }
        if (!$exists) {
            $repair->execute([(int) $person['id'], $role]);
            $roles[$role] = ['status' => 'pending', 'record_id' => null];
            $person[$def['link_column']] = null;
        }
    }

    $person['roles'] = $roles;
    return $person;
}

/** Roles still to be completed, in canonical order. */
function peoplePendingRoles($person)
{
    $pending = [];
    foreach (peopleRoleDefinitions() as $role => $def) {
        if (($person['roles'][$role] ?? ['status' => 'complete'])['status'] === 'pending') {
            $pending[$role] = $def;
        }
    }
    return $pending;
}

/** Roles that were declined on purpose, so they are neither done nor to-do. */
function peopleDeclinedRoles($person)
{
    $declined = [];
    foreach (peopleRoleDefinitions() as $role => $def) {
        if (($person['roles'][$role] ?? ['status' => null])['status'] === 'declined') {
            $declined[$role] = $def;
        }
    }
    return $declined;
}

/**
 * Is this module form finishing an onboarding step?
 *
 * Returns the person only when the request really is a wizard hand-off: a
 * person exists, that role was selected for them, it is still pending, and the
 * link column is still empty. Anything else — a plain visit to the module's
 * create screen, a role already filled, a stale bookmarked link — yields null
 * and the module behaves exactly as it always did.
 */
function peopleOnboardingSubject($db, $role)
{
    $def = peopleRoleDefinition($role);
    if ($def === null || empty($_GET['person_id'])) {
        return null;
    }
    $person = peopleLoad($db, (int) $_GET['person_id']);
    if (!$person) {
        return null;
    }
    if (($person['roles'][$role] ?? ['status' => null])['status'] !== 'pending') {
        return null;
    }
    if (!empty($person[$def['link_column']])) {
        return null;
    }
    $person['onboarding_role'] = $role;
    return $person;
}

/**
 * Preload the module form with the shared identity.
 *
 * The three target forms render from old(), so seeding the session slot is
 * what prefills them — no field-by-field changes in module markup. Values
 * already in the slot win, because on a failed submission the slot holds what
 * the user just typed and re-typing the person row over it would destroy
 * their work.
 */
function peopleOnboardingPrefill($person, $role)
{
    $fullName = trim($person['first_name'] . ' ' . $person['last_name']);

    $identity = [
        'first_name'    => $person['first_name'],
        'last_name'     => (string) $person['last_name'],
        'gender'        => (string) $person['gender'],
        'date_of_birth' => (string) $person['date_of_birth'],
        'email'         => (string) $person['email'],
        'phone'         => (string) $person['phone'],
        'address'       => (string) $person['address'],
        'notes'         => (string) $person['notes'],
    ];

    // The customer master has no person-shaped columns: company_name is the
    // only required one, and 'individual' is its natural-person type.
    if ($role === 'customer') {
        $identity['company_name']  = $fullName;
        $identity['customer_type'] = 'individual';
        $identity['contact_person'] = $fullName;
        unset($identity['first_name'], $identity['last_name']);
    }

    foreach ($identity as $key => $value) {
        if ($value === '') {
            unset($identity[$key]);
        }
    }

    $_SESSION['_old_input'] = array_merge($identity, $_SESSION['_old_input'] ?? []);
}

/**
 * Record the selected roles on a newly created person.
 *
 * Called in the same transaction as the people insert, so a person never
 * exists without the role rows that say what they were created for.
 */
function peopleRolesInsert($db, $personId, array $roles)
{
    $stmt = $db->prepare("INSERT INTO person_roles (person_id, role, status) VALUES (?, ?, 'pending')");
    foreach ($roles as $role) {
        $stmt->execute([(int) $personId, $role]);
    }
}

/**
 * Mint the next Person Code: PER<YYYY><nnnn>.
 *
 * Derived from the highest code of the year rather than a counter, so it
 * self-corrects after deletions, and re-checked against the table because
 * `people.person_code` is unique database-wide. The suffix is read past the
 * prefix instead of as the last four characters, so the series keeps working
 * once a year passes 9,999 people, where a fixed-width read would truncate.
 */
function peopleNextPersonCode($db)
{
    $prefix = 'PER' . date('Y');
    $stmt = $db->prepare("SELECT MAX(person_code) FROM people WHERE person_code LIKE ?");
    $stmt->execute([$prefix . '%']);
    $last = $stmt->fetchColumn();
    $base = $last ? (int) substr($last, strlen($prefix)) : 0;

    $free = $db->prepare("SELECT COUNT(*) FROM people WHERE person_code = ?");
    for ($step = 1; $step <= 25; $step++) {
        $code = $prefix . str_pad((string) ($base + $step), 4, '0', STR_PAD_LEFT);
        $free->execute([$code]);
        if ((int) $free->fetchColumn() === 0) {
            return $code;
        }
    }
    throw new RuntimeException('Could not allocate a unique Person Code — check for gaps in the ' . $prefix . ' series.');
}

/**
 * Close one step for a person: write the link column and mark the role complete,
 * inside the caller's transaction.
 *
 * Shared by the wizard hand-off and by minting a directory entry from a module,
 * so the two paths cannot disagree about what "complete" means.
 */
function peopleMarkRoleComplete($db, $personId, $role, $recordId, $linkAlreadySet = false)
{
    $def = peopleRoleDefinition($role);
    if ($def === null) {
        return false;
    }
    if (!$linkAlreadySet) {
        $db->prepare("UPDATE people SET `{$def['link_column']}` = ? WHERE id = ?")->execute([(int) $recordId, (int) $personId]);
    }
    $marked = $db->prepare("UPDATE person_roles SET status = 'complete', record_id = ?, completed_at = NOW()
                            WHERE person_id = ? AND role = ? AND status <> 'complete'");
    $marked->execute([(int) $recordId, (int) $personId, $role]);
    if ($marked->rowCount() === 0) {
        $exists = $db->prepare("SELECT COUNT(*) FROM person_roles WHERE person_id = ? AND role = ?");
        $exists->execute([(int) $personId, $role]);
        if ((int) $exists->fetchColumn() === 0) {
            $db->prepare("INSERT INTO person_roles (person_id, role, status, record_id, completed_at)
                          VALUES (?, ?, 'complete', ?, NOW())")->execute([(int) $personId, $role, (int) $recordId]);
        }
    }
    return true;
}

/**
 * Read the identity a module record carries, shaped like a `people` row.
 *
 * Returns null when the record must not be in the human directory at all: gone,
 * soft-deleted, or an organisation rather than an individual customer.
 */
function peopleIdentityFromRecord($db, $role, $recordId)
{
    $def = peopleRoleDefinition($role);
    $recordId = (int) $recordId;
    if ($def === null || $recordId <= 0) {
        return null;
    }

    $where = "id = ?";
    if (!empty($def['deleted_column'])) {
        $where .= " AND `{$def['deleted_column']}` IS NULL";
    }

    if (($def['identity_mode'] ?? '') === 'split_name') {
        $stmt = $db->prepare("SELECT first_name, last_name, email, phone, address, gender, date_of_birth,
                                     `{$def['code_column']}` AS code
                              FROM `{$def['table']}` WHERE $where LIMIT 1");
        $stmt->execute([$recordId]);
        $row = $stmt->fetch();
        if (!$row) {
            return null;
        }
        $first = trim((string) $row['first_name']);
        $last = trim((string) $row['last_name']);
    } else {
        $stmt = $db->prepare("SELECT company_name, customer_type, email, phone, address,
                                     `{$def['code_column']}` AS code
                              FROM `{$def['table']}` WHERE $where LIMIT 1");
        $stmt->execute([$recordId]);
        $row = $stmt->fetch();
        // Organisations are customers but they are not people: the directory is a
        // list of humans, and `people` must not become a mirror of `clients`.
        if (!$row || $row['customer_type'] !== 'individual') {
            return null;
        }
        $name = trim(preg_replace('/\s+/u', ' ', (string) $row['company_name']));
        $space = strpos($name, ' ');
        $first = $space === false ? $name : substr($name, 0, $space);
        $last = $space === false ? '' : substr($name, $space + 1);
    }

    if ($first === '') {
        $first = (string) $row['code'];   // a code always exists and beats an empty name
    }

    return [
        'first_name'    => $first,
        'last_name'     => $last,
        'email'         => trim((string) ($row['email'] ?? '')),
        'phone'         => trim((string) ($row['phone'] ?? '')),
        'address'       => trim((string) ($row['address'] ?? '')),
        'gender'        => in_array($row['gender'] ?? '', ['male', 'female', 'other'], true) ? $row['gender'] : null,
        'date_of_birth' => !empty($row['date_of_birth']) ? $row['date_of_birth'] : null,
        'code'          => $row['code'],
        'record_id'     => $recordId,
    ];
}

/**
 * Decide what the directory should do about one module record, writing nothing.
 *
 * The live save path and the backfill's --dry-run both read this, so a preview
 * cannot promise something the real run would then do differently.
 */
function peoplePersonDecision($db, $role, $recordId)
{
    $def = peopleRoleDefinition($role);
    if ($def === null) {
        return ['action' => 'skipped', 'reason' => 'unknown person type', 'person_id' => 0, 'person_code' => null];
    }

    $identity = peopleIdentityFromRecord($db, $role, $recordId);
    if ($identity === null) {
        return ['action' => 'skipped', 'reason' => 'not a natural person', 'person_id' => 0, 'person_code' => null];
    }

    $linkColumn = $def['link_column'];

    $linked = $db->prepare("SELECT id, person_code FROM people WHERE `$linkColumn` = ? LIMIT 1");
    $linked->execute([(int) $recordId]);
    if ($existing = $linked->fetch()) {
        return ['action' => 'already', 'reason' => 'the record is already in the directory',
                'person_id' => (int) $existing['id'], 'person_code' => $existing['person_code'],
                'identity' => $identity];
    }

    $person = null;
    if ($identity['email'] !== '') {
        $match = $db->prepare("SELECT id, person_code, `$linkColumn` FROM people WHERE email = ? LIMIT 1");
        $match->execute([$identity['email']]);
        $person = $match->fetch();
    }

    if ($person && !empty($person[$linkColumn])) {
        return ['action' => 'conflict',
                'reason' => 'that person already holds another ' . strtolower($def['label']) . ' record',
                'person_id' => (int) $person['id'], 'person_code' => $person['person_code'],
                'identity' => $identity];
    }
    if ($person) {
        return ['action' => 'attached', 'reason' => 'same email as ' . $person['person_code'],
                'person_id' => (int) $person['id'], 'person_code' => $person['person_code'],
                'identity' => $identity];
    }
    return ['action' => 'created', 'reason' => 'no person carries that email', 'person_id' => 0,
            'person_code' => null, 'identity' => $identity];
}

/**
 * Guarantee the invariant that every category member has exactly one directory
 * entry. Called after a module has saved its own record directly, without the
 * onboarding wizard.
 *
 * The module row is already committed when this runs, so a failure here can only
 * ever cost the directory entry — never the employee, contractor or customer.
 * The unique index on people.email is the last guard against two concurrent
 * creations forking one human.
 */
function peopleEnsurePersonForRecord($db, $role, $recordId)
{
    $def = peopleRoleDefinition($role);
    $decision = peoplePersonDecision($db, $role, $recordId);

    if (!in_array($decision['action'], ['created', 'attached'], true)) {
        $messages = [
            'skipped'  => 'No directory entry needed: ' . $decision['reason'] . '.',
            'already'  => 'Already in the directory as ' . $decision['person_code'] . '.',
            'conflict' => $decision['person_code'] . ' ' . $decision['reason'] . ', so this record was left unlinked.',
        ];
        return ['action' => $decision['action'], 'person_id' => (int) $decision['person_id'],
                'person_code' => $decision['person_code'], 'message' => $messages[$decision['action']]];
    }

    $identity = $decision['identity'];
    $linkColumn = $def['link_column'];
    $action = $decision['action'];
    $personId = (int) $decision['person_id'];
    $personCode = $decision['person_code'];

    try {
        $db->beginTransaction();

        // Re-read the link inside the transaction: the decision was taken without
        // a lock, and a second tab may have linked this record in the meantime.
        $fresh = $db->prepare("SELECT id, person_code FROM people WHERE `$linkColumn` = ? LIMIT 1");
        $fresh->execute([(int) $recordId]);
        if ($concurrent = $fresh->fetch()) {
            $db->commit();
            return ['action' => 'already', 'person_id' => (int) $concurrent['id'],
                    'person_code' => $concurrent['person_code'],
                    'message' => 'Already in the directory as ' . $concurrent['person_code'] . '.'];
        }

        if ($action === 'attached') {
            peopleMarkRoleComplete($db, $personId, $role, $recordId);
        } else {
            $personCode = peopleNextPersonCode($db);
            $db->prepare("INSERT INTO people (
                person_code, first_name, last_name, email, phone, address,
                gender, date_of_birth, category, notes, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')")->execute([
                $personCode,
                $identity['first_name'],
                $identity['last_name'] ?: null,
                $identity['email'] ?: null,
                $identity['phone'] ?: null,
                $identity['address'] ?: null,
                $identity['gender'],
                $identity['date_of_birth'],
                $role,
                'Directory entry created from ' . $def['module'] . ' record ' . $identity['code'] . '.',
            ]);
            $personId = (int) $db->lastInsertId();
            // The row was inserted without a link column, so markRoleComplete
            // writes it — passing true here would leave the person and their
            // record pointing at nothing.
            peopleMarkRoleComplete($db, $personId, $role, $recordId);
        }

        $db->commit();
    } catch (Throwable $e) {
        if ($db->inTransaction()) {
            $db->rollBack();
        }
        return ['action' => 'failed', 'person_id' => 0, 'person_code' => null,
                'message' => 'The record was saved, but no directory entry could be created for it: ' . $e->getMessage()];
    }

    logAudit($_SESSION['user_id'] ?? null,
        ($action === 'created' ? 'Issued ' : 'Linked ') . $personCode
        . ' for ' . $def['label'] . ' ' . $identity['code'], 'people_management');

    return ['action' => $action, 'person_id' => $personId, 'person_code' => $personCode,
            'message' => $action === 'created'
                ? 'Person Code ' . $personCode . ' issued for this ' . strtolower($def['label']) . '.'
                : 'Linked to the existing person ' . $personCode . '.'];
}

/**
 * Every code a person holds, in canonical order, permission-filtered.
 *
 * One place decides who may see which code, so the directory profile, the list,
 * the edit screen and the three module profiles render the same identity block
 * instead of four slightly different ones.
 */
function peopleIdentityCodes($db, $person)
{
    $codes = [];
    foreach (peopleRoleDefinitions() as $role => $def) {
        $visible = !function_exists('hasPermission') || hasPermission($def['view_perm']);
        $recordId = !empty($person[$def['link_column']]) ? (int) $person[$def['link_column']] : 0;
        $code = null;
        if ($recordId && $visible) {
            $stmt = $db->prepare("SELECT `{$def['code_column']}` AS code FROM `{$def['table']}` WHERE id = ? LIMIT 1");
            $stmt->execute([$recordId]);
            $code = $stmt->fetchColumn();
        }
        $codes[$role] = [
            'label'    => $def['label'],
            'module'   => $def['module'],
            'code'     => $code ? (string) $code : null,
            'record'   => $recordId,
            'visible'  => $visible,
            'status'   => $person['roles'][$role]['status'] ?? null,
            'view_url' => $recordId ? $def['view_url'] . $recordId : null,
        ];
    }
    return $codes;
}

/**
 * Reverse lookup for a module's own screens: the directory entry behind a
 * record, or null when there is none or the viewer cannot see the directory.
 */
function peoplePersonForRecord($db, $role, $recordId)
{
    $def = peopleRoleDefinition($role);
    if ($def === null || (int) $recordId <= 0) {
        return null;
    }
    if (!function_exists('hasPermission') || !hasPermission('people_management.view')) {
        return null;
    }
    $stmt = $db->prepare("SELECT id, person_code, first_name, last_name, email, status
                          FROM people WHERE `{$def['link_column']}` = ? LIMIT 1");
    $stmt->execute([(int) $recordId]);
    $person = $stmt->fetch();
    return $person ?: null;
}

/**
 * Write a role's record back onto the person and close that step.
 *
 * Short transaction of its own, taken after the module has already committed.
 * The row lock plus the status='pending' condition makes it idempotent: a
 * double submit, a replayed redirect or two tabs on the same step link once
 * and are then told the step was already recorded.
 */
function peopleOnboardingLink($db, $person, $role, $recordId)
{
    $def = peopleRoleDefinition($role);
    $recordId = (int) $recordId;
    if ($def === null || $recordId <= 0) {
        return ['ok' => false, 'message' => 'The record could not be linked to this person.'];
    }

    $linkColumn = $def['link_column'];

    try {
        $db->beginTransaction();

        $lock = $db->prepare("SELECT `$linkColumn` FROM people WHERE id = ? FOR UPDATE");
        $lock->execute([(int) $person['id']]);
        $current = $lock->fetch();

        if (!$current) {
            $db->rollBack();
            return ['ok' => false, 'message' => 'The person record no longer exists, so nothing was linked.'];
        }

        if (!empty($current[$linkColumn])) {
            // Someone linked this role already (or the column was set by hand).
            // Point the role row at the truth instead of overwriting a link.
            $db->rollBack();
            $existing = (int) $current[$linkColumn];
            return ['ok' => $existing === $recordId, 'message' => 'This person is already linked to another '
                . $def['label'] . ' record (#' . $existing . ').'];
        }

        peopleMarkRoleComplete($db, (int) $person['id'], $role, $recordId);

        $db->commit();
    } catch (Throwable $e) {
        if ($db->inTransaction()) {
            $db->rollBack();
        }
        return ['ok' => false, 'message' => 'The ' . strtolower($def['label']) . ' record was saved, but linking it to this person failed: ' . $e->getMessage()];
    }

    logAudit($_SESSION['user_id'] ?? null, 'Onboarded ' . $person['person_code'] . ' as ' . $def['label'] . " (#$recordId)", 'people_management');

    peopleOnboardingForgetInput();
    $_SESSION['people_onboarding_return'] = (int) $person['id'];

    return ['ok' => true, 'message' => $def['label'] . ' details saved and linked to ' . $person['first_name'] . '.'];
}

/**
 * Attach a module record that already exists to the person, without creating a
 * second one. Used by the coordinator's "link the existing record" recovery.
 */
function peopleOnboardingAttachExisting($db, $person, $role, $recordId)
{
    $def = peopleRoleDefinition($role);
    if ($def === null) {
        return ['ok' => false, 'message' => 'Unknown role.'];
    }
    $check = $db->prepare("SELECT COUNT(*) FROM `{$def['table']}` WHERE id = ?");
    $check->execute([(int) $recordId]);
    if ((int) $check->fetchColumn() === 0) {
        return ['ok' => false, 'message' => 'That ' . strtolower($def['label']) . ' record does not exist.'];
    }
    return peopleOnboardingLink($db, $person, $role, $recordId);
}

/**
 * Give up on a role without deleting the person or the other completed roles.
 * The step is recorded as declined, which keeps the workflow honest: an
 * unfinished onboarding is never reported as a finished one.
 */
function peopleOnboardingDecline($db, $person, $role, $reason = '')
{
    $def = peopleRoleDefinition($role);
    if ($def === null) {
        return false;
    }
    $stmt = $db->prepare("UPDATE person_roles SET status = 'declined'
                          WHERE person_id = ? AND role = ? AND status = 'pending'");
    $stmt->execute([(int) $person['id'], $role]);
    if ($stmt->rowCount() === 0) {
        return false;
    }
    logAudit($_SESSION['user_id'] ?? null,
        'Onboarding step declined: ' . $person['person_code'] . ' as ' . $def['label'] . ($reason !== '' ? ' — ' . $reason : ''),
        'people_management');
    return true;
}

/** Re-open a declined step so it can be finished later. */
function peopleOnboardingReopen($db, $person, $role)
{
    if (peopleRoleDefinition($role) === null) {
        return false;
    }
    $stmt = $db->prepare("UPDATE person_roles SET status = 'pending' WHERE person_id = ? AND role = ? AND status = 'declined'");
    $stmt->execute([(int) $person['id'], $role]);
    return $stmt->rowCount() > 0;
}

/**
 * Add a role to an existing person. Never creates a second person row, and a
 * role that is already recorded is left exactly as it is.
 */
function peopleRoleAdd($db, $person, $role)
{
    if (peopleRoleDefinition($role) === null) {
        return false;
    }
    $stmt = $db->prepare("INSERT IGNORE INTO person_roles (person_id, role, status) VALUES (?, ?, 'pending')");
    $stmt->execute([(int) $person['id'], $role]);
    return $stmt->rowCount() > 0;
}

/**
 * Remove a role from a person.
 *
 * Refuses a role that has a record behind it: unlinking would orphan a real
 * employee, customer or contractor row, and deleting it would destroy payroll,
 * invoice or contract history. That decision belongs to the module that owns
 * the record, not to the directory.
 */
function peopleRoleRemove($db, $person, $role)
{
    $def = peopleRoleDefinition($role);
    if ($def === null) {
        return ['ok' => false, 'message' => 'Unknown role.'];
    }
    if (!empty($person[$def['link_column']])) {
        return ['ok' => false, 'message' => $def['label'] . ' cannot be removed here — this person is linked to '
            . $def['module'] . '. Remove or unlink the record there first.'];
    }
    $stmt = $db->prepare("DELETE FROM person_roles WHERE person_id = ? AND role = ?");
    $stmt->execute([(int) $person['id'], $role]);
    return ['ok' => true, 'message' => $def['label'] . ' removed from this person.'];
}

/**
 * Find an existing module record for this person, so onboarding can adopt it
 * instead of creating a duplicate that the database may or may not reject.
 *
 * Employees and contractors key on email. The customer master cannot: email is
 * neither required nor unique there, and a name match would happily merge two
 * different humans, so customers are not adopted automatically.
 */
function peopleFindExistingRecord($db, $person, $role)
{
    $def = peopleRoleDefinition($role);
    $email = trim((string) $person['email']);
    if ($def === null || $email === '' || $role === 'customer') {
        return null;
    }
    $gone = !empty($def['deleted_column']) ? " AND `{$def['deleted_column']}` IS NULL" : '';
    $stmt = $db->prepare("SELECT id, `{$def['code_column']}` AS code FROM `{$def['table']}` WHERE email = ?$gone LIMIT 1");
    $stmt->execute([$email]);
    $row = $stmt->fetch();
    if (!$row) {
        return null;
    }
    // A record already claimed by another person is not a candidate.
    $taken = $db->prepare("SELECT person_code FROM people WHERE `{$def['link_column']}` = ? AND id <> ? LIMIT 1");
    $taken->execute([(int) $row['id'], (int) $person['id']]);
    if ($other = $taken->fetch()) {
        $row['claimed_by'] = $other['person_code'];
    }
    return $row;
}

/** Where the wizard hands the user back to. */
function peopleOnboardingUrl($personId, $extra = '')
{
    return 'modules/people_management/onboarding.php?person_id=' . (int) $personId . $extra;
}

/**
 * Drop the seeded identity from the shared old-input slot.
 *
 * $_SESSION['_old_input'] is global, so values placed here for a module form
 * are still sitting there the next time any unrelated form renders — and the
 * customer form never clears it on a GET. Leaving the wizard always clears.
 */
function peopleOnboardingForgetInput()
{
    if (function_exists('clearOldInput')) {
        clearOldInput();
    } else {
        unset($_SESSION['_old_input']);
    }
}

/** One-shot: did a step have to be saved before the record could be linked? */
function peopleOnboardingReturnPending($personId)
{
    return isset($_SESSION['people_onboarding_return'])
        && (int) $_SESSION['people_onboarding_return'] === (int) $personId;
}

function peopleOnboardingClearReturn()
{
    unset($_SESSION['people_onboarding_return']);
}
/**
 * A module record has just been deleted. Make the directory tell the truth.
 *
 * The FK is ON DELETE SET NULL, so `people.employee_id` goes back to NULL by
 * itself — but `person_roles` still claims the role is complete and points at a
 * record that no longer exists. Until that is corrected the directory advertises
 * a relationship it cannot show, which is worse than an empty one.
 *
 * A person left with no record in any category and no login account is a shell:
 * it exists only to represent the record that has just gone, so it is removed
 * too, with the reason in the audit log. Anything that still holds a login, or a
 * second category, is kept and its reopened step is left for someone to finish.
 */
function peopleForfeitRecord($db, $role, $recordId)
{
    $def = peopleRoleDefinition($role);
    if ($def === null) {
        return ['reopened' => 0, 'removed' => 0];
    }

    $stmt = $db->prepare("SELECT person_id FROM person_roles WHERE role = ? AND record_id = ?");
    $stmt->execute([$role, (int) $recordId]);
    $personIds = array_column($stmt->fetchAll(), 'person_id');

    $reopened = 0;
    $removed = 0;

    try {
        $db->beginTransaction();

        // The stale claim goes first, whatever happens to the row afterwards.
        $db->prepare("UPDATE person_roles SET status = 'pending', record_id = NULL, completed_at = NULL
                      WHERE role = ? AND record_id = ?")->execute([$role, (int) $recordId]);

        foreach ($personIds as $personId) {
            $personId = (int) $personId;
            $live = 0;
            foreach (peopleRoleDefinitions() as $otherRole => $otherDef) {
                $row = $db->prepare("SELECT `{$otherDef['link_column']}` FROM people WHERE id = ? LIMIT 1");
                $row->execute([$personId]);
                if ($row->fetchColumn()) {
                    $live++;
                }
            }
            $detail = $db->prepare("SELECT person_code, first_name, last_name, user_id FROM people WHERE id = ? LIMIT 1");
            $detail->execute([$personId]);
            $person = $detail->fetch();
            if (!$person) {
                continue;
            }

            if ($live === 0 && empty($person['user_id'])) {
                $db->prepare("DELETE FROM people WHERE id = ?")->execute([$personId]);
                logAudit($_SESSION['user_id'] ?? null,
                    'Removed ' . $person['person_code'] . ' — its last ' . strtolower($def['label'])
                    . ' record #' . (int) $recordId . ' was deleted', 'people_management');
                $removed++;
                continue;
            }

            // Still something to come back for: say so on the person, not just in a log.
            logAudit($_SESSION['user_id'] ?? null,
                $person['person_code'] . ' lost its ' . strtolower($def['label'])
                . ' record #' . (int) $recordId . ' — step reopened', 'people_management');
            $reopened++;
        }

        $db->commit();
    } catch (Throwable $e) {
        if ($db->inTransaction()) {
            $db->rollBack();
        }
        error_log('peopleForfeitRecord failed: ' . $e->getMessage());
    }

    return ['reopened' => $reopened, 'removed' => $removed];
}

/**
 * Records that exist in a module but have no directory entry.
 *
 * People Management is the assembly point: an employee, contractor or individual
 * customer that nobody can find in the directory is a gap in it, so the list page
 * shows the count and offers to close it rather than leaving the CLI auditor as
 * the only way to discover the difference.
 */
function peopleUnlistedRecords($db)
{
    $found = [];
    foreach (peopleRoleDefinitions() as $role => $def) {
        $deleted = !empty($def['deleted_column']) ? "AND c.`{$def['deleted_column']}` IS NULL" : '';
        $individual = ($role === 'customer') ? "AND c.customer_type = 'individual'" : '';
        // The customer master has no first/last name columns, so the display
        // name comes from a different place per module.
        $name = ($def['identity_mode'] ?? '') === 'split_name'
            ? "CONCAT_WS(' ', c.first_name, c.last_name)"
            : 'c.company_name';
        $rows = $db->query("SELECT c.id, c.`{$def['code_column']}` AS code, $name AS nm
                            FROM `{$def['table']}` c
                            LEFT JOIN people p ON p.`{$def['link_column']}` = c.id
                            WHERE p.id IS NULL $deleted $individual
                            ORDER BY 2")->fetchAll();
        foreach ($rows as $r) {
            $found[] = ['role' => $role, 'id' => (int) $r['id'], 'code' => $r['code'], 'name' => trim((string) $r['nm'])];
        }
    }
    return $found;
}

/**
 * Put every unlisted record into the directory through the normal path.
 *
 * This is the same decision the save hook makes — reuse a person matched on
 * email, otherwise mint a Person Code — so a click on the list page cannot
 * create an identity that the modules would not have created themselves.
 */
function peopleSyncDirectory($db)
{
    $tallies = ['created' => 0, 'attached' => 0, 'already' => 0, 'skipped' => 0, 'conflict' => 0, 'failed' => 0];
    $notes = [];
    foreach (peopleUnlistedRecords($db) as $record) {
        $result = peopleEnsurePersonForRecord($db, $record['role'], $record['id']);
        $action = $result['action'];
        $tallies[$action] = ($tallies[$action] ?? 0) + 1;
        if ($action === 'conflict' || $action === 'failed') {
            $notes[] = $record['code'] . ': ' . $result['message'];
        }
    }
    return ['tallies' => $tallies, 'notes' => $notes];
}

/**
 * Directory entries with nothing behind them: no employee, no customer, no
 * contractor, and no login account.
 *
 * These are what a module deletion leaves if it happens without
 * peopleForfeitRecord() — restored dumps, hand-edited SQL, deletes made before
 * this existed. The person is not wrong, but with nothing to represent it is
 * noise on the page that is supposed to be the assembled view of everyone.
 */
function peopleShellPeople($db)
{
    return $db->query("SELECT id, person_code, first_name, last_name, email, created_at
                       FROM people
                       WHERE employee_id IS NULL AND customer_id IS NULL AND contractor_id IS NULL
                         AND user_id IS NULL
                       ORDER BY first_name, id")->fetchAll();
}

/**
 * Remove shell entries, reporting what was dropped.
 *
 * Deliberately refuses anything that still holds a link or a login account, so
 * this can never take a real person out of the directory: it clears rows that no
 * longer describe anything. The cascade on person_roles handles their role rows.
 */
function peoplePruneShells($db)
{
    $removed = [];
    $stmt = $db->prepare("SELECT id, person_code, first_name, last_name FROM people
                          WHERE employee_id IS NULL AND customer_id IS NULL
                            AND contractor_id IS NULL AND user_id IS NULL");
    $stmt->execute();
    $rows = $stmt->fetchAll();

    foreach ($rows as $row) {
        try {
            $db->beginTransaction();
            // Re-check under the transaction: a save in another tab may have
            // linked this person between the list and the delete.
            $guard = $db->prepare("SELECT id FROM people WHERE id = ?
                                   AND employee_id IS NULL AND customer_id IS NULL
                                   AND contractor_id IS NULL AND user_id IS NULL");
            $guard->execute([(int) $row['id']]);
            if (!$guard->fetch()) {
                $db->rollBack();
                continue;
            }
            $db->prepare("DELETE FROM people WHERE id = ?")->execute([(int) $row['id']]);
            $db->commit();
            $removed[] = $row['person_code'];
            logAudit($_SESSION['user_id'] ?? null,
                'Removed ' . $row['person_code'] . ' (' . trim($row['first_name'] . ' ' . (string) $row['last_name'])
                . ') — no record in any category', 'people_management');
        } catch (Throwable $e) {
            if ($db->inTransaction()) {
                $db->rollBack();
            }
        }
    }
    return $removed;
}

/**
 * Persist the truth the list already derives: a role marked complete whose record
 * no longer exists is an open step, not a finished one.
 *
 * Non-destructive. Nothing is removed and no person is touched — only the stale
 * claim is corrected, so the audit, the profile and the tiles stop disagreeing
 * with each other. This is the same repair peopleLoad() performs when someone
 * opens a person; this does it for every person at once.
 */
function peopleReconcileRoles($db)
{
    $repaired = [];
    foreach (peopleRoleDefinitions() as $role => $def) {
        $deleted = !empty($def['deleted_column']) ? "AND r.`{$def['deleted_column']}` IS NULL" : '';
        $stmt = $db->prepare("SELECT pr.id, pr.person_id, p.person_code
                               FROM person_roles pr
                               JOIN people p ON p.id = pr.person_id
                               LEFT JOIN `{$def['table']}` r ON r.id = pr.record_id $deleted
                               WHERE pr.role = ? AND pr.status = 'complete' AND r.id IS NULL");
        $stmt->execute([$role]);
        $rows = $stmt->fetchAll();
        if (!$rows) {
            continue;
        }
        $db->prepare("UPDATE person_roles SET status = 'pending', record_id = NULL, completed_at = NULL
                      WHERE role = ? AND status = 'complete'
                        AND (record_id IS NULL OR record_id NOT IN (SELECT id FROM `{$def['table']}` WHERE 1 $deleted))")
           ->execute([$role]);
        foreach ($rows as $row) {
            $repaired[] = $row['person_code'] . '/' . $role;
        }
    }
    if ($repaired) {
        logAudit($_SESSION['user_id'] ?? null,
            'Reconciled ' . count($repaired) . ' stale person-type row(s) after record deletions', 'people_management');
    }
    return $repaired;
}

/**
 * The photograph of a person, wherever it is kept.
 *
 * `people` has no photo column by design: the passport-size image is uploaded
 * and owned by the module that verifies identity — HRMS for an employee, the
 * contractor register for a contractor. So a directory page reads the photo from
 * the linked record instead of collecting a second copy that would drift.
 *
 * Returns null when nobody has uploaded one, which is what the initials avatar
 * is for. `exists` is checked on disk as well, because the uploaded files live
 * outside the database: restoring only the SQL leaves every path pointing at
 * nothing, and a broken image tag is worse than an honest initial.
 */
function peoplePhotoFor($db, $person)
{
    foreach (['employee', 'contractor'] as $role) {
        $def = peopleRoleDefinition($role);
        $recordId = !empty($person[$def['link_column']]) ? (int) $person[$def['link_column']] : 0;
        if ($recordId <= 0) {
            continue;
        }
        $stmt = $db->prepare("SELECT photo_path FROM `{$def['table']}` WHERE id = ? LIMIT 1");
        $stmt->execute([$recordId]);
        $path = $stmt->fetchColumn();
        if (!$path) {
            continue;
        }
        $path = (string) $path;
        return [
            'path'   => $path,
            'role'   => $role,
            'module' => $def['module'],
            'record' => $recordId,
            'code'   => $def['code_column'],
            'exists' => is_file(dirname(__DIR__) . '/' . ltrim($path, '/')),
        ];
    }
    return null;
}

/**
 * Photo paths for a whole page of people, in the list query itself.
 *
 * One lookup per row would be fifteen stat calls plus fifteen queries for a page
 * that is meant to be scanned, so the list selects both columns and this picks
 * the same way peoplePhotoFor() does: employee first, contractor second.
 */
function peoplePhotoFromRow(array $row)
{
    if (!empty($row['employee_photo'])) {
        $role = 'employee';
        $path = $row['employee_photo'];
    } elseif (!empty($row['contractor_photo'])) {
        $role = 'contractor';
        $path = $row['contractor_photo'];
    } else {
        return null;
    }
    return ['role' => $role, 'path' => $path];
}
