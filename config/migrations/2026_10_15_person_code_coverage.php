<?php
/**
 * Person Code coverage backfill.
 *
 * The rule this enforces: every human in the system has exactly one directory
 * entry — one Person Code — and one code per category they belong to (Employee,
 * Contractor, Customer), all linked to that same entry. Employee, contractor and
 * customer records created directly in their own modules never minted a person,
 * so the directory was only ever as complete as the wizard that fills it.
 *
 * What it does per candidate record, through peoplePersonDecision() — the same
 * function the live save path uses, so a preview cannot promise something the
 * real run would do differently:
 *   - the record already has a person   -> left alone
 *   - a person with that email exists   -> the record is attached to that person
 *   - nobody matches                    -> a new Person Code is minted and linked
 * Organisations are not people: `clients` rows whose customer_type is anything
 * other than 'individual' are skipped, so the directory does not become a mirror
 * of the customer master. One human with an employee row and a contractor row
 * sharing an email becomes ONE person holding two roles.
 *
 * Nothing is deleted, no existing code is reissued, and people.category is set
 * only on rows this migration creates.
 *
 * Usage:
 *   php config/migrations/2026_10_15_person_code_coverage.php            # dry run
 *   php config/migrations/2026_10_15_person_code_coverage.php --apply    # write
 *
 * Applying is idempotent — re-running finds every record already linked and
 * writes nothing.
 */

require_once __DIR__ . '/../database.php';
require_once __DIR__ . '/../../helpers/security.php';
require_once __DIR__ . '/../../helpers/people_onboarding.php';

$db = getDB();
$apply = in_array('--apply', $argv ?? [], true);

echo "== Person Code coverage backfill == " . ($apply ? "APPLYING" : "DRY RUN (nothing will be written)") . "\n";

$candidates = [];
foreach (['employee', 'contractor', 'customer'] as $role) {
    $def = peopleRoleDefinition($role);
    $where = $def['deleted_column'] ? "`{$def['deleted_column']}` IS NULL" : "1=1";
    $extra = ($role === 'customer') ? " AND customer_type = 'individual'" : '';
    $rows = $db->query("SELECT id, `{$def['code_column']}` AS code FROM `{$def['table']}`
                        WHERE $where$extra ORDER BY id")->fetchAll();
    foreach ($rows as $r) {
        $candidates[] = ['role' => $role, 'id' => (int) $r['id'], 'code' => $r['code']];
    }
}

$tallies = ['already' => 0, 'attached' => 0, 'created' => 0, 'skipped' => 0, 'conflict' => 0, 'failed' => 0];

foreach ($candidates as $candidate) {
    $def = peopleRoleDefinition($candidate['role']);
    $decision = peoplePersonDecision($db, $candidate['role'], $candidate['id']);
    $action = $decision['action'];
    $tallies[$action] = ($tallies[$action] ?? 0) + 1;

    if ($action === 'already') {
        continue;   // the invariant already holds for this record
    }

    $name = isset($decision['identity'])
        ? trim($decision['identity']['first_name'] . ' ' . $decision['identity']['last_name'])
        : '-';
    $email = $decision['identity']['email'] ?? '-';

    printf("  %-11s %-12s %-24s %-34s %-9s %s\n",
        $def['label'],
        $candidate['code'],
        mb_substr($name, 0, 24),
        mb_substr($email, 0, 34),
        $action,
        $action === 'created' ? 'new Person Code' : ($decision['person_code'] ?? '')
    );
    if (!$apply) {
        continue;
    }

    $result = peopleEnsurePersonForRecord($db, $candidate['role'], $candidate['id']);
    if ($result['action'] === 'failed' || $result['action'] === 'conflict') {
        $tallies[$result['action']]++;
        $tallies[$action]--;
        echo "    ! " . $candidate['code'] . ': ' . $result['message'] . "\n";
    }
}

echo "\nCandidates: " . count($candidates) . "  |  already covered: " . $tallies['already'] . "\n";
echo "To write: " . ($tallies['created'] + $tallies['attached']) . "  (create " . $tallies['created']
    . ", attach " . $tallies['attached'] . ")\n";
if ($tallies['conflict']) echo "Conflicts needing a human decision: " . $tallies['conflict'] . "\n";
if ($tallies['failed']) echo "FAILED: " . $tallies['failed'] . "\n";

if (!$apply) {
    echo "\nDry run only. Re-run with --apply to write.\n";
    exit(0);
}

echo "\n-- verification --\n";
$orphans = [];
foreach (['employee', 'contractor', 'customer'] as $role) {
    $def = peopleRoleDefinition($role);
    $where = $def['deleted_column'] ? "AND c.`{$def['deleted_column']}` IS NULL" : '';
    $extra = ($role === 'customer') ? "AND c.customer_type = 'individual'" : '';
    $n = (int) $db->query("SELECT COUNT(*) FROM `{$def['table']}` c
                           LEFT JOIN people p ON p.{$def['link_column']} = c.id
                           WHERE p.id IS NULL $where $extra")->fetchColumn();
    $orphans[$def['label']] = $n;
    echo "  " . $def['label'] . " without a Person Code: $n\n";
}
$missingCodes = (int) $db->query("SELECT COUNT(*) FROM people WHERE person_code IS NULL OR person_code = ''")->fetchColumn();
echo "  Directory rows missing a Person Code: $missingCodes\n";
echo "  Directory total: " . (int) $db->query("SELECT COUNT(*) FROM people")->fetchColumn() . "\n";

exit(array_sum($orphans) === 0 && $missingCodes === 0 ? 0 : 1);
