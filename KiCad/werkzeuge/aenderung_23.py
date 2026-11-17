#!/usr/bin/python3
# Einmalige Aenderung 23 (17.11.2026), nach Datenblatt TPS54308 (SLUSCV2B) Kap. 7.2.3.6.3 und Tabelle 7-2:
# R14 2 kOhm in Reihe zum Vorkopplungskondensator C28 (+5V -> R14 -> C28 -> FB).
# Dafuer laeuft die EN-Leitung zwischen U2 und R8 jetzt ueber zwei Durchkontaktierungen auf der Unterseite.
# Aufruf: python3 aenderung_23.py KiCad/RadioHAT.kicad_pcb   (nicht erneut ausfuehren)
import sys, pcbnew
B = pcbnew.LoadBoard(sys.argv[1]); MM = pcbnew.FromMM
V = lambda x, y: pcbnew.VECTOR2I(MM(x), MM(y))
def net(name):
    n = B.FindNet(name)
    if n is None:
        n = pcbnew.NETINFO_ITEM(B, name); B.Add(n)
    return n
TR = [t for t in B.Tracks()]; DEL = []
same = lambda a, b: abs(a.x - b.x) < 10000 and abs(a.y - b.y) < 10000
def remove_track(layer, a, b):
    for t in TR:
        if t.GetClass() == 'PCB_TRACK' and t.GetLayerName() == layer and \
           ((same(t.GetStart(), V(*a)) and same(t.GetEnd(), V(*b))) or (same(t.GetStart(), V(*b)) and same(t.GetEnd(), V(*a)))):
            DEL.append(t); return
    raise SystemExit(f'Leiterbahn nicht gefunden: {layer} {a} {b}')
def track(layer, pts, w, n):
    for a, b in zip(pts, pts[1:]):
        t = pcbnew.PCB_TRACK(B); t.SetStart(V(*a)); t.SetEnd(V(*b)); t.SetWidth(MM(w))
        t.SetLayer(B.GetLayerID(layer)); t.SetNet(net(n)); B.Add(t)
def via(x, y, n):
    v = pcbnew.PCB_VIA(B); v.SetPosition(V(x, y)); v.SetDrill(MM(0.3)); v.SetWidth(MM(0.6)); v.SetNet(net(n)); B.Add(v)

# alte EN-Fuehrung rechts an C28 vorbei entfernen
for a, b in [((108.88, 111.75), (109.38, 112.25)), ((109.38, 112.25), (109.38, 115.0)), ((109.38, 115.0), (109.12, 115.25)),
             ((109.12, 115.25), (109.12, 115.5)), ((109.12, 115.5), (108.12, 116.5)), ((108.12, 116.5), (108.12, 117.0))]:
    remove_track('F.Cu', a, b)
remove_track('F.Cu', (107.0, 114.38), (108.5, 114.38))     # +5V direkt an C28 entfaellt
for t in DEL: B.Remove(t)

# EN neu: unter dem BOOT-Pin vorbei zur Durchkontaktierung, Unterseite, Durchkontaktierung links neben R8
track('F.Cu', [(108.88, 111.75), (109.45, 111.75)], 0.25, 'EN'); via(109.45, 111.75, 'EN')
track('B.Cu', [(109.45, 111.75), (107.2, 117.0)], 0.25, 'EN'); via(107.2, 117.0, 'EN')
track('F.Cu', [(107.2, 117.0), (108.17, 117.0)], 0.25, 'EN')

# R14 2 kOhm waagerecht unter R6/C28
fp = pcbnew.Cast_to_FOOTPRINT(B.FindFootprintByReference('R7').Duplicate())
fp.SetReference('R14'); fp.SetValue('2k 1%'); fp.SetPosition(V(107.7, 115.75)); fp.SetOrientationDegrees(0)
B.Add(fp)
ps = sorted(fp.Pads(), key=lambda p: p.GetPosition().x)
ps[0].SetNet(net('+5V')); ps[1].SetNet(net('FB_FF'))
for p in B.FindFootprintByReference('C28').Pads():
    if p.GetNetname() == '+5V': p.SetNet(net('FB_FF'))
print('R14', [(p.GetNumber(), p.GetNetname(), round(p.GetPosition().x / 1e6, 3), round(p.GetPosition().y / 1e6, 3)) for p in ps])
track('F.Cu', [(106.12, 115.25), (ps[0].GetPosition().x / 1e6, 115.75)], 0.25, '+5V')
track('F.Cu', [(ps[1].GetPosition().x / 1e6, 115.75), (108.5, 114.38)], 0.25, 'FB_FF')
pcbnew.SaveBoard(sys.argv[1], B)
