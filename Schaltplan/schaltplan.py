"""Schaltplan Retro-Radio (Raspberry Pi 4B + DigiAMP+). Erzeugt schaltplan.pdf und blatt1/2.png.
Aufruf: python3 schaltplan.py   (braucht: pip install schemdraw matplotlib)"""
import schemdraw
import schemdraw.elements as elm
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

schemdraw.use('matplotlib')
FS = 9

def ic(d, xy, titel, links=(), rechts=(), unten=(), oben=(), w=4, h=None, ps=0.8):
    # schemdraw zählt Pins links/rechts von unten nach oben; hier wird die erste Angabe oben gezeichnet
    pins = [elm.IcPin(name=n, side='left', anchorname=a) for n, a in reversed(links)]
    pins += [elm.IcPin(name=n, side='right', anchorname=a) for n, a in reversed(rechts)]
    pins += [elm.IcPin(name=n, side='bottom', anchorname=a) for n, a in unten]
    pins += [elm.IcPin(name=n, side='top', anchorname=a) for n, a in oben]
    n = max(len(links), len(rechts), 1)
    if h is None:
        h = n * ps + 0.8
    e = d.add(elm.Ic(pins=pins, size=(w, h), pinspacing=ps, edgepadW=0.6, edgepadH=0.5,
                     fontsize=FS, lblsize=FS).theta(0).at(xy).anchor('center'))
    d.add(elm.Label().at((xy[0], xy[1] + h / 2 + 0.25)).label(titel, fontsize=FS, valign='bottom'))
    return e

def tag(d, at, text, richtung='right', l=0.8):
    """Netzname: kurze Leitung, offener Punkt, Text dahinter."""
    th = {'right': 0, 'left': 180, 'up': 90, 'down': -90}[richtung]
    d.add(elm.Line().at(at).theta(th).length(l))
    end = d.here
    d.add(elm.Dot(open=True).at(end))
    ha, va, dx, dy = {'right': ('left', 'center', 0.25, 0), 'left': ('right', 'center', -0.25, 0),
                      'up': ('center', 'bottom', 0, 0.25), 'down': ('center', 'top', 0, -0.25)}[richtung]
    d.add(elm.Label().at((end[0] + dx, end[1] + dy)).label(text, fontsize=FS, halign=ha, valign=va, color='navy'))

def gnd(d, at, l=0.6):
    d.add(elm.Line().at(at).down().length(l))
    d.add(elm.Ground())

def titel(d, xy, text, sub):
    d.add(elm.Label().at(xy).label(text, fontsize=14, halign='left'))
    d.add(elm.Label().at((xy[0], xy[1] - 0.8)).label(sub, fontsize=FS, halign='left'))

# ---------------------------------------------------------------- Blatt 1
def blatt1():
    d = schemdraw.Drawing(show=False, unit=2)
    titel(d, (0, 9), 'Blatt 1: Stromversorgung, Soft-Off, Verstärker, LED-Ansteuerung',
          'Retro-Radio, Stand 18.11.2026, ungetestet. Bauteile auf der Steuerplatine (Lochraster 70 × 50) mit * markiert.')

    # Netzteil und Einbaubuchse
    nt = ic(d, (1, 5), 'Netzteil 19 V / 4,74 A\n(Mean Well GST90A19-P1M)', rechts=[('+', 'P'), ('−', 'M')], w=3)
    j1 = ic(d, (6, 5), 'J1 Einbaubuchse 5,5 × 2,5\nDelock 90188 (Rückwand)', links=[('Mitte', 'P1'), ('Hülse', 'M1')],
            rechts=[('+', 'P2'), ('−', 'M2')], w=2.6)
    d.add(elm.Wire('-').at(nt.P).to(j1.P1).label('Hohlstecker', fontsize=7))
    d.add(elm.Wire('-').at(nt.M).to(j1.M1))

    # Pololu Schaltmodul
    q = ic(d, (13, 5), '*Q1 Pololu Big MOSFET\nSlide Switch HP (#2815)\nBordschalter auf OFF',
           links=[('VIN', 'VIN'), ('GND', 'G1')], rechts=[('VOUT', 'VOUT'), ('GND', 'G2')],
           unten=[('SW', 'SW'), ('ON', 'ON')], w=4.4)
    d.add(elm.Wire('-').at(j1.P2).to(q.VIN).label('X1 EIN +', fontsize=7))
    d.add(elm.Wire('-').at(j1.M2).to(q.G1))
    d.add(elm.Line().at(q.G1).left().length(0.01))
    gnd(d, j1.M2, 1.2)
    d.add(elm.Dot().at(j1.M2))

    # 19-V-Schiene
    d.add(elm.Line().at(q.VOUT).right().length(2))
    p19 = d.here
    d.add(elm.Dot())
    tag(d, p19, '+19V_SW', 'up', 0.8)
    gnd(d, q.G2, 0.6)

    # DigiAMP+
    amp = ic(d, (24, 6), 'Raspberry Pi DigiAMP+ (TAS5756M)\nsteckt auf dem Pi, liefert 5,1 V / 2,5 A\nüber den GPIO-Stecker an den Pi',
             links=[('DC +', 'DCP'), ('DC −', 'DCM')],
             rechts=[('LEFT +', 'LP'), ('LEFT −', 'LM'), ('RIGHT +', 'RP'), ('RIGHT −', 'RM')], w=6)
    d.add(elm.Wire('-|').at(p19).to(amp.DCP).label('X2 VERST → Hohlstecker\n5,5 × 2,5, 0,75 mm²', fontsize=7, loc='bottom'))
    gnd(d, amp.DCM, 0.6)
    for a, b, n, dx in ((amp.LP, amp.LM, 'LS links 8 Ω', 1.5), (amp.RP, amp.RM, 'LS rechts 8 Ω', 4.0)):
        sp = d.add(elm.Speaker().at((a[0] + dx, a[1])).right().label(n, fontsize=8, loc='right'))
        d.add(elm.Wire('-').at(a).to(sp.in1))
        d.add(elm.Wire('-|').at(b).to(sp.in2))
    d.add(elm.Label().at((27.5, 0.6)).label('Lautsprecher Sharp VSP0010PBS78A, beide Klemmen\nführen Signal (Brücke): nie mit Masse verbinden', fontsize=7, halign='left'))

    # A/E-Erkennung
    d.add(elm.Line().at(q.SW).down().length(1.4))
    d.add(elm.Schottky().down().label('*D1 BAT85', fontsize=8, loc='bottom'))
    x = d.here
    d.add(elm.Dot())
    d.add(elm.Line().at(x).left().length(2.5))
    d.add(elm.Switch().down().label('A/E (Original RFT)\nX3, ~0,4 mA', fontsize=8, loc='bottom'))
    d.add(elm.Ground())
    d.add(elm.Line().at(x).right().length(1.2))
    d.add(elm.Schottky().right().reverse().label('*D2 BAT85', fontsize=8))
    tag(d, d.here, 'GPIO10 (Pin 19)', 'right', 0.4)
    d.add(elm.Line().at(q.ON).down().length(1.0))
    tag(d, d.here, 'GPIO9 (Pin 21)', 'right', 1.0)
    d.add(elm.Label().at((9, -5.6)).label(
        'A/E zu: SW über D1 auf GND → Q1 an. Pi hält über GPIO9 → ON (high = an).\n'
        'A/E auf: GPIO10 high (Pull-up im Pi) → gpio-shutdown; am Ende GPIO9 low (gpio-poweroff) → Q1 aus.\n'
        'D2 sperrt die ~19 V an X, solange der Pi aus ist.', fontsize=7, halign='left'))

    # 5-V-Wandler
    bk = ic(d, (13, -9), '*U1 Pololu D36V28F5, 5 V / 3,2 A\n(EN und PG frei)', links=[('VIN', 'VIN'), ('GND', 'G')],
            rechts=[('VOUT', 'VOUT'), ('GND', 'G2')], w=4)
    tag(d, bk.VIN, '+19V_SW', 'left', 0.8)
    d.add(elm.Line().at(bk.G).left().length(0.8)); d.add(elm.Ground())
    d.add(elm.Line().at(bk.VOUT).right().length(1.5))
    p5 = d.here
    d.add(elm.Dot())
    d.add(elm.Capacitor(polar=True).down().label('*C1\n1000 µF\n10 V', fontsize=8, loc='bottom'))
    d.add(elm.Ground())
    d.add(elm.Line().at(p5).right().length(1.5))
    tag(d, d.here, '+5V_LED', 'up', 0.6)
    gnd(d, bk.G2, 0.6)

    # Pegelwandler
    u2 = ic(d, (25, -9), '*U2 74HCT245 (DIP-20)',
            links=[('A1 (2)', 'A'), ('DIR (1)', 'DIR'), ('/OE (19)', 'OE'), ('GND (10)', 'G')],
            rechts=[('B1 (18)', 'Y'), ('VCC (20)', 'V')], w=4)
    tag(d, u2.A, 'GPIO12 (Pin 32)', 'left', 1.0)
    tag(d, u2.DIR, '+5V_LED', 'left', 1.0)
    d.add(elm.Line().at(u2.OE).left().length(0.6)); d.add(elm.Ground())
    d.add(elm.Line().at(u2.G).left().length(0.6)); d.add(elm.Ground())
    d.add(elm.Line().at(u2.V).right().length(1.0))
    v = d.here; d.add(elm.Dot())
    d.add(elm.Capacitor().at(v).down().label('*C3 100 nF', fontsize=8, loc='bottom')); d.add(elm.Ground())
    tag(d, v, '+5V_LED', 'right', 1.0)
    d.add(elm.Resistor().at(u2.Y).right().label('*R1 330 Ω', fontsize=8))
    tag(d, d.here, 'LED_DIN', 'right', 0.6)
    d.add(elm.Label().at((22.0, -13.4)).label('A2–A8 (Pins 3–9) an GND, B2–B8 (11–17) frei. DIR high = Richtung A → B.', fontsize=7, halign='left'))

    # LED-Skala
    y0 = -16.5
    d.add(elm.Label().at((0, y0 + 2.9)).label('LED-Skala im Lichtkasten: 4 Streifen WS2812B à 28 LEDs (144/m), Daten in Reihe, Versorgung je Streifen einzeln. '
                                              'Software-Grenze ≤ 2 A (Weiß ≤ 30 %).', fontsize=8, halign='left'))
    prev = (0.6, y0 - 0.4 + 0.8)
    tag(d, prev, 'LED_DIN', 'left', 0.01)
    for i, name in enumerate(['U-Band', 'K-Band', 'Stationsmarken', 'L-Band']):
        s = ic(d, (3.5 + i * 7.5, y0 - 0.4), f'Streifen {i+1}: {name}\n28 LEDs', links=[('DIN', 'DI'), ('+5V', 'V'), ('GND', 'G')],
               rechts=[('DOUT', 'DO')], w=3.4)
        if i == 0:
            d.add(elm.Wire('-').at(prev).to(s.DI))
        else:
            d.add(elm.Line().at(prev).right().length(0.5))
            d.add(elm.Line().up().toy(s.DI[1]))
            d.add(elm.Line().right().tox(s.DI[0]))
        prev = s.DO
        tag(d, s.V, '+5V', 'left', 0.5)
        d.add(elm.Line().at(s.G).left().length(0.5)); d.add(elm.Ground())
    d.add(elm.Capacitor(polar=True).at((31.5, y0 - 0.4)).down().label('C2 1000 µF 10 V\nam Lichtkasten', fontsize=8, loc='bottom'))
    d.add(elm.Ground())
    tag(d, (31.5, y0 - 0.4), '+5V_LED', 'up', 0.4)
    return d

# ---------------------------------------------------------------- Blatt 2
def blatt2():
    d = schemdraw.Drawing(show=False, unit=2)
    titel(d, (0, 13), 'Blatt 2: Raspberry Pi 4B, Tasten, Drehgeber',
          'Alle Verbindungen mit Dupont-Kabeln am durchgeführten GPIO-Stecker oben auf dem DigiAMP+. Pull-ups der Tasten im Pi (Software).')
    pins = [  # (Pin, Name, Seite)
        ('1', '3V3'), ('7', 'GPIO4'), ('8', 'GPIO14'), ('9', 'GND'), ('11', 'GPIO17'), ('13', 'GPIO27'),
        ('16', 'GPIO23'), ('17', '3V3'), ('18', 'GPIO24'), ('19', 'GPIO10'), ('21', 'GPIO9'), ('22', 'GPIO25'),
        ('23', 'GPIO11'), ('24', 'GPIO8'), ('26', 'GPIO7'), ('29', 'GPIO5'), ('31', 'GPIO6'), ('32', 'GPIO12'),
        ('33', 'GPIO13'), ('36', 'GPIO16'), ('37', 'GPIO26'), ('39', 'GND')]
    links = [(f'{n} ({p})', f'P{p}') for p, n in pins[:11]]
    rechts = [(f'{n} ({p})', f'P{p}') for p, n in pins[11:]]
    pi = ic(d, (10, 4), 'Raspberry Pi 4B, 40-pol. GPIO\n(über DigiAMP+ durchgeführt)\nDigiAMP+ belegt GPIO0–3, 18–22',
            links=links, rechts=rechts, w=6, ps=0.9)
    # linke Seite
    tag(d, pi.P1, '+3V3', 'left', 0.8)
    d.add(elm.Line().at(pi.P9).left().length(0.8)); d.add(elm.Ground())
    tag(d, pi.P17, '+3V3', 'left', 0.8)
    tag(d, pi.P19, 'GPIO10 → Blatt 1 (A/E)', 'left', 0.8)
    tag(d, pi.P8, 'E1_T', 'left', 0.8)
    for p, n in (('7', 'S3'), ('11', 'S1'), ('13', 'S2'), ('16', 'S4'), ('18', 'S5')):
        d.add(elm.Line().at(getattr(pi, 'P' + p)).left().length(1.5))
        d.add(elm.Button().left().label(f'{n} Cherry MX', fontsize=7))
        d.add(elm.Ground().theta(0))
    # rechte Seite
    d.add(elm.Line().at(pi.P22).right().length(1.5))
    d.add(elm.Button().right().label('S6 Cherry MX', fontsize=7)); d.add(elm.Ground().theta(0))
    tag(d, pi.P21, 'GPIO9 → Blatt 1 (ON)', 'left', 0.8)
    tag(d, pi.P32, 'GPIO12 → Blatt 1 (LED)', 'right', 0.8)
    d.add(elm.Line().at(pi.P39).right().length(0.8)); d.add(elm.Ground())
    for p, n in (('29', 'E1_A'), ('31', 'E1_B'), ('33', 'E2_A'), ('36', 'E2_B'), ('37', 'E2_T'),
                 ('23', 'E3_A'), ('24', 'E3_B'), ('26', 'E3_T')):
        tag(d, getattr(pi, 'P' + p), n, 'right', 0.8)
    d.add(elm.Label().at((0, -2.6)).label('Tasten S1–S6: Reihenfolge von links nach rechts in der Frontplatte (L, M, K, U, TA-TB, AFC-AUS). '
                                         'GPIO14 nur mit abgeschalteter serieller Schnittstelle.', fontsize=7, halign='left'))

    # Drehgeber
    for i, (n, name) in enumerate((('E1', 'Klang'), ('E2', 'Lautstärke'), ('E3', 'Sender'))):
        x0 = i * 11
        y0 = -6.5
        e = ic(d, (x0 + 6, y0), f'{n} {name}\nALPS STEC11B03\nauf Lochraster 20 × 25',
               links=[('A', 'A'), ('B', 'B'), ('Taster 1', 'T')], rechts=[('C', 'C'), ('Taster 2', 'T2')], w=3)
        for a, net, r in (('A', f'{n}_A', '2,7 kΩ'), ('B', f'{n}_B', '2,7 kΩ'), ('T', f'{n}_T', '270 Ω')):
            pin = getattr(e, a)
            d.add(elm.Line().at(pin).left().length(1.2))
            k = d.here
            d.add(elm.Dot())
            d.add(elm.Line().at(k).left().length(0.6))
            d.add(elm.Tag().left().label(net, fontsize=FS))
        d.add(elm.Line().at(e.C).right().length(0.6)); d.add(elm.Ground())
        d.add(elm.Line().at(e.T2).right().length(0.6)); d.add(elm.Ground())
        # Widerstände als Reihe darunter
        yb = y0 - 3.2
        for j, (a, r) in enumerate((('A', '2,7 kΩ'), ('B', '2,7 kΩ'), ('T', '270 Ω'))):
            xx = x0 + 1 + j * 2.4
            d.add(elm.Resistor().at((xx, yb)).down().label(f'{r}', fontsize=7, loc='bottom'))
            d.add(elm.Vdd().at((xx, yb)).label('+3V3', fontsize=7))
            tag(d, (xx, yb - 2.0), f'{n}_{a}', 'down', 0.4)
    d.add(elm.Label().at((0, -14.5)).label(
        'Drehgeber: mindestens 1 mA an A/B und 10 mA am Taster (Datenblatt) → Pull-ups 2,7 kΩ und 270 Ω nach 3,3 V auf der Drehgeberplatine. '
        'Pro Drehgeber 5 Adern: A, B, Taster, 3,3 V, GND.\nKernel: dtoverlay=rotary-encoder, steps-per-period=2 (30 Rastungen, 15 Impulse).', fontsize=7, halign='left'))
    return d

if __name__ == '__main__':
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    zeichnungen = [blatt1(), blatt2()]
    with PdfPages('schaltplan.pdf') as pdf:
        for i, dr in enumerate(zeichnungen, 1):
            fig = dr.draw(show=False)
            f = fig.fig
            f.set_size_inches(16.5, 11.7)  # A3 quer
            dr.save(f'blatt{i}.png', dpi=110)
            pdf.savefig(f, bbox_inches='tight')
            plt.close(f)
