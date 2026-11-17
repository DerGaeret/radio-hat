#!/usr/bin/python3
# Einmalige Aenderung 28 (17.11.2026): Alle Leiterbahnen nur noch waagerecht, senkrecht oder unter 45 Grad.
# Die aus den Gerber-Daten zurueckgewonnenen Bahnen enthielten Boegen aus vielen kurzen Stuecken und schraege Stuecke mit
# beliebigem Winkel. Ablauf:
#  1. Kurze Stuecke in einer Linie (gleiches Netz, gleiche Lage, gleiche Breite, kein Via, keine Abzweigung) zusammenfassen.
#  2. Jede Folge schraeger Stuecke zwischen zwei festen Punkten (Abzweigung, Via, Pad, Ende, gerades Stueck) durch einen Zug
#     aus 2 bis 3 Stuecken mit 0/45/90 Grad ersetzen. Unter den Varianten, die die Abstaende einhalten, gewinnt die, die am
#     wenigsten vom bisherigen Verlauf abweicht (Hausdorff-Abstand). Breite bleibt; bei wechselnder Breite gilt die groesste.
# Danach von Hand: Revisionsangabe im Bestueckungsdruck "Rev. 1.0" -> "Rev. 1.1  11/2026".
# Ausgangsstand: Platine nach Aenderung 27. Danach DRC 0 Verstoesse, 0 unverbundene Pads.
# Aufruf: python3 aenderung_28.py KiCad/RadioHAT.kicad_pcb   (nicht erneut ausfuehren)
import math, os, sys, collections, pcbnew
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import router
B = pcbnew.LoadBoard(sys.argv[1]); MM = pcbnew.FromMM
CLR = 0.1995                                      # Mindestabstand 0,2 mm (Pads als umschliessendes Rechteck; der DRC prueft genau)
K = lambda p: (round(p[0], 3), round(p[1], 3))
mm = lambda v: (v.x / 1e6, v.y / 1e6)

# ---- Bestand einlesen (eigene Liste, damit nicht nach dem Entfernen ueber B.Tracks() iteriert wird)
OLD = [t for t in B.Tracks()]
segs = []   # dict: a, b, w, layer, net
vias = []   # (x, y, r, net)
for t in OLD:
    if t.GetClass() == 'PCB_VIA':
        x, y = mm(t.GetPosition()); vias.append((x, y, t.GetWidth() / 2e6, t.GetNetname()))
    elif t.GetClass() == 'PCB_TRACK':
        segs.append(dict(a=mm(t.GetStart()), b=mm(t.GetEnd()), w=t.GetWidth() / 1e6, layer=t.GetLayerName(), net=t.GetNetname()))
    else: raise SystemExit('unerwartet: ' + t.GetClass())
n0 = len(segs)
viapos = {K(v[:2]) for v in vias}
padpos = collections.defaultdict(set)              # Pad-Mittelpunkte je Lage (dort nichts zusammenfassen/verschieben)
for f in B.GetFootprints():
    for p in f.Pads():
        for L in ('F.Cu', 'In1.Cu', 'In2.Cu', 'B.Cu'):
            if p.IsOnLayer(B.GetLayerID(L)): padpos[L].add(K(mm(p.GetPosition())))
def odd(s):
    dx, dy = s['b'][0] - s['a'][0], s['b'][1] - s['a'][1]
    if math.hypot(dx, dy) < 1e-4: return False
    a = math.degrees(math.atan2(dy, dx)) % 45
    return min(a, 45 - a) > 0.3
def ang(s):
    return math.atan2(s['b'][1] - s['a'][1], s['b'][0] - s['a'][0])
def adjacency(segs):
    adj = collections.defaultdict(list)
    for i, s in enumerate(segs):
        adj[(s['net'], s['layer'], K(s['a']))].append(i); adj[(s['net'], s['layer'], K(s['b']))].append(i)
    return adj
def fixed(net, layer, k, adj):
    return len(adj[(net, layer, k)]) != 2 or k in viapos or k in padpos[layer]

# ---- 1. Gerade Folgen zusammenfassen (auch nach Schritt 2 noch einmal)
def merge(segs):
    changed = True
    while changed:
        changed = False; adj = adjacency(segs)
        for key, ids in adj.items():
            net, layer, k = key
            if len(ids) != 2 or k in viapos or k in padpos[layer]: continue
            i, j = ids; s, t = segs[i], segs[j]
            if s is None or t is None or abs(s['w'] - t['w']) > 1e-6: continue
            far_s = s['a'] if K(s['b']) == k else s['b']; far_t = t['a'] if K(t['b']) == k else t['b']
            d1 = math.atan2(k[1] - far_s[1], k[0] - far_s[0]); d2 = math.atan2(far_t[1] - k[1], far_t[0] - k[0])
            if abs((d1 - d2 + math.pi) % (2 * math.pi) - math.pi) > math.radians(0.3): continue
            segs[i] = dict(s, a=far_s, b=far_t); segs[j] = None; changed = True
            segs = [x for x in segs if x is not None]; break
    return segs
segs = merge(segs)
n1 = len(segs)

# ---- 2. Schraege Folgen ersetzen
extra = []
for f in B.GetFootprints():
    if f.GetReference() in ('H1', 'H2', 'H3', 'H4'):
        x, y = mm(f.GetPosition()); extra.append((x, y, 3.0))         # Sperrflaechen 6 mm
eb = B.GetBoardEdgesBoundingBox(); EDGE = (eb.GetLeft() / 1e6, eb.GetTop() / 1e6, eb.GetRight() / 1e6, eb.GetBottom() / 1e6)
pads_all = [p for f in B.GetFootprints() for p in f.Pads()]
def obstacles(net, layer, w, skip):
    L = B.GetLayerID(layer); half = w / 2; obs = []
    for i, s in enumerate(segs):
        if s is None or i in skip or s['layer'] != layer or s['net'] == net: continue
        obs.append(('s', (*s['a'], *s['b']), s['w'] / 2 + CLR + half))
    for x, y, r, n in vias:
        if n != net: obs.append(('c', (x, y), r + CLR + half))
    for p in pads_all:
        if p.GetNetname() == net and net: continue
        obs += router.pad_obstacle(p, L, CLR + half)
    for x, y, r in extra: obs.append(('c', (x, y), r + half))
    return obs
def candidates(P, Q):
    dx, dy = Q[0] - P[0], Q[1] - P[1]; ax, ay = abs(dx), abs(dy); sx, sy = math.copysign(1, dx), math.copysign(1, dy)
    m = min(ax, ay); diag = (sx * m, sy * m)
    st = (sx * (ax - m), 0) if ax > ay else (0, sy * (ay - m))
    out = []
    for t in [0, 1] + [k / 10 for k in range(1, 10)]:            # gerade t, schraeg, gerade (1-t)
        a = (P[0] + st[0] * t, P[1] + st[1] * t); b = (a[0] + diag[0], a[1] + diag[1])
        out.append([P, a, b, Q])
    for t in [k / 10 for k in range(1, 10)]:                      # schraeg t, gerade, schraeg (1-t)
        a = (P[0] + diag[0] * t, P[1] + diag[1] * t); b = (a[0] + st[0], a[1] + st[1])
        out.append([P, a, b, Q])
    res = []
    for c in out:
        c2 = [c[0]]
        for p in c[1:]:
            if math.hypot(p[0] - c2[-1][0], p[1] - c2[-1][1]) > 1e-4: c2.append(p)
        res.append(c2)
    return res
def hausdorff(A, Bp):
    def sample(pl):
        pts = []
        for a, b in zip(pl, pl[1:]):
            n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 0.05))
            pts += [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(n + 1)]
        return pts
    def d(pts, pl): return max(min(router.dist_seg(x, y, *a, *b) for a, b in zip(pl, pl[1:])) for x, y in pts)
    return max(d(sample(A), Bp), d(sample(Bp), A))
fails = []; done = 0; new_total = 0; devs = []
while True:
    adj = adjacency(segs)
    run = None
    for i, s in enumerate(segs):
        if s is None or not odd(s): continue
        # Folge in beide Richtungen ueber nicht feste Knoten mit schraegen Nachbarn erweitern
        ids = [i]; ends = []
        for start in (s['a'], s['b']):
            cur, prev = K(start), i
            while not fixed(s['net'], s['layer'], cur, adj):
                nxt = [j for j in adj[(s['net'], s['layer'], cur)] if j != prev][0]
                if not odd(segs[nxt]) or nxt in ids: break
                ids.append(nxt); t = segs[nxt]; cur = K(t['b']) if K(t['a']) == cur else K(t['a']); prev = nxt
            ends.append(cur)
        if (s['net'], s['layer'], tuple(ends)) in [f[:3] for f in fails]: continue
        run = (ids, ends); break
    if run is None: break
    ids, (Pk, Qk) = run; s = segs[ids[0]]
    # Polylinie des alten Verlaufs von P nach Q
    chain = []; cur = Pk; rest = set(ids)
    pl = [Pk]
    while rest:
        j = [j for j in rest if K(segs[j]['a']) == cur or K(segs[j]['b']) == cur][0]; rest.discard(j)
        t = segs[j]; cur = K(t['b']) if K(t['a']) == cur else K(t['a']); pl.append(cur)
    w = max(segs[j]['w'] for j in ids)
    obs = obstacles(s['net'], s['layer'], w, set(ids))
    def solve(P, Q, pl):
        best = None
        for c in candidates(P, Q):
            if all(router.seg_free((a[0], a[1], b[0], b[1]), obs, EDGE) for a, b in zip(c, c[1:])):
                h = hausdorff(c, pl)
                if best is None or h < best[0] - 1e-6 or (abs(h - best[0]) < 1e-6 and len(c) < len(best[1])): best = (h, c)
        return best
    best = solve(Pk, Qk, pl)
    if best is None and len(pl) > 2:            # ganze Folge geht nicht: jedes Stueck einzeln, Zwischenpunkte bleiben
        parts = [solve(a, b, [a, b]) for a, b in zip(pl, pl[1:])]
        if all(parts): best = (0, [pl[0]] + [p for h, c in parts for p in c[1:]])
    if best is None:                            # Folge um das anschliessende gerade Stueck verlaengern (bis zum naechsten festen Punkt)
        for side in (1, 0, 2):
            P2, Q2, ids2, pl2 = Pk, Qk, list(ids), list(pl)
            for end in ((0,) if side == 0 else (1,) if side == 1 else (0, 1)):
                cur = P2 if end == 0 else Q2
                nb = [j for j in adj[(s['net'], s['layer'], cur)] if j not in ids2]
                if fixed(s['net'], s['layer'], cur, adj) or len(nb) != 1: break
                t = segs[nb[0]]; far = K(t['b']) if K(t['a']) == cur else K(t['a']); ids2.append(nb[0])
                if end == 0: P2 = far; pl2.insert(0, far)
                else: Q2 = far; pl2.append(far)
            else:
                obs = obstacles(s['net'], s['layer'], max(segs[j]['w'] for j in ids2), set(ids2))
                best = solve(P2, Q2, pl2)
                if best: ids = ids2; w = max(segs[j]['w'] for j in ids2); break
    if best is None and os.environ.get('DEBUG'):
        print('DBG', s['net'], s['layer'], w, [(round(x-100,3), round(150-y,3)) for x, y in pl])
        for c in candidates(Pk, Qk)[:2]:
            for a, b in zip(c, c[1:]):
                for o in obs:
                    if not router.seg_free((a[0], a[1], b[0], b[1]), [o], EDGE): print('   block', o[0], [round(v,2) for v in o[1]], round(o[2],2)); break
    if best is None:                            # verjuengte Folge (Breite wechselt): mit der kleinsten Breite der Folge
        w = min(segs[j]['w'] for j in ids); obs = obstacles(s['net'], s['layer'], w, set(ids)); best = solve(Pk, Qk, pl)
    if best is None:
        fails.append((s['net'], s['layer'], (Pk, Qk), w, pl)); continue
    for j in ids: segs[j] = None
    for a, b in zip(best[1], best[1][1:]): segs.append(dict(a=a, b=b, w=w, layer=s['layer'], net=s['net'])); new_total += 1
    segs = [x for x in segs if x is not None]; done += 1; devs.append((round(best[0], 2), s['net'], s['layer']))
    # die Pruefung "nicht erneut" haengt an den Endpunkten; neue Stuecke sind nie schraeg
print(f'Stuecke: {n0} -> {n1} nach Zusammenfassen; {done} schraege Folgen ersetzt; nicht ersetzbar: {len(fails)}')
for f in fails: print('  FEHLT', f[0], f[1], [tuple(round(v - o, 3) for v, o in zip(p, (100, 0))) for p in f[2]], f[3])
segs = merge(segs); print('nach erneutem Zusammenfassen:', len(segs), 'Stuecke; groesste Abweichungen vom alten Verlauf (mm):', sorted(devs, reverse=True)[:6])
left = sum(1 for s in segs if odd(s)); print('schraeg uebrig:', left)
if fails or left: raise SystemExit('nicht gespeichert')

# ---- Platine neu schreiben: alle alten Leiterbahnen raus, neue rein (Vias bleiben)
for t in OLD:
    if t.GetClass() == 'PCB_TRACK': B.Remove(t)
for s in segs:
    t = pcbnew.PCB_TRACK(B); t.SetStart(pcbnew.VECTOR2I(MM(s['a'][0]), MM(s['a'][1])))
    t.SetEnd(pcbnew.VECTOR2I(MM(s['b'][0]), MM(s['b'][1]))); t.SetWidth(MM(s['w']))
    t.SetLayer(B.GetLayerID(s['layer'])); t.SetNet(B.FindNet(s['net'])); B.Add(t)
pcbnew.SaveBoard(sys.argv[1], B)
print('Aenderung 28 eingebaut,', len(segs), 'Leiterbahnstuecke')
