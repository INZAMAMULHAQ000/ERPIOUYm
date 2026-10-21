<?php
/**
 * Shared definition of the engagement (contract) field set.
 *
 * The same terms are entered in two places: on their own in contract_form.php,
 * and inline on the contractor master form so registering a person and opening
 * their first engagement is one action rather than two screens. Defining the
 * fields twice would let the two copies drift, so both pages call these.
 */

/**
 * Option lists for the engagement fields, loaded once per request.
 *
 * $companyId narrows the people and projects that can legitimately be chosen.
 * Passing null keeps every row visible, which is what an engagement with no
 * company selected yet must render — the two dependent lists are disabled in
 * the browser until a company is picked.
 */
function contractorEngagementOptions($db, $companyId = null)
{
    $vendorOpts = [];
    foreach ($db->query("SELECT id, vendor_code, vendor_name FROM vendors WHERE status='active' ORDER BY vendor_name") as $v) {
        $vendorOpts[$v['id']] = ($v['vendor_code'] ? $v['vendor_code'] . ' — ' : '') . $v['vendor_name'];
    }

    $empSql = "SELECT id, first_name, last_name FROM employees WHERE status='active'";
    $projSql = "SELECT id, project_name FROM projects";
    $poSql = "SELECT id, po_number FROM purchase_orders";
    $empParams = $projParams = [];
    if ($companyId) {
        $empSql .= " AND company_id = ?";
        $empParams[] = $companyId;
        $projSql .= " WHERE company_id = ?";
        $projParams[] = $companyId;
    }
    $empStmt = $db->prepare($empSql . " ORDER BY first_name");
    $empStmt->execute($empParams);
    $empOpts = [];
    foreach ($empStmt as $e) {
        $empOpts[$e['id']] = trim($e['first_name'] . ' ' . $e['last_name']);
    }

    $projStmt = $db->prepare($projSql . " ORDER BY project_name LIMIT 400");
    $projStmt->execute($projParams);

    return [
        'type_labels'   => lookupOptions('contractor.contract_type', [
            'statement_of_work' => 'Statement of Work (SOW)', 'purchase_order' => 'Purchase Order',
            'direct_engagement' => 'Direct Engagement', 'retainer' => 'Retainer',
            'framework_agreement' => 'Framework Agreement', 'master_service_agreement' => 'Master Service Agreement',
            'staffing_placement' => 'Agency Staffing Placement',
        ]),
        'arrangements'  => lookupOptions('contractor.work_arrangement', ['on_site' => 'On-site', 'off_site' => 'Off-site', 'hybrid' => 'Hybrid', 'remote' => 'Remote']),
        'billing'       => lookupOptions('contractor.billing_frequency', ['weekly' => 'Weekly', 'bi_weekly' => 'Every two weeks', 'monthly' => 'Monthly', 'quarterly' => 'Quarterly', 'upon_milestone' => 'Upon milestone', 'upon_delivery' => 'Upon delivery']),
        'rate_bases'    => contractorRateBases(),
        'payment_terms' => lookupOptions('trade.payment_terms', []),
        'vendors'       => $vendorOpts,
        'departments'   => array_column($db->query("SELECT id, department_name FROM departments WHERE status='active' ORDER BY department_name")->fetchAll(), 'department_name', 'id'),
        'designations'  => array_column($db->query("SELECT id, designation_name FROM designations WHERE status='active' ORDER BY designation_name")->fetchAll(), 'designation_name', 'id'),
        'employees'     => $empOpts,
        'projects'      => array_column($projStmt->fetchAll(), 'project_name', 'id'),
        'purchase_orders' => array_column($db->query("SELECT id, po_number FROM purchase_orders ORDER BY id DESC LIMIT 300")->fetchAll(), 'po_number', 'id'),
        'currencies'    => array_column($db->query("SELECT code, name FROM currencies WHERE is_active = 1 ORDER BY sort_order")->fetchAll(), 'name', 'code'),
    ];
}

/**
 * Section descriptors for contractorRenderSection(). $withNumber shows the
 * contract number card, which only makes sense on the dedicated contract form;
 * on the master form the number is shown as a read-only caption instead.
 *
 * $companyId drives the initial disabled state of the two company-dependent
 * lists, so the form is correct before any script runs.
 */
function contractorEngagementSections(array $opts, $withNumber = true, $companyId = null)
{
    $sections = [];
    $dependent = !$companyId;

    if ($withNumber) {
        $sections[] = ['title' => 'Contract', 'icon' => 'fa-hashtag', 'lockable' => true, 'fields' => [
            ['n' => 'contract_number', 'l' => 'Contract Number', 't' => 'static', 'span' => 1,
             'hint' => 'Allocated from the numbering scheme'],
        ]];
    }

    $sections[] = ['title' => 'Engagement', 'icon' => 'fa-file-signature', 'lockable' => true, 'fields' => [
        ['n' => 'title', 'l' => 'Contract Title', 't' => 'text', 'span' => 2, 'req' => true, 'ph' => 'e.g. Substation commissioning support'],
        ['n' => 'contract_type', 'l' => 'Contract Type', 't' => 'select', 'opts' => $opts['type_labels'], 'span' => 1],
        ['n' => 'supply_source', 'l' => 'Supply Source', 't' => 'select', 'span' => 1, 'blank' => '',
         'opts' => ['direct' => 'Direct (we engage the person)', 'agency' => 'Agency-supplied']],
        ['n' => 'agency_vendor_id', 'l' => 'Supplying Vendor / Agency', 't' => 'select', 'opts' => $opts['vendors'], 'span' => 2,
         'blank' => '— Direct, no agency —', 'hint' => 'Required when agency-supplied; invoices route through this vendor'],
        ['n' => 'purchase_order_id', 'l' => 'Linked Purchase Order', 't' => 'select', 'opts' => $opts['purchase_orders'], 'span' => 1, 'blank' => '— None —'],
        ['n' => 'po_reference', 'l' => 'External PO / Ref.', 't' => 'text', 'span' => 1, 'hint' => 'When the PO lives outside this ERP'],
    ]];

    $sections[] = ['title' => 'Scope of Work', 'icon' => 'fa-list-check', 'lockable' => true, 'fields' => [
        ['n' => 'scope_of_work', 'l' => 'Deliverables and scope', 't' => 'textarea', 'span' => 4, 'rows' => 4],
    ]];

    $sections[] = ['title' => 'Assignment & Term', 'icon' => 'fa-calendar-range', 'lockable' => true, 'fields' => [
        ['n' => 'start_date', 'l' => 'Start Date', 't' => 'date', 'span' => 1, 'req' => true],
        ['n' => 'end_date', 'l' => 'End Date', 't' => 'date', 'span' => 1, 'hint' => 'Blank = open-ended'],
        ['n' => 'department_id', 'l' => 'Department', 't' => 'select', 'opts' => $opts['departments'], 'span' => 1, 'blank' => '— Not set —'],
        ['n' => 'designation_id', 'l' => 'Designation', 't' => 'select', 'opts' => $opts['designations'], 'span' => 1, 'blank' => '— Not set —'],
        ['n' => 'contractual_job_title', 'l' => 'Contractual Job Title', 't' => 'text', 'span' => 2, 'hint' => 'As written on the contract, independent of the designation list'],
        ['n' => 'company_id', 'l' => 'Company', 't' => 'company', 'span' => 1,
         'attrs' => ['data-cascade-master' => 'engagement-scope'],
         'hint' => 'Sets which Reporting Manager and Project you may choose'],
        ['n' => 'manager_employee_id', 'l' => 'Reporting Manager', 't' => 'select', 'opts' => $opts['employees'], 'span' => 1, 'blank' => '— Not set —',
         'dis' => $dependent,
         'attrs' => ['data-cascade-child' => 'engagement-scope', 'data-cascade-source' => 'employees']],
        ['n' => 'project_id', 'l' => 'Project', 't' => 'select', 'opts' => $opts['projects'], 'span' => 1, 'blank' => '— None —',
         'dis' => $dependent,
         'attrs' => ['data-cascade-child' => 'engagement-scope', 'data-cascade-source' => 'projects']],
        ['n' => 'work_arrangement', 'l' => 'Work Arrangement', 't' => 'select', 'opts' => $opts['arrangements'], 'span' => 1, 'blank' => '— Not set —'],
        ['n' => 'fte_allocation', 'l' => 'Allocation %', 't' => 'number', 'span' => 1, 'step' => '0.01', 'min' => '0', 'max' => '100'],
        ['n' => 'timesheet_required', 'l' => 'Timesheets required', 't' => 'checkbox', 'span' => 1, 'hint' => 'Engagement is billed against recorded hours'],
        ['n' => 'security_clearance', 'l' => 'Security Clearance', 't' => 'text', 'span' => 1],
        ['n' => 'badge_number', 'l' => 'Badge / Access Card', 't' => 'text', 'span' => 1],
    ]];

    $sections[] = ['title' => 'Commercial Terms', 'icon' => 'fa-coins', 'lockable' => true, 'fields' => [
        ['n' => 'rate_basis', 'l' => 'Rate Basis', 't' => 'select', 'opts' => $opts['rate_bases'], 'span' => 1, 'blank' => '— Not set —'],
        ['n' => 'rate_amount', 'l' => 'Rate', 't' => 'number', 'span' => 1, 'step' => '0.01', 'min' => '0'],
        ['n' => 'currency_code', 'l' => 'Currency', 't' => 'select', 'opts' => $opts['currencies'], 'span' => 1, 'blank' => '— Default —'],
        ['n' => 'estimated_value', 'l' => 'Estimated Total Value', 't' => 'number', 'span' => 1, 'step' => '0.01', 'min' => '0'],
        ['n' => 'not_to_exceed_amount', 'l' => 'Not-to-Exceed', 't' => 'number', 'span' => 1, 'step' => '0.01', 'min' => '0', 'hint' => 'Hard ceiling for SOW engagements'],
        ['n' => 'billing_frequency', 'l' => 'Billing Frequency', 't' => 'select', 'opts' => $opts['billing'], 'span' => 1, 'blank' => '— Not set —'],
        ['n' => 'payment_terms', 'l' => 'Payment Terms', 't' => 'select', 'opts' => $opts['payment_terms'], 'span' => 1, 'blank' => '— Not set —'],
    ]];

    $sections[] = ['title' => 'Extension Control', 'icon' => 'fa-rotate', 'lockable' => true, 'fields' => [
        ['n' => 'extension_limit', 'l' => 'Max Extensions', 't' => 'number', 'span' => 1, 'min' => '0', 'max' => '999', 'hint' => 'Blank = no agreed ceiling'],
        ['n' => 'extension_period_days', 'l' => 'Extension Period (days)', 't' => 'number', 'span' => 1, 'min' => '1', 'max' => '3650'],
    ]];

    return $sections;
}

/**
 * Script behind the Company -> Reporting Manager / Project cascade.
 *
 * Emitted as a function rather than inline because the same engagement block is
 * rendered by two pages (the contractor master form and the standalone contract
 * form), and a second copy would drift from the first.
 */
function contractorEngagementCascadeScript()
{
    $endpoint = htmlspecialchars(url('modules/contractors/ajax_engagement_options.php'), ENT_QUOTES);
    ?>
<script>
(function () {
    var ENDPOINT = <?= json_encode($endpoint) ?>;

    function blankText(select) {
        return select.getAttribute('data-cascade-blank') || '— Not set —';
    }

    /** Rebuild the option list, keeping `keep` only if the new list offers it. */
    function populate(select, rows, keep) {
        select.innerHTML = '';
        var blank = document.createElement('option');
        blank.value = '';
        blank.textContent = blankText(select);
        select.appendChild(blank);

        rows.forEach(function (row) {
            var opt = document.createElement('option');
            opt.value = row.id;
            opt.textContent = row.label;
            select.appendChild(opt);
        });

        // A stored manager or project that has moved to another company is
        // dropped rather than silently re-posted under the new one.
        select.value = keep || '';
        if (select.value !== (keep || '')) { select.value = ''; }
        select.dispatchEvent(new Event('change', { bubbles: true }));
    }

    function wire(master) {
        var group = master.getAttribute('data-cascade-master');
        var children = Array.prototype.slice.call(
            document.querySelectorAll('[data-cascade-child="' + group + '"]')
        );
        if (!children.length) { return; }

        children.forEach(function (c) {
            var first = c.querySelector('option');
            c.setAttribute('data-cascade-blank', first ? first.textContent : '— Not set —');
            c._token = 0;
        });

        function load(child, companyId, keep) {
            child.disabled = true;
            var mine = ++child._token;
            var source = child.getAttribute('data-cascade-source');

            if (!companyId) {
                populate(child, [], '');
                return;
            }

            fetch(ENDPOINT + '?action=' + encodeURIComponent(source) + '&company_id=' + encodeURIComponent(companyId), {
                credentials: 'same-origin'
            }).then(function (r) {
                if (!r.ok) { throw new Error('HTTP ' + r.status); }
                return r.json();
            }).then(function (json) {
                // Each child tracks its own request, so a slow answer for an
                // earlier company cannot overwrite the list now on screen —
                // and cannot make its sibling look stale.
                if (mine !== child._token) { return; }
                if (!json || json.success !== true) { throw new Error((json && json.error) || 'Failed'); }
                populate(child, json.data || [], keep);
                child.disabled = false;
            }).catch(function () {
                if (mine !== child._token) { return; }
                populate(child, [], '');
                child.disabled = true;
            });
        }

        // First run keeps the stored selection; a later company change is a
        // deliberate user action, so the old choices are cleared.
        var first = true;
        function sync() {
            var keep = first;
            first = false;
            var companyId = master.value;
            children.forEach(function (c) {
                load(c, companyId, keep ? c.value : '');
            });
        }

        master.addEventListener('change', sync);
        sync();
    }

    function start() {
        Array.prototype.forEach.call(document.querySelectorAll('[data-cascade-master]'), wire);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', start);
    } else {
        start();
    }
})();
</script>
    <?php
}

/**
 * Did the user actually fill the inline engagement block? Empty blocks on the
 * master form must not create an empty draft contract.
 */
function contractorEngagementPosted(array $post)
{
    foreach (['title', 'contract_type', 'scope_of_work', 'start_date', 'end_date', 'rate_amount',
              'agency_vendor_id', 'purchase_order_id', 'department_id', 'project_id',
              'estimated_value', 'not_to_exceed_amount', 'contractual_job_title'] as $field) {
        if (trim((string) ($post[$field] ?? '')) !== '') {
            return true;
        }
    }
    return !empty($post['timesheet_required']);
}
