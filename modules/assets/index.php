<?php
$pageTitle = 'Assets';
require_once '../../includes/header.php';
require_once '../../helpers/redirect.php';
require_once '../../helpers/pagination.php';

if (!hasPermission('assets.view')) { die('Access Denied'); }

$db = getDB();
$search = trim($_GET['search'] ?? '');
$category_id = $_GET['category_id'] ?? '';
$status = $_GET['status'] ?? '';
$condition = $_GET['condition'] ?? '';
$page = getPageNumber();
$perPage = 15;

$where = "WHERE 1=1";
$params = [];

// The KPI cards, the list and the search all read this one fragment, so they
// cannot disagree about which rows are in scope.
$companyFilter = applyCompanyScope('a.company_id', $where, $params);

if ($search) { $where .= " AND (a.asset_code LIKE ? OR a.asset_name LIKE ? OR a.serial_number LIKE ?)"; $params[] = "%$search%"; $params[] = "%$search%"; $params[] = "%$search%"; }
if ($category_id) { $where .= " AND a.category_id = ?"; $params[] = $category_id; }
if ($status) { $where .= " AND a.status = ?"; $params[] = $status; }
if ($condition) { $where .= " AND a.asset_condition = ?"; $params[] = $condition; }

$hasFilters = ($search !== '' || $category_id !== '' || $status !== '' || $condition !== '' || array_key_exists('company_id', $_GET));

$countStmt = $db->prepare("SELECT COUNT(*) as cnt FROM assets a $where");
$countStmt->execute($params);
$total = (int) $countStmt->fetch()['cnt'];
$pagination = paginate($total, $perPage, $page);

$queryParams = array_merge($params, [$perPage, $pagination['offset']]);
$stmt = $db->prepare("SELECT a.*, c.category_name, v.vendor_name 
    FROM assets a 
    LEFT JOIN asset_categories c ON a.category_id = c.id 
    LEFT JOIN vendors v ON a.vendor_id = v.id 
    $where 
    ORDER BY a.id DESC 
    LIMIT ? OFFSET ?");
$stmt->execute($queryParams);
$assets = $stmt->fetchAll();

$categories = $db->query("SELECT id, category_name FROM asset_categories WHERE status = 'active' ORDER BY category_name")->fetchAll();

// Counters are derived from the filtered set so the cards never contradict the list below.
$statusCounts = array_fill_keys(['available', 'assigned', 'maintenance', 'damaged', 'lost', 'retired'], 0);
$statusStmt = $db->prepare("SELECT a.status, COUNT(*) as c FROM assets a $where GROUP BY a.status");
$statusStmt->execute($params);
foreach ($statusStmt->fetchAll() as $row) {
    if (isset($statusCounts[$row['status']])) $statusCounts[$row['status']] = (int) $row['c'];
}
$expiringStmt = $db->prepare("SELECT COUNT(*) as c FROM assets a $where AND a.warranty_expiry BETWEEN CURRENT_DATE AND DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY)");
$expiringStmt->execute($params);
$expiring = (int) $expiringStmt->fetch()['c'];

$statusColors = ['available' => 'bg-green-100 text-green-800', 'assigned' => 'bg-blue-100 text-blue-800', 'maintenance' => 'bg-yellow-100 text-yellow-800', 'damaged' => 'bg-red-100 text-red-800', 'lost' => 'bg-gray-100 text-gray-800', 'retired' => 'bg-red-200 text-red-800'];
$conditionColors = ['new' => 'bg-blue-100 text-blue-800', 'good' => 'bg-green-100 text-green-800', 'fair' => 'bg-yellow-100 text-yellow-800', 'damaged' => 'bg-red-100 text-red-800'];
?>

<div class="mb-6 flex justify-between items-center">
    <div>
        <h1 class="text-2xl font-bold text-gray-800">Assets</h1>
        <p class="text-gray-600">Manage IT assets and equipment</p>
    </div>
    <?php if (hasPermission('assets.create')): ?>
    <a href="<?= url('modules/assets/create.php') ?>" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"><i class="fas fa-plus mr-2"></i>Add Asset</a>
    <?php endif; ?>
</div>

<div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500">Total Assets</div>
        <div class="text-2xl font-bold text-gray-800"><?= $total ?></div>
    </div>
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500">Available</div>
        <div class="text-2xl font-bold text-green-600"><?= $statusCounts['available'] ?></div>
    </div>
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500">Assigned</div>
        <div class="text-2xl font-bold text-blue-600"><?= $statusCounts['assigned'] ?></div>
    </div>
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500">Maintenance</div>
        <div class="text-2xl font-bold text-yellow-600"><?= $statusCounts['maintenance'] ?></div>
    </div>
    <div class="bg-white rounded-lg shadow p-4">
        <div class="text-sm text-gray-500">Warranty Expiring</div>
        <div class="text-2xl font-bold text-orange-600"><?= $expiring ?></div>
    </div>
</div>

<div class="bg-white rounded-lg shadow mb-6">
    <form method="GET" class="p-4 flex flex-wrap gap-4 items-end">
        <div class="flex-1 min-w-[200px]">
            <label class="block text-sm font-medium text-gray-700 mb-1">Search</label>
            <input type="text" name="search" value="<?= sanitize($search) ?>" placeholder="Asset code, name, serial..." class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500">
        </div>
        <div class="w-40">
            <label class="block text-sm font-medium text-gray-700 mb-1">Organisation</label>
            <?php
            $companySel = $companyFilter === null ? activeCompanyId() : (int) $companyFilter;
            $allCompanies = count(companyOptions()) > 1;
            ?>
            <select name="company_id" onchange="this.form.submit()" class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500">
                <?php if ($allCompanies): ?>
                <option value="" <?= $companySel === 0 ? 'selected' : '' ?>>All companies</option>
                <?php endif; ?>
                <?php foreach (companyOptions() as $cid => $label): ?>
                <option value="<?= (int) $cid ?>" <?= $companySel === (int) $cid ? 'selected' : '' ?>><?= sanitize($label) ?></option>
                <?php endforeach; ?>
            </select>
        </div>
        <div class="w-40">
            <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select name="category_id" onchange="this.form.submit()" class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500">
                <option value="">All</option>
                <?php foreach ($categories as $cat): ?><option value="<?= $cat['id'] ?>" <?= $category_id == $cat['id'] ? 'selected' : '' ?>><?= sanitize($cat['category_name']) ?></option><?php endforeach; ?>
            </select>
        </div>
        <div class="w-32">
            <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select name="status" onchange="this.form.submit()" class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500">
                <option value="">All</option>
                <option value="available" <?= $status === 'available' ? 'selected' : '' ?>>Available</option>
                <option value="assigned" <?= $status === 'assigned' ? 'selected' : '' ?>>Assigned</option>
                <option value="maintenance" <?= $status === 'maintenance' ? 'selected' : '' ?>>Maintenance</option>
                <option value="damaged" <?= $status === 'damaged' ? 'selected' : '' ?>>Damaged</option>
                <option value="lost" <?= $status === 'lost' ? 'selected' : '' ?>>Lost</option>
                <option value="retired" <?= $status === 'retired' ? 'selected' : '' ?>>Retired</option>
            </select>
        </div>
        <div class="w-32">
            <label class="block text-sm font-medium text-gray-700 mb-1">Condition</label>
            <select name="condition" onchange="this.form.submit()" class="w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500">
                <option value="">All</option>
                <option value="new" <?= $condition === 'new' ? 'selected' : '' ?>>New</option>
                <option value="good" <?= $condition === 'good' ? 'selected' : '' ?>>Good</option>
                <option value="fair" <?= $condition === 'fair' ? 'selected' : '' ?>>Fair</option>
                <option value="damaged" <?= $condition === 'damaged' ? 'selected' : '' ?>>Damaged</option>
            </select>
        </div>
        <button type="submit" class="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"><i class="fas fa-search mr-1"></i>Search</button>
        <?php if ($hasFilters): ?>
        <a href="<?= url('modules/assets/index.php') ?>" class="px-4 py-2 rounded border border-gray-300 text-gray-600 hover:bg-gray-50">Clear</a>
        <?php endif; ?>
    </form>
</div>

<div class="bg-white rounded-lg shadow overflow-hidden">
    <table class="w-full">
        <thead class="bg-gray-50">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Asset Code</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Serial #</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Condition</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Organisation</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Warranty</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
            <?php foreach ($assets as $asset): ?>
            <tr class="hover:bg-gray-50">
                <td class="px-6 py-4 font-medium text-gray-900"><?= sanitize($asset['asset_code']) ?></td>
                <td class="px-6 py-4 text-gray-600"><?= sanitize($asset['asset_name']) ?></td>
                <td class="px-6 py-4 text-gray-600"><?= sanitize($asset['category_name']) ?></td>
                <td class="px-6 py-4 text-gray-600"><?= sanitize($asset['serial_number'] ?? '-') ?></td>
                <td class="px-6 py-4">
                    <span class="px-2 py-1 text-xs rounded <?= $statusColors[$asset['status']] ?? 'bg-gray-100' ?>"><?= ucfirst($asset['status']) ?></span>
                </td>
                <td class="px-6 py-4">
                    <span class="px-2 py-1 text-xs rounded <?= $conditionColors[$asset['asset_condition']] ?? 'bg-gray-100' ?>"><?= ucfirst($asset['asset_condition']) ?></span>
                </td>
                <td class="px-6 py-4 text-gray-600"><?= sanitize($asset['location'] ?? '') ?: '-' ?></td>
                <td class="px-6 py-4 text-gray-600"><?= sanitize(companyLabel($asset['company_id']) ?? '-') ?></td>
                <td class="px-6 py-4 text-gray-600">
                    <?php if ($asset['warranty_expiry']): ?>
                        <?php if (strtotime($asset['warranty_expiry']) < time()): ?>
                            <span class="text-red-600">Expired</span>
                        <?php elseif (strtotime($asset['warranty_expiry']) < strtotime('+30 days')): ?>
                            <span class="text-orange-600"><?= date('M d, Y', strtotime($asset['warranty_expiry'])) ?></span>
                        <?php else: ?>
                            <?= date('M d, Y', strtotime($asset['warranty_expiry'])) ?>
                        <?php endif; ?>
                    <?php else: ?>
                        -
                    <?php endif; ?>
                </td>
                <td class="px-6 py-4 text-right">
                    <a href="<?= url('modules/assets/view.php?id=' . $asset['id'] . '') ?>" class="text-blue-600 hover:text-blue-900 mr-2"><i class="fas fa-eye"></i></a>
                    <?php if (hasPermission('assets.edit')): ?>
                    <a href="<?= url('modules/assets/edit.php?id=' . $asset['id'] . '') ?>" class="text-yellow-600 hover:text-yellow-900 mr-2"><i class="fas fa-edit"></i></a>
                    <?php endif; ?>
                    <?php if (hasPermission('assets.assign') && $asset['status'] == 'available'): ?>
                    <a href="<?= url('modules/asset_assignments/create.php?asset_id=' . $asset['id'] . '') ?>" class="text-green-600 hover:text-green-900 mr-2" title="Assign"><i class="fas fa-user-plus"></i></a>
                    <?php endif; ?>
                </td>
            </tr>
            <?php endforeach; ?>
            <?php if (empty($assets)): ?>
            <tr><td colspan="10" class="px-6 py-8 text-center text-gray-500">No assets found</td></tr>
            <?php endif; ?>
        </tbody>
    </table>
</div>

<?= paginationLinks($pagination, '?') ?>
<?php require_once '../../includes/footer.php'; ?>

