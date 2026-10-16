<?php
$pageTitle = 'Login Access';
require_once '../../includes/header.php';
require_once '../../helpers/redirect.php';
require_once '../../helpers/people_onboarding.php';
require_once '../../helpers/account.php';

/**
 * Give a directory entry a login account, or take the link away again.
 *
 * Posting only, and deliberately not a page anyone lands on by typing a URL: the
 * form lives on the person's profile so the state you act on is the state you see.
 * Creating the account itself is delegated to accountCreate() — the same code the
 * Users module runs — so a login minted from here cannot be shaped differently
 * from one minted over there.
 */

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    flash('error', 'Login access is changed from the person\u2019s profile.', 'error');
    to('modules/people_management/index.php');
}

if (!verifyCsrf($_POST['csrf_token'] ?? '')) {
    flash('error', 'Invalid security token. Please try again.', 'error');
    to('modules/people_management/view.php?id=' . (int) ($_POST['id'] ?? 0));
}

$id = (int) ($_POST['id'] ?? 0);
$action = $_POST['account_action'] ?? 'grant';
$db = getDB();

$person = peopleLoad($db, $id);
if (!$person) {
    flash('error', 'Person not found.', 'error');
    to('modules/people_management/index.php');
}

$back = 'modules/people_management/view.php?id=' . $id;

// Linking an account that already exists but belongs to nobody: the common shape
// of "give this person a login" in an office that has been running for a while.
if ($action === 'link') {
    if (!hasPermission('users.edit') || !hasPermission('people_management.edit')) {
        die('Access Denied');
    }
    if (!empty($person['user_id'])) {
        flash('error', $person['person_code'] . ' already has a login account.', 'error');
        to($back);
    }
    $error = accountAttachExistingPerson($db, (int) ($_POST['user_id'] ?? 0), $id, $_SESSION['user_id']);
    flash($error ? 'error' : 'success',
        $error ?? 'Linked to the existing login. No second account was created.',
        $error ? 'error' : 'success');
    to($back);
}

// Detaching is a smaller change than creating, and it is not the same permission.
if ($action === 'detach') {
    if (!hasPermission('users.edit') || !hasPermission('people_management.edit')) {
        die('Access Denied');
    }
    if (empty($person['user_id'])) {
        flash('error', 'That person has no login to detach.', 'error');
        to($back);
    }
    $error = accountDetachPerson($db, $id, $_SESSION['user_id']);
    flash($error ? 'error' : 'success',
        $error ?? 'The login is no longer attached to this person. The account itself was not deleted.',
        $error ? 'error' : 'success');
    to($back);
}

// A login that can open no module is useless, so granting needs both the right to
// create accounts and the right to edit this directory entry.
if (!hasPermission('users.create') || !hasPermission('people_management.edit')) {
    die('Access Denied');
}

if (!empty($person['user_id'])) {
    flash('error', $person['person_code'] . ' already has a login account.', 'error');
    to($back);
}

if (trim((string) ($_POST['email'] ?? '')) === '' && trim((string) $person['email']) === '') {
    flash('error', 'This person has no email address, and an email is what a login is identified by. '
        . 'Add the email to the record first.', 'error');
    to($back);
}

$result = accountCreate($db, [
    'name'     => $_POST['name'] ?? ($person['first_name'] . ' ' . (string) $person['last_name']),
    'email'    => $_POST['email'] ?? $person['email'],
    'password' => $_POST['password'] ?? '',
    'status'   => $_POST['status'] ?? 'active',
    'roles'    => $_POST['roles'] ?? [],
    'person_id' => $id,
], $_SESSION['user_id']);

if ($result['errors']) {
    // flash() is keyed, so one message per key would leave only the last; the
    // whole refusal is reported as a single notice instead.
    flash('error', 'Login not created: ' . implode(' ', $result['errors']), 'error');
    to($back);
}

flash('success', $person['first_name'] . ' ' . (string) $person['last_name']
    . ' can now sign in as ' . strtolower(trim((string) ($_POST['email'] ?? $person['email']))) . '.', 'success');
to($back);
