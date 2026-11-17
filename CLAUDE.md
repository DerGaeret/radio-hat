# Projektstand für neue Sessions

Retro-Radio: Holzgehäuse mit Original-Frontplatte und -Lautsprecherabdeckungen eines DDR-Radios, innen Raspberry Pi mit eigener Verstärkerplatine (Radio HAT). Kommunikation mit dem Nutzer auf Deutsch, kurze Antworten, bei Unklarheiten nachfragen. Direkt auf `main` arbeiten und pushen (vom Nutzer so gewünscht).

## Was wo liegt

| Pfad | Inhalt |
|---|---|
| `README.md` | Radio HAT: Platine, Bestellung JLCPCB, Steckerbelegung, Pi-Einrichtung |
| `KiCad/`, `JLCPCB/`, `PRUEFBERICHT.md`, `REICHELT.md` | Platine (4 Lagen, 65 × 65 mm, Lochbild wie Pi) |
| `Gehaeuse/README.md` | Gehäuse: Aufbau, Zuschnittliste, Leisten, Zusammenbau, Einkaufsliste |
| `Gehaeuse/gehaeuse.scad` | Gehäusemodell (OpenSCAD), bindet `traeger.scad` ein |
| `Gehaeuse/zeichnung.py` | Maßzeichnungen → `zeichnung_gehaeuse.pdf`, `bilder/zeichnung_blatt*.png` |
| `Gehaeuse/DRUCKTEILE.md` | 3D-Druckteile, Beleuchtungs-Auswertung, offene Fragen |
| `Gehaeuse/traeger.scad`, `Gehaeuse/stl/` | Druckteile und STL-Exporte |
| `Gehaeuse/render/render.py` | POV-Ray-Renderings Tag/Nacht (Texturen im selben Ordner) |

## Werkzeuge (in einer frischen Cloud-Session fehlen sie)

```bash
apt-get update && apt-get install -y openscad xvfb povray
pip install matplotlib numpy scipy pillow
```

- Bilder: `cd Gehaeuse && xvfb-run -a openscad -o bilder/ansicht_vorne.png --imgsize=1600,900 --camera=336,95,60,75,0,20,1250 --colorscheme=Tomorrow gehaeuse.scad` (weitere Ansichten: `-D 'ansicht="ohne_deckel"'` Kamera `336,95,60,50,0,200,1250`; `"hinten_offen"` `336,120,60,68,0,215,1400`; `"explosion"` `336,30,60,65,0,25,1900`)
- Zeichnungen: `cd Gehaeuse && python3 zeichnung.py`
- STL: `cd Gehaeuse && openscad -o stl/TEIL.stl -D 'teil="TEIL"' traeger.scad` (TEIL = traeger_links, traeger_rechts, lichtkasten, pi_halter, tastenadapter)
- Renderings: `cd Gehaeuse/render && python3 render.py 1600 1000 gut` (ca. 1 min)
- Maße stehen doppelt in `gehaeuse.scad` und `zeichnung.py` (und teils `render.py`) – bei Änderungen alle anpassen.

## Stand Platine (Radio HAT), 17.11.2026 (sechste Fassung)

- Fertig zum Bestellen, aber ungetestet. 4 Lagen (F.Cu, In1.Cu, In2.Cu, B.Cu), 1,6 mm. DRC in KiCad 7.0.11: 0 Verstöße, 0 unverbundene Pads.
- `KiCad/RadioHAT.kicad_pcb` ist die Quelle. Es gibt keinen Schaltplan; die Platine wurde aus den Gerber-Daten vom 8.11. zurückgewonnen. Änderungen direkt in der Platine machen (KiCad-Python: Objekte erst sammeln, dann entfernen, sonst stürzt `pcbnew` ab).
- Fertigungsdaten neu erzeugen: `bash KiCad/werkzeuge/fertigungsdaten.sh` (DRC, Gerber-ZIP mit 12 Dateien, CPL). Vorher die Platine mit neu gefüllten Flächen speichern (`drc.py … refill` legt eine gefüllte Kopie an). Stückliste von Hand pflegen. Bilder: `KiCad/werkzeuge/bilder.sh`. Messwerte: `python3 KiCad/werkzeuge/verify.py KiCad/RadioHAT.kicad_pcb`.
- Werkzeuge in einer frischen Cloud-Session: `apt-get install -y kicad zip` (KiCad 7 mit `kicad-cli` und Python-Modul `pcbnew`), `pip install shapely`; für die Bilder Node.js, `pcb-stackup@4.2.8` und Playwright. ti.com, mouser.com und lcsc.com sind aus der Cloud nicht erreichbar, GitHub schon.
- `PRUEFBERICHT.md` enthält alle 19 Änderungen, die Prüfung nach TI SLAA902, PCBWay und Analog Devices und die Antwort auf die Rückmeldung vom 17.11. (Eingangsschutz F1/Q2/D2/D3/FB1/C46, Regler TPS54308 statt TPS54302, Startskript mit 768 kHz, 175 kHz Bandbreite, Lautstärke ≤ 0 dB, Hochpass 50 Hz).
- Bewusst so belassen (vom Nutzer bestätigt):
  - Ausgänge am Pin: die ersten 1,5 mm einlagig, davon 0,55 mm schmaler als 0,76 mm. Grund ist das Pinraster von 0,65 mm, das lässt sich nicht ändern.
  - 3,3 V: zwei kurze Stellen mit 0,35 bis 0,45 mm.
  - SPKB+: 1,5 mm lang nur 0,9 mm breit.
- Bewusst nicht eingebaut (Entscheidung des Nutzers steht aus): Rückspeiseschutz 5 V gegen USB-C; X7R im Ausgangsfilter bleibt.
- Netzteil höchstens 22 V (TVS-Diode SMBJ22A).
- Offen vor der Bestellung (Liste in `PRUEFBERICHT.md`, „Offene Punkte“):
  - bei JLCPCB 4 Lagen wählen; der Preis vom 8.11. galt für 2 Lagen;
  - Lieferbarkeit von U1 (C478472), U2 (C168839), C16772 und den neuen Extended-Teilen prüfen;
  - Drehlagen in der Bestückungsvorschau prüfen, besonders Q2, D2, D3.



- Außen 672 × 138 × 190 mm + 4 Chromfüße Ø 25 × 20. Platte 8 mm Dekor „Nuss Sizilia“ (holzzuschnitt-shop.de), alle Ecken innen mit Kiefernleisten 15 × 15 verleimt.
- Frontplatte 300 × 114 × 3 zwischen zwei Abdeckungen 178 × 112 × 7, Abdeckungen stoßen an die Seitenwände. Holz steht 3 mm vor den Abdeckungen; Frontplatte hinten bündig mit den Abdeckungen (vorne 4 mm tiefer).
- Chromleisten: Alu-Vierkant 4 × 4 × 656 mm (Amazon B0FKGXWN44), oben und unten.
- Zwei Frontbretter 200 × 122 (je 22 mm hinter die Frontplatte), dazwischen 256 mm frei für die Bedienteile.
- Lautsprecher Sharp VSP0010PBS78A (Korb 110, Löcher 84 mm Quadrat, Ausschnitt Ø 100), geschlossene Kammern je 3,0 l netto, M4-Senkkopf von vorne.
- Abdeckungen abnehmbar über Magnete 10 × 3 im Frontbrett + Stahlplättchen.
- Rückwände innen eingesetzt: Kammern eingeleimt (170 × 122), Technikfach-Deckel 299 × 121 magnetisch mit Griffloch, Lüftung, DC-Buchse.

## Frontplatte (vom Nutzer gemessen, px ab links, pz ab unten)

- Löcher Ø 10 bei pz 33: A/E px 29, Klang 54, Lautstärke 104, Sender 264 (36 von rechts).
- 6 Tastenfenster 13 × 13, Abstand 7 mm, Unterkante pz 7, erstes ab px 126.
- Befestigungslöcher: Mitte 19 mm vom Seitenrand (Höhe aus Foto ca. pz 11 und 102).
- Durchsichtig (aus Foto, ±1,5): Schlitze U pz 56,5–61,5, K 69–74,5, L 94–99,5 (je px 33–222), Stationsmarken pz 79,5–89.
- Originalknöpfe: 19 mm lang + 3 mm Nase, Ø vorne 15 / hinten 16. Originaltasten: 18 lang, hinten 12, vorne 11 breit.

## Stand 3D-Druck

Entwurf v1 fertig (siehe `Gehaeuse/DRUCKTEILE.md`), noch nicht gedruckt. Annahmen: Drehgeber-Welle 20 mm, Tasten 8 mm vor der Frontplatte, Drehgeber auf Lochraster 20 × 25, Pi vorne/HAT hinten auf dem Boden.

## Offene Fragen an den Nutzer (Antworten stehen noch aus)

1. Bohrung der Originalknöpfe (Ø, Tiefe, rund/abgeflacht/Feder) → danach Knopfadapter entwerfen.
2. Welches Bauteil an A/E (Platz bisher 12 × 12 wie Drehgeber; Alternative Poti mit Schalter)?
3. Wellenlänge der STEC11B (angenommen 20 mm; Parameter `enc_welle`).
4. LED-Skalenbeleuchtung mit Senderzeiger (WS2812B + RP2040-Zero per USB) oder nur warmweiß über GPIO20?
5. Druckbettgröße (Teile sind auf ≤ 200 mm ausgelegt).

## Hinweise

- Shop-Seiten (amazon.de, holzzuschnitt-shop.de, ebay.de) sind aus der Cloud-Umgebung nicht erreichbar.
- Belegte GPIOs siehe `README.md`; frei sind nur GPIO14, 15, 20.
