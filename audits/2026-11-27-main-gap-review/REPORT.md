# `main` sonrası durum: hangi planlar yapıldı, hangileri kalmadı

> **Tarih:** 27 Kasım 2026 · **Tür:** salt okunur gözden geçirme (kod değişmedi)
> **İstek (İsmail):** canlıdaki `main` ile yeni sürüm arasında ne yapıldı, ne yapılmadı?
> **Sonraki adım:** sunucu rehberi [`../../operations/deployment/YAYIN-REHBERI-v1.3.0.md`](../../operations/deployment/YAYIN-REHBERI-v1.3.0.md)

## 1. Karşılaştırılan uçlar

| Depo | Canlıda (`origin/main`) | Yayın adayı | Fark |
|---|---|---|---|
| backend | `03d3940` (26 Eki) | `faz-21-backlog` @ `1191a95` (27 Kas) | +382 commit, `main` geride değil (ileri sarma mümkün) |
| frontend | `47aedc8` (26 Eki) | `faz-21-backlog` @ `e28b599` (27 Kas) | +192 commit, `main` geride değil |
| docs | `dcae80b` (16 Kas, Faz 18 planı) | `docs/2026-11-27-faz-21-backlog` @ `86d9bf8` | +139 commit, `main` geride değil |

- Üç depoda da en yeni dal `faz-21-backlog`. Faz 18, 19, 19-fix, 20 dallarının ve bütün `fix/…` dallarının tamamı onun içinde
  (`git rev-list <dal> ^faz-21-backlog` = 0).
- İçinde **olmayan** dallar yalnızca `main`'den eski işler: frontend `edit-desing*`, `feature/*`, `new/*`, `fix/desing` (Temmuz–Eylül),
  `new-page-desing` (1 commit, 25 Eyl, `ARC-08` listesinde), backend `faz-11` (Eki başı). Yayına girmeleri gerekmiyor.
- Üç depoda da **hiç etiket yok** (`v1.0.0` bile).
- Canlıdaki commit'ler `YAYIN-PLANI.md` §8 Y10.3b kaydından: backend `03d3940`, frontend `47aedc8`. Sunucuda doğrulanmadı (B7).

## 2. Bu oturumda koşulanlar (B7)

| Kontrol | Sonuç (görülen çıktı) |
|---|---|
| Frontend `npm ci` + `npm run check` (aday uç, Node 22.23) | çıkış 0 |
| Backend `composer audit --locked` (aday `composer.lock`) | "No security vulnerability advisories found." |
| `contracts/plan-rules.json` ve `error-codes.json`, backend ↔ frontend (satır sonu yok sayılarak) | ikisi de AYNI |
| Backend `composer check` | **koşmadı**: bu ortamda PHP 8.3 var, proje `^8.5` istiyor. Son yeşil kayıt: Faz 21 §7 (1354/1354) |
| `npm run e2e` | **koşmadı** (backend PHP 8.5 gerektiriyor). Son yeşil kayıt: Faz 21 §7 (6/6) |
| Sunucu | **koşmadı**; erişim yok |

## 3. Yapılanlar (kod tamam, `faz-21-backlog`'da, henüz `main`'de değil)

### 3.1 `AUD-2026-11-12` (62 bulgu)

| Grup | Adet | Nerede kapandı | Durum |
|---|---|---|---|
| 🟠 Yüksek | 6 | Faz 18: `OPS-01`, `OPS-02`, `SEC-01`, `SEC-02`, `SEC-03`, `SEC-04` | ✅ kod. `OPS-02` (yedek) ve `SEC-04` (Nginx) sunucuda **kurulmadı** |
| 🟡 Orta | 29 | `TST-01` Faz 18.1; kalan 28 Faz 19 (19.1–19.28) | ✅ kod. Tek kısmi: `SEC-10` (telefon gerçek, TCKN/adres Shopier cevabına kadar yer tutucu) |
| 🟢 / 💡 | 27 | Faz 18–19: `ARC-09`, `SEC-14`, `FE-05`, `FE-09`, `FE-56` · Faz 20: `OPS-06`, `FE-06`, `FE-55`, `FE-57` · Faz 21: 18 madde | ✅ 23 kod · 4 yalnızca plan/liste (aşağıda) |

Faz 21'de **kod yazılmayan**, bilinçli olarak plan ya da liste bırakılan dört madde:

| Bulgu | Ne yapıldı | Kalan |
|---|---|---|
| `SEC-18` (token `httpOnly` çerezde) | Geçiş planı, K274 (`phases/faz-21/README.md` Ek A) | Uygulama ayrı faz; önkoşul CSP zorlaması (K175). Beş karar sorusu (Ek A.10) |
| `OPS-09` (yatay ölçek) | Eşik tablosu `YAYIN-PLANI.md` §6.1, ölçüm komutları `IZLEME.md` §6 | Sunucuda haftalık bakılacak |
| `SEC-17` (diskteki eski kod arşivleri) | Ad listesi (Ek B) | Arşivleri sil/şifrele; içlerindeki AWS ve Gemini anahtarları doluysa **döndür** |
| `ARC-08` (dal hijyeni, etiket) | Komut listesi `phases/faz-21/FAZ-21-ARC-08-KOMUTLARI.md` | Etiketler ve dal silme İsmail'in |

### 3.2 Denetim dışı düzeltmeler

| Kaynak | Kapanan |
|---|---|
| Faz 19 ortak düzeltme (Hat A/B/C) | Hat A H1–H4, E1–E4, E6–E9 (K260 mevcut hesaplar doğrulanmış sayılır, K261 boş taslak temizliği, K262 alıcı telefonu); Hat B B-H1–B-H7, B-E1/2/4/6/7/8/10 (K233 silme günlüğü, K234 sipariş saklama, K235 paylaşım kapakları, K236 e2e iş akışı taslağı, K237 bundle bütçesi), B-D8/10/11/14; Hat C #1–#4, #7, #11–#20, #27, #30 |
| `AUD-2026-11-26` → Faz 20 | `OPS-10` (sağlık ucunda `schema`), `SEC-51` (Symfony yaması), `OPS-11` (`composer sync`), `OPS-06` ↑ (deploy bakım kipinde, K264), `OPS-13`, `FE-57`, `FE-55`, `FE-06` |

## 4. Yapılmayanlar

### 4.1 Yayının kendisi (hiçbiri yapılmadı)

| # | İş | Not |
|---|---|---|
| 1 | Üç depoda `faz-21-backlog` → `main` birleştirmesi ve push | Sıra: backend → frontend → docs (K148) |
| 2 | Etiketler | `v1.0.0` (canlıdaki iki commit, önce sunucuda doğrula), sonra yayın etiketi. `v1.1.0`/`v1.2.0` için soru açık: `v1.2.0`'ın `faz-19-fix` ucu `composer audit` kırmızı (`SEC-51`). Öneri: yalnızca tarihî işaret ya da hiç atma; yayın etiketi **`v1.3.0`** |
| 3 | Sunucuda deploy | Rehber: `YAYIN-REHBERI-v1.3.0.md` |
| 4 | İki commit konusunda proje kural dosyasının adı geçiyor (fe `2cc799f`, docs `56a65ca`) | İsteğe bağlı: push'tan önce `reword` (Faz 21 §6 21.90). Push'tan sonra yapılamaz |

### 4.2 Sunucu ve AWS adımları (kod hazır, kurulmadı)

| Adım | Kaynak | Yayına etkisi |
|---|---|---|
| Nginx: güvenlik başlıkları snippet'i + paylaşım önizlemesi + `/fonts/` | `SEC-04` K173, `FE-04` K230, `SEC-12` K226 | Kurulmazsa SPA başlıksız, WhatsApp önizlemesi yok |
| PHP OPcache (`validate_timestamps=0`) + FPM havuzu | `OPS-07` K269 | İsteğe bağlı ama önerilen; bellek sorusu açık |
| Nginx `log_format` ile istek kimliği | `OPS-08` K268 | İsteğe bağlı |
| Gece yedeği: bucket, IAM, AWS CLI, betik, cron, ilk prova | `OPS-02` K151–K157, Y11.5–Y11.6 | 🔴 Canlıda bugün yalnızca Lightsail görüntüsü var |
| Sentry DSN + Crons | `OPS-03`, Y11.3 | Hata ve iş takibi yok |
| Dış izleyici (`/api/health`, SSL bitişi, yedek kalp atışları) | `OPS-03` K255–K256, Y11.7 | Site düşerse haber yok |
| **SES production erişimi** | Y7.5 (26 Ekim'den beri ertelendi) | 🔴 **Yeni sürümle yayın engeline dönüşüyor:** `SEC-09` (K191) yeni hesaplarda ödeme/yayını doğrulama postasına bağlıyor; sandbox'ta posta yalnızca doğrulanmış adreslere gider. Mevcut hesaplar K260 göçüyle doğrulanmış sayılır |
| Gemini anahtarı | Y11.4 | Sunucuda `AI_PROVIDER=null` |
| Y12 canlı doğrulama, `main` dal koruması | Y12 | — |
| `media:move-disk` (canlıda `public` diskte medya varsa) | Hat A İ8 | Sunucu ilk günden S3'te; büyük olasılıkla 0 dosya, `--dry-run` ile bak |
| `env:template --env=.env --check`, `about`, `schedule:list` | Hat A İ2, İ3 | Deploy'dan sonra |

### 4.3 Karar bekleyenler (hepsi varsayılanla çalışıyor)

| Konu | Şu an geçerli | Kaynak |
|---|---|---|
| Faz 21 §5'in bütün soruları | Varsayılanlar, K265–K275 "İsmail cevaplamadı" | `phases/faz-21/README.md` |
| FPM bellek payı | 4 süreç; tavanlar toplamı 2 048 MB'ı ~220 MB aşıyor. Sunucuda 2 GB takas zaten var (Y5.2) | 21.5 |
| `composer test:parallel` `check`'e girsin mi | Hayır | 21.10 |
| SEC-18 beş soru | — | Ek A.10 |
| Zayıf parolalı mevcut hesaplar | Zorlanmıyor (K258) | Hat C #28 |
| Frontend K18 cırcırı | Yok | Hat C #26 |
| K252 (Gold tanımı) onayı | Yalnızca kod yorumunda | Hat C #24 |
| Hat A K-1…K-5, K-8 · Hat B K-1…K-7 | Varsayılanlar (misafir yükleme kapalı, e2e CI'da koşmaz …) | Hat A/B §5 |
| Shopier TCKN/adres | Yer tutucu; soru gönderilmedi | `notes/04-SHOPIER-ALICI-ALANLARI-SORUSU.md` |
| Natro posta (11 Ocak 2027'de bitiyor) | Karar **11 Aralık 2026**'ya kadar | `SURE-TAKVIMI.md` §3 |
| `davetkart.com` otomatik yenileme | 4 Ekim'de kapalıydı; durum bilinmiyor | `SURE-TAKVIMI.md` §1 |
| Lansman kapısı (YD-5, KVKK aydınlatma) | Açık | `YAYIN-PLANI.md` §7 |

### 4.4 Ürün kapsamında kalan, kod dışı işler

- Gizlilik metninin hukukçuya okutulması (Hat B B-İ5), WhatsApp'ta gerçek önizleme (B-İ3), Narrator (B-İ10), gerçek cihazda mobil ölçüm (B-İ12).
- İngilizce çeviri ayrı faz (B-E9); `motion` ilk yüklemeden çıkmadı (B-E5 yarısı).
- İlk CI koşusu: pcov kapsam eşiği 92,9 (K273), `.nvmrc` (K272), `e2e.yml` için `BACKEND_REPO_TOKEN` (K236).
- "Gördüm, dokunmadım" listesi (Faz 21 §7 madde 13): `INVITATION_LOCKED` yorumları, `vite.config.ts` AI Studio yorumu,
  izlenen `.pyc`, okunmayan `auth.login_rate_limit_per_minute`, başka sekmede ödeme dönüşü (K267 B6).

## 5. Bu gözden geçirmede görülen yeni noktalar

| # | Gözlem | Öneri |
|---|---|---|
| G1 | Canlıdaki `deploy.sh` eski sürüm: `git pull`'u bakım kipi **olmadan** yapar, `deploy/` değiştiği için yeni betiğe geçer, `artisan down` ancak o zaman açılır. Arada yeni kod eski `vendor/` ve eski şemayla birkaç saniye cevap verebilir (`deploy.md` adım 0b uyarısı) | İlk deploy'dan önce bakım kipini **elle** aç (rehber §4.1) |
| G2 | `2026_11_16` göçü, aynı kullanıcının birden fazla bekleyen ilk yayın indirimli siparişi varsa **bilerek durur** (K162); site bakımda kalır | Deploy'dan önce çakışma sorgusu (rehber §3.4) |
| G3 | `SEC-09` + SES sandbox: yeni kayıtlar doğrulama postası alamaz → ödeme/yayın 403 | SES production talebi yayından önce ya da hemen sonra (rehber §7) |
| G4 | `opcache.validate_timestamps=0` kurulduktan sonra `.env` değişikliği + `config:cache` da FPM reload ister (`config.php` bir PHP dosyası) | Rehber §5.2 |
| G5 | Silme günlüğü (K233) üretimde medya bucket'ına (`deletion-log/`) yazılır; CloudFront o yolu da sunar. Dosya adları tahmin edilemez (mikrosaniye + ULID), içerik yalnızca tür + kimlik + zaman | Bilgi; istenirse CloudFront'ta `deletion-log/*` engellenir ya da ayrı önek/bucket (karar) |
