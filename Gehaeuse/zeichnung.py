"""Erzeugt Maßzeichnungen (PDF + PNG) für das Radiogehäuse. Maße wie in gehaeuse.scad."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.backends.backend_pdf import PdfPages

t = 19
platte_b, platte_h, platte_t = 300, 114, 3
abd_b, abd_h, abd_t = 178, 112, 8
ueberl, rueck, spalt, tiefe, ls_x, ls_loch, ls_korb, ls_tiefe = 19, 10, 6, 180, 70, 95, 112, 47
kammer_b = abd_b - ueberl - t
schall_b = abd_b - ueberl
innen_b = 2 * schall_b + platte_b
innen_h = platte_h + 2 * spalt
B, H = innen_b + 2 * t, innen_h + 2 * t
korpus_t = tiefe - t
y_schall = rueck + abd_t
y_wand = y_schall + t

HOLZ, KANTE = "#e8c9a0", "#7a5230"

def rect(ax, x, y, w, h, fc=HOLZ, ec=KANTE, lw=1, **kw):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, **kw))

def mass(ax, p1, p2, off, text=None, vert=False, fs=8):
    """Bemaßung zwischen p1 und p2 (Skalare entlang Achse), off = Lage der Maßlinie."""
    a, b = sorted((p1, p2))
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

# ---------- Blatt 1: Vorderansicht + Schnitt von oben ----------
fig, ax = blatt("Radiogehäuse – Vorderansicht und Schnitt A–A (von oben)   Maße in mm, Spanplatte 19 mm")
# Vorderansicht (y nach oben = Höhe)
oy = 330
rect(ax, 0, oy, B, t); rect(ax, 0, oy + H - t, B, t)
rect(ax, 0, oy + t, t, innen_h); rect(ax, B - t, oy + t, t, innen_h)
rect(ax, t + schall_b - 0, oy + t + spalt, platte_b, platte_h, fc="#c0c0c0", ec="k")
rect(ax, t + schall_b + 12, oy + t + spalt + 8, platte_b - 24, platte_h - 16, fc="#222", ec="none")
for x in (t, B - t - abd_b):
    rect(ax, x, oy + t + (innen_h - abd_h) / 2, abd_b, abd_h, fc="#333", ec="k")
    for z in range(4, abd_h - 2, 4):
        ax.plot([x + 2, x + abd_b - 2], [oy + t + (innen_h - abd_h) / 2 + z] * 2, color="#555", lw=0.4)
for z in (oy + t, oy + H - t - 10):
    rect(ax, t, z, innen_b, 10, fc="#f0f0f0", ec="#888")
for lx in (t + ls_x, B - t - ls_x):
    ax.add_patch(Circle((lx, oy + H / 2), ls_loch / 2, fill=False, ls="--", ec="#d08000", lw=0.8))
ax.text(t + ls_x, oy + H / 2, "LS Ø95\n(verdeckt)", color="#d08000", ha="center", va="center", fontsize=7)
mass(ax, 0, B, oy + H + 12)
mass(ax, t, B - t, oy + H + 30, f"{innen_b} innen")
mass(ax, t, t + abd_b, oy - 14, f"Abdeckung {abd_b}")
mass(ax, t + schall_b, t + schall_b + platte_b, oy - 30, f"Frontplatte {platte_b} (je {ueberl} unter den Abdeckungen)")
mass(ax, B - t - abd_b, B - t, oy - 14, f"Abdeckung {abd_b}")
mass(ax, oy, oy + H, -12, f"{H}", vert=True)
mass(ax, oy + t, oy + H - t, -32, f"{innen_h} innen", vert=True)
ax.text(B + 10, oy + H - t - 5, "Chromleiste: Alu-Winkel 10×10×1\n(oben und unten, je 618 lang)", fontsize=8, va="top")
ax.text(B + 10, oy + 40, f"Abdeckungen sitzen {rueck} mm\nhinter der Holzvorderkante", fontsize=8)

# Schnitt A-A von oben (y = Tiefe nach unten gezeichnet: vorne oben)
oy2 = 250  # Vorderkante
def r2(x, y, w, d, **kw):  # y = Tiefe ab Vorderkante
    rect(ax, x, oy2 - y - d, w, d, **kw)
r2(0, 0, t, korpus_t); r2(B - t, 0, t, korpus_t)
r2(0, korpus_t, B, t, fc="#d9a96b")
for x in (t + kammer_b, B - t - kammer_b - t):
    r2(x, y_wand, t, korpus_t - y_wand, fc="#f3e0b5")
for x in (t, B - t - schall_b):
    r2(x, y_schall, schall_b, t, fc="#e9a86a")
for x in (t, B - t - abd_b):
    r2(x, rueck, abd_b, abd_t, fc="#333", ec="k")
r2(t + schall_b, y_schall, platte_b, platte_t, fc="#c0c0c0", ec="k")
for lx in (t + ls_x, B - t - ls_x):
    r2(lx - ls_loch / 2, y_schall - 0.5, ls_loch, t + 1, fc="white", ec="#d08000", ls="--")
    r2(lx - ls_korb / 2, y_wand, ls_korb, 2, fc="#c8a000", ec="k")
    r2(lx - 39, y_wand + ls_tiefe - 18, 78, 18, fc="#555", ec="k")
    ax.plot([lx - 50, lx - 39, lx + 39, lx + 50], [oy2 - y_wand - 2, oy2 - y_wand - ls_tiefe + 18, oy2 - y_wand - ls_tiefe + 18, oy2 - y_wand - 2], color="#8a6d00", lw=0.8)
ax.add_patch(Rectangle((t + schall_b + 10, oy2 - y_schall - platte_t - 125), platte_b - 20, 120, fill=False, ls=":", ec="b"))
ax.text(B / 2, oy2 - 110, "Technikfach 300 × 126 innen\n(3D-gedruckter Träger mit Pi, Verstärker,\nTasten und Drehgebern – nächster Schritt)", ha="center", fontsize=8, color="b")
for x in (t + kammer_b / 2, B - t - kammer_b / 2):
    ax.text(x, oy2 - 135, f"LS-Kammer\n{kammer_b}×{innen_h}×{korpus_t - y_wand}\n≈ 2,2 l", ha="center", fontsize=7)
mass(ax, oy2, oy2 - tiefe, -12, f"{tiefe}", vert=True)
mass(ax, oy2, oy2 - korpus_t, -32, f"{korpus_t}", vert=True)
mass(ax, oy2, oy2 - rueck, B + 25, f"{rueck}", vert=True)
mass(ax, oy2 - rueck, oy2 - y_schall, B + 45, f"{abd_t}", vert=True)
mass(ax, oy2 - y_schall, oy2 - y_wand, B + 25, f"{t}", vert=True)
mass(ax, t, t + kammer_b, oy2 - tiefe - 14, f"{kammer_b}")
mass(ax, t, t + ls_x, oy2 + 8, f"{ls_x}")
mass(ax, t + kammer_b + t, B - t - kammer_b - t, oy2 - tiefe - 14, f"{platte_b}")
ax.text(0, oy2 + 22, "Schnitt A–A (Blick von oben, vorne = oben)", fontsize=10, weight="bold")
ax.text(0, oy + H + 50, "Vorderansicht", fontsize=10, weight="bold")
ax.set_xlim(-60, B + 140); ax.set_ylim(oy2 - tiefe - 40, oy + H + 60)
blaetter = [fig]

# ---------- Blatt 2: Seitenschnitt + Einzelteile ----------
fig, ax = blatt("Radiogehäuse – Schnitt B–B durch Lautsprecher, Schallwand, Rückwand", h=6.5)
# Schnitt B-B (Seitenansicht, vorne links)
ox = 0
rect(ax, ox, 0, korpus_t, t); rect(ax, ox, H - t, korpus_t, t)
rect(ax, ox + korpus_t, 0, t, H, fc="#d9a96b")
rect(ax, ox + y_schall, t, t, innen_h, fc="#e9a86a")
rect(ax, ox + rueck, t + (innen_h - abd_h) / 2, abd_t, abd_h, fc="#333", ec="k")
for z, s in ((H - t - 1, 1), (t, 1)):
    rect(ax, ox, z, 10, s, fc="#bbb", ec="k", lw=0.5)
rect(ax, ox + 9, H - t - 10, 1, 10, fc="#bbb", ec="k", lw=0.5)
rect(ax, ox + 9, t, 1, 10, fc="#bbb", ec="k", lw=0.5)
rect(ax, ox + y_wand, H / 2 - ls_korb / 2, 2, ls_korb, fc="#c8a000", ec="k")
rect(ax, ox + y_wand + ls_tiefe - 18, H / 2 - 39, 18, 78, fc="#555", ec="k")
ax.plot([ox + y_wand + 2, ox + y_wand + ls_tiefe - 18, ox + y_wand + ls_tiefe - 18, ox + y_wand + 2],
        [H / 2 + 50, H / 2 + 39, H / 2 - 39, H / 2 - 50], color="#8a6d00")
rect(ax, ox + y_schall - 0.5, H / 2 - ls_loch / 2, t + 1, ls_loch, fc="white", ec="#d08000", ls="--")
mass(ax, 0, tiefe, -14); mass(ax, y_wand, y_wand + ls_tiefe, H + 10, f"LS {ls_tiefe}")
mass(ax, y_wand + ls_tiefe, korpus_t, H + 10, f"{korpus_t - y_wand - ls_tiefe} frei")
mass(ax, 0, H, -12, vert=True)
ax.text(ox + 12, H + 30, "Schnitt B–B (Seitenansicht, vorne = links)", fontsize=10, weight="bold")
ax.annotate("Alu-Winkel 10×10×1\n(Chromleiste)", (ox + 9, H - t - 5), (ox - 70, H + 20), fontsize=7, arrowprops=dict(arrowstyle="->", lw=0.6))

# Schallwand-Einzelteil
sx = 260
rect(ax, sx, 0, schall_b, innen_h, fc="#e9a86a")
ax.add_patch(Circle((sx + ls_x, innen_h / 2), ls_loch / 2, fc="white", ec="k"))
for dx in (-41, 41):
    for dz in (-41, 41):
        ax.add_patch(Circle((sx + ls_x + dx, innen_h / 2 + dz), 1.6, fc="k"))
mass(ax, sx, sx + schall_b, -14); mass(ax, sx, sx + ls_x, innen_h + 10, f"{ls_x}")
mass(ax, 0, innen_h, sx - 10, vert=True)
ax.text(sx + ls_x, innen_h / 2, f"Ø {ls_loch}", ha="center", va="center", fontsize=9)
ax.text(sx, innen_h + 30, "Schallwand (2×, rechts gespiegelt)\nLochmitte mittig in der Höhe (63)\nSchraublöcher: Lautsprecher als Schablone",
        fontsize=8, va="bottom")

# Rückwand
rx = 470
rect(ax, rx, 0, B * 0.5, H * 0.5, fc="#d9a96b")
s = 0.5
for i in range(7):
    for j in range(3):
        ax.add_patch(Circle((rx + (t + schall_b + 60 + i * 30) * s, (40 + j * 25) * s), 5 * s, fc="white", ec="k", lw=0.5))
ax.add_patch(Circle((rx + (t + schall_b + platte_b - 30) * s, (H - 45) * s), 5 * s, fc="white", ec="r", lw=0.6))
for x in (t + kammer_b + t / 2, B - t - kammer_b - t / 2, t / 2, B - t / 2):
    for z in (t / 2, H - t / 2, H / 2):
        ax.add_patch(Circle((rx + x * s, z * s), 1.2, fc="k"))
ax.text(rx, H * s + 8, f"Rückwand {B} × {H} (Maßstab 1:2, Blick von hinten)\n"
        "● Schrauben 4×40 in die Plattenkanten (vorbohren Ø 2,5)\n"
        "○ Lüftung: 21 × Ø 10 nur im Technikfach   ○ rot: DC-Buchse (Ø nach Buchse)",
        fontsize=8, va="bottom")
ax.set_xlim(-90, rx + B * 0.5 + 20); ax.set_ylim(-40, H + 80)
blaetter.append(fig)

with PdfPages("zeichnung_gehaeuse.pdf") as pdf:
    for f in blaetter:
        pdf.savefig(f)
for i, f in enumerate(blaetter, 1):
    f.savefig(f"bilder/zeichnung_blatt{i}.png", dpi=110, bbox_inches="tight")
print("ok", B, H, tiefe)
