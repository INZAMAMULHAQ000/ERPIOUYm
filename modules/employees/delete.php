<?php
$pageTitle = 'Delete Employee';
require_once '../../includes/header.php';
require_once '../../helpers/redirect.php';
require_once '../../helpers/people_onboarding.php';

if (!hasPermission('employees.delete')) {
    die('Access Denied');
}

$db = getDB();
$id = (int) ($_POST['id'] ?? $_GET['id'] ?? 0);

$stmt = $db->prepare("SELECT id, employee_code, first_name, last_name, email
                      FROM employees WHERE id = ? LIMIT 1");
$stmt->execute([$id]);
$employee = $stmt->fetch();

if (!$employee) {
    flash('error', 'Employee not found.');
    to('modules/employees/index.php');
}

/*
 * This endpoint used to delete on GET, so a stray link or an embedded request
 * could remove a personnel record. The row now only goes on a POST carrying the
 * session CSRF token, and the directory is told about it either way.
 */
if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    if (!verifyCsrf($_POST['csrf_token'] ?? '')) {
        flash('error', 'Invalid security token. Please try again.');
        to('modules/employees/index.php');
    }

    try {
        $db->prepare("DELETE FROM employees WHERE id = ?")->execute([$id]);
    } catch (PDOException $e) {
        // Payroll, attendance and documents reference this employee with RESTRICT
        // foreign keys; the honest answer is to say so, not to cascade silently.
        flash('error', 'This employee cannot be deleted while related records exist '
            . '(attendance, payroll or documents). Terminate them instead to keep the history.');
        to('modules/employees/index.php');
    }

    $directory = peopleForfeitRecord($db, 'employee', $id);
    $note = $directory['removed'] ? ' Their directory entry was removed with it.'
        : ($directory['reopened'] ? ' Their directory entry stays, with the Employee step reopened.' : '');

    logAudit($_SESSION['user_id'], 'Deleted employee: ' . trim($employee['first_name'] . ' ' . (string) $employee['last_name'])
        . ' (' . $employee['employee_code'] . ')', 'employees');
    flash('success', 'Employee deleted.' . $note);
    to('modules/employees/index.php');
}

$name = trim($employee['first_name'] . ' ' . (string) $employee['last_name']);
?>
<div class="mb-6">
    <a href="view.php?id=<?= $id ?>" class="text-blue-600 hover:text-blue-900">
        <i class="fas fa-arrow-left mr-1"></i>Back to <?= sanitize($name) ?>
    </a>
</div>

<div class="bg-white rounded-lg shadow p-6 max-w-2xl">
    <h2 class="text-xl font-semibold text-red-700 mb-4">Delete <?= sanitize($name) ?>?</h2>
    <p class="text-sm text-gray-600 mb-4">
        <span class="font-mono"><?= sanitize($employee['employee_code']) ?></span>
        &middot; <?= sanitize($employee['email'] ?: 'no email') ?>
    </p>
    <ul class="text-sm text-gray-600 list-disc list-inside space-y-1 mb-6">
        <li>The employee record is removed permanently.</li>
        <li>Attendance, payroll and document history that points at them will block this until it is dealt with.</li>
        <li>If they are also a customer or contractor, the directory entry survives with only the Employee step reopened.</li>
    </ul>

    <form method="POST" class="flex items-center gap-4">
        <input type="hidden" name="csrf_token" value="<?= csrfToken() ?>">
        <input type="hidden" name="id" value="<?= $id ?>">
        <button type="submit" class="bg-red-600 text-white px-5 py-2 rounded hover:bg-red-700 transition">
            <i class="fas fa-trash mr-2"></i>Delete employee
        </button>
        <a href="view.php?id=<?= $id ?>" class="text-gray-600 px-5 py-2 border border-gray-200 rounded hover:text-gray-900">Cancel</a>
    </form>
</div>

<?php require_once '../../includes/footer.php'; ?>
