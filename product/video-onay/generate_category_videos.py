#!/usr/bin/env python3
"""
DavetKart - kategori bazlı videolu tema konseptleri.

  kina-bordo         : bordo ipek + altın ışık süzülmesi        (Kına)
  nisan-sampanya     : fildişi/şampanya ipek + altın toz        (Nişan)
  sunnet-yildiz      : gece mavisi + yıldız tozu                (Sünnet)
  dogum-konfeti      : krem zemin + düşen konfeti               (Doğum Günü)
  mezuniyet-lacivert : lacivert + çapraz ışık süpürmesi         (Mezuniyet)
  baby-kabarcik      : pastel degrade + yükselen kabarcıklar    (Baby Shower)
  parti-neon         : gece siyahı + neon aurora şeritleri      (Parti)

Ortak motor video_engine.py'dedir; bu dosya yalnızca "ne göründüğünü" tarif eder.
"""

import numpy as np

from video_engine import (BaseScene, WaveField, hexc, smoothstep, variants, run_cli)


# ---------------------------------------------------------------------------
# Ortak: kusursuz döngülü ışık süzülmesi (sheen)
# ---------------------------------------------------------------------------
def sheen(scene, p, width=0.14, tilt=0.30):
    """Tuvali çapraz kat eden geniş ışık bandı. p 0->1 giderken tam tur atar."""
    u = ((1.0 - tilt) * scene.X + tilt * scene.Y - p) % 1.0
    d = np.minimum(u, 1.0 - u)
    return np.exp(-(d ** 2) / (2 * width ** 2))


# ---------------------------------------------------------------------------
# 1) KINA — bordo ipek
# ---------------------------------------------------------------------------
KINA_DARK = hexc("#2e0a17")
KINA_MID = hexc("#5e1329")
KINA_LIGHT = hexc("#96263f")
KINA_GOLD = hexc("#e8c07a")


class KinaBordo(BaseScene):
    def build(self):
        self.silk = WaveField(self.rw, self.rh, 41, 44, 1.0, 5.5, 1.35, 0.45, self.scale, 1.5)
        self.wash = WaveField(self.rw, self.rh, 43, 20, 0.7, 2.4, 1.15, 0.25, self.scale, 1.2)
        cx, cy = self.cfg["focus"]
        self.key = self.radial(cx, cy, 0.55)

        rng = np.random.default_rng(808)
        self.dust = [dict(x=rng.uniform(0, 1), y=rng.uniform(0, 1),
                          r=rng.uniform(0.002, 0.008), a=rng.uniform(0.15, 0.55),
                          m=int(rng.integers(1, 4)), ph=rng.uniform(0, 2 * np.pi),
                          ax=rng.uniform(0.005, 0.02), ay=rng.uniform(0.005, 0.02))
                     for _ in range(30)]

    def frame(self, p):
        f = self.silk.value(p)
        col = KINA_DARK[None, None, :] + (KINA_MID - KINA_DARK)[None, None, :] * f[..., None]
        # En parlak kıvrımlar şaraba, tepe noktaları altına döner: kumaş hissi.
        top = np.clip((f - 0.62) / 0.38, 0.0, 1.0) ** 1.6
        col = col + (KINA_LIGHT[None, None, :] - col) * (0.85 * top)[..., None]
        # Altın KARIŞTIRARAK değil EKLENEREK giriyor: koyu bordoya altın
        # karıştırmak zeytin yeşili bir çamur üretir; eklemek ise kumaşın
        # üstünde ışık gibi durur, rengi kirletmez.
        col = col + KINA_GOLD[None, None, :] * (0.20 * self.wash.value(p) * self.key * top)[..., None]
        col = col + KINA_GOLD[None, None, :] * (0.16 * sheen(self, p, 0.11) * (0.35 + 0.65 * top))[..., None]
        col = col + (0.06 * self.key)[..., None]

        psi = 2.0 * np.pi * p
        for d in self.dust:
            x = d["x"] + d["ax"] * np.cos(d["m"] * psi + d["ph"])
            y = d["y"] + d["ay"] * np.sin(d["m"] * psi + d["ph"])
            self.glow(col, x, y, d["r"], d["a"] * (0.4 + 0.6 * np.cos(d["m"] * psi) ** 2), KINA_GOLD)

        col = col * (1.0 - 0.32 * smoothstep(0.30, 0.88, self.center_d)[..., None])
        return np.clip(col, 0.0, 1.0)


# ---------------------------------------------------------------------------
# 2) NİŞAN — şampanya ipek
# ---------------------------------------------------------------------------
NISAN_LO = hexc("#e4d8c6")
NISAN_HI = hexc("#fdfaf4")
NISAN_CHAMP = hexc("#e6cfa4")
NISAN_GOLD = hexc("#c9a961")


class NisanSampanya(BaseScene):
    def build(self):
        self.silk = WaveField(self.rw, self.rh, 61, 46, 1.2, 6.5, 1.40, 0.45, self.scale, 1.6)
        self.wash = WaveField(self.rw, self.rh, 67, 18, 0.6, 2.2, 1.10, 0.25, self.scale, 1.2)
        cx, cy = self.cfg["focus"]
        self.key = self.radial(cx, cy, 0.52)

        rng = np.random.default_rng(2024)
        self.dust = [dict(x=rng.uniform(0, 1), y=rng.uniform(0, 1),
                          r=rng.uniform(0.004, 0.016) * self.scale, a=rng.uniform(0.10, 0.32),
                          m=int(rng.integers(1, 3)), ph=rng.uniform(0, 2 * np.pi),
                          ax=rng.uniform(0.006, 0.026), ay=rng.uniform(0.008, 0.030))
                     for _ in range(26)]

    def frame(self, p):
        f = self.silk.value(p)
        col = NISAN_LO[None, None, :] + (NISAN_HI - NISAN_LO)[None, None, :] * smoothstep(0.0, 1.0, f)[..., None]
        champ = np.clip((f - 0.60) / 0.40, 0.0, 1.0) ** 1.7
        col = col + (NISAN_CHAMP[None, None, :] - col) * (0.55 * champ)[..., None]
        col = col + (0.05 * sheen(self, p, 0.15))[..., None]
        col = col + (NISAN_CHAMP[None, None, :] - col) * (0.18 * self.wash.value(p))[..., None]
        col = col + (0.06 * self.key)[..., None]

        psi = 2.0 * np.pi * p
        for d in self.dust:
            x = d["x"] + d["ax"] * np.cos(d["m"] * psi + d["ph"])
            y = d["y"] + d["ay"] * np.sin(d["m"] * psi + d["ph"])
            self.disc(col, x, y, d["r"], d["a"] * (0.55 + 0.45 * np.cos(d["m"] * psi + d["ph"])),
                      NISAN_GOLD, rim=0.45)

        col = col * (1.0 - 0.14 * smoothstep(0.34, 0.90, self.center_d)[..., None])
        return np.clip(col, 0.0, 1.0)


# ---------------------------------------------------------------------------
# 3) SÜNNET — gece mavisi + yıldız tozu
# ---------------------------------------------------------------------------
SUNNET_DEEP = hexc("#060f26")
SUNNET_MID = hexc("#13305f")
SUNNET_GLOW = hexc("#2f5fa8")
SUNNET_GOLD = hexc("#f2d79b")


class SunnetYildiz(BaseScene):
    def build(self):
        self.base = self.vgradient([(0.0, SUNNET_DEEP), (0.55, SUNNET_MID), (1.0, SUNNET_DEEP)])
        cx, cy = self.cfg["focus"]
        self.key = self.radial(cx, cy, 0.42)
        self.neb = WaveField(self.rw, self.rh, 91, 22, 0.7, 2.8, 1.20, 0.30, self.scale, 1.3)

        rng = np.random.default_rng(1453)
        self.stars = [dict(x=rng.uniform(0, 1), y=rng.uniform(0, 1),
                           r=rng.uniform(0.0012, 0.0042), a=rng.uniform(0.25, 0.95),
                           m=int(rng.integers(1, 5)), ph=rng.uniform(0, 2 * np.pi))
                      for _ in range(120)]
        self.big = [dict(x=rng.uniform(0.05, 0.95), y=rng.uniform(0.05, 0.95),
                         r=rng.uniform(0.010, 0.026) * self.scale, a=rng.uniform(0.10, 0.26),
                         m=int(rng.integers(1, 3)), ph=rng.uniform(0, 2 * np.pi))
                    for _ in range(14)]

    def frame(self, p):
        col = self.base.copy()
        col = col + (SUNNET_GLOW[None, None, :] - col) * (0.22 * self.neb.value(p) * self.key)[..., None]
        col = col + (SUNNET_GOLD[None, None, :] - col) * (0.10 * self.key)[..., None]

        psi = 2.0 * np.pi * p
        for s in self.stars:
            # Titreşim: cos^2 hep pozitif, yıldız sönüp yeniden parlar.
            a = s["a"] * (0.25 + 0.75 * np.cos(s["m"] * psi + s["ph"]) ** 2)
            self.glow(col, s["x"], s["y"], s["r"], a, SUNNET_GOLD, sharp=0.9)
        for b in self.big:
            self.disc(col, b["x"], b["y"], b["r"],
                      b["a"] * (0.6 + 0.4 * np.cos(b["m"] * psi + b["ph"])), SUNNET_GLOW, rim=0.35)

        col = col * (1.0 - 0.30 * smoothstep(0.32, 0.90, self.center_d)[..., None])
        return np.clip(col, 0.0, 1.0)


# ---------------------------------------------------------------------------
# 4) DOĞUM GÜNÜ — düşen konfeti
# ---------------------------------------------------------------------------
DG_TOP = hexc("#fffdfa")
DG_MID = hexc("#fdf3ea")
DG_LOW = hexc("#f8e7dc")
CONFETTI = [hexc("#e8705f"), hexc("#f0b429"), hexc("#3fa8a0"), hexc("#8b6bd9"), hexc("#e88fb0")]
WRAP = 1.24


class DogumKonfeti(BaseScene):
    def build(self):
        self.base = self.vgradient([(0.0, DG_TOP), (0.6, DG_MID), (1.0, DG_LOW)])
        cx, cy = self.cfg["focus"]
        self.base = self.base + (0.05 * self.radial(cx, cy, 0.45))[..., None]

        rng = np.random.default_rng(99)
        self.bits = []
        for _ in range(46):
            depth = rng.uniform(0.0, 1.0)
            self.bits.append(dict(
                x=rng.uniform(-0.03, 1.03), y=rng.uniform(0.0, 1.0),
                size=(0.006 + 0.014 * depth) * self.scale,
                ratio=rng.uniform(0.30, 0.62),
                a=0.35 + 0.55 * depth,
                fall=int(rng.integers(1, 3)),
                sway=rng.uniform(0.010, 0.040), ms=int(rng.integers(1, 4)),
                spin=int(rng.integers(1, 5)), ph=rng.uniform(0, 2 * np.pi),
                col=CONFETTI[int(rng.integers(0, len(CONFETTI)))]))

    def frame(self, p):
        col = self.base.copy()
        psi = 2.0 * np.pi * p
        for b in self.bits:
            # Sarma modülü WRAP; döngü başına yol WRAP'in tam katı olmalı.
            y = (b["y"] + b["fall"] * WRAP * p) % WRAP - 0.12
            x = b["x"] + b["sway"] * np.sin(b["ms"] * psi + b["ph"])
            ang = b["spin"] * psi + b["ph"]
            self.quad(col, x, y, b["size"], b["ratio"], ang, b["a"], b["col"],
                      flutter=0.30 + 0.70 * abs(np.cos(ang)))
        return np.clip(col, 0.0, 1.0)


# ---------------------------------------------------------------------------
# 5) MEZUNİYET — lacivert + çapraz ışık süpürmesi
# ---------------------------------------------------------------------------
MZ_DEEP = hexc("#071328")
MZ_MID = hexc("#102a51")
MZ_GOLD = hexc("#f0c761")
MZ_BEAM = hexc("#fff3d6")


class MezuniyetLacivert(BaseScene):
    def build(self):
        self.base = self.vgradient([(0.0, MZ_DEEP), (0.5, MZ_MID), (1.0, MZ_DEEP)])
        cx, cy = self.cfg["focus"]
        self.key = self.radial(cx, cy, 0.50)
        self.haze = WaveField(self.rw, self.rh, 77, 20, 0.6, 2.6, 1.15, 0.30, self.scale, 1.3)

        rng = np.random.default_rng(2026)
        self.motes = [dict(x=rng.uniform(0, 1), y=rng.uniform(0, 1),
                           r=rng.uniform(0.0016, 0.0060), a=rng.uniform(0.20, 0.70),
                           rise=int(rng.integers(1, 3)), sway=rng.uniform(0.006, 0.026),
                           ms=int(rng.integers(1, 4)), ph=rng.uniform(0, 2 * np.pi))
                      for _ in range(54)]

    def frame(self, p):
        col = self.base.copy()
        col = col + (MZ_MID[None, None, :] - col) * (0.30 * self.haze.value(p))[..., None]
        # İki bant zıt yönde süpürür: tören ışığı hissi, tek bantta monotonluk olurdu.
        # Eklenerek ve DAR uygulanır: geniş bir altın bant lacivert üzerinde
        # gri-kahve bir lekeye dönüşür; dar ve parlak olan ise ışık huzmesi
        # gibi okunur. Renk de doygun altın değil sıcak beyaz.
        col = col + MZ_BEAM[None, None, :] * (0.20 * sheen(self, p, 0.045, 0.25))[..., None]
        col = col + MZ_BEAM[None, None, :] * (0.08 * sheen(self, p, 0.10, 0.25))[..., None]
        col = col + (0.06 * self.key)[..., None]

        psi = 2.0 * np.pi * p
        for m in self.motes:
            y = (m["y"] - m["rise"] * WRAP * p) % WRAP - 0.12
            x = m["x"] + m["sway"] * np.sin(m["ms"] * psi + m["ph"])
            self.glow(col, x, y, m["r"], m["a"] * (0.35 + 0.65 * np.cos(m["ms"] * psi + m["ph"]) ** 2),
                      MZ_GOLD, sharp=1.0)

        col = col * (1.0 - 0.28 * smoothstep(0.32, 0.90, self.center_d)[..., None])
        return np.clip(col, 0.0, 1.0)


# ---------------------------------------------------------------------------
# 6) BABY SHOWER — pastel degrade + yükselen kabarcıklar
# ---------------------------------------------------------------------------
BB_TOP = hexc("#eaf6f3")
BB_MID = hexc("#fdf5ec")
BB_LOW = hexc("#fbe6e4")
BB_MINT = hexc("#bfe3da")
BB_PEACH = hexc("#f7cfc0")
BB_WHITE = hexc("#ffffff")


class BabyKabarcik(BaseScene):
    def build(self):
        self.base = self.vgradient([(0.0, BB_TOP), (0.52, BB_MID), (1.0, BB_LOW)])
        self.wash = WaveField(self.rw, self.rh, 33, 18, 0.6, 2.2, 1.10, 0.30, self.scale, 1.3)

        rng = np.random.default_rng(777)
        self.bubbles = []
        for _ in range(30):
            depth = rng.uniform(0.0, 1.0)
            self.bubbles.append(dict(
                x=rng.uniform(0.02, 0.98), y=rng.uniform(0.0, 1.0),
                r=(0.012 + 0.055 * depth) * self.scale,
                a=0.10 + 0.26 * depth,
                rise=int(rng.integers(1, 3)),
                sway=rng.uniform(0.008, 0.032), ms=int(rng.integers(1, 4)),
                ph=rng.uniform(0, 2 * np.pi),
                col=BB_MINT if rng.random() < 0.5 else BB_PEACH))

    def frame(self, p):
        col = self.base.copy()
        col = col + (BB_MINT[None, None, :] - col) * (0.12 * self.wash.value(p))[..., None]

        psi = 2.0 * np.pi * p
        for b in self.bubbles:
            y = (b["y"] - b["rise"] * WRAP * p) % WRAP - 0.12
            x = b["x"] + b["sway"] * np.sin(b["ms"] * psi + b["ph"])
            self.disc(col, x, y, b["r"], b["a"], b["col"], rim=0.85)
            # Küçük ışık noktası kabarcığa cam hissi verir.
            self.glow(col, x - b["r"] * 0.35, y - b["r"] * 0.35, b["r"] * 0.18,
                      b["a"] * 1.4, BB_WHITE)
        return np.clip(col, 0.0, 1.0)


# ---------------------------------------------------------------------------
# 7) PARTİ — neon aurora
# ---------------------------------------------------------------------------
PT_BG = hexc("#06060c")
PT_MAGENTA = hexc("#ff3fa4")
PT_CYAN = hexc("#35e0ff")
PT_VIOLET = hexc("#8b5cff")


class PartiNeonAurora(BaseScene):
    def build(self):
        self.base = self.vgradient([(0.0, PT_BG), (1.0, hexc("#0b0a16"))])
        s = self.scale
        self.a1 = WaveField(self.rw, self.rh, 11, 30, 1.0, 4.0, 1.30, 0.50, s, 2.2)
        self.a2 = WaveField(self.rw, self.rh, 22, 30, 1.4, 5.5, 1.35, -0.50, s, 2.4)
        self.a3 = WaveField(self.rw, self.rh, 33, 24, 0.8, 3.0, 1.20, 0.25, s, 2.0)
        self.clear_center = 0.22 + 0.78 * smoothstep(0.12, 0.52, self.center_d)
        rng = np.random.default_rng(606)
        self.glints = [dict(x=rng.uniform(0, 1), y=rng.uniform(0, 1),
                            r=rng.uniform(0.0015, 0.005), a=rng.uniform(0.25, 0.8),
                            m=int(rng.integers(1, 5)), ph=rng.uniform(0, 2 * np.pi))
                       for _ in range(34)]

    def _ribbon(self, field, p, width, color, gain):
        # Alanın 0.5 seviyesine yakınlığı ince bir şerit üretir; ekleyerek
        # (additive) bindirince neon ışık üst üste binmiş gibi parlar.
        # clear_center: şeritler merkeze yaklaşınca söner, isimler okunur kalır.
        band = np.exp(-((field.value(p) - 0.5) ** 2) / (2 * width ** 2))
        return (band * gain * self.clear_center)[..., None] * color[None, None, :]

    def frame(self, p):
        col = self.base.copy()
        col = col + self._ribbon(self.a1, p, 0.060, PT_MAGENTA, 0.55)
        col = col + self._ribbon(self.a2, p, 0.052, PT_CYAN, 0.45)
        col = col + self._ribbon(self.a3, p, 0.090, PT_VIOLET, 0.28)

        psi = 2.0 * np.pi * p
        for g in self.glints:
            self.glow(col, g["x"], g["y"], g["r"],
                      g["a"] * (0.2 + 0.8 * np.cos(g["m"] * psi + g["ph"]) ** 2), hexc("#ffffff"))

        col = col * (1.0 - 0.34 * smoothstep(0.30, 0.90, self.center_d)[..., None])
        return np.clip(col, 0.0, 1.0)


CONCEPTS = {
    "kina-bordo": dict(cls=KinaBordo, variants=variants((0.50, 0.48), (0.50, 0.46))),
    "nisan-sampanya": dict(cls=NisanSampanya, variants=variants((0.50, 0.45), (0.50, 0.42))),
    "sunnet-yildiz": dict(cls=SunnetYildiz, variants=variants((0.50, 0.72), (0.50, 0.70))),
    "dogum-konfeti": dict(cls=DogumKonfeti, variants=variants((0.50, 0.35), (0.50, 0.32))),
    "mezuniyet-lacivert": dict(cls=MezuniyetLacivert, variants=variants((0.50, 0.55), (0.50, 0.52))),
    "baby-kabarcik": dict(cls=BabyKabarcik, variants=variants((0.50, 0.50), (0.50, 0.50))),
    "parti-neon": dict(cls=PartiNeonAurora, variants=variants((0.50, 0.50), (0.50, 0.50))),
}


if __name__ == "__main__":
    run_cli(CONCEPTS)
