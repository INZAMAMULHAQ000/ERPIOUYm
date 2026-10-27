<?php
$dir = new RecursiveIteratorIterator(new RecursiveDirectoryIterator('.'));
$bad = 0;
$checked = 0;
foreach ($dir as $f) {
    if ($f->isFile() && substr($f->getFilename(), -4) === '.php') {
        $cmd = 'php -l ' . escapeshellarg($f->getPathname());
        $out = shell_exec($cmd);
        $checked++;
        if ($out === null || strpos($out, 'No syntax errors') === false) {
            echo "BROKEN: " . $f->getPathname() . "\n";
            echo ($out === null ? "null\n" : $out . "\n");
            $bad++;
        }
    }
}
echo "checked=$checked broken=$bad\n";
