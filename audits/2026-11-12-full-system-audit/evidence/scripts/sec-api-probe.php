<?php

/**
 * AUD-2026-11-12 — canlı güvenlik sondası (yalnızca http://127.0.0.1:8000, kopya: _audit-snap/backend-e2e).
 *
 * Laravel'i kopyadan önyükler (DB okuma, imza için app.key, artisan), HTTP isteklerini yerel sunucuya atar.
 * Hiçbir dış adrese istek atmaz. Sır yazdırmaz. Çıktı satırı: [OK|ACIK|BILGI] kimlik — açıklama — gözlem
 *   OK    = güvenli/beklenen davranış gözlendi      ACIK = zafiyet/sapma kanıtlandı      BILGI = not
 *
 * Kullanım (PowerShell): php sec-api-probe.php > ..\commands\SEC-api-probe.txt
 */

declare(strict_types=1);

use App\Models\Invitation;
use App\Models\Media;
use App\Models\Order;
use App\Models\Rsvp;
use App\Models\User;
use App\Support\IpHasher;
use GuzzleHttp\Client;
use Illuminate\Contracts\Console\Kernel;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\DB;

$base = 'D:/Projects/davetkart/_audit-snap/backend-e2e';
require $base.'/vendor/autoload.php';
$app = require $base.'/bootstrap/app.php';
$app->make(Kernel::class)->bootstrap();

$http = new Client(['base_uri' => 'http://127.0.0.1:8000', 'http_errors' => false, 'timeout' => 60]);
$run = substr(bin2hex(random_bytes(4)), 0, 6);
$counts = ['OK' => 0, 'ACIK' => 0, 'BILGI' => 0];

function out(string $tag, string $id, string $desc, string $obs): void
{
    global $counts;
    $counts[$tag]++;
    echo sprintf("[%s] %s — %s — %s\n", $tag, $id, $desc, $obs);
}
function expect(bool $ok, string $id, string $desc, string $obs): void
{
    out($ok ? 'OK' : 'ACIK', $id, $desc, $obs);
}
/** @return array{s:int,j:mixed,h:array<string,list<string>>,raw:string} */
function call(string $method, string $path, ?string $token = null, ?array $json = null, array $opt = []): array
{
    global $http;
    $headers = ['Accept' => 'application/json'] + ($opt['headers'] ?? []);
    if ($token !== null) {
        $headers['Authorization'] = 'Bearer '.$token;
    }
    $o = ['headers' => $headers];
    if ($json !== null) {
        $o['json'] = $json;
    }
    foreach (['body', 'multipart', 'query'] as $k) {
        if (isset($opt[$k])) {
            $o[$k] = $opt[$k];
        }
    }
    $r = $http->request($method, $path, $o);
    $raw = (string) $r->getBody();

    return ['s' => $r->getStatusCode(), 'j' => json_decode($raw, true), 'h' => $r->getHeaders(), 'raw' => $raw];
}
function code(array $r): string
{
    return $r['s'].' '.($r['j']['error']['code'] ?? '');
}
function clearLimits(): void
{
    Artisan::call('cache:clear');
}
function register(string $first, string $last, string $tag): array
{
    global $run;
    $email = "{$tag}.{$run}@example.test";
    $r = call('POST', '/api/auth/register', null, ['firstName' => $first, 'lastName' => $last, 'email' => $email, 'password' => 'Denetim-Parolasi-2026!']);
    if ($r['s'] !== 201) {
        throw new RuntimeException("register {$tag}: ".code($r).' '.substr($r['raw'], 0, 200));
    }

    return ['email' => $email, 'token' => $r['j']['token'], 'id' => (int) $r['j']['user']['id']];
}
function newInvitation(string $token, array $extra = []): array
{
    $r = call('POST', '/api/invitations', $token, ['invitation' => $extra + [
        'categoryId' => 'dugun', 'imageTheme' => 'dugun-klasik', 'palette' => 'altin',
        'title' => 'Zeynep & Emre', 'names' => 'Zeynep Yılmaz & Emre Kaya', 'venue' => 'Çırağan Sarayı, Beşiktaş / İstanbul',
        'date' => '2027-06-12T19:00', 'showRSVP' => true, 'showTimer' => true,
    ]]);
    if ($r['s'] !== 201) {
        throw new RuntimeException('create invitation: '.code($r).' '.substr($r['raw'], 0, 300));
    }

    return $r['j']['data'];
}
function webhook(string $providerRef, string $status, ?string $sig = null): array
{
    $payload = json_encode(['providerRef' => $providerRef, 'status' => $status]);
    $sig ??= hash_hmac('sha256', (string) $payload, (string) config('app.key'));

    return call('POST', '/api/public/payments/webhook', null, null, ['body' => $payload, 'headers' => ['Content-Type' => 'application/json', 'X-Signature' => $sig]]);
}
function payOrder(string $orderId): array
{
    $ref = Order::query()->findOrFail($orderId)->provider_ref;

    return webhook((string) $ref, 'paid');
}
function mailLinks(string $needle): array
{
    global $base;
    $log = $base.'/storage/logs/laravel.log';
    $size = filesize($log);
    $fh = fopen($log, 'rb');
    fseek($fh, max(0, $size - 400000));
    $tail = quoted_printable_decode((string) stream_get_contents($fh));
    fclose($fh);
    preg_match_all('~https?://localhost:3000[^\s"<>\)]*'.$needle.'[^\s"<>\)]*~', $tail, $m);

    return array_values(array_unique(array_map('html_entity_decode', $m[0])));
}
function section(string $t): void
{
    echo "\n## {$t}\n";
    clearLimits();
}

echo "# AUD-2026-11-12 canlı güvenlik sondası · ".date('Y-m-d H:i:s')." · hedef http://127.0.0.1:8000 · kopya backend-e2e (d810410) · koşu {$run}\n";

try {
    // ------------------------------------------------------------------ hazırlık
    section('Hazırlık');
    $A = register('Zeynep', 'Yılmaz', 'zeynep');
    $B = register('Mehmet', 'Öztürk', 'mehmet');
    $invA = newInvitation($A['token']);
    $idA = $invA['id'];
    out('BILGI', 'S00', 'iki kullanıcı ve A\'nın davetiyesi', "A#{$A['id']} B#{$B['id']} davetiye {$idA} durum {$invA['status']}");

    // ------------------------------------------------------------------ kimliksiz erişim
    section('Kimliksiz erişim (API2)');
    foreach ([['GET', '/api/invitations'], ['GET', "/api/invitations/{$idA}"], ['GET', '/api/orders'], ['GET', '/api/account/entitlements'], ['GET', '/api/auth/me'], ['GET', '/api/auth/sessions'], ['POST', '/api/assistant/chat'], ['GET', '/api/pricing']] as [$m, $p]) {
        $r = call($m, $p);
        expect($r['s'] === 401, 'P01', "kimliksiz {$m} {$p}", code($r));
    }

    // ------------------------------------------------------------------ BOLA
    section('Nesne düzeyinde yetki — B, A\'nın nesnelerine (API1)');
    $r = call('GET', "/api/invitations/{$idA}", $B['token']);
    expect($r['s'] === 404, 'P02', 'B → GET A davetiyesi', code($r));
    $r = call('PUT', "/api/invitations/{$idA}", $B['token'], ['invitation' => ['title' => 'ELE GECIRILDI']]);
    expect($r['s'] === 404 && Invitation::find($idA)->title !== 'ELE GECIRILDI', 'P03', 'B → PUT A davetiyesi', code($r).' başlık='.Invitation::find($idA)->title);
    $r = call('POST', "/api/invitations/{$idA}/publish", $B['token']);
    expect($r['s'] === 404, 'P04', 'B → publish A davetiyesi', code($r));
    $r = call('POST', "/api/invitations/{$idA}/checkout", $B['token'], ['tier' => 'standart']);
    expect($r['s'] === 404, 'P05', 'B → checkout A davetiyesi', code($r));
    $r = call('GET', "/api/invitations/{$idA}/rsvps", $B['token']);
    expect($r['s'] === 404, 'P06', 'B → A\'nın LCV listesi', code($r));
    $r = call('DELETE', "/api/invitations/{$idA}", $B['token']);
    expect($r['s'] === 404 && Invitation::find($idA) !== null, 'P07', 'B → DELETE A davetiyesi', code($r));
    $r = call('GET', '/api/invitations', $B['token']);
    expect($r['s'] === 200 && count($r['j']['data']) === 0, 'P08', 'B\'nin listesi A\'nın davetiyesini içermiyor', $r['s'].' adet='.count($r['j']['data'] ?? []));

    // ------------------------------------------------------------------ toplu atama
    section('Toplu atama (API3)');
    $m = newInvitation($A['token'], ['status' => 'published', 'userId' => $B['id'], 'user_id' => $B['id'], 'publishedAt' => '2026-01-01T00:00:00Z', 'published_at' => '2026-01-01', 'id' => '01ARZ3NDEKTSV4RRFFQ69G5FAV', 'galleryMediaIds' => ['x']]);
    $row = Invitation::find($m['id']);
    expect($row->status->value === 'saved' && $row->user_id === $A['id'] && $row->published_at === null, 'P09', 'oluştururken status/userId/publishedAt enjeksiyonu', "status={$row->status->value} user_id={$row->user_id} published_at=".var_export($row->published_at, true));
    $r = call('PUT', "/api/invitations/{$m['id']}", $A['token'], ['invitation' => ['status' => 'published', 'user_id' => $B['id']], 'status' => 'published']);
    $row->refresh();
    expect($row->status->value === 'saved' && $row->user_id === $A['id'], 'P10', 'PUT ile status/user_id enjeksiyonu', code($r)." status={$row->status->value} user_id={$row->user_id}");

    // ------------------------------------------------------------------ paywall + fiyat
    section('Paywall ve fiyat (M6, K-1)');
    $r = call('POST', "/api/invitations/{$idA}/publish", $A['token']);
    expect($r['s'] === 402, 'P11', 'ödeme yokken yayın', code($r));
    $r = call('POST', "/api/invitations/{$idA}/checkout", $A['token'], ['tier' => 'standart', 'price' => 1, 'amount' => 1, 'amountMinor' => 1, 'totalMinor' => 1, 'priceMinor' => 1, 'currency' => 'USD', 'status' => 'paid']);
    $o1 = $r['j']['data'] ?? [];
    $row1 = Order::find($o1['orderId'] ?? '');
    expect($r['s'] === 201 && $row1 && $row1->status->value === 'pending' && $row1->amount_minor === 9960 && $row1->currency === 'TRY', 'P12', 'checkout gövdesinde fiyat/para birimi/durum enjeksiyonu', code($r).' amount_minor='.($row1->amount_minor ?? '?').' currency='.($row1->currency ?? '?').' status='.($row1->status->value ?? '?').' promotion='.json_encode($o1['promotion'] ?? null));
    $r = call('POST', '/api/payments/checkout', $A['token'], ['tier' => 'standart']);
    $o2 = $r['j']['data'] ?? [];
    $row2 = Order::find($o2['orderId'] ?? '');
    out('BILGI', 'P13a', 'ilk ödeme tamamlanmadan ikinci (paket) sipariş', code($r).' amount_minor='.($row2->amount_minor ?? '?').' promotion='.json_encode($o2['promotion'] ?? null));
    $r1 = payOrder($o1['orderId']);
    $r2 = payOrder($o2['orderId']);
    $row1->refresh();
    $row2->refresh();
    $both = $row1->status->value === 'paid' && $row2->status->value === 'paid' && $row1->promotion?->value === 'first_publish' && $row2->promotion?->value === 'first_publish';
    expect(! $both, 'P13', '"ilk yayın" indirimi tek siparişle sınırlı', "sipariş1 {$row1->status->value} {$row1->amount_minor} kuruş ({$row1->promotion?->value}) · sipariş2 {$row2->status->value} {$row2->amount_minor} kuruş ({$row2->promotion?->value}) · webhook {$r1['s']}/{$r2['s']}");
    $r = call('POST', '/api/payments/checkout', $A['token'], ['tier' => 'standart']);
    out('BILGI', 'P13b', 'ödeme sonrası üçüncü sipariş fiyatı', code($r).' totalMinor='.($r['j']['data']['totalMinor'] ?? '?').' promotion='.json_encode($r['j']['data']['promotion'] ?? null));
    $o3 = $r['j']['data']['orderId'] ?? null;

    $r = call('POST', "/api/invitations/{$idA}/publish", $A['token']);
    expect($r['s'] === 200 && ($r['j']['data']['status'] ?? '') === 'published', 'P14', 'Standart ödendi → yayın', code($r).' status='.($r['j']['data']['status'] ?? '?'));
    foreach ([['showGallery', true, 'Elit modülü'], ['showGift', true, 'Elit modülü'], ['showEnvelope', true, 'Gold modülü'], ['showTimeline', true, 'Gold modülü'], ['imageTheme', 'dugun-saray-kapisi', 'Gold şablonu (Faz 16)'], ['imageTheme', 'dugun-kelebek', 'Gold şablonu (Faz 17)']] as [$k, $v, $what]) {
        $r = call('PUT', "/api/invitations/{$idA}", $A['token'], ['invitation' => [$k => $v]]);
        expect($r['s'] === 402, 'P15', "yayındaki Standart davetiyede {$what} açma ({$k})", code($r));
    }
    clearLimits();
    $pub = call('GET', "/api/public/invitations/{$idA}");
    $d = $pub['j']['data']['invitation'] ?? [];
    expect($pub['s'] === 200 && ($d['showGallery'] ?? null) === false && ($d['showGift'] ?? null) === false && ($d['imageTheme'] ?? '') === 'dugun-klasik' && ! array_key_exists('iban', $d), 'P16', 'misafir yanıtında üst plan modülü yok, IBAN anahtarı yok', $pub['s'].' showGallery='.var_export($d['showGallery'] ?? null, true).' showGift='.var_export($d['showGift'] ?? null, true).' imageTheme='.($d['imageTheme'] ?? '?').' iban_anahtari='.var_export(array_key_exists('iban', $d), true).' showBranding='.var_export($d['showBranding'] ?? null, true));
    $r = call('PUT', "/api/invitations/{$idA}", $A['token'], ['invitation' => ['venue' => 'Sait Halim Paşa Yalısı, Sarıyer / İstanbul']]);
    expect($r['s'] === 200, 'P17', 'yayındaki davetiyede olağan alan düzenleme', code($r));
    $r = call('POST', "/api/invitations/{$idA}/publish", $A['token']);
    expect($r['s'] === 409, 'P18', 'ikinci yayın isteği', code($r));

    // ------------------------------------------------------------------ webhook
    section('Webhook (W1–W3, M8, K69, K89)');
    $ref1 = (string) $row1->provider_ref;
    $r = webhook($ref1, 'paid', str_repeat('0', 64));
    expect(in_array($r['s'], [404, 401, 403], true), 'P19', 'geçersiz imzalı bildirim', code($r));
    $r = webhook('fake_BILINMEYEN', 'paid');
    expect($r['s'] === 204, 'P20', 'imzalı ama bilinmeyen provider_ref', (string) $r['s']);
    $paidAt = $row1->paid_at;
    $r = webhook($ref1, 'paid');
    $row1->refresh();
    expect($r['s'] === 204 && $row1->status->value === 'paid' && $row1->paid_at == $paidAt, 'P21', 'paid bildirimi tekrar oynatma', $r['s'].' status='.$row1->status->value.' paid_at değişti mi='.var_export($row1->paid_at != $paidAt, true));
    $r = webhook($ref1, 'failed');
    $row1->refresh();
    expect($row1->status->value === 'paid', 'P22', 'paid siparişe failed bildirimi', $r['s'].' status='.$row1->status->value);
    if ($o3) {
        DB::table('orders')->where('id', $o3)->update(['expires_at' => now()->subHour()]);
        Artisan::call('orders:expire');
        $row3 = Order::find($o3);
        $before = $row3->status->value;
        $r = payOrder($o3);
        $row3->refresh();
        expect($before === 'expired' && $row3->status->value === 'paid', 'P23', 'süresi dolan siparişe geç gelen paid (K-4/K89)', "önce={$before} sonra={$row3->status->value} webhook={$r['s']}");
    }

    // ------------------------------------------------------------------ LCV
    section('LCV: kota, düzenleme kodu, IP (K50, K101, K14)');
    $rs = call('POST', "/api/public/invitations/{$idA}/rsvps", null, ['guestName' => 'Ayşe Demir', 'guestCount' => 2, 'status' => 'attending', 'message' => 'Mutluluklar dileriz!'], ['headers' => ['X-Forwarded-For' => '203.0.113.77']]);
    $rsvpId = $rs['j']['data']['id'] ?? '';
    $edit = $rs['j']['data']['editCode'] ?? '';
    $rv = Rsvp::find($rsvpId);
    expect($rs['s'] === 201 && $rv && $rv->ip_hash === IpHasher::hash('127.0.0.1') && ! str_contains(json_encode($rv->getAttributes()), '203.0.113'), 'P24', 'LCV kaydı: IP hash\'li, X-Forwarded-For (güvenilmeyen vekil) yok sayıldı', $rs['s'].' ip_hash=='.($rv && $rv->ip_hash === IpHasher::hash('127.0.0.1') ? 'hash(127.0.0.1)' : 'FARKLI').' yanıtta ip alanı='.var_export(isset($rs['j']['data']['ipHash']) || isset($rs['j']['data']['ip']), true));
    $r = call('PUT', "/api/public/invitations/{$idA}/rsvps/{$rsvpId}", null, ['guestName' => 'Saldırgan', 'guestCount' => 1, 'status' => 'declined', 'editCode' => str_repeat('x', 40)]);
    expect($r['s'] === 404 || $r['s'] === 422, 'P25', 'yanlış düzenleme koduyla LCV güncelleme', code($r).' ad='.Rsvp::find($rsvpId)->guest_name);
    $r = call('PUT', "/api/public/invitations/{$idA}/rsvps/{$rsvpId}", null, ['guestName' => 'Ayşe Demir', 'guestCount' => 3, 'status' => 'attending', 'editCode' => $edit]);
    expect($r['s'] === 200 && Rsvp::where('invitation_id', $idA)->count() === 1, 'P26', 'doğru kodla güncelleme yeni satır açmıyor', code($r).' satır='.Rsvp::where('invitation_id', $idA)->count());
    $r = call('DELETE', "/api/rsvps/{$rsvpId}", $B['token']);
    expect($r['s'] === 404 && Rsvp::find($rsvpId) !== null, 'P27', 'B → A\'nın LCV kaydını silme', code($r));
    $last = null;
    for ($i = 0; $i < 10; $i++) {
        $last = call('POST', "/api/public/invitations/{$idA}/rsvps", null, ['guestName' => "Misafir Ailesi {$i}", 'guestCount' => 10, 'status' => 'attending']);
    }
    $sum = (int) Rsvp::where('invitation_id', $idA)->whereIn('status', ['attending', 'pending'])->sum('guest_count');
    expect($sum <= 100 && $last['s'] === 403, 'P28', 'Standart LCV kotası 100 kişi (SUM guest_count)', 'toplam kişi='.$sum.' son istek='.code($last));
    $r = call('POST', "/api/public/invitations/{$m['id']}/rsvps", null, ['guestName' => 'Ayşe Demir', 'guestCount' => 1, 'status' => 'attending']);
    expect($r['s'] === 404, 'P29', 'yayınlanmamış davetiyeye LCV', code($r));
    $r = call('GET', "/api/public/invitations/{$m['id']}");
    expect($r['s'] === 404, 'P30', 'yayınlanmamış davetiyenin misafir ucu', code($r));

    // ------------------------------------------------------------------ bozuk girdi
    section('Bozuk girdi (K91, K92, K-8)');
    $r = call('POST', "/api/public/invitations/{$idA}/rsvps", null, null, ['body' => '{"guestName":"Ali","guestCount":', 'headers' => ['Content-Type' => 'application/json']]);
    expect($r['s'] === 400, 'P31', 'yarım JSON', code($r));
    $r = call('POST', "/api/public/invitations/{$idA}/rsvps", null, ['guestName' => "Ali\0Veli", 'guestCount' => 1, 'status' => 'declined']);
    expect($r['s'] === 400, 'P32', 'NUL baytı', code($r));
    $r = call('POST', "/api/public/invitations/{$idA}/rsvps", null, ['guestName' => 'Ali Veli', 'guestCount' => true, 'status' => 'declined']);
    expect($r['s'] === 422, 'P33', 'guestCount: true', code($r));
    $r = call('POST', "/api/public/invitations/{$idA}/rsvps", null, ['guestName' => 'Ali Veli', 'guestCount' => '3', 'status' => 'declined']);
    expect($r['s'] === 422, 'P34', 'guestCount: "3"', code($r));
    foreach (['javascript:alert(1)', 'smb://sunucu/paylasim', 'data:text/html,<script>alert(1)</script>', 'ms-settings:privacy'] as $u) {
        $r = call('PUT', "/api/invitations/{$m['id']}", $A['token'], ['invitation' => ['mapUrl' => $u]]);
        expect($r['s'] === 422, 'P35', "mapUrl şeması {$u}", code($r));
    }
    $r = call('PUT', "/api/invitations/{$m['id']}", $A['token'], ['invitation' => ['title' => '<img src=x onerror=alert(1)>', 'iban' => 'TR000000000000000000000000']]);
    out($r['s'] === 422 ? 'OK' : 'BILGI', 'P36', 'başlıkta HTML + geçersiz IBAN', code($r).' alanlar='.json_encode(array_keys($r['j']['error']['fields'] ?? [])));

    // ------------------------------------------------------------------ hediye kodu
    section('Hediye kodu (K107–K113)');
    Artisan::call('gift-codes:create', ['code' => "AUDFREE{$run}", '--benefit' => 'free', '--tier' => 'standart', '--max-uses' => '2']);
    Artisan::call('gift-codes:create', ['code' => "AUDPCT{$run}", '--benefit' => 'percent', '--percent' => '100', '--max-uses' => '5']);
    $C = register('Elif', 'Şahin', 'elif');
    $invC = newInvitation($C['token']);
    $r = call('POST', '/api/gift-codes/preview', $C['token'], ['code' => "aud-free-{$run}", 'tier' => 'standart']);
    out('BILGI', 'P37', 'kod önizleme (küçük harf + tire normalizasyonu)', code($r).' '.substr(json_encode($r['j']['data'] ?? $r['j']), 0, 160));
    $r = call('POST', "/api/invitations/{$invC['id']}/checkout", $C['token'], ['tier' => 'gold', 'giftCode' => "AUDFREE{$run}"]);
    expect($r['s'] !== 201, 'P38', 'Standart "free" kodu Gold\'da', code($r));
    $r = call('POST', "/api/invitations/{$invC['id']}/checkout", $C['token'], ['tier' => 'standart', 'giftCode' => "AUDFREE{$run}", 'discountMinor' => 999999]);
    $g = Order::find($r['j']['data']['orderId'] ?? '');
    expect($r['s'] === 201 && $g && $g->status->value === 'paid' && $g->amount_minor === 0 && $g->provider === 'gift', 'P39', 'free kodla hediye siparişi', code($r).' status='.($g->status->value ?? '?').' amount='.($g->amount_minor ?? '?').' provider='.($g->provider ?? '?'));
    $r = call('POST', '/api/payments/checkout', $C['token'], ['tier' => 'standart', 'giftCode' => "AUDFREE{$run}"]);
    expect($r['s'] !== 201 && ($r['j']['error']['code'] ?? '') === 'GIFT_CODE_ALREADY_USED', 'P40', 'aynı kullanıcı aynı kodu ikinci kez', code($r));
    $r = call('POST', '/api/payments/checkout', $B['token'], ['tier' => 'standart', 'giftCode' => "AUDFREE{$run}"]);
    $r2 = call('POST', '/api/payments/checkout', $A['token'], ['tier' => 'standart', 'giftCode' => "AUDFREE{$run}"]);
    expect($r['s'] === 201 && $r2['s'] !== 201, 'P41', 'max-uses=2: ikinci kişi alır, üçüncü alamaz', 'B '.code($r).' · A '.code($r2));
    $r = call('POST', '/api/payments/checkout', $A['token'], ['tier' => 'elit', 'giftCode' => "AUDPCT{$run}"]);
    $p = Order::find($r['j']['data']['orderId'] ?? '');
    out('BILGI', 'P42', '%100 indirim kodu (plan kısıtsız) Elit\'te', code($r).' status='.($p->status->value ?? '?').' amount='.($p->amount_minor ?? '?').' provider='.($p->provider ?? '?'));
    clearLimits();
    $hit = null;
    for ($i = 1; $i <= 14; $i++) {
        $r = call('POST', '/api/gift-codes/preview', $C['token'], ['code' => 'YANLIS'.$i, 'tier' => 'standart']);
        if ($r['s'] === 429) {
            $hit = $i;
            break;
        }
    }
    expect($hit !== null && $hit <= 11, 'P43', 'kod tahmini hız sınırı (10/dk)', 'ilk 429 istek no='.var_export($hit, true).' Retry-After='.($r['h']['Retry-After'][0] ?? 'yok'));

    // ------------------------------------------------------------------ iade
    section('İade / hak iptali (Faz 14)');
    $D = register('Can', 'Arslan', 'can');
    $invD = newInvitation($D['token']);
    $r = call('POST', "/api/invitations/{$invD['id']}/checkout", $D['token'], ['tier' => 'standart']);
    $od = $r['j']['data']['orderId'];
    payOrder($od);
    $r = call('POST', "/api/orders/{$od}/refund-request", $D['token'], ['reason' => 'Vazgeçtim']);
    expect($r['s'] !== 201, 'P44', 'davetiyeye bağlı (kullanımda) sipariş için iade talebi', code($r).' '.json_encode($r['j']['error']['params'] ?? null));
    $r = call('POST', "/api/orders/{$od}/refund-request", $B['token'], ['reason' => 'Benim değil']);
    expect($r['s'] === 404, 'P45', 'B → D\'nin siparişi için iade talebi', code($r));
    $r = call('GET', "/api/orders/{$od}", $B['token']);
    expect($r['s'] === 404, 'P46', 'B → D\'nin siparişini okuma', code($r));
    $r = call('POST', "/api/invitations/{$invD['id']}/publish", $D['token']);
    $pubD = call('GET', "/api/public/invitations/{$invD['id']}");
    $r2 = call('POST', "/api/public/invitations/{$invD['id']}/rsvps", null, ['guestName' => 'Fatma Çelik', 'guestCount' => 4, 'status' => 'attending']);
    $del = call('DELETE', "/api/invitations/{$invD['id']}", $D['token']);
    $rr = call('POST', "/api/orders/{$od}/refund-request", $D['token'], ['reason' => 'Etkinlik bitti']);
    $ordD = Order::find($od);
    expect($rr['s'] !== 201, 'P47', 'yayınla → misafir topla → 3 gün içinde sil → aynı hak için iade talebi reddedilmeli', "yayın {$r['s']} · misafir ucu {$pubD['s']} · LCV {$r2['s']} · silme {$del['s']} · iade talebi ".code($rr).' · sipariş invitation_id='.var_export($ordD->invitation_id, true).' consumed_at='.var_export($ordD->consumed_at, true));
    if ($rr['s'] === 201) {
        $inv2 = newInvitation($D['token']);
        $r = call('POST', "/api/invitations/{$inv2['id']}/publish", $D['token']);
        expect($r['s'] === 402, 'P48', 'iade talebi açıkken hak donuk (yeni yayın açmıyor)', code($r));
        Artisan::call('refunds:list');
        $list = Artisan::output();
        out('BILGI', 'P49', 'refunds:list yöneticiye hakkın daha önce yayınlandığını gösteriyor mu', 'çıktıda "yayın"/"publish"/"kullan" geçiyor mu='.var_export((bool) preg_match('/yay[ıi]n|publish|kullan/iu', $list), true).' · sütunlar: '.trim(preg_replace('/\s+/', ' ', (string) (preg_split('/\R/', trim($list))[1] ?? ''))));
    }

    // ------------------------------------------------------------------ yükleme
    section('Dosya yükleme (F1–F5)');
    $up = static fn (string $path, ?string $token, string $kind, string $bytes, string $name): array => call('POST', $path, $token, null, ['multipart' => [['name' => 'kind', 'contents' => $kind], ['name' => 'file', 'contents' => $bytes, 'filename' => $name]]]);
    $ownerPath = "/api/invitations/{$idA}/media";
    $guestPath = "/api/public/invitations/{$idA}/media";
    $r = $up($ownerPath, $A['token'], 'gallery', "<?php echo 'AUDIT'; ?>", 'resim.jpg');
    expect($r['s'] === 422, 'P50', 'PHP metni .jpg adıyla', code($r));
    $r = $up($guestPath, null, 'rsvp_photo', '<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"><script>alert(1)</script></svg>', 'resim.svg');
    expect($r['s'] === 422, 'P51', 'SVG (misafir)', code($r));
    $r = $up($guestPath, null, 'rsvp_photo', "GIF89a<script>alert(1)</script>", 'resim.png');
    expect($r['s'] === 422, 'P52', 'GIF başlıklı HTML .png adıyla', code($r));
    $r = $up($guestPath, null, 'gallery', 'x', 'resim.jpg');
    expect($r['s'] === 422, 'P53', 'misafir ucundan galeri türü', code($r));
    $im = imagecreatetruecolor(320, 240);
    imagefilledrectangle($im, 0, 0, 320, 240, imagecolorallocate($im, 180, 40, 90));
    ob_start();
    imagejpeg($im, null, 90);
    $jpeg = (string) ob_get_clean();
    $exif = "Exif\0\0II\x2A\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00AUDIT-GPS-MARKER-41.0082N-28.9784E";
    $poly = substr($jpeg, 0, 2)."\xFF\xE1".pack('n', strlen($exif) + 2).$exif.substr($jpeg, 2)."<?php echo 'AUDIT-POLYGLOT'; ?>";
    $r = $up($guestPath, null, 'rsvp_photo', $poly, '../../evil.php.jpg');
    $mid = $r['j']['data']['id'] ?? '';
    $mrow = Media::find($mid);
    $stored = $mrow ? @file_get_contents($base.'/storage/app/public/'.$mrow->path) : false;
    $files = $mrow ? glob($base.'/storage/app/public/'.dirname($mrow->path).'/*') : [];
    $leak = 0;
    foreach ($files ?: [] as $f) {
        $c = (string) @file_get_contents($f);
        if (str_contains($c, 'AUDIT-GPS-MARKER') || str_contains($c, 'AUDIT-POLYGLOT')) {
            $leak++;
        }
    }
    expect($r['s'] === 201 && $mrow && ! str_contains($mrow->path, '..') && ! str_contains($mrow->path, 'evil') && preg_match('/\.(jpg|jpeg|webp)$/', $mrow->path) === 1, 'P54', 'EXIF + PHP kuyruğu taşıyan JPEG: sunucu adı üretiyor, uzantı güvenli', code($r).' path='.($mrow->path ?? '?').' mime='.($mrow->mime_type ?? '?'));
    expect($stored !== false && ! str_contains($stored, 'AUDIT-GPS-MARKER') && ! str_contains($stored, 'AUDIT-POLYGLOT'), 'P55', 'saklanan dosyada EXIF ve PHP kuyruğu kalmadı (kuyruk sync)', 'dosya okundu='.var_export($stored !== false, true).' EXIF izi='.var_export($stored !== false && str_contains($stored, 'AUDIT-GPS-MARKER'), true).' PHP kuyruğu='.var_export($stored !== false && str_contains($stored, 'AUDIT-POLYGLOT'), true).' · aynı klasörde iz taşıyan dosya='.$leak);
    $url = $r['j']['data']['url'] ?? '';
    out('BILGI', 'P56', 'medya URL\'si ve disk', 'url='.preg_replace('~^https?://[^/]+~', '', (string) $url).' disk='.($mrow->disk ?? '?'));

    // ------------------------------------------------------------------ başlıklar, CORS
    section('Güvenlik başlıkları ve CORS (K85, K86)');
    $r = call('GET', '/api/ping');
    $h = array_change_key_case(array_map(static fn ($v) => implode(', ', $v), $r['h']));
    foreach (['x-content-type-options', 'x-frame-options', 'referrer-policy', 'content-security-policy'] as $k) {
        expect(isset($h[$k]), 'P57', "başlık {$k}", $h[$k] ?? 'YOK');
    }
    out(isset($h['strict-transport-security']) ? 'BILGI' : 'OK', 'P58', 'HSTS düz HTTP\'de gönderilmiyor', $h['strict-transport-security'] ?? 'yok');
    out(isset($h['x-powered-by']) ? 'ACIK' : 'OK', 'P59', 'X-Powered-By sızıntısı (artisan serve; üretimde php.ini expose_php)', $h['x-powered-by'] ?? 'yok');
    $r = call('OPTIONS', '/api/invitations', null, null, ['headers' => ['Origin' => 'https://kotu.example', 'Access-Control-Request-Method' => 'GET', 'Access-Control-Request-Headers' => 'authorization']]);
    expect(! isset($r['h']['Access-Control-Allow-Origin']), 'P60', 'CORS: yabancı origin', $r['s'].' ACAO='.($r['h']['Access-Control-Allow-Origin'][0] ?? 'yok'));
    $r = call('OPTIONS', '/api/invitations', null, null, ['headers' => ['Origin' => 'http://localhost:3000', 'Access-Control-Request-Method' => 'GET', 'Access-Control-Request-Headers' => 'authorization']]);
    out('BILGI', 'P61', 'CORS: izinli origin', $r['s'].' ACAO='.($r['h']['Access-Control-Allow-Origin'][0] ?? 'yok').' ACAC='.($r['h']['Access-Control-Allow-Credentials'][0] ?? 'yok'));
    $r = call('GET', '/up');
    out('BILGI', 'P62', '/up sağlık ucu', $r['s'].' gövde uzunluğu='.strlen($r['raw']));

    // ------------------------------------------------------------------ kimlik akışları
    section('Kimlik: numaralandırma, oturum, token ömrü (A1–A7, K90)');
    $r1 = call('POST', '/api/auth/login', null, ['email' => "yok.{$run}@example.test", 'password' => 'Yanlis-Parola-1']);
    $r2 = call('POST', '/api/auth/login', null, ['email' => $A['email'], 'password' => 'Yanlis-Parola-1']);
    expect($r1['s'] === $r2['s'] && $r1['raw'] === $r2['raw'], 'P63', 'giriş: olmayan hesap ↔ yanlış parola aynı yanıt', code($r1).' ↔ '.code($r2));
    $r1 = call('POST', '/api/auth/forgot-password', null, ['email' => "yok.{$run}@example.test"]);
    $r2 = call('POST', '/api/auth/forgot-password', null, ['email' => $A['email']]);
    expect($r1['s'] === $r2['s'] && $r1['raw'] === $r2['raw'], 'P64', 'parola sıfırlama: olmayan ↔ var olan e-posta aynı yanıt', $r1['s'].' ↔ '.$r2['s']);
    $r = call('POST', '/api/auth/register', null, ['firstName' => 'Zeynep', 'lastName' => 'Yılmaz', 'email' => strtoupper($A['email']), 'password' => 'Baska-Parola-2026!']);
    out($r['s'] === 201 ? 'ACIK' : 'BILGI', 'P65', 'kayıt: var olan e-posta (büyük harfle)', code($r).' → kayıt ucu e-postanın kayıtlı olduğunu '.(($r['j']['error']['code'] ?? '') === 'REGISTRATION_FAILED' ? 'genel kodla söylüyor' : 'ayrı kodla söylüyor').' fields='.json_encode($r['j']['error']['fields'] ?? null));
    $r = call('POST', '/api/auth/register', null, ['firstName' => 'İsmail', 'lastName' => 'Çankaya', 'email' => "İSMAİL.{$run}@Example.TEST", 'password' => 'Denetim-Parolasi-2026!']);
    $r2 = call('POST', '/api/auth/login', null, ['email' => "ismail.{$run}@example.test", 'password' => 'Denetim-Parolasi-2026!']);
    expect($r['s'] === 201 && $r2['s'] === 200, 'P66', 'Türkçe İ ile kayıt, küçük harfle giriş (K-3)', 'kayıt '.code($r).' · giriş '.code($r2).' · saklanan='.(User::find($r['j']['user']['id'] ?? 0)?->email === "ismail.{$run}@example.test" ? 'normalize' : 'FARKLI'));
    foreach (['12345678', 'password', 'aaaaaaaa'] as $weak) {
        $r = call('POST', '/api/auth/register', null, ['firstName' => 'Zayıf', 'lastName' => 'Parola', 'email' => 'zayif.'.bin2hex(random_bytes(3))."@example.test", 'password' => $weak]);
        out($r['s'] === 201 ? 'ACIK' : 'OK', 'P67', "zayıf parola kabulü: {$weak}", code($r));
    }
    clearLimits();
    $L = call('POST', '/api/auth/login', null, ['email' => $B['email'], 'password' => 'Denetim-Parolasi-2026!'], ['headers' => ['User-Agent' => 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) Safari/604.1']]);
    $tokB2 = $L['j']['token'] ?? '';
    $sess = call('GET', '/api/auth/sessions', $B['token']);
    $sidB = $sess['j']['data'][0]['id'] ?? 0;
    $r = call('DELETE', "/api/auth/sessions/{$sidB}", $A['token']);
    expect($r['s'] === 404 && call('GET', '/api/auth/me', $B['token'])['s'] === 200, 'P68', 'A → B\'nin oturumunu kapatma', code($r).' oturum sayısı='.count($sess['j']['data'] ?? []));
    $r = call('POST', '/api/auth/logout', $tokB2);
    $r2 = call('GET', '/api/auth/me', $tokB2);
    expect($r['s'] === 204 && $r2['s'] === 401, 'P69', 'çıkıştan sonra token geçersiz', $r['s'].' → me '.code($r2));
    $tid = (int) explode('|', $B['token'])[0];
    DB::table('personal_access_tokens')->where('id', $tid)->update(['created_at' => now()->subDays(31)]);
    $r = call('GET', '/api/auth/me', $B['token']);
    expect($r['s'] === 401, 'P70', '31 günlük token reddediliyor (K90)', code($r));
    DB::table('personal_access_tokens')->where('id', $tid)->update(['created_at' => now()]);
    out('BILGI', 'P71', 'token deposu', 'tabloda düz token saklanmıyor: token kolonu uzunluğu='.strlen((string) DB::table('personal_access_tokens')->where('id', $tid)->value('token')).' (sha256 hex 64)');

    section('Kimlik: e-posta değişikliği ve parola sıfırlama (Faz 10, Faz 14)');
    $newMail = "elif.yeni.{$run}@example.test";
    $r = call('POST', '/api/auth/email-change', $C['token'], ['email' => $newMail, 'currentPassword' => 'yanlis-parola']);
    expect($r['s'] === 422, 'P72', 'e-posta değişikliği: yanlış mevcut parola', code($r));
    $r = call('POST', '/api/auth/email-change', $C['token'], ['email' => $newMail, 'currentPassword' => 'Denetim-Parolasi-2026!']);
    $links = mailLinks('signature=');
    $link = end($links) ?: '';
    $q = (string) parse_url($link, PHP_URL_QUERY);
    out('BILGI', 'P73', 'e-posta değişikliği talebi', code($r).' · postada imzalı bağlantı bulundu='.var_export($link !== '', true).' · yol='.parse_url($link, PHP_URL_PATH).' · parametreler='.implode(',', array_keys((static function (string $q): array { parse_str($q, $o); return $o; })($q))));
    if ($q !== '') {
        parse_str($q, $qa);
        $bad = $qa;
        $bad['email'] = "saldirgan.{$run}@example.test";
        $r = call('POST', '/api/public/email-change/confirm?'.http_build_query($bad));
        expect($r['s'] !== 204 && $r['s'] !== 200, 'P74', 'imzalı bağlantıda e-postayı değiştirme', code($r));
        $r = call('POST', '/api/public/email-change/confirm?'.$q);
        $cu = User::find($C['id']);
        $r2 = call('GET', '/api/auth/me', $C['token']);
        expect(in_array($r['s'], [200, 204], true) && $cu->email === $newMail && $r2['s'] === 401, 'P75', 'geçerli bağlantı: adres değişti, eski oturumlar kapandı', code($r).' email değişti='.var_export($cu->email === $newMail, true).' eski token '.code($r2));
        $r = call('POST', '/api/public/email-change/confirm?'.$q);
        expect(! in_array($r['s'], [200, 204], true), 'P76', 'aynı bağlantı ikinci kez', code($r));
    }
    clearLimits();
    call('POST', '/api/auth/forgot-password', null, ['email' => $D['email']]);
    $links = mailLinks('token=');
    $link = end($links) ?: '';
    parse_str((string) parse_url($link, PHP_URL_QUERY), $rp);
    if (isset($rp['token'])) {
        $r = call('POST', '/api/auth/reset-password', null, ['token' => $rp['token'], 'email' => $A['email'], 'password' => 'Yeni-Parola-2026!']);
        expect($r['s'] !== 204, 'P77', 'D\'nin sıfırlama token\'ı A\'nın e-postasıyla', code($r));
        $r = call('POST', '/api/auth/reset-password', null, ['token' => $rp['token'], 'email' => $D['email'], 'password' => 'Yeni-Parola-2026!']);
        $r2 = call('GET', '/api/auth/me', $D['token']);
        expect($r['s'] === 204 && $r2['s'] === 401, 'P78', 'parola sıfırlandı, eski oturumlar kapandı', code($r).' eski token '.code($r2));
        $r = call('POST', '/api/auth/reset-password', null, ['token' => $rp['token'], 'email' => $D['email'], 'password' => 'Ucuncu-Parola-2026!']);
        expect($r['s'] !== 204, 'P79', 'sıfırlama token\'ı ikinci kez', code($r));
    } else {
        out('BILGI', 'P77', 'parola sıfırlama bağlantısı postada bulunamadı', 'bağlantı sayısı='.count($links));
    }

    // ------------------------------------------------------------------ hesap silme
    section('Hesap silme (K97)');
    $E = register('Deniz', 'Koç', 'deniz');
    $invE = newInvitation($E['token']);
    $r = call('POST', "/api/invitations/{$invE['id']}/checkout", $E['token'], ['tier' => 'standart']);
    $oe = $r['j']['data']['orderId'];
    payOrder($oe);
    call('POST', "/api/invitations/{$invE['id']}/publish", $E['token']);
    $rg = call('POST', "/api/public/invitations/{$invE['id']}/rsvps", null, ['guestName' => 'Hatice Güneş', 'guestCount' => 2, 'status' => 'attending', 'message' => 'Görüşmek üzere']);
    $ug = $up("/api/public/invitations/{$invE['id']}/media", null, 'rsvp_photo', $jpeg, 'misafir.jpg');
    $mE = Media::find($ug['j']['data']['id'] ?? '');
    $fileE = $mE ? $base.'/storage/app/public/'.$mE->path : '';
    $r = call('DELETE', '/api/auth/me', $E['token'], ['password' => 'yanlis']);
    expect($r['s'] === 422 && User::find($E['id']) !== null, 'P80', 'hesap silme: yanlış parola', code($r));
    $r = call('DELETE', '/api/auth/me', $E['token'], ['password' => 'Denetim-Parolasi-2026!']);
    $ordE = DB::table('orders')->where('id', $oe)->first();
    expect($r['s'] === 204 && User::find($E['id']) === null && Invitation::withTrashed()->find($invE['id']) === null && Rsvp::where('invitation_id', $invE['id'])->count() === 0 && ($fileE === '' || ! file_exists($fileE)) && $ordE !== null && $ordE->user_id === null, 'P81', 'hesap silindi: kullanıcı, davetiye, LCV, medya dosyası yok; sipariş anonim kaldı', code($r).' kullanıcı='.var_export(User::find($E['id']) !== null, true).' davetiye='.var_export(Invitation::withTrashed()->find($invE['id']) !== null, true).' LCV='.Rsvp::where('invitation_id', $invE['id'])->count().' dosya='.var_export($fileE !== '' && file_exists($fileE), true).' sipariş.user_id='.var_export($ordE->user_id ?? 'satır yok', true));
    $r = call('GET', "/api/public/invitations/{$invE['id']}");
    expect($r['s'] === 404, 'P82', 'silinen hesabın davetiyesi misafir ucunda (cache temizlendi mi)', code($r));

    // ------------------------------------------------------------------ hız sınırları
    section('Hız sınırları (K36, K93, K104)');
    $hit = null;
    for ($i = 1; $i <= 8; $i++) {
        $r = call('POST', '/api/auth/login', null, ['email' => $A['email'], 'password' => 'Kaba-Kuvvet-'.$i]);
        if ($r['s'] === 429) {
            $hit = $i;
            break;
        }
    }
    expect($hit === 6, 'P83', 'giriş kaba kuvvet: e-posta+IP başına 5/dk', 'ilk 429 istek no='.var_export($hit, true).' Retry-After='.($r['h']['Retry-After'][0] ?? 'yok').' gövde='.json_encode($r['j']['error'] ?? null));
    $r = call('POST', '/api/auth/login', null, ['email' => $A['email'], 'password' => 'Denetim-Parolasi-2026!']);
    out('BILGI', 'P84', 'kilitliyken DOĞRU parola (hesap sahibini kilitleme etkisi)', code($r));
    clearLimits();
    $hit = null;
    for ($i = 1; $i <= 70; $i++) {
        $r = call('GET', "/api/public/invitations/{$idA}");
        if ($r['s'] === 429) {
            $hit = $i;
            break;
        }
    }
    out($hit !== null ? 'BILGI' : 'OK', 'P85', 'tek IP\'den misafir sayfası okuma tavanı (genel api kovası 60/dk, IP anahtarlı)', 'ilk 429 istek no='.var_export($hit, true).' Retry-After='.($r['h']['Retry-After'][0] ?? 'yok'));
    $r = call('GET', '/api/invitations', $A['token']);
    out($r['s'] === 429 ? 'ACIK' : 'OK', 'P86', 'aynı IP\'deki GİRİŞ YAPMIŞ kullanıcı da aynı kovada mı (misafir trafiği sahibi kilitliyor mu)', code($r));
    clearLimits();
} catch (Throwable $e) {
    echo "\n!! SONDA DURDU: ".get_class($e).': '.$e->getMessage().' @ '.basename($e->getFile()).':'.$e->getLine()."\n";
    clearLimits();
}

echo "\n# Özet: OK {$counts['OK']} · ACIK {$counts['ACIK']} · BILGI {$counts['BILGI']}\n";
