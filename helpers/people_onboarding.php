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
 * Deliberately does not reconcile — that needs per-row existence checks and
 * would cost three queries per person on a page of fifteen.
 */
function peopleRoleSummary($db, array $personIds)
{
    if (!$personIds) {
        return [];
    }
    $in = implode(',', array_fill(0, count($personIds), '?'));
    $stmt = $db->prepare("SELECT person_id, role, status FROM person_roles WHERE person_id IN ($in)");
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
