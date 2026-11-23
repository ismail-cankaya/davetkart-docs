# Faz 19.17 — `SEC-12` commit komutları

## Beklenen durum

**`D:\Projects\davetkart-hat-b\davetkart-backend-php-laravel`** (`fix/2026-11-23-sec-12-self-hosted-fonts`): 6 değişen dosya (` M`, 19.17.4'teki liste).

**`D:\Projects\davetkart-hat-b\davetkart-frontent`** (`fix/2026-11-23-sec-12-self-hosted-fonts`): ` M` `src/index.css`, `package.json`, beş yardımcı + `KagitKok.tsx`, dört `fontlar.md`; `??` 129 font dosyası + `templates.css` + 3 yeni kaynak + 3 yeni kılavuz (toplam 148).

**`D:\Projects\davetkart-hat-b\davetkart-docs`** (`docs/2026-11-23-sec-12-self-hosted-fonts`): `??` kayıt + bu dosya.

Sıra: backend → frontend → docs.

## 19.17.4 — backend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-backend-php-laravel
git add deploy/nginx/snippets/davetkart-security-headers.conf
git add deploy/nginx/davetkart.conf
git add deploy/smoke/check-security-headers.sh
git add docs/rehber/deploy/nginx/snippets/davetkart-security-headers.md
git add docs/rehber/deploy/nginx/davetkart.md
git add docs/rehber/deploy/smoke/check-security-headers.md
git commit -m "19.17.4 - fix(nginx): Drop Google Fonts from the CSP and cache self-hosted fonts"
git status --short
```

## 19.17.1 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add public/fonts/inter/inter-latin-ext-opsz-normal.woff2
git add public/fonts/inter/inter-latin-opsz-normal.woff2
git add public/fonts/inter/inter-latin-ext-opsz-italic.woff2
git add public/fonts/inter/inter-latin-opsz-italic.woff2
git add public/fonts/inter/LICENSE
git add public/fonts/playfair-display/playfair-display-latin-ext-wght-normal.woff2
git add public/fonts/playfair-display/playfair-display-latin-wght-normal.woff2
git add public/fonts/playfair-display/playfair-display-latin-ext-wght-italic.woff2
git add public/fonts/playfair-display/playfair-display-latin-wght-italic.woff2
git add public/fonts/playfair-display/LICENSE
git add public/fonts/cormorant-garamond/cormorant-garamond-latin-ext-wght-normal.woff2
git add public/fonts/cormorant-garamond/cormorant-garamond-latin-wght-normal.woff2
git add public/fonts/cormorant-garamond/cormorant-garamond-latin-ext-wght-italic.woff2
git add public/fonts/cormorant-garamond/cormorant-garamond-latin-wght-italic.woff2
git add public/fonts/cormorant-garamond/LICENSE
git add public/fonts/barlow-condensed/barlow-condensed-latin-ext-400-normal.woff2
git add public/fonts/barlow-condensed/barlow-condensed-latin-400-normal.woff2
git add public/fonts/barlow-condensed/barlow-condensed-latin-ext-600-normal.woff2
git add public/fonts/barlow-condensed/barlow-condensed-latin-600-normal.woff2
git add public/fonts/barlow-condensed/LICENSE
git add public/fonts/barlow-semi-condensed/barlow-semi-condensed-latin-ext-400-normal.woff2
git add public/fonts/barlow-semi-condensed/barlow-semi-condensed-latin-400-normal.woff2
git add public/fonts/barlow-semi-condensed/barlow-semi-condensed-latin-ext-500-normal.woff2
git add public/fonts/barlow-semi-condensed/barlow-semi-condensed-latin-500-normal.woff2
git add public/fonts/barlow-semi-condensed/LICENSE
git add public/fonts/newsreader/newsreader-latin-ext-opsz-italic.woff2
git add public/fonts/newsreader/newsreader-latin-opsz-italic.woff2
git add public/fonts/newsreader/LICENSE
git add public/fonts/libre-caslon-display/libre-caslon-display-latin-ext-400-normal.woff2
git add public/fonts/libre-caslon-display/libre-caslon-display-latin-400-normal.woff2
git add public/fonts/libre-caslon-display/LICENSE
git add public/fonts/libre-caslon-text/libre-caslon-text-latin-ext-400-normal.woff2
git add public/fonts/libre-caslon-text/libre-caslon-text-latin-400-normal.woff2
git add public/fonts/libre-caslon-text/libre-caslon-text-latin-ext-700-normal.woff2
git add public/fonts/libre-caslon-text/libre-caslon-text-latin-700-normal.woff2
git add public/fonts/libre-caslon-text/libre-caslon-text-latin-ext-400-italic.woff2
git add public/fonts/libre-caslon-text/libre-caslon-text-latin-400-italic.woff2
git add public/fonts/libre-caslon-text/LICENSE
git add public/fonts/instrument-serif/instrument-serif-latin-ext-400-normal.woff2
git add public/fonts/instrument-serif/instrument-serif-latin-400-normal.woff2
git add public/fonts/instrument-serif/instrument-serif-latin-ext-400-italic.woff2
git add public/fonts/instrument-serif/instrument-serif-latin-400-italic.woff2
git add public/fonts/instrument-serif/LICENSE
git add public/fonts/instrument-sans/instrument-sans-latin-ext-wght-normal.woff2
git add public/fonts/instrument-sans/instrument-sans-latin-wght-normal.woff2
git add public/fonts/instrument-sans/LICENSE
git add public/fonts/pinyon-script/pinyon-script-latin-ext-400-normal.woff2
git add public/fonts/pinyon-script/pinyon-script-latin-400-normal.woff2
git add public/fonts/pinyon-script/LICENSE
git add public/fonts/alex-brush/alex-brush-latin-ext-400-normal.woff2
git add public/fonts/alex-brush/alex-brush-latin-400-normal.woff2
git add public/fonts/alex-brush/LICENSE
git add public/fonts/caveat/caveat-latin-ext-wght-normal.woff2
git add public/fonts/caveat/caveat-latin-wght-normal.woff2
git add public/fonts/caveat/LICENSE
git add public/fonts/eb-garamond/eb-garamond-latin-ext-wght-normal.woff2
git add public/fonts/eb-garamond/eb-garamond-latin-wght-normal.woff2
git add public/fonts/eb-garamond/eb-garamond-latin-ext-wght-italic.woff2
git add public/fonts/eb-garamond/eb-garamond-latin-wght-italic.woff2
git add public/fonts/eb-garamond/LICENSE
git add public/fonts/big-shoulders-display/big-shoulders-display-latin-ext-wght-normal.woff2
git add public/fonts/big-shoulders-display/big-shoulders-display-latin-wght-normal.woff2
git add public/fonts/big-shoulders-display/LICENSE
git add public/fonts/bodoni-moda/bodoni-moda-latin-ext-opsz-normal.woff2
git add public/fonts/bodoni-moda/bodoni-moda-latin-opsz-normal.woff2
git add public/fonts/bodoni-moda/bodoni-moda-latin-ext-opsz-italic.woff2
git add public/fonts/bodoni-moda/bodoni-moda-latin-opsz-italic.woff2
git add public/fonts/bodoni-moda/LICENSE
git add public/fonts/cinzel-decorative/cinzel-decorative-latin-ext-400-normal.woff2
git add public/fonts/cinzel-decorative/cinzel-decorative-latin-400-normal.woff2
git add public/fonts/cinzel-decorative/cinzel-decorative-latin-ext-700-normal.woff2
git add public/fonts/cinzel-decorative/cinzel-decorative-latin-700-normal.woff2
git add public/fonts/cinzel-decorative/LICENSE
git add public/fonts/cinzel/cinzel-latin-ext-wght-normal.woff2
git add public/fonts/cinzel/cinzel-latin-wght-normal.woff2
git add public/fonts/cinzel/LICENSE
git add public/fonts/dm-serif-display/dm-serif-display-latin-ext-400-normal.woff2
git add public/fonts/dm-serif-display/dm-serif-display-latin-400-normal.woff2
git add public/fonts/dm-serif-display/dm-serif-display-latin-ext-400-italic.woff2
git add public/fonts/dm-serif-display/dm-serif-display-latin-400-italic.woff2
git add public/fonts/dm-serif-display/LICENSE
git add public/fonts/fraunces/fraunces-latin-ext-opsz-normal.woff2
git add public/fonts/fraunces/fraunces-latin-opsz-normal.woff2
git add public/fonts/fraunces/fraunces-latin-ext-opsz-italic.woff2
git add public/fonts/fraunces/fraunces-latin-opsz-italic.woff2
git add public/fonts/fraunces/LICENSE
git add public/fonts/marcellus/marcellus-latin-ext-400-normal.woff2
git add public/fonts/marcellus/marcellus-latin-400-normal.woff2
git add public/fonts/marcellus/LICENSE
git add public/fonts/quicksand/quicksand-latin-ext-wght-normal.woff2
git add public/fonts/quicksand/quicksand-latin-wght-normal.woff2
git add public/fonts/quicksand/LICENSE
git add public/fonts/space-grotesk/space-grotesk-latin-ext-wght-normal.woff2
git add public/fonts/space-grotesk/space-grotesk-latin-wght-normal.woff2
git add public/fonts/space-grotesk/LICENSE
git add public/fonts/syne/syne-latin-ext-wght-normal.woff2
git add public/fonts/syne/syne-latin-wght-normal.woff2
git add public/fonts/syne/LICENSE
git add public/fonts/unbounded/unbounded-latin-ext-wght-normal.woff2
git add public/fonts/unbounded/unbounded-latin-wght-normal.woff2
git add public/fonts/unbounded/LICENSE
git add public/fonts/yeseva-one/yeseva-one-latin-ext-400-normal.woff2
git add public/fonts/yeseva-one/yeseva-one-latin-400-normal.woff2
git add public/fonts/yeseva-one/LICENSE
git add public/fonts/baloo-2/baloo-2-latin-ext-wght-normal.woff2
git add public/fonts/baloo-2/baloo-2-latin-wght-normal.woff2
git add public/fonts/baloo-2/LICENSE
git add public/fonts/nunito/nunito-latin-ext-wght-normal.woff2
git add public/fonts/nunito/nunito-latin-wght-normal.woff2
git add public/fonts/nunito/LICENSE
git add public/fonts/manrope/manrope-latin-ext-wght-normal.woff2
git add public/fonts/manrope/manrope-latin-wght-normal.woff2
git add public/fonts/manrope/LICENSE
git add public/fonts/allura/allura-latin-ext-400-normal.woff2
git add public/fonts/allura/allura-latin-400-normal.woff2
git add public/fonts/allura/LICENSE
git add public/fonts/special-elite/special-elite-latin-ext-400-normal.woff2
git add public/fonts/special-elite/special-elite-latin-400-normal.woff2
git add public/fonts/special-elite/LICENSE
git add public/fonts/fredoka/fredoka-latin-ext-wght-normal.woff2
git add public/fonts/fredoka/fredoka-latin-wght-normal.woff2
git add public/fonts/fredoka/LICENSE
git add public/fonts/italiana/italiana-latin-400-normal.woff2
git add public/fonts/italiana/LICENSE
git add public/fonts/libre-baskerville/libre-baskerville-latin-ext-400-normal.woff2
git add public/fonts/libre-baskerville/libre-baskerville-latin-400-normal.woff2
git add public/fonts/libre-baskerville/libre-baskerville-latin-ext-400-italic.woff2
git add public/fonts/libre-baskerville/libre-baskerville-latin-400-italic.woff2
git add public/fonts/libre-baskerville/LICENSE
git add public/fonts/templates.css
git add src/styles/fonts.css
git add src/index.css
git add docs/rehber/src/styles/fonts.md
git commit -m "19.17.1 - fix(fonts): Self-host font files with latin and latin-ext subsets"
git status --short
```

## 19.17.2 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add src/utils/templateFonts.ts
git add src/components/templates/konsept/harita/fontlar.ts
git add src/components/templates/konsept/kitap/fontlar.ts
git add src/components/templates/konsept/sergi/fontlar.ts
git add src/components/templates/shared/paper/fontlar.ts
git add src/components/templates/shared/paper/KagitKok.tsx
git add src/components/templates/shared/sinema/useTemplateFont.ts
git add docs/rehber/src/utils/templateFonts.md
git add docs/rehber/src/components/templates/konsept/harita/fontlar.md
git add docs/rehber/src/components/templates/konsept/kitap/fontlar.md
git add docs/rehber/src/components/templates/konsept/sergi/fontlar.md
git add docs/rehber/src/components/templates/shared/paper/fontlar.md
git commit -m "19.17.2 - fix(templates): Load template fonts from the local stylesheet"
git status --short
```

## 19.17.3 — frontend

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-frontent
git add scripts/verify-fonts.ts
git add package.json
git add docs/rehber/scripts/verify-fonts.md
git commit -m "19.17.3 - test(verify): Fail the check when the build references Google Fonts"
git status --short
```

## 19.17.6 — docs

```powershell
cd D:\Projects\davetkart-hat-b\davetkart-docs
git add phases/faz-19/kayit/19-17-SEC-12.md
git add phases/faz-19/FAZ-19-SEC-12-COMMIT-KOMUTLARI.md
git commit -m "docs(faz-19): Add 19.17 SEC-12 record and commit commands (K226)"
git status --short
```

## Birleştirme — ana klasör

```powershell
cd D:\Projects\davetkart\davetkart-backend-php-laravel
git merge --no-ff fix/2026-11-23-sec-12-self-hosted-fonts -m "Merge SEC-12 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-frontent
git merge --no-ff fix/2026-11-23-sec-12-self-hosted-fonts -m "Merge SEC-12 into faz-19-audit-fixes"
git status --short

cd D:\Projects\davetkart\davetkart-docs
git merge --no-ff docs/2026-11-23-sec-12-self-hosted-fonts -m "Merge SEC-12 into docs/2026-11-20-faz-19-audit-fixes"
git status --short
```

Çakışma çıkarsa: `prompts/faz-19-agent/19-CAKISMA.md`.
