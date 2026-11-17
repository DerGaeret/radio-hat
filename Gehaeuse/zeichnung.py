"""Erzeugt Maßzeichnungen (PDF + PNG) für das Radiogehäuse. Maße wie in gehaeuse.scad."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from matplotlib.backends.backend_pdf import PdfPages

t, L = 8, 15
platte_b, platte_h, platte_t = 300, 114, 3
abd_b, abd_h, abd_t = 178, 112, 7
ls_korb, ls_lochabst, ls_loch, ls_tiefe = 110, 84, 100, 47
rueck, chrom_h, tiefe = 10, 4, 210
fuss_d, fuss_h, fuss_x, fuss_y = 25, 20, 60, 55
innen_b, innen_h = 2 * abd_b + platte_b, platte_h + 2 * chrom_h
B, H = innen_b + 2 * t, innen_h + 2 * t
korpus_t = tiefe - t
y_front, y_wand = rueck + abd_t, rueck + abd_t + t
kammer_b, kammer_t = abd_b - t, korpus_t - (rueck + abd_t + t)
ls_x = abd_b / 2
xw = [t + kammer_b, B - t - abd_b]
vol = kammer_b * innen_h * kammer_t / 1e6

NUSS, NUSS2, KIEFER, KANTE = "#8a5a3a", "#a87850", "#f0d9a8", "#3b2414"

def rect(ax, x, y, w, h, fc=NUSS, ec=KANTE, lw=0.8, **kw):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, **kw))

def mass(ax, a, b, off, text=None, vert=False, fs=8):
    a, b = sorted((a, b))
    txt = text or f"{b - a:g}"
    if not vert:
        ax.annotate("", (a, off), (b, off), arrowprops=dict(arrowstyle="<->", lw=0.7))
        ax.text((a + b) / 2, off + 2, txt, ha="center", va="bottom", fontsize=fs)
    else:
        ax.annotate("", (off, a), (off, b), arrowprops=dict(arrowstyle="<->", lw=0.7))
        ax.text(off - 2, (a + b) / 2, txt, ha="right", va="center", fontsize=fs, rotation=90)

def blatt(titel, h=11.7):
    fig, ax = plt.subplots(figsize=(16.5, h))
    ax.set_aspect("equal"); ax.axis("off")
    fig.suptitle(titel, fontsize=14, x=0.02, ha="left")
    return fig, ax

def fuss_seite(ax, x, y0):   # Fuß von vorne/seitlich gesehen, y0 = Unterkante Boden
    ax.add_patch(Polygon([(x - fuss_d / 2, y0), (x + fuss_d / 2, y0), (x + fuss_d * 0.35, y0 - fuss_h), (x - fuss_d * 0.35, y0 - fuss_h)],
                         fc="#d8d8d8", ec="#666", lw=0.7))

# ---------- Blatt 1 ----------
fig, ax = blatt("Radiogehäuse – Vorderansicht und Schnitt A–A (von oben)   Maße in mm, Spanplatte 8 mm Nussbaum")
oy = 330
rect(ax, 0, oy, B, t); rect(ax, 0, oy + H - t, B, t)
rect(ax, 0, oy + t, t, innen_h, fc=NUSS2); rect(ax, B - t, oy + t, t, innen_h, fc=NUSS2)
rect(ax, t + abd_b, oy + t + chrom_h, platte_b, platte_h, fc="#c0c0c0", ec="k")
rect(ax, t + abd_b + 12, oy + t + chrom_h + 8, platte_b - 24, platte_h - 16, fc="#222", ec="none")
for x in (t, B - t - abd_b):
    z0 = oy + t + (innen_h - abd_h) / 2
    rect(ax, x, z0, abd_b, abd_h, fc="#333", ec="k")
    for z in range(4, abd_h - 2, 4):
        ax.plot([x + 2, x + abd_b - 2], [z0 + z] * 2, color="#555", lw=0.4)
for z in (oy + t, oy + H - t - chrom_h):
    rect(ax, t, z, innen_b, chrom_h, fc="#f4f4f4", ec="#777", lw=0.5)
for lx in (t + ls_x, B - t - ls_x):
    ax.add_patch(Circle((lx, oy + H / 2), ls_loch / 2, fill=False, ls="--", ec="#d08000", lw=0.8))
for x in (fuss_x, B - fuss_x):
    fuss_seite(ax, x, oy)
mass(ax, 0, B, oy + H + 12)
mass(ax, t, B - t, oy + H + 30, f"{innen_b} innen")
mass(ax, t, t + abd_b, oy - 34, f"Abdeckung {abd_b}")
mass(ax, t + abd_b, t + abd_b + platte_b, oy - 34, f"Frontplatte {platte_b}")
mass(ax, B - t - abd_b, B - t, oy - 34, f"Abdeckung {abd_b}")
mass(ax, 0, fuss_x, oy - 52, f"{fuss_x}")
mass(ax, oy, oy + H, -12, vert=True)
mass(ax, oy + t, oy + H - t, -32, f"{innen_h} innen", vert=True)
mass(ax, oy - fuss_h, oy, -12, f"{fuss_h}", vert=True)
ax.text(B + 10, oy + H - t, f"Chromleiste {chrom_h} mm hoch,\noben und unten je {innen_b} lang", fontsize=8, va="top")
ax.text(B + 10, oy + 55, f"Abdeckungen {rueck} mm hinter\nder Holzvorderkante,\nFrontplatte 4 mm dahinter\n(hinten bündig)", fontsize=8)
ax.text(B + 10, oy - 15, f"4 Chromfüße Ø{fuss_d}, {fuss_h} hoch", fontsize=8)
ax.text(0, oy + H + 50, "Vorderansicht", fontsize=10, weight="bold")

oy2 = 230
def r2(x, y, w, d, **kw):
    rect(ax, x, oy2 - y - d, w, d, **kw)
r2(0, 0, t, korpus_t, fc=NUSS2); r2(B - t, 0, t, korpus_t, fc=NUSS2)
r2(0, korpus_t, B, t)
r2(t, y_front, innen_b, t, fc=NUSS2)
for x in xw:
    r2(x, y_wand, t, kammer_t, fc=NUSS2)
for x in (t, B - t - abd_b):
    r2(x, rueck, abd_b, abd_t, fc="#333", ec="k")
r2(t + abd_b, y_front - platte_t, platte_b, platte_t, fc="#c0c0c0", ec="k")
for x in (t, B - t - L, xw[0] - L, xw[1] + t):     # Leisten (Schnitt zeigt die Längsleisten am Boden)
    r2(x, y_wand, L, kammer_t - (0 if x in (t, B - t - L) else L), fc=KIEFER, ec="#b09060", lw=0.5, alpha=0.6)
r2(xw[0] + t, korpus_t - L, xw[1] - xw[0] - t, L, fc=KIEFER, ec="#b09060", lw=0.5, alpha=0.6)
for x in (t + L, xw[1] + t + L):
    r2(x, korpus_t - L, kammer_b - 2 * L, L, fc=KIEFER, ec="#b09060", lw=0.5, alpha=0.6)
for lx in (t + ls_x, B - t - ls_x):
    r2(lx - ls_loch / 2, y_front - 0.5, ls_loch, t + 1, fc="white", ec="#d08000", ls="--")
    r2(lx - ls_korb / 2, y_wand, ls_korb, 2, fc="#c8a000", ec="k")
    r2(lx - 39, y_wand + ls_tiefe - 18, 78, 18, fc="#555", ec="k")
    ax.plot([lx - ls_loch / 2, lx - 39, lx + 39, lx + ls_loch / 2],
            [oy2 - y_wand - 2, oy2 - y_wand - ls_tiefe + 18, oy2 - y_wand - ls_tiefe + 18, oy2 - y_wand - 2], color="#8a6d00", lw=0.8)
for x in (fuss_x, B - fuss_x):
    for y in (fuss_y, tiefe - fuss_y):
        ax.add_patch(Circle((x, oy2 - y), fuss_d / 2, fill=False, ec="#888", ls=":"))
ax.text(B / 2, oy2 - 110, f"Technikfach {platte_b} × {innen_h} innen\n(3D-gedruckter Träger – nächster Schritt)", ha="center", fontsize=8, color="b")
for x in (t + kammer_b / 2, B - t - kammer_b / 2):
    ax.text(x, oy2 - 150, f"LS-Kammer\n{kammer_b}×{innen_h}×{kammer_t}\n≈ {vol:.1f} l brutto", ha="center", fontsize=7)
mass(ax, oy2, oy2 - tiefe, -12, f"{tiefe}", vert=True)
mass(ax, oy2, oy2 - korpus_t, -32, f"{korpus_t}", vert=True)
mass(ax, oy2, oy2 - rueck, B + 22, f"{rueck}", vert=True)
mass(ax, oy2 - rueck, oy2 - y_front, B + 40, f"{abd_t}", vert=True)
mass(ax, oy2 - y_front, oy2 - y_wand, B + 22, f"{t}", vert=True)
mass(ax, t, t + kammer_b, oy2 - tiefe - 14, f"{kammer_b}")
mass(ax, t, t + ls_x, oy2 + 8, f"{ls_x:g}")
mass(ax, xw[0] + t, xw[1], oy2 - tiefe - 14, f"{xw[1] - xw[0] - t}")
ax.text(0, oy2 + 24, "Schnitt A–A (Blick von oben, vorne = oben; hell = Kiefernleisten 15×15, gepunktet = Füße)", fontsize=10, weight="bold")
ax.set_xlim(-60, B + 150); ax.set_ylim(oy2 - tiefe - 40, oy + H + 60)
blaetter = [fig]

# ---------- Blatt 2 ----------
fig, ax = blatt("Radiogehäuse – Schnitt B–B, Frontbrett, Rückwand", h=5.5)
rect(ax, 0, 0, korpus_t, t); rect(ax, 0, H - t, korpus_t, t)
rect(ax, korpus_t, 0, t, H)
rect(ax, y_front, t, t, innen_h, fc=NUSS2)
rect(ax, rueck, t + (innen_h - abd_h) / 2, abd_t, abd_h, fc="#333", ec="k")
for z in (t, H - t - chrom_h):
    rect(ax, rueck, z, abd_t, chrom_h, fc="#ddd", ec="k", lw=0.5)
rect(ax, y_wand, H / 2 - ls_korb / 2, 2, ls_korb, fc="#c8a000", ec="k")
rect(ax, y_wand + ls_tiefe - 18, H / 2 - 39, 18, 78, fc="#555", ec="k")
ax.plot([y_wand + 2, y_wand + ls_tiefe - 18, y_wand + ls_tiefe - 18, y_wand + 2],
        [H / 2 + ls_loch / 2, H / 2 + 39, H / 2 - 39, H / 2 - ls_loch / 2], color="#8a6d00")
rect(ax, y_front - 0.5, H / 2 - ls_loch / 2, t + 1, ls_loch, fc="white", ec="#d08000", ls="--")
rect(ax, korpus_t - L, t + L, L, innen_h - 2 * L, fc=KIEFER, ec="#b09060", lw=0.5)
rect(ax, fuss_y - 15, t, 30, 10, fc=KIEFER, ec="#b09060", lw=0.5)
rect(ax, tiefe - fuss_y - 15, t, 30, 10, fc=KIEFER, ec="#b09060", lw=0.5)
for y in (fuss_y, tiefe - fuss_y):
    fuss_seite(ax, y, 0)
mass(ax, 0, tiefe, -fuss_h - 14)
mass(ax, y_wand, y_wand + ls_tiefe, H + 10, f"LS {ls_tiefe}")
mass(ax, y_wand + ls_tiefe, korpus_t, H + 10, f"{kammer_t - ls_tiefe} frei")
mass(ax, 0, fuss_y, -fuss_h - 32, f"{fuss_y}")
mass(ax, 0, H, -12, vert=True)
ax.text(0, H + 30, "Schnitt B–B (Seitenansicht, vorne = links)", fontsize=10, weight="bold")

# Frontbrett
s = 0.5; fx = 280
rect(ax, fx, 0, innen_b * s, innen_h * s, fc=NUSS2)
for lx in (ls_x, innen_b - ls_x):
    ax.add_patch(Circle((fx + lx * s, innen_h / 2 * s), ls_loch / 2 * s, fc="white", ec="k"))
    for dx in (-ls_lochabst / 2, ls_lochabst / 2):
        for dz in (-ls_lochabst / 2, ls_lochabst / 2):
            ax.add_patch(Circle((fx + (lx + dx) * s, (innen_h / 2 + dz) * s), 1.0, fc="k"))
ax.add_patch(Rectangle((fx + (abd_b + 15) * s, 15 * s), (platte_b - 30) * s, (innen_h - 30) * s, fill=False, ls=":", ec="b"))
ax.text(fx + innen_b / 2 * s, innen_h / 2 * s, "Ausschnitte für Tasten\nund Drehgeber folgen\nmit dem 3D-Träger", ha="center", va="center", fontsize=7, color="b")
mass(ax, fx, fx + innen_b * s, -12, f"{innen_b}")
mass(ax, fx, fx + ls_x * s, innen_h * s + 6, f"{ls_x:g}")
mass(ax, 0, innen_h * s, fx - 6, f"{innen_h}", vert=True)
ax.text(fx, innen_h * s + 22, f"Frontbrett {innen_b} × {innen_h} (1:2)\nLöcher Ø {ls_loch}, mittig in der Höhe\n"
        f"Schrauben: Quadrat {ls_lochabst} mm, Ø 4,5 mit Senkung vorne (M4 Senkkopf)", fontsize=8, va="bottom")

# Rückwand
rx = fx + innen_b * s + 30
rect(ax, rx, 0, B * s, H * s)
for i in range(7):
    for j in range(3):
        ax.add_patch(Circle((rx + (t + abd_b + 60 + i * 30) * s, (35 + j * 25) * s), 5 * s, fc="white", ec="k", lw=0.5))
ax.add_patch(Circle((rx + (t + abd_b + platte_b - 30) * s, (H - 40) * s), 5 * s, fc="white", ec="r", lw=0.6))
for x in (t + L / 2, B - t - L / 2, xw[0] - L / 2, xw[1] + t + L / 2):
    for z in (t + L + 10, H / 2, H - t - L - 10):
        ax.add_patch(Circle((rx + x * s, z * s), 0.9, fc="k"))
for x in (xw[0] + t + 50, B / 2, xw[1] - 50, t + kammer_b / 2, B - t - kammer_b / 2):
    for z in (t + L / 2, H - t - L / 2):
        ax.add_patch(Circle((rx + x * s, z * s), 0.9, fc="k"))
ax.text(rx, H * s + 6, f"Rückwand {B} × {H} (1:2, Blick von hinten)\n"
        "● Spax 3,5×20 in die Kiefernleisten\n○ Lüftung 21 × Ø10 nur im Technikfach\n○ rot: DC-Buchse", fontsize=8, va="bottom")
ax.set_xlim(-60, rx + B * s + 10); ax.set_ylim(-fuss_h - 45, H + 45)
blaetter.append(fig)

with PdfPages("zeichnung_gehaeuse.pdf") as pdf:
    for f in blaetter:
        pdf.savefig(f)
for i, f in enumerate(blaetter, 1):
    f.savefig(f"bilder/zeichnung_blatt{i}.png", dpi=110, bbox_inches="tight")
print("ok", B, H, tiefe, round(vol, 2))
