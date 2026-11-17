#!/usr/bin/python3
# Einmalige Aenderung 27 (17.11.2026): Platz fuer Schraubklemmen bis 11 mm Tiefe an J2, J3, J4.
# Die Platine wird unten um 5 mm laenger (65 x 70 mm). J2, J3, J4 ruecken mit 5 mm nach unten, ihre Lotstifte bleiben 4 mm
# vom (neuen) Rand. Vom Lotstift bis zum naechsten Bauteil (F1) sind es danach 8,85 mm, frei gehalten werden 7,5 mm:
# Eine 11 mm tiefe Klemme mit mittigen Stiften ragt 5,5 mm nach innen, eine mit Stiften 3,5 mm hinter der Vorderkante 7,5 mm.
# Bestueckungsdruck der Klemmen: Rahmen von 0,36 mm ueber dem Rand bis 7,5 mm ueber den Stiften (= Platz fuer die Klemme).
# Masseflaechen, Platinenrand, Bohr-/Platzierungsursprung und Passbohrung TH1 ruecken mit. Die Befestigungsloecher
# H1-H4 bleiben, wo sie sind (Raster des Pi). Ausgangsstand: Rev. 1.0 (Git 41ceedf).
# Koordinaten wie im Pruefbericht (bisheriger Ursprung): x nach rechts, y nach oben; der neue Rand liegt bei y = -5.
# Aufruf: python3 aenderung_27.py KiCad/RadioHAT.kicad_pcb   (nicht erneut ausfuehren)
import sys, pcbnew
B = pcbnew.LoadBoard(sys.argv[1]); MM = pcbnew.FromMM
X0, Y0 = 100, 150; D = 5.0
V = lambda x, y: pcbnew.VECTOR2I(MM(X0 + x), MM(Y0 - y))
P = lambda v: (v.x / 1e6 - X0, Y0 - v.y / 1e6)
DOWN = pcbnew.VECTOR2I(0, MM(D))
net = lambda n: B.FindNet(n)
def track(layer, pts, w, n):
    for a, b in zip(pts, pts[1:]):
        t = pcbnew.PCB_TRACK(B); t.SetStart(V(*a)); t.SetEnd(V(*b)); t.SetWidth(MM(w))
        t.SetLayer(B.GetLayerID(layer)); t.SetNet(net(n)); B.Add(t)

# 1. Platinenrand: untere Kante und die beiden unteren Ecken 5 mm tiefer, Seitenkanten verlaengert
for d in list(B.GetDrawings()):
    if d.GetLayerName() != 'Edge.Cuts': continue
    s, e = P(d.GetStart()), P(d.GetEnd())
    if d.GetShapeStr() == 'Arc' and min(s[1], e[1]) < 1: d.Move(DOWN)
    elif d.GetShapeStr() == 'Line' and max(s[1], e[1]) < 1: d.Move(DOWN)
    elif d.GetShapeStr() == 'Line' and abs(s[0] - e[0]) < 0.01:
        if s[1] < e[1]: d.SetStart(V(s[0], s[1] - D))
        else: d.SetEnd(V(e[0], e[1] - D))
# 2. Masseflaechen nach unten erweitern
for z in B.Zones():
    if z.GetIsRuleArea(): continue
    o = z.Outline()
    for i in range(o.TotalVertices()):
        x, y = P(o.CVertex(i))
        if y < 0.01: o.SetVertex(i, V(x, y - D))
# 3. Ursprung (Bohr-/Platzierungsdateien) auf die neue Ecke links unten
B.GetDesignSettings().SetAuxOrigin(V(0, -D)); B.GetDesignSettings().SetGridOrigin(V(0, -D))
# 4. Klemmen J2, J3, J4 nach unten, Zuleitungen verlaengern (je 1,5 mm wie bisher)
for r in ('J2', 'J3', 'J4'): B.FindFootprintByReference(r).Move(DOWN)
for x, n in ((9.5, 'VIN'), (21.7, 'SPKB+'), (26.7, 'SPKB-'), (41.5, 'SPKA-'), (46.5, 'SPKA+')):
    track('F.Cu', [(x, 4.0), (x, 4.0 - D)], 1.5, n)
# Masse-Vias neben J4 Pin 2 mitnehmen; GPIO11 lief auf der Oberseite bei y = 2,38 unter den Klemmen durch und wuerde
# jetzt die verlaengerten Zuleitungen kreuzen: dieses Stueck auf die Unterseite (Via bei x = 7,5 entfaellt, neues bei 48,125)
DEL = []
for t in list(B.Tracks()):
    if t.GetClass() == 'PCB_VIA':
        x, y = P(t.GetPosition())
        if abs(y - 4.0) < 0.01 and (abs(x - 13.0) < 0.01 or abs(x - 18.0) < 0.01): t.Move(DOWN)
        if t.GetNetname() == 'GPIO11' and abs(x - 7.5) < 0.01 and abs(y - 2.38) < 0.01: DEL.append(t)
    elif t.GetNetname() == 'GPIO11' and t.GetLayerName() == 'F.Cu':
        s, e = P(t.GetStart()), P(t.GetEnd())
        if max(s[1], e[1]) < 2.7: DEL.append(t)
assert len(DEL) == 4, len(DEL)
for t in DEL: B.Remove(t)
track('B.Cu', [(7.5, 2.38), (47.88, 2.38), (48.125, 2.625)], 0.25, 'GPIO11')
v = pcbnew.PCB_VIA(B); v.SetPosition(V(48.125, 2.625)); v.SetDrill(MM(0.3)); v.SetWidth(MM(0.6)); v.SetNet(net('GPIO11')); B.Add(v)
# 5. Passbohrung TH1 in die neue Ecke
B.FindFootprintByReference('TH1').Move(DOWN)
# 6. Bestueckungsdruck der Klemmen: Rahmen 0,36 mm ueber dem Rand bis 7,5 mm ueber den Stiften (y = -1)
for d in list(B.GetDrawings()):
    if d.GetLayerName() != 'F.Silkscreen' or d.GetClass() != 'PCB_SHAPE': continue
    s, e = P(d.GetStart()), P(d.GetEnd())
    for x0, x1 in ((6.9, 17.1), (19.1, 29.3), (38.9, 49.1)):
        if all(x0 - 0.01 <= p[0] <= x1 + 0.01 and 0.3 <= p[1] <= 7.71 for p in (s, e)):
            f = lambda y: -4.64 if y < 0.4 else (6.5 if y > 7.6 else y - D)
            d.SetStart(V(s[0], f(s[1]))); d.SetEnd(V(e[0], f(e[1])))
pcbnew.SaveBoard(sys.argv[1], B)
print('Aenderung 27 eingebaut')
