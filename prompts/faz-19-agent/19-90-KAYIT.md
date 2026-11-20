# 19.90 — Hat kayıtlarını birleştir (paylaşılan dosyalar)

> **Ne zaman:** üç hattın bütün bulguları (ARC-03 hariç) `faz-19-audit-fixes`'e ve docs entegrasyon dalına birleştikten sonra. **Hat C** klasöründe. **Model:** `/model sonnet` · **Çağrı bütçesi:** 40 · Kurallar: `BAGLAM.md`.
> Bu prompt §2'deki "paylaşılan dosyalara dokunma" kuralının **tek istisnasıdır**.

## Önkoşul

- Takip tablosundaki 26 bulgunun (ARC-03 hariç) dalları birleşmiş: kod `git branch --merged faz-19-audit-fixes --list "fix/*"`, docs `git branch --merged docs/2026-11-20-faz-19-audit-fixes --list "docs/*"`; eksik varsa listele ve dur.
- Dallar: backend `fix/<YYYY-MM-DD>-faz19-records`, docs `docs/<YYYY-MM-DD>-faz19-records` (entegrasyon dallarından).

## Adımlar (girdi yalnızca `phases/faz-19/kayit/*.md`; bulgu ve kod dosyalarını açma)

1. **Docs** — kayıt dosyalarını numara sırasıyla oku (her biri ≤60 satır):
   - `decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-19.md`: bütün K'lar (19.1'inkiler dahil, varsa koru).
   - `decisions/DECISION-INDEX.md`: K satırları sıralı; kullanılmayan hat aralıkları için tek satır not ("K… – K… ayrılmıştı, kullanılmadı"); "Sıradaki boş numara" = kullanılan en büyük + 1 (ARC-03 bu numarayı alacak); eski kararların durum notları.
   - `CHANGELOG.md` (tek tarihli başlık, bulgu başına satır), `phases/faz-19/README.md` (durum `birleşti`, dal, K), `prompts/README.md` (`faz-19-agent/` klasörü satırı yoksa).
   - `ARC-01`'in `python -I _restructure/build_decision_index.py --check` → 0.
2. **Backend** — `docs/rehber/fazlar/FAZ-19.md`: başlık + 28 bulgu tablosu + her kayıt dosyasının "Faz bölümü" (19.1'in mevcut bölümünü koru) · `docs/rehber/fazlar/README.md` satırı. Kod değişmez; `composer check` gerekmez, `vendor/bin/pint --test` yeter.
3. Kayıt dosyalarını silme; başlarına "Birleştirildi → 19.90" notu.
4. Commit komutları `phases/faz-19/FAZ-19-KAYIT-COMMIT-KOMUTLARI.md`; rapor ≤25 satır.
