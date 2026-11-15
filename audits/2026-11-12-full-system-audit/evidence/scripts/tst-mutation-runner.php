<?php

/**
 * AUD-2026-11-12 — örnek mutasyon koşucusu (kopya: _audit-snap/backend-tst; gerçek depoya DOKUNMAZ).
 *
 * Her mutant: tek satırlık metin değişikliği → hedefli testler → geri alma → sha256 karşılaştırması.
 * Hedefli testlerde hayatta kalan mutant TAM paketle yeniden koşturulur (yanlış süzgeç = sahte "hayatta").
 * Koşan test sayısı 0 ise sonuç REDDEDİLİR. TestSuiteIsolationTest hariç tutulur (kopyada test DB adı farklı).
 *
 * Kullanım (PowerShell): php tst-mutation-runner.php            → hepsi
 *                        php tst-mutation-runner.php M05 M12    → seçilenler
 */

declare(strict_types=1);

$copy = 'D:/Projects/davetkart/_audit-snap/backend-tst';
$out = 'D:/Projects/davetkart/davetkart-docs/audits/2026-11-12-full-system-audit/evidence/mutation';
$summary = 'D:/Projects/davetkart/davetkart-docs/audits/2026-11-12-full-system-audit/evidence/commands/TST-mutation-summary.txt';

// [kimlik, kural, dosya, aranan (dosyada TAM 1 kez), yerine, test süzgeci]
$mutants = [
    ['M01', 'K-1: yayındaki davetiyede plan kontrolü', 'app/Actions/Invitation/UpdateInvitationAction.php', 'if ($fresh->status === InvitationStatus::Published) {', 'if (false) {', 'PaywallTest|InvitationTest'],
    ['M02', 'K-1: sahip olunan plan yükseltilen planı kapsamalı', 'app/Actions/Invitation/UpdateInvitationAction.php', 'if (! $owned->covers($after)) {', 'if (false) {', 'PaywallTest'],
    ['M03', 'Yayın: plan yetmezse 402', 'app/Actions/Invitation/PublishInvitationAction.php', 'if (! $owned->covers($required)) {', 'if (false) {', 'PaywallTest'],
    ['M04', 'K-4/K89: expired → paid geçişi', 'app/Enums/OrderStatus.php', 'self::Expired => $next === self::Paid,', 'self::Expired => false,', 'PaywallTest|OrderStatusTest|MaintenanceTest'],
    ['M05', 'M8: paid yalnızca refunded olabilir', 'app/Enums/OrderStatus.php', 'self::Paid => $next === self::Refunded,', 'self::Paid => true,', 'PaywallTest|OrderStatusTest'],
    ['M06', 'M6: fiyat config\'ten', 'app/Enums/SubscriptionTier.php', "return (int) \$this->config('price');", 'return 1;', 'PaywallTest|PricingTest|QuotePriceActionTest|FirstPublishCheckoutTest'],
    ['M07', 'K126: bildirim tutarı siparişle eşleşmeli', 'app/Actions/Payment/HandlePaymentCallbackAction.php', 'return $notification->amountMinor === $order->amount_minor', 'return true', 'PaymentNotificationAmountTest|ShopierOsbTest'],
    ['M08', 'K126: para birimi eşleşmeli', 'app/Actions/Payment/HandlePaymentCallbackAction.php', '&& $notification->currency === $order->currency;', '&& true;', 'PaymentNotificationAmountTest|ShopierOsbTest'],
    ['M09', 'W2: sahte ağ geçidi imzası', 'app/Services/Payment/FakeGateway.php', 'if (! hash_equals($expected, $signature)) {', 'if (false) {', 'PaywallTest'],
    ['M10', 'Shopier OSB imzası', 'app/Services/Payment/Shopier/ShopierSignature.php', 'return hash_equals($expected, strtolower($hash));', 'return true;', 'ShopierSignatureTest|ShopierOsbTest'],
    ['M11', 'Shopier callback imzası', 'app/Services/Payment/Shopier/ShopierSignature.php', 'return hash_equals($expected, $decoded);', 'return true;', 'ShopierSignatureTest|ShopierCallbackTest'],
    ['M12', 'K111: kişi başı tek kullanım', 'app/Actions/GiftCode/QuoteGiftCodeAction.php', 'if ($usedByUser) {', 'if (false) {', 'GiftCode'],
    ['M13', 'K110: kullanım tavanı', 'app/Actions/GiftCode/QuoteGiftCodeAction.php', 'if ($active >= $giftCode->max_redemptions) {', 'if (false) {', 'GiftCode'],
    ['M14', 'K111: kod satırı kilidi (yarış)', 'app/Actions/GiftCode/ReserveGiftCodeAction.php', '->lockForUpdate()', '', 'GiftCode'],
    ['M15', 'Sahiplik: davetiye', 'app/Policies/InvitationPolicy.php', 'return $user->id === $invitation->user_id;', 'return true;', 'InvitationTest|PaywallTest|RsvpTest|MediaTest'],
    ['M16', 'Sahiplik: sipariş', 'app/Policies/OrderPolicy.php', 'return $user->id === $order->user_id;', 'return true;', 'OrderTest|RefundRequestTest'],
    ['M17', 'LCV kotası SUM(guest_count)', 'app/Actions/Rsvp/EnsureRsvpQuotaAction.php', "->sum('guest_count');", '->count();', 'RsvpTest|RsvpEditTest'],
    ['M18', 'Misafir cache anahtarında kimlik', 'app/Models/Invitation.php', "':public-invitation:'.strtolower(\$id);", "':public-invitation:';", 'PublicInvitationTest'],
    ['M19', 'K90: token ömrü 30 gün', 'config/sanctum.php', "'expiration' => 60 * 24 * 30,", "'expiration' => null,", 'AuthTest|SessionTest'],
    ['M20', 'K91: NUL baytı 400', 'app/Http/Middleware/RejectMalformedInput.php', ' || $this->containsNulByte($request->all())', '', 'MalformedInputTest|RsvpTest'],
    ['M21', 'K91: yarım JSON 400', 'app/Http/Middleware/RejectMalformedInput.php', "return \$body !== '' && ! json_validate(\$body);", 'return false;', 'MalformedInputTest|RsvpTest'],
    ['M22', 'K92: giftOptions integer:strict', 'app/Http/Requests/Invitation/InvitationRequest.php', "['integer:strict', 'min:0', 'max:1000000']", "['integer', 'min:0', 'max:1000000']", 'InvitationTest'],
    ['M23', 'K92: guestCount integer:strict', 'app/Http/Requests/Rsvp/RsvpRequest.php', "                'integer:strict',", "                'integer',", 'RsvpTest'], // 16 boşluk: yorum satırındaki aynı metinden ayırır (ilk koşuda ATLANDI)
    ['M24', 'K-8: mapUrl yalnızca http/https', 'app/Http/Requests/Invitation/InvitationRequest.php', "'url:http,https'", "'url'", 'InvitationTest'],
    ['M25', 'K93: Retry-After başlığı', 'app/Exceptions/ApiExceptionRenderer.php', "return is_int(\$retryAfter) ? ['Retry-After' => (string) \$retryAfter] : [];", 'return [];', 'MalformedInputTest|RateLimitTest|AssistantTest'],
    ['M26', 'HSTS yalnızca HTTPS\'te', 'app/Http/Middleware/SecurityHeaders.php', 'if ($request->secure()) {', 'if (false) {', 'HardeningTest'],
    ['M27', 'K-3: Türkçe İ normalizasyonu', 'app/Support/EmailNormalizer.php', "return str_replace(self::DOTTED_SMALL_I, 'i', mb_strtolower(trim(\$email)));", 'return mb_strtolower(trim($email));', 'AuthTest|EmailNormalizerTest|MaintenanceTest'],
    ['M28', 'K36: giriş hız sınırı 5/dk', 'app/Providers/AppServiceProvider.php', "Limit::perMinute(5)->by(\$identity.'|'.IpBucket::of(\$request->ip())),", "Limit::perMinute(500)->by(\$identity.'|'.IpBucket::of(\$request->ip())),", 'AuthTest|RateLimitTest|MalformedInputTest'],
    ['M29', 'F1: MIME içerikten', 'app/Actions/Media/StoreUploadedMediaAction.php', '$mimeType = $file->getMimeType();', '$mimeType = $file->getClientMimeType();', 'MediaTest'],
    ['M30', 'K139: kullanımdaki hak iade edilemez', 'app/Services/Refund/RefundEligibility.php', '$order->invitation_id !== null || $order->isConsumed() => RefundBlocker::InUse,', 'false => RefundBlocker::InUse,', 'RefundRequestTest|SummarizeEntitlementsActionTest|AccountEntitlementsTest'],
    ['M31', 'K139: iade penceresi 14 gün', 'app/Services/Refund/RefundEligibility.php', '! $this->windowIsOpen($order) => RefundBlocker::WindowClosed,', 'false => RefundBlocker::WindowClosed,', 'RefundRequestTest|SummarizeEntitlementsActionTest|AccountEntitlementsTest'],
    ['M32', 'K144: e-posta bağlantısı tek kullanımlık', 'app/Actions/Account/ConfirmEmailChangeAction.php', "if (! hash_equals(EmailChangeLink::fingerprint(\$user->email), \$change['old_fingerprint'])) {", 'if (false) {', 'EmailChangeTest'],
    ['M33', 'K97: hesap silinince token\'lar silinir', 'app/Actions/Auth/DeleteAccountAction.php', '$user->tokens()->delete();', '// mutant;', 'AccountDeletionTest'],
    ['M34', 'K98: çöp kutusu 30 gün', 'app/Console/Commands/PurgeExpiredData.php', "Invitation::onlyTrashed()->where('deleted_at', '<', \$cutoff);", 'Invitation::onlyTrashed();', 'MaintenanceTest'],
    ['M35', 'Faz 17: şablon Gold', 'config/davetkart.php', "'dugun-kelebek' => 'gold',", '', 'TemplateCatalogueTest|PaywallTest'],
    ['M36', 'K131: ilk yayın yalnızca hiç ödeme yokken', 'app/Actions/Pricing/QuotePriceAction.php', 'return $hasPaid ? null : Promotion::firstPublish($percent);', 'return Promotion::firstPublish($percent);', 'QuotePriceActionTest|FirstPublishCheckoutTest|PricingTest'],
    ['M37', 'K134: kapalı ödeme yöntemi reddedilir', 'app/Services/Payment/PaymentMethods.php', 'if (! $this->isEnabled($method)) {', 'if (false) {', 'PaymentMethodGateTest|PaymentMethodsTest'],
    ['M38', 'K82: 3 günlük serbest bırakma penceresi', 'app/Actions/Invitation/DeleteInvitationAction.php', 'return $endsAt === null || $endsAt->isFuture();', 'return true;', 'OrderConsumptionTest|MaintenanceTest|InvitationTest|PaywallTest'],
    ['M39', 'Misafir ucu yalnızca yayınlanmışı gösterir', 'app/Actions/Invitation/ResolvePublicInvitationAction.php', "->where('status', InvitationStatus::Published)", '', 'PublicInvitationTest|RsvpTest'],
    ['M40', 'K101: düzenleme kodu', 'app/Actions/Rsvp/UpdateRsvpAction.php', ' || ! RsvpEditCode::matches($rsvp->edit_code_hash, $editCode)', '', 'RsvpEditTest'],
    ['M41', 'Checkout: seçilen plan davetiyeyi kapsamalı', 'app/Actions/Payment/StartCheckoutAction.php', 'if (! $tier->covers($required)) {', 'if (false) {', 'PaywallTest|CheckoutActionTest'],
    ['M42', 'Hesap silme mevcut parolayı ister', 'app/Http/Requests/Auth/DeleteAccountRequest.php', "'current_password:sanctum'", "'string'", 'AccountDeletionTest'],
    ['M43', 'R7: 4xx Sentry\'ye gitmez', 'bootstrap/app.php', '&& $e->errorCode()->status() < 500,', '&& false,', 'ExceptionReportingTest'],
    ['M44', 'K102: imza yalnızca Elit\'te kalkar', 'app/Actions/Invitation/ResolveBrandingAction.php', '$owned === null || ! $owned->covers($whiteLabel)', 'true', 'PaywallTest|PublicInvitationTest|InvitationTest'],
    ['M45', 'K137: yanmış hak yeniden kullanılamaz', 'app/Actions/Payment/ClaimReleasedOrderAction.php', '->unconsumed()', '', 'OrderConsumptionTest|PaywallTest'],
    ['M46', 'K138: iade talebi açık hak donuk', 'app/Actions/Payment/ClaimReleasedOrderAction.php', '->withoutOpenRefundRequest()', '', 'RefundRequestTest|PaywallTest'],
    // 15 Kasım 2026 eki: M14 hayatta kaldı; "kilitlerin hiçbiri testle korunmuyor mu?" sorusu için üç kilit daha.
    ['M47', 'Kilit: ödeme bildirimi sipariş satırı', 'app/Actions/Payment/HandlePaymentCallbackAction.php', '->lockForUpdate()', '', 'PaywallTest|PaymentNotificationAmountTest|ShopierOsbTest'],
    ['M48', 'Kilit: LCV kotası davetiye satırı', 'app/Actions/Rsvp/EnsureRsvpQuotaAction.php', '->lockForUpdate()', '', 'RsvpTest|RsvpEditTest'],
    ['M49', 'Kilit: serbest hakkın sahiplenilmesi', 'app/Actions/Payment/ClaimReleasedOrderAction.php', '->lockForUpdate()', '', 'OrderConsumptionTest|PaywallTest|RefundRequestTest'],
    // R12: 24 Eylül denetiminde PaywallTest'te hayatta kalan iki mutantın birebir tekrarı.
    ['M50', 'R12: para birimi TRY', 'config/davetkart.php', "'currency' => 'TRY',", "'currency' => 'USD',", 'PaywallTest|PricingTest|OrderTest'],
    ['M51', 'R12: zarf modülü Gold', 'config/davetkart.php', "'show_envelope' => 'gold',", "'show_envelope' => 'standart',", 'PaywallTest'],
];

$only = array_slice($argv, 1);
chdir($copy);
$php = '"'.PHP_BINARY.'"';

function runTests(string $php, string $args): array
{
    $start = microtime(true);
    $raw = (string) shell_exec("{$php} artisan test {$args} 2>&1");
    $secs = round(microtime(true) - $start, 1);
    $tests = 0;
    $failed = 0;
    $failures = [];
    if (preg_match('/\{"tool":"phpunit".*\}/s', $raw, $m) && is_array($j = json_decode($m[0], true))) {
        $tests = (int) ($j['tests'] ?? 0);
        $failed = (int) ($j['failed'] ?? 0) + (int) ($j['errors'] ?? 0);
        foreach (($j['failures'] ?? []) as $f) {
            $failures[] = preg_replace('/^Tests\\\\(Feature|Unit)\\\\/', '', (string) ($f['test'] ?? '?'));
        }
        foreach (($j['errors_list'] ?? $j['error_details'] ?? []) as $f) {
            $failures[] = preg_replace('/^Tests\\\\(Feature|Unit)\\\\/', '', (string) ($f['test'] ?? '?'));
        }
        if (($j['result'] ?? '') !== 'passed' && $failed === 0) {
            $failed = 1;
        }
    } elseif (preg_match('/Tests:\s+(?:(\d+) failed, )?.*?(\d+) passed/', $raw, $m)) {
        $failed = (int) ($m[1] ?? 0);
        $tests = $failed + (int) $m[2];
    } else {
        $failed = -1; // çıktı ayrıştırılamadı (ör. ölümcül hata): mutant kodu çalışmaz hâle getirdi
    }

    return ['tests' => $tests, 'failed' => $failed, 'failures' => array_slice($failures, 0, 4), 'secs' => $secs, 'tail' => substr($raw, -700)];
}

$rows = [];
foreach ($mutants as [$id, $rule, $file, $search, $replace, $filter]) {
    if ($only !== [] && ! in_array($id, $only, true)) {
        continue;
    }
    $path = "{$copy}/{$file}";
    $orig = (string) file_get_contents($path);
    $shaBefore = hash('sha256', $orig);
    $line = substr_count(substr($orig, 0, (int) strpos($orig, $search)), "\n") + 1;
    $log = "# {$id} — {$rule}\n# dosya: {$file}:{$line}\n# aranan : {$search}\n# yerine : ".($replace === '' ? '(silindi)' : $replace)."\n# süzgeç : {$filter}\n# sha256 önce: {$shaBefore}\n";
    if (substr_count($orig, $search) !== 1) {
        $verdict = 'ATLANDI';
        $log .= '# SONUÇ: ATLANDI — hedef metin dosyada '.substr_count($orig, $search)." kez geçiyor (tam 1 olmalı)\n";
        $rows[] = [$id, $rule, "{$file}:-", $filter, 0, $verdict, '-'];
        file_put_contents("{$out}/{$id}.txt", $log);
        echo "{$id} {$verdict}\n";

        continue;
    }
    file_put_contents($path, str_replace($search, $replace, $orig));
    try {
        $r = runTests($php, '--filter="'.$filter.'"');
        $stage = 'hedefli';
        if ($r['failed'] === 0 && $r['tests'] > 0) {
            $log .= "# hedefli koşu: {$r['tests']} test, 0 kırmızı ({$r['secs']} sn) → tam paketle doğrulanıyor\n";
            $r = runTests($php, '--exclude-filter=TestSuiteIsolationTest');
            $stage = 'tam paket';
        }
    } finally {
        file_put_contents($path, $orig);
    }
    $shaAfter = hash('sha256', (string) file_get_contents($path));
    if ($r['tests'] === 0 && $r['failed'] >= 0) {
        $verdict = 'REDDEDİLDİ (0 test)';
    } elseif ($r['failed'] !== 0) {
        $verdict = 'ÖLDÜ';
    } else {
        $verdict = 'HAYATTA';
    }
    $killers = $r['failed'] === -1 ? 'paket çalışmadı (ölümcül hata)' : implode(' ; ', $r['failures']);
    $log .= "# koşu ({$stage}): {$r['tests']} test, {$r['failed']} kırmızı, {$r['secs']} sn\n# öldüren: {$killers}\n# sha256 sonra: {$shaAfter} → ".($shaBefore === $shaAfter ? 'GERİ ALINDI' : '!!! FARKLI')."\n# SONUÇ: {$verdict}\n# --- test çıktısının sonu ---\n".$r['tail']."\n";
    file_put_contents("{$out}/{$id}.txt", $log);
    $rows[] = [$id, $rule, "{$file}:{$line}", $stage, $r['tests'], $verdict, $killers];
    echo "{$id} {$verdict} ({$stage}, {$r['tests']} test, {$r['secs']} sn)\n";
}

$lines = ['# AUD-2026-11-12 mutasyon özeti · '.date('Y-m-d H:i:s')." · kopya backend-tst (d810410)", '# id | kural | dosya:satır | koşu | test | sonuç | öldüren'];
foreach ($rows as $row) {
    $lines[] = implode(' | ', $row);
}
$counts = array_count_values(array_column($rows, 5));
$lines[] = '# TOPLAM: '.count($rows).' · '.implode(' · ', array_map(static fn ($k, $v) => "{$k} {$v}", array_keys($counts), $counts));
file_put_contents($summary, implode("\n", $lines)."\n", $only === [] ? 0 : FILE_APPEND);
echo end($lines)."\n";
