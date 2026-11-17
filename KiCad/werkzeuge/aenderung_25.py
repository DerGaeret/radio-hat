#!/usr/bin/python3
# Einmalige Aenderung 25 (17.11.2026): Bestellreife fuer ein verkaufbares Geraet.
# 1. Befestigungsloecher H1-H4: Sperrflaechen 6 mm Durchmesser (wie am Pi) auf allen Kupferlagen, darin keine Leiterbahn
#    und kein Via. GPIO11 lief an H3 1,97 mm vom Lochmittelpunkt (unter jedem Schraubenkopf) und laeuft jetzt ueber die
#    Unterseite innen am Loch vorbei; an H1 ist GPIO11 und an H2 VENC (3,3 V vom Pi) um 0,15 mm abgerueckt; das GND-Via an
#    H1 ist verschoben.
# 2. Bedrahtete Massepads (J1, J4, S1-S6, E1-E3) mit Waermefallen, damit sie sich von Hand loeten lassen. Die 24 Vias im
#    Kuehlpad von U1 bleiben voll angebunden (TI, Kap. 9.1.3.2.1).
# 3. Drei Passbohrungen 1,152 mm ohne Kupfer (TH1-TH3), die JLCPCB fuer die Economic-Bestueckung verlangt. Ohne sie bohrt
#    JLCPCB eigene Loecher an Stellen, die es selbst waehlt.
# 4. Bestueckungsdruck: Revisionsangabe unter "Radio HAT".
# 5. Bestueckungsdruck: alle Linien mindestens 0,16 mm breit (vorher 0,12 mm), Texte "+20V" und "EIN/AUS" 1,0 mm hoch.
# Dazu gehoert KiCad/RadioHAT.kicad_dru: Auf der Unterseite reicht an S1-S3 Pin 2 und J1 Pin 14/30 wegen der Leitungen
# nur ein Steg der Waermefalle an die Masseflaeche; die Pads haengen zusaetzlich voll an F.Cu, In1 und In2.
# Ausgangsstand: Platine nach Aenderung 24 (Git 8186a74). Danach DRC 0 Verstoesse, 0 unverbundene Pads.
# Aufruf: python3 aenderung_25.py KiCad/RadioHAT.kicad_pcb   (nicht erneut ausfuehren)
import math, sys, pcbnew
B = pcbnew.LoadBoard(sys.argv[1]); MM = pcbnew.FromMM
X0, Y0 = 100, 150                                       # Platinenursprung links unten (Bohr-/Platzierungsursprung)
V = lambda x, y: pcbnew.VECTOR2I(MM(X0 + x), MM(Y0 - y))  # Koordinaten wie im Pruefbericht: x nach rechts, y nach oben
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

# ---- 1a. GPIO11 an H3 (3,5/12,5): bisher Oberseite x = 1,4 am Rand entlang, jetzt Unterseite innen vorbei
rm_track('F.Cu', (1.4, 23.27), (1.4, 6.0)); rm_track('F.Cu', (1.4, 6.0), (5.0, 2.38)); rm_track('F.Cu', (5.0, 2.38), (20.38, 2.38))
track('F.Cu', [(1.4, 23.27), (1.4, 19.6)], 0.25, 'GPIO11'); via(1.4, 19.6, 'GPIO11')
track('B.Cu', [(1.4, 19.6), (7.0, 14.0), (7.0, 2.88), (7.5, 2.38)], 0.25, 'GPIO11'); via(7.5, 2.38, 'GPIO11')
track('F.Cu', [(7.5, 2.38), (20.38, 2.38)], 0.25, 'GPIO11')
# ---- 1b. GPIO11 an H1 (3,5/61,5): senkrechtes Stueck von x = 6,5 auf 6,65
for a, b in [((7.125, 62.0), (6.625, 61.5)), ((6.625, 61.5), (6.625, 61.375)), ((6.625, 61.375), (6.5, 61.25)),
             ((6.5, 61.25), (6.5, 60.125)), ((6.5, 60.125), (6.125, 59.75))]:
    rm_track('F.Cu', a, b)
track('F.Cu', [(7.125, 62.0), (6.65, 61.525), (6.65, 60.275), (6.125, 59.75)], 0.25, 'GPIO11')
rm_via(3.0, 59.0); via(2.0, 57.9, 'GND')                  # GND-Via lag 2,25 mm vom Loch
# ---- 1c. VENC an H2 (61,5/61,5): senkrechtes Stueck von x = 58,5 auf 58,35
for a, b in [((57.125, 62.75), (58.375, 61.5)), ((58.375, 61.5), (58.375, 61.375)), ((58.375, 61.375), (58.5, 61.25)),
             ((58.5, 61.25), (58.5, 59.25)), ((58.5, 59.25), (59.625, 58.125))]:
    rm_track('F.Cu', a, b)
track('F.Cu', [(57.125, 62.75), (58.35, 61.525), (58.35, 59.4), (59.625, 58.125)], 0.25, 'VENC')
for t in DEL: B.Remove(t)
# ---- 1d. Sperrflaechen: Kreis 6 mm um jedes Befestigungsloch, alle Kupferlagen, keine Leiterbahnen und Vias
cu = pcbnew.LSET(); [cu.AddLayer(l) for l in (pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.B_Cu)]
for name, (hx, hy) in (('H1', (3.5, 61.5)), ('H2', (61.5, 61.5)), ('H3', (3.5, 12.5)), ('H4', (61.5, 12.5))):
    z = pcbnew.ZONE(B); z.SetIsRuleArea(True); z.SetLayerSet(cu); z.SetZoneName('Sperrflaeche ' + name)
    z.SetDoNotAllowTracks(True); z.SetDoNotAllowVias(True); z.SetDoNotAllowCopperPour(False)
    z.SetDoNotAllowPads(False); z.SetDoNotAllowFootprints(False)
    z.Outline().NewOutline()
    for k in range(48):
        a = 2 * math.pi * k / 48; z.Outline().Append(V(hx + 3.0 * math.cos(a), hy + 3.0 * math.sin(a)))
    B.Add(z)
# ---- 2. Waermefallen fuer bedrahtete Pads in allen Masseflaechen, Kuehlpad-Vias von U1 bleiben voll angebunden
for z in B.Zones():
    if not z.GetIsRuleArea() and z.GetNetname() == 'GND': z.SetPadConnection(pcbnew.ZONE_CONNECTION_THT_THERMAL)
u1 = B.FindFootprintByReference('U1')
for p in u1.Pads():
    if p.GetNumber() == '29' and p.GetDrillSize().x > 0: p.SetZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
# ---- 3. Passbohrungen fuer die Bestueckung bei JLCPCB: 1,152 mm ohne Kupfer, Loetstopp 0,148 mm groesser
for ref, (x, y) in (('TH1', (2.6, 6.4)), ('TH2', (62.9, 17.2)), ('TH3', (63.0, 57.0))):
    fp = pcbnew.FOOTPRINT(B); fp.SetFPIDAsString('Passbohrung_JLCPCB_1.152mm'); fp.SetReference(ref)
    fp.SetValue('Passbohrung 1,152 mm'); fp.SetPosition(V(x, y))
    fp.SetAttributes(pcbnew.FP_EXCLUDE_FROM_POS_FILES | pcbnew.FP_EXCLUDE_FROM_BOM | pcbnew.FP_BOARD_ONLY)
    B.Add(fp)
    p = pcbnew.PAD(fp); p.SetAttribute(pcbnew.PAD_ATTRIB_NPTH); p.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
    p.SetSize(pcbnew.VECTOR2I(MM(1.152), MM(1.152))); p.SetDrillSize(pcbnew.VECTOR2I(MM(1.152), MM(1.152)))
    p.SetLayerSet(pcbnew.PAD.UnplatedHoleMask()); p.SetLocalSolderMaskMargin(MM(0.148)); p.SetNumber('')
    fp.Add(p); p.SetPos0(pcbnew.VECTOR2I(0, 0)); p.SetDrawCoord()
    fp.Reference().SetLayer(B.GetLayerID('F.Fab')); fp.Value().SetVisible(False)
# ---- 4. Revisionsangabe im Bestueckungsdruck
t = pcbnew.PCB_TEXT(B); t.SetText('Rev. 1.0  11/2026'); t.SetLayer(B.GetLayerID('F.Silkscreen'))
t.SetTextSize(pcbnew.VECTOR2I(MM(1.0), MM(1.0))); t.SetPosition(V(34.6, 12.9)); B.Add(t)
# ---- 5. Bestueckungsdruck: Linien mindestens 0,16 mm (JLCPCB: 0,153 mm), Texte 1,0 mm hoch und 0,16 mm stark
for d in list(B.GetDrawings()):
    if d.GetLayerName() not in ('F.Silkscreen', 'B.Silkscreen'): continue
    if d.GetClass() == 'PCB_SHAPE' and 0 < d.GetWidth() < MM(0.16): d.SetWidth(MM(0.16))
    elif d.GetClass() == 'PCB_TEXT':
        if d.GetTextHeight() < MM(1.0): d.SetTextSize(pcbnew.VECTOR2I(MM(1.0), MM(1.0)))
        d.SetTextThickness(MM(0.16))
        if d.GetText() == '+20V': d.SetPosition(d.GetPosition() + pcbnew.VECTOR2I(0, MM(-0.2)))  # 0,2 mm hoeher, sonst beruehrt er J4
pcbnew.SaveBoard(sys.argv[1], B)
print('Aenderung 25 eingebaut:', len(DEL), 'Leiterbahnen/Vias entfernt')
