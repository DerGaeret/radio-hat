#!/usr/bin/python3
# Einmalige Aenderung 24 (17.11.2026): Kuehlflaeche unter U1 nach dem Land Pattern im Datenblatt TAS5805M (Seite 99):
# Kupfer 3,4 x 9,7 mm unter dem IC (frei bleibt wie bisher 3,1 x 4,05 mm), 24 Vias im Raster 1,2 mm (3 x 8).
# Unter U1 laeuft danach keine Signalleitung mehr: GPIO12 und GPIO6 (Encoder 1) auf der Unterseite am Nordrand des Via-Felds,
# HOLD auf Innenlage 1 direkt vom Sockelpin 7 (nicht unter I2S/I2C), GPIO7 auf der Oberseite links neben U1.
# Nebenbei: +3V3 auf der Unterseite am frueheren Umweg zwischen GPIO24 und HOLD 0,5 statt 0,35 mm breit.
# Ausgangsstand: Platine nach Aenderung 23 (Git ecbaa72). DRC danach 0 Verstoesse, 0 unverbundene Pads.
# Aufruf: python3 aenderung_24.py KiCad/RadioHAT.kicad_pcb   (nicht erneut ausfuehren)
import os, sys, pcbnew
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import router   # router.py im selben Ordner
B = pcbnew.LoadBoard(sys.argv[1]); MM = pcbnew.FromMM
V = lambda x, y: pcbnew.VECTOR2I(MM(x), MM(y))
net = lambda n: B.FindNet(n)
TR = [t for t in B.Tracks()]; DEL = []
same = lambda a, b: abs(a.x - b.x) < 10000 and abs(a.y - b.y) < 10000
def rm_track(layer, a, b):
    for t in TR:
        if t.GetClass() == 'PCB_TRACK' and t.GetLayerName() == layer and \
           ((same(t.GetStart(), V(*a)) and same(t.GetEnd(), V(*b))) or (same(t.GetStart(), V(*b)) and same(t.GetEnd(), V(*a)))):
            DEL.append(t); return
    raise SystemExit(f'Leiterbahn nicht gefunden: {layer} {a} {b}')
def rm_via(x, y):
    for t in TR:
        if t.GetClass() == 'PCB_VIA' and same(t.GetPosition(), V(x, y)): DEL.append(t); return
    raise SystemExit(f'Via nicht gefunden: {x} {y}')
def track(layer, pts, w, n):
    for a, b in zip(pts, pts[1:]):
        t = pcbnew.PCB_TRACK(B); t.SetStart(V(*a)); t.SetEnd(V(*b)); t.SetWidth(MM(w))
        t.SetLayer(B.GetLayerID(layer)); t.SetNet(net(n)); B.Add(t)
def via(x, y, n):
    v = pcbnew.PCB_VIA(B); v.SetPosition(V(x, y)); v.SetDrill(MM(0.3)); v.SetWidth(MM(0.6)); v.SetNet(net(n)); B.Add(v)

# --- alte Teile entfernen
rm_via(128.775, 110.35)                                                     # GND-Via an Pin 14 (liegt jetzt im Via-Feld)
for a, b in [((126.125, 107.875), (128.0, 109.75)), ((128.0, 109.75), (128.0, 110.625)), ((128.0, 110.625), (128.375, 111.0)),
             ((128.375, 111.0), (128.375, 111.5)), ((128.375, 113.0), (127.5, 113.875)), ((127.5, 113.875), (127.5, 114.875))]:
    rm_track('F.Cu', a, b)                                                  # GPIO7 Oberseite am linken Rand von U1
rm_track('B.Cu', (128.375, 113.0), (128.375, 111.5)); rm_via(128.375, 111.5); rm_via(128.375, 113.0)
for a, b in [((138.875, 110.5), (138.25, 111.125)), ((138.25, 111.125), (137.25, 111.125)), ((137.25, 111.125), (137.125, 111.25)),
             ((137.125, 111.25), (136.25, 111.25)), ((136.25, 111.25), (136.125, 111.375)), ((136.125, 111.375), (135.875, 111.375)),
             ((135.875, 111.375), (135.75, 111.5)), ((151.5, 110.5), (138.875, 110.5))]:
    rm_track('F.Cu', a, b)                                                  # GPIO12 Oberseite unter/neben U1
rm_via(135.75, 111.5); rm_track('B.Cu', (135.75, 111.5), (131.125, 111.5)); rm_track('B.Cu', (131.125, 111.5), (116.125, 96.5))
for a, b in [((145.25, 104.125), (138.25, 111.125)), ((138.25, 111.125), (137.125, 111.125)), ((137.125, 111.125), (136.0, 112.25)),
             ((136.0, 112.25), (130.375, 112.25))]:
    rm_track('B.Cu', a, b)                                                  # HOLD Unterseite unter U1
rm_via(130.375, 112.25)
rm_track('B.Cu', (137.625, 110.0), (138.0, 110.375)); rm_via(138.0, 110.375)            # GPIO6-Via lag im neuen Kuehlkupfer
for a, b in [((132.5, 109.125), (133.25, 109.875)), ((133.25, 109.875), (133.375, 109.875)), ((133.375, 109.875), (133.5, 110.0)),
             ((133.5, 110.0), (137.625, 110.0))]:
    rm_track('B.Cu', a, b)                                                  # GPIO6 Unterseite, lag 0,1 mm zu nah an der oberen Via-Reihe
rm_track('F.Cu', (138.0, 110.375), (138.25, 110.375)); rm_track('F.Cu', (138.25, 110.375), (139.375, 109.25))
# HOLD: ganzer bisheriger Weg auf der Unterseite entfaellt, HOLD beginnt jetzt auf In1 direkt am Sockelpin 7 (durchkontaktiert)
for a, b in [((149.0, 87.25), (149.25, 87.25)), ((149.25, 87.25), (150.5, 86.0)), ((150.5, 86.0), (152.625, 86.0)),
             ((152.625, 86.0), (152.75, 86.125)), ((152.75, 86.125), (152.75, 86.375)), ((152.75, 86.375), (152.875, 86.5))]:
    rm_track('B.Cu', a, b)
for a, b in [((152.875, 86.5), (152.875, 90.5)), ((152.875, 90.5), (152.75, 90.625)), ((152.75, 90.625), (152.75, 90.875)),
             ((152.75, 90.875), (152.25, 91.375)), ((152.25, 91.375), (152.25, 93.0)), ((152.25, 93.0), (151.25, 94.0)), ((151.25, 94.0), (151.25, 96.0)),
             ((151.25, 96.0), (151.125, 96.125)), ((151.125, 96.125), (151.125, 96.25)), ((151.125, 96.25), (151.0, 96.375)),
             ((151.0, 96.375), (151.0, 96.5)), ((151.0, 96.5), (148.0, 99.5)), ((148.0, 99.5), (148.0, 100.125)),
             ((148.0, 100.125), (147.875, 100.25)), ((147.875, 100.25), (147.875, 100.375)), ((147.875, 100.375), (145.25, 103.0)),
             ((145.25, 103.0), (145.25, 104.125))]:
    rm_track('B.Cu', a, b)
for a, b in [((130.375, 112.25), (125.25, 112.25)), ((125.25, 112.25), (122.625, 109.625)), ((122.625, 109.625), (120.375, 109.625)),
             ((120.375, 109.625), (117.625, 112.375))]:
    rm_track('F.Cu', a, b)                                                  # HOLD Oberseite links von U1
# +3V3 auf der Unterseite: Der Umweg zwischen GPIO24 und dem alten HOLD-Weg (0,35 bis 0,45 mm) wird frei und 0,5 mm breit
for a, b in [((146.7536, 97.7536), (147.0643, 98.0643)), ((147.0643, 98.0643), (147.375, 98.375)), ((147.375, 98.375), (147.375, 98.8125)),
             ((147.375, 98.8125), (147.375, 99.25)), ((147.375, 99.25), (147.375, 99.6875)), ((147.375, 99.6875), (147.375, 100.125)),
             ((147.375, 100.125), (147.125, 100.375)), ((147.125, 100.375), (146.875, 100.625)), ((146.875, 100.625), (146.4375, 100.625))]:
    rm_track('B.Cu', a, b)
U1 = B.FindFootprintByReference('U1')
oldvias = [p for p in U1.Pads() if p.GetNumber() == '29' and p.GetDrillSize().x > 0]
assert len(oldvias) == 8
tmpl = pcbnew.Cast_to_PAD(oldvias[0].Duplicate())
expad = [p for p in U1.Pads() if p.GetNumber() == '29' and p.GetDrillSize().x == 0][0]
for t in DEL: B.Remove(t)
for p in oldvias: U1.Remove(p)

# --- Kuehlflaeche: Kupfer 9,7 x 3,4 mm unter Loetstopp, dazu 24 Vias 0,3/0,6 mm im Raster 1,2 mm
cu = pcbnew.PAD(U1); cu.SetAttribute(pcbnew.PAD_ATTRIB_SMD); cu.SetShape(pcbnew.PAD_SHAPE_RECT)
ls = pcbnew.LSET(); ls.AddLayer(pcbnew.F_Cu); cu.SetLayerSet(ls); cu.SetNumber('29')
U1.Add(cu); cu.SetOrientation(expad.GetOrientation()); cu.SetSize(V(3.4, 9.7)); cu.SetPos0(V(0, 0)); cu.SetDrawCoord()
cu.SetNet(net('GND'))
for dx in (-4.2, -3.0, -1.8, -0.6, 0.6, 1.8, 3.0, 4.2):
    for dy in (-1.2, 0.0, 1.2):
        p = pcbnew.Cast_to_PAD(tmpl.Duplicate()); U1.Add(p)
        p.SetPos0(V(dy, -dx)); p.SetDrawCoord(); p.SetNet(net('GND'))       # Bauteilkoordinaten: x = dy, y = -dx (U1 um -90 Grad)

# --- +3V3 Unterseite: Umweg 0,5 mm breit, 0,825 mm neben den Vias von GND und GPIO24
track('B.Cu', [(146.7536, 97.7536), (147.05, 97.7536), (147.45, 98.1536), (147.45, 100.375), (147.2, 100.625), (146.4375, 100.625)], 0.5, '+3V3')
# --- GPIO7: Oberseite links an U1 vorbei
track('F.Cu', [(126.125, 107.875), (127.5, 109.25), (127.5, 114.875)], 0.25, 'GPIO7')
# --- GPIO12 und GPIO6 auf der Unterseite nebeneinander am Nordrand des Via-Felds (Mitte y 110,15 und 109,45),
#     Abstand zu den Vias (y 110,8) 0,225 mm, zu SDA (y 108,75) 0,45 mm
track('B.Cu', [(116.125, 96.5), (129.775, 110.15), (139.25, 110.15), (139.6, 110.5)], 0.25, 'GPIO12')
track('F.Cu', [(151.5, 110.5), (139.6, 110.5)], 0.25, 'GPIO12'); via(139.6, 110.5, 'GPIO12')
track('B.Cu', [(132.5, 109.125), (132.825, 109.45), (139.075, 109.45), (139.375, 109.15)], 0.25, 'GPIO6'); via(139.375, 109.15, 'GPIO6')
track('F.Cu', [(139.375, 109.15), (139.375, 109.25)], 0.25, 'GPIO6')
# --- HOLD: Oberseite zu D1 beginnt an einer Durchkontaktierung bei C1, der Weg vom Sockelpin 7 dorthin folgt unten auf In1
track('F.Cu', [(119.65, 110.3), (117.625, 112.375)], 0.25, 'HOLD'); via(119.65, 110.3, 'HOLD')

EDGE = (100.6, 85.6, 164.4, 149.4)
# Takt- und Datenleitungen der Oberseite (I2S, I2C) haben ihre Bezugsflaeche auf In1: darunter wird nicht geroutet.
TAKT = ('SCLK_PI', 'SCLK', 'LRCLK_PI', 'LRCLK', 'SDIN_PI', 'SDIN', 'SDA', 'SCL')
unter_takt = []
for t in B.Tracks():
    if t.GetClass() == 'PCB_TRACK' and t.GetLayerName() == 'F.Cu' and t.GetNetname() in TAKT:
        a, b = t.GetStart(), t.GetEnd()
        unter_takt.append(('s', (a.x / 1e6, a.y / 1e6, b.x / 1e6, b.y / 1e6), t.GetWidth() / 2e6 + 0.3 + 0.125))
for f in B.GetFootprints():
    for p in f.Pads():
        if p.GetNetname() in TAKT and p.IsOnLayer(pcbnew.F_Cu): unter_takt += router.pad_obstacle(p, pcbnew.F_Cu, 0.3 + 0.125)
for n, s, g, box in [('HOLD', (149.01, 87.23), (119.65, 110.3), (112, 86, 157, 118))]:
    # Sperrbereiche auf In1: I2S/I2C zwischen U1 und R2-R5/C8-C10, Endstufe (Ausgaenge, Spulen, PVDD), Schaltknoten des 5-V-Reglers
    keep = [('r', (128.9, 102.6, 136.9, 108.3), 0.2), ('r', (114.0, 113.6, 152.0, 135.0), 0.2), ('r', (101.0, 97.0, 114.5, 118.0), 0.2)]
    keep += unter_takt
    obs = router.obstacles(B, 'In1.Cu', n, 0.25, extra=keep)
    path = router.route(obs, s, g, EDGE, box)
    if path is None: raise SystemExit('kein Weg fuer ' + n)
    print(n, 'In1:', path, 'Laenge %.1f mm' % sum(((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5 for a, b in zip(path, path[1:])))
    track('In1.Cu', path, 0.25, n)
pcbnew.SaveBoard(sys.argv[1], B)
