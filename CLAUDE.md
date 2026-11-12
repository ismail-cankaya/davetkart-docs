# CLAUDE.md — davetkart-docs kuralları

Bu dosya bu depoda çalışan **her** yapay zekâ asistanı için bağlayıcıdır. Başka bir dokümanla
çelişirse bu dosya kazanır. Uzun açıklama için bağlantılara bak.

## 1. Bu depo nedir

- DavetKart'ın (dijital davetiye SaaS'ı) **kod dışı** dokümanları. Eski adı `claude/`.
- Kod depoları burada **değil**: `../davetkart-backend-php-laravel`, `../davetkart-frontent`.
  Onların kod kılavuzları (`docs/rehber/`) da kendi depolarında kalır.
- Yığın: backend PHP 8.5 + Laravel 13 (modüler monolit, Action katmanı) · frontend React 19 + TypeScript.

## 2. Oturum başında oku (sırayla)

1. [`README.md`](README.md): harita.
2. [`context/PHP-LARAVEL-SETUP.md`](context/PHP-LARAVEL-SETUP.md): §9 şu anki durum, §10 yol
   haritası, §11 ihlal edilemez kurallar, §2 çalışma kuralları.
3. [`decisions/DECISION-INDEX.md`](decisions/DECISION-INDEX.md): K numaraları, sıradaki boş numara.
4. İşle ilgili `phases/faz-NN/` klasörü (yayın işi için `operations/deployment/`).

## 3. Klasör haritası

| Klasör | Girer | Girmez |
|---|---|---|
| `context/` | Projenin güncel bağlamı ve çalışma kuralları | Faz raporu, prompt |
| `decisions/` | `DECISION-INDEX.md`, `addenda/PHP-LARAVEL-SETUP-EK-FAZ-NN.md` | Kararın tartışması (faz raporuna) |
| `phases/faz-NN/` | O fazın planı, raporu, devir notu, commit komutları, ara çıktıları | Kod kılavuzu (`docs/rehber/` kod deposunda) |
| `prompts/` | Ajanlara verilen `PROMPT-*.md` | Ajanın ürettiği rapor (`phases/` ya da `audits/`) |
| `audits/YYYY-MM-DD-<konu>/` | Denetim ve gözden geçirme raporları | Düzeltme kodu |
| `operations/` | Yayın, AWS, sunucu, DNS (`deployment/` altında) | Sırlar |
| `product/` | Fiyat, plan, tasarım/video onayları | Kod |
| `notes/` | Serbest notlar, araştırmalar, dış kaynak özetleri | Karar (karar `decisions/`'a) |
| `archive/` | Geçersiz kılınmış ya da mükerrer dosyalar (bantlı) | Güncel bir dosyanın kopyası |
| `_restructure/` | 2026-11-12 düzenlemesinin kayıtları ve betikleri | Yeni iş |

**Yeni dosya nereye?**

| Dosya | Yer |
|---|---|
| Ajan prompt'u | `prompts/PROMPT-<konu>.md` |
| Faz planı / raporu / devir notu / commit komutları | `phases/faz-NN/` |
| Tarihli inceleme, denetim | `audits/YYYY-MM-DD-<konu>/` |
| Yeni karar | Fazın `decisions/addenda/` dosyası **ve** `decisions/DECISION-INDEX.md` |
| Yayın / sunucu notu | `operations/deployment/` |
| Eskiyen dosya | `archive/` + en üste bant + `archive/README.md` satırı |
| Hiçbirine uymuyor | `_triage/` + İsmail'e sor |

Arşiv bandı (tek satır, dosyanın en üstü):
`> 🗄️ ARŞİV (YYYY-MM-DD) — Yerine geçen: <yol>. Neden: <tek cümle>.`

## 4. Adlandırma

- Klasörler İngilizce, küçük harf, `kebab-case`. Faz klasörleri `faz-NN` (`faz-07`, `faz-15`).
- Tarihli dosya ve klasörler `YYYY-MM-DD-<konu>`.
- Mevcut dosya adları **korunur**. `context/PHP-LARAVEL-SETUP.md` adı **asla değişmez**.
- Dallar: bu depoda `docs/<YYYY-MM-DD>-<konu>`, `audit/<YYYY-MM-DD>-<konu>`; kod depolarındaki
  düzeltme dalları `fix/<YYYY-MM-DD>-<bulgu-id>-<kısa-ad>`.
- Bulgu kimlikleri `ARC-NN`, `SEC-NN`, `TST-NN`, `FE-NN`, `OPS-NN`; denetim kimliği `AUD-YYYY-MM-DD`.

## 5. Karar kaydı

- Yeni karar = `DECISION-INDEX.md`'deki **sıradaki boş K numarası**.
- Numara asla yeniden kullanılmaz, değiştirilmez. Çakışma görürsen ⚠️ ile işaretle, numarayı İsmail'e bırak.
- Geçersiz kılınan karar silinmez; durumuna `geçersiz kılındı → K…` yazılır.
- Karar hem fazın `addenda/` dosyasına hem `DECISION-INDEX.md`'ye işlenir.
- Çelişkide daha yeni olan kazanır: ek dosyaları > `PHP-LARAVEL-SETUP.md`
  ([`context/PHP-LARAVEL-SETUP.md`](context/PHP-LARAVEL-SETUP.md), başlık notu).

## 6. Yazım

- Dokümanlar Türkçe, kısa ve doğrudan (`PHP-LARAVEL-SETUP.md` §2, kural 6).
- Commit mesajları İngilizce. Bu depoda: `docs(<alan>): <Fiil> ...`
  (ör. `docs(decisions): Add K128 for ...`).
- Bir bilginin tek bir güncel evi olur; diğer yerler ona bağlantı verir, kopyalamaz.
- Klasöre dosya ekleyen ya da çıkaran, o klasörün `README.md`'sini aynı değişiklikte günceller.
- Bu deponun her değişikliği [`CHANGELOG.md`](CHANGELOG.md)'ye bir satır olarak işlenir.

## 7. Çalışma biçimi (mevcut dokümanlardan)

- **Git yazma işlemlerini İsmail yapar.** `add`, `commit`, `push`, `stash`, `reset` çalıştırma;
  commit komutlarını ver ([`prompts/PROMPT-FAZ-11.md`](prompts/PROMPT-FAZ-11.md) §0 madde 2;
  `PHP-LARAVEL-SETUP.md` §2 kural 4: *"Komutları o çalıştırıyor."*).
- Commit komutu: her adım ayrı PowerShell bloğu, dosyalar **tek tek, açık yolla**; joker ve `-A`
  yok; blok `git status --short` ile biter ([`prompts/PROMPT-FAZ-12.md`](prompts/PROMPT-FAZ-12.md) §10 madde 3).
- **B7:** çıktısını görmediğin hiçbir şeye "doğrulandı / geçti" yazma; koşmadıysa "koşmadı" yaz
  ([`prompts/PROMPT-FAZ-11.md`](prompts/PROMPT-FAZ-11.md) §0 madde 5).
- **K18:** kod yorumu kısa (1–3 satır); ayrıntı kod deposunda `docs/rehber/<aynı-yol>.md`
  (`PHP-LARAVEL-SETUP.md` §2 "Açıklama nereye yazılır?").
- **Frontend deposunda CRLF tuzağı:** `git add -A` alakasız yüzlerce dosyayı sürükler; dosyalar tek tek
  eklenir ([`notes/03-FRONTEND-YAPILACAKLAR.md`](notes/03-FRONTEND-YAPILACAKLAR.md);
  [`phases/faz-14/FAZ-14-FRONTEND-COMMIT-KOMUTLARI.md`](phases/faz-14/FAZ-14-FRONTEND-COMMIT-KOMUTLARI.md)).
- **Sırlar bu depoya asla yazılmaz:** `.env`, API anahtarları, parolalar, hesap numaraları.
  Para değerindeki sır düz yazılmaz (H14, [`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md`](decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-11.md) §B).
  Kod arşivleri (`.tgz`, `.tar`, `.bundle`) `.gitignore`'dadır; içlerinde `.env` olabilir.
- Plandan kendi kararınla sapma; yanlış bulduğun kararı önce söyle ve tartış
  (`PHP-LARAVEL-SETUP.md` §2 kural 5).

## 8. Yapma

- Dosya silme: arşivle (`archive/` + bant).
- Geçmiş raporları, prompt'ları ya da kararları yeniden yazma, özetleme, "düzeltme". Taşıma yüzünden
  kırılan bağlantıyı düzeltmek serbest.
- Yeni plan, rapor ya da prompt dosyasını kök dizine bırakma.
- Bu depodan çalışırken kod depolarında değişiklik yapma; onlar salt okunurdur.
- K numarasını yeniden kullanma ya da değiştirme.
