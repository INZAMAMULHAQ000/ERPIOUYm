<?php
/**
 * Company-scoped option lists for the contractor engagement form.
 *
 * Reporting Manager and Project are chosen after Company, so their contents
 * have to be re-fetched per company rather than shipped as one long list.
 *
 * This deliberately does NOT include includes/header.php. That file renders the
 * navbar and sidebar, so any page built on it emits HTML around the JSON body —
 * which is why the older inventory endpoints answer a fetch() with a document.
 * Only the session, the guards and the helpers used below are loaded.
 */

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

require_once dirname(__DIR__, 2) . '/config/database.php';
require_once dirname(__DIR__, 2) . '/helpers/security.php';
require_once dirname(__DIR__, 2) . '/helpers/url.php';
require_once dirname(__DIR__, 2) . '/helpers/rbac.php';
require_once dirname(__DIR__, 2) . '/helpers/company.php';
require_once dirname(__DIR__, 2) . '/middleware/auth.php';

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

function engagementJson($payload, $status = 200)
{
    http_response_code($status);
    echo json_encode($payload);
    exit;
}

// Answer 401 as JSON rather than letting requireAuth() redirect an XHR to the
// login page, which the browser would happily follow and hand back as HTML.
if (empty($_SESSION['user_id'])) {
    engagementJson(['success' => false, 'error' => 'Not authenticated.'], 401);
}

requireAuth();

if (!hasPermission('contractors.view') && !hasPermission('contractors.create') && !hasPermission('contractors.edit')) {
    engagementJson(['success' => false, 'error' => 'Permission denied.'], 403);
}

$action = $_GET['action'] ?? '';
$companyId = (int) ($_GET['company_id'] ?? 0);

if ($companyId <= 0) {
    engagementJson(['success' => true, 'data' => []]);
}

// The company comes from the request, so it is checked against the user's own
// grants — otherwise this endpoint would be a way to read another company's
// staff and project names.
if (!array_key_exists($companyId, companyOptions())) {
    engagementJson(['success' => false, 'error' => 'You are not permitted to list that company.'], 403);
}

$db = getDB();

if ($action === 'employees') {
    $stmt = $db->prepare("
        SELECT id, TRIM(CONCAT(first_name, ' ', COALESCE(last_name, ''))) AS label
        FROM employees
        WHERE status = 'active' AND company_id = ?
        ORDER BY first_name, last_name
    ");
    $stmt->execute([$companyId]);
    engagementJson(['success' => true, 'data' => $stmt->fetchAll(PDO::FETCH_ASSOC)]);
}

if ($action === 'projects') {
    $stmt = $db->prepare("
        SELECT id, project_name AS label
        FROM projects
        WHERE company_id = ?
        ORDER BY project_name
        LIMIT 400
    ");
    $stmt->execute([$companyId]);
    engagementJson(['success' => true, 'data' => $stmt->fetchAll(PDO::FETCH_ASSOC)]);
}

engagementJson(['success' => false, 'error' => 'Unknown action.'], 400);
