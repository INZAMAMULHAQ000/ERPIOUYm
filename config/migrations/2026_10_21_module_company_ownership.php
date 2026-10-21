<?php
/**
 * Company ownership for operational masters + Indian-national identity evidence.
 *
 * Closes the change requests raised in the 21 Oct 2026 review:
 *
 *  1. company_id on employees, projects, contractors and assets, so a record
 *     declares its owning registered company instead of inheriting one silently.
 *     Backfilled to the default company so nothing becomes invisible.
 *  2. assets.location — the review asked for an indication of where an asset is
 *     stored; the owning organisation is covered by assets.company_id.
 *  3. employees.aadhaar_number / employees.pan_number — identity evidence that
 *     applies only to Indian nationals.
 *  4. lookup type person.nationality — nationality was free text, so "Indian",
 *     "India " and "India" were three different answers. A controlled list is
 *     what makes the Aadhaar/PAN conditional reliable. Existing free-text values
 *     are normalised to country names.
 *
 * Idempotent — safe to re-run.
 *   php config/migrations/2026_10_21_module_company_ownership.php
 */

require_once __DIR__ . '/../database.php';

$db = getDB();
$DB = DB_NAME;

function hasColumn($db, $table, $col) {
    global $DB;
    $s = $db->prepare("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema=? AND table_name=? AND column_name=?");
    $s->execute([$DB, $table, $col]);
    return (bool) $s->fetchColumn();
}
function addColumn($db, $table, $col, $def, $after = null) {
    if (!hasColumn($db, $table, $col)) {
        $pos = $after ? " AFTER `$after`" : '';
        $db->exec("ALTER TABLE `$table` ADD COLUMN `$col` $def$pos");
        echo "  + $table.$col\n";
    } else {
        echo "  = $table.$col exists\n";
    }
}
function hasIndex($db, $table, $name) {
    global $DB;
    $s = $db->prepare("SELECT COUNT(*) FROM information_schema.statistics WHERE table_schema=? AND table_name=? AND index_name=?");
    $s->execute([$DB, $table, $name]);
    return (bool) $s->fetchColumn();
}
function addIndex($db, $table, $name, $cols) {
    if (hasIndex($db, $table, $name)) { echo "  i $table.$name exists\n"; return; }
    $db->exec("ALTER TABLE `$table` ADD INDEX `$name` ($cols)");
    echo "  i $table.$name\n";
}
function hasConstraint($db, $table, $name) {
    global $DB;
    $s = $db->prepare("SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema=? AND table_name=? AND constraint_name=?");
    $s->execute([$DB, $table, $name]);
    return (bool) $s->fetchColumn();
}
function addFk($db, $table, $name, $col, $ref, $refCol = 'id', $onDel = 'SET NULL') {
    if (hasConstraint($db, $table, $name)) { echo "  -> $table.$name exists\n"; return; }
    $db->exec("ALTER TABLE `$table` ADD CONSTRAINT `$name` FOREIGN KEY (`$col`) REFERENCES `$ref`(`$refCol`) ON DELETE $onDel");
    echo "  -> $table.$col FK $ref\n";
}

$defaultCompanyId = (int) $db->query("SELECT id FROM companies WHERE is_default = 1 AND deleted_at IS NULL LIMIT 1")->fetchColumn();
if (!$defaultCompanyId) {
    $defaultCompanyId = (int) $db->query("SELECT id FROM companies WHERE deleted_at IS NULL ORDER BY id LIMIT 1")->fetchColumn();
}
if (!$defaultCompanyId) {
    fwrite(STDERR, "No company row to backfill against — create a company first.\n");
    exit(1);
}
echo "== Module company ownership + Indian identity evidence ==\n";
echo "   Backfill target: company #$defaultCompanyId\n";

/*
|------------------------------------------------------------------------------
| 1. Company ownership on the operational masters
|------------------------------------------------------------------------------
*/
echo "\n-- company_id --\n";
$scoped = [
    'employees'   => 'fk_employee_company',
    'projects'    => 'fk_project_company',
    'contractors' => 'fk_contractor_company',
    'assets'      => 'fk_asset_company',
];
foreach ($scoped as $table => $fkName) {
    addColumn($db, $table, 'company_id', 'INT UNSIGNED NULL', 'status');
    addIndex($db, $table, 'idx_' . rtrim($table, 's') . '_company', '`company_id`');
    addFk($db, $table, $fkName, 'company_id', 'companies');
    $s = $db->prepare("UPDATE `$table` SET company_id = ? WHERE company_id IS NULL");
    $s->execute([$defaultCompanyId]);
    if ($s->rowCount()) { echo "  ~ backfilled {$s->rowCount()} $table row(s)\n"; }
}

/*
|------------------------------------------------------------------------------
| 2. Asset storage location
|------------------------------------------------------------------------------
*/
echo "\n-- asset location --\n";
addColumn($db, 'assets', 'location', 'VARCHAR(255) NULL', 'asset_condition');

/*
|------------------------------------------------------------------------------
| 3. Aadhaar + PAN
|------------------------------------------------------------------------------
|
| Stored as plain strings rather than a numeric type: Aadhaar may be captured
| with spaces for readability and PAN is alphanumeric. Validation is in the
| form layer, which is where the client-facing message belongs.
|
|------------------------------------------------------------------------------
*/
echo "\n-- Indian identity evidence --\n";
addColumn($db, 'employees', 'aadhaar_number', 'VARCHAR(12) NULL', 'nationality');
addColumn($db, 'employees', 'pan_number', 'VARCHAR(10) NULL', 'aadhaar_number');

/*
|------------------------------------------------------------------------------
| 4. Controlled nationality list
|------------------------------------------------------------------------------
*/
echo "\n-- person.nationality lookup --\n";

$countries = [
    'Afghanistan','Albania','Algeria','Andorra','Angola','Antigua and Barbuda','Argentina','Armenia','Australia','Austria',
    'Azerbaijan','Bahamas','Bahrain','Bangladesh','Barbados','Belarus','Belgium','Belize','Benin','Bhutan',
    'Bolivia','Bosnia and Herzegovina','Botswana','Brazil','Brunei','Bulgaria','Burkina Faso','Burundi','Cabo Verde','Cambodia',
    'Cameroon','Canada','Central African Republic','Chad','Chile','China','Colombia','Comoros','Congo (Democratic Republic)','Congo (Republic)',
    'Costa Rica','Croatia','Cuba','Cyprus','Czechia','Denmark','Djibouti','Dominica','Dominican Republic','Ecuador',
    'Egypt','El Salvador','Equatorial Guinea','Eritrea','Estonia','Eswatini','Ethiopia','Fiji','Finland','France',
    'Gabon','Gambia','Georgia','Germany','Ghana','Greece','Grenada','Guatemala','Guinea','Guinea-Bissau',
    'Guyana','Haiti','Honduras','Hungary','Iceland','India','Indonesia','Iran','Iraq','Ireland',
    'Israel','Italy','Jamaica','Japan','Jordan','Kazakhstan','Kenya','Kiribati','Kosovo','Kuwait',
    'Kyrgyzstan','Laos','Latvia','Lebanon','Lesotho','Liberia','Libya','Liechtenstein','Lithuania','Luxembourg',
    'Madagascar','Malawi','Malaysia','Maldives','Mali','Malta','Marshall Islands','Mauritania','Mauritius','Mexico',
    'Micronesia','Moldova','Monaco','Mongolia','Montenegro','Morocco','Mozambique','Myanmar','Namibia','Nauru',
    'Nepal','Netherlands','New Zealand','Nicaragua','Niger','Nigeria','North Korea','North Macedonia','Norway','Oman',
    'Pakistan','Palau','Palestine','Panama','Papua New Guinea','Paraguay','Peru','Philippines','Poland','Portugal',
    'Qatar','Romania','Russia','Rwanda','Saint Kitts and Nevis','Saint Lucia','Saint Vincent and the Grenadines','Samoa','San Marino','Sao Tome and Principe',
    'Saudi Arabia','Senegal','Serbia','Seychelles','Sierra Leone','Singapore','Slovakia','Slovenia','Solomon Islands','Somalia',
    'South Africa','South Korea','South Sudan','Spain','Sri Lanka','Sudan','Suriname','Sweden','Switzerland','Syria',
    'Taiwan','Tajikistan','Tanzania','Thailand','Timor-Leste','Togo','Tonga','Trinidad and Tobago','Tunisia','Turkey',
    'Turkmenistan','Tuvalu','Uganda','Ukraine','United Arab Emirates','United Kingdom','United States of America','Uruguay','Uzbekistan','Vanuatu',
    'Vatican City','Venezuela','Vietnam','Yemen','Zambia','Zimbabwe',
];

// Nationality was typed by hand, so adjectival forms are the norm. Map the ones
// that plausibly occur in this install's region before anything else.
$adjectival = [
    'indian' => 'India', 'pakistani' => 'Pakistan', 'bangladeshi' => 'Bangladesh', 'sri lankan' => 'Sri Lanka',
    'nepali' => 'Nepal', 'filipino' => 'Philippines', 'pinoy' => 'Philippines', 'indonesian' => 'Indonesia',
    'malaysian' => 'Malaysia', 'emirati' => 'United Arab Emirates', 'uae' => 'United Arab Emirates',
    'saudi' => 'Saudi Arabia', 'kuwaiti' => 'Kuwait', 'qatari' => 'Qatar', 'omani' => 'Oman',
    'bahraini' => 'Bahrain', 'egyptian' => 'Egypt', 'jordanian' => 'Jordan', 'lebanese' => 'Lebanon',
    'syrian' => 'Syria', 'iraqi' => 'Iraq', 'iranian' => 'Iran', 'persian' => 'Iran',
    'turkish' => 'Turkey', 'british' => 'United Kingdom', 'english' => 'United Kingdom', 'scottish' => 'United Kingdom',
    'walsh' => 'United Kingdom', 'american' => 'United States of America', 'us' => 'United States of America',
    'usa' => 'United States of America', 'australian' => 'Australia', 'new zealand' => 'New Zealand',
    'canadian' => 'Canada', 'chinese' => 'China', 'japanese' => 'Japan', 'korean' => 'South Korea',
    'south korean' => 'South Korea', 'north korean' => 'North Korea', 'german' => 'Germany', 'french' => 'France',
    'italian' => 'Italy', 'spanish' => 'Spain', 'portuguese' => 'Portugal', 'dutch' => 'Netherlands',
    'belgian' => 'Belgium', 'swiss' => 'Switzerland', 'austrian' => 'Austria', 'swedish' => 'Sweden',
    'norwegian' => 'Norway', 'danish' => 'Denmark', 'finnish' => 'Finland', 'polish' => 'Poland',
    'russian' => 'Russia', 'ukrainian' => 'Ukraine', 'nigerian' => 'Nigeria', 'ghanaian' => 'Ghana',
    'kenyan' => 'Kenya', 'ethiopian' => 'Ethiopia', 'south african' => 'South Africa', 'zimbabwean' => 'Zimbabwe',
    'brazilian' => 'Brazil', 'mexican' => 'Mexico', 'argentine' => 'Argentina', 'colombian' => 'Colombia',
    'chilean' => 'Chile', 'peruvian' => 'Peru', 'venezuelan' => 'Venezuela', 'palestinian' => 'Palestine',
    'yemeni' => 'Yemen', 'sudanese' => 'Sudan', 'moroccan' => 'Morocco', 'tunisian' => 'Tunisia',
    'algerian' => 'Algeria', 'libyan' => 'Libya', 'thai' => 'Thailand', 'vietnamese' => 'Vietnam',
    'cambodian' => 'Cambodia', 'myanmar' => 'Myanmar', 'burmese' => 'Myanmar', 'singaporean' => 'Singapore',
    'hong kong' => 'China', 'taiwanese' => 'Taiwan', 'srilankan' => 'Sri Lanka',
];

$existingTypes = $db->prepare("SELECT COUNT(*) FROM lookup_types WHERE type_key = ?");
$existingTypes->execute(['person.nationality']);
if (!$existingTypes->fetchColumn()) {
    $db->prepare("INSERT INTO lookup_types (type_key, label, description, group_name, is_active) VALUES (?,?,?,?,1)")
       ->execute(['person.nationality', 'Nationality', 'Country of citizenship captured on people records', 'hr']);
    echo "  + lookup type person.nationality\n";
} else {
    echo "  = lookup type person.nationality exists\n";
}

$insVal = $db->prepare("INSERT INTO lookup_values (type_key, value_key, value_label, is_active, sort_order) VALUES (?,?,?,1,?)");
$added = 0;
foreach ($countries as $i => $country) {
    $chk = $db->prepare("SELECT COUNT(*) FROM lookup_values WHERE type_key=? AND value_key=?");
    $chk->execute(['person.nationality', $country]);
    if ($chk->fetchColumn()) { continue; }
    $insVal->execute(['person.nationality', $country, $country, ($i + 1) * 10]);
    $added++;
}
echo "  + $added nationality value(s) (list now has "
   . $db->query("SELECT COUNT(*) FROM lookup_values WHERE type_key='person.nationality'")->fetchColumn()
   . ")\n";

// Normalise hand-typed values onto the controlled list, in both tables.
$normalise = [
    'employees'   => 'employee',
    'contractors' => 'contractor',
];
foreach (array_keys($normalise) as $table) {
    $rows = $db->query("SELECT id, nationality FROM `$table` WHERE nationality IS NOT NULL AND nationality <> ''")->fetchAll();
    $upd = $db->prepare("UPDATE `$table` SET nationality = ? WHERE id = ?");
    $changed = 0;
    foreach ($rows as $r) {
        $raw = trim(preg_replace('/\s+/', ' ', (string) $r['nationality']));
        if ($raw === '') { continue; }
        $lower = mb_strtolower($raw);
        $target = $adjectival[$lower] ?? null;
        if ($target === null) {
            // Title-case a plain country name so "india" matches "India".
            foreach ($countries as $c) {
                if (mb_strtolower($c) === $lower) { $target = $c; break; }
            }
        }
        if ($target === null || $target === $raw) { continue; }
        $upd->execute([$target, $r['id']]);
        $changed++;
        echo "  ~ $table#{$r['id']}: \"$raw\" -> \"$target\"\n";
    }
    if (!$changed) { echo "  = $table.nationality already conforms\n"; }
}

echo "\n== Done ==\n";
foreach ($scoped as $table => $fkName) {
    $n = $db->query("SELECT COUNT(*) FROM `$table` WHERE company_id IS NOT NULL")->fetchColumn();
    echo "  $table: $n row(s) with an owning company\n";
}
echo "  assets.location, employees.aadhaar_number, employees.pan_number present\n";
