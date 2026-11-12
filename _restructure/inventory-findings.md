## 3. Başlangıç durumu (2026-11-12)

- `davetkart-docs`'ta hiç commit yoktu; bütün dosyalar takip edilmiyordu.
- `claude/` kendi `.git`'i olan ayrı bir depoydu (`davetkart-claude`, 5 commit, son 2026-09-04).
  Çalışma ağacında `PHP-LARAVEL-SETUP.md` değişmiş (+200/−53 satır), `EK-FAZ-11/12` eklenmemişti.
- İsmail'in kararı (**B seçeneği**): sıfırdan başla. `claude/.git` →
  `D:\Projects\davetkart\_backup\davetkart-claude.git` (depo dışı; silinmedi). Eski commit listesi
  `_restructure/claude-git-log.txt`, dosya bazında son commit tarihleri `claude-git-dates.tsv`.
- Başlangıç commit'i `9e428a8` (`main`): o anki hâl, olduğu gibi. `PHP-LARAVEL-SETUP.md`'nin
  bekleyen değişikliği de bu commit'e girdi; EK-11/12'nin "önce o commit'lensin" ön koşulu artık sağlandı.
- 🔴 `Claude outputs/_snap/` içindeki 3 arşivde `.env` var (`repo.tgz`, `fe.tgz`,
  `_partial-snapshot.tgz`). Hiçbir `.tgz/.tar/.bundle` git'e alınmadı (`.gitignore`); diskte duruyor.
- Metin dosyalarında sır taraması (AWS anahtarı, `APP_KEY`, özel anahtar, IBAN deseni): bulgu yok.

## 4. Mükerrerler

Belge düzeyinde mükerrer yok. Benzer görünenler:

| Dosyalar | Sonuç |
|---|---|
| `claude/PROMPT.md` ↔ `claude/PROMPT-ARSIV-FAZ-4.md` | Aynı başlık, farklı dönem. ARSIV, PROMPT'un Faz 4'e kadarki eski sürümü (PROMPT.md bunu kendisi söylüyor). İkisi de arşive. |
| `Claude outputs/f14/backend/14.x/...` içinde aynı dosyanın birkaç sürümü (`routes/api.php`, `docs/rehber/routes/api.md`, `config/davetkart.php`, `ErrorCode.php`) | Mükerrer değil: her adım klasörü o adımdaki hâldir. Klasör bütün olarak taşındı. |
| `f13-ara/13.2` ↔ `f13-ara/son` | Aynı, ara ve son sürüm. Bütün olarak taşındı. |

## 5. Karar kaydı (K numaraları)

Taranan yerler: bu depodaki `PHP-LARAVEL-SETUP.md` + `EK-FAZ-11/12`, ve **salt okunur**
olarak backend deposundaki `claude/PHP-LARAVEL-SETUP-EK-FAZ-5…9.md`, `claude/FAZ-10-PLANI.md`,
`docs/rehber/fazlar/FAZ-*.md`, `docs/07`.

| Aralık | Tanımlandığı yer | Ana dosyada (`§7`)? |
|---|---|---|
| K1–K48 | `PHP-LARAVEL-SETUP.md` §7 | ✅ |
| K49–K53 | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-5.md` | ❌ |
| K54–K63 | backend `claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md` | ❌ |
| K64–K71 | backend `claude/…-EK-FAZ-7.md` | ✅ (işlenmiş) |
| K72–K79 | backend `claude/…-EK-FAZ-8.md` | ❌ |
| K80–K86 | backend `claude/…-EK-FAZ-9.md` | ❌ |
| K87–K93, K95–K106 | backend `claude/FAZ-10-PLANI.md` (`EK-FAZ-10` hiç yazılmadı) | ❌ |
| K94 | Faz 10 planında Shopier için ayrıldı; Faz 12'de `EK-FAZ-12` + `FAZ-12.md`'de tanımlandı | ❌ |
| K107–K116 | `EK-FAZ-11.md` | ❌ |
| K117–K127 | `EK-FAZ-12.md` | ❌ |

- **Eksik numara:** yok. K1–K127 arası her numaranın bir tanımı var. K9 `K9'` olarak yazılı
  (MySQL kararı PostgreSQL ile değişti, numara asal işaretle korunmuş).
- **Çakışma:** daha önce görülen ikinci **K18** backend `docs/07` §8'deydi (Pest/PHPUnit satırı).
  Orada zaten **K24** olarak düzeltilmiş, satırda not var (`docs/07:958`). Bu depoda çakışma yok.
  ⚠️ Sıra dışı: K94, K95–K106'dan sonra (Faz 12'de) tanımlandı. Çakışma değil, numara önceden ayrılmıştı.
- **Geçersiz kılınan / sapılan:** K9 → K9' · K66 "public_slug üretilmiyor" (K40'ın sonucu) ·
  K122 callback'te **K69'dan bilinçli sapma** (OSB ucunda K69 geçerli) · K43 ⚠️ "Faz 7'de uygulanmadı"
  (açık ticari karar) · K67 ↔ frontend 11.6 çelişki sorusu açık (`EK-FAZ-12` §F-7) ·
  K11'in durumu ana dosyada hâlâ "📋 Faz 2'de uygulanacak" (eskimiş durum metni).
- **Ana dosyaya işlenmemiş:** K49–K63, K72–K127 (yukarıdaki ❌ satırlar). Ana dosyanın başındaki
  uyarı K49–K63 ve K72–K86 için bunu zaten söylüyor; K87 sonrası için bir uyarı yok.

## 6. Bağlantılar (düzenleme öncesi)

- Markdown bağlantısı: belge katmanında yalnızca 1 tane var
  (`claude/PROMPT.md` → `PROMPT-ARSIV-FAZ-4.md`, hedef var). `f14/` içindeki bağlantılar kod deposunun
  `docs/rehber/` ağacına göre yazılmış; bu depoda kırık görünmeleri doğal, kapsam dışı.
- Düz metin yollar (`claude\…`, `claude/…`): ~40 atıf. Çoğu **backend deposunun** `claude/`
  klasörüne (`GOZDEN-GECIRME-RAPORU.md`, `FAZ-9-DEVIR.md`, `EK-FAZ-5…9`, `FAZ-10-PLANI.md`) gidiyor,
  taşımadan etkilenmiyor. Bu depodaki dosyalara giden düz metin yollar (`claude\Notlar\…`,
  `claude/PHP-LARAVEL-SETUP.md`, `claude/YAYIN-PLANI.md`, `Claude outputs\f14` …) tarihsel
  anlatımın parçası. **Değiştirilmedi**; eski → yeni karşılıkları kök `README.md`'de tablo olarak var.

## 7. Dış atıflar (salt okunur, listelendi)

Backend (`davetkart-backend-php-laravel`) — `CLAUDE.md`/`README.md`/`docs/` içinde 58 satır,
frontend (`davetkart-frontent`) — 1 satır. **Bu depoya** işaret edenler:

| Hedef (eski) | Yeni yol | Atıf yapan dosyalar |
|---|---|---|
| `claude/PHP-LARAVEL-SETUP.md` | `context/PHP-LARAVEL-SETUP.md` | backend `docs/09:888`, `docs/11:2906`, `docs/11:2981`, `docs/rehber/fazlar/FAZ-0.md:266`, `FAZ-1.md:314`, `FAZ-2.md:381`, `FAZ-3.md:444`, `FAZ-5.md:431`, `FAZ-6.md:325`, `FAZ-12.md:74` |
| `claude/Notlar/03-FRONTEND-YAPILACAKLAR.md` | `notes/03-FRONTEND-YAPILACAKLAR.md` | backend `docs/03:314`, `docs/07:382`, `docs/08:300`, `rehber/app/Exceptions/InvalidCredentialsException.md:107`, `rehber/app/Http/Resources/UserResource.md:222`, `rehber/database/migrations/2026_08_19_120100_create_timeline_events_table.md:235`, `rehber/fazlar/FAZ-0.md:75`, `FAZ-0.md:267`, `FAZ-2.md:298`, `FAZ-2.md:380`, `FAZ-3.md:443`, `FAZ-5.md:432`, `rehber/tests/Feature/InvitationTest.md:360`; frontend `docs/rehber/src/data.md:136` |
| `claude/Notlar/04` | — (bu depoda yok; backend `claude/Notlar/`'a bakılmalı) | backend `docs/07:557` |
| `claude/PHP-LARAVEL-SETUP-EK-FAZ-11.md` | `decisions/addenda/…` | backend `docs/rehber/fazlar/FAZ-11.md` |

Geri kalan atıflar backend deposunun **kendi** `claude/` klasörüne gidiyor (22 dosya, git'te
takipli): `GOZDEN-GECIRME-RAPORU.md`, `GOZDEN-GECIRME-2026-10-09-{BACKEND,FRONTEND}.md`,
`TEST-DENETIMI-2026-09-24.md`, `FAZ-{5,6,7,9}-DEVIR.md`, `FAZ-10-PLANI.md`, `PROMPT-FAZ-{6,7,8,9}*.md`,
`OKUBENI-FAZ-5.md`, `PHP-LARAVEL-SETUP-EK-FAZ-5…9.md`, `Notlar/`. Atıflar arasında
`claude/FAZ-13-PLANI.md`, `claude/FAZ-14-PLANI.md`, `claude/PROMPT-FAZ-12.md` de var; ilk ikisi hiçbir
depoda bulunamadı.
