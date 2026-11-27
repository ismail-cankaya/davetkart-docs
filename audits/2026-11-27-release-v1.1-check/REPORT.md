# Yayın öncesi son kontrol: `release-2026-11-28-v1.1`

> **Tarih:** 27 Kasım 2026 · **Tür:** yayın öncesi doğrulama (kod değişmedi)
> **İstek (İsmail):** Hat A/B/C ve denetim bulgularının hepsi bitti; yayından önce son kez kontrol et, hata/eksik yoksa
> `release 2026-11-28-v1.1` dalını aç ve raporla.
> **Önceki gözden geçirme:** [`../2026-11-27-main-gap-review/REPORT.md`](../2026-11-27-main-gap-review/REPORT.md) (kalan sunucu işleri ve kararlar orada; burada kopyalanmadı)

## 1. Sonuç

- **Yayını engelleyen kod hatası yok.** Dört kapı da (backend `composer check`, `composer audit`, frontend `npm run check`, e2e)
  bu oturumda, yayın adayının tam ucunda, PHP 8.5 + PostgreSQL + Node 24 ile yeşil (§3).
- **Bir düşük bulgu (R1, test altyapısı):** e2e betiği `LOG_LEVEL`'i sabitlemiyor. `.env.example`'dan kurulan her ortamda (CI'daki
  `e2e.yml` dahil) yayın yolculuğu düşer. Üretim koduna etkisi yok. Düzeltme tek satır (§4).
- Hat A/B/C ve `AUD-2026-11-12` / `AUD-2026-11-26`'nın **kod** maddelerinin hepsi kapalı (kayıtlarla ve kapılarla uyumlu). Açık
  kalanlar yalnızca sunucu/AWS adımları ve İsmail'in kararları ([gap review §4](../2026-11-27-main-gap-review/REPORT.md#4-yapılmayanlar)).
- Release dalı üç depoda açıldı (§2). `main` birleştirmesi, etiket ve sunucu deploy'u **yapılmadı**.

## 2. Release dalı

| Depo | Dal | Uç | Kaynak |
|---|---|---|---|
| backend | `release-2026-11-28-v1.1` | `1191a95` | `faz-21-backlog` (`main`'den +382 commit, `main` geride değil) |
| frontend | `release-2026-11-28-v1.1` | `e28b599` | `faz-21-backlog` (`main`'den +125 commit, `main` geride değil) |
| docs | `release-2026-11-28-v1.1` | `2fcaf88` + bu rapor | `claude/main-branch-release-guide-l4zmf0` (= `docs/2026-11-27-faz-21-backlog` + yayın rehberi) |

- Ad, mevcut `release-v1.0` / `release-2026-10-20` düzenine göre `release-` önekli.
- Backend ve frontend dalları **doğrulanan uçların ta kendisi**; üstüne commit eklenmedi.

## 3. Bu oturumda koşulan kapılar (B7)

Ortam: PHP **8.5.13** (resmî `php:8.5-cli` imajındaki kaynaktan derlendi; gd, exif, pgsql, pdo_pgsql, mbstring, bcmath, zip,
curl, intl, sodium, argon2, pcov), PostgreSQL 16, Node **24.22.3** (`.nvmrc` = 24), Chromium (Playwright 1.61.1).

| Kapı | Sonuç (görülen çıktı) |
|---|---|
| Backend `composer check` | pint `passed` · phpstan `passed`, 0 hata · `errors:export --check` "Katalog guncel" · `plans:export --check` "guncel" · `env:template --check` "in sync" · `k18: 47 dosya, 0 ihlal` · phpunit **1354/1354**, 5303 assertion (Faz 21 §7 ile aynı) · çıkış 0 |
| Backend satır kapsamı (CI adımı, ilk kez koşuldu) | `php artisan test --parallel --coverage --min=92.9` (pcov): paratest 1354/1354 · **Total 96.0 %** ≥ 92,9 · çıkış 0 |
| Backend `composer audit` | "No security vulnerability advisories found." · `composer validate` "valid" |
| Frontend `npm ci` + `npm run check` | çıkış 0 · lint (`tsc --noEmit`, strict) · build · 15 `verify:*` hepsi ✓ · `npm audit` (tümü ve `--omit=dev`) "found 0 vulnerabilities" |
| Paket bütçesi (`verify:bundle`) | ilk yükleme **712,1 / 720 kB** · misafir sayfası **790,4 / 800 kB** · şablonlar tembel (307) |
| Frontend `npm run e2e` (6 test) | 1. koşu: ❌ `publish` düştü, 5 test koşmadı (R1) · `LOG_LEVEL=debug` ile 2. koşu: **6 passed (1,6 dk)** |
| Sözleşmeler | `error-codes.json`, `plan-rules.json`: backend `contracts/` ↔ frontend `src/contracts/` (satır sonu yok sayılarak) **AYNI** |
| Göçler | `main`'den beri 4 yeni göç okundu; e2e'de boş veritabanında hepsi `DONE`. `2026_11_16` çakışmada bilerek durur (gap review G2) |
| Gizli bilgi taraması | İzlenen `.env` yok (yalnızca `.env.example`); `AIza…`, `AKIA…`, `sk_live`, `-----BEGIN` deseni üç depoda 0; frontend `.env*.example`'da yalnızca `VITE_API_BASE_URL` |
| Deploy betikleri | `bash -n` 6/6 · `shellcheck -S warning` 0 uyarı · `visudo -cf deploy/sudoers/davetkart-deploy` "parsed OK" |
| Nginx (`deploy/nginx/davetkart.conf` + güvenlik snippet'i) | `nginx -t` (1.24, sahte sertifikayla): "syntax is ok". Sonraki adım `[::]:80` bağlanmasında düştü: konteynerde IPv6 yok (ortam) |
| Docs karar indeksi | `build_decision_index.py --check`: `indeks 237 · tanım 237 · eksik 0 · tanımsız 0 · bekleyen 0` (sıradaki K276) |
| Docs iç bağlantılar | Arşiv ve Faz 14 anlık görüntüleri dışında 8 kırık bağlantı; hepsi geçmiş kayıt/prompt (`CLAUDE.md` §8: düzeltilmez) |

**Koşmayanlar:** sunucu (erişim yok) · `php-fpm -t` (FPM derlenmedi) · gerçek SES/Shopier/S3 · CI'ın kendisi (ilk koşu bekliyor).

## 4. Bulgular

| # | Önem | Bulgu | Kanıt | Öneri |
|---|---|---|---|---|
| R1 | 🟢 düşük (test altyapısı) | `scripts/e2e/backend.ps1` `LOG_CHANNEL=single`'ı sabitliyor ama `LOG_LEVEL`'i sabitlemiyor. `.env.example`'da `LOG_LEVEL=error` (Faz 10'dan beri); `log` posta sürücüsü `debug` seviyesinde yazar → doğrulama postası (SEC-09) `laravel.log`'a düşmez, `e2e/support/flows.ts:61` 20 sn bekleyip düşer, bağımlı 5 test koşmaz. CI'daki `e2e.yml` `.env`'i `.env.example`'dan kurduğu için ilk elle tetiklemede **kırmızı** olur. Faz 21'de yerelde 6/6 geçmesi, yerel `.env`'in `debug` olmasından | 1. koşu: `verification mail for e2e.…@example.test` zaman aşımı; kullanıcı oluştu, `jobs` 0, günlükte posta yok. Elle: `config("logging.default")=single`, gönderim "sent", günlükte satır yok. `LOG_LEVEL=debug` eklenince 6/6 | `backend.ps1`'de `$env:LOG_CHANNEL = 'single'` satırının yanına `$env:LOG_LEVEL = 'debug'` + kılavuz (`docs/rehber/scripts/e2e/backend.md` madde 4) bir satır. Ayrı `fix/2026-11-27-…` dalı ya da release dalına tek commit (İsmail karar verir) |
| R2 | 💡 bilgi | Sürüm adı kayıtlarla çakışıyor: `FAZ-21-ARC-08-KOMUTLARI.md` §4 `v1.1.0` = Faz 18 (be `44f6022`, fe `fefa647`), `v1.2.0` = Faz 19/20, bu yayın için önerilen **`v1.3.0`**; gap review ve `YAYIN-REHBERI-v1.3.0.md` de `v1.3.0` diyor | — | Dal adı istendiği gibi bırakıldı. Etikete karar verirken ya bu yayına `v1.1.0` verip ARC-08 tablosunu yeni K ile değiştir, ya da etiket `v1.3.0` olsun. İki depoda aynı ad (K149) |
| R3 | 💡 bilgi | Yayın aralığında yapay zekâ izi: Faz 15–17 commit'lerinin yazarı "Claude" (be `343a775`, `80b9558`, `82c7312`, `d810410`; fe `ffccbe8`, `d637c3c`, `c1e3126`, `44caa49`), `Co-Authored-By` satırlı commit be 29, fe 6; docs `2fcaf88`. Faz 21 §7 taraması yalnızca Faz 21 commit'lerini kapsıyordu ("üç depoda 0" o aralık için doğru). fe `2cc799f` / docs `56a65ca` konusu Faz 21 §6'da zaten not edilmiş | `git log origin/main..faz-21-backlog` | Hepsi zaten `origin`'deki paylaşılan dallarda; yeniden yazmak bütün sonraki hash'leri değiştirir ve zorla push ister. Öneri: geçmiş olarak kabul et; kural yalnızca yeni commit'ler için |
| R4 | 💡 bilgi | Paket bütçesinde pay dar: ilk yükleme 7,9 kB, misafir sayfası 9,6 kB | `verify:bundle` | Bir sonraki özellikten önce B-E5 (`motion` ilk yüklemeden) ya da bütçe kararı |
| R5 | 💡 bilgi | Gap review §1'deki frontend farkı "+192 commit" yazıyor; ölçülen `git rev-list --count origin/main..origin/faz-21-backlog` = **125** | bu oturum | Bilgi (rapor geçmiş kayıt, düzeltilmedi) |

Faz 21 §7 madde 13'teki "gördüm, dokunmadım" listesi (izlenen `.pyc`, `vite.config.ts` AI Studio yorumu, `INVITATION_LOCKED`
yorumları …) değişmedi; yeni bir şey eklenmedi.

## 5. Yayından önce hatırlatma (ayrıntı gap review'da)

Kod hazır; aşağıdakiler kodla çözülmüyor ve yayın günü sırası [`YAYIN-REHBERI-v1.3.0.md`](../../operations/deployment/YAYIN-REHBERI-v1.3.0.md)'de:

1. 🔴 **SES production erişimi** (G3): yoksa yeni kayıtlar doğrulama postası alamaz → ödeme/yayın 403 (`SEC-09`).
2. İlk deploy'da bakım kipini **elle** aç (G1; canlıdaki eski `deploy.sh`).
3. Deploy'dan önce `2026_11_16` çakışma sorgusu (G2).
4. 🔴 Gece yedeği (`OPS-02`) sunucuda kurulu değil.
5. Nginx güvenlik başlıkları / paylaşım önizlemesi / `/fonts/` (`SEC-04`, `FE-04`, `SEC-12`) kurulmadı.
6. Birleştirme sırası backend → frontend → docs (K148); `v1.0.0` için önce sunucudaki commit'i doğrula.
