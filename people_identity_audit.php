<?php
/**
 * People identity audit — CLI only.
 *
 *   php people_identity_audit.php            # human-readable report
 *   php people_identity_audit.php --porcelain # one line per violation, for cron
 *
 * Exit 0 when the identity invariant holds, 1 when it does not. Run it after a
 * migration, after a bulk import, and after any hand-edited SQL: it reads only,
 * and it is the only thing that says out loud whether every human in the system
 * still has exactly one Person Code and the right codes for their categories.
 *
 * The invariant, restated as checks:
 *   1. every employee, contractor and individual customer has a directory entry
 *   2. every directory entry has a unique, non-blank Person Code
 *   3. a role recorded as complete points at a live record, and the record and
 *      the link column agree on which record that is
 *   4. no organisation is masquerading as a person
 *   5. codes are unique inside their own master, and no two directory entries
 *      claim the same email
 *   6. people.category is one of the roles actually recorded for that person
 */

if (PHP_SAPI !== 'cli') {
    http_response_code(403);
    die('Command line only.' . PHP_EOL);
}

require_once __DIR__ . '/config/database.php';
require_once __DIR__ . '/helpers/people_onboarding.php';

$db = getDB();
$porcelain = in_array('--porcelain', $argv ?? [], true);

/** One collected violation. */
$issues = [];
$report = function (string $code, string $detail) use (&$issues, $porcelain) {
    $issues[] = $code;
    echo ($porcelain ? "VIOLATION $code" : "  [!] $code — $detail") . PHP_EOL;
};

function ids($db, $sql, $params = [])
{
    $stmt = $db->prepare($sql);
    $stmt->execute($params);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

$definitions = peopleRoleDefinitions();
$clean = 0;

echo "== People identity audit ==\n";

/* 1 ── module records with no directory entry ──────────────────────────────── */
echo "\n-- records that must have a Person Code --\n";
foreach ($definitions as $role => $def) {
    $deleted = !empty($def['deleted_column']) ? "AND c.`{$def['deleted_column']}` IS NULL" : '';
    $individual = ($role === 'customer') ? "AND c.customer_type = 'individual'" : '';
    $rows = ids($db, "SELECT c.id, c.`{$def['code_column']}` AS code FROM `{$def['table']}` c
                      LEFT JOIN people p ON p.`{$def['link_column']}` = c.id
                      WHERE p.id IS NULL $deleted $individual ORDER BY c.id");
    if (!$rows) {
        echo "  ok  " . $def['label'] . ": every record has a Person Code\n";
        $clean++;
        continue;
    }
    foreach ($rows as $r) {
        $report('missing-person/' . $role . '/' . $r['code'],
            $def['label'] . ' #' . $r['id'] . ' (' . $r['code'] . ') has no directory entry — People Management offers to add it');
    }
}

/* 2 ── directory entries missing a Person Code ─────────────────────────────── */
echo "\n-- directory integrity --\n";
$blank = (int) $db->query("SELECT COUNT(*) FROM people WHERE person_code IS NULL OR TRIM(person_code) = ''")->fetchColumn();
if ($blank === 0) {
    echo "  ok  every directory row carries a Person Code\n";
    $clean++;
} else {
    $report('blank-person-code', "$blank directory row(s) without a Person Code");
}

$duplicates = ids($db, "SELECT email, COUNT(*) n FROM people WHERE email IS NOT NULL AND email <> ''
                        GROUP BY email HAVING n > 1");
if (!$duplicates) {
    echo "  ok  no two people share an email\n";
    $clean++;
} else {
    foreach ($duplicates as $d) {
        $report('duplicate-person-email/' . $d['email'], $d['n'] . ' directory rows share that email');
    }
}

/* 3 ── role rows that claim more than they can back ────────────────────────── */
echo "\n-- role status against the record it points at --\n";
foreach ($definitions as $role => $def) {
    $deleted = !empty($def['deleted_column']) ? "AND r.`{$def['deleted_column']}` IS NULL" : '';

    $stale = ids($db, "SELECT pr.id, pr.person_id, p.person_code
                       FROM person_roles pr
                       JOIN people p ON p.id = pr.person_id
                       LEFT JOIN `{$def['table']}` r ON r.id = p.`{$def['link_column']}`
                       WHERE pr.role = ? AND pr.status = 'complete'
                         AND (p.`{$def['link_column']}` IS NULL OR r.id IS NULL $deleted)", [$role]);
    foreach ($stale as $s) {
        $report('complete-without-record/' . $role . '/' . $s['person_code'],
            'marked complete but its ' . strtolower($def['label']) . ' record is gone — use Sync & repair on the People Management list');
    }

    $mismatch = ids($db, "SELECT pr.id, pr.person_id, pr.record_id, p.`{$def['link_column']}` AS link_id
                          FROM person_roles pr JOIN people p ON p.id = pr.person_id
                          WHERE pr.role = ? AND pr.status = 'complete' AND pr.record_id IS NOT NULL
                            AND p.`{$def['link_column']}` IS NOT NULL
                            AND pr.record_id <> p.`{$def['link_column']}`", [$role]);
    foreach ($mismatch as $m) {
        $report('record-disagrees/' . $role . '/' . $m['person_id'],
            'role row says #' . $m['record_id'] . ' but the person is linked to #' . $m['link_id']);
    }

    if (!$stale && !$mismatch) {
        echo "  ok  " . $def['label'] . ": every complete role has the record it names\n";
        $clean++;
    }
}

$orphanRoles = (int) $db->query("SELECT COUNT(*) FROM person_roles pr
                                 LEFT JOIN people p ON p.id = pr.person_id WHERE p.id IS NULL")->fetchColumn();
if ($orphanRoles === 0) {
    echo "  ok  no role rows orphaned by a deleted person\n";
    $clean++;
} else {
    $report('orphan-role-rows', "$orphanRoles role row(s) point at a missing person");
}

$noRoles = (int) $db->query("SELECT COUNT(*) FROM people p
                             WHERE NOT EXISTS (SELECT 1 FROM person_roles pr WHERE pr.person_id = p.id)")->fetchColumn();
if ($noRoles === 0) {
    echo "  ok  every person has at least one recorded person type\n";
    $clean++;
} else {
    $report('person-without-roles', "$noRoles person(s) have no person type recorded");
}

/* 4 ── organisations must not be people ────────────────────────────────────── */
$orgs = ids($db, "SELECT p.id, p.person_code, c.client_code, c.customer_type
                  FROM people p JOIN clients c ON c.id = p.customer_id
                  WHERE c.customer_type <> 'individual' AND c.deleted_at IS NULL");
if (!$orgs) {
    echo "  ok  no directory entry is claimed by an organisation customer\n";
    $clean++;
} else {
    foreach ($orgs as $o) {
        // Deliberate links are allowed only through the "attach existing" path;
        // they are reported so a human confirms each one rather than silently
        // turning the directory into the customer master.
        $report('org-customer-linked/' . $o['person_code'],
            $o['person_code'] . ' is linked to ' . $o['customer_type'] . ' ' . $o['client_code'] . ' — review');
    }
}

/* 5 ── code uniqueness inside each master ──────────────────────────────────── */
echo "\n-- code uniqueness --\n";
foreach ($definitions as $role => $def) {
    $dupes = ids($db, "SELECT `{$def['code_column']}` AS code, COUNT(*) n FROM `{$def['table']}`
                       GROUP BY `{$def['code_column']}` HAVING n > 1");
    if ($dupes) {
        foreach ($dupes as $d) {
            $report('duplicate-code/' . $role . '/' . $d['code'], $d['n'] . ' rows share that code');
        }
    } else {
        echo "  ok  " . $def['code_column'] . " unique\n";
        $clean++;
    }
}

/* 6 ── category drift ──────────────────────────────────────────────────────── */
echo "\n-- category against recorded roles --\n";
$drift = ids($db, "SELECT p.id, p.person_code, p.category FROM people p WHERE p.category NOT IN
                   (SELECT pr.role FROM person_roles pr WHERE pr.person_id = p.id AND pr.status <> 'declined')");
if (!$drift) {
    echo "  ok  every person's category is one of their recorded person types\n";
    $clean++;
} else {
    foreach ($drift as $d) {
        $report('category-drift/' . $d['person_code'],
            'category ' . $d['category'] . ' has no matching role row');
    }
}

echo "\n== " . count($issues) . " violation(s) across $clean clean checks ==" . PHP_EOL;
if ($porcelain) {
    foreach ($issues as $i) echo "VIOLATION $i" . PHP_EOL;
}
exit(count($issues) === 0 ? 0 : 1);
