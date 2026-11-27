# Faz 23 — v1.4 Frontend: Ana Sayfa Vitrin Sahnesi (Plan)

> **Durum:** 🔧 Yön A kodlandı (23.1–23.4, §0.2) · kod dalı push edildi · `main`'e birleştirme ve kalan adımlar bekliyor.
> **Tarih:** 27 Kasım 2026 · **Sürüm:** v1.4 (frontend) · **Sıra:** Faz 22 → `v1.3` yayını → Faz 23.
> **Kod dalı:** `faz-23-v1.4-frontend`, frontend `faz-22-release-prep` (`v1.3` hazırlığı) @ `b0a07dc` ucundan açıldı (27 Kasım). Faz 22'ye gelen yeni commit'ler bu dala `merge` ile alınır.
> **Sürüm notu:** İlk taslakta sürümler bir eksik yazılmıştı (27 Kasım, İsmail düzeltti): Faz 22'nin sonu `v1.3`, Faz 23 `v1.4`. Docs dalının adındaki `v1.3` değişmedi.
> **Docs dalı:** `docs/2026-11-27-faz-23-v1.3-frontend-plan` (`docs/2026-11-27-faz-21-backlog` ucundan; `main` Faz 18'de kaldığı için).
> **Analiz tabanı:** frontend `faz-21-backlog` @ `e28b599` (21.18). Faz 22 ve `v1.3` kodu görülmedi; dal açılınca §2 yeniden ölçülür.

## 0. Özet

Ana sayfada hero ile tasarım vitrini (`PreviewSection`) arasına **kısa, kaydırmaya bağlı bir "vitrin sahnesi"** eklenir.
Ortada büyük bir telefonda ana davetiye, iki yanda en güzel davetiyeleri gösteren telefonlar olur. Kaydırdıkça
telefonlar hareket eder; sahne Apple ürün tanıtımlarındaki gibi **sabitlenip (pin) kaydırmayla oynatılır**, ama
1–1,5 ekran boyunu geçmez. Amaç: ziyaretçi **hiçbir şeye tıklamadan** davetiyelerin gerçek, açılmış halini görsün.

Üç tasarım yönü (§5), önerilen: **A — Üçlü Sahne**. Telefon içerikleri canlı şablon değil, **önceden üretilmiş
görsel/video** (§6). Mevcut önizleme bölümü ve stüdyo akışı korunur.

## 0.1 İlk geri bildirim (27 Kasım 2026)

- İsmail **A** ve **C**'yi beğendi: **A** vitrin sahnesi için daha mantıklı; **C** ileride ana sayfanın daha alt bölümlerinde
  kullanılabilir (Faz 23 kapsamı dışında, ayrı karar). **B** öne çıkmadı.
- Kaydırmalı maket (A, B, C; gerçek şablon kapaklarıyla): https://claude.ai/artifact/2ExNJ3W8Rhn1i5MubgWWXk (özel bağlantı,
  yalnızca İsmail açabilir). Kesin seçim (S1) maketten sonra.

## 0.2 Yön A kodlandı (27 Kasım 2026)

- İsmail: A ve B favori; **A** ile devam, gerekirse B'ye geçiş. Telefon, tablet ve bilgisayar uyumu şart.
- Faz 22 = `v1.3` hazırlığı; Faz 23 dalı `faz-22-release-prep`'ten açıldı (İsmail onayı). Commit'ler:

| Commit | İçerik |
|---|---|
| `5843087` 23.1 | `src/components/ui/PhoneFrame.tsx` |
| `4bd8b83` 23.2 | `scripts/showcase/capture.ts`, `showcaseSlides.ts`, `public/showcase/*.webp` (3 görsel, 50–63 kB), kılavuz |
| `19a022a` 23.3 | Vitrin sahnesi (`src/components/home/showcase/`), `HomePage`/`Hero`/`useLenis` bağlantısı, 10 dil, kılavuz |
| `105169f` 23.4 | `e2e/home-showcase.spec.ts`, Playwright `home` projesi |

- Cihaz modları: telefon (< 640 px, 170 svh), tablet (640–1023 px, 200 svh), masaüstü (≥ 1024 px, 220 svh), sabit
  (hareketi azalt ya da yükseklik < 560 px; sabitleme yok). Orta Düğün "Dilek Fenerleri", yanlar "Kelebek Bahçesi" ve
  Nişan "Koi Havuzu". Telefon içerikleri gerçek ekran görüntüsü; orta telefon videosu ertelendi.
- Doğrulama: `npm run check` 0 (ilk yükleme 712,2 → 713,6 kB, bütçe 720; sahne parçası 6 kB); yeni e2e 5/5 (geliştirme
  sunucusuna karşı, geçici yapılandırma); axe bölümde 0 ihlal. Tüm e2e paketi **koşmadı** (backend + PowerShell ister).
- Plandan sapmalar: `PhoneFrame` yeni yazıldı, `DeviceSimulator` dokunulmadı (cihazlar arası geçiş yapıyor). Önizleme
  başlığının kısaltılması (23.5) ve hero (S5) yapılmadı.
- Açık: orta telefon videosu, S5 hero, önizleme başlığı, final animasyonu (23.8). Karar numarası alınmadı.

## 1. İstek (İsmail, 27 Kasım 2026)

> Ana sayfada ilk açılan sayfadan sonra aşağıya kaydırdığımızda direk davetiye oluştur kısmı geliyor. Ancak müşteri
> önizleme kısmına tıklamadığı taktirde davetiyeleri göremiyor. […] İlk kısmından aşağı kaydırdığımızda sağ ve solda
> telefonlarda şu anlık en güzel olan davetiyelerin resimleri telefonda olacak şekilde aşağı kaydırdıkça hareket eden,
> orta kısımda da cihaza göre daha çok ana davetiyeyi gösterecek şekilde bir tasarım düşünüyorum. Konsept olarak apple
> iphone tanıtımları gibi bir kısım düşünüyorum. Çok uzun olmamasını da istiyorum. Ayrıca modern ve profesyonel olmalı,
> standart yapılan ai vibe vermemeli.

Gereksinimlere bölünmüş hali:

| # | Gereksinim | Ölçüt |
|---|---|---|
| G1 | Hero'dan sonraki ilk şey davetiyelerin **kendisi** olsun | İlk kaydırmada en az 3 davetiye telefon ekranında, açılmış halde görünür; tıklama gerekmez |
| G2 | Ortada büyük telefon, ana davetiye | Masaüstünde orta telefon yanlardan belirgin büyük (≈1,25×); mobilde ekranın odağı |
| G3 | Sağ ve solda telefonlar, kaydırdıkça hareket | Hareket kaydırma ilerlemesine bağlı (zamana değil); geri kaydırınca geri oynar |
| G4 | Apple tanıtımı hissi | Sabitlenen sahne, büyük tipografi, bol boşluk, ürünün kendisi kahraman |
| G5 | Kısa | Sahnenin kaydırma maliyeti masaüstünde ≤ 1,5 ekran boyu, mobilde ≤ 1 ekran boyu |
| G6 | Modern, profesyonel, "AI vibe" yok | §4'teki yap/yapma listesine uyar; gözden geçirmede liste tek tek işaretlenir |
| G7 | Mevcut kalite kapıları bozulmaz | `npm run check` 0, e2e yeşil, `perf` CLS < 0,1, ilk yükleme paketi bütçede (720 kB) |

## 2. Mevcut durum (kod ölçümü)

Ana sayfa sırası (`src/pages/HomePage.tsx`):

| Sıra | Bölüm | Dosya | Not |
|---|---|---|---|
| 1 | Hero (video arka plan, başlık, 2 CTA, 4 sayaç, "Keşfet") | `components/home/Hero.tsx` | `min-h-[100dvh]`; "Keşfet" → `#animasyon-ve-onizleme` |
| 2 | Önizleme: 5 kapak kartı + "Tüm tasarımlar" + AI kartı · canlı cihaz simülatörü | `components/preview/PreviewSection.tsx`, `TemplateGrid.tsx`, `DeviceSimulator.tsx` | Tembel parça (FE-10) |
| 3 | "Kendi Davetiyeni Oluştur" bandı | `HomePage.tsx` → `CreateCtaBanner` | |
| 4 | Özellikler | `components/home/Features.tsx` | Bilerek ertelenmez (uzun görev ölçümü, yorum `HomePage.tsx`) |
| 5 | Canlı LCV paneli (demo) | `components/rsvp/LiveRsvpPanel.tsx` | `DeferredSection` |
| 6 | Yorumlar | `components/home/Testimonials.tsx` | `DeferredSection` |

İsteğin kökü (gözlem → kod):

- **Kartlar davetiyenin kendisi değil.** `TemplateGrid` kartları kapak görselinin `h-36`/`h-48` kırpılmış hali;
  yatay kart, dikey davetiyeyi göstermez.
- **Simülatör tek şablon gösterir ve davetiye kapalı açılır.** `DeviceSimulator showcase` canlı `TemplateRenderer`
  çizer; çoğu şablon zarf/mühür ile başlar (`templates/shared/Envelope.tsx`). Ziyaretçi içeriği görmek için zarfa
  ya da bir karta tıklamak zorunda.
- **Hero snap'i doğrudan önizlemeye iner.** `hooks/useLenis.ts` `SNAP_SECTION_ID = 'animasyon-ve-onizleme'`:
  masaüstünde tekerlek ile hero'nun altından önizleme bölümüne kayar. Yeni sahne araya girince hedef değişmeli (§7).

Yeniden kullanılabilir varlıklar:

| Varlık | Yer | Kullanım |
|---|---|---|
| Telefon geometrisi (9:19, çerçeve 42 px, ekran 26 px, kenar 12 px) | `DeviceSimulator.tsx` `DEVICE_SPECS.phone` | `ui/PhoneFrame` olarak dışarı alınır (23.1) |
| Öne çıkan 5 şablon | `src/data.ts` `FEATURED_TEMPLATES` | Sahnenin varsayılan listesi |
| Örnek içerik (isimler, tarih, mekân) | `data.ts` `SHOWCASE_CONTENT`, `utils/showcase.ts` | Ekran görüntülerinde aynı içerik |
| Hareket token'ları | `utils/motion.ts` (`ease.out`, `duration.stage`) | Yeni eğri icat edilmez |
| Ekran görüntüsü aracı | `scripts/onizleme/cek.ts` (headless Chrome, 360/768/1280) | Telefon görsellerini üretme hattına temel (23.2) |
| "Görünürken oynat" ve "load'dan sonra indir" | `Hero.tsx` `usePlayWhileVisible`, `useAfterLoad` (FE-53) | Video telefonlar için aynı desen; ortak hook'a taşınır |

Kısıtlar (mevcut kapılar):

- `verify:bundle`: ilk yükleme ≤ 720 kB ham. Sahne ilk pakete **girmez**, tembel parça olur.
- `npm run perf`: kısıtlı mobilde CLS < 0,1. Sabitlenen sahne yüksekliğini baştan ayırmalı.
- `verify:i18n`: yeni metinler 10 dilin hepsinde (`tr en de es fr pt ru ar hi zh`); `ar` sağdan sola.
- Mevcut 🔴 kural: giriş animasyonları `transform` dizesi + `opacity` (compositor), bağımsız `x/y/scale` değil
  (`TemplateGrid.tsx` başlık yorumu). Kaydırmaya bağlı değerler de yalnızca bu iki özelliği yazar.

## 3. Hedef akış

```
Hero (100dvh)
  └─ "Keşfet" / snap
Vitrin sahnesi (YENİ)        ← sabitlenir, kaydırmayla oynar, ≤ 1,5 ekran
  └─ "Tüm tasarımları keşfet"
Önizleme (mevcut, başlığı sadeleşir)
CTA bandı → Özellikler → LCV → Yorumlar (değişmez)
```

Sahne önizlemenin yerini **almaz**: sahne "görün, beğenin" der; önizleme "seçin, deneyin" der. Önizlemenin mobil
başlığı ("Davetiyenizi Görüntüleyin") sahneyle tekrar eder; 23.5'te kısaltılır.

## 4. "AI vibe" vermemesi için yap / yapma

Bugünkü sayfada da bulunan kalıplar **⚠️** ile işaretli; Faz 23'ün kapsamı yalnızca yeni sahne, hero'ya dokunmak
ayrı bir karar (§10, S5).

| Yapma | Neden | Yerine |
|---|---|---|
| Parıltı ikonu (✨ `Sparkles`), "Yeni / AI" rozeti başlık üstünde ⚠️ | Hazır şablon imzası | Rozet yok; başlık kendi başına durur |
| Mor-mavi degrade, bulanık renk lekeleri, "glow" | 2023–25 yapay zekâ sitelerinin varsayılanı | Markanın krem + yeşil + altın paleti, düz zemin |
| Her başlıkta kelime kelime bulanıklıktan çıkma ⚠️ | Tekrarlandıkça şablon hissi | Sahnede tek bir büyük başlık, tek bir yumuşak giriş |
| Butonda sürekli parıltı (`animate-shimmer`) ⚠️ | Dikkat dilenmesi | Sakin buton; hover'da yalnızca renk ve 1–2 px yükselme |
| Cam efekti (glassmorphism) her yüzeyde | Derinlik taklidi | Gerçek, katmanlı, düşük opaklıklı gölge (telefonlarda) |
| Belirsiz üstünlük cümleleri ("Yeni nesil deneyim") | Her ürün için yazılabilir | Somut cümle: ne olduğu, kime, ne kadar sürede |
| 3 sütun ikon + başlık + paragraf kartı | En tanıdık "AI landing" bloğu | Sahnede kart yok; ürün görüntüsü + bir cümle |
| Zamanla kendiliğinden dönen karuseller | Kullanıcı kontrolü yok | Hareketi kaydırma sürer; durunca sahne durur |
| Emoji | Profesyonellik | — |

Yap:

1. **Ürün kahraman:** ekranın en büyük öğesi gerçek davetiye görüntüsü.
2. **Tipografi disiplini:** mevcut serif + sans ikilisi; başlık büyük (masaüstü 64–80 px), sıkı satır aralığı,
   tek vurgu kelimesi italik. Yeni font eklenmez (`verify:fonts`).
3. **Tek vurgu rengi:** `brand` yeşili; altın yalnızca ince ayrıntıda.
4. **Boşluk:** sahnede en fazla 1 başlık, 1 alt cümle, 1 bağlantı.
5. **Hassas hareket:** tek eğri ailesi (`ease.out`, `inOut`), hareket mesafeleri ölçülü (yan telefonlar ≤ 18°
   eğim, ≤ 120 px dikey kayma), hiçbir şey "zıplamaz".
6. **Kopya önerileri (seçim §10, S6):**
   - "Davetiyeniz artık *cepte*." / alt: "Düğünden sünnete, her tasarım telefonda kusursuz açılır."
   - "Kâğıttan değil, *ekrandan* açılır."
   - "Bir bağlantı. *Bütün* misafirleriniz."

## 5. Tasarım yönleri

Üçü de aynı teknik temeli kullanır (§6, §7); fark koreografide. Süreler kaydırma ilerlemesi (0 → 1) cinsinden.

### A — Üçlü Sahne (önerilen)

İsteğe en yakın, en kısa yön.

```
 ilerleme 0.0            0.4                    1.0
 ┌───────────────┐   ┌───────────────┐   ┌──────────────────────┐
 │   BAŞLIK      │   │   BAŞLIK ↑    │   │  ┌──┐  ┌────┐  ┌──┐   │
 │   ┌────┐      │   │ ┌──┐┌────┐┌──┐│   │  │K │  │ D  │  │N │   │
 │   │ D  │      │ → │ │K ││ D  ││N ││ → │  │  │  │    │  │  │   │
 │   │    │      │   │ └──┘│    │└──┘│   │  └──┘  │    │  └──┘   │
 │   └────┘      │   │     └────┘    │   │  "Tüm tasarımları →"  │
 └───────────────┘   └───────────────┘   └──────────────────────┘
 D = Düğün (orta, büyük) · K = Kına · N = Nişan
```

- **0.0–0.35:** Başlık ve orta telefon görünür. Yan telefonlar orta telefonun arkasında, %85 boyutta, saydam.
- **0.35–0.75:** Yan telefonlar sola ve sağa açılır; hafif içe eğilir (`rotateY` ±12–18°) ve biraz aşağıda durur.
  Aynı anda **her telefonun ekranındaki davetiye içeriği yukarı kayar**: davetiye telefonun içinde kaydırılıyormuş
  gibi görünür (Apple'ın ekran içi kaydırma tekniği).
- **0.75–1.0:** Başlık yukarı çekilip söner, altta "Tüm tasarımları keşfet" bağlantısı belirir. Sabitleme biter,
  sayfa önizlemeye akar.
- **Mobil (< 1024 px):** Orta telefon ekran genişliğinin ~%62'si; yan telefonlar kenardan yarısı taşacak şekilde
  görünür. Sabitleme kısa (sahne kabı 160 svh) ya da yok (S4).
- **Artı:** Odak net, kısa, isteğe birebir. Üretilecek varlık az (3 şablon).
- **Eksi:** Yalnızca 3 şablon görünür; çeşitlilik sahnede değil önizlemede.
- **İş yükü:** Orta.

### B — Akan Sütunlar

Çeşitliliği öne çıkarır.

- Ortada büyük telefon sabit durur. Solda ve sağda **dikey telefon sütunları** (her biri 3 telefon) kaydırmayla
  **zıt yönlere** akar: sol yukarı, sağ aşağı.
- Orta telefonun içeriği kaydırmanın üç eşiğinde değişir (Düğün → Kına → Sünnet). Altında ince bir kategori
  göstergesi olur.
- **Mobil:** Sütunlar telefonun arkasında, düşük opaklıkta, yatay şerit olarak akar.
- **Artı:** 7 şablona kadar görünür; "çok tasarım var" mesajı güçlü.
- **Eksi:** Ekran kalabalıklaşır, "sakin ve premium" hissi zayıflar. Varlık sayısı ve indirme ağırlığı ~2,5×.
  İçerik değişimi bir tür "slayt" hissi verir.
- **İş yükü:** Orta-yüksek.

### C — Odak Yayı

Her tasarıma isim koyar.

- Beş telefon yatay bir yay üzerinde durur. Kaydırma yayı döndürür ve her adımda bir telefon merkeze gelip büyür.
  Altında kategori ve tasarım adı görünür (ör. "Düğün — Zümrüt").
- **Mobil:** Aynı yay, merkezde tek telefon ve kenarlarda iki komşu.
- **Artı:** Her şablon tek tek tanıtılır; seçim önizlemeye en doğal geçer (merkezdeki telefon seçili şablon olur).
- **Eksi:** 5 adım uzun sürer, G5'i zorlar (≈ 2,5 ekran). Kaydırmanın "ele geçirilmiş" hissi en güçlü olan yön.
- **İş yükü:** Yüksek.

### Karşılaştırma

| Ölçüt | A Üçlü Sahne | B Akan Sütunlar | C Odak Yayı |
|---|---|---|---|
| İsteğe uyum (G1–G3) | ●●● | ●●○ | ●●○ |
| Kısalık (G5) | ●●● ~1,2 ekran | ●●○ ~1,5 ekran | ●○○ ~2,5 ekran |
| Premium / sakin (G6) | ●●● | ●●○ | ●●○ |
| Görünen şablon | 3 | 7 | 5 |
| Medya ağırlığı (masaüstü, tahmin) | ~0,8 MB | ~2 MB | ~1,3 MB |
| Mobil uyum | ●●● | ●●○ | ●●○ |
| İş yükü | Orta | Orta-yüksek | Yüksek |

**Öneri: A.** İsteğin üç maddesini (orta büyük telefon, yanlarda hareket eden telefonlar, kısa) doğrudan karşılar ve
en sakin görünen yön. B'den yalnızca **ekran içi kaydırma** fikri alınır (A'da zaten var). İsteğe bağlı finali
§8, 23.8'de: orta telefon önizleme bölümündeki simülatörün yerine "konar".

## 6. Telefon içerikleri: canlı mı, görsel mi?

| Seçenek | Görüntü | Maliyet | Risk |
|---|---|---|---|
| 1. Canlı `TemplateRenderer` × 3 | Gerçek, animasyonlu | Şablonlar three.js, video ve font yükler; 3 kopya aynı anda | Ana sayfada takılma; paket ve bellek; zarf yine kapalı açılır |
| 2. **Uzun ekran görüntüsü** (AVIF + WebP, 1×/2×) | Keskin, açılmış davetiye; ekran içinde kaydırılır | Telefon başına ~60–150 kB | Animasyon görünmez |
| 3. **Kısa video döngüsü** (WebM + MP4, 5–8 sn, sessiz) | Şablonun gerçek animasyonu (zarf açılışı, efekt) | Telefon başına ~300–600 kB | Mobil veri; düşük güçte pil |

**Öneri:** yan telefonlar = **2** (ekran görüntüsü, kaydırmayla kayar), orta telefon = **3** (video; posteri
ekran görüntüsünün ilk karesi). Video yalnızca `load` olayından sonra iner ve yalnızca görünürken oynar (FE-53 deseni);
`prefers-reduced-motion` ya da `navigator.connection.saveData` açıksa poster kalır. Canlı çizim (1) sahnede
kullanılmaz; canlı deneyim önizleme bölümünde zaten var.

Varlık üretimi (23.2):

- `scripts/showcase/capture.ts`: Playwright (zaten devDependency) ile her şablonu `SHOWCASE_CONTENT` ile 390 × 844,
  DPR 2'de açar, zarfı açar, tam boy ekran görüntüsü alır ve 6 sn video kaydeder. `scripts/onizleme/cek.ts`'in
  senaryo altyapısı yeniden kullanılır.
- Kodlama: ekran görüntüsü → AVIF + WebP; video → WebM (VP9) + MP4 (H.264). `ffmpeg` gerekir (İsmail'in makinesinde
  var mı: S7). Çıktı `public/showcase/<preset>/`'a girer; `.gitattributes` ikili kalıpları kapsar (K275).
- Bütçe kapısı: yeni `verify:showcase` ya da `verify:bundle`'a ek. Telefon başına görsel ≤ 150 kB, video ≤ 600 kB,
  sahne toplamı masaüstü ≤ 1,2 MB / mobil ≤ 0,5 MB.
- Örnek içerik kurgusaldır (`SHOWCASE_CONTENT`); gerçek müşteri verisi kullanılmaz.

## 7. Teknik tasarım

### Bileşenler (CLAUDE.md: atomik, iş mantığı UI dışında, prop drilling yok)

```
src/components/ui/PhoneFrame.tsx           ← DeviceSimulator'dan çıkarılan çerçeve (sunum, durum yok)
src/components/home/showcase/
  ShowcaseSection.tsx                      ← kap: sahne yüksekliği, sticky, ilerleme
  ShowcasePhone.tsx                        ← tek telefon: çerçeve + ekran içi görsel/video
  ShowcaseHeadline.tsx                     ← başlık, alt cümle, "keşfet" bağlantısı
  useShowcaseProgress.ts                   ← useScroll + useTransform; bileşene MotionValue verir
  showcaseSlides.ts                        ← hangi şablon, hangi rol (orta/sol/sağ), varlık yolları
src/hooks/useMediaWhenVisible.ts           ← Hero'daki usePlayWhileVisible + useAfterLoad ortaklaşır
```

- **Durum:** Kaydırma ilerlemesi React durumu değil, `MotionValue`; her karede yeniden çizim olmaz. Zustand store
  gerekmez. Yalnızca "telefona tıklayınca o şablonu seç" eylemi mevcut `useInvitationStore.selectTemplate`'i çağırır.
- **Hareket:** `motion/react` `useScroll({ target, offset: ['start start', 'end end'] })` → `useTransform`. Yazılan
  özellikler yalnızca `transform` ve `opacity`. Hafif `useSpring` (stiffness ~120, damping ~30) Lenis'in üstüne
  ikinci bir yumuşatma eklemeyecek kadar düşük tutulur; Lenis açıkken kapalı denenir.
- **Sabitleme:** CSS `position: sticky` (kaydırma ele geçirilmez; tarayıcı kaydırması doğal kalır). Kap yüksekliği
  masaüstü `220svh`, mobil `160svh` (ya da sabitleme yok). Yükseklik baştan ayrıldığı için CLS üretmez.
- **Kod bölme:** Sahne `React.lazy` ile ayrı parça olur; içe aktarma hero mount olur olmaz başlar. Yer tutucu
  sahnenin tam yüksekliğini ayırır. `Features`'ı ertelememe dersi (uzun görev) burada da geçerli: ilk kaydırmanın
  ortasına ilk çizim düşmemeli. 4× CPU yavaşlatmasıyla ölçülür (23.7).
- **Lenis ve hero snap:** `SNAP_SECTION_ID` yeni sahnenin kimliğine (`vitrin-sahnesi`) çevrilir; hero'dan sahnenin
  başına kayar. Sahnenin içinde snap yoktur. "Keşfet" bağlantısı da aynı kimliğe gider.
- **Hareketi azalt:** `useReducedMotion` → sabitleme yok, üç telefon son konumda statik, video yerine poster.
- **Erişilebilirlik:** Telefonlar `<button>` olur, `aria-label="Düğün — Zümrüt tasarımını önizle"`. Dekoratif kopyalar
  `aria-hidden`; klavyede sıra orta → sol → sağ → bağlantı. Video `muted`, `playsInline`, kontrolsüz, dekoratif.
- **RTL (`ar`):** Yerleşim simetrik; yalnızca eğim yönü ve ok ikonu aynalanır (`rtl:` sınıfları).
- **i18n:** `home.showcase.*` anahtarları 10 dilde. TR metni İsmail onaylar (S6), diğerleri çeviri.

### Tıklama davranışı (S3)

Seçenek 1 (önerilen): telefona tıkla → o şablon seçilir → önizleme bölümüne kayılır, simülatör o şablonla açılır.
Seçenek 2: doğrudan `/create` (şablon seçili). Seçenek 3: tıklama yok, sahne yalnızca vitrin.

## 8. Uygulama adımları (Faz 23, kod dalı `faz-23-v1.4-frontend`)

Her adım tek commit (`23.N - <tip>(<alan>): <Fiil> ...`), her adımın sonunda `npm run check`.

| Adım | İş | Bitti ölçütü |
|---|---|---|
| 23.0 | Dal: `v1.3` ucundan `faz-23-v1.4-frontend`. Taban ölçüm: `npm run check`, e2e, `perf` (ana sayfa LCP/CLS/TBT), 360/390/768/1280/1440 ekran görüntüleri | Taban sayıları bu dosyaya (§11) yazıldı |
| 23.1 | `ui/PhoneFrame` `DeviceSimulator`'dan çıkarılır; görünüm değişmez | `verify:render` + ekran görüntüsü farkı 0 |
| 23.2 | Varlık hattı `scripts/showcase/capture.ts` + seçilen şablonların görsel/video çıktıları + bütçe kapısı | Bütçe kapısı yeşil; varlıklar `public/showcase/` |
| 23.3 | `ShowcaseSection` **statik** yerleşim (hareketsiz), mobil/tablet/masaüstü, i18n 10 dil, RTL | 5 genişlikte ekran görüntüsü; `verify:i18n` yeşil |
| 23.4 | Kaydırma koreografisi (`useShowcaseProgress`), sticky, ekran içi kaydırma, hareketi azalt yolu | 60 fps (masaüstü), 4× CPU'da uzun görev < 100 ms |
| 23.5 | `HomePage`'e yerleştirme; hero snap ve "Keşfet" hedefi; önizleme başlığının sadeleşmesi | Hero → sahne → önizleme akışı elle ve e2e'de |
| 23.6 | Tıklama (S3), klavye, `aria`, video yükleme kuralları (`saveData`, görünürken oynat) | axe 0 ihlal |
| 23.7 | Testler: `e2e/home-showcase.spec.ts` (ilk kaydırmada 3 telefon görünür, reduced-motion statik), `perf` yeniden, a11y | `perf` CLS < 0,1, LCP tabandan kötü değil; e2e yeşil |
| 23.8 | *(İsteğe bağlı)* Final: orta telefon önizlemedeki simülatörün konumuna "konar" (paylaşılan düzen animasyonu) | Ayrı karar; 23.7 yeşilken |
| 23.9 | Kılavuz: frontend `docs/rehber/` altında yeni dosyalar (K18), `README.md`; docs'ta faz kaydı ve kapanış | Bağlantılar açılıyor |

## 9. Riskler

| Risk | Etki | Önlem |
|---|---|---|
| Sabitleme "kaydırma ele geçirildi" hissi verir | Kullanıcı rahatsız olur, hemen çıkar | Sahne ≤ 1,5 ekran; sticky (doğal kaydırma); mobilde kısa ya da yok |
| Lenis + `useScroll` + sticky uyumsuzluğu | Titreme | 23.4'te Lenis açık/kapalı iki yolda ölçülür; `useSpring` kapatılabilir |
| iOS Safari adres çubuğu yüksekliği | Sahne zıplar | `svh` birimi; `dvh` değil |
| Düşük güçlü telefonda video + 3 görsel | Pil, takılma | Mobilde video yok (yalnızca orta telefonda poster + ekran içi kaydırma); `saveData` |
| Ana sayfa uzar | "Çok uzun olmasın" ihlali | Önizleme başlığı kısalır; sahne + önizleme toplamı bugünkü önizlemeden en fazla ~1 ekran uzun |
| Ekran görüntüleri şablon değişince eskir | Vitrin ile gerçek tasarım farklı | Hat tek komut; şablon değişen commit'te yeniden üretim kontrol listesi |
| `v1.3` dalına gelen düzeltmeler `HomePage`/`useLenis`'e dokunur | Birleştirme çakışması | `v1.3` → Faz 23 düzenli `merge` (rebase yok); tek yönlü |
| Apple'a fazla benzerlik | Marka/ticari görünüm | Yalnızca teknik ilham; Apple cihaz görseli, Dynamic Island kopyası, Apple metni kullanılmaz; çerçeve kendi `PhoneFrame`'imiz |

## 10. İsmail'e sorular (karar noktaları)

| # | Soru | Seçenekler | Önerim |
|---|---|---|---|
| S1 | Tasarım yönü | A Üçlü Sahne · B Akan Sütunlar · C Odak Yayı | **A** |
| S2 | Hangi şablonlar? (orta + 2 yan; B/C'de daha çok) | `FEATURED_TEMPLATES` (Düğün `dugun-2`, Kına `manzara`, Nişan `sekilli`, Sünnet `sunnet-klasik`, Doğum günü `dogum-gunu-neseli`) ya da senin seçimin | Orta: Düğün; yanlar: Kına, Nişan — "şu an en güzel" listesini sen ver |
| S3 | Telefona tıklayınca ne olsun? | Önizlemede seç · `/create` · tıklama yok | **Önizlemede seç** |
| S4 | Mobilde sabitleme | Kısa sabitleme (160 svh) · sabitleme yok, statik üçlü | **Kısa sabitleme**, 23.4 ölçümüne göre |
| S5 | Hero'daki "AI vibe" kalıpları (✨ rozet, parıltılı buton, kelime kelime bulanık giriş) Faz 23'e girsin mi? | Evet (23.5'e ek) · Hayır, ayrı faz | Evet, küçük kapsamla (rozet ve parıltı kalkar) |
| S6 | Başlık metni | §4.6'daki üç öneri ya da senin metnin | "Davetiyeniz artık *cepte*." |
| S7 | Video/görsel üretimi kimde? | Ben betikle üretirim (bulut ortamında, `ffmpeg` kurulabiliyorsa) · sen kendi makinende | Betik + senin son kontrolün |
| S8 | Final animasyonu (23.8) | Evet · Hayır · Sonra | Sonra (23.7 yeşilken karar) |
| S9 | Seçimden önce tıklanabilir HTML maket ister misin? | A/B/C'nin kaydırmalı maketi · yalnızca A · istemiyorum | A ve B maketi (C'yi yalnızca istersen) |

Yeni karar(lar) S1–S8 cevaplanınca açılır: sıradaki boş K numarası bu dalda **K276**; ⚠️ Faz 22 numara
tüketebilir, karar anında `DECISION-INDEX.md`'nin en güncel hali esas alınır.

## 11. Ölçümler

| Ölçüm | Taban (23.0) | Sonuç (23.7) |
|---|---|---|
| `npm run check` | koşmadı | — |
| e2e | koşmadı | — |
| `perf` ana sayfa LCP / CLS / TBT | koşmadı | — |
| İlk yükleme paketi (`verify:bundle`) | koşmadı | — |
| Sahne medya toplamı (masaüstü / mobil) | — | — |
