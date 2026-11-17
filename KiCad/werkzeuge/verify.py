#!/usr/bin/python3
# Messwerte fuer den Pruefbericht: Breiten, Abstaende, Lagen, Netzliste
# Aufruf: python3 verify.py Platine.kicad_pcb [Vergleichsplatine.kicad_pcb]   (braucht pcbnew und shapely)
import sys, math, collections, pcbnew
from shapely.geometry import LineString, box, Point
b = pcbnew.LoadBoard(sys.argv[1]); X0, Y0 = 100, 150
P = lambda v: (v.x / 1e6 - X0, Y0 - v.y / 1e6)
pads = {(f.GetReference(), p.GetNumber()): p for f in b.GetFootprints() for p in f.Pads()}
def pbox(p):
    bb = p.GetBoundingBox(); a, c = P(bb.GetOrigin()), P(bb.GetEnd()); return box(min(a[0], c[0]), min(a[1], c[1]), max(a[0], c[0]), max(a[1], c[1]))
trk = [t for t in b.Tracks() if t.GetClass() == 'PCB_TRACK']
print('== Ausgaenge: Abschnitte < 0,76 mm (Abstand vom Pin-Pad) und Laenge je Lagenzahl')
PIN = {'OUTB+': '17', 'OUTB-': '20', 'OUTA-': '23', 'OUTA+': '26'}
for n, pin in PIN.items():
    pb = pbox(pads[('U1', pin)]); narrow = []
    for t in trk:
        if t.GetNetname() == n and t.GetWidth() < 0.76e6 - 1:
            a_, b_ = P(t.GetStart()), P(t.GetEnd()); d_ = max(pb.distance(Point(a_)), pb.distance(Point(b_))); narrow.append((round(d_, 2), round(t.GetWidth() / 1e6, 2), t.GetLayerName(), tuple(round(v, 2) for v in a_ + b_)))
    narrow = [x for x in narrow if x[0] > 0]
    tot = collections.Counter()
    for t in trk:
        if t.GetNetname() == n: tot[t.GetLayerName()] += t.GetLength() / 1e6
    print(f'  {n}: schmal (max. Abstand vom Pad mm, Breite, Lage):', sorted(set(narrow)), ' Laengen:', {k: round(v, 1) for k, v in tot.items()})
print('== Abstand Kondensator-Pad zu Pin-Pad (Kante zu Kante, mm)')
for c, pin in (('C8', '2'), ('C9', '13'), ('C10', '4'), ('C11', '18'), ('C12', '21'), ('C13', '22'), ('C14', '25')):
    cp = [p for (r, _), p in pads.items() if r == c and p.GetNetname() == pads[('U1', pin)].GetNetname()][0]
    print(f'  {c} -> U1.{pin} ({cp.GetNetname()}): {pbox(cp).distance(pbox(pads[("U1", pin)])):.2f}')
for c, pin in (('C11', '17'), ('C12', '20'), ('C13', '23'), ('C14', '26')):
    cp = [p for (r, _), p in pads.items() if r == c and p.GetNetname() == pads[('U1', pin)].GetNetname()][0]
    print(f'  {c} OUT-Pad -> U1.{pin}: {pbox(cp).distance(pbox(pads[("U1", pin)])):.2f}')
print('== +3V3 kleinste Breite je Lage:', {l: round(min(t.GetWidth() for t in trk if t.GetNetname() == '+3V3' and t.GetLayerName() == l) / 1e6, 2) for l in ('F.Cu', 'B.Cu')})
for z in b.Zones():
    if z.GetLayerName().startswith('In'): print('==', z.GetLayerName(), 'Stuecke', z.GetFilledPolysList(z.GetLayer()).OutlineCount(), 'Flaeche', round(z.GetFilledArea() / 1e12))
print('== Vias', sum(1 for t in b.Tracks() if t.GetClass() == 'PCB_VIA'))
if len(sys.argv) > 2:
    o = pcbnew.LoadBoard(sys.argv[2]); on = {(f.GetReference(), p.GetNumber(), round(p.GetPosition().x, -3) if False else 0): p.GetNetname() for f in o.GetFootprints() for p in f.Pads()}
    nn = collections.Counter((f.GetReference(), p.GetNumber(), p.GetNetname()) for f in b.GetFootprints() for p in f.Pads())
    oo = collections.Counter((f.GetReference(), p.GetNumber(), p.GetNetname()) for f in o.GetFootprints() for p in f.Pads())
    print('== Netzliste gleich:', nn == oo, sum(nn.values()), 'Pads', (nn - oo) or '', (oo - nn) or '')
