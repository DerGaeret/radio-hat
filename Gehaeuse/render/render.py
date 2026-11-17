"""Erzeugt eine POV-Ray-Szene des Radios und rendert sie (Tag und Nacht mit Skalenbeleuchtung).
Aufruf: python3 render.py [breite] [hoehe] [qualitaet: schnell|gut]"""
import subprocess, sys

breite = int(sys.argv[1]) if len(sys.argv) > 1 else 1600
hoehe = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
gut = (sys.argv[3] if len(sys.argv) > 3 else "gut") == "gut"

# Maße wie gehaeuse.scad / traeger.scad (Gehäusekoordinaten: x Breite, y Tiefe, z Höhe)
t, B, H, T = 8, 672, 138, 190
abd_b, abd_h, abd_t, rueck = 178, 112, 7, 3
pl_x, pl_z = t + abd_b, t + 4            # Frontplatte links unten
knoepfe = [(29, 33, "rot"), (54, 33, "schwarz"), (104, 33, "schwarz"), (264, 33, "schwarz")]
tasten = [132.5 + 20 * i for i in range(6)]
fuss = [(60, 55), (B - 60, 55), (60, T - 55), (B - 60, T - 55)]

def v(x, y, z):            # Gehäuse -> POV (y oben, z in die Tiefe)
    return f"<{x:.2f},{z:.2f},{y:.2f}>"

def box(x0, y0, z0, x1, y1, z1, tex):
    return f"box {{ {v(x0,y0,z0)}, {v(x1,y1,z1)} texture {{ {tex} }} }}\n"

def szene(nacht):
    s = []
    s.append('#version 3.7;\nglobal_settings { assumed_gamma 1.0 max_trace_level 12 ')
    if gut:
        s.append('radiosity { pretrace_start 0.08 pretrace_end 0.004 count 300 error_bound 0.6 recursion_limit 2 brightness 1 }')
    s.append('}\n#include "colors.inc"\n#include "metals.inc"\n')
    # Kamera: schräg von vorne links, leicht von oben
    s.append(f'camera {{ location {v(B/2-380, -1000, 360)} look_at {v(B/2-10, 80, 45)} angle 40 right x*{breite}/{hoehe} }}\n')
    hell = 0.12 if nacht else 1.0
    s.append(f'background {{ rgb {0.02 if nacht else 0.93} }}\n')
    s.append(f'sky_sphere {{ pigment {{ gradient y color_map {{ [0 rgb {0.03 if nacht else 0.95}] [1 rgb {0.05 if nacht else 1.0}] }} }} }}\n')
    s.append(f'light_source {{ {v(-300,-700,900)} color rgb {0.85*hell} area_light <600,0,0>, <0,0,600>, 6, 6 adaptive 1 jitter }}\n')
    s.append(f'light_source {{ {v(1200,-500,500)} color rgb {0.35*hell} area_light <400,0,0>, <0,0,400>, 4, 4 adaptive 1 jitter }}\n')
    s.append(f'light_source {{ {v(B/2,600,800)} color rgb {0.35*hell} }}\n')
    # Untergrund
    s.append(f'plane {{ y, -20 texture {{ pigment {{ rgb {0.06 if nacht else 0.78} }} finish {{ diffuse 0.9 specular 0.05 reflection 0.03 }} }} }}\n')
    # Holztexturen (Nuss Sizilia), Maserung längs
    s.append('#declare Nuss_Flach = texture { pigment { image_map { png "nuss_sizilia.png" interpolate 2 } scale <420,290,1> rotate x*90 } '
             'finish { diffuse 0.85 specular 0.12 roughness 0.04 } }\n')
    s.append('#declare Nuss_Seite = texture { pigment { image_map { png "nuss_sizilia.png" interpolate 2 } scale <420,290,1> rotate y*90 } '
             'finish { diffuse 0.85 specular 0.12 roughness 0.04 } }\n')
    s.append('#declare Nuss_Front = texture { pigment { image_map { png "nuss_sizilia.png" interpolate 2 } scale <420,290,1> } '
             'finish { diffuse 0.85 specular 0.12 roughness 0.04 } }\n')
    s.append('#declare Chrom = texture { pigment { rgb <0.82,0.83,0.85> } finish { ambient 0 diffuse 0.15 specular 0.9 roughness 0.002 metallic reflection { 0.75 metallic } } }\n')
    s.append('#declare Schwarz = texture { pigment { rgb 0.025 } finish { diffuse 0.6 specular 0.35 roughness 0.015 reflection 0.03 } }\n')
    # Korpus
    s.append(box(0, 0, 0, B, T, t, "Nuss_Flach"))
    s.append(box(0, 0, H - t, B, T, H, "Nuss_Flach"))
    s.append(box(0, 0, t, t, T, H - t, "Nuss_Seite"))
    s.append(box(B - t, 0, t, B, T, H - t, "Nuss_Seite"))
    s.append(box(t, 18, t, B - t, T - t, H - t, "pigment { rgb 0.05 }"))   # Innenraum dunkel
    # Frontbretter (sichtbar durch den klaren Rand der Frontplatte)
    s.append(box(t, 10, t, pl_x + 22, 18, H - t, "Nuss_Front"))
    s.append(box(pl_x + 278, 10, t, B - t, 18, H - t, "Nuss_Front"))
    s.append(box(pl_x + 22, 10.3, t, pl_x + 278, 13.3, pl_z + 49.3, "pigment { rgb 0.03 } finish { diffuse 0.6 }"))   # Träger, schwarz gedruckt
    # Lichtkasten-Diffusor hinter der Skala
    if nacht:
        diff = 'pigment { rgb <1,0.72,0.38> } finish { emission 1.6 diffuse 0 }'
    else:
        diff = 'pigment { rgb 0.92 } finish { diffuse 0.9 }'
    s.append(box(pl_x + 28, 9.9, pl_z + 49.5, pl_x + 228, 10.3, pl_z + 105.5, diff))
    if nacht:   # Senderzeiger: eine rote LED-Spalte bei "Radio DDR"
        zx = pl_x + 152
        s.append(box(zx - 2.5, 9.85, pl_z + 50, zx + 2.5, 9.95, pl_z + 105, 'pigment { rgb <1,0.08,0.03> } finish { emission 4 diffuse 0 }'))
    # Frontplatte mit Fotografie, durchsichtige Stellen per Alphakanal
    s.append(f'box {{ <0,0,0>, <1,1,1> texture {{ pigment {{ image_map {{ png "frontplatte.png" interpolate 2 }} }} '
             f'finish {{ diffuse 0.8 specular 0.35 roughness 0.01 reflection 0.04 }} }} '
             f'scale <300,114,3> translate {v(pl_x, 7, pl_z)} }}\n')
    # Lautsprecherabdeckungen mit Riffelung
    for x0 in (t, B - t - abd_b):
        z0 = t + (122 - abd_h) / 2
        s.append(box(x0, rueck + 2, z0, x0 + abd_b, rueck + abd_t, z0 + abd_h, "Schwarz"))
        s.append(box(x0, rueck, z0, x0 + 2, rueck + 2, z0 + abd_h, "Schwarz"))
        s.append(box(x0 + abd_b - 2, rueck, z0, x0 + abd_b, rueck + 2, z0 + abd_h, "Schwarz"))
        z = z0 + 1.2
        while z + 2.2 < z0 + abd_h:
            s.append(f'cylinder {{ {v(x0+2, rueck+1.4, z+1.1)}, {v(x0+abd_b-2, rueck+1.4, z+1.1)}, 1.2 texture {{ Schwarz }} }}\n')
            z += 3.2
    # Chromleisten 4 x 4
    for z0 in (t, H - t - 4):
        s.append(box(t, rueck, z0, B - t, rueck + 4, z0 + 4, "Chrom"))
    # Drehknöpfe: Chrom, geriffelt, farbiger Deckel
    for px, pz, farbe in knoepfe:
        x, z = pl_x + px, pl_z + pz
        deckel = 'rgb <0.75,0.05,0.04>' if farbe == "rot" else 'rgb 0.03'
        s.append('difference { ')
        s.append(f'cone {{ {v(x,7,z)}, 8, {v(x,-12,z)}, 7.5 }}')
        for i in range(10):
            s.append(f'box {{ <-0.9,-30,-2>, <0.9,30,2> translate <0,0,-8.2> rotate y*0 translate <0,0,0> '
                     f'rotate z*{i*36} translate {v(x,-2.5,z)} scale 1 }}' if False else '')
        s.append(f'cylinder {{ {v(x,-12.5,z)}, {v(x,-11,z)}, 6.6 }}')
        s.append(' texture { Chrom } }\n')
        for i in range(12):   # Rippen
            import math
            a = 2 * math.pi * i / 12
            dx, dz = 7.6 * math.cos(a), 7.6 * math.sin(a)
            s.append(f'cylinder {{ {v(x+dx,5,z+dz)}, {v(x+dx*0.95,-10.5,z+dz*0.95)}, 0.7 texture {{ Chrom }} }}\n')
        s.append(f'cylinder {{ {v(x,-11.3,z)}, {v(x,-11.0,z)}, 6.6 texture {{ pigment {{ {deckel} }} finish {{ specular 0.5 roughness 0.01 reflection 0.05 }} }} }}\n')
    # Tasten (schwarz, verjüngt)
    for px in tasten:
        x, z = pl_x + px, pl_z + 13.5
        s.append(f'prism {{ linear_sweep linear_spline 0, 18, 5, <-6,-6>, <6,-6>, <6,6>, <-6,6>, <-6,-6> '
                 f'scale <0.95,1,0.95> rotate x*-90 translate {v(x,-1,z)} texture {{ Schwarz }} }}\n'.replace(
                 f'translate {v(x,-1,z)}', f'translate <{x:.2f},{z:.2f},-1>'))
    # Chromfüße
    for fx, fy in fuss:
        s.append(f'cone {{ {v(fx,fy,0)}, 12.5, {v(fx,fy,-20)}, 8.5 texture {{ Chrom }} }}\n')
    return "".join(s)

for name, nacht in (("rendering_tag", False), ("rendering_nacht", True)):
    open(f"{name}.pov", "w").write(szene(nacht))
    q = "+A0.1 +AM2 +R3" if gut else "-A"
    subprocess.run(f"povray -D +I{name}.pov +O{name}.png +W{breite} +H{hoehe} {q} +Q9 2>&1 | tail -3", shell=True)
