# Yayın sırası ve sürüm etiketi — çalıştırma kitabı

> **Tarih:** 16 Kasım 2026 · **Kaynak:** `AUD-2026-11-12` → `OPS-01` (Faz 18.1) · **Kararlar:** K146–K150
> ([`decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md`](../../decisions/addenda/PHP-LARAVEL-SETUP-EK-FAZ-18.md))
> **Ne bu:** Bir sürümü yayına alırken izlenen sıra. Sunucu kurulumu [`YAYIN-PLANI.md`](YAYIN-PLANI.md)'de,
> betiklerin ayrıntısı backend deposunda `docs/rehber/deploy/deploy.md` ve `deploy-frontend.md`'de.
> ⚠️ **B7:** §3–§5'teki sunucu ve etiket komutları **yazıldı, çalıştırılmadı.** Betiklerdeki etiket bloğu
> yerelde sahte `git` ile denendi; sunucuda ilk kez `v1.1.0` yayınında koşacak.

## 1. İki kural

| # | Kural | Neden |
|---|---|---|
| **K148** | **Önce backend, sonra frontend.** Tersine sıra yasak. | Plan kuralını sunucu uygular, arayüz gösterir. Arayüz önce çıkarsa "Gold+" dediği şablonu sunucu henüz korumaz: Standart planla premium şablon yayınlanır (şablon başına 150 ₺). |
| **K149** | **Sürüm etiketle izlenir, dalla değil.** İki depo aynı etiketi taşır: `vMAJOR.MINOR.PATCH`. | "Hangi iki commit birlikte doğrulandı?" sorusunun cevabı dal olamaz; dal her commit'te ilerler. |

Etiket "hangi commit" sorusunu, sözleşme "kurallar aynı mı" sorusunu cevaplar. İkisi ayrı denetimdir:

```
backend config ─[plans:export]→ contracts/plan-rules.json ─(kopya)→ frontend src/contracts/plan-rules.json
      composer check: plans:export --check                      npm run check: verify:plans
```

**Sürüm numarası:** `MAJOR` API sözleşmesini kıran değişiklik · `MINOR` yeni özellik, şablon ya da plan
kuralı · `PATCH` düzeltme. Yalnızca bir depo değişse bile **iki depo da** yeni etiketi alır.
Faz 18 sonu: `v1.1.0`.

## 2. Yayın öncesi kontrol listesi (yerelde, İsmail)

Hepsi yeşil olmadan etiket atılmaz.

| # | Kontrol | Komut | Beklenen |
|---|---|---|---|
| 1 | Backend kalite kapısı | `composer check` | Son satır `"result":"passed"`; zincirde `plans:export --check` var |
| 2 | Backend bağımlılık taraması (`SEC-07`) | `composer audit` | Açık yok. 🔴 16 Kasım'da **kırmızı**; etiketten önce kapanmalı |
| 3 | Frontend kalite kapısı | `npm ci` → `npm run check` | Çıkış 0; zincirde `verify:plans` var |
| 4 | Sözleşme kopyası güncel | aşağıdaki blok | `AYNI` |
| 5 | İki depoda aynı etiket | `git describe --tags --exact-match main` (iki depoda) | İkisi de aynı `vX.Y.Z` |
| 6 | Yedek alınıyor (`OPS-02`) | Faz 18.2 kapanınca buraya yazılacak | Son gece dökümü S3'te |

```powershell
# 4 — frontend'in kopyası backend'in sözleşmesiyle aynı mı? (satır sonu farkını yok sayar)
cd D:\Projects\davetkart
$fark = Compare-Object (Get-Content davetkart-backend-php-laravel\contracts\plan-rules.json) `
                       (Get-Content davetkart-frontent\src\contracts\plan-rules.json)
if ($fark) { 'FARKLI'; $fark } else { 'AYNI' }
```

`FARKLI` çıkarsa kopyayı elle düzeltme: kural backend'de değişir (`config/davetkart.php` →
`php artisan plans:export`), kopya oradan gelir, sonra `npm run verify:plans`. Hangi şablonun hangi
planda olduğu bir fiyat kararıdır.

## 3. Etiket komutları (İsmail çalıştırır)

Önkoşul: iki depoda `main`, kontrol listesinden geçen commit'te. `main`'e alma komutlarını faz
kapanış prompt'u verir (Faz 18 için 18.6 §11).

```powershell
# Backend
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git switch main
git log --oneline -1                                  # yayınlanacak commit bu mu?
git tag -a v1.1.0 -m "v1.1.0 - Faz 18 audit fixes (AUD-2026-11-12)"
git describe --tags --exact-match main                # v1.1.0
```

```powershell
# Frontend
cd D:\Projects\davetkart\davetkart-frontent
git switch main
git log --oneline -1
git tag -a v1.1.0 -m "v1.1.0 - Faz 18 audit fixes (AUD-2026-11-12)"
git describe --tags --exact-match main                # v1.1.0
```

`-a` açıklamalı etiket üretir: kim, ne zaman, neden bilgisi etiketin içinde kalır. Etiketler burada
yalnızca **yereldedir**; itme §4'te, sırayla.

**Öneri (karar İsmail'in):** `v1.1.0`'dan önce, bugün sunucuda çalışan iki commit'i `v1.0.0` diye
etiketle. Yoksa geri dönülecek bir etiket olmaz (§5). Hangi commit'lerin yayında olduğuna sunucudan
bak, `main`'den tahmin etme:

```bash
# sunucuda, 'deploy' ile
git -C /var/www/davetkart/backend rev-parse --short HEAD
git -C /var/www/davetkart/frontend rev-parse --short HEAD
```

## 4. Dağıtım sırası (K148)

### 4.1 Backend

```powershell
# yerelde
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git push origin main
git push origin v1.1.0
```

```bash
# sunucuda, 'deploy' ile
cd /var/www/davetkart/backend
bash deploy/deploy.sh
```

Günlükte aranacak satırlar:

```
==> Surum: <kimlik> (v1.1.0)
==> Backend bitti: <önceki> -> <kimlik> (v1.1.0)
```

`(etiketsiz)` ve `UYARI: … etiketli bir surum degil` görürsen etiket itilmemiştir. Deploy durmaz
(K149); frontend'e geçmeden önce etiketi it.

`deploy.sh` sonunda frontend betiğini de çağırır. Frontend `main`'i henüz itilmediği için o adım
yayındaki siteyi aynı commit'ten yeniden derler; zararsızdır.

### 4.2 Ara kontrol: yeni kural sunucuda etkin mi?

```bash
cd /var/www/davetkart/backend
git describe --tags --exact-match HEAD                          # v1.1.0
sudo -n -u www-data /usr/bin/php artisan plans:export --check   # "Plan kurallari sozlesmesi guncel."
grep -c '": "gold"' contracts/plan-rules.json                   # v1.1.0 için 34 (32 şablon + 2 modül)
```

`plans:export --check` önbelleğe alınmış config'i sözleşme dosyasıyla karşılaştırır. Yeşilse sunucunun
uyguladığı kurallar bu commit'in sözleşmesidir. Kırmızıysa **dur**, frontend'i yayınlama.

### 4.3 Frontend

```powershell
# yerelde
cd D:\Projects\davetkart\davetkart-frontent
git push origin main
git push origin v1.1.0
```

```bash
# sunucuda: yayınlanacak frontend'in sözleşme kopyası, yayındaki backend'inkiyle aynı mı?
cd /var/www/davetkart/frontend
git fetch origin
git show origin/main:src/contracts/plan-rules.json \
  | cmp - /var/www/davetkart/backend/contracts/plan-rules.json && echo "sozlesme ayni"

bash /var/www/davetkart/backend/deploy/deploy-frontend.sh
```

`cmp` fark bulursa (ya da `sozlesme ayni` yazmazsa) frontend'i yayınlama: backend eski kalmıştır ya da
kopya bayattır. Günlükte aranacak satır:

```
==> [frontend] Surum: <kimlik> (v1.1.0) | backend: v1.1.0
```

`UYARI: frontend v1.1.0, backend etiketsiz: iki depo ayni etikette degil` görürsen sıra bozulmuştur:
§4.1'e dön.

> Tek `bash deploy/deploy.sh` de sırayı korur (önce backend, sonra frontend), ama ara kontrolü atlar.
> Plan kuralı değiştiren sürümlerde iki adımlı yolu kullan.

## 5. Geri alma: önceki etikete dönüş

🔴 **Sıra tersine döner: önce frontend, sonra backend.** Geri alırken de arayüz sunucunun uyguladığından
fazlasını söylememeli.

**5.1 Yalnızca frontend, hemen** (kod değişmez; bir önceki derleme geri gelir):

```bash
cd /var/www/davetkart/frontend
mv dist dist.bad && mv dist.old dist
```

**5.2 Önceki etikete tam dönüş.** Sunucu her zaman `main`'i çeker (Y8.2a) ve `deploy.sh` her çalıştığında
`git pull` yapar. Bu yüzden sunucuda `git reset --hard <etiket>` kalıcı bir geri alma **değildir**:
betik bir sonraki çalıştırmada yeni sürüme geri sarar. Geri alma `main` üzerinden, yeni bir commit'le
yapılır; geçmiş silinmez, zorla itme gerekmez.

```powershell
# yerelde; önce frontend, sonra aynı blok backend deposu için
cd D:\Projects\davetkart\davetkart-frontent
git switch main
git restore --source=v1.0.0 --staged --worktree -- .   # ağacı v1.0.0 hâline getirir
git commit -m "revert: Roll back to v1.0.0"
git diff --stat v1.0.0 HEAD                            # BOŞ olmalı: ağaç v1.0.0 ile aynı
git tag -a v1.1.1 -m "v1.1.1 - Roll back to v1.0.0"
git push origin main
git push origin v1.1.1
```

Sunucuda sıra: `bash /var/www/davetkart/backend/deploy/deploy-frontend.sh` → sonra backend için aynı blok
ve `bash deploy/deploy.sh`.

Geri almadan önce bil:

- **Göçler geri alınmaz.** Yeni şemayı eski kod genelde taşır (sütun eklemeleri); silme ya da yeniden
  adlandırma içeren göç varsa önce onu değerlendir (`deploy.md` §4).
- **Veri geri alınmaz.** Yeni sürümde eklenen bir şablonla yayınlanmış davetiye varsa eski frontend o
  şablonu tanımaz. Geri almadan önce say:
  `sudo -n -u www-data /usr/bin/php artisan tinker --execute="echo App\Models\Invitation::whereIn('preset_id', ['<yeni-kimlik>'])->count();"`

## 6. Dağıtım sonrası duman testi

Faz 18.6'da (`SEC-04`) eklenecek.

## 7. Bu sıra neyi önlemez?

- **Etiketsiz yayın.** Betik uyarır, durdurmaz (K149). İlk sürümde katı kural fazla bulundu; karar
  ileride sıkılaştırılabilir.
- **`deploy-frontend.sh`'ın tek başına, eski backend'in üstüne çalıştırılması.** Etiket uyarısı ve §4.3'teki
  `cmp` bunu görünür yapar ama betik kendiliğinden durmaz. Öneri (karar bekliyor): `cmp` denetimini
  `deploy-frontend.sh`'a koyup fark varsa derlemeden önce durdurmak.
- **Bayat kopya.** `verify:plans` frontend'i kendi kopyasıyla karşılaştırır, backend deposuna bakmaz
  (hata kataloğuyla aynı desen). Kopyanın güncelliğini §2'deki 4. kontrol ve §4.3'teki `cmp` yakalar.
