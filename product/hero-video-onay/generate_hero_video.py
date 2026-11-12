#!/usr/bin/env python3
"""
DavetKart — Hero arkaplan videosu üreteci.
"Akan ipek + altın bokeh", açık krem tonlarında, kusursuz döngülü.

Palet doğrudan src/index.css @theme bloğundan alınmıştır.

DÖNGÜ GARANTİSİ
---------------
Tüm zamana bağlı ifadeler sin/cos(k * p) biçimindedir; burada p = 2*pi*i/N
ve k bir TAM SAYIdır. Böylece i=0 ile i=N kareleri matematiksel olarak
aynıdır -> videonun başı ve sonu arasında "dikiş" (seam) oluşmaz.
Işık süzülmesi (sheen) ise mod-1 sarmalı ile sürekli ilerler, o da tam döner.
"""

import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

# ----------------------------------------------------------------------------
# Ayarlar
# ----------------------------------------------------------------------------
W, H = 1920, 1080
FPS, DUR = 30, 12
N = FPS * DUR                 # 360 kare

LW, LH = 320, 180             # ipek alanı çözünürlüğü (upscale ile yumuşar)
BW, BH = 960, 540             # bokeh katmanı (yarı çözünürlük = ücretsiz blur)

OUT_RAW = "/tmp/hero_lossless.mkv"


def hexc(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float64) / 255.0


# index.css --color-* değerleriyle uyumlu.
# NOT: ilk denemede aralık #ece6d9..#fdfcf9 idi ve neredeyse düz beyaz çıktı;
# hem ipek kıvrımları hem bokeh kayboldu. Işık katmanlarının görünebilmesi
# için tabanın "tavana yapışmaması", yani parlaklık payı bırakması şart.
IVORY_LO = hexc("#dbd2bd")    # ipeğin gölge tarafı (luma ~211)
IVORY_HI = hexc("#faf7f0")    # ipeğin ışık tarafı  (luma ~247)
CHAMPAGNE = hexc("#e7d3a6")   # --color-champagne'in biraz doygunlaştırılmışı
EMERALD_WASH = hexc("#ccdbd2")  # --color-brand'in çok seyreltilmiş hâli
GOLD = hexc("#c9a961")        # --color-gold

# ----------------------------------------------------------------------------
# Koordinat ızgaraları (bir kez kurulur, her karede yeniden kullanılır)
# ----------------------------------------------------------------------------
_x = np.linspace(0.0, 1.0, LW, dtype=np.float64)
_y = np.linspace(0.0, 1.0, LH, dtype=np.float64)
X, Y = np.meshgrid(_x, _y)

# Merkeze uzaklık — 16:9'da dairesel görünmesi için Y ölçeklenir
RAD = np.sqrt((X - 0.5) ** 2 + ((Y - 0.5) * (H / W) * (W / H) * 1.55) ** 2)


def smoothstep(t: np.ndarray) -> np.ndarray:
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


# ----------------------------------------------------------------------------
# Katman 1 — akan ipek
# ----------------------------------------------------------------------------
def silk_layer(p: float, prog: float) -> np.ndarray:
    """LH x LW x 3 float RGB döndürür."""

    # Üst üste binen düşük frekanslı dalgalar: hiçbiri tek başına fark
    # edilmez, toplamı organik bir kumaş kıvrımı hissi verir.
    v = 1.00 * np.sin(5.2 * X + 3.6 * Y + 1.0 * p)
    v += 0.78 * np.sin(3.7 * X - 4.9 * Y - 1.0 * p + 1.72)
    v += 0.58 * np.sin(7.4 * X * Y + 2.0 * p + 0.41)
    v += 0.42 * np.sin(4.8 * (X + Y) - 2.0 * p + 2.93)
    v += 0.30 * np.sin(9.6 * Y - 3.0 * p + 0.85)
    v = 0.5 + 0.5 * (v / 3.08)
    v = np.clip(v, 0.0, 1.0)

    # İkinci, bağımsız alan: emerald yıkamasını ipekten ayrı hareket ettirir,
    # böylece iki renk kütlesi birbirine kilitlenmiş görünmez.
    w = 0.5 + 0.5 * np.sin(2.9 * X - 3.3 * Y + 1.0 * p + 4.1) * 0.7 \
        + 0.5 * np.sin(4.4 * Y + 2.0 * p + 1.3) * 0.3
    w = np.clip(w, 0.0, 1.0)

    vs = smoothstep(v)

    # Temel geçiş: fildişi gölge -> fildişi ışık
    col = IVORY_LO[None, None, :] + (IVORY_HI - IVORY_LO)[None, None, :] * vs[..., None]

    # Şampanya yalnızca en aydınlık tepelerde belirir (üst %35)
    champ = np.clip((vs - 0.65) / 0.35, 0.0, 1.0) ** 1.7
    col = col + (CHAMPAGNE[None, None, :] - col) * (0.60 * champ)[..., None]

    # Emerald yıkama: markanın yeşilini hissettirir ama kontrastı düşürmez
    em = np.clip((w - 0.55) / 0.45, 0.0, 1.0) ** 2.0
    col = col + (EMERALD_WASH[None, None, :] - col) * (0.26 * em)[..., None]

    # Işık süzülmesi (sheen): çapraz geniş bir bant tuvali kat eder.
    # mod-1 sarmalı sayesinde tek turda tam olarak başa döner.
    u = (0.68 * X + 0.32 * Y - prog) % 1.0
    d = np.minimum(u, 1.0 - u)
    sheen = np.exp(-(d ** 2) / (2 * 0.135 ** 2))
    col = col + (0.042 * sheen)[..., None]

    # Merkez aydınlatma + kenar vinyeti:
    # başlık ve butonlar tam ortada olduğu için merkezi bilinçli olarak
    # açık tutuyoruz — koyu metnin kontrastı hiç düşmesin.
    col += (0.048 * np.exp(-(RAD / 0.44) ** 2))[..., None]
    col -= (0.075 * smoothstep((RAD - 0.32) / 0.62))[..., None]

    return col


# ----------------------------------------------------------------------------
# Katman 2 — odaktan çıkmış altın bokeh
# ----------------------------------------------------------------------------
rng = np.random.default_rng(20260730)
P_COUNT = 22

# Orblar merkezden dışarı itiliyor. Kompozisyonun ortası başlık, alt başlık
# ve butonlara ait; oraya ışık lekesi koymak hem metni yorar hem de ucuz bir
# "stok bokeh overlay" hissi verir. Bir halka (annulus) içinde örnekleyip
# merkezi bilinçli olarak boş bırakıyoruz.
_ang = rng.uniform(0.0, 2 * np.pi, P_COUNT)
_dst = rng.uniform(0.62, 1.35, P_COUNT)
_px = 0.5 + np.cos(_ang) * _dst * 0.62
_py = 0.5 + np.sin(_ang) * _dst * 0.58
_pr = rng.uniform(0.045, 0.150, P_COUNT)          # BW'ye oranla yarıçap
_pa = rng.uniform(0.022, 0.070, P_COUNT)          # taban opaklık
_ox = rng.uniform(0.010, 0.055, P_COUNT)          # yörünge genlikleri
_oy = rng.uniform(0.010, 0.055, P_COUNT)
_pk = rng.choice([1, 1, 1, 2], P_COUNT)           # tamsayı harmonik -> döngü korunur
_pp = rng.uniform(0.0, 2 * np.pi, P_COUNT)
_pw = rng.uniform(0.0, 1.0, P_COUNT)              # gold <-> beyaz karışımı

_bx = np.arange(BW)
_by = np.arange(BH)


def bokeh_layer(p: float) -> np.ndarray:
    """Toplamalı ışık katmanı, BH x BW x 3 float."""
    layer = np.zeros((BH, BW, 3), dtype=np.float64)

    for i in range(P_COUNT):
        k, ph = float(_pk[i]), _pp[i]
        cx = (_px[i] + _ox[i] * np.cos(k * p + ph)) * BW
        cy = (_py[i] + _oy[i] * np.sin(k * p + ph * 1.7)) * BH
        r = _pr[i] * BW * (1.0 + 0.14 * np.sin(k * p + ph * 0.6))
        a = _pa[i] * (0.72 + 0.28 * np.sin(k * p + ph * 2.1))
        if a <= 0.0 or r <= 1.0:
            continue

        x0, x1 = max(0, int(cx - r)), min(BW, int(cx + r) + 1)
        y0, y1 = max(0, int(cy - r)), min(BH, int(cy + r) + 1)
        if x0 >= x1 or y0 >= y1:
            continue

        dx = (_bx[x0:x1] - cx) / r
        dy = (_by[y0:y1] - cy) / r
        dist2 = dy[:, None] ** 2 + dx[None, :] ** 2
        m = np.clip(1.0 - dist2, 0.0, 1.0)

        # Gerçek bokeh düz merkez + hafif parlak kenar verir:
        # yumuşak dolgu + ince halka.
        prof = m ** 1.35 + 0.30 * np.exp(-((np.sqrt(dist2) - 0.86) ** 2) / (2 * 0.10 ** 2)) * (dist2 < 1.0)

        tint = GOLD * (1.0 - _pw[i] * 0.55) + np.array([1.0, 1.0, 1.0]) * (_pw[i] * 0.55)
        layer[y0:y1, x0:x1, :] += (prof * a)[..., None] * tint[None, None, :]

    return layer


# ----------------------------------------------------------------------------
# Katman 3 — minik altın parıltılar (tam çözünürlükte, keskin)
# ----------------------------------------------------------------------------
S_COUNT = 64
_sx = rng.uniform(0.0, 1.0, S_COUNT)
_sy = rng.uniform(0.0, 1.0, S_COUNT)
_sr = rng.uniform(1.6, 4.2, S_COUNT)
_sk = rng.choice([2, 3, 4, 5], S_COUNT)
_sp = rng.uniform(0.0, 2 * np.pi, S_COUNT)
_sa = rng.uniform(0.10, 0.30, S_COUNT)
_sd = rng.uniform(0.006, 0.020, S_COUNT)

_fx = np.arange(W)
_fy = np.arange(H)


def sparkle_into(img: np.ndarray, p: float) -> None:
    """img üzerine yerinde (in-place) ekler."""
    for i in range(S_COUNT):
        k, ph = float(_sk[i]), _sp[i]
        tw = 0.5 + 0.5 * np.sin(k * p + ph)
        a = _sa[i] * (tw ** 2.4)          # keskin yanıp sönme, yumuşak sönme
        if a < 0.004:
            continue
        r = _sr[i] * 3.0
        cx = (_sx[i] + _sd[i] * np.cos(1.0 * p + ph)) * W
        cy = (_sy[i] + _sd[i] * np.sin(1.0 * p + ph)) * H

        x0, x1 = max(0, int(cx - r)), min(W, int(cx + r) + 1)
        y0, y1 = max(0, int(cy - r)), min(H, int(cy + r) + 1)
        if x0 >= x1 or y0 >= y1:
            continue
        dx = (_fx[x0:x1] - cx) / r
        dy = (_fy[y0:y1] - cy) / r
        g = np.exp(-(dy[:, None] ** 2 + dx[None, :] ** 2) * 3.2)
        # img 0-255 ölçeğinde tutuluyor, bu yüzden 255 ile ölçekle
        img[y0:y1, x0:x1, :] += (g * a * 255.0)[..., None] * GOLD[None, None, :]


# ----------------------------------------------------------------------------
# Bantlanmayı (banding) önleyen SABİT dither deseni
# ----------------------------------------------------------------------------
# 8-bit'e yuvarlarken çok yumuşak gradyanlar halka halka bantlar üretir.
# Kare başına rastgele gürültü bunu çözer ama video sıkıştırmasını çökertir.
# Bu yüzden desen bir kez üretilip TÜM karelerde aynı kullanılır: bantlar
# kırılır, ardışık kareler arası fark sıfır kalır -> bit-rate patlamaz.
# 0..1 aralığı: ortalaması 0.5 olduğu için aynı zamanda uint8'e kesme
# (truncation) işleminin yuvarlamaya dönüşmesini de sağlar.
DITHER = rng.random((H, W, 1)).astype(np.float32)


def render(i: int) -> bytes:
    p = 2.0 * np.pi * i / N
    prog = i / N

    silk = silk_layer(p, prog).astype(np.float32)
    silk_img = Image.fromarray(np.clip(silk * 255.0, 0, 255).astype(np.uint8), "RGB")
    silk_full = np.asarray(silk_img.resize((W, H), Image.BICUBIC), dtype=np.float32)

    bok = bokeh_layer(p).astype(np.float32)
    bok_img = Image.fromarray(np.clip(bok * 255.0, 0, 255).astype(np.uint8), "RGB")
    bok_img = bok_img.filter(ImageFilter.GaussianBlur(2.2)).resize((W, H), Image.BICUBIC)
    bok_full = np.asarray(bok_img, dtype=np.float32)

    # Toplamalı (additive) harman. Screen denendi ama taban zaten açık
    # olduğu için screen(x, ~beyaz) ≈ beyaz veriyor ve bokeh tamamen
    # kayboluyordu. Toplamalı harman, tabanda bıraktığımız parlaklık payını
    # kullanarak orbları görünür kılar; clip zaten yanmayı sınırlıyor.
    # Tüm işlemler 0-255 ölçeğinde ve yerinde (in-place): 1080p'de her ara
    # dizi tahsisi kare süresine doğrudan yansıyor.
    out = silk_full
    np.add(out, bok_full, out)

    sparkle_into(out, p)

    np.add(out, DITHER, out)
    np.clip(out, 0.0, 255.0, out)
    return out.astype(np.uint8).tobytes()


def main() -> None:
    # Sandbox'ta her kabuk çağrısı bağımsız ve ~45s ile sınırlı; bu yüzden
    # render parçalara bölünür, her parça kayıpsız bir segment üretir,
    # segmentler sonda concat edilir.
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    end = int(sys.argv[2]) if len(sys.argv) > 2 else N
    out_path = sys.argv[3] if len(sys.argv) > 3 else OUT_RAW

    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "ffv1", "-level", "3",
        out_path,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert proc.stdin is not None
    for i in range(start, end):
        proc.stdin.write(render(i))
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("ffmpeg kayipsiz segmentte basarisiz oldu")
    print(f"tamam {start}..{end} -> {out_path}")


if __name__ == "__main__":
    main()
