#!/usr/bin/python3
# Einmalige Aenderungen 20 und 21 (17.11.2026), nach dem Abgleich mit dem Datenblatt TAS5805M (SLASEH5D):
# 20: C47/C48 10 uF 50 V 0805 an PVDD je Seite (Datenblatt 8.1.3 und Tabelle 8-4: 22 uF keramisch je PVDD-Seite)
# 21: Lotpaste unter dem Kuehlpad von U1 als 2x2-Raster mit 75 % der Padflaeche (Datenblatt 9.1.3.2.2: 70-80 %, mehrere Oeffnungen)
# Aufruf: python3 aenderung_20_21.py KiCad/RadioHAT.kicad_pcb   (nicht erneut ausfuehren)
import sys, pcbnew
B = pcbnew.LoadBoard(sys.argv[1]); MM = pcbnew.FromMM
V = lambda x, y: pcbnew.VECTOR2I(MM(x), MM(y))
net = lambda n: B.FindNet(n)

def track(layer, pts, w, n):
    for a, b in zip(pts, pts[1:]):
        t = pcbnew.PCB_TRACK(B); t.SetStart(V(*a)); t.SetEnd(V(*b)); t.SetWidth(MM(w))
        t.SetLayer(B.GetLayerID(layer)); t.SetNet(net(n)); B.Add(t)

def via(x, y, n):
    v = pcbnew.PCB_VIA(B); v.SetPosition(V(x, y)); v.SetDrill(MM(0.3)); v.SetWidth(MM(0.6)); v.SetNet(net(n)); B.Add(v)

def cap(ref, x, y):
    fp = pcbnew.Cast_to_FOOTPRINT(B.FindFootprintByReference('C7').Duplicate())   # C7 ist 0805
    fp.SetReference(ref); fp.SetValue('10uF 50V X5R'); fp.SetPosition(V(x, y)); fp.SetOrientationDegrees(90)
    B.Add(fp)
    ps = sorted(fp.Pads(), key=lambda p: p.GetPosition().y)          # oberes Pad GND, unteres Pad an der PVDD-Leitung
    ps[0].SetNet(net('GND')); ps[1].SetNet(net('PVDD'))
    return [(p.GetNumber(), p.GetNetname(), round(p.GetPosition().x / 1e6, 3), round(p.GetPosition().y / 1e6, 3)) for p in ps]

print('C47', cap('C47', 125.9, 114.15))
print('C48', cap('C48', 139.0, 114.1))
track('F.Cu', [(125.9, 115.1), (125.9, 116.0)], 0.8, 'PVDD')
track('F.Cu', [(139.0, 115.05), (139.0, 116.0)], 0.8, 'PVDD')
track('F.Cu', [(125.9, 113.2), (124.6, 113.2)], 0.5, 'GND'); via(124.6, 113.2, 'GND')
track('F.Cu', [(139.0, 113.15), (139.0, 112.0)], 0.5, 'GND'); via(139.0, 112.0, 'GND')

# Lotpaste U1: alte Einzeloeffnung (Pad ohne Nummer, nur F.Paste) durch 4 Oeffnungen ersetzen
U1 = B.FindFootprintByReference('U1')
old = [p for p in U1.Pads() if p.GetNumber() == '' and p.GetLayerSet().Seq() and all(B.GetLayerName(l) == 'F.Paste' for l in p.GetLayerSet().Seq())]
assert len(old) == 1, old
o = old[0]; c = o.GetPosition()
for dx in (-1.0, 1.0):                 # Platinenkoordinaten: 2 Spalten 1,75 mm breit, 2 Reihen 1,35 mm hoch
    for dy in (-0.775, 0.775):
        p = pcbnew.PAD(U1)
        p.SetAttribute(o.GetAttribute()); p.SetShape(o.GetShape()); p.SetLayerSet(o.GetLayerSet())
        p.SetOrientation(o.GetOrientation())
        p.SetSize(V(1.35, 1.75))        # Padkoordinaten (Bauteil um -90 Grad gedreht)
        p.SetNumber('')
        U1.Add(p)
        p.SetPos0(V(dy, -dx)); p.SetDrawCoord()   # Bauteilkoordinaten: x_lokal = dy, y_lokal = -dx (Drehung -90 Grad)
U1.Remove(o)
paste = [p for p in U1.Pads() if p.GetNumber() == '' ]
print('Pastenoeffnungen U1:', [(round(p.GetPosition().x/1e6,3), round(p.GetPosition().y/1e6,3), round(p.GetBoundingBox().GetWidth()/1e6,2), round(p.GetBoundingBox().GetHeight()/1e6,2)) for p in paste])
pcbnew.SaveBoard(sys.argv[1], B)
