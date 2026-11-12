#!/usr/bin/env python3
"""
DavetKart - "Gokyuzu Ruyasi" davetiye arka plan videosu ureteci.

Iki ayri kompozisyon uretir:
  * desktop : 1280x720  (yatay - laptop / masaustu)
  * mobile  : 720x1280  (dikey - telefon)

Neden iki ayri render? Bir 16:9 videoyu telefonda object-cover ile gostermek
kadrajin ~%65'ini kirpar; gunes ve bulut kutleleri disarida kalir, kompozisyon
dagilir. Bu yuzden mobil surum "kirpilmis kopya" degil, ayni gorsel dille
yeniden komponize edilmis bagimsiz bir renderdir.

DONGU GARANTISI
---------------
Tum zamana bagli terimler cos(2*pi*m*p) bicimindedir; p = i/N ve m TAM SAYI.
Boylece i=0 ile i=N kareleri matematiksel olarak ozdestir -> dikis (seam) yok.

BULUT HAREKETININ SIRRI
-----------------------
Bulut alani, rastgele yonlu duzlem dalgalarinin toplamidir. Her dalganin
zamansal harmonigi m = round(kx * drift) secilir. drift=0.5 icin kx>=2 olan
tum dalgalar tam olarak 0.5 ekran genisligi/dongu hizinda kayar; en buyuk
kutleler (kx<=1) sabit kalir. Sonuc: derinlik hissi veren, dongude kusursuz
kapanan organik bir suruklenme.
"""

import argparse
import subprocess
import sys

import numpy as np
from PIL import Image

# ---------------------------------------------------------------------------
# Genel ayarlar
# ---------------------------------------------------------------------------
FPS = 24
DUR = 15
N = FPS * DUR                      # 360 kare

# Renk paleti - sabah ruyasi gokyuzu
def hexc(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255.0


ZENITH = hexc("#6f9ccb")      # tepe - doygun ama yumusak gok mavisi
MIDSKY = hexc("#b6cee4")      # orta kusak
HORIZON = hexc("#f7ddcb")     # ufuk - pudra
GLOWCOL = hexc("#ffd6a2")     # gunes halesi - sicak sampanya
CLOUD_LIT = hexc("#fffefb")   # bulutun isik alan tepesi
CLOUD_MID = hexc("#f2e9e8")   # bulut govdesi
CLOUD_SHA = hexc("#a8b2cf")   # bulutun golge tarafi - soguk lavanta
CLOUD_ROSE = hexc("#dfb6b8")  # gunese yakin bulut altlarinin sicak yansimasi
MOTE = hexc("#ffe9c4")        # altin toz zerresi


VARIANTS = {
    "desktop": dict(
        out=(1280, 720), render=(640, 360),
        sun=(0.26, 0.74),        # gunes: sol-alt ucte bir, metin sagda nefes alsin
        cloud_scale=1.00,
        bands=(0.30, 0.55, 0.78),
    ),
    "mobile": dict(
        out=(720, 1280), render=(360, 640),
        sun=(0.50, 0.72),        # dikeyde gunes ortada - metin ustte/altta durur
        cloud_scale=0.60,        # dar kadrajda ayni puf boyutu daha az dalga demek
        bands=(0.34, 0.58, 0.80),
    ),
}


def smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


# ---------------------------------------------------------------------------
# Bulut katmani: onceden hesaplanmis cos/sin bankasi
# ---------------------------------------------------------------------------
class CloudLayer:
    """
    field(p) = SUM_k a_k * cos(theta_k + 2*pi*m_k*p)
             = SUM_k [ (a_k cos theta_k) cos(psi) - (a_k sin theta_k) sin(psi) ]

    theta_k uzaysal faz (kareden kareye degismez) -> bir kez hesaplanir.
    Kare basina is, iki kucuk matris carpimina duser: 360 kare saniyeler icinde.
    """

    def __init__(self, rw, rh, seed, n_waves, k_lo, k_hi, exponent, drift, scale):
        rng = np.random.default_rng(seed)
        xs = np.linspace(0.0, 1.0, rw, endpoint=False, dtype=np.float32)
        ys = np.linspace(0.0, 1.0, rh, endpoint=False, dtype=np.float32) * (rh / rw)
        X, Y = np.meshgrid(xs, ys)

        cos_bank, sin_bank, ms = [], [], []
        for _ in range(n_waves):
            k = float(np.exp(rng.uniform(np.log(k_lo), np.log(k_hi)))) * scale
            ang = rng.uniform(0.0, 2.0 * np.pi)
            # Yatay uzanan bulut kutleleri icin dikey frekansi bilincli olarak
            # sikistiriyoruz (1.7 kat): gercek bulutlar genise yayilir.
            kx, ky = k * np.cos(ang), k * np.sin(ang) * 1.7
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

        # Normalizasyon: birkac kareyi orneklep std olcuyoruz ki alan her
        # varyantta ayni kontrastta olsun (elle katsayi ayarlamak yerine).
        samples = np.concatenate([self._raw(p) for p in (0.0, 0.31, 0.67)])
        self.norm = float(samples.std()) * 2.6 + 1e-6

    def _raw(self, p: float) -> np.ndarray:
        psi = 2.0 * np.pi * self.m * p
        return np.cos(psi) @ self.C - np.sin(psi) @ self.S

    def value(self, p: float) -> np.ndarray:
        """0..1 araligina oturtulmus bulut yogunluk alani."""
        v = self._raw(p) / self.norm
        return np.clip(0.5 + 0.5 * v, 0.0, 1.0).reshape(self.shape)


# ---------------------------------------------------------------------------
# Sahne
# ---------------------------------------------------------------------------
class Scene:
    def __init__(self, cfg):
        self.rw, self.rh = cfg["render"]
        self.out_w, self.out_h = cfg["out"]
        self.sun = cfg["sun"]
        bands = cfg["bands"]
        s = cfg["cloud_scale"]

        xs = np.linspace(0.0, 1.0, self.rw, endpoint=False, dtype=np.float32)
        ys = np.linspace(0.0, 1.0, self.rh, endpoint=False, dtype=np.float32)
        self.X, self.Y = np.meshgrid(xs, ys)
        aspect = self.rh / self.rw
        self.Yiso = self.Y * aspect          # izotropik (dairesel) mesafe icin

        # --- Statik gokyuzu degradesi -------------------------------------
        t = self.Y[..., None]
        upper = ZENITH + (MIDSKY - ZENITH) * smoothstep(0.0, 0.62, self.Y)[..., None]
        self.sky = upper + (HORIZON - upper) * smoothstep(0.45, 1.0, self.Y)[..., None]
        self.sky = self.sky.astype(np.float32)
        del t

        # --- Gunes mesafesi -----------------------------------------------
        sx, sy = self.sun
        self.sun_d = np.sqrt((self.X - sx) ** 2 + (self.Yiso - sy * aspect) ** 2)
        self.sun_ang = np.arctan2(self.Yiso - sy * aspect, self.X - sx)

        # --- Kenar karartma (vignette) ------------------------------------
        cd = np.sqrt((self.X - 0.5) ** 2 + (self.Yiso - 0.5 * aspect) ** 2)
        self.vignette = smoothstep(0.34 * max(1.0, aspect), 0.78 * max(1.0, aspect), cd)

        # --- Uc bulut katmani (uzak -> yakin) ------------------------------
        # lo/hi araligi ne kadar dar olursa bulut kenari o kadar KESIN olur.
        # Uzak katmanda genis (puslu), yakin katmanda dar (pamuksu) tutuyoruz.
        self.layers = [
            dict(layer=CloudLayer(self.rw, self.rh, 11, 34, 0.8, 3.0, 1.35, 0.25, s),
                 lo=0.54, hi=0.78, opacity=0.42, center=bands[0], spread=0.50, gain=1.6),
            dict(layer=CloudLayer(self.rw, self.rh, 23, 58, 1.4, 9.0, 1.55, 0.50, s),
                 lo=0.56, hi=0.67, opacity=0.96, center=bands[1], spread=0.34, gain=3.0),
            dict(layer=CloudLayer(self.rw, self.rh, 37, 46, 2.6, 14.0, 1.60, 1.00, s),
                 lo=0.58, hi=0.70, opacity=0.45, center=bands[2], spread=0.24, gain=3.5),
        ]

        # Isik yonu: gunesten tuvalin merkezine bakan birim vektor. Bulut
        # kabartmasini bu yone gore hesaplayacagiz (kabartma = ayni alanin
        # birkac piksel kaydirilmis kopyasiyla farki -> bedava normal haritasi).
        lx, ly = sx - 0.5, sy - 0.5
        ln = max(1e-6, (lx * lx + ly * ly) ** 0.5)
        self.light_dx = int(round(-lx / ln * 4))
        self.light_dy = int(round(-ly / ln * 4))

        # Her katmanin dikey yerlesim maskesi: bulutlar tum tuvale esit
        # dagilirsa duvar kagidi gibi durur; kusaklara ayirmak derinlik verir.
        for L in self.layers:
            d = np.abs(self.Y - L["center"]) / L["spread"]
            L["mask"] = np.clip(1.0 - d ** 2, 0.0, 1.0) ** 0.8

        # --- Altin toz zerreleri ------------------------------------------
        rng = np.random.default_rng(4242)
        self.motes = []
        for _ in range(22):
            self.motes.append(dict(
                x=rng.uniform(0.04, 0.96),
                y=rng.uniform(0.10, 0.94),
                r=rng.uniform(0.006, 0.017),
                a=rng.uniform(0.10, 0.30),
                ax=rng.uniform(0.010, 0.032),
                ay=rng.uniform(0.008, 0.026),
                ph=rng.uniform(0.0, 2.0 * np.pi),
                hm=int(rng.integers(1, 3)),          # tamsayi harmonik -> dongu guvenli
            ))

        self.grain_rng = np.random.default_rng(9090)

    # -----------------------------------------------------------------
    def frame(self, p: float) -> np.ndarray:
        img = self.sky.copy()

        # 1) Gunes halesi - yaricap cok hafif nefes alir (m=1 -> dongu guvenli)
        breathe = 1.0 + 0.05 * np.cos(2.0 * np.pi * p)
        glow = np.exp(-(self.sun_d / (0.46 * breathe)) ** 2)
        core = np.exp(-(self.sun_d / (0.15 * breathe)) ** 2)
        halo = np.clip(0.55 * glow + 0.38 * core, 0.0, 1.0)
        img = img + (GLOWCOL[None, None, :] - img) * (0.72 * halo)[..., None]

        # 2) Bulutlar: uzaktan yakina ust uste bindirilir
        warm = np.exp(-(self.sun_d / 0.62) ** 2)
        for L in self.layers:
            f = L["layer"].value(p)
            alpha = smoothstep(L["lo"], L["hi"], f) * L["mask"] * L["opacity"]

            # Kabartma: alani isiga dogru birkac piksel kaydirip farkini al.
            # Yogunluk gunese dogru azaliyorsa orasi bulutun isik alan sirti,
            # artiyorsa golgede kalan karnidir. Tam bir normal haritasi kadar
            # dogru degil ama kare basina maliyeti neredeyse sifir.
            shifted = np.roll(f, (self.light_dy, self.light_dx), axis=(0, 1))
            body = smoothstep(L["lo"], L["hi"] + 0.16, f)
            # Kabartmayi body ile carpiyoruz: aksi halde bulutun disindaki
            # sisli bolgelerde de fark olusur ve ekrana ince tarama cizgileri
            # (kontur) duser. Golge yalnizca govdesi olan bulutta anlamlidir.
            relief = np.clip(0.5 + (f - shifted) * L["gain"] * 8.0 * body, 0.0, 1.0)
            lit = np.clip(0.42 * body + 0.58 * relief, 0.0, 1.0)

            # Golge rengi sabit degil: gunese yakin bulut altlari yerden ve
            # atmosferden pembe yansima alir, uzaktakiler soguk lavantada kalir.
            shadow = CLOUD_SHA[None, None, :] + (CLOUD_ROSE - CLOUD_SHA)[None, None, :] * (0.55 * warm)[..., None]
            col = shadow + (CLOUD_MID[None, None, :] - shadow) * lit[..., None]
            col = col + (CLOUD_LIT - col) * (0.80 * lit ** 1.6)[..., None]
            col = col + (GLOWCOL[None, None, :] - col) * (0.45 * warm)[..., None]

            a = alpha[..., None]
            img = img * (1.0 - a) + col * a

        # 3) Gunes sizmasi: hale bulutlarin UZERINE de hafifce eklenir. Gercek
        #    atmosferde isik bulutun onunden de sacilir; bu katman olmazsa
        #    bulutlar gunesin onune yapistirilmis kagit gibi durur.
        bleed = np.exp(-(self.sun_d / (0.34 * breathe)) ** 2) * 0.15
        img = img + (GLOWCOL[None, None, :] - img) * bleed[..., None]

        # 4) Altin toz zerreleri
        for m in self.motes:
            psi = 2.0 * np.pi * m["hm"] * p + m["ph"]
            cx = m["x"] + m["ax"] * np.cos(psi)
            cy = m["y"] + m["ay"] * np.sin(psi)
            self._blob(img, cx, cy, m["r"], m["a"] * (0.7 + 0.3 * np.cos(psi)))

        # 5) Ufuk sisi + kenar karartma
        haze = smoothstep(0.80, 1.0, self.Y)[..., None]
        img = img + (HORIZON[None, None, :] - img) * (0.22 * haze)
        img = img * (1.0 - 0.16 * self.vignette[..., None])

        return np.clip(img, 0.0, 1.0)

    # -----------------------------------------------------------------
    def _blob(self, img, cx, cy, r, a):
        """Tek bir isik zerresini yerel bir pencerede toplar (tam tuval degil)."""
        aspect = self.rh / self.rw
        px, py = cx * self.rw, cy * self.rh
        rad = r * self.rw
        x0, x1 = int(max(0, px - 3 * rad)), int(min(self.rw, px + 3 * rad + 1))
        y0, y1 = int(max(0, py - 3 * rad * aspect * (self.rw / self.rh))), \
                 int(min(self.rh, py + 3 * rad * aspect * (self.rw / self.rh) + 1))
        if x1 <= x0 or y1 <= y0:
            return
        gx = (np.arange(x0, x1, dtype=np.float32) - px) / rad
        gy = (np.arange(y0, y1, dtype=np.float32) - py) / rad
        d2 = gx[None, :] ** 2 + gy[:, None] ** 2
        g = np.exp(-d2 * 1.6) * a
        patch = img[y0:y1, x0:x1]
        img[y0:y1, x0:x1] = patch + (MOTE[None, None, :] - patch) * g[..., None]


# ---------------------------------------------------------------------------
# Kodlama
# ---------------------------------------------------------------------------
def to_bytes(scene: Scene, img: np.ndarray) -> bytes:
    """Buyut + gurultu ekle + 8 bit'e yuvarla."""
    small = Image.fromarray((img * 255.0 + 0.5).astype(np.uint8), "RGB")
    big = small.resize((scene.out_w, scene.out_h), Image.LANCZOS)
    arr = np.asarray(big, dtype=np.float32)
    # Ince film graini: hem banding'i (gradyan halkalarini) kirar hem de
    # dijital duzlugu gercek film hissine yaklastirir.
    noise = scene.grain_rng.normal(0.0, 1.9, size=arr.shape[:2]).astype(np.float32)
    arr = arr + noise[..., None]
    return np.clip(arr, 0, 255).astype(np.uint8).tobytes()


def preview(name: str, outdir: str) -> None:
    scene = Scene(VARIANTS[name])
    for idx in (0, 90, 180, 270):
        Image.frombytes("RGB", (scene.out_w, scene.out_h),
                        to_bytes(scene, scene.frame(idx / N))).save(
            f"{outdir}/preview-{name}-{idx:03d}.png")
    print(f"[{name}] onizleme kareleri yazildi")


def write_raw(name: str, raw_path: str, start: int, end: int) -> None:
    """
    [start, end) araligindaki kareleri ham RGB olarak dosyaya EKLER.

    Neden parcali? Uretim ortami her komutu bagimsiz ve kisa omurlu
    calistiriyor; 360 karelik tek hamle zaman asimina ugruyor. Kareler
    birbirinden bagimsiz oldugu icin (durum yok, sadece p degeri) isi
    boluyoruz - bu ayni zamanda islemin yeniden baslatilabilir olmasi demek.
    """
    scene = Scene(VARIANTS[name])
    mode = "wb" if start == 0 else "ab"
    with open(raw_path, mode) as fh:
        for i in range(start, end):
            fh.write(to_bytes(scene, scene.frame(i / N)))
    print(f"[{name}] {start}-{end} yazildi")


def encode(name: str, raw_path: str, outdir: str) -> None:
    cfg = VARIANTS[name]
    w, h = cfg["out"]
    src = ["-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
           "-r", str(FPS), "-i", raw_path]
    base = f"{outdir}/sky-{name}"

    # H.264: her cihazda DONANIMDA cozulur -> telefon isinmaz, pil erimez.
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *src,
                    "-c:v", "libx264", "-profile:v", "high", "-level", "4.0",
                    "-preset", "slow", "-crf", "24", "-pix_fmt", "yuv420p",
                    "-g", str(FPS * 5), "-movflags", "+faststart", "-an",
                    f"{base}.mp4"], check=True)
    # VP9: ayni kalitede ~%40 kucuk; Chrome/Android bunu tercih eder.
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *src,
                    "-c:v", "libvpx-vp9", "-crf", "36", "-b:v", "0",
                    "-deadline", "good", "-cpu-used", "3", "-row-mt", "1",
                    "-pix_fmt", "yuv420p", "-an", f"{base}.webm"], check=True)
    # Poster: video ilk kareyi boyayana kadar gorunen katman (LCP'yi kurtarir).
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *src,
                    "-frames:v", "1", "-q:v", "6", f"{base}-poster.jpg"],
                   check=True)
    print(f"[{name}] tamam -> {base}.mp4 / .webm / -poster.jpg")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--variant", choices=list(VARIANTS), required=True)
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--raw", default=None, help="ham RGB dosyasi")
    ap.add_argument("--frames", default=None, help="START:END")
    ap.add_argument("--encode", action="store_true")
    args = ap.parse_args()

    if args.preview:
        preview(args.variant, args.outdir)
    elif args.frames:
        a, b = (int(x) for x in args.frames.split(":"))
        write_raw(args.variant, args.raw, a, min(b, N))
    elif args.encode:
        encode(args.variant, args.raw, args.outdir)
    else:
        sys.exit("--preview | --frames | --encode secilmeli")
