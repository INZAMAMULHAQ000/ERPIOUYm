<?php
/**
 * Active company context.
 *
 * Resolves the company the current request operates against. Nothing here is
 * hardcoded: the session value wins, otherwise the company flagged
 * `is_default` is used, otherwise the lowest active company id.
 */

require_once __DIR__ . '/security.php';
require_once __DIR__ . '/url.php';

if (!function_exists('companyLogoUrl')) {
    /**
     * Public URL for a companies.logo_path value, or null when there is none.
     *
     * The column holds either an uploaded path relative to the app root or, for
     * rows created before uploads existed, an external URL. url() passes
     * absolute URLs straight through and prefixes everything else with BASE_URL,
     * so both render from any directory and on any host.
     */
    function companyLogoUrl($logoPath) {
        $value = trim((string) $logoPath);
        if ($value === '') { return null; }
        return isAbsoluteUrl($value) ? $value : url($value);
    }
}

if (!function_exists('activeCompanyLogoUrl')) {
    /** Logo for the company a document is being produced for. */
    function activeCompanyLogoUrl($companyId = null) {
        $id = $companyId === null ? (int) activeCompanyId() : (int) $companyId;
        if ($id <= 0) { return null; }
        static $cache = [];
        if (array_key_exists($id, $cache)) { return $cache[$id]; }
        try {
            $s = getDB()->prepare("SELECT logo_path FROM companies WHERE id = ? AND deleted_at IS NULL");
            $s->execute([$id]);
            return $cache[$id] = companyLogoUrl($s->fetchColumn());
        } catch (Throwable $e) {
            return $cache[$id] = null;
        }
    }
}

if (!function_exists('appSetting')) {
    /** Typed accessor for the app_settings table. Cached per request. */
    function appSetting($key, $default = null) {
        static $cache = [];
        if (array_key_exists($key, $cache)) { return $cache[$key]; }
        try {
            $s = getDB()->prepare("SELECT setting_value, value_type FROM app_settings WHERE setting_key = ?");
            $s->execute([$key]);
            $row = $s->fetch();
            if (!$row || $row['setting_value'] === null) { return $cache[$key] = $default; }
            $v = $row['setting_value'];
            $out = match ($row['value_type']) {
                'boolean' => in_array(strtolower((string) $v), ['1', 'true', 'yes'], true),
                'integer' => (int) $v,
                'decimal' => (float) $v,
                'json'    => json_decode((string) $v, true),
                default   => (string) $v,
            };
            return $cache[$key] = $out;
        } catch (Throwable $e) {
            return $cache[$key] = $default;
        }
    }
}

if (!function_exists('appName')) {
    function appName() {
        return appSetting('app_name', 'ERP System') ?: 'ERP System';
    }
}

if (!function_exists('activeCompany')) {
    /** Full companies row for the active company, or null if none is configured. */
    function activeCompany() {
        static $cache = null;
        if ($cache !== null) { return $cache; }

        $db = getDB();
        $uid = (int) ($_SESSION['user_id'] ?? 0);
        $wanted = (int) ($_SESSION['active_company_id'] ?? 0);

        $sql = "
            SELECT * FROM companies c
            WHERE c.deleted_at IS NULL AND c.status = 'active'
              AND (
                    EXISTS (SELECT 1 FROM user_roles ur WHERE ur.user_id = ? AND ur.role_id = 1)
                 OR EXISTS (SELECT 1 FROM user_companies uc WHERE uc.user_id = ? AND uc.company_id = c.id)
              )
        ";
        $params = [$uid, $uid];

        $order = [];
        if ($wanted > 0) {
            // Rank the user's chosen company first without excluding the others,
            // so an inaccessible or deleted preference degrades to the default.
            $order[] = '(c.id = ?) DESC';
            $params[] = $wanted;
        }
        $order[] = 'c.is_default DESC';
        $order[] = 'c.id ASC';
        $sql .= ' ORDER BY ' . implode(', ', $order) . ' LIMIT 1';

        // The preference only applies when the user may actually use that company,
        // so fall back through is_default rather than leaking an inaccessible one.
        $stmt = $db->prepare($sql);
        $stmt->execute($params);
        $row = $stmt->fetch() ?: null;

        if ($row && $wanted > 0 && (int) $row['id'] !== $wanted) {
            unset($_SESSION['active_company_id']);
        }
        if ($row) {
            $_SESSION['active_company_id'] = (int) $row['id'];
        }
        $cache = $row;
        return $cache;
    }
}

if (!function_exists('activeCompanyId')) {
    function activeCompanyId() {
        $c = activeCompany();
        return $c ? (int) $c['id'] : 0;
    }
}

if (!function_exists('activeCompanyCurrency')) {
    function activeCompanyCurrency($fallback = null) {
        $c = activeCompany();
        if ($c) { return $c['base_currency']; }
        if ($fallback !== null) { return $fallback; }
        $s = getDB()->prepare("SELECT setting_value FROM app_settings WHERE setting_key = 'base_currency'");
        $s->execute();
        return $s->fetchColumn() ?: 'USD';
    }
}

if (!function_exists('companyFilterSql')) {
    /**
     * SQL fragment restricting rows to the active company.
     * $allowNull keeps shared rows (e.g. a group chart of accounts) visible.
     */
    function companyFilterSql($column, &$params, $allowNull = false) {
        $id = activeCompanyId();
        if ($id <= 0) { return ''; }
        $params[] = $id;
        return $allowNull
            ? " ($column IS NULL OR $column = ?)"
            : " $column = ?";
    }
}

if (!function_exists('accessibleCompanies')) {
    /**
     * Companies the signed-in user may own records in.
     *
     * Same rule as activeCompany() and CompanyService: role 1 (Super Admin) sees
     * every active company, everyone else only their user_companies grants. Kept
     * here rather than in the finance service because every module loads helpers.
     */
    function accessibleCompanies() {
        static $cache = null;
        if ($cache !== null) { return $cache; }
        $db = getDB();
        $uid = (int) ($_SESSION['user_id'] ?? 0);
        try {
            if ($uid && activeCompanyIsSuperAdmin($uid)) {
                $rows = $db->query("
                    SELECT id, company_code, company_name FROM companies
                    WHERE deleted_at IS NULL AND status = 'active'
                    ORDER BY is_default DESC, company_name ASC
                ")->fetchAll();
            } else {
                $s = $db->prepare("
                    SELECT c.id, c.company_code, c.company_name
                    FROM user_companies uc
                    JOIN companies c ON c.id = uc.company_id
                    WHERE uc.user_id = ? AND c.deleted_at IS NULL AND c.status = 'active'
                    ORDER BY c.is_default DESC, c.company_name ASC
                ");
                $s->execute([$uid]);
                $rows = $s->fetchAll();
            }
        } catch (Throwable $e) {
            error_log('accessibleCompanies failed: ' . $e->getMessage());
            $rows = [];
        }
        // A user with no grants must still be able to transact against the
        // company they actually resolve to, or the dropdown would be empty.
        if (!$rows) {
            $active = activeCompany();
            if ($active) {
                $rows = [[
                    'id' => $active['id'],
                    'company_code' => $active['company_code'],
                    'company_name' => $active['company_name'],
                ]];
            }
        }
        return $cache = $rows;
    }
}

if (!function_exists('activeCompanyIsSuperAdmin')) {
    function activeCompanyIsSuperAdmin($userId = null) {
        $uid = (int) ($userId ?? ($_SESSION['user_id'] ?? 0));
        if (!$uid) { return false; }
        try {
            $s = getDB()->prepare("SELECT COUNT(*) FROM user_roles WHERE user_id = ? AND role_id = 1");
            $s->execute([$uid]);
            return (int) $s->fetchColumn() > 0;
        } catch (Throwable $e) {
            return false;
        }
    }
}

if (!function_exists('companyOptions')) {
    /** [id => label] for the companies the user may select. */
    function companyOptions() {
        $out = [];
        foreach (accessibleCompanies() as $c) {
            $label = (string) $c['company_name'];
            $code = trim((string) ($c['company_code'] ?? ''));
            $out[(int) $c['id']] = $code !== '' ? "$label ($code)" : $label;
        }
        return $out;
    }
}

if (!function_exists('resolveCompanyForSave')) {
    /**
     * The company a submitted form is allowed to write.
     *
     * The dropdown is only a convenience — the posted value is attacker
     * controlled, so a form must never persist `$_POST['company_id']` directly.
     * An out-of-scope id is rejected rather than silently swapped, because a
     * record landing in the wrong company is a bookkeeping error, not a typo.
     *
     * @return int|null  null means "no company selected".
     * @throws RuntimeException when the selection is not the user's to make.
     */
    function resolveCompanyForSave($posted, $required = false) {
        $options = companyOptions();
        $id = (int) $posted;

        if ($id <= 0) {
            if ($required) {
                throw new RuntimeException('A company must be selected.');
            }
            return null;
        }
        if (!array_key_exists($id, $options)) {
            throw new RuntimeException('You are not permitted to assign records to that company.');
        }
        return $id;
    }
}

if (!function_exists('renderCompanySelect')) {
    /**
     * Company dropdown shared by every module that owns records per company, so
     * the access rule, blank option and selected state are not re-implemented
     * per form.
     *
     * @param array $attrs  name/class/id/required/onchange/blank/placeholder
     */
    function renderCompanySelect($name = 'company_id', $selected = null, array $attrs = []) {
        $options = companyOptions();
        $class   = $attrs['class'] ?? 'w-full px-3 py-2 border rounded focus:ring-2 focus:ring-blue-500';
        $id      = $attrs['id'] ?? $name;
        $blank   = array_key_exists('blank', $attrs) ? (string) $attrs['blank'] : 'Select Company';
        $onchange = $attrs['onchange'] ?? '';
        $required = !empty($attrs['required']);
        $extra = '';
        // Pass through any data-* attribute; cascading dropdowns key off these.
        foreach ($attrs as $k => $v) {
            if (strpos($k, 'data-') === 0) {
                $extra .= ' ' . $k . '="' . htmlspecialchars((string) $v, ENT_QUOTES) . '"';
            }
        }

        $html  = '<select name="' . htmlspecialchars($name, ENT_QUOTES) . '" id="' . htmlspecialchars($id, ENT_QUOTES) . '"';
        $html .= ' class="' . htmlspecialchars($class, ENT_QUOTES) . '"';
        if ($required) { $html .= ' required'; }
        if ($onchange !== '') { $html .= ' onchange="' . htmlspecialchars($onchange, ENT_QUOTES) . '"'; }
        $html .= $extra . '>' . PHP_EOL;
        if ($blank !== '') {
            $html .= '    <option value="">' . htmlspecialchars($blank, ENT_QUOTES) . '</option>' . PHP_EOL;
        }

        // One option only means there is nothing to choose, so preselect it and
        // still submit it — hiding it would drop the value from the POST body.
        if (count($options) === 1 && empty($attrs['force_list'])) {
            $onlyId = (int) array_key_first($options);
            $html .= '    <option value="' . $onlyId . '" selected>' . htmlspecialchars($options[$onlyId], ENT_QUOTES) . '</option>' . PHP_EOL;
            $html .= '</select>';
            return $html;
        }

        $current = $selected === null || $selected === '' ? activeCompanyId() : (int) $selected;
        foreach ($options as $oid => $label) {
            $sel = ((int) $oid === $current) ? ' selected' : '';
            $html .= '    <option value="' . (int) $oid . '"' . $sel . '>' . htmlspecialchars((string) $label, ENT_QUOTES) . '</option>' . PHP_EOL;
        }
        $html .= '</select>';
        return $html;
    }
}

if (!function_exists('companyLabel')) {
    /** Display name for a stored company_id, without assuming it is accessible. */
    function companyLabel($companyId) {
        $id = (int) $companyId;
        if ($id <= 0) { return null; }
        static $labels = null;
        if ($labels === null) {
            $labels = [];
            try {
                foreach (getDB()->query("SELECT id, company_name FROM companies")->fetchAll() as $r) {
                    $labels[(int) $r['id']] = $r['company_name'];
                }
            } catch (Throwable $e) {
                $labels = [];
            }
        }
        return $labels[$id] ?? ('#' . $id);
    }
}

if (!function_exists('applyCompanyScope')) {
    /**
     * Company predicate for a list view.
     *
     * Three states, so a reviewer is never stuck:
     *   no ?company_id     -> scope to the active company (the navbar switcher)
     *   ?company_id=<id>   -> narrow to that company, if the user may see it
     *   ?company_id=       -> widen to every company the user can access
     *
     * An out-of-scope id degrades to "all accessible" rather than silently
     * showing another company's rows.
     *
     * @return int|null  null when scoping to the active company, else the id
     *                   the filter should render as selected (0 = all).
     */
    function applyCompanyScope($column, &$where, &$params) {
        if (!array_key_exists('company_id', $_GET)) {
            $frag = companyFilterSql($column, $params);
            // companyFilterSql() yields a bare predicate, so it has to be joined
            // with AND — and must not consume a param when it returns nothing.
            if ($frag !== '') { $where .= " AND" . $frag; }
            return null;
        }
        $cid = (int) $_GET['company_id'];
        if ($cid > 0 && array_key_exists($cid, companyOptions())) {
            $where .= " AND $column = ?";
            $params[] = $cid;
            return $cid;
        }
        return 0;
    }
}

if (!function_exists('nextDocumentNumber')) {
    /**
     * Allocation-safe document number.
     *
     * Replaces the old COUNT(*)+1 generators, which produced duplicate numbers
     * under concurrency and reused a number after any deletion. The counter row
     * is bumped and read in a single atomic UPDATE, and the rendered shape comes
     * from the sequence's own `format` template so existing numbering is preserved.
     *
     * @param string $docType  document_sequences.doc_type
     * @param string|null $periodKey  overrides the sequence's date_format period
     */
    function nextDocumentNumber($db, $docType, $periodKey = null) {
        $companyId = activeCompanyId();
        if ($companyId <= 0) {
            throw new RuntimeException('No active company — cannot allocate a document number.');
        }

        $stmt = $db->prepare("SELECT * FROM document_sequences WHERE company_id = ? AND doc_type = ? AND period_key = '' LIMIT 1");
        $stmt->execute([$companyId, $docType]);
        $base = $stmt->fetch();
        if (!$base) {
            throw new RuntimeException("No document sequence configured for '$docType'. Add it under Configuration → Document Numbering.");
        }

        // Resolve the period this number belongs to ('' = one counter for all time).
        if ($periodKey === null) {
            $periodKey = $base['date_format'] ? date($base['date_format']) : '';
        }

        // Materialise the counter row for this period, inheriting the template.
        $db->prepare("
            INSERT INTO document_sequences (company_id, doc_type, period_key, prefix, padding, date_format, format, next_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            ON DUPLICATE KEY UPDATE document_sequences.id = document_sequences.id
        ")->execute([$companyId, $docType, $periodKey, $base['prefix'], $base['padding'], $base['date_format'], $base['format']]);

        // Single atomic read-and-increment: LAST_INSERT_ID() yields the value before the bump.
        $db->prepare("
            UPDATE document_sequences
               SET next_number = LAST_INSERT_ID(next_number) + 1
             WHERE company_id = ? AND doc_type = ? AND period_key = ?
        ")->execute([$companyId, $docType, $periodKey]);
        $allocated = (int) $db->query("SELECT LAST_INSERT_ID()")->fetchColumn();

        $fy = getCompanyFinancialYear($db, $companyId);
        $tokens = [
            '{prefix}'    => (string) $base['prefix'],
            '{seq}'       => str_pad((string) $allocated, max(1, (int) $base['padding']), '0', STR_PAD_LEFT),
            '{period}'    => $periodKey,
            '{year}'      => date('Y'),
            '{month}'     => date('m'),
            '{fy}'        => $fy ? date('Y', strtotime($fy['start_date'])) : date('Y'),
            '{fy_short}'  => $fy ? date('Y', strtotime($fy['start_date'])) . '-' . date('Y', strtotime($fy['end_date'])) : date('Y') . '-' . date('Y'),
        ];

        $format = (string) ($base['format'] ?: '{prefix}{seq}');
        return str_replace(array_keys($tokens), array_values($tokens), $format);
    }
}

if (!function_exists('nextUniqueDocumentNumber')) {
    /**
     * Allocate a document number only if the target column is actually free.
     *
     * `document_sequences` counters are per company, but the master codes they
     * feed — `clients.client_code`, `contractors.contractor_code` — are unique
     * across the whole database. So a second company's counter can hand out a
     * code the first company already used, and the insert dies on error 1062 in
     * front of the user. Re-allocating is cheap and correct; skipping forward
     * leaves a gap, and gaps in a legal document sequence are normal.
     *
     * $table and $column are code-level constants, never request input.
     */
    function nextUniqueDocumentNumber($db, $docType, $table, $column, $maxAttempts = 25) {
        for ($attempt = 0; $attempt < $maxAttempts; $attempt++) {
            $number = nextDocumentNumber($db, $docType);
            $check = $db->prepare("SELECT COUNT(*) FROM `$table` WHERE `$column` = ?");
            $check->execute([$number]);
            if ((int) $check->fetchColumn() === 0) {
                return $number;
            }
        }
        throw new RuntimeException(
            "Could not allocate a unique number for $docType after $maxAttempts attempts — "
            . "check the counter for '$docType' under Configuration → Document Numbering."
        );
    }
}

if (!function_exists('peekDocumentNumber')) {
    /**
     * Render the number the next allocation WOULD produce, without consuming it.
     * Use for form previews: allocating on page view would burn a number every
     * time someone opens and abandons a create form, punching gaps into a legal
     * document sequence.
     */
    function peekDocumentNumber($db, $docType, $periodKey = null) {
        $companyId = activeCompanyId();
        if ($companyId <= 0) {
            throw new RuntimeException('No active company — cannot preview a document number.');
        }
        $stmt = $db->prepare("SELECT * FROM document_sequences WHERE company_id = ? AND doc_type = ? AND period_key = '' LIMIT 1");
        $stmt->execute([$companyId, $docType]);
        $base = $stmt->fetch();
        if (!$base) {
            throw new RuntimeException("No document sequence configured for '$docType'.");
        }
        if ($periodKey === null) {
            $periodKey = $base['date_format'] ? date($base['date_format']) : '';
        }
        $s = $db->prepare("SELECT next_number FROM document_sequences WHERE company_id = ? AND doc_type = ? AND period_key = ?");
        $s->execute([$companyId, $docType, $periodKey]);
        $next = (int) ($s->fetchColumn() ?: 1);

        $fy = getCompanyFinancialYear($db, $companyId);
        $tokens = [
            '{prefix}'   => (string) $base['prefix'],
            '{seq}'      => str_pad((string) $next, max(1, (int) $base['padding']), '0', STR_PAD_LEFT),
            '{period}'   => $periodKey,
            '{year}'     => date('Y'),
            '{month}'    => date('m'),
            '{fy}'       => $fy ? date('Y', strtotime($fy['start_date'])) : date('Y'),
            '{fy_short}' => $fy ? date('Y', strtotime($fy['start_date'])) . '-' . date('Y', strtotime($fy['end_date'])) : date('Y') . '-' . date('Y'),
        ];
        $format = (string) ($base['format'] ?: '{prefix}{seq}');
        return str_replace(array_keys($tokens), array_values($tokens), $format);
    }
}

if (!function_exists('getCompanyFinancialYear')) {
    /** The company's current financial year, or null. Never borrows another's. */
    function getCompanyFinancialYear($db, $companyId) {
        static $cache = [];
        $cid = (int) $companyId;
        if (array_key_exists($cid, $cache)) { return $cache[$cid]; }
        try {
            $s = $db->prepare("
                SELECT * FROM financial_years
                WHERE company_id = ? AND status = 'active'
                  AND CURDATE() BETWEEN start_date AND end_date
                ORDER BY start_date DESC LIMIT 1
            ");
            $s->execute([$cid]);
            $row = $s->fetch() ?: null;
            if (!$row) {
                $s2 = $db->prepare("SELECT * FROM financial_years WHERE company_id = ? AND status = 'active' ORDER BY start_date DESC LIMIT 1");
                $s2->execute([$cid]);
                $row = $s2->fetch() ?: null;
            }
            return $cache[$cid] = $row;
        } catch (Throwable $e) {
            return $cache[$cid] = null;
        }
    }
}
