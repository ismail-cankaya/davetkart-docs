# Faz 19.4 — `ARC-05` (backend `claude/` taşıması) commit komutları

> **Tarih:** 22 Kasım 2026 · **Kararlar:** K253, K254 · **Kayıt:** [`kayit/19-04-ARC-05.md`](kayit/19-04-ARC-05.md)
> **Dallar:** backend `fix/2026-11-22-arc-05-claude-folder` · docs `docs/2026-11-22-arc-05-claude-folder` · frontend değişmedi.
> Komutları İsmail çalıştırır. **Docs'ta sıra önemli:** 19.4.2 dosyaları **birebir** (backend blob'u) işler —
> `update-index --cacheinfo` çalışma ağacına dokunmaz; 19.4.3 bağlantı düzeltmelerini ayrı commit'ler (§A-2).

## Başlamadan

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git branch --show-current                     # fix/2026-11-22-arc-05-claude-folder
git status --short --untracked-files=all
```

```
 M README.md
 M docs/03-MIMARI-PLAN.md
 M docs/07-GELISTIRME-YOL-HARITASI.md
 M docs/08-HATA-SOZLESMESI.md
 M docs/09-TUM-FAZLAR-PLANI.md
 M docs/11-PROJE-TARIHCESI-VE-IS-AKISLARI.md
 M docs/rehber/app/Actions/Invitation/UpdateInvitationAction.md
 M docs/rehber/app/Exceptions/InvalidCredentialsException.md
 M docs/rehber/app/Http/Resources/UserResource.md
 M docs/rehber/database/migrations/2026_08_19_120100_create_timeline_events_table.md
 M docs/rehber/fazlar/FAZ-0.md
 M docs/rehber/fazlar/FAZ-1.md
 M docs/rehber/fazlar/FAZ-11.md
 M docs/rehber/fazlar/FAZ-12.md
 M docs/rehber/fazlar/FAZ-13.md
 M docs/rehber/fazlar/FAZ-14.md
 M docs/rehber/fazlar/FAZ-2.md
 M docs/rehber/fazlar/FAZ-3.md
 M docs/rehber/fazlar/FAZ-5.md
 M docs/rehber/fazlar/FAZ-6.md
 M docs/rehber/fazlar/FAZ-7-ELLE-DOGRULAMA.md
 M docs/rehber/fazlar/FAZ-9.md
 M docs/rehber/fazlar/README.md
 M docs/rehber/phpstan.md
 M docs/rehber/tests/Feature/InvitationTest.md
?? claude/README.md
?? docs/rehber/kavramlar/davetkart-docs-yollari.md
```

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git branch --show-current                     # docs/2026-11-22-arc-05-claude-folder
git status --short --untracked-files=all
```

```
 M _restructure/build_decision_index.py
 M audits/README.md
 M decisions/DECISION-INDEX.md
 M decisions/README.md
 M notes/README.md
 M phases/README.md
?? _restructure/2026-11-backend-claude-map.md
?? audits/2026-09-23-backend-review/GOZDEN-GECIRME-RAPORU.md
?? audits/2026-09-24-test-audit/TEST-DENETIMI-2026-09-24.md
?? audits/2026-10-09-code-review/GOZDEN-GECIRME-2026-10-09-BACKEND.md
?? audits/2026-10-09-code-review/GOZDEN-GECIRME-2026-10-09-FRONTEND.md
?? decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-5.md
?? decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-6.md
?? decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-7.md
?? decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-8.md
?? decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-9.md
?? notes/04-FAZ-5-FRONTEND-YAPILACAKLAR.md
?? phases/faz-05/FAZ-5-DEVIR.md
?? phases/faz-05/OKUBENI-FAZ-5.md
?? phases/faz-06/FAZ-6-DEVIR.md
?? phases/faz-07/FAZ-7-DEVIR.md
?? phases/faz-09/FAZ-9-DEVIR.md
?? phases/faz-10/FAZ-10-PLANI.md
?? phases/faz-19/FAZ-19-ARC-05-COMMIT-KOMUTLARI.md
?? phases/faz-19/HAT-C-ACIK-HATALAR.md
?? phases/faz-19/kayit/19-04-ARC-05.md
?? prompts/PROMPT-FAZ-6.md
?? prompts/PROMPT-FAZ-7-KAPANIS.md
?? prompts/PROMPT-FAZ-7-TEK-SEFERDE.md
?? prompts/PROMPT-FAZ-7.md
?? prompts/PROMPT-FAZ-8.md
?? prompts/PROMPT-FAZ-9.md
```

## 1. Backend — 19.4.4 (eski yollar)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git add README.md
git add docs/03-MIMARI-PLAN.md
git add docs/07-GELISTIRME-YOL-HARITASI.md
git add docs/08-HATA-SOZLESMESI.md
git add docs/09-TUM-FAZLAR-PLANI.md
git add docs/11-PROJE-TARIHCESI-VE-IS-AKISLARI.md
git add docs/rehber/app/Actions/Invitation/UpdateInvitationAction.md
git add docs/rehber/app/Exceptions/InvalidCredentialsException.md
git add docs/rehber/app/Http/Resources/UserResource.md
git add docs/rehber/database/migrations/2026_08_19_120100_create_timeline_events_table.md
git add docs/rehber/fazlar/FAZ-0.md
git add docs/rehber/fazlar/FAZ-1.md
git add docs/rehber/fazlar/FAZ-11.md
git add docs/rehber/fazlar/FAZ-12.md
git add docs/rehber/fazlar/FAZ-13.md
git add docs/rehber/fazlar/FAZ-14.md
git add docs/rehber/fazlar/FAZ-2.md
git add docs/rehber/fazlar/FAZ-3.md
git add docs/rehber/fazlar/FAZ-5.md
git add docs/rehber/fazlar/FAZ-6.md
git add docs/rehber/fazlar/FAZ-7-ELLE-DOGRULAMA.md
git add docs/rehber/fazlar/FAZ-9.md
git add docs/rehber/fazlar/README.md
git add docs/rehber/phpstan.md
git add docs/rehber/tests/Feature/InvitationTest.md
git commit -m "19.4.4 - docs(paths): Point old claude/ paths at their davetkart-docs homes (K254)"
git status --short
```

## 2. Backend — 19.4.5 (yönlendirme + `git rm`)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-backend-php-laravel
git add claude/README.md
git add docs/rehber/kavramlar/davetkart-docs-yollari.md
git rm claude/PHP-LARAVEL-SETUP-EK-FAZ-5.md
git rm claude/PHP-LARAVEL-SETUP-EK-FAZ-6.md
git rm claude/PHP-LARAVEL-SETUP-EK-FAZ-7.md
git rm claude/PHP-LARAVEL-SETUP-EK-FAZ-8.md
git rm claude/PHP-LARAVEL-SETUP-EK-FAZ-9.md
git rm claude/OKUBENI-FAZ-5.md
git rm claude/FAZ-5-DEVIR.md
git rm claude/FAZ-6-DEVIR.md
git rm claude/FAZ-7-DEVIR.md
git rm claude/FAZ-9-DEVIR.md
git rm claude/FAZ-10-PLANI.md
git rm claude/GOZDEN-GECIRME-RAPORU.md
git rm claude/TEST-DENETIMI-2026-09-24.md
git rm claude/GOZDEN-GECIRME-2026-10-09-BACKEND.md
git rm claude/GOZDEN-GECIRME-2026-10-09-FRONTEND.md
git rm claude/PROMPT-FAZ-6.md
git rm claude/PROMPT-FAZ-7.md
git rm claude/PROMPT-FAZ-7-KAPANIS.md
git rm claude/PROMPT-FAZ-7-TEK-SEFERDE.md
git rm claude/PROMPT-FAZ-8.md
git rm claude/PROMPT-FAZ-9.md
git rm claude/Notlar/04-FAZ-5-FRONTEND-YAPILACAKLAR.md
git commit -m "19.4.5 - docs(claude): Move the claude/ folder to davetkart-docs and leave a redirect (K254)"
git status --short
```

## 3. Docs — 19.4.1 (eşleme)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add _restructure/2026-11-backend-claude-map.md
git commit -m "docs(restructure): Add the backend claude/ to davetkart-docs path map"
git status --short
```

## 4. Docs — 19.4.2 (birebir kopyalar + klasör README'leri)

Her satır: backend'deki blob kimliği (kopyayla aynı) → yeni yol. Çalışma ağacındaki 6 dosya bağlantısı düzeltilmiş hâlde kalır.

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git update-index --add --cacheinfo "100644,6d15b4fbddb3511ea79b7574b5fb57c4d90d4eec,decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-5.md"
git update-index --add --cacheinfo "100644,a60bf5883115441fc3b71520c971693a8fa1dda0,decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-6.md"
git update-index --add --cacheinfo "100644,d2472f84256290be715485b13d4fa3c7dba037f7,decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-7.md"
git update-index --add --cacheinfo "100644,94cd148db617256dfc32fb01723e9bea006dd3f2,decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-8.md"
git update-index --add --cacheinfo "100644,289653ec85faac90643bd50a44282c5ef2853f9c,decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-9.md"
git update-index --add --cacheinfo "100644,374a9a07ec9c597736057cfe15a7505a2872e8b4,phases/faz-05/OKUBENI-FAZ-5.md"
git update-index --add --cacheinfo "100644,9731f436ef509b2fa63b88f41de59909a44aa999,phases/faz-05/FAZ-5-DEVIR.md"
git update-index --add --cacheinfo "100644,32145bcecae37b39e73f6c5c648c749813616ff3,phases/faz-06/FAZ-6-DEVIR.md"
git update-index --add --cacheinfo "100644,c6a55539dc8d39df8e92bb8499ed6776cf72316d,phases/faz-07/FAZ-7-DEVIR.md"
git update-index --add --cacheinfo "100644,39fccd54759d5b0c6a74567120058747f033c248,phases/faz-09/FAZ-9-DEVIR.md"
git update-index --add --cacheinfo "100644,838f6847b9a6c34033d3d68ca998a519033ae4cd,phases/faz-10/FAZ-10-PLANI.md"
git update-index --add --cacheinfo "100644,3eabf8f546fb5b0c9b8b31707d73309e5312e51c,audits/2026-09-23-backend-review/GOZDEN-GECIRME-RAPORU.md"
git update-index --add --cacheinfo "100644,a8bbacce663ba138fbd3a923d6e7876e47fc43a9,audits/2026-09-24-test-audit/TEST-DENETIMI-2026-09-24.md"
git update-index --add --cacheinfo "100644,d626521a7d4e09904e4ee75f07468175dd672ead,audits/2026-10-09-code-review/GOZDEN-GECIRME-2026-10-09-BACKEND.md"
git update-index --add --cacheinfo "100644,1788a99566f399bd22c67cd62ad7a3afc26994bf,audits/2026-10-09-code-review/GOZDEN-GECIRME-2026-10-09-FRONTEND.md"
git update-index --add --cacheinfo "100644,e6441d4eaf6fa29c3eccd88eb0f08d6a2e252b8c,prompts/PROMPT-FAZ-6.md"
git update-index --add --cacheinfo "100644,c1f7981d04ab5829625cb3b60c1a46a56b47b157,prompts/PROMPT-FAZ-7.md"
git update-index --add --cacheinfo "100644,abfdb89302eb098f0a68540833848a8c72f884ed,prompts/PROMPT-FAZ-7-KAPANIS.md"
git update-index --add --cacheinfo "100644,8f58ec86c66a772d5c94d020e72aa84ef30710f2,prompts/PROMPT-FAZ-7-TEK-SEFERDE.md"
git update-index --add --cacheinfo "100644,08a1a6126b8e02c2410f41d1e1ebfca1c94747eb,prompts/PROMPT-FAZ-8.md"
git update-index --add --cacheinfo "100644,387f639a55cdc9a504dbe5ac250c63ad120c6db2,prompts/PROMPT-FAZ-9.md"
git update-index --add --cacheinfo "100644,d6565eea9640eda6e6a2432ec08f75520ac85928,notes/04-FAZ-5-FRONTEND-YAPILACAKLAR.md"
git add decisions/README.md
git add audits/README.md
git add phases/README.md
git add notes/README.md
git commit -m "docs(restructure): Copy the backend claude/ files verbatim into their new homes"
git status --short   # beklenen: 6 kopya + indeks + betik " M", kayıt dosyaları "??"
```

## 5. Docs — 19.4.3 (bağlantılar + indeks)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add phases/faz-05/FAZ-5-DEVIR.md
git add phases/faz-05/OKUBENI-FAZ-5.md
git add phases/faz-06/FAZ-6-DEVIR.md
git add decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-5.md
git add prompts/PROMPT-FAZ-7.md
git add prompts/PROMPT-FAZ-7-TEK-SEFERDE.md
git add decisions/DECISION-INDEX.md
git add _restructure/build_decision_index.py
git commit -m "docs(decisions): Fix moved links and point K49-K106 sources at the moved addenda (K253)"
git status --short
python -I _restructure/build_decision_index.py --check   # beklenen: çıkış 0
```

## 6. Docs — 19.4.6 (kayıt)

```powershell
cd D:\Projects\davetkart-hat-c\davetkart-docs
git add phases/faz-19/kayit/19-04-ARC-05.md
git add phases/faz-19/HAT-C-ACIK-HATALAR.md
git add phases/faz-19/FAZ-19-ARC-05-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add the ARC-05 record, commit commands and the lane C open issues (K253, K254)"
git status --short
```

## 7. Birleştirme (ana klasör)

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-22-arc-05-claude-folder -m "Merge ARC-05 into faz-19-audit-fixes"
git status --short
```

```powershell
cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-22-arc-05-claude-folder -m "Merge ARC-05 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `19-CAKISMA.md`. ⚠️ Backend `composer check` bu daldan bağımsız nedenle kırmızı ([`HAT-C-ACIK-HATALAR.md`](HAT-C-ACIK-HATALAR.md) #1).
