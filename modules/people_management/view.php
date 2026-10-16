<?php
$pageTitle = 'View Person';
require_once '../../includes/header.php';
require_once '../../helpers/people_onboarding.php';
require_once '../../helpers/account.php';
require_once '../../helpers/attachment_storage.php';
require_once __DIR__ . '/../contractors/document_service.php';
require_once __DIR__ . '/../contractors/contract_service.php';

if (!hasPermission('people_management.view')) {
    die('Access Denied');
}

$db = getDB();
$id = (int)($_GET['id'] ?? 0);

// peopleLoad() gives the person, their role set, and repairs any role whose
// module record no longer exists, so this page cannot advertise a link that
// has been deleted behind its back.
$person = peopleLoad($db, $id);

if (!$person) {
    flash('error', 'Person not found', 'error');
    to('modules/people_management/index.php');
}

$loginUser = null;
if (!empty($person['user_id'])) {
    $userStmt = $db->prepare("SELECT name, email, status FROM users WHERE id = ? LIMIT 1");
    $userStmt->execute([(int) $person['user_id']]);
    $loginUser = $userStmt->fetch();
}
$person['user_name'] = $loginUser['name'] ?? null;
$person['user_email'] = $loginUser['email'] ?? null;
$person['user_status'] = $loginUser['status'] ?? null;

// Load linked employee data if applicable
$employee = null;
if ($person['employee_id']) {
    $empStmt = $db->prepare("
        SELECT e.*, d.department_name, desig.designation_name
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        LEFT JOIN designations desig ON e.designation_id = desig.id
        WHERE e.id = ?
    ");
    $empStmt->execute([$person['employee_id']]);
    $employee = $empStmt->fetch();
}

// Get user roles if login exists
$userRoles = [];
if ($person['user_id']) {
    $roleStmt = $db->prepare("
        SELECT r.name FROM roles r
        JOIN user_roles ur ON r.id = ur.role_id
        WHERE ur.user_id = ?
    ");
    $roleStmt->execute([$person['user_id']]);
    $userRoles = $roleStmt->fetchAll(PDO::FETCH_COLUMN);
}

// A directory entry with no login is the dead end this panel exists to close.
// Creating the account needs the right to create users *and* to edit this person,
// because the point is to attach one to the other.
$canGrantLogin = !$person['user_id']
              && hasPermission('users.create')
              && hasPermission('people_management.edit');
$grantableRoles = [];
if ($canGrantLogin) {
    $allRoleIds = $db->query("SELECT id FROM roles WHERE deleted_at IS NULL")
                     ->fetchAll(PDO::FETCH_COLUMN);
    $allowed = accountGrantableRoleIds($db, $allRoleIds, $_SESSION['user_id'])['ids'];
    if ($allowed) {
        $in = implode(',', array_fill(0, count($allowed), '?'));
        $stmt = $db->prepare("SELECT id, name FROM roles WHERE id IN ($in) ORDER BY name");
        $stmt->execute(array_values($allowed));
        $grantableRoles = $stmt->fetchAll();
    } else {
        $canGrantLogin = false;
    }
}

// An account that exists but is attached to nobody is not a reason to create another.
$orphanLogin = $person['user_id'] ? null : accountUnclaimedForPerson($db, $person);

$catLabels = ['employee' => 'Employee', 'customer' => 'Customer', 'contractor' => 'Contractor'];
$catColors = ['employee' => 'bg-blue-100 text-blue-800', 'customer' => 'bg-purple-100 text-purple-800', 'contractor' => 'bg-orange-100 text-orange-800'];

// Every code this person holds, filtered by what the viewer is allowed to see.
$codes = peopleIdentityCodes($db, $person);
// The image itself belongs to the employee or contractor record; the directory
// reads it rather than keeping a second copy that could disagree.
$personPhoto = peoplePhotoFor($db, $person);
$stateChip = ['complete' => 'bg-green-100 text-green-800', 'pending' => 'bg-amber-100 text-amber-800', 'declined' => 'bg-gray-100 text-gray-500'];
?>
<div class="mb-6 flex justify-between items-center">
    <div class="flex items-start gap-4">
        <?php if ($personPhoto && $personPhoto['exists']): ?>
            <button type="button" onclick="attachmentViewerOpen(this)"
                    data-url="<?= attachmentFileUrl($personPhoto['path']) ?>"
                    data-mime="<?= attachmentMimeFromPath($personPhoto['path']) ?>"
                    data-name="Profile photo — <?= sanitize(trim($person['first_name'] . ' ' . (string) $person['last_name'])) ?>"
                    class="shrink-0" title="Photo from the <?= strtolower($personPhoto['module']) ?> record — click to view">
                <img src="<?= attachmentFileUrl($personPhoto['path']) ?>"
                     alt="<?= sanitize(trim($person['first_name'] . ' ' . (string) $person['last_name'])) ?>"
                     class="h-20 w-20 rounded-full object-cover border-2 border-white shadow">
            </button>
        <?php else: ?>
            <div class="h-20 w-20 rounded-full bg-gray-700 text-white flex items-center justify-center text-2xl font-bold shrink-0"
                 <?= $personPhoto ? 'title="A photo is recorded but the file is not on this server — the uploads/ folder is not part of the SQL dump"' : 'title="No profile photo on the employee or contractor record"' ?>>
                <?= strtoupper(substr($person['first_name'], 0, 1)) ?><?= strtoupper(substr((string) $person['last_name'], 0, 1)) ?>
            </div>
        <?php endif; ?>
        <div>
        <a href="index.php" class="text-blue-600 hover:text-blue-900 mb-2 inline-block">
            <i class="fas fa-arrow-left mr-1"></i>Back to People
        </a>
        <h1 class="text-2xl font-bold text-gray-800"><?= sanitize($person['first_name'] . ' ' . $person['last_name']) ?></h1>
        <p class="text-gray-600">
            <?php
            $displayRoles = $person['roles'];
            if (!$displayRoles && !empty($person['category'])) {
                $displayRoles = [$person['category'] => ['status' => 'complete', 'record_id' => null]];
            }
            foreach (peopleRoleDefinitions() as $roleKey => $def):
                if (!isset($displayRoles[$roleKey])) continue;
                $state = $displayRoles[$roleKey]['status'];
                $chip = $state === 'complete'
                    ? ($catColors[$roleKey] ?? 'bg-gray-100 text-gray-800')
                    : ($state === 'declined' ? 'bg-gray-100 text-gray-400' : 'bg-amber-100 text-amber-800');
            ?>
            <span class="px-2 py-0.5 text-xs rounded <?= $chip ?>">
                <?= $catLabels[$roleKey] ?? ucfirst($roleKey) ?><?php if ($state !== 'complete'): ?> &middot; <?= $state === 'declined' ? 'declined' : 'to complete' ?><?php endif; ?>
            </span>
            <?php endforeach; ?>
            <span class="ml-2 text-sm">Code: <?= sanitize($person['person_code']) ?></span>
        </p>
        </div>
    </div>
    <div class="flex gap-2">
        <?php if (hasPermission('people_management.edit')): ?>
        <a href="edit.php?id=<?= $person['id'] ?>" class="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600 transition">
            <i class="fas fa-edit mr-2"></i>Edit
        </a>
        <?php endif; ?>
    </div>
</div>

<div class="bg-white rounded-lg shadow p-6 mb-6">
    <h3 class="text-lg font-semibold text-gray-800 mb-1 border-b pb-2">Identity &amp; Codes</h3>
    <p class="text-xs text-gray-500 mb-4">
        One person, one Person Code. Each category they belong to carries its own code, assigned by that
        module and linked here.
    </p>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="border rounded-lg p-3 bg-gray-50">
            <div class="text-xs text-gray-500 uppercase tracking-wide">Person Code</div>
            <div class="font-mono font-semibold text-gray-900 mt-1"><?= sanitize($person['person_code']) ?></div>
            <div class="text-xs mt-1">
                <span class="px-2 py-0.5 text-xs rounded <?= $person['status'] === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-700' ?>">
                    <?= ucfirst($person['status']) ?>
                </span>
            </div>
        </div>
        <?php foreach ($codes as $roleKey => $info): ?>
        <div class="border rounded-lg p-3 <?= $info['code'] ? '' : 'opacity-70' ?>">
            <div class="text-xs text-gray-500 uppercase tracking-wide"><?= $info['label'] ?> Code</div>
            <div class="font-mono font-semibold mt-1 <?= $info['code'] ? 'text-gray-900' : 'text-gray-400' ?>">
                <?php if ($info['code']): ?>
                    <?= sanitize($info['code']) ?>
                <?php elseif (!$info['visible']): ?>
                    <span class="text-xs font-sans italic">restricted</span>
                <?php elseif ($info['status'] === 'pending'): ?>
                    <span class="text-xs font-sans italic">not issued yet</span>
                <?php else: ?>
                    <span class="text-gray-400">&mdash;</span>
                <?php endif; ?>
            </div>
            <div class="text-xs mt-1">
                <?php if ($info['status'] === null): ?>
                    <span class="text-gray-400">— not in this category</span>
                <?php elseif ($info['code']): ?>
                    <a href="<?= url($info['view_url']) ?>" class="text-blue-600 hover:text-blue-900">
                        <i class="fas fa-external-link-alt text-xs mr-1"></i><?= $info['module'] ?>
                    </a>
                <?php else: ?>
                    <span class="px-2 py-0.5 rounded <?= $stateChip[$info['status']] ?? 'bg-gray-100 text-gray-700' ?>">
                        <?= $info['status'] === 'pending' ? 'awaiting details' : ucfirst((string) $info['status']) ?>
                    </span>
                <?php endif; ?>
            </div>
        </div>
        <?php endforeach; ?>
    </div>
</div>

<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Main Info -->
    <div class="lg:col-span-2 space-y-6">
        <!-- Person Details -->
        <div class="bg-white rounded-lg shadow p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">Personal Details</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">First Name</div>
                    <div class="font-medium"><?= sanitize($person['first_name']) ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Last Name</div>
                    <div class="font-medium"><?= sanitize($person['last_name'] ?? '-') ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Email</div>
                    <div class="font-medium"><?= sanitize($person['email'] ?? '-') ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Phone</div>
                    <div class="font-medium"><?= sanitize($person['phone'] ?? '-') ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Gender</div>
                    <div class="font-medium"><?= $person['gender'] ? ucfirst($person['gender']) : '-' ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Date of Birth</div>
                    <div class="font-medium"><?= $person['date_of_birth'] ? date('M d, Y', strtotime($person['date_of_birth'])) : '-' ?></div>
                </div>
                <div class="md:col-span-2">
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Address</div>
                    <div class="font-medium"><?= sanitize($person['address'] ?? '-') ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Status</div>
                    <div>
                        <span class="px-2 py-1 text-xs rounded <?= $person['status'] === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800' ?>">
                            <?= ucfirst($person['status']) ?>
                        </span>
                    </div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Created</div>
                    <div class="font-medium"><?= date('M d, Y h:i A', strtotime($person['created_at'])) ?></div>
                </div>
            </div>
            <?php if ($person['notes']): ?>
            <div class="mt-4 pt-4 border-t">
                <div class="text-xs text-gray-500 uppercase tracking-wide mb-1">Notes</div>
                <div class="text-gray-700"><?= nl2br(sanitize($person['notes'])) ?></div>
            </div>
            <?php endif; ?>
        </div>

        <!-- Onboarding still open -->
        <?php $openRoles = peoplePendingRoles($person); ?>
        <?php if ($openRoles): ?>
        <div class="bg-amber-50 border border-amber-200 rounded-lg p-6 mb-6">
            <h3 class="text-lg font-semibold text-amber-900 mb-1">Onboarding incomplete</h3>
            <p class="text-sm text-amber-800 mb-3">
                <?= count($openRoles) ?> selected person type<?= count($openRoles) === 1 ? '' : 's' ?> still
                <?= count($openRoles) === 1 ? 'needs' : 'need' ?> details in
                <?= htmlspecialchars(implode(', ', array_map(fn($d) => $d['module'], $openRoles)), ENT_QUOTES) ?>.
                The person record and every completed role are already saved.
            </p>
            <a href="onboarding.php?person_id=<?= $person['id'] ?>" class="inline-block px-4 py-2 bg-amber-600 text-white text-sm rounded hover:bg-amber-700">
                <i class="fas fa-list-check mr-1"></i>Continue onboarding
            </a>
        </div>
        <?php endif; ?>

        <!-- Linked Customer -->
        <?php
        $linkedCustomer = null;
        if (!empty($person['customer_id'])) {
            $custStmt = $db->prepare("SELECT id, client_code, company_name, status, currency_code, credit_limit FROM clients WHERE id = ? AND deleted_at IS NULL");
            $custStmt->execute([$person['customer_id']]);
            $linkedCustomer = $custStmt->fetch();
        }
        ?>
        <?php if ($linkedCustomer): ?>
        <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
                Customer Master
                <a href="<?= url('modules/customers/view.php?id=' . $linkedCustomer['id']) ?>" class="text-blue-600 text-sm font-normal ml-2">
                    <i class="fas fa-external-link-alt mr-1"></i>Open Customer Record
                </a>
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Customer Code</div>
                    <div class="font-medium font-mono"><?= sanitize($linkedCustomer['client_code']) ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Organisation</div>
                    <div class="font-medium"><?= sanitize($linkedCustomer['company_name']) ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Status</div>
                    <div class="font-medium capitalize"><?= sanitize($linkedCustomer['status']) ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Credit Limit</div>
                    <div class="font-medium"><?= sanitize($linkedCustomer['currency_code'] . ' ' . number_format((float) $linkedCustomer['credit_limit'], 2)) ?></div>
                </div>
            </div>
        </div>
        <?php endif; ?>

        <!-- Linked Contractor Register -->
        <?php
        // Register data (contracts, rates, compliance) is only shown to holders
        // of contractors.view; the directory itself does not imply that right.
        $linkedContractor = null;
        $canSeeRegister = hasPermission('contractors.view');
        if ($canSeeRegister && !empty($person['contractor_id'])) {
            $ctrStmt = $db->prepare("SELECT * FROM contractors WHERE id = ? AND deleted_at IS NULL");
            $ctrStmt->execute([$person['contractor_id']]);
            $linkedContractor = $ctrStmt->fetch();
        }
        ?>
        <?php if ($canSeeRegister && ($person['roles']['contractor']['status'] ?? '') === 'pending' && !$linkedContractor): ?>
        <div class="bg-white rounded-lg shadow p-6 mb-6 border-l-4 border-orange-400">
            <h3 class="text-lg font-semibold text-gray-800 mb-2">Not on the contractor register</h3>
            <p class="text-sm text-gray-600 mb-3">
                This person was selected as a contractor but has no register entry, so their right-to-work
                documents and engagement contracts have nowhere to live.
            </p>
            <?php if (hasPermission('contractors.create')): ?>
            <a href="<?= url('modules/contractors/form.php?person_id=' . $person['id']) ?>" class="px-4 py-2 bg-indigo-600 text-white text-sm rounded hover:bg-indigo-700">
                <i class="fas fa-user-plus mr-1"></i>Complete the contractor step
            </a>
            <?php endif; ?>
        </div>
        <?php elseif ($linkedContractor): ?>
        <?php
        $ctrCurrent = contractorCurrentContract($db, (int) $linkedContractor['id']);
        $ctrDates = array_filter([
            $linkedContractor['emirates_id_expiry'], $linkedContractor['passport_expiry'],
            $linkedContractor['visa_expiry'], $linkedContractor['work_permit_expiry'], $linkedContractor['labor_card_expiry'],
        ]);
        $ctrWorst = null;
        foreach ($ctrDates as $d) {
            $days = intdiv(strtotime($d) - time(), 86400);
            if ($ctrWorst === null || $days < $ctrWorst) { $ctrWorst = $days; }
        }
        $ctrState = $ctrWorst === null ? ['label' => 'No dates recorded', 'class' => 'bg-gray-100 text-gray-600']
            : ($ctrWorst < 0 ? ['label' => 'Expired ' . abs($ctrWorst) . ' days ago', 'class' => 'bg-red-100 text-red-700']
            : ($ctrWorst <= 60 ? ['label' => 'Expires in ' . $ctrWorst . ' days', 'class' => 'bg-amber-100 text-amber-700']
            : ['label' => 'All documents valid', 'class' => 'bg-green-100 text-green-700']));
        ?>
        <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
                Contractor Register
                <a href="<?= url('modules/contractors/view.php?id=' . $linkedContractor['id']) ?>" class="text-blue-600 text-sm font-normal ml-2">
                    <i class="fas fa-external-link-alt mr-1"></i>Open Contractor Profile
                </a>
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Contractor Code</div>
                    <div class="font-medium font-mono"><?= sanitize($linkedContractor['contractor_code']) ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Register Status</div>
                    <div class="font-medium capitalize"><?= sanitize($linkedContractor['status']) ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Current Contract</div>
                    <div class="font-medium">
                        <?php if ($ctrCurrent): ?>
                            <?= sanitize($ctrCurrent['contract_number']) ?>
                            <span class="block text-xs text-gray-500 font-normal">
                                <?= $ctrCurrent['end_date'] ? 'ends ' . date('M d, Y', strtotime($ctrCurrent['end_date'])) : 'open-ended' ?>
                            </span>
                        <?php else: ?>
                            <span class="text-gray-400">None</span>
                        <?php endif; ?>
                    </div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Compliance</div>
                    <div class="mt-1"><span class="px-2 py-0.5 text-xs rounded <?= $ctrState['class'] ?>"><?= $ctrState['label'] ?></span></div>
                </div>
            </div>
        </div>
        <?php endif; ?>

        <!-- Employee Details -->
        <?php if ($employee): ?>
        <div class="bg-white rounded-lg shadow p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
                Employee Record
                <a href="<?= url('modules/employees/view.php?id=' . $employee['id']) ?>" class="text-blue-600 text-sm font-normal ml-2">
                    <i class="fas fa-external-link-alt mr-1"></i>View in Employees Module
                </a>
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Employee Code</div>
                    <div class="font-medium"><?= sanitize($employee['employee_code']) ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Department</div>
                    <div class="font-medium"><?= sanitize($employee['department_name'] ?? '-') ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Designation</div>
                    <div class="font-medium"><?= sanitize($employee['designation_name'] ?? '-') ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Joining Date</div>
                    <div class="font-medium"><?= $employee['joining_date'] ? date('M d, Y', strtotime($employee['joining_date'])) : '-' ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Employment Type</div>
                    <div class="font-medium"><?= ucfirst(str_replace('_', ' ', $employee['employment_type'] ?? '-')) ?></div>
                </div>
                <div>
                    <div class="text-xs text-gray-500 uppercase tracking-wide">Work Location</div>
                    <div class="font-medium"><?= sanitize($employee['work_location'] ?? '-') ?></div>
                </div>
            </div>
        </div>
        <?php endif; ?>
    </div>

    <!-- Sidebar -->
    <div class="space-y-6">
        <!-- System Access -->
        <div class="bg-white rounded-lg shadow p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">System Access</h3>
            <?php if ($person['user_id']): ?>
                <div class="space-y-3">
                    <div>
                        <div class="text-xs text-gray-500 uppercase tracking-wide">Login Email</div>
                        <div class="font-medium"><?= sanitize($person['user_email'] ?? '-') ?></div>
                    </div>
                    <div>
                        <div class="text-xs text-gray-500 uppercase tracking-wide">Login Name</div>
                        <div class="font-medium"><?= sanitize($person['user_name'] ?? '-') ?></div>
                    </div>
                    <div>
                        <div class="text-xs text-gray-500 uppercase tracking-wide">Account Status</div>
                        <span class="px-2 py-1 text-xs rounded <?= $person['user_status'] === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800' ?>">
                            <?= ucfirst($person['user_status'] ?? 'unknown') ?>
                        </span>
                    </div>
                    <?php if ($userRoles): ?>
                    <div>
                        <div class="text-xs text-gray-500 uppercase tracking-wide mb-1">Login roles</div>
                        <?php foreach ($userRoles as $role): ?>
                        <span class="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded mr-1"><?= sanitize($role) ?></span>
                        <?php endforeach; ?>
                        <?php if (hasPermission('users.edit')): ?>
                        <p class="text-xs text-gray-500 mt-1">
                            Roles decide what the login may do, and are separate from the person types above.
                            <a href="<?= url('modules/users/edit.php?id=' . (int) $person['user_id']) ?>" class="text-blue-600 hover:text-blue-900">
                                <i class="fas fa-user-gear mr-1"></i>Change this login's role
                            </a>
                        </p>
                        <?php endif; ?>
                    </div>
                    <?php endif; ?>
                    <div class="pt-2">
                        <a href="<?= url('modules/users/view.php?id=' . $person['user_id']) ?>" class="text-blue-600 text-sm hover:text-blue-800">
                            <i class="fas fa-external-link-alt mr-1"></i>View User Record
                        </a>
                    </div>
                    <?php if (hasPermission('users.edit') && hasPermission('people_management.edit')): ?>
                    <form method="post" action="login.php" class="pt-2 border-t"
                          onsubmit="return confirm('Unlink this login from <?= sanitize($person['person_code']) ?>? The account stays and can be attached again later; neither it nor this person is deleted.');">
                        <input type="hidden" name="csrf_token" value="<?= csrfToken() ?>">
                        <input type="hidden" name="id" value="<?= $person['id'] ?>">
                        <input type="hidden" name="account_action" value="detach">
                        <button type="submit" class="text-xs text-gray-500 hover:text-red-700">
                            <i class="fas fa-link-slash mr-1"></i>Unlink this login from the person
                        </button>
                    </form>
                    <?php endif; ?>
                </div>
            <?php else: ?>
                <?php if ($orphanLogin && hasPermission('users.edit') && hasPermission('people_management.edit')): ?>
                <form method="post" action="login.php" class="space-y-2 mb-4 p-3 bg-blue-50 rounded border border-blue-200">
                    <input type="hidden" name="csrf_token" value="<?= csrfToken() ?>">
                    <input type="hidden" name="id" value="<?= $person['id'] ?>">
                    <input type="hidden" name="account_action" value="link">
                    <input type="hidden" name="user_id" value="<?= (int) $orphanLogin['id'] ?>">
                    <p class="text-sm text-gray-700">
                        <i class="fas fa-link mr-1 text-blue-600"></i>
                        An account already exists for <strong><?= sanitize($orphanLogin['email']) ?></strong>
                        (<?= sanitize($orphanLogin['name']) ?>, <?= sanitize($orphanLogin['status']) ?>)
                        and no directory entry claims it.
                    </p>
                    <button type="submit" class="bg-blue-600 text-white px-3 py-1.5 rounded hover:bg-blue-700 transition text-sm">
                        <i class="fas fa-link mr-1"></i>Link the existing account
                    </button>
                </form>
                <?php endif; ?>
            <?php endif; ?>
            <?php if (!$person['user_id'] && $canGrantLogin): ?>
                <form method="post" action="login.php" class="space-y-3">
                    <input type="hidden" name="csrf_token" value="<?= csrfToken() ?>">
                    <input type="hidden" name="id" value="<?= $person['id'] ?>">
                    <input type="hidden" name="account_action" value="grant">
                    <p class="text-sm text-gray-600">
                        <i class="fas fa-user-plus mr-1 text-blue-500"></i>
                        Give <strong><?= sanitize($person['first_name']) ?></strong> a login account.
                        This creates the sign-in record and attaches it to this directory entry, so the
                        person keeps one record with all of their codes.
                    </p>
                    <div>
                        <label class="block text-xs text-gray-500 uppercase tracking-wide mb-1" for="login_name">Name on the login</label>
                        <input type="text" id="login_name" name="name" required maxlength="100"
                           value="<?= sanitize(trim($person['first_name'] . ' ' . (string) $person['last_name'])) ?>"
                           class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                    <div>
                        <label class="block text-xs text-gray-500 uppercase tracking-wide mb-1" for="login_email">Login email</label>
                        <input type="email" id="login_email" name="email" required
                           value="<?= sanitize($person['email']) ?>" placeholder="person@company.com" autocomplete="off"
                           class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <?php if (empty($person['email'])): ?>
                        <p class="text-xs text-amber-600 mt-1">This person has no email on file — type the address they will sign in with.</p>
                        <?php endif; ?>
                    </div>
                    <div>
                        <label class="block text-xs text-gray-500 uppercase tracking-wide mb-1" for="login_password">Password</label>
                        <input type="password" id="login_password" name="password" required minlength="6" autocomplete="new-password"
                           class="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <p class="text-xs text-gray-500 mt-1">At least 6 characters. Share it with the person directly — the system does not email passwords.</p>
                    </div>
                    <div>
                        <span class="block text-xs text-gray-500 uppercase tracking-wide mb-1">Roles</span>
                        <?php foreach ($grantableRoles as $role): ?>
                        <label class="inline-flex items-center mr-4 mb-1 text-sm">
                            <input type="checkbox" name="roles[]" value="<?= (int) $role['id'] ?>" class="rounded text-blue-600"
                                <?= (int) $role['id'] === 3 ? 'checked' : '' ?>>
                            <span class="ml-2"><?= sanitize($role['name']) ?></span>
                        </label>
                        <?php endforeach; ?>
                        <p class="text-xs text-gray-500 mt-1">
                            Only roles your own account holds can be handed out. Saving without a tick leaves
                            the account able to sign in but unable to open any module.
                        </p>
                    </div>
                    <div class="flex items-center gap-3 pt-1">
                        <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition text-sm">
                            <i class="fas fa-user-plus mr-1"></i>Create login &amp; attach
                        </button>
                        <a href="<?= url('modules/users/create.php') ?>" class="text-xs text-gray-500 hover:text-gray-700">
                            Need a standalone account? Use Users
                        </a>
                    </div>
                </form>
            <?php elseif (!$person['user_id']): ?>
                <div class="text-center py-4">
                    <i class="fas fa-user-slash text-gray-300 text-4xl mb-2"></i>
                    <p class="text-gray-500 text-sm">No login credentials created</p>
                    <p class="text-xs text-gray-400 mt-1">
                        This person cannot log in to the ERP system.
                        <?php if (!hasPermission('users.create')): ?>
                        Granting access needs the <code>users.create</code> permission.
                        <?php endif; ?>
                    </p>
                </div>
            <?php endif; ?>
        </div>

        <!-- Quick Links -->
        <div class="bg-white rounded-lg shadow p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">Quick Actions</h3>
            <div class="space-y-2">
                <?php if (hasPermission('people_management.edit')): ?>
                <a href="edit.php?id=<?= $person['id'] ?>" class="block w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">
                    <i class="fas fa-edit text-yellow-500 mr-2"></i>Edit this person
                </a>
                <?php endif; ?>
                <?php if ($employee && hasPermission('employees.edit')): ?>
                <a href="<?= url('modules/employees/edit.php?id=' . $employee['id']) ?>" class="block w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">
                    <i class="fas fa-user-tie text-blue-500 mr-2"></i>Edit Employee Record
                </a>
                <?php endif; ?>
                <?php if (hasPermission('people_management.create')): ?>
                <a href="create.php" class="block w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded">
                    <i class="fas fa-plus text-green-500 mr-2"></i>Add another person
                </a>
                <?php endif; ?>
            </div>
        </div>
    </div>
</div>

<?php // Click-to-view modal for the profile photo, the same one HRMS and Contracts use.
if ($personPhoto && $personPhoto['exists']) {
    require __DIR__ . '/../../templates/document_viewer.php';
}
require_once '../../includes/footer.php'; ?>
