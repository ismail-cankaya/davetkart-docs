#!/usr/bin/env python3
"""
DavetKart - prosedürel arka plan videosu motoru (konseptlerden bağımsız).

Bu dosya "nasıl üretilir"i bilir: dalga alanı, parçacık çizimi, kare yazımı,
kodlama, komut satırı. "Ne üretilir"i (renk, kompozisyon, hareket) bilmez -
onu konsept dosyaları söyler. Tek Sorumluluk İlkesi'nin dosya düzeyindeki
karşılığı; yeni bir konsept eklemek motoru hiç değiştirmez.

DÖNGÜ SÖZLEŞMESİ
----------------
Zamana bağlı her terim cos/sin(2*pi*m*p) biçiminde olmalı ve m TAM SAYI
olmalıdır (p = i/N). Sarmalı hareketlerde (düşen parçacık) döngü başına
alınan yol, sarma modülünün tam katı olmalıdır. Bu iki kural tutulursa
i=0 ve i=N kareleri özdeş olur; video sonsuz döner, dikiş görünmez.
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


def smoothstep(edge0: float, edge1: float, x):
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


# ---------------------------------------------------------------------------
# Dalga alanı: ipek, su, sis, aurora dokularının tamamı buradan çıkar
# ---------------------------------------------------------------------------
class WaveField:
    """
    field(p) = SUM_k a_k * cos(theta_k + 2*pi*m_k*p)

    Uzaysal faz bir kez hesaplanır, kare başına iş iki matris çarpımına düşer.
    m_k = round(kx * drift) seçimi alanın döngü başına 'drift' kadar ekran
    genişliği kaymasını sağlar; en büyük kütleler sabit kalır (derinlik).
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
# Sahne iskeleti + ortak çizim ilkelleri
# ---------------------------------------------------------------------------
class BaseScene:
    def __init__(self, cfg):
        self.cfg = cfg
        self.rw, self.rh = cfg["render"]
        self.out_w, self.out_h = cfg["out"]
        self.scale = cfg.get("scale", 1.0)
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

    # -- yardımcılar -----------------------------------------------------
    def vgradient(self, stops):
        """[(konum, renk)] listesinden dikey degrade üretir."""
        out = np.repeat(np.repeat(stops[0][1][None, None, :], self.rh, 0), self.rw, 1)
        for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
            t = smoothstep(p0, p1, self.Y)[..., None]
            out = out + (c1[None, None, :] - out) * t
        return out.astype(np.float32)

    def radial(self, cx, cy, radius):
        d = np.sqrt((self.X - cx) ** 2 + (self.Yiso - cy * self.aspect) ** 2)
        return np.exp(-(d / radius) ** 2)

    def _window(self, cx, cy, rx, ry):
        px, py = cx * self.rw, cy * self.rh
        x0, x1 = int(max(0, px - rx)), int(min(self.rw, px + rx + 1))
        y0, y1 = int(max(0, py - ry)), int(min(self.rh, py + ry + 1))
        if x1 <= x0 or y1 <= y0:
            return None
        gx = np.arange(x0, x1, dtype=np.float32) - px
        gy = np.arange(y0, y1, dtype=np.float32) - py
        return x0, x1, y0, y1, gx, gy

    def _paint(self, img, box, g, color):
        x0, x1, y0, y1 = box
        patch = img[y0:y1, x0:x1]
        img[y0:y1, x0:x1] = patch + (color[None, None, :] - patch) * g[..., None]

    def glow(self, img, cx, cy, r, a, color, sharp=1.3):
        """Yumuşak ışık zerresi (gauss)."""
        rad = max(1.2, r * self.rw)
        win = self._window(cx, cy, rad * 3.2, rad * 3.2)
        if win is None:
            return
        x0, x1, y0, y1, gx, gy = win
        d2 = (gx[None, :] ** 2 + gy[:, None] ** 2) / (rad * rad)
        self._paint(img, (x0, x1, y0, y1), np.exp(-d2 * sharp) * a, color)

    def disc(self, img, cx, cy, r, a, color, rim=0.55):
        """Odaktan çıkmış ışık dairesi: kenarı içinden parlaktır (bokeh)."""
        rad = max(1.0, r * self.rw)
        win = self._window(cx, cy, rad * 1.35, rad * 1.35)
        if win is None:
            return
        x0, x1, y0, y1, gx, gy = win
        dist = np.sqrt(gx[None, :] ** 2 + gy[:, None] ** 2) / rad
        core = 1.0 - smoothstep(0.72, 1.02, dist)
        ring = np.exp(-((dist - 0.88) / 0.16) ** 2) * rim
        self._paint(img, (x0, x1, y0, y1), np.clip(core + ring, 0.0, 1.4) * a, color)

    def quad(self, img, cx, cy, size, ratio, ang, a, color, flutter=1.0):
        """Dönen dikdörtgen parça (konfeti/yaprak gövdesi)."""
        rad = max(1.0, size * self.rw)
        win = self._window(cx, cy, rad * 1.5, rad * 1.5)
        if win is None:
            return
        x0, x1, y0, y1, gx, gy = win
        ca, sa = np.cos(ang), np.sin(ang)
        u = np.abs(gx[None, :] * ca - gy[:, None] * sa) / (rad * ratio * flutter + 1e-3)
        v = np.abs(gx[None, :] * sa + gy[:, None] * ca) / rad
        g = (1.0 - smoothstep(0.78, 1.0, u)) * (1.0 - smoothstep(0.78, 1.0, v))
        self._paint(img, (x0, x1, y0, y1), g * a, color)


# ---------------------------------------------------------------------------
# Varyant kayıtları + komut satırı
# ---------------------------------------------------------------------------
def variants(focus_landscape, focus_portrait, scale_portrait=0.62):
    return {
        "desktop": dict(out=(1280, 720), render=(640, 360), focus=focus_landscape, scale=1.0),
        "mobile": dict(out=(720, 1280), render=(360, 640), focus=focus_portrait, scale=scale_portrait),
    }


def scene_of(concepts, concept, variant):
    entry = concepts[concept]
    return entry["cls"](entry["variants"][variant])


def to_bytes(scene, img):
    small = Image.fromarray((img * 255.0 + 0.5).astype(np.uint8), "RGB")
    big = small.resize((scene.out_w, scene.out_h), Image.LANCZOS)
    arr = np.asarray(big, dtype=np.float32)
    # İnce film graini gradyan halkalanmasını (banding) kırar.
    noise = scene.grain_rng.normal(0.0, scene.grain, size=arr.shape[:2]).astype(np.float32)
    return np.clip(arr + noise[..., None], 0, 255).astype(np.uint8).tobytes()


def preview(concepts, concept, variant, outdir):
    scene = scene_of(concepts, concept, variant)
    for idx in (0, 60, 120, 180):
        Image.frombytes("RGB", (scene.out_w, scene.out_h),
                        to_bytes(scene, scene.frame(idx / N))).save(
            f"{outdir}/prev-{concept}-{variant}-{idx:03d}.png")
    print(f"[{concept}/{variant}] onizleme yazildi")


def write_raw(concepts, concept, variant, raw_path, start, end):
    """Kareler bağımsız olduğu için iş parçalara bölünebilir (yeniden başlatılabilir)."""
    scene = scene_of(concepts, concept, variant)
    with open(raw_path, "wb" if start == 0 else "ab") as fh:
        for i in range(start, end):
            fh.write(to_bytes(scene, scene.frame(i / N)))
    print(f"[{concept}/{variant}] {start}-{end} yazildi")


def encode(concepts, concept, variant, raw_path, outdir):
    w, h = concepts[concept]["variants"][variant]["out"]
    src = ["-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(FPS), "-i", raw_path]
    base = f"{outdir}/{concept}-{variant}"
    # H.264 birincil: her telefonda donanımda çözülür (pil, ısı).
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


def seam_report(concepts):
    """Döngü dikişini sayısal olarak ölçer: 0 ile 1 aynı kare olmalı."""
    for name in concepts:
        scene = scene_of(concepts, name, "desktop")
        gap = float(np.abs(scene.frame(0.0) - scene.frame(1.0)).max())
        step = float(np.abs(scene.frame(1 / N) - scene.frame(0.0)).mean())
        flag = "OK " if gap < 1e-4 else "!! "
        print(f"{flag}{name:18s} dikis={gap:.2e} kare_adimi={step:.5f}")


def run_cli(concepts):
    ap = argparse.ArgumentParser()
    ap.add_argument("--concept", choices=list(concepts))
    ap.add_argument("--variant", choices=["desktop", "mobile"], default="desktop")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--seam", action="store_true")
    ap.add_argument("--raw", default=None)
    ap.add_argument("--frames", default=None, help="START:END")
    ap.add_argument("--encode", action="store_true")
    args = ap.parse_args()

    if args.seam:
        seam_report(concepts)
    elif args.preview:
        preview(concepts, args.concept, args.variant, args.outdir)
    elif args.frames:
        a, b = (int(x) for x in args.frames.split(":"))
        write_raw(concepts, args.concept, args.variant, args.raw, a, min(b, N))
    elif args.encode:
        encode(concepts, args.concept, args.variant, args.raw, args.outdir)
    else:
        sys.exit("--preview | --frames | --encode | --seam secilmeli")
