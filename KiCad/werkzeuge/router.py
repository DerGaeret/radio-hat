# Einfacher A*-Wegsucher fuer eine Kupferlage mit Abstandsregeln (Raster 0,05 mm), danach Vereinfachung per Sichtlinie.
# Wird von aenderung_24.py benutzt. Hindernisse: ('c', (x, y), r) Kreis, ('s', (x1, y1, x2, y2), r) Strecke mit Abstand r,
# ('r', (x0, y0, x1, y1), r) Rechteck, um r vergroessert (Ecken rund). r gilt fuer die Mittellinie der neuen Leiterbahn.
# Der DRC in KiCad bleibt die eigentliche Pruefung; dieser Wegsucher rechnet eher zu vorsichtig.
import heapq, math, numpy as np, pcbnew
G = 0.05
def obstacles(B, layer, net, width, clr=0.2, extra=()):
    """Liste (Typ, Geometrie, Radius) aller fremden Objekte auf der Lage; Radius = halbe Breite + Abstand + halbe Leiterbahn."""
    L = B.GetLayerID(layer); half = width / 2; obs = []
    for t in B.Tracks():
        if t.GetNetname() == net: continue
        if t.GetClass() == 'PCB_VIA':
            p = t.GetPosition(); obs.append(('c', (p.x / 1e6, p.y / 1e6), t.GetWidth() / 2e6 + clr + half))
        elif t.GetLayer() == L:
            a, b = t.GetStart(), t.GetEnd()
            obs.append(('s', (a.x / 1e6, a.y / 1e6, b.x / 1e6, b.y / 1e6), t.GetWidth() / 2e6 + clr + half))
    for f in B.GetFootprints():
        for p in f.Pads():
            if p.GetNetname() == net and net: continue
            obs += pad_obstacle(p, L, clr + half)
    for o in extra: obs.append(o)
    return obs
def pad_obstacle(p, L, r):
    """Pad als Hindernis: Kreis, Langloch als Strecke, alles andere als umschliessendes Rechteck."""
    drill = p.GetDrillSize().x / 1e6
    bb = p.GetBoundingBox(); cx, cy = bb.GetCenter().x / 1e6, bb.GetCenter().y / 1e6
    w, h = bb.GetWidth() / 1e6, bb.GetHeight() / 1e6
    if not p.IsOnLayer(L):
        return [('c', (p.GetPosition().x / 1e6, p.GetPosition().y / 1e6), drill / 2 + 0.05 + r)] if drill > 0 else []   # Loch ohne Kupfer
    gerade = abs(p.GetOrientation().AsDegrees()) % 90 < 0.01
    if p.GetShape() == pcbnew.PAD_SHAPE_CIRCLE:
        return [('c', (cx, cy), w / 2 + r)]
    if p.GetShape() == pcbnew.PAD_SHAPE_OVAL and gerade:
        if w >= h: return [('s', (cx - (w - h) / 2, cy, cx + (w - h) / 2, cy), h / 2 + r)]
        return [('s', (cx, cy - (h - w) / 2, cx, cy + (h - w) / 2), w / 2 + r)]
    return [('r', (bb.GetLeft() / 1e6, bb.GetTop() / 1e6, bb.GetRight() / 1e6, bb.GetBottom() / 1e6), r)]
def dist_seg(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1; L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / L2))
    return math.hypot(px - x1 - t * dx, py - y1 - t * dy)
def seg_seg(a, b):
    return min(dist_seg(a[0], a[1], *b), dist_seg(a[2], a[3], *b), dist_seg(b[0], b[1], *a), dist_seg(b[2], b[3], *a)) if not _cross(a, b) else 0
def _cross(a, b):
    def o(p, q, r): return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    p1, p2, p3, p4 = (a[0], a[1]), (a[2], a[3]), (b[0], b[1]), (b[2], b[3])
    return (o(p1, p2, p3) * o(p1, p2, p4) < 0) and (o(p3, p4, p1) * o(p3, p4, p2) < 0)
def dist_pt_rect(x, y, g):
    return math.hypot(max(g[0] - x, 0, x - g[2]), max(g[1] - y, 0, y - g[3]))
def dist_seg_rect(s, g):
    """Abstand Strecke - achsparalleles Rechteck (0 bei Ueberschneidung)."""
    if dist_pt_rect(s[0], s[1], g) == 0 or dist_pt_rect(s[2], s[3], g) == 0: return 0
    ecken = ((g[0], g[1]), (g[2], g[1]), (g[2], g[3]), (g[0], g[3]))
    for k in range(4):
        if _cross(s, (*ecken[k], *ecken[(k + 1) % 4])): return 0
    return min([dist_pt_rect(s[0], s[1], g), dist_pt_rect(s[2], s[3], g)] + [dist_seg(x, y, *s) for x, y in ecken])
def seg_free(s, obs, edge):
    x0, y0, x1, y1 = edge
    for x, y in ((s[0], s[1]), (s[2], s[3])):
        if not (x0 <= x <= x1 and y0 <= y <= y1): return False
    for typ, g, r in obs:
        if typ == 'c':
            if dist_seg(g[0], g[1], *s) < r: return False
        elif typ == 'r':
            if dist_seg_rect(s, g) < r: return False
        else:
            if seg_seg(s, g) < r: return False
    return True
def route(obs, start, goal, edge, box):
    bx0, by0, bx1, by1 = box
    nx, ny = int((bx1 - bx0) / G) + 1, int((by1 - by0) / G) + 1
    free = np.ones((nx, ny), bool)
    xs = bx0 + np.arange(nx) * G; ys = by0 + np.arange(ny) * G
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    free &= (X >= edge[0]) & (X <= edge[2]) & (Y >= edge[1]) & (Y <= edge[3])
    for typ, g, r in obs:
        if typ == 'c':
            free &= (X - g[0]) ** 2 + (Y - g[1]) ** 2 >= (r + 0.03) ** 2
        elif typ == 'r':
            dx = np.maximum(np.maximum(g[0] - X, 0), X - g[2]); dy = np.maximum(np.maximum(g[1] - Y, 0), Y - g[3])
            free &= dx * dx + dy * dy >= (r + 0.03) ** 2
        else:
            x1, y1, x2, y2 = g; dx, dy = x2 - x1, y2 - y1; L2 = dx * dx + dy * dy or 1e-12
            t = np.clip(((X - x1) * dx + (Y - y1) * dy) / L2, 0, 1)
            free &= (X - x1 - t * dx) ** 2 + (Y - y1 - t * dy) ** 2 >= (r + 0.03) ** 2
    S = (int(round((start[0] - bx0) / G)), int(round((start[1] - by0) / G)))
    T = (int(round((goal[0] - bx0) / G)), int(round((goal[1] - by0) / G)))
    for P in (S, T):  # Endpunkte freiraeumen (gehoeren zum eigenen Netz)
        free[max(P[0]-3,0):P[0]+4, max(P[1]-3,0):P[1]+4] = True
    nb = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1), (1, 1, 1.4142), (1, -1, 1.4142), (-1, 1, 1.4142), (-1, -1, 1.4142)]
    h = lambda p: math.hypot(p[0] - T[0], p[1] - T[1])
    openq = [(h(S), 0.0, S, None)]; came = {}; gbest = {S: 0.0}
    while openq:
        f, g, p, d = heapq.heappop(openq)
        if p in came: continue
        came[p] = d
        if p == T: break
        for dx, dy, c in nb:
            q = (p[0] + dx, p[1] + dy)
            if not (0 <= q[0] < nx and 0 <= q[1] < ny) or not free[q]: continue
            ng = g + c + (0.3 if d is not None and d[1] != (dx, dy) else 0)
            if ng < gbest.get(q, 1e18):
                gbest[q] = ng; heapq.heappush(openq, (ng + h(q), ng, q, (p, (dx, dy))))
    if T not in came: return None
    path = [T]
    while came[path[-1]] is not None: path.append(came[path[-1]][0])
    path = path[::-1]
    pts = [(bx0 + i * G, by0 + j * G) for i, j in path]
    pts[0] = start; pts[-1] = goal
    # Sichtlinien-Vereinfachung
    out = [pts[0]]; i = 0
    while i < len(pts) - 1:
        j = len(pts) - 1
        while j > i + 1 and not seg_free((pts[i][0], pts[i][1], pts[j][0], pts[j][1]), obs, edge): j -= 1
        out.append(pts[j]); i = j
    # Zwischenpunkte weglassen, solange die direkte Verbindung frei ist
    changed = True
    while changed:
        changed = False
        for i in range(1, len(out) - 1):
            if seg_free((out[i - 1][0], out[i - 1][1], out[i + 1][0], out[i + 1][1]), obs, edge):
                del out[i]; changed = True; break
    return [(round(x, 3), round(y, 3)) for x, y in out]
