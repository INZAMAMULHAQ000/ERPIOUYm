<?php
require_once __DIR__ . '/../config/database.php';

function hasRole($role) {
    if (!isset($_SESSION['user_id'])) {
        return false;
    }
    
    $db = getDB();
    $stmt = $db->prepare("
        SELECT r.name FROM roles r
        JOIN user_roles ur ON r.id = ur.role_id
        WHERE ur.user_id = ? AND r.name = ?
    ");
    $stmt->execute([$_SESSION['user_id'], $role]);
    return $stmt->fetch() !== false;
}

function hasPermission($permission) {
    if (!isset($_SESSION['user_id'])) {
        return false;
    }
    
    $originalPermission = $permission;
    
    // Handle fixed_assets module permissions (fixedasset.* -> fixed_assets.fixedasset.*)
    // This must be checked first, before the dot check, because fixedasset.* permissions contain dots
    if (str_starts_with($permission, 'fixedasset')) {
        $permission = 'fixed_assets.' . $permission;
    }
    // If no dot and no module prefix, try to infer from known modules
    elseif (!str_contains($permission, '.')) {
        $moduleMap = [
            'dashboard' => 'dashboard',
            'users' => 'users',
            'roles' => 'roles',
            'permissions' => 'permissions',
            'departments' => 'departments',
            'designations' => 'designations',
            'employees' => 'employees',
            'attendance' => 'attendance',
            'leaves' => 'leaves',
            'holidays' => 'holidays',
            'projects' => 'projects',
            'tasks' => 'tasks',
            'timesheets' => 'timesheets',
            'milestones' => 'milestones',
            'leads' => 'leads',
            'clients' => 'clients',
            'deals' => 'deals',
            'invoices' => 'invoices',
            'payments' => 'payments',
            'expenses' => 'expenses',
            'vendors' => 'vendors',
            'inventory' => 'inventory',
            'helpdesk' => 'helpdesk',
            'tickets' => 'tickets',
            'ticket_categories' => 'ticket_categories',
            'slas' => 'slas',
            'knowledgebase' => 'knowledgebase',
            'reports' => 'reports',
            'analytics' => 'analytics',
            'auditlogs' => 'auditlogs',
            'scheduled_reports' => 'scheduled_reports',
            'settings' => 'settings',
            'people_management' => 'people_management',
            'leave_management' => 'leave_management',
            'widgets' => 'widgets',
            'template_designer' => 'template_designer',
            'finance' => 'finance',
            'assets' => 'assets',
            'asset_assignments' => 'asset_assignments',
            'asset_returns' => 'asset_returns',
            'maintenance' => 'maintenance',
            'licenses' => 'licenses',
        ];
        
        foreach ($moduleMap as $key => $module) {
            if (str_starts_with($permission, $key . '.')) {
                $permission = $module . '.' . $permission;
                break;
            }
        }
    }
    
    $db = getDB();
    $stmt = $db->prepare("
        SELECT CONCAT(p.module, '.', p.name) as perm FROM permissions p
        JOIN role_permissions rp ON p.id = rp.permission_id
        JOIN user_roles ur ON rp.role_id = ur.role_id
        WHERE ur.user_id = ?
    ");
    $stmt->execute([$_SESSION['user_id']]);
    $perms = array_column($stmt->fetchAll(), 'perm');
    
    return in_array($permission, $perms);
}

function getUserRoles($userId = null) {
    $userId = $userId ?? $_SESSION['user_id'] ?? null;
    if (!$userId) {
        return [];
    }
    
    $db = getDB();
    $stmt = $db->prepare("
        SELECT r.id, r.name FROM roles r
        JOIN user_roles ur ON r.id = ur.role_id
        WHERE ur.user_id = ?
    ");
    $stmt->execute([$userId]);
    return $stmt->fetchAll();
}

function getUserPermissions($userId = null) {
    $userId = $userId ?? $_SESSION['user_id'] ?? null;
    if (!$userId) {
        return [];
    }
    
    $db = getDB();
    $stmt = $db->prepare("
        SELECT DISTINCT CONCAT(p.module, '.', p.name) as perm FROM permissions p
        JOIN role_permissions rp ON p.id = rp.permission_id
        JOIN user_roles ur ON rp.role_id = ur.role_id
        WHERE ur.user_id = ?
    ");
    $stmt->execute([$userId]);
    return array_column($stmt->fetchAll(), 'perm');
}

function requireRole($role) {
    if (!hasRole($role)) {
        die('Access Denied: Role required');
    }
}

function requirePermission($permission) {
    if (!hasPermission($permission)) {
        die('Access Denied: Permission required');
    }
}

/**
 * The role id the rest of the application treats as untouchable.
 *
 * helpers/company.php hardcodes role id 1 as the "sees every company" bypass,
 * and users.delete / people_management.delete are granted to nothing else, so
 * losing the last holder of it is not an inconvenience — it is an organisation
 * that can no longer administer itself.
 */
function superAdminRoleId()
{
    return 1;
}

/**
 * Filter requested role ids down to the ones that exist.
 *
 * The forms post `roles[]` straight into user_roles, which has a foreign key to
 * roles — so a hand-crafted or stale submission used to surface as an uncaught
 * PDO error after the user row had already been written.
 */
function assignableRoleIds($db, $requested)
{
    $requested = is_array($requested) ? $requested : [];
    $ids = [];
    foreach ($requested as $roleId) {
        $roleId = (int) $roleId;
        if ($roleId > 0) {
            $ids[$roleId] = $roleId;
        }
    }
    if (!$ids) {
        return [];
    }
    $in = implode(',', array_fill(0, count($ids), '?'));
    $stmt = $db->prepare("SELECT id FROM roles WHERE id IN ($in) AND deleted_at IS NULL");
    $stmt->execute(array_values($ids));
    return array_map('intval', $stmt->fetchAll(PDO::FETCH_COLUMN));
}

/** Human-readable role names, for the audit trail. */
function roleNamesFor($db, array $roleIds)
{
    if (!$roleIds) {
        return [];
    }
    $in = implode(',', array_fill(0, count($roleIds), '?'));
    $stmt = $db->prepare("SELECT name FROM roles WHERE id IN ($in) ORDER BY name");
    $stmt->execute(array_values(array_map('intval', $roleIds)));
    return $stmt->fetchAll(PDO::FETCH_COLUMN);
}

/** Roles currently held by a user. */
function assignedRoleIds($db, $userId)
{
    $stmt = $db->prepare("SELECT role_id FROM user_roles WHERE user_id = ?");
    $stmt->execute([(int) $userId]);
    return array_map('intval', $stmt->fetchAll(PDO::FETCH_COLUMN));
}

/**
 * Would saving this change lock the organisation out of its administration?
 *
 * Two cases are refused: an administrator removing their own Super Admin role or
 * deactivating their own account, and emptying the last active Super Admin
 * account. Anything else is a legitimate change of mind.
 */
function roleChangeBlocked($db, $userId, array $newRoleIds, $newStatus, $actorId)
{
    $super = superAdminRoleId();
    $userId = (int) $userId;
    $current = assignedRoleIds($db, $userId);

    if (!in_array($super, $current, true)) {
        return null;
    }
    $keeps = in_array($super, $newRoleIds, true) && $newStatus === 'active';
    if ($keeps) {
        return null;
    }

    if ((int) $actorId === $userId) {
        return 'You cannot remove your own Super Admin role or deactivate your own account — '
             . 'you would lose the ability to change it back.';
    }

    // Only an account that can actually sign in counts as a fallback: a leftover
    // with a non-crypt password (test data, an imported row) holds the role in the
    // database but can never be used to put it back.
    $stmt = $db->prepare("SELECT COUNT(DISTINCT u.id) FROM users u
                          JOIN user_roles ur ON ur.user_id = u.id
                          WHERE ur.role_id = ? AND u.id <> ? AND u.status = 'active'
                            AND u.deleted_at IS NULL AND LEFT(u.password, 1) = '\$'");
    $stmt->execute([$super, $userId]);
    if ((int) $stmt->fetchColumn() === 0) {
        return 'This is the last active Super Admin. Promote another account first — without one, '
             . 'no user can manage roles, permissions, deletions or the people directory.';
    }
    return null;
}
