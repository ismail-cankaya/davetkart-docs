#!/usr/bin/env python3
"""
DavetKart - "premium" konsept serisi videoları.

  dugun-sahil : gün batımında deniz, güneş yolu (glitter path), ufuk bulutları

TASARIM KARARI - iş bölümü
--------------------------
Video yalnızca ATMOSFERİ taşır (gökyüzü, deniz, ışık). Salıncak/çift silüeti,
martılar ve altın ışık tozu videoya GÖMÜLMEZ; bunlar frontend'de SVG ve canvas
katmanı olarak durur. Sebepleri:
  * vektör silüet her çözünürlükte keskin kalır, 300 KB video ise ölçeklenince bulanır
  * mouse'a duyarlı parallax ancak ayrı katmanlarda mümkündür
  * silüetin rengi/pozu koda dokunmadan tema başına değiştirilebilir
Video = değişmeyen sinematik zemin, DOM = etkileşen ön plan.
"""

import numpy as np

from video_engine import BaseScene, WaveField, hexc, smoothstep, variants, run_cli

# Palet - sinematik gün batımı
SKY_TOP = hexc("#2d3d6b")      # alacakaranlık moru
SKY_MID = hexc("#8a5a7a")      # geçiş
SKY_WARM = hexc("#e08a5c")     # mercan
SKY_HOT = hexc("#f9c66b")      # ufuk altını
SUN = hexc("#fff2c4")
SEA_FAR = hexc("#5d5470")
SEA_NEAR = hexc("#191627")
GLITTER = hexc("#ffd98a")
CLOUD_DARK = hexc("#6b4a63")
CLOUD_LIT = hexc("#ffc98f")


class DugunSahil(BaseScene):
    def build(self):
        self.hor = self.cfg.get("horizon", 0.58)      # ufuk çizgisi
        sx, sy = self.cfg["focus"]
        self.sun_x, self.sun_y = sx, self.hor - 0.035

        # --- gökyüzü degradesi (ufka doğru ısınır) ---
        self.sky = self.vgradient([(0.0, SKY_TOP), (0.34, SKY_MID),
                                   (0.50, SKY_WARM), (self.hor, SKY_HOT)])

        # --- deniz degradesi (uzakta açık, yakında koyu) ---
        sea_t = np.clip((self.Y - self.hor) / max(1e-3, 1.0 - self.hor), 0.0, 1.0)
        self.sea = SEA_FAR[None, None, :] + (SEA_NEAR - SEA_FAR)[None, None, :] * (sea_t ** 0.7)[..., None]
        self.sea_mask = smoothstep(self.hor - 0.004, self.hor + 0.004, self.Y)[..., None]
        self.sea_t = sea_t

        # --- güneş mesafeleri ---
        d = np.sqrt((self.X - self.sun_x) ** 2 + ((self.Y - self.sun_y) * (1.0 / max(0.3, self.aspect))) ** 2)
        self.sun_d = d

        # --- katmanlar ---
        s = self.scale
        # Bulutlar: y_squash yüksek -> yatay uzanan şeritler (ufuk bulutu)
        self.clouds = WaveField(self.rw, self.rh, 51, 34, 1.0, 5.0, 1.30, 0.35, s, 4.2)
        # Deniz dokusu: çok yüksek y frekansı -> ince yatay dalga çizgileri
        self.ripple = WaveField(self.rw, self.rh, 53, 34, 3.0, 14.0, 1.05, 0.60, s, 14.0)
        self.swell = WaveField(self.rw, self.rh, 59, 16, 0.8, 2.6, 1.10, 0.30, s, 6.0)

        # Güneş yolu maskesi: aşağı indikçe genişleyen koni (perspektif)
        width = 0.026 + 0.20 * np.clip(self.sea_t, 0.0, 1.0)
        self.path = np.exp(-((self.X - self.sun_x) / width) ** 2)

    def frame(self, p):
        # 1) Gökyüzü + güneş halesi
        img = self.sky.copy()
        breathe = 1.0 + 0.04 * np.cos(2.0 * np.pi * p)
        halo = np.exp(-(self.sun_d / (0.30 * breathe)) ** 2)
        img = img + (SUN[None, None, :] - img) * (0.75 * halo)[..., None]
        img = img + (SUN[None, None, :] - img) * (0.98 * np.exp(-(self.sun_d / (0.062 * breathe)) ** 2))[..., None]

        # 2) Ufuk bulutları - yalnızca gökyüzü bandında, alttan aydınlık
        c = self.clouds.value(p)
        band = np.exp(-((self.Y - (self.hor - 0.16)) / 0.13) ** 2)
        alpha = smoothstep(0.54, 0.74, c) * band * 0.85
        lit = smoothstep(0.50, 0.86, c)
        warm = np.exp(-(self.sun_d / 0.42) ** 2)
        col = CLOUD_DARK[None, None, :] + (CLOUD_LIT - CLOUD_DARK)[None, None, :] * (0.35 + 0.65 * warm)[..., None]
        col = col + (SUN[None, None, :] - col) * (0.45 * lit * warm)[..., None]
        img = img * (1.0 - alpha[..., None]) + col * alpha[..., None]

        # 3) Deniz
        sea = self.sea.copy()
        # Uzun soluklu kabarma + ince dalga çizgileri
        sea = sea + (SEA_FAR[None, None, :] - sea) * (0.25 * self.swell.value(p))[..., None]
        ripple = self.ripple.value(p)
        sea = sea * (1.0 + 0.22 * (ripple - 0.5))[..., None]

        # Güneş yolu: dalga tepelerinde kırılan ışık. Eşik yüksek tutulur ki
        # sürekli bir sütun değil, titreşen ayrı ayrı parıltılar oluşsun.
        spark = smoothstep(0.62, 0.84, ripple) * self.path
        near = 0.35 + 0.65 * smoothstep(0.0, 0.55, self.sea_t)   # yakında daha iri parıltı
        sea = sea + (GLITTER[None, None, :] - sea) * np.clip(0.95 * spark * near, 0.0, 1.0)[..., None]
        sea = sea + (SUN[None, None, :] - sea) * (0.42 * self.path * np.exp(-self.sea_t * 2.6))[..., None]

        img = img * (1.0 - self.sea_mask) + sea * self.sea_mask

        # 4) Sinematik kapanış: kenar karartma + hafif sıcak yıkama
        img = img + (SKY_HOT[None, None, :] - img) * (0.10 * np.exp(-(self.sun_d / 0.75) ** 2))[..., None]
        img = img * (1.0 - 0.34 * smoothstep(0.30, 0.92, self.center_d)[..., None])
        return np.clip(img, 0.0, 1.0)


# ---------------------------------------------------------------------------
# 2) DÜĞÜN — Onyx & sıvı altın (Modern & Lüks Soyut)
# ---------------------------------------------------------------------------
ONYX = hexc("#07070a")
ONYX_LIFT = hexc("#141119")

# Metalik rampa: koyu bronzdan spekülere. Sıvı metal görünümünün sırrı
# renk değil RAMPADIR - gerçek metal ışığı kademesiz değil, keskin
# bantlar hâlinde yansıtır. Yumuşak degrade plastik görünür.
GOLD_RAMP = ["#0d0903", "#3d2a08", "#8a6418", "#d0a03c", "#f7dc9c", "#fffdf5"]
ROSE_RAMP = ["#0d0505", "#3a1a16", "#8a4638", "#c9806a", "#f0bfae", "#fff4ee"]


def build_ramp(stops, size=256):
    cols = np.array([hexc(c) for c in stops], dtype=np.float32)
    xs = np.linspace(0.0, 1.0, len(stops), dtype=np.float32)
    grid = np.linspace(0.0, 1.0, size, dtype=np.float32)
    return np.stack([np.interp(grid, xs, cols[:, k]) for k in range(3)], axis=1).astype(np.float32)


def apply_ramp(lut, t):
    """
    Rampadan renk okur. Doğrudan tamsayı indeksleme (lut[int(t*255)]) rampayı
    256 basamağa yuvarlar; koyu zeminde bu hem bantlaşma yapar hem de döngü
    dikişi ölçümünde 1 basamaklık sahte fark üretir. Komşu iki girdi arasında
    doğrusal harmanlamak ikisini de yok eder.
    """
    n = lut.shape[0] - 1
    pos = np.clip(t, 0.0, 1.0) * n
    i0 = np.floor(pos).astype(np.int32)
    i1 = np.minimum(i0 + 1, n)
    frac = (pos - i0)[..., None]
    return lut[i0] * (1.0 - frac) + lut[i1] * frac


class DugunOnyx(BaseScene):
    def build(self):
        s = self.scale
        self.base = ONYX[None, None, :] + (ONYX_LIFT - ONYX)[None, None, :] * \
            (0.55 * self.radial(0.5, 0.5, 0.75))[..., None]

        # İki bağımsız akış: altın ana kütle, rose-gold ikincil vurgu.
        self.flow_a = WaveField(self.rw, self.rh, 101, 30, 0.9, 3.6, 1.35, 0.45, s, 1.5)
        self.flow_b = WaveField(self.rw, self.rh, 103, 26, 1.3, 4.8, 1.40, -0.45, s, 1.7)
        self.mask_f = WaveField(self.rw, self.rh, 107, 14, 0.6, 1.8, 1.10, 0.25, s, 1.2)

        self.gold = build_ramp(GOLD_RAMP)
        self.rose = build_ramp(ROSE_RAMP)

        # Metal yalnızca kenarlarda yaşar: merkez onyx kalır, metin oraya oturur.
        self.edge = 0.06 + 0.94 * smoothstep(0.20, 0.66, self.center_d)

        # Geometrik hat: yavaşça nefes alan ince altın halka (art deco aksanı).
        r = np.sqrt((self.X - 0.5) ** 2 + ((self.Y - 0.5) * (1.0 / max(0.35, self.aspect))) ** 2)
        self.ring_r = r
        self.hair = hexc("#e9c880")

    def frame(self, p):
        img = self.base.copy()

        # Sıvı altın: alanı üçgen dalgayla katlayıp rampadan geçiriyoruz.
        # Katlama, tek bir alandan birden fazla ışık bandı doğurur - erimiş
        # metalin üst üste binen yansımaları böyle oluşur.
        fa = self.flow_a.value(p)
        ta = np.abs(((3.0 * fa) % 1.0) * 2.0 - 1.0)
        gold = apply_ramp(self.gold, ta)
        amp_a = smoothstep(0.45, 0.84, fa) * self.edge
        img = img + (gold - img) * (0.92 * amp_a)[..., None]

        fb = self.flow_b.value(p)
        tb = np.abs(((2.0 * fb) % 1.0) * 2.0 - 1.0)
        rose = apply_ramp(self.rose, tb)
        amp_b = smoothstep(0.58, 0.92, fb) * self.edge * smoothstep(0.45, 0.85, self.mask_f.value(p))
        img = img + (rose - img) * (0.70 * amp_b)[..., None]

        # NOT: art deco halkası bilinçli olarak videoda DEĞİL, SVG katmanında.
        # 1 piksellik altın hat videoda kodlayıcı tarafından ezilir (ringing),
        # vektörde ise her çözünürlükte jilet gibi kalır ve çizilerek girebilir.

        img = img * (1.0 - 0.38 * smoothstep(0.34, 0.95, self.center_d)[..., None])
        return np.clip(img, 0.0, 1.0)


CONCEPTS = {
    "dugun-onyx": dict(cls=DugunOnyx, variants=variants((0.50, 0.50), (0.50, 0.50))),
    "dugun-sahil": dict(cls=DugunSahil, variants={
        "desktop": dict(out=(1280, 720), render=(640, 360), focus=(0.50, 0.58), scale=1.0, horizon=0.58),
        # Dikeyde ufuk yukarı çekilir: deniz alanı büyür, isimler gökte durur.
        "mobile": dict(out=(720, 1280), render=(360, 640), focus=(0.50, 0.46), scale=0.62, horizon=0.46),
    }),
}


if __name__ == "__main__":
    run_cli(CONCEPTS)
