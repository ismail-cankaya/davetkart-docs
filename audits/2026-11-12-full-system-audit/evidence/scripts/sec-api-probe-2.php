<?php

/**
 * AUD-2026-11-12 — canlı güvenlik sondası, 2. bölüm: e-posta değişikliği ve parola sıfırlama bağlantıları.
 * (İlk sondada bağlantılar bulunamadı: log düz metin olduğu hâlde quoted-printable çözülüyordu ve
 *  "expires=17…" gibi değerler bozuluyordu. Burada log olduğu gibi okunur.)
 * Yalnızca http://127.0.0.1:8000. Sır yazdırmaz (imza ve token değerleri çıktıya girmez).
 */

declare(strict_types=1);

use App\Models\User;
use GuzzleHttp\Client;
use Illuminate\Contracts\Console\Kernel;
use Illuminate\Support\Facades\Artisan;

$base = 'D:/Projects/davetkart/_audit-snap/backend-e2e';
require $base.'/vendor/autoload.php';
$app = require $base.'/bootstrap/app.php';
$app->make(Kernel::class)->bootstrap();
$http = new Client(['base_uri' => 'http://127.0.0.1:8000', 'http_errors' => false, 'timeout' => 60]);
$run = substr(bin2hex(random_bytes(4)), 0, 6);
$pw = 'Denetim-Parolasi-2026!';

function call(string $m, string $p, ?string $t = null, ?array $j = null): array
{
    global $http;
    $h = ['Accept' => 'application/json'] + ($t ? ['Authorization' => 'Bearer '.$t] : []);
    $r = $http->request($m, $p, ['headers' => $h] + ($j !== null ? ['json' => $j] : []));
    $raw = (string) $r->getBody();

    return ['s' => $r->getStatusCode(), 'j' => json_decode($raw, true)];
}
function code(array $r): string
{
    return $r['s'].' '.($r['j']['error']['code'] ?? '');
}
function expect(bool $ok, string $id, string $d, string $o): void
{
    echo sprintf("[%s] %s — %s — %s\n", $ok ? 'OK' : 'ACIK', $id, $d, $o);
}
function lastLink(string $path, string $mustContain): string
{
    global $base;
    $log = (string) file_get_contents($base.'/storage/logs/laravel.log');
    preg_match_all('~http://localhost:3000'.preg_quote($path, '~').'\?[^\s"<>\]\)]+~', $log, $m);
    $links = array_values(array_filter(array_map('html_entity_decode', $m[0]), static fn (string $l): bool => str_contains($l, $mustContain)));

    return $links === [] ? '' : (string) end($links);
}
function reg(string $tag): array
{
    global $run, $pw;
    $email = "{$tag}.{$run}@example.test";
    $r = call('POST', '/api/auth/register', null, ['firstName' => 'Selin', 'lastName' => 'Aydın', 'email' => $email, 'password' => $pw]);

    return ['email' => $email, 'token' => $r['j']['token'], 'id' => (int) $r['j']['user']['id']];
}

echo '# AUD-2026-11-12 canlı güvenlik sondası 2 · '.date('Y-m-d H:i:s')." · koşu {$run}\n";
echo "# İlk sondanın (SEC-api-probe.txt) iki satırı için değerlendirme düzeltmesi:\n";
echo "#  P60: ACIK değil. Laravel tek izinli origin tanımlıyken ACAO başlığını isteğin Origin'inden bağımsız, sabit olarak yollar;\n";
echo "#       tarayıcı ACAO ≠ Origin olduğu için yabancı origin'in yanıtı okumasına izin vermez. Sonda denetimi yanlış yazılmıştı.\n";
echo "#  P81: \"sipariş.user_id='satır yok'\" ifadesi yanıltıcı: satır VAR, user_id NULL (PHP ?? işleci NULL'da da yedeğe düşer).\n\n";

Artisan::call('cache:clear');
$U = reg('selin');
$V = reg('kerem');
$new = "selin.yeni.{$run}@example.test";

echo "## E-posta değişikliği (K144)\n";
$r = call('POST', '/api/auth/email-change', $U['token'], ['email' => $V['email'], 'currentPassword' => $pw]);
echo '[BILGI] Q01 — başkasına ait adrese değişiklik talebi (numaralandırma) — '.code($r)."\n";
$r = call('POST', '/api/auth/email-change', $U['token'], ['email' => $new, 'currentPassword' => $pw]);
$link = lastLink('/eposta-onay', rawurlencode($new));
parse_str((string) parse_url($link, PHP_URL_QUERY), $q);
echo '[BILGI] Q02 — talep ve posta — '.code($r).' · bağlantı bulundu='.var_export($link !== '', true).' · parametreler='.implode(',', array_keys($q))."\n";
if ($link !== '') {
    $bad = $q;
    $bad['email'] = "saldirgan.{$run}@example.test";
    $r = call('POST', '/api/public/email-change/confirm?'.http_build_query($bad));
    expect(! in_array($r['s'], [200, 204], true), 'Q03', 'imzalı bağlantıda e-postayı değiştirme', code($r));
    $bad = $q;
    $bad['user'] = (string) $V['id'];
    $r = call('POST', '/api/public/email-change/confirm?'.http_build_query($bad));
    expect(! in_array($r['s'], [200, 204], true) && User::find($V['id'])->email === $V['email'], 'Q04', 'imzalı bağlantıda kullanıcı kimliğini değiştirme', code($r));
    $bad = $q;
    $bad['expires'] = (string) ((int) $q['expires'] + 86400);
    $r = call('POST', '/api/public/email-change/confirm?'.http_build_query($bad));
    expect(! in_array($r['s'], [200, 204], true), 'Q05', 'imzalı bağlantıda süreyi uzatma', code($r));
    $r = call('POST', '/api/public/email-change/confirm?'.http_build_query($q));
    $u = User::find($U['id']);
    $me = call('GET', '/api/auth/me', $U['token']);
    expect(in_array($r['s'], [200, 204], true) && $u->email === $new && $me['s'] === 401, 'Q06', 'geçerli bağlantı: adres değişti, bütün oturumlar kapandı', code($r).' değişti='.var_export($u->email === $new, true).' eski token '.code($me).' email_verified_at dolu='.var_export($u->email_verified_at !== null, true));
    $r = call('POST', '/api/public/email-change/confirm?'.http_build_query($q));
    expect(! in_array($r['s'], [200, 204], true), 'Q07', 'aynı bağlantı ikinci kez (tek kullanımlık)', code($r));
    $log = (string) file_get_contents($base.'/storage/logs/laravel.log');
    echo '[BILGI] Q08 — eski adrese bilgilendirme postası — eski adrese giden posta logda='.var_export(substr_count($log, 'To: '.$U['email']) > 0, true)."\n";
}

echo "\n## Parola sıfırlama\n";
Artisan::call('cache:clear');
$r = call('POST', '/api/auth/forgot-password', null, ['email' => $V['email']]);
$link = lastLink('/sifre-sifirla', rawurlencode($V['email']));
parse_str((string) parse_url($link, PHP_URL_QUERY), $rp);
echo '[BILGI] Q09 — talep ve posta — '.code($r).' · bağlantı bulundu='.var_export($link !== '', true).' · parametreler='.implode(',', array_keys($rp)).' · token uzunluğu='.strlen((string) ($rp['token'] ?? ''))."\n";
if (isset($rp['token'])) {
    $r = call('POST', '/api/auth/reset-password', null, ['token' => $rp['token'], 'email' => $new, 'password' => 'Yeni-Parola-2026!']);
    expect($r['s'] !== 204, 'Q10', "bir kullanıcının token'ı başka kullanıcının e-postasıyla", code($r));
    $r = call('POST', '/api/auth/reset-password', null, ['token' => $rp['token'], 'email' => $V['email'], 'password' => 'kisa']);
    expect($r['s'] === 422, 'Q11', 'sıfırlamada kısa parola', code($r));
    $r = call('POST', '/api/auth/reset-password', null, ['token' => $rp['token'], 'email' => $V['email'], 'password' => 'Yeni-Parola-2026!']);
    $me = call('GET', '/api/auth/me', $V['token']);
    $login = call('POST', '/api/auth/login', null, ['email' => $V['email'], 'password' => 'Yeni-Parola-2026!']);
    expect($r['s'] === 204 && $me['s'] === 401 && $login['s'] === 200, 'Q12', 'parola sıfırlandı, eski oturumlar kapandı, yeni parola çalışıyor', code($r).' eski token '.code($me).' yeni giriş '.code($login));
    $r = call('POST', '/api/auth/reset-password', null, ['token' => $rp['token'], 'email' => $V['email'], 'password' => 'Ucuncu-Parola-2026!']);
    expect($r['s'] !== 204, 'Q13', "sıfırlama token'ı ikinci kez", code($r));
    $r1 = call('POST', '/api/auth/forgot-password', null, ['email' => $V['email']]);
    echo '[BILGI] Q14 — 60 sn içinde ikinci sıfırlama talebi (broker kısması, yanıt farkı var mı) — '.code($r1)."\n";
}
Artisan::call('cache:clear');
