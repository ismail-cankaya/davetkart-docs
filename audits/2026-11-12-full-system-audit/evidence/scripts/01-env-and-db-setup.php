<?php

/**
 * AUD-2026-11-12 — anlık görüntü kopyaları için .env + denetim veritabanları.
 *
 * - Gerçek .env'den YALNIZCA DB_HOST / DB_PORT / DB_USERNAME / DB_PASSWORD satırları alınır
 *   (yerel PostgreSQL'e bağlanmak için). Değerler ekrana, loga ya da rapora YAZILMAZ.
 * - Diğer her şey .env.example'dan gelir: AI_PROVIDER=null, MAIL_MAILER=log, PAYMENT_PROVIDER=fake,
 *   SENTRY boş, AWS boş. Yani kopyalar hiçbir dış servise (Gemini, SES, Shopier, AWS, Sentry) çıkamaz.
 * - Kod depolarına yazmaz. Yazdığı yerler: D:\Projects\davetkart\_audit-snap\backend*\{.env,phpunit.xml}
 *
 * Kullanım: php 01-env-and-db-setup.php
 */

declare(strict_types=1);

$root = 'D:/Projects/davetkart';
$realEnv = $root.'/davetkart-backend-php-laravel/.env';
$snap = $root.'/_audit-snap';

/** kopya => [uygulama DB, test DB, APP_URL, ek .env satırları] */
$copies = [
    'backend' => ['davetkart_aud_arc', 'davetkart_aud_arc_test', 'http://localhost:8300', []],
    'backend-sec' => ['davetkart_aud_sec', 'davetkart_aud_sec_test', 'http://localhost:8200', [
        'PAYMENT_METHODS' => 'card,gift_code', 'QUEUE_CONNECTION' => 'sync',
    ]],
    'backend-tst' => ['davetkart_aud_tst', 'davetkart_aud_tst_test', 'http://localhost:8400', []],
    'backend-e2e' => ['davetkart_aud_e2e', 'davetkart_aud_e2e_test', 'http://localhost:8000', [
        'PAYMENT_METHODS' => 'card,gift_code', 'QUEUE_CONNECTION' => 'sync',
    ]],
];

// --- 1. Gerçek .env'den DB bağlantı satırları (ham hâliyle, tırnaklar korunur) ---
$rawDb = [];
foreach (file($realEnv, FILE_IGNORE_NEW_LINES) ?: [] as $line) {
    if (preg_match('/^(DB_HOST|DB_PORT|DB_USERNAME|DB_PASSWORD)=(.*)$/', rtrim($line, "\r"), $m)) {
        $rawDb[$m[1]] = $m[2];
    }
}
foreach (['DB_HOST', 'DB_PORT', 'DB_USERNAME', 'DB_PASSWORD'] as $k) {
    if (! array_key_exists($k, $rawDb)) {
        fwrite(STDERR, "Gerçek .env'de $k yok.\n");
        exit(1);
    }
}
$unquote = static function (string $v): string {
    $v = trim($v);
    if (strlen($v) >= 2 && ($v[0] === '"' || $v[0] === "'") && $v[strlen($v) - 1] === $v[0]) {
        return substr($v, 1, -1);
    }

    return $v;
};

// --- 2. Veritabanları ---
$dsn = sprintf('pgsql:host=%s;port=%s;dbname=postgres', $unquote($rawDb['DB_HOST']), $unquote($rawDb['DB_PORT']));
$pdo = new PDO($dsn, $unquote($rawDb['DB_USERNAME']), $unquote($rawDb['DB_PASSWORD']), [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
echo 'PostgreSQL: '.$pdo->query('SHOW server_version')->fetchColumn()."\n";
foreach ($copies as [$appDb, $testDb]) {
    foreach ([$appDb, $testDb] as $db) {
        $exists = $pdo->query('SELECT 1 FROM pg_database WHERE datname = '.$pdo->quote($db))->fetchColumn();
        if ($exists) {
            echo "var: $db\n";
        } else {
            $pdo->exec('CREATE DATABASE "'.$db.'"');
            echo "oluşturuldu: $db\n";
        }
    }
}

// --- 3. Her kopyaya .env ve phpunit.xml ---
foreach ($copies as $dir => [$appDb, $testDb, $appUrl, $extra]) {
    $base = "$snap/$dir";
    if (! is_dir($base)) {
        echo "ATLANDI (klasör yok): $dir\n";

        continue;
    }
    $set = array_merge([
        'APP_URL' => $appUrl,
        'DB_HOST' => $rawDb['DB_HOST'],
        'DB_PORT' => $rawDb['DB_PORT'],
        'DB_USERNAME' => $rawDb['DB_USERNAME'],
        'DB_PASSWORD' => $rawDb['DB_PASSWORD'],
        'DB_DATABASE' => $appDb,
        'CORS_ALLOWED_ORIGINS' => 'http://localhost:3000',
        'LOG_LEVEL' => 'debug',
    ], $extra);
    $out = [];
    foreach (file("$base/.env.example", FILE_IGNORE_NEW_LINES) ?: [] as $line) {
        $line = rtrim($line, "\r");
        if (preg_match('/^([A-Z0-9_]+)=/', $line, $m) && array_key_exists($m[1], $set)) {
            $out[] = $m[1].'='.$set[$m[1]];
            unset($set[$m[1]]);
        } else {
            $out[] = $line;
        }
    }
    foreach ($set as $k => $v) {
        $out[] = "$k=$v";
    }
    file_put_contents("$base/.env", implode("\n", $out)."\n");

    $xml = file_get_contents("$base/phpunit.xml");
    $new = str_replace('<server name="DB_DATABASE" value="davetkart_test"/>', '<server name="DB_DATABASE" value="'.$testDb.'"/>', (string) $xml, $n);
    if ($n === 1) {
        file_put_contents("$base/phpunit.xml", $new);
    }
    echo "$dir: .env yazıldı (uygulama DB=$appDb), phpunit.xml test DB=$testDb (değişen satır: $n)\n";
}
