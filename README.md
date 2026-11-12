# davetkart-docs

DavetKart'ın (dijital davetiye SaaS'ı) **kod dışı** dokümanları: bağlam ve karar kaydı, faz kayıtları,
ajan prompt'ları, denetimler, yayın planı, ürün çalışmaları, notlar. Eski adı `claude/`
(`davetkart-claude` deposu).

Kod ve kodun kılavuzları burada **değil**:
`../davetkart-backend-php-laravel` (PHP 8.5 + Laravel 13) ve `../davetkart-frontent` (React 19 +
TypeScript); kılavuzları kendi `docs/rehber/` klasörlerinde.

## Okuma sırası (yeni bir oturum)

1. Bu dosya.
2. [`context/PHP-LARAVEL-SETUP.md`](context/PHP-LARAVEL-SETUP.md): §2 çalışma kuralları, §9 şu anki
   durum, §10 yol haritası, §11 ihlal edilemez kurallar.
3. [`decisions/DECISION-INDEX.md`](decisions/DECISION-INDEX.md): bütün K numaraları ve sıradaki boş numara.
4. İşle ilgili klasör: bir faz için [`phases/`](phases/README.md), yayın için
   [`operations/`](operations/README.md).

Yapay zekâ asistanları için kurallar: [`CLAUDE.md`](CLAUDE.md).

## Harita: neyi nerede bulurum?

| Arıyorum | Klasör |
|---|---|
| Proje ne, şu an neredeyiz, çalışma kuralları | [`context/`](context/README.md) |
| Bir kararın numarası, gerekçesi, geçerli mi | [`decisions/`](decisions/README.md) |
| Bir fazın raporu, commit komutları, ara çıktıları | [`phases/`](phases/README.md) |
| Bir ajana verilmiş prompt | [`prompts/`](prompts/README.md) |
| Denetim / gözden geçirme raporu | [`audits/`](audits/README.md) |
| Yayın, AWS, sunucu, DNS | [`operations/`](operations/README.md) |
| Fiyat, plan, tasarım/video onayları | [`product/`](product/README.md) |
| Serbest notlar, analizler | [`notes/`](notes/README.md) |
| Eskimiş, yerine başkası geçmiş dosyalar | [`archive/`](archive/README.md) |
| Bu deponun değişiklik günlüğü | [`CHANGELOG.md`](CHANGELOG.md) |

## Eski yollar (2026-11-12 öncesi)

Eski dokümanlarda düz metin olarak geçen yollar değiştirilmedi. Karşılıkları:

| Eski | Yeni |
|---|---|
| `claude/PHP-LARAVEL-SETUP.md` | `context/PHP-LARAVEL-SETUP.md` |
| `claude/PHP-LARAVEL-SETUP-EK-FAZ-11.md`, `-12.md` | `decisions/addenda/` |
| `claude/Notlar/01…03-*.md` | `notes/` |
| `claude/hero-video-onay/`, `claude/video-onay/` | `product/` |
| `claude/PROMPT.md`, `claude/PROMPT-ARSIV-FAZ-4.md`, `claude/README.md` | `archive/` |
| `PROMPT-FAZ-11.md`, `PROMPT-FAZ-12.md`, `PROMPT-YAYIN.md` (kök) | `prompts/` |
| `YAYIN-PLANI.md`, `YAYIN-DEVIR.md` (kök) | `operations/deployment/` |
| `Claude outputs/FAZ-NN-*.md`, `f13-ara/`, `f14/` | `phases/faz-NN/` |
| `Claude outputs/FRONTEND-YAKALAMA-PLANI.md` | `phases/frontend-catch-up/` |
| `scaffold-structure.ps1` (kök) | `archive/` |

⚠️ `claude/GOZDEN-GECIRME-*.md`, `claude/FAZ-*-DEVIR.md`, `claude/FAZ-10-PLANI.md`,
`claude/PHP-LARAVEL-SETUP-EK-FAZ-5…9.md`, `claude/TEST-DENETIMI-*.md` bu depoda hiç olmadı: onlar
**backend deposunun** `claude/` klasöründe. Tam taşıma tablosu:
[`_restructure/MIGRATION-PLAN.md`](_restructure/MIGRATION-PLAN.md).
