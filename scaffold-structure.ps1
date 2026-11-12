# =============================================================================
#  DavetKart Backend — Mimari Klasör İskeleti
# =============================================================================
#  NE YAPAR : Mimari planda (docs/03-MIMARI-PLAN.md) tanımlanan, Laravel'in
#             varsayılan kurulumunda BULUNMAYAN klasörleri oluşturur ve her
#             birine .gitkeep koyar.
#
#  NE YAPMAZ: Hiçbir dosyayı silmez, hiçbir dosyanın üzerine yazmaz.
#             Zaten var olan klasörleri atlar. Tekrar tekrar çalıştırılabilir
#             (idempotent).
#
#  ÖN KOŞUL : Laravel kurulu olmalı. Bu betiği proje kökünde çalıştırın:
#             cd D:\Projects\davetkart\davetkart-backend
#             powershell -ExecutionPolicy Bypass -File .\scaffold-structure.ps1
# =============================================================================

$ErrorActionPreference = 'Stop'

# --- Doğrulama: doğru klasörde miyiz? ---------------------------------------
if (-not (Test-Path 'artisan')) {
    Write-Host ""
    Write-Host "  HATA: 'artisan' dosyasi bulunamadi." -ForegroundColor Red
    Write-Host "  Bu betigi Laravel proje kokunde calistirin." -ForegroundColor Red
    Write-Host "  Once Laravel'i kurun: docs/04-KURULUM-VE-KLASOR-YAPISI.md - Bolum 2" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# --- Oluşturulacak klasörler -------------------------------------------------
# Her satır: "yol|aciklama"  (aciklama sadece ekrana basilir)
$folders = @(
    # ---- Actions: is kurallari (domain basina gruplu) ----
    'app/Actions/Auth|Kayit, giris, token iptali',
    'app/Actions/Invitation|Olustur, guncelle, yayinla, public cozumleme',
    'app/Actions/Rsvp|LCV gonderimi ve silme',
    'app/Actions/Media|Dosya yukleme ve kayit',
    'app/Actions/Payment|Checkout baslatma, webhook isleme',

    # ---- Enums: sabit deger kumeleri ----
    'app/Enums|InvitationStatus, RsvpStatus, SubscriptionTier, OrderStatus...',

    # ---- HTTP katmani ----
    'app/Http/Controllers/Api/V1|Namespace''te versiyon, URL''de degil',
    'app/Http/Requests/Auth|LoginRequest, RegisterRequest',
    'app/Http/Requests/Invitation|Store/Update dogrulamalari',
    'app/Http/Requests/Rsvp|StoreRsvpRequest',
    'app/Http/Resources|snake_case -> camelCase donusumu',
    'app/Http/Middleware|SetLocaleFromHeader, ForceJsonResponse',

    # ---- Yetkilendirme ----
    'app/Policies|IDOR korumasi: bu kaynak bu kullanicinin mi?',

    # ---- Dis dunya adaptorleri (Ports & Adapters) ----
    'app/Services/Payment|PaymentGateway arayuzu + Fake/Iyzico',
    'app/Services/Ai|AiProvider arayuzu + Gemini (API anahtari SADECE burada)',
    'app/Services/Pricing|TierResolver - paywall''in sunucu ikizi',

    # ---- Asenkron is ve olaylar ----
    'app/Jobs|15 sn timeout''a takilmayacak uzun isler',
    'app/Events|InvitationPublished, RsvpReceived',
    'app/Listeners|ClearInvitationCache, SendNotification',

    # ---- Ozel istisnalar ----
    'app/Exceptions|PaywallViolationException, RsvpQuotaExceededException',

    # ---- Test ----
    'tests/Feature/Api|Endpoint testleri - asil guvencemiz',
    'tests/Unit/Services|TierResolver gibi saf mantik testleri'
)

Write-Host ""
Write-Host "  DavetKart - Mimari klasor iskeleti kuruluyor" -ForegroundColor Cyan
Write-Host "  ------------------------------------------------------------" -ForegroundColor DarkGray

$created = 0
$skipped = 0

foreach ($entry in $folders) {
    $parts = $entry -split '\|', 2
    $path = $parts[0]
    $desc = if ($parts.Count -gt 1) { $parts[1] } else { '' }

    if (Test-Path $path) {
        Write-Host ("  [ atlandi ] {0}" -f $path) -ForegroundColor DarkGray
        $skipped++
    }
    else {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host ("  [ olustu  ] {0}" -f $path) -ForegroundColor Green
        if ($desc) { Write-Host ("              -> {0}" -f $desc) -ForegroundColor DarkGray }
        $created++
    }

    # .gitkeep: Git bos klasorleri takip etmez, bu dosya klasoru depoda gorunur kilar.
    $keep = Join-Path $path '.gitkeep'
    if (-not (Test-Path $keep)) {
        New-Item -ItemType File -Path $keep -Force | Out-Null
    }
}

Write-Host "  ------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host ("  Tamamlandi.  Olusturulan: {0}   Zaten vardi: {1}" -f $created, $skipped) -ForegroundColor Cyan
Write-Host ""
Write-Host "  Sonraki adim:" -ForegroundColor Yellow
Write-Host "    1) php artisan install:api      (Sanctum + routes/api.php)"
Write-Host "    2) php artisan storage:link     (/storage proxy'si icin)"
Write-Host "    3) php artisan serve            (port 8000 - proxy oraya bakiyor)"
Write-Host ""
Write-Host "  Detaylar: docs/04-KURULUM-VE-KLASOR-YAPISI.md" -ForegroundColor DarkGray
Write-Host ""
