<?php

/**
 * AUD-2026-11-12 · Dilim C · statik kapsam haritası (yalnızca okur).
 *
 * Kapsam sürücüsü (Xdebug/PCOV) kurulu olmadığı için satır kapsamı ÖLÇÜLEMEDİ. Bu betik bir YAKLAŞIMDIR:
 *   1) Her rota için: testlerde o URI'ye (ve HTTP fiiline) istek atan bir satır var mı?
 *   2) Her Action / Job / Console komutu / Middleware / Policy için: sınıf adı testlerde geçiyor mu,
 *      geçmiyorsa onu çağıran üretim dosyaları hangileri (dolaylı kapsam ipucu)?
 * "0 eşleşme" = "testi yok" DEMEK DEĞİLDİR; elle bakılacak adayların listesidir.
 *
 * Kullanım: php tst-coverage-map.php   (kopya: _audit-snap/backend-tst, rota listesi: evidence/commands/FE-route-list.json)
 */

declare(strict_types=1);

$copy = 'D:/Projects/davetkart/_audit-snap/backend-tst';
$routesFile = __DIR__.'/../commands/FE-route-list.json';

function phpFiles(string $dir): array
{
    $out = [];
    $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, FilesystemIterator::SKIP_DOTS));
    foreach ($it as $f) {
        if ($f->isFile() && $f->getExtension() === 'php') {
            $out[] = str_replace('\\', '/', $f->getPathname());
        }
    }
    sort($out);

    return $out;
}

// --- test metinleri: değişken parçalarını tek bir yer tutucuya indir ---
$tests = [];
foreach (phpFiles("{$copy}/tests") as $f) {
    $src = (string) file_get_contents($f);
    $norm = preg_replace('/\{\$[^}]+\}/u', '§', $src);                       // "{$x->id}"
    $norm = preg_replace('/[\'"]\s*\.\s*[^.\'"]+?\s*\.\s*[\'"]/u', '§', $norm);  // '...'.$id.'...'
    $norm = preg_replace('/[\'"]\s*\.\s*\$[\w>\-\[\]\'()]+/u', '§"', $norm);     // '...'.$id  (sonda)
    $tests[basename($f)] = ['raw' => $src, 'norm' => $norm];
}

// --- 1) rotalar ---
$routes = json_decode((string) file_get_contents($routesFile), true);
$verbs = ['GET' => 'get', 'POST' => 'post', 'PUT' => 'put', 'PATCH' => 'patch', 'DELETE' => 'delete'];
echo '# 1) ROTALAR ('.count($routes)." rota) — fiil+URI eşleşmesi | yalnız URI eşleşmesi | rota adı | dosyalar\n";
$untested = [];
foreach ($routes as $r) {
    $uri = '/'.ltrim((string) $r['uri'], '/');
    if (! str_starts_with($uri, '/api')) {
        continue;
    }
    $method = explode('|', (string) $r['method'])[0];
    $re = preg_quote($uri, '~');
    $re = preg_replace('~\\\\\{[^}]+\\\\\}~', '(?:§|[^/\'"?]+)', $re);
    $uriRe = '~[\'"]'.$re.'(?:\?[^\'"]*)?[\'"§]~u';
    $verb = $verbs[$method] ?? strtolower($method);
    $callRe = '~(?:->'.$verb.'(?:Json)?\(\s*|json\(\s*[\'"]'.$method.'[\'"]\s*,\s*|call\(\s*[\'"]'.$method.'[\'"]\s*,\s*)[\'"]'.$re.'(?:\?[^\'"]*)?[\'"§]~ui';
    $withVerb = 0;
    $uriOnly = 0;
    $files = [];
    foreach ($tests as $name => $t) {
        $a = preg_match_all($callRe, $t['norm']);
        $b = preg_match_all($uriRe, $t['norm']);
        $withVerb += $a;
        $uriOnly += $b;
        if ($a + $b > 0) {
            $files[] = $name;
        }
    }
    $nameHits = 0;
    if (! empty($r['name'])) {
        foreach ($tests as $t) {
            $nameHits += substr_count($t['raw'], "'".$r['name']."'");
        }
    }
    printf("%-7s %-52s %4d | %4d | %2d | %s\n", $method, $uri, $withVerb, $uriOnly, $nameHits, implode(',', array_slice($files, 0, 4)).(count($files) > 4 ? ',…(+'.(count($files) - 4).')' : ''));
    if ($withVerb + $uriOnly + $nameHits === 0) {
        $untested[] = "{$method} {$uri}";
    }
}
echo "\n# Hiç eşleşmeyen rotalar (".count($untested)."):\n".($untested === [] ? "(yok)\n" : implode("\n", $untested)."\n");

// --- 2) sınıflar ---
$prod = [];
foreach (phpFiles("{$copy}/app") as $f) {
    $prod[$f] = (string) file_get_contents($f);
}
foreach (['routes/api.php', 'routes/console.php', 'bootstrap/app.php'] as $extra) {
    if (is_file("{$copy}/{$extra}")) {
        $prod["{$copy}/{$extra}"] = (string) file_get_contents("{$copy}/{$extra}");
    }
}
foreach (['Actions', 'Jobs', 'Console/Commands', 'Http/Middleware', 'Policies', 'Services', 'Support', 'Rules', 'Notifications', 'Mail', 'Listeners', 'Observers'] as $group) {
    $dir = "{$copy}/app/{$group}";
    if (! is_dir($dir)) {
        continue;
    }
    $files = phpFiles($dir);
    $named = 0;
    $missing = [];
    foreach ($files as $f) {
        $class = basename($f, '.php');
        $hits = 0;
        foreach ($tests as $t) {
            $hits += preg_match_all('~\b'.preg_quote($class, '~').'\b~', $t['raw']);
        }
        if ($hits > 0) {
            $named++;

            continue;
        }
        $callers = [];
        foreach ($prod as $pf => $src) {
            if ($pf !== $f && preg_match('~\b'.preg_quote($class, '~').'\b~', $src)) {
                $callers[] = str_replace("{$copy}/", '', $pf);
            }
        }
        $missing[] = sprintf('  %-70s ← %s', str_replace("{$copy}/", '', $f), $callers === [] ? '(çağıran yok!)' : implode(', ', array_slice($callers, 0, 3)).(count($callers) > 3 ? ', …' : ''));
    }
    printf("\n# 2) app/%s: %d dosya · testlerde adı geçen %d · geçmeyen %d\n", $group, count($files), $named, count($missing));
    echo $missing === [] ? '' : implode("\n", $missing)."\n";
}
