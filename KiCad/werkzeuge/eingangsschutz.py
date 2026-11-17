#!/usr/bin/python3
# Einmalige Aenderung 17 (17.11.2026): Eingangsschutz an J4 einbauen.
# J4+ -> F1 (Sicherung) -> Q2 (P-MOSFET, Verpolungsschutz) -> FB1 (Ferrit) -> PVDD
# D2 (TVS) und C46 (10 uF) hinter Q2 nach GND, D3 (Z-Diode) + R13 begrenzen die Gate-Spannung von Q2.
# Ausserdem GPIO11 vom Diagonalweg an den Platinenrand verlegt, damit die Ecke frei wird.
# Aufruf: python3 eingangsschutz.py KiCad/RadioHAT.kicad_pcb
import sys, pcbnew
B = pcbnew.LoadBoard(sys.argv[1])
MM = pcbnew.FromMM
V = lambda x, y: pcbnew.VECTOR2I(MM(x), MM(y))
LIB = '/usr/share/kicad/footprints/'

def net(name):
    n = B.FindNet(name)
    if n is None:
        n = pcbnew.NETINFO_ITEM(B, name); B.Add(n)
    return n

TR = [t for t in B.Tracks()]
DEL = []

def same(a, b): return abs(a.x - b.x) < 10000 and abs(a.y - b.y) < 10000

def remove_track(layer, a, b):
    for t in TR:
        if t.GetClass() == 'PCB_TRACK' and t.GetLayerName() == layer and \
           ((same(t.GetStart(), V(*a)) and same(t.GetEnd(), V(*b))) or (same(t.GetStart(), V(*b)) and same(t.GetEnd(), V(*a)))):
            DEL.append(t); return
    raise SystemExit(f'Leiterbahn nicht gefunden: {layer} {a} {b}')

def remove_via(x, y):
    for t in TR:
        if t.GetClass() == 'PCB_VIA' and same(t.GetPosition(), V(x, y)):
            DEL.append(t); return
    raise SystemExit(f'Via nicht gefunden: {x} {y}')

def track(layer, pts, w, n):
    for a, b in zip(pts, pts[1:]):
        t = pcbnew.PCB_TRACK(B); t.SetStart(V(*a)); t.SetEnd(V(*b)); t.SetWidth(MM(w))
        t.SetLayer(B.GetLayerID(layer)); t.SetNet(net(n)); B.Add(t)

def via(x, y, n, drill=0.4, dia=0.8):
    v = pcbnew.PCB_VIA(B); v.SetPosition(V(x, y)); v.SetDrill(MM(drill)); v.SetWidth(MM(dia))
    v.SetNet(net(n)); B.Add(v)

def place(lib, name, ref, val, x, y, rot, nets, fpid=None):
    if lib:
        fp = pcbnew.FootprintLoad(LIB + lib, name)
    else:
        fp = pcbnew.Cast_to_FOOTPRINT(B.FindFootprintByReference(name).Duplicate())
    fp.SetReference(ref); fp.SetValue(val)
    if fpid: fp.SetFPIDAsString(fpid)
    fp.SetPosition(V(x, y)); fp.SetOrientationDegrees(rot)
    B.Add(fp)
    for p in fp.Pads(): p.SetNet(net(nets[p.GetNumber()]))
    fp.Value().SetVisible(False)
    fp.Reference().SetLayer(B.GetLayerID('F.Fab'))  # wie bei den uebrigen Bauteilen: Bezeichner auf F.Fab
    return fp

# ---- GPIO11 an den Rand verlegen
remove_track('F.Cu', (102.88, 125.62), (120.12, 142.88))
remove_track('F.Cu', (120.12, 142.88), (120.12, 147.38))
remove_track('F.Cu', (120.12, 147.38), (120.38, 147.62))
remove_track('F.Cu', (102.75, 125.38), (102.88, 125.5))
remove_track('F.Cu', (102.88, 125.5), (102.88, 125.62))
remove_via(103, 146)
GPIO11_NEU = ([(102.75, 125.38), (101.4, 126.73), (101.4, 144.0), (105.0, 147.62), (120.38, 147.62)], 0.25, 'GPIO11')

# ---- alte Zuleitung J4 -> PVDD auf der Unterseite entfernen
remove_track('B.Cu', (109.5, 146.0), (109.5, 137.0))
remove_track('B.Cu', (109.5, 137.0), (112.0, 131.0))
for x, y in ((113, 141), (113, 126), (108, 136)): remove_via(x, y)
for t in DEL: B.Remove(t)
track('F.Cu', *GPIO11_NEU)
for p in B.FindFootprintByReference('J4').Pads():
    if p.GetNumber() == '1': p.SetNet(net('VIN'))

# ---- Bestueckungsdruck: Texte "EIN/AUS" und "+ 20V -" liegen auf den neuen Bauteilen -> entfernen, neu setzen
BOXES = [(105.3, 127.8, 111.1, 129.3),     # EIN/AUS
         (108.8, 140.0, 115.2, 142.2)]     # + 20V -
SILK = []
for d in B.GetDrawings():
    if d.GetLayerName() != 'F.Silkscreen': continue
    bb = d.GetBoundingBox()
    if any(bb.GetX() >= MM(x0) and bb.GetRight() <= MM(x1) and bb.GetY() >= MM(y0) and bb.GetBottom() <= MM(y1) for x0, y0, x1, y1 in BOXES):
        SILK.append(d)
for d in SILK: B.Remove(d)
def silk_text(t, x, y, rot, h=1.0):
    tx = pcbnew.PCB_TEXT(B); tx.SetText(t); tx.SetPosition(V(x, y)); tx.SetLayer(B.GetLayerID('F.Silkscreen'))
    tx.SetTextSize(V(h, h)); tx.SetTextThickness(MM(0.15)); tx.SetTextAngleDegrees(rot); B.Add(tx)
silk_text('EIN/AUS', 103.3, 130.4, 90, 0.8)
silk_text('+20V', 106.2, 141.7, 0, 0.9)

# ---- Bauteile
Q2 = place('Package_SO.pretty', 'SOIC-8_3.9x4.9mm_P1.27mm', 'Q2', 'AO4407A', 111.5, 134.5, 0,
           {'1': 'VIN_P', '2': 'VIN_P', '3': 'VIN_P', '4': 'Q2G', '5': 'VIN_F', '6': 'VIN_F', '7': 'VIN_F', '8': 'VIN_F'},
           'RadioHAT:SOIC-8_3.9x4.9mm_P1.27mm')
F1 = place('Fuse.pretty', 'Fuse_1206_3216Metric', 'F1', '5A T 63V', 111.9, 141.0, 0, {'1': 'VIN', '2': 'VIN_F'},
           'RadioHAT:Fuse_1206_3216Metric')
D3 = place('Diode_SMD.pretty', 'D_SOD-123', 'D3', 'BZT52C15', 109.0, 138.6, 0, {'1': 'VIN_P', '2': 'Q2G'},
           'RadioHAT:D_SOD-123')
R13 = place(None, 'R7', 'R13', '10k 1%', 111.9, 138.0, 90, {'1': 'GND', '2': 'Q2G'})
FB1 = place('Inductor_SMD.pretty', 'L_1206_3216Metric', 'FB1', 'BLM31KN121SN1L', 109.025, 129.45, 90,
            {'1': 'VIN_P', '2': 'PVDD'}, 'RadioHAT:L_1206_3216Metric')
C46 = place(None, 'C23', 'C46', '10uF 50V X5R', 111.9, 129.5, 90, {'1': 'VIN_P', '2': 'GND'})
D2 = place('Diode_SMD.pretty', 'D_SMB', 'D2', 'SMBJ22A', 105.5, 130.7, 90, {'1': 'VIN_P', '2': 'GND'},
           'RadioHAT:D_SMB')

# ---- Leiterbahnen (Oberseite)
track('F.Cu', [(109.5, 146.0), (109.5, 143.0), (110.5, 142.0), (110.5, 141.0)], 1.5, 'VIN')
track('F.Cu', [(113.3, 141.0), (113.975, 140.0), (113.975, 136.405)], 1.5, 'VIN_F')
track('F.Cu', [(113.975, 136.405), (113.975, 133.2)], 0.9, 'VIN_F')
track('F.Cu', [(109.025, 131.025), (109.025, 132.595)], 1.5, 'VIN_P')
track('F.Cu', [(109.025, 132.595), (109.025, 135.135)], 0.9, 'VIN_P')
track('F.Cu', [(109.025, 131.0), (111.9, 131.0)], 1.0, 'VIN_P')
track('F.Cu', [(105.5, 132.85), (106.4, 132.6), (109.025, 132.6)], 1.0, 'VIN_P')
track('F.Cu', [(108.05, 135.135), (107.35, 135.135), (107.35, 138.6)], 0.4, 'VIN_P')
track('F.Cu', [(110.0, 136.405), (110.65, 137.055), (110.65, 138.6)], 0.4, 'Q2G')
track('F.Cu', [(110.65, 137.175), (111.9, 137.175)], 0.4, 'Q2G')
track('F.Cu', [(111.9, 138.825), (111.9, 139.75)], 0.4, 'GND'); via(111.9, 139.75, 'GND', 0.3, 0.6)
track('F.Cu', [(111.9, 128.025), (111.9, 126.9)], 0.5, 'GND'); via(111.9, 126.9, 'GND', 0.3, 0.6)
track('F.Cu', [(105.5, 128.55), (105.5, 126.5)], 0.8, 'GND'); via(105.5, 126.5, 'GND', 0.3, 0.6)
# PVDD hinter dem Ferrit: zwei Durchkontaktierungen 0,4/0,8 auf die bestehende Leitung der Unterseite
track('F.Cu', [(109.025, 127.875), (109.025, 126.6)], 1.5, 'PVDD')
track('F.Cu', [(108.5, 126.6), (109.6, 126.6)], 0.8, 'PVDD')
via(108.5, 126.6, 'PVDD'); via(109.6, 126.6, 'PVDD')
track('B.Cu', [(108.5, 126.6), (109.6, 126.6)], 0.8, 'PVDD')
track('B.Cu', [(109.05, 126.6), (109.05, 131.0)], 1.5, 'PVDD')
for fp in (Q2, F1, D3, R13, FB1, C46, D2):
    print(fp.GetReference(), [(p.GetNumber(), p.GetNetname(), round(p.GetPosition().x / 1e6, 3), round(p.GetPosition().y / 1e6, 3)) for p in fp.Pads()])
# kein Bestueckungsdruck an den neuen Bauteilen (wie bei C11 bis C14); Lage zeigen F.Fab und die Bestueckungsvorschau
for fp in (Q2, F1, D3, FB1, D2, R13, C46):
    silk = [g for g in fp.GraphicalItems() if g.GetLayerName() == 'F.Silkscreen']
    for g in silk: fp.Remove(g)
pcbnew.SaveBoard(sys.argv[1], B)
