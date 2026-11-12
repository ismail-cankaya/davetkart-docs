#!/usr/bin/env python3
"""
DavetKart - Düğün davetiyeleri için prosedürel arka plan videosu üreteci.

Konseptler:
  mum-isigi     : koyu gece, süzülen altın bokeh (akşam nikâhı)
  gul-yapraklari: pudra zemin, düşen gül yaprakları (klasik romantik)
  deniz-isiltisi: akvamarin su yüzeyi kaustikleri (kıyı düğünü)

Her konsept iki bağımsız kompozisyon üretir: 1280x720 (yatay) ve 720x1280
(dikey). Telefonda yatay videoyu kırpmak kadrajın ~%65'ini yok ederdi.

DÖNGÜ GARANTİSİ: tüm zaman terimleri cos/sin(2*pi*m*p) biçiminde, m tam sayı;
düşen yapraklarda ise konum (y0 + k*p) mod 1 ile sarılır, k tam sayı.
Böylece i=0 ve i=N kareleri özdeştir -> dikiş yok.
"""

import argparse
import subprocess
import sys

import numpy as np
from PIL import Image

FPS = 24
DUR = 10
N = FPS * DUR                      # 240 kare


def hexc(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255.0


def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


# ---------------------------------------------------------------------------
# Ortak dalga alanı motoru (ipek/su/sis dokuları buradan çıkar)
# ---------------------------------------------------------------------------
class WaveField:
    """
    field(p) = SUM_k a_k * cos(theta_k + 2*pi*m_k*p)

    Uzaysal faz bir kez hesaplanır; kare başına iş iki küçük matris çarpımına
    düşer. m_k = round(kx * drift) seçimi, alanın döngü başına 'drift' kadar
    ekran genişliği kaymasını sağlar - dalga boyundan bağımsız, dolayısıyla
    büyük kütleler sabit kalırken orta ölçek akar (derinlik hissi).
    """

    def __init__(self, rw, rh, seed, n_waves, k_lo, k_hi, exponent, drift,
                 scale=1.0, y_squash=1.0):
        rng = np.random.default_rng(seed)
        xs = np.linspace(0.0, 1.0, rw, endpoint=False, dtype=np.float32)
        ys = np.linspace(0.0, 1.0, rh, endpoint=False, dtype=np.float32) * (rh / rw)
        X, Y = np.meshgrid(xs, ys)

        cos_bank, sin_bank, ms = [], [], []
        for _ in range(n_waves):
            k = float(np.exp(rng.uniform(np.log(k_lo), np.log(k_hi)))) * scale
            ang = rng.uniform(0.0, 2.0 * np.pi)
            kx, ky = k * np.cos(ang), k * np.sin(ang) * y_squash
            phase = rng.uniform(0.0, 2.0 * np.pi)
            amp = k ** (-exponent)

            theta = 2.0 * np.pi * (kx * X + ky * Y) + phase
            cos_bank.append((amp * np.cos(theta)).astype(np.float32))
            sin_bank.append((amp * np.sin(theta)).astype(np.float32))
            ms.append(int(np.round(kx * drift)))

        self.shape = (rh, rw)
        self.C = np.stack(cos_bank).reshape(n_waves, -1)
        self.S = np.stack(sin_bank).reshape(n_waves, -1)
        self.m = np.array(ms, dtype=np.float32)
        samples = np.concatenate([self._raw(p) for p in (0.0, 0.31, 0.67)])
        self.norm = float(samples.std()) * 2.6 + 1e-6

    def _raw(self, p: float) -> np.ndarray:
        psi = 2.0 * np.pi * self.m * p
        return np.cos(psi) @ self.C - np.sin(psi) @ self.S

    def value(self, p: float) -> np.ndarray:
        v = self._raw(p) / self.norm
        return np.clip(0.5 + 0.5 * v, 0.0, 1.0).reshape(self.shape)


# ---------------------------------------------------------------------------
# Ortak sahne iskeleti
# ---------------------------------------------------------------------------
class BaseScene:
    def __init__(self, cfg):
        self.cfg = cfg
        self.rw, self.rh = cfg["render"]
        self.out_w, self.out_h = cfg["out"]
        xs = np.linspace(0.0, 1.0, self.rw, endpoint=False, dtype=np.float32)
        ys = np.linspace(0.0, 1.0, self.rh, endpoint=False, dtype=np.float32)
        self.X, self.Y = np.meshgrid(xs, ys)
        self.aspect = self.rh / self.rw
        self.Yiso = self.Y * self.aspect
        cd = np.sqrt((self.X - 0.5) ** 2 + (self.Yiso - 0.5 * self.aspect) ** 2)
        self.center_d = cd / max(1.0, self.aspect)
        self.grain_rng = np.random.default_rng(7777)
        self.grain = cfg.get("grain", 1.9)
        self.build()

    def build(self) -> None:
        raise NotImplementedError

    def frame(self, p: float) -> np.ndarray:
        raise NotImplementedError

    # -- yardımcı: yerel pencerede yumuşak leke ---------------------------
    def _window(self, cx, cy, rx, ry):
        px, py = cx * self.rw, cy * self.rh
        x0, x1 = int(max(0, px - rx)), int(min(self.rw, px + rx + 1))
        y0, y1 = int(max(0, py - ry)), int(min(self.rh, py + ry + 1))
        if x1 <= x0 or y1 <= y0:
            return None
        gx = np.arange(x0, x1, dtype=np.float32) - px
        gy = np.arange(y0, y1, dtype=np.float32) - py
        return x0, x1, y0, y1, gx, gy


# ---------------------------------------------------------------------------
# 1) MUM IŞIĞI — koyu gece, altın bokeh
# ---------------------------------------------------------------------------
NIGHT_DEEP = hexc("#080b12")
NIGHT_WARM = hexc("#2a1d13")
CANDLE = hexc("#f4cf94")
EMBER = hexc("#d99b4e")


class MumIsigi(BaseScene):
    def build(self):
        cx, cy = self.cfg["focus"]
        d = np.sqrt((self.X - cx) ** 2 + (self.Yiso - cy * self.aspect) ** 2)
        warm = np.exp(-(d / 0.52) ** 2) * 0.78
        self.base = NIGHT_DEEP[None, None, :] + (NIGHT_WARM - NIGHT_DEEP)[None, None, :] * warm[..., None]
        self.base = self.base + (EMBER[None, None, :] - self.base) * (0.13 * np.exp(-(d / 0.26) ** 2))[..., None]
        self.haze = WaveField(self.rw, self.rh, 5, 22, 0.7, 2.4, 1.2, 0.30,
                              self.cfg["scale"], 1.4)

        rng = np.random.default_rng(1907)
        self.discs = []
        for _ in range(34):
            self.discs.append(dict(
                x=rng.uniform(-0.05, 1.05), y=rng.uniform(-0.05, 1.05),
                r=rng.uniform(0.010, 0.068) * self.cfg["scale"],
                a=rng.uniform(0.06, 0.26),
                ax=rng.uniform(0.008, 0.035), ay=rng.uniform(0.010, 0.045),
                mx=int(rng.integers(1, 3)), my=int(rng.integers(1, 3)),
                ph=rng.uniform(0, 2 * np.pi), pulse=int(rng.integers(1, 3)),
                tint=rng.uniform(0.0, 1.0)))

        # Keskin kıvılcımlar: defokus disklerin arasına birkaç net nokta
        # koymak sahneye "mum alevi" okunurluğu katar.
        self.sparks = []
        for _ in range(16):
            self.sparks.append(dict(
                x=rng.uniform(0.03, 0.97), y=rng.uniform(0.03, 0.97),
                r=rng.uniform(0.0018, 0.0045), a=rng.uniform(0.30, 0.75),
                m=int(rng.integers(1, 4)), ph=rng.uniform(0, 2 * np.pi)))

    def frame(self, p):
        img = self.base.copy()
        img = img + (EMBER[None, None, :] - img) * (0.05 * self.haze.value(p))[..., None]
        psi = 2.0 * np.pi * p

        for d in self.discs:
            cx = d["x"] + d["ax"] * np.cos(d["mx"] * psi + d["ph"])
            cy = d["y"] + d["ay"] * np.sin(d["my"] * psi + d["ph"])
            # Metin alanı temiz kalsın: bokeh merkeze yaklaştıkça söner.
            edge = smoothstep(0.14, 0.60, float(np.hypot(cx - 0.5, cy - 0.5)))
            alpha = d["a"] * (0.15 + 0.85 * edge) * (0.82 + 0.18 * np.cos(d["pulse"] * psi + d["ph"]))
            self._bokeh(img, cx, cy, d["r"], alpha, d["tint"])

        for s in self.sparks:
            edge = smoothstep(0.14, 0.60, float(np.hypot(s["x"] - 0.5, s["y"] - 0.5)))
            amp = s["a"] * edge * (0.45 + 0.55 * np.cos(s["m"] * psi + s["ph"]) ** 2)
            self._spark(img, s["x"], s["y"], s["r"], amp)

        img = img * (1.0 - 0.34 * smoothstep(0.28, 0.85, self.center_d)[..., None])
        return np.clip(img, 0.0, 1.0)

    def _spark(self, img, cx, cy, r, a):
        rad = max(1.2, r * self.rw)
        win = self._window(cx, cy, rad * 4.0, rad * 4.0)
        if win is None:
            return
        x0, x1, y0, y1, gx, gy = win
        d2 = (gx[None, :] ** 2 + gy[:, None] ** 2) / (rad * rad)
        g = np.exp(-d2 * 0.9) * a
        patch = img[y0:y1, x0:x1]
        img[y0:y1, x0:x1] = patch + (CANDLE[None, None, :] - patch) * g[..., None]

    def _bokeh(self, img, cx, cy, r, a, tint):
        rad = r * self.rw
        win = self._window(cx, cy, rad * 1.35, rad * 1.35)
        if win is None:
            return
        x0, x1, y0, y1, gx, gy = win
        dist = np.sqrt(gx[None, :] ** 2 + gy[:, None] ** 2) / rad
        # Gerçek defokus diskinin kenarı içinden hafif parlaktır (rim).
        core = 1.0 - smoothstep(0.72, 1.02, dist)
        rim = np.exp(-((dist - 0.88) / 0.16) ** 2) * 0.55
        g = np.clip(core + rim, 0.0, 1.4) * a
        col = CANDLE * (1.0 - 0.35 * tint) + EMBER * (0.35 * tint)
        patch = img[y0:y1, x0:x1]
        img[y0:y1, x0:x1] = patch + (col[None, None, :] - patch) * g[..., None]


# ---------------------------------------------------------------------------
# 2) GÜL YAPRAKLARI — pudra zemin, düşen yapraklar
# ---------------------------------------------------------------------------
PETAL_TOP = hexc("#fdf4f2")
PETAL_MID = hexc("#f9e3e1")
PETAL_LOW = hexc("#f2d5d2")
PETAL_COLORS = [hexc("#e7a3a9"), hexc("#dc8f97"), hexc("#f0c3c4"), hexc("#c97d88")]


class GulYapraklari(BaseScene):
    def build(self):
        upper = PETAL_TOP[None, None, :] + (PETAL_MID - PETAL_TOP)[None, None, :] * smoothstep(0.0, 0.65, self.Y)[..., None]
        self.base = upper + (PETAL_LOW - upper) * smoothstep(0.55, 1.0, self.Y)[..., None]
        cx, cy = self.cfg["focus"]
        d = np.sqrt((self.X - cx) ** 2 + (self.Yiso - cy * self.aspect) ** 2)
        self.base = self.base + (0.055 * np.exp(-(d / 0.45) ** 2))[..., None]
        self.silk = WaveField(self.rw, self.rh, 13, 26, 1.0, 4.0, 1.3, 0.40,
                              self.cfg["scale"], 1.6)

        rng = np.random.default_rng(524)
        self.petals = []
        for _ in range(34):
            depth = rng.uniform(0.0, 1.0)          # 0 uzak, 1 yakın
            self.petals.append(dict(
                x=rng.uniform(-0.05, 1.05), y=rng.uniform(0.0, 1.0),
                size=(0.016 + 0.040 * depth) * self.cfg["scale"],
                a=0.26 + 0.52 * depth,
                fall=int(rng.integers(1, 3)),       # döngü başına tam tur sayısı
                sway=rng.uniform(0.012, 0.045),
                ms=int(rng.integers(1, 4)),
                spin=int(rng.integers(1, 4)),
                tilt=rng.uniform(-0.5, 0.5),
                ph=rng.uniform(0, 2 * np.pi),
                col=PETAL_COLORS[int(rng.integers(0, len(PETAL_COLORS)))],
                soft=0.50 - 0.34 * depth))

    def frame(self, p):
        img = self.base.copy()
        img = img + (PETAL_TOP[None, None, :] - img) * (0.10 * self.silk.value(p))[..., None]

        psi = 2.0 * np.pi * p
        for q in self.petals:
            # Sarma modülü 1.24 olduğu için döngü başına alınan yol da 1.24'ün
            # tam katı olmalı; yoksa p=1'de yapraklar sıçrar (döngü dikişi).
            y = (q["y"] + q["fall"] * 1.24 * p) % 1.24 - 0.12
            x = q["x"] + q["sway"] * np.sin(q["ms"] * psi + q["ph"])
            self._petal(img, x, y, q, psi)
        return np.clip(img, 0.0, 1.0)

    def _petal(self, img, cx, cy, q, psi):
        rad = q["size"] * self.rw
        win = self._window(cx, cy, rad * 1.3, rad * 1.3)
        if win is None:
            return
        x0, x1, y0, y1, gx, gy = win

        # Yaprağın düzlem içi dönüşü + genişliğin |cos| ile daralması
        # (kendi ekseninde çırpınma). İkisi de tam sayı harmonikte döner.
        ang = q["spin"] * psi + q["ph"] + q["tilt"]
        ca, sa = np.cos(ang), np.sin(ang)
        flutter = 0.30 + 0.70 * abs(np.cos(ang))

        v = (gx[None, :] * sa + gy[:, None] * ca) / rad            # uzun eksen
        u = (gx[None, :] * ca - gy[:, None] * sa) / (rad * 0.62 * flutter)

        # Gül yaprağı profili: uçta sivri, tabanda geniş ve yuvarlak.
        width = np.sqrt(np.clip(1.0 - v * v, 0.0, 1.0)) * (0.58 + 0.42 * (v + 1.0) * 0.5)
        t = np.abs(u) / (width + 1e-3)
        g = (1.0 - smoothstep(1.0 - q["soft"], 1.0, t)) * (1.0 - smoothstep(0.92, 1.0, np.abs(v)))

        # Hafif hacim: bir yan aydınlık, diğer yan gölgeli — düz leke olmasın.
        shade = np.clip(0.82 + 0.30 * np.clip(u, -1.0, 1.0), 0.0, 1.25)
        col = np.clip(q["col"][None, None, :] * shade[..., None], 0.0, 1.0)

        a = (g * q["a"])[..., None]
        patch = img[y0:y1, x0:x1]
        img[y0:y1, x0:x1] = patch + (col - patch) * a


# ---------------------------------------------------------------------------
# 3) DENİZ IŞILTISI — su yüzeyi kaustikleri
# ---------------------------------------------------------------------------
SEA_TOP = hexc("#f2fbfa")
SEA_MID = hexc("#cfe8e6")
SEA_LOW = hexc("#a9d2d2")
CAUSTIC = hexc("#ffffff")
SEA_GOLD = hexc("#f6e3bd")


class DenizIsiltisi(BaseScene):
    def build(self):
        upper = SEA_TOP[None, None, :] + (SEA_MID - SEA_TOP)[None, None, :] * smoothstep(0.0, 0.62, self.Y)[..., None]
        self.base = upper + (SEA_LOW - upper) * smoothstep(0.52, 1.0, self.Y)[..., None]
        s = self.cfg["scale"]
        # İki bağımsız alan: kaustik ağı bunların sıfır kümelerinin
        # kesişiminden doğar, tek alanla düz çizgiler çıkardı.
        self.f1 = WaveField(self.rw, self.rh, 71, 40, 1.6, 7.0, 1.25, 0.50, s, 1.3)
        self.f2 = WaveField(self.rw, self.rh, 89, 40, 2.2, 9.0, 1.30, -0.50, s, 1.3)
        self.deep = WaveField(self.rw, self.rh, 97, 18, 0.6, 2.0, 1.10, 0.25, s, 1.2)

        rng = np.random.default_rng(3131)
        self.glints = []
        for _ in range(26):
            self.glints.append(dict(
                x=rng.uniform(0.02, 0.98), y=rng.uniform(0.05, 0.98),
                r=rng.uniform(0.004, 0.012) * s, a=rng.uniform(0.25, 0.65),
                m=int(rng.integers(1, 4)), ph=rng.uniform(0, 2 * np.pi)))

    def frame(self, p):
        img = self.base.copy()
        img = img + (SEA_LOW[None, None, :] - img) * (0.18 * self.deep.value(p))[..., None]

        # Kaustik: alanın 0.5 seviyesine yakınlığı ince parlak bantlar üretir.
        a = np.exp(-((self.f1.value(p) - 0.5) ** 2) / (2 * 0.045 ** 2))
        b = np.exp(-((self.f2.value(p) - 0.5) ** 2) / (2 * 0.055 ** 2))
        web = np.clip(a * 0.75 + b * 0.55 + a * b * 1.10, 0.0, 1.35)
        depth_mask = 0.35 + 0.65 * smoothstep(0.15, 0.85, self.Y)
        img = img + (CAUSTIC[None, None, :] - img) * (0.55 * web * depth_mask)[..., None]
        img = img + (SEA_GOLD[None, None, :] - img) * (0.18 * web * (1.0 - depth_mask))[..., None]

        psi = 2.0 * np.pi * p
        for g in self.glints:
            amp = g["a"] * (0.5 + 0.5 * np.cos(g["m"] * psi + g["ph"]))
            self._glint(img, g["x"], g["y"], g["r"], amp)

        img = img * (1.0 - 0.12 * smoothstep(0.34, 0.86, self.center_d)[..., None])
        return np.clip(img, 0.0, 1.0)

    def _glint(self, img, cx, cy, r, a):
        rad = max(1.5, r * self.rw)
        win = self._window(cx, cy, rad * 3.0, rad * 3.0)
        if win is None:
            return
        x0, x1, y0, y1, gx, gy = win
        d2 = (gx[None, :] ** 2 + gy[:, None] ** 2) / (rad * rad)
        g = np.exp(-d2 * 1.3) * a
        patch = img[y0:y1, x0:x1]
        img[y0:y1, x0:x1] = patch + (CAUSTIC[None, None, :] - patch) * g[..., None]


# ---------------------------------------------------------------------------
# Konsept / varyant kayıtları
# ---------------------------------------------------------------------------
def variants(focus_landscape, focus_portrait, scale_portrait=0.62):
    return {
        "desktop": dict(out=(1280, 720), render=(640, 360), focus=focus_landscape, scale=1.0),
        "mobile": dict(out=(720, 1280), render=(360, 640), focus=focus_portrait, scale=scale_portrait),
    }


CONCEPTS = {
    "mum-isigi": dict(cls=MumIsigi, variants=variants((0.50, 0.62), (0.50, 0.58))),
    "gul-yapraklari": dict(cls=GulYapraklari, variants=variants((0.50, 0.28), (0.50, 0.24))),
    "deniz-isiltisi": dict(cls=DenizIsiltisi, variants=variants((0.50, 0.50), (0.50, 0.50))),
}


def scene_of(concept: str, variant: str) -> BaseScene:
    entry = CONCEPTS[concept]
    return entry["cls"](entry["variants"][variant])


def to_bytes(scene: BaseScene, img: np.ndarray) -> bytes:
    small = Image.fromarray((img * 255.0 + 0.5).astype(np.uint8), "RGB")
    big = small.resize((scene.out_w, scene.out_h), Image.LANCZOS)
    arr = np.asarray(big, dtype=np.float32)
    # İnce film graini gradyan halkalanmasını (banding) kırar.
    noise = scene.grain_rng.normal(0.0, scene.grain, size=arr.shape[:2]).astype(np.float32)
    return np.clip(arr + noise[..., None], 0, 255).astype(np.uint8).tobytes()


def preview(concept: str, variant: str, outdir: str) -> None:
    scene = scene_of(concept, variant)
    for idx in (0, 72, 144, 216):
        Image.frombytes("RGB", (scene.out_w, scene.out_h),
                        to_bytes(scene, scene.frame(idx / N))).save(
            f"{outdir}/prev-{concept}-{variant}-{idx:03d}.png")
    print(f"[{concept}/{variant}] onizleme yazildi")


def write_raw(concept: str, variant: str, raw_path: str, start: int, end: int) -> None:
    scene = scene_of(concept, variant)
    with open(raw_path, "wb" if start == 0 else "ab") as fh:
        for i in range(start, end):
            fh.write(to_bytes(scene, scene.frame(i / N)))
    print(f"[{concept}/{variant}] {start}-{end} yazildi")


def encode(concept: str, variant: str, raw_path: str, outdir: str) -> None:
    w, h = CONCEPTS[concept]["variants"][variant]["out"]
    src = ["-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
           "-r", str(FPS), "-i", raw_path]
    base = f"{outdir}/{concept}-{variant}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *src,
                    "-c:v", "libx264", "-profile:v", "high", "-level", "4.0",
                    "-preset", "slow", "-crf", "24", "-pix_fmt", "yuv420p",
                    "-g", str(FPS * 5), "-movflags", "+faststart", "-an",
                    f"{base}.mp4"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *src,
                    "-c:v", "libvpx-vp9", "-crf", "36", "-b:v", "0",
                    "-deadline", "good", "-cpu-used", "3", "-row-mt", "1",
                    "-pix_fmt", "yuv420p", "-an", f"{base}.webm"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *src,
                    "-frames:v", "1", "-q:v", "6", f"{base}-poster.jpg"], check=True)
    print(f"[{concept}/{variant}] tamam")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--concept", choices=list(CONCEPTS), required=True)
    ap.add_argument("--variant", choices=["desktop", "mobile"], default="desktop")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--raw", default=None)
    ap.add_argument("--frames", default=None, help="START:END")
    ap.add_argument("--encode", action="store_true")
    args = ap.parse_args()

    if args.preview:
        preview(args.concept, args.variant, args.outdir)
    elif args.frames:
        a, b = (int(x) for x in args.frames.split(":"))
        write_raw(args.concept, args.variant, args.raw, a, min(b, N))
    elif args.encode:
        encode(args.concept, args.variant, args.raw, args.outdir)
    else:
        sys.exit("--preview | --frames | --encode secilmeli")
