<?php
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/rbac.php';
require_once __DIR__ . '/security.php';

/**
 * Login accounts: one implementation, so the Users module and a person's profile
 * cannot drift apart. Creating an account is the privilege-escalation path in this
 * application (Admin holds users.create), so the rules that matter live here
 * rather than in whichever form happens to be on screen.
 */

/**
 * Which of the requested roles may this actor hand out?
 *
 * A Super Admin may grant anything. Anyone else may only grant roles they already
 * hold, so an Admin cannot mint themselves a Super Admin account or promote a
 * colleague past their own reach.
 *
 * @return array ids=>allowed role ids, refused=>role names that were dropped
 */
function accountGrantableRoleIds($db, $requested, $actorId)
{
    $ids = assignableRoleIds($db, $requested);
    if (!$ids) {
        return ['ids' => [], 'refused' => []];
    }

    if (in_array(superAdminRoleId(), assignedRoleIds($db, (int) $actorId), true)) {
        return ['ids' => $ids, 'refused' => []];
    }

    $held = assignedRoleIds($db, (int) $actorId);
    $allowed = array_values(array_intersect($ids, $held));
    $refused = roleNamesFor($db, array_diff($ids, $allowed));

    return ['ids' => $allowed, 'refused' => $refused];
}

/**
 * Validate and create a `users` row, optionally linking it to a directory entry.
 *
 * Never call this outside a transaction when a person link is involved: the account
 * and the link must land together or not at all.
 *
 * @param array $data name, email, password, status, roles (raw post array), person_id?
 * @return array user_id (0 when refused) and errors keyed by field
 */
function accountCreate($db, array $data, $actorId)
{
    $actorId = (int) $actorId;
    $name = trim((string) ($data['name'] ?? ''));
    $email = strtolower(trim((string) ($data['email'] ?? '')));
    $password = (string) ($data['password'] ?? '');
    $status = (string) ($data['status'] ?? 'active');
    $personId = isset($data['person_id']) ? (int) $data['person_id'] : 0;

    $errors = [];

    if (mb_strlen($name) < 2) {
        $errors['name'] = 'Name must be at least 2 characters';
    }
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors['email'] = 'Enter a valid email address';
    }
    if (strlen($password) < 6) {
        $errors['password'] = 'Password must be at least 6 characters';
    }
    if (!in_array($status, ['active', 'inactive', 'suspended'], true)) {
        $errors['status'] = 'Choose a valid status';
    }

    // users.email is UNIQUE across every row, including soft-deleted ones, so a
    // lookup that filters on deleted_at would let the insert die on a raw
    // duplicate-key error in front of the user.
    if (empty($errors['email'])) {
        $stmt = $db->prepare("SELECT id, name, deleted_at FROM users WHERE email = ? LIMIT 1");
        $stmt->execute([$email]);
        $clash = $stmt->fetch();
        if ($clash) {
            if ($clash['deleted_at'] !== null) {
                $errors['email'] = 'A deleted account still holds this email (' . $clash['name']
                                 . ') — restore it from Users instead of creating a second one';
            } else {
                $held = $db->prepare("SELECT p.person_code FROM people p WHERE p.user_id = ? LIMIT 1");
                $held->execute([(int) $clash['id']]);
                $owner = $held->fetch();
                $errors['email'] = $owner
                    ? 'That email is already the login of directory entry ' . $owner['person_code']
                    : 'A user with this email already exists, but no directory entry claims it — use "Link the existing account" on the profile instead of creating a second login';
            }
        }
    }

    $grant = accountGrantableRoleIds($db, $data['roles'] ?? [], $actorId);
    if ($grant['refused']) {
        $errors['roles'] = 'You may only grant roles you hold yourself: ' . implode(', ', $grant['refused'])
                         . ' cannot be assigned by this account.';
    }

    // An account created from the Users module for an email that already belongs to
    // a directory entry is the same human: attach it instead of leaving the profile
    // saying "cannot log in" next to a live login. Ambiguity is not guessed at.
    $attachedCode = null;
    if ($personId === 0 && empty($errors['email'])) {
        $stmt = $db->prepare("SELECT id, person_code FROM people
                              WHERE LOWER(email) = ? AND (user_id IS NULL OR user_id = 0) LIMIT 1");
        $stmt->execute([$email]);
        if ($match = $stmt->fetch()) {
            $personId = (int) $match['id'];
            $attachedCode = $match['person_code'];
        }
    }

    if ($personId > 0) {
        $stmt = $db->prepare("SELECT id, person_code, user_id FROM people WHERE id = ? LIMIT 1");
        $stmt->execute([$personId]);
        $person = $stmt->fetch();
        if (!$person) {
            $errors['person_id'] = 'Directory entry not found';
        } elseif ((int) $person['user_id'] > 0) {
            $errors['person_id'] = 'That person already has a login (' . $person['person_code'] . ')';
            $personId = 0;
        } else {
            $attachedCode = $person['person_code'];
        }
    }

    if ($errors) {
        return ['user_id' => 0, 'errors' => $errors, 'person_id' => 0, 'person_code' => null];
    }

    $own = $db->inTransaction();
    if (!$own) {
        $db->beginTransaction();
    }

    try {
        $stmt = $db->prepare("INSERT INTO users (name, email, password, status, created_by) VALUES (?, ?, ?, ?, ?)");
        $stmt->execute([$name, $email, password_hash($password, PASSWORD_DEFAULT), $status, $actorId]);
        $userId = (int) $db->lastInsertId();

        $roleStmt = $db->prepare("INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)");
        foreach ($grant['ids'] as $roleId) {
            $roleStmt->execute([$userId, $roleId]);
        }

        if ($personId > 0) {
            // people has no created_by/updated_by columns; the audit line is the trail.
            $db->prepare("UPDATE people SET user_id = ? WHERE id = ?")->execute([$userId, $personId]);
        }

        if (!$own) {
            $db->commit();
        }
    } catch (Exception $e) {
        if (!$own) {
            $db->rollBack();
        }
        throw $e;
    }

    $roleNote = $grant['ids'] ? ' — roles [' . implode(', ', roleNamesFor($db, $grant['ids'])) . ']' : ' — no role yet';
    logAudit($actorId, 'Created login: ' . $email . $roleNote
        . ($personId > 0 ? ' for ' . ($attachedCode ?: "#$personId") : ''), 'users');

    // Deliberately no flash() here: the two callers report this outcome in the words
    // their own screen needs, and a helper that also writes to the session is how a
    // success message ends up attached to a refusal.
    return ['user_id' => $userId, 'errors' => [], 'person_id' => $personId, 'person_code' => $attachedCode];
}

/**
 * Attach a login that already exists but belongs to nobody.
 *
 * The common shape of this in a real office: someone was given an account months
 * ago, the directory entry was made later (or the link was detached), and creating
 * "a new login" would either collide on email or leave two accounts for one human.
 */
function accountAttachExistingPerson($db, $userId, $personId, $actorId)
{
    $userId = (int) $userId;
    $personId = (int) $personId;

    $stmt = $db->prepare("SELECT id, person_code FROM people WHERE id = ? LIMIT 1");
    $stmt->execute([$personId]);
    $person = $stmt->fetch();
    if (!$person) {
        return 'Directory entry not found.';
    }
    if (!empty($person['user_id'])) {
        return 'That person already has a login attached.';
    }

    $stmt = $db->prepare("SELECT id, email, status, deleted_at FROM users WHERE id = ? LIMIT 1");
    $stmt->execute([$userId]);
    $user = $stmt->fetch();
    if (!$user) {
        return 'That login account no longer exists.';
    }
    if ($user['deleted_at'] !== null) {
        return 'That account is deleted — restore it from Users first.';
    }

    // people.user_id is indexed but not unique, so the application is the only thing
    // standing between one account serving two directory entries.
    $stmt = $db->prepare("SELECT person_code FROM people WHERE user_id = ? LIMIT 1");
    $stmt->execute([$userId]);
    if ($owner = $stmt->fetch()) {
        return 'That login is already attached to ' . $owner['person_code'] . '.';
    }

    $db->prepare("UPDATE people SET user_id = ? WHERE id = ?")->execute([$userId, $personId]);

    logAudit($actorId, 'Linked login ' . $user['email'] . ' to ' . $person['person_code'], 'users');
    return null;
}

/**
 * The unclaimed account whose email matches this person, if there is one.
 *
 * @return array|null id, name, email, status
 */
function accountUnclaimedForPerson($db, $person)
{
    $email = trim((string) ($person['user_email'] ?: $person['email']));
    if ($email === '' || !empty($person['user_id'])) {
        return null;
    }

    $stmt = $db->prepare("SELECT u.id, u.name, u.email, u.status FROM users u
                          WHERE LOWER(u.email) = LOWER(?) AND u.deleted_at IS NULL
                            AND NOT EXISTS (SELECT 1 FROM people p WHERE p.user_id = u.id)
                          LIMIT 1");
    $stmt->execute([$email]);
    $row = $stmt->fetch();
    return $row ?: null;
}
/**
 * Detach a login from a directory entry without deleting either.
 *
 * Used when a person leaves and their account is closed but the history (employee,
 * customer or contractor records) must stay readable.
 */
function accountDetachPerson($db, $personId, $actorId)
{
    $personId = (int) $personId;
    $stmt = $db->prepare("SELECT id, user_id, person_code FROM people WHERE id = ? LIMIT 1");
    $stmt->execute([$personId]);
    $person = $stmt->fetch();

    if (!$person || empty($person['user_id'])) {
        return 'That directory entry has no login attached.';
    }

    $db->prepare("UPDATE people SET user_id = NULL WHERE id = ?")->execute([$personId]);

    logAudit($actorId, 'Detached login #' . (int) $person['user_id'] . ' from ' . $person['person_code'], 'users');
    return null;
}
