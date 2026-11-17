# Projektstand für neue Sessions

Retro-Radio: Holzgehäuse mit Original-Frontplatte und -Lautsprecherabdeckungen eines DDR-Radios, innen Raspberry Pi mit eigener Verstärkerplatine (Radio HAT). Kommunikation mit dem Nutzer auf Deutsch, kurze Antworten, bei Unklarheiten nachfragen. Direkt auf `main` arbeiten und pushen (vom Nutzer so gewünscht). Gibt die Umgebung einen eigenen Session-Branch vor, zusätzlich dorthin pushen.

Der Nutzer achtet auf Nutzungslimits: PDFs mit `pdftotext -layout` als Text auslesen; Bilder (Kennlinien, Schaltbilder, Formeln) nur von den Seiten lesen, die welche enthalten (`pdftoppm -r 110 -f N -l N -png`, Kopf/Fuß abschneiden, dann als PNG lesen). Keine Subagenten ohne Grund. Neue Datenblätter muss der Nutzer hochladen (ti.com, mouser.com, lcsc.com sind gesperrt).

## Einstieg in eine neue Sitzung

1. Diese Datei lesen.
2. Für die Platine: `PRUEFBERICHT.md` (alle Änderungen mit Begründung, Prüfung zur Bestellreife, offene Punkte), `README.md` (Einbau, Pi-Einrichtung, erster Test), `BESTELLUNG.md` (jedes Feld des JLCPCB-Bestellformulars).
3. Für die Chips: `Datenblaetter/TAS5805M.md` (Verstärker; 1.11 Abgleich, 1.12 Bildinhalte) und `Datenblaetter/TPS54308.md` (5-V-Regler; 1.4 Formeln, 1.7 Abgleich, 2 Bildinhalte) statt der PDFs. Beide Datenblätter sind vollständig gelesen, einschließlich aller Bilder.
4. Für das Gehäuse: `Gehaeuse/README.md`, `Gehaeuse/DRUCKTEILE.md`.

## Was wo liegt

| Pfad | Inhalt |
|---|---|
| `README.md` | Radio HAT: Platine, Bestellung JLCPCB, Netzteil, Steckerbelegung, Pi-Einrichtung, erster Test |
| `BESTELLUNG.md` | Bestellanleitung JLCPCB/JLCONE: alle Felder mit Auswahl und Grund, BOM-Abgleich mit Ersatzteilen, Drehlagen-Tabelle für die Vorschau |
| `PRUEFBERICHT.md` | 26 Änderungen an der Platine mit Grund, Prüfung zur Bestellreife (zehnte Fassung), Prüfung nach TI SLAA902/PCBWay/Analog Devices, Rückmeldung vom 17.11., Datenblattabgleich, offene Punkte, LCSC-Nummern |
| `REICHELT.md` | Bestellliste der Teile zum Selbstlöten (Sockel, Elkos, JST) |
| `Datenblaetter/TAS5805M.md` | Datenblatt TAS5805M (SLASEH5D Rev. D) als Text: deutsche Zusammenfassung (Grenzwerte, Pins, Register, Ein-/Abschaltfolge, Schutz, Filter, Layout, Gehäuse, Abgleich), Bildinhalte, Volltext |
| `Datenblaetter/TPS54308.md` | Datenblatt TPS54308 (SLUSCV2B Rev. B) als Text: Zusammenfassung mit allen Formeln und Tabelle 7-2, Abgleich mit U2, Bildinhalte, Volltext |
| `KiCad/RadioHAT.kicad_pcb` | Platine, einzige Quelle (kein Schaltplan); dazu `RadioHAT.kicad_pro` (Regeln) und `RadioHAT.kicad_dru` (Zusatzregel: auf B.Cu reicht ein Steg der Wärmefalle) |
| `KiCad/werkzeuge/` | `fertigungsdaten.sh`, `drc.py`, `verify.py`, `bilder.sh`; einmalige Änderungsskripte `eingangsschutz.py` (Änd. 17), `aenderung_20_21.py` (Änd. 20/21), `aenderung_23.py` (Änd. 23), `aenderung_24.py` (Änd. 24, Kühlfläche) und `aenderung_25.py` (Änd. 25, Bestellreife; arbeitet in Prüfbericht-Koordinaten x/y ab links unten), nicht erneut ausführen; als Vorlage für neue Änderungen brauchbar. `router.py`: A*-Wegsucher für eine Kupferlage (Raster 0,05 mm, Sperrbereiche), von `aenderung_24.py` benutzt |
| `KiCad/jlc_cpl.py` | Bestückungsdatei mit JLCPCB-Drehwinkeln |
| `JLCPCB/` | Gerber-ZIP (12 Dateien), BOM (31 Zeilen), CPL (96 Bauteile; Passbohrungen und Befestigungslöcher nicht enthalten) |
| `radio_hat_start.sh` | Steuerskript Verstärker: `start [Lautstärke]`, `stop`, `status`, `clear` |
| `Pi/radio-hat.service`, `Pi/asound.conf` | systemd-Dienst (start beim Booten, stop vor dem Herunterfahren), ALSA immer 32 Bit je Kanal |
| `Bilder/` | Renderings der Platine Ober-/Unterseite |
| `Gehaeuse/README.md` | Gehäuse: Aufbau, Zuschnittliste, Leisten, Zusammenbau, Einkaufsliste |
| `Gehaeuse/gehaeuse.scad` | Gehäusemodell (OpenSCAD), bindet `traeger.scad` ein |
| `Gehaeuse/zeichnung.py` | Maßzeichnungen → `zeichnung_gehaeuse.pdf`, `bilder/zeichnung_blatt*.png` |
| `Gehaeuse/DRUCKTEILE.md` | 3D-Druckteile, Beleuchtungs-Auswertung, offene Fragen |
| `Gehaeuse/traeger.scad`, `Gehaeuse/stl/` | Druckteile und STL-Exporte |
| `Gehaeuse/render/render.py` | POV-Ray-Renderings Tag/Nacht (Texturen im selben Ordner) |

## Werkzeuge Gehäuse (in einer frischen Cloud-Session fehlen sie)

```bash
apt-get update && apt-get install -y openscad xvfb povray
pip install matplotlib numpy scipy pillow
```

- Bilder: `cd Gehaeuse && xvfb-run -a openscad -o bilder/ansicht_vorne.png --imgsize=1600,900 --camera=336,95,60,75,0,20,1250 --colorscheme=Tomorrow gehaeuse.scad` (weitere Ansichten: `-D 'ansicht="ohne_deckel"'` Kamera `336,95,60,50,0,200,1250`; `"hinten_offen"` `336,120,60,68,0,215,1400`; `"explosion"` `336,30,60,65,0,25,1900`)
- Zeichnungen: `cd Gehaeuse && python3 zeichnung.py`
- STL: `cd Gehaeuse && openscad -o stl/TEIL.stl -D 'teil="TEIL"' traeger.scad` (TEIL = traeger_links, traeger_rechts, lichtkasten, pi_halter, tastenadapter)
- Renderings: `cd Gehaeuse/render && python3 render.py 1600 1000 gut` (ca. 1 min)
- Maße stehen doppelt in `gehaeuse.scad` und `zeichnung.py` (und teils `render.py`) – bei Änderungen alle anpassen.

## Werkzeuge Platine

```bash
apt-get update && apt-get install -y kicad zip
pip install shapely numpy   # numpy für router.py
```

KiCad 7.0.11 mit `kicad-cli` und Python-Modul `pcbnew` (mit `/usr/bin/python3` aufrufen). `pdftotext` ist vorhanden. Für `bilder.sh`: Node.js und Playwright sind vorinstalliert, Aufruf mit `NODE_PATH=$(npm root -g) bash KiCad/werkzeuge/bilder.sh GERBER-ORDNER`.

Ablauf nach einer Änderung:

1. Änderung per Python-Skript an `KiCad/RadioHAT.kicad_pcb` (vorher Kopie sichern).
2. `python3 KiCad/werkzeuge/drc.py KiCad/RadioHAT.kicad_pcb /tmp/drc refill` → muss 0 Verstöße, 0 unverbundene Pads melden (`drc.py` kopiert `.kicad_pro` und `.kicad_dru` mit). Die gefüllte Kopie `/tmp/drc/RadioHAT.kicad_pcb` zurück nach `KiCad/` kopieren (der Gerber-Export füllt Flächen nicht neu).
3. `bash KiCad/werkzeuge/fertigungsdaten.sh` (DRC, Gerber-ZIP, CPL). BOM von Hand nachtragen, dann BOM- und CPL-Bezeichner abgleichen.
4. `python3 KiCad/werkzeuge/verify.py KiCad/RadioHAT.kicad_pcb ALTE_KOPIE.kicad_pcb` → Messwerte und Netzlistenvergleich (nur gewollte Unterschiede).
5. Bilder neu (`bilder.sh` mit dem Gerber-Ordner, den `fertigungsdaten.sh` ausgibt), `KiCad/RadioHAT.kicad_prl` löschen.
6. `PRUEFBERICHT.md` (Änderungstabelle, Zahlen, LCSC-Tabelle, offene Punkte) und `README.md` nachziehen.

Fallstricke mit `pcbnew` (KiCad 7):

- Nie Objekte entfernen, während über `B.Tracks()`, `B.GetDrawings()` oder `fp.GraphicalItems()` iteriert wird, und danach nicht erneut iterieren: erst alles sammeln, dann in einem Rutsch entfernen, sonst Absturz oder `SwigPyObject`-Fehler.
- Neues Pad in einem Bauteil: nach `fp.Add(pad)` die Bauteilkoordinate mit `pad.SetPos0(...)` setzen und `pad.SetDrawCoord()` aufrufen; `SetPosition` allein speichert (0,0). Bei U1 (Drehung −90°) gilt x_lokal = dy, y_lokal = −dx.
- Ausgegebene Koordinaten sind gerundet; beim Suchen von Leiterbahnen 0,01 mm Toleranz nehmen.
- Lagenname des Bestückungsdrucks ist `F.Silkscreen`. Bestückungsdruck der Platine besteht aus Einzellinien (keine Texte); neue Texte als `PCB_TEXT`.
- Sichtprüfung: `kicad-cli pcb export svg -l F.Cu,F.SilkS,Edge.Cuts,F.Fab --page-size-mode 2 --exclude-drawing-sheet …` und mit Playwright als PNG fotografieren (1300 px = 65 mm, Platinenursprung links oben bei x 100, y 85 mm).
- `jlc_cpl.py` Drehkorrekturen: SOT-23/TSOT-23 +180°, HTSSOP/SOIC +270°, sonst 0°. Für SMB und SOD-123 (D2, D3) ist 0° nicht bestätigt → in der Bestückungsvorschau prüfen.
- `pcbnew.SaveBoard` legt neben einer Kopie ohne `.kicad_pro` eine Standard-Projektdatei an. Vor `drc.py` auf einer Kopie die echte `KiCad/RadioHAT.kicad_pro` daneben kopieren, sonst meldet der DRC 116 `lib_footprint_issues` und andere Netzklassen.
- Neue Leitungen auf Innenlage 1 nicht unter I²S/I²C-Leitungen der Oberseite legen (In1 ist deren Bezugsfläche), nicht unter Endstufe und 5-V-Regler; Vorlage mit Sperrbereichen in `aenderung_24.py`.
- Um H1–H4 liegen Sperrflächen (Regelbereiche) mit 6 mm Durchmesser: keine Leiterbahnen, keine Vias. Neue Teile nicht auf die Passbohrungen TH1–TH3 (1,152 mm) setzen.
- Masseflächen: Pad-Anbindung „THT thermal“; die gebohrten Pads 29 von U1 haben eine eigene Einstellung „voll“. Neue bedrahtete Massepads bekommen damit Wärmefallen.
- Rule Areas in KiCad 7: `ZONE.SetIsRuleArea(True)`, Umriss über `z.Outline().Append(...)`; `PAD.SetZoneConnection(...)` für die Anbindung je Pad; `.kicad_dru`-Regel `(constraint min_resolved_spokes 1)` (Zahl ohne `(min …)`).

## Stand Platine (Radio HAT), 17.11.2026, zehnte Fassung (Rev. 1.0)

Fertig zum Bestellen und für den Einbau in ein Gerät zum Verkauf durchgeprüft (Prüfbericht, „Prüfung zur Bestellreife“), aber ungetestet. 65 × 65 mm, 4 Lagen (F.Cu, In1.Cu, In2.Cu, B.Cu), 1,6 mm. DRC in KiCad 7.0.11: 0 Verstöße, 0 unverbundene Pads. 96 SMD-Bauteile von JLCPCB, 16 zum Selbstlöten. Die Platine wurde aus den Gerber-Daten vom 8.11. zurückgewonnen; es gibt keinen Schaltplan.

Wichtigste Auslegung:

- Verstärker U1 TAS5805M, I²C-Adresse 0x2D (R1 15 kΩ), PDN an GPIO9 mit 10 kΩ nach GND, I²S vom Pi. Alle 28 Pins gegen Datenblatt Tabelle 5-1 geprüft.
- Netzteil 20 V, höchstens 22 V. Eingang: J4+ → F1 (5 A träge) → Q2 AO4407A (Verpolungsschutz, Gate über R13 10 kΩ an GND, Z-Diode D3 15 V) → FB1 (Ferrit 6 A) → PVDD; hinter Q2 TVS D2 SMBJ22A und C46 10 µF.
- 5-V-Regler U2 TPS54308 (350 kHz, FCCM, ersetzt TPS54302 wegen dessen Frequenzspreizung um 400 kHz), L5 10 µH (TI empfiehlt 15 µH, 10 µH zulässig), 2 × 22 µF, Teiler 75 k/10 k → 5,07 V, Vorkopplung C28 100 pF mit R14 2 k in Reihe. Dauerlast etwa 2,4 A (Grenze ist die Spule L5, nicht der Regler). Ein/Aus über X1, Start ab etwa 7,4 V PVDD, Selbsthaltung über GPIO4, Abschalt-Erkennung GPIO10.
- PVDD je Seite: 470 µF Elko, 10 µF 50 V 0805 (C47/C48), 1 µF, 100 nF an den Pins.
- Ausgangsfilter 10 µH (Isat 3,5 A) + 680 nF X7R 1206, dazu 1 nF nach Masse. Bootstrap 220 nF 16 V 0402 direkt unter den Pins.
- Kühlfläche unter U1 wie im TI-Land-Pattern (Änderung 24): Kupfer 3,4 × 9,7 mm, davon 3,1 × 4,05 mm frei, 24 Vias 0,3/0,6 mm im Raster 1,2 mm, an alle Lagen ohne Wärmefallen. Unter U1 liegt auf keiner Lage eine Signalleitung. Lötpaste 2 × 2 Öffnungen, 75 %; 12 Vias liegen unter der Paste.
- Innenlage 1: Masse mit den Doppelbahnen der Ausgänge, 3,3 V am Sockel und HOLD (39 mm vom Sockelpin 7 bis D1, nicht unter I²S/I²C). Innenlage 2: durchgehend Masse.
- Änderung 25 (zehnte Fassung): Sperrflächen 6 mm um H1–H4 (GPIO11 an H3 über B.Cu innen vorbei, GPIO11 an H1 und VENC an H2 um 0,15 mm abgerückt), Wärmefallen an bedrahteten Massepads, Passbohrungen TH1–TH3 1,152 mm für JLCPCB Economic, Bestückungsdruck 0,16 mm / Text 1 mm, „Rev. 1.0 11/2026“. Änderung 26: C15–C18 jetzt C1881 (C377117 war nicht auffindbar). Alle 31 LCSC-Nummern am 17.11. bestätigt.

Bewusst so belassen (vom Nutzer bestätigt):

- Ausgänge am Pin: die ersten 1,5 mm einlagig, davon 0,55 mm schmaler als 0,76 mm (Pinraster 0,65 mm).
- 3,3 V: Pinaustritt an U1 mit 0,4 bis 0,45 mm auf 1,2 mm (der Umweg bei GPIO24 ist seit Änderung 24 0,5 mm breit).
- SPKB+: 1,5 mm lang nur 0,9 mm breit.

Bewusst nicht geändert (begründet in `PRUEFBERICHT.md`, Rückmeldung vom 17.11.):

- X7R im Ausgangsfilter (C0G in 680 nF/1206 gibt es nicht, Wirkung nur oberhalb des Hörbereichs).
- Kein DSP-Limiter (DRC); die Lautstärkegrenze 0 dB im Skript verhindert die Übersteuerung.
- Kein Rückspeiseschutz 5 V gegen USB-C: vom Nutzer entschieden (17.11.2026), am Pi wird nie ein USB-Netzteil angesteckt.
- PDN mit 10 kΩ nach Masse (TI: Pull-up nach DVDD), damit der Verstärker aus bleibt, bis der Pi ihn startet.
- Platine bleibt 65 × 65 mm (Nutzer: „falls es Sinn macht“, 17.11.2026). Bei Musik unter 1 W Verlust; nur Dauer-Sinus mit Vollaussteuerung (etwa 5 W) führt zum Zurückregeln, das verschiebt auch eine größere Platine nur. Größer hieße neuer Pi-Halter und neue Gehäuseplanung.
- Analogverstärkung 0x54 = 0x09 bleibt (Nutzer, 17.11.2026).

Offen vor der Bestellung (Details in `BESTELLUNG.md` und `PRUEFBERICHT.md`, „Offene Punkte“):

- in JLCONE: 4 Lagen, JLC04161H-7628, ENIG oder LeadFree HASL (nicht bleihaltig, RoHS), Via Covering „Epoxy Filled & Capped“ > „Plugged“ > „Tented“ (nie „Untented“), PCBA Economic, Tooling holes „Added by Customer“, Confirm Parts Placement „Yes“;
- Lieferbarkeit von U1 (C478472) und U2 (C168839) prüfen, Ersatztabelle für die übrigen Teile in `BESTELLUNG.md`;
- Drehlagen in der Bestückungsvorschau nach der Tabelle in `BESTELLUNG.md`, Schritt 4.

Am fertigen Gerät zu prüfen (Ablauf in README, „Erster Test“): 5 V am Sockel ohne Pi, `radio_hat_start.sh status` (Play, 48 kHz, 64 Bittakte, keine Fehler), Hörtest auf Pfeifen/Zirpen, Hochpass hörbar, Fehlerregister nach Volllast.

Quellenlage: TAS5805M und TPS54308 vollständig an den PDFs geprüft, Text und Bilder (vom Nutzer hochgeladen, nicht im Repo; Inhalt in `Datenblaetter/`). Die Biquad-Adressen (Buch 0xAA, Seite 0x24, ab 0x18, Format 5.27, a1/a2 negiert) stammen aus TI SLOA263 und dem Treiber mariosgit/TAS58xx, nicht aus dem Datenblatt. Die Frequenzspreizung des alten TPS54302 (±6 %) ist nur aus Suchauszügen belegt.

## Software auf dem Pi

- `radio_hat_start.sh start` folgt Datenblatt 7.5.3.1: PDN high, Stille abspielen für die I²S-Takte, Hi-Z + DSP an, dann 0x02 = 0x00 (768 kHz, BD), 0x53 = 0x60 (175 kHz), 0x54 = 0x09 (17,5 V Spitze = 19 W an 8 Ω), 0x76 = 0x10 (Rückkehr nach Übertemperatur), 0x4C = Lautstärke (Standard 0x60 = −24 dB, nie unter 0x30 = 0 dB), Hochpass 50 Hz in Biquad 1 links (rechts nutzt dieselben Koeffizienten, 0x66 Bit 3 = 0), Fehler löschen (0x78 = 0x80), Play.
- `stop` folgt 7.5.3.2: Mute-Rampe (wenn Takt da), Hi-Z, PDN low. Der Dienst `Pi/radio-hat.service` ruft es vor dem Herunterfahren auf.
- `status` und `clear` zeigen bzw. löschen Fehler (0x70–0x73) im Klartext.
- Einrichtung (README, „Pi einrichten“): `config.txt` mit `dtoverlay=hifiberry-dac`, `gpio-shutdown` (GPIO10), `gpio-poweroff` (GPIO4), I²C und I²S an, SPI aus; Skript nach `/usr/local/bin/`, Dienst nach `/etc/systemd/system/`, `Pi/asound.conf` nach `/etc/asound.conf`.
- Das Skript ist nur mit nachgebauten I²C-Befehlen getestet, nicht am Gerät.

## Festgelegte Entscheidungen (Gehäuse)

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

Gehäuse:

1. Bohrung der Originalknöpfe (Ø, Tiefe, rund/abgeflacht/Feder) → danach Knopfadapter entwerfen.
2. Welches Bauteil an A/E (Platz bisher 12 × 12 wie Drehgeber; Alternative Poti mit Schalter)?
3. Wellenlänge der STEC11B (angenommen 20 mm; Parameter `enc_welle`).
4. LED-Skalenbeleuchtung mit Senderzeiger (WS2812B + RP2040-Zero per USB) oder nur warmweiß über GPIO20?
5. Druckbettgröße (Teile sind auf ≤ 200 mm ausgelegt).

Platine: keine offenen Fragen (17.11.2026 entschieden: kein Rückspeiseschutz; Kühlfläche nach TI umgesetzt; Platine bleibt 65 × 65 mm; Analogverstärkung bleibt 0x09; Bestellreife geprüft, Rev. 1.0).

## Nächste Schritte (Stand Ende der Sitzung vom 17.11.2026)

- Letzte Sitzung (17.11.2026, abends): vollständige Prüfung zur Bestellreife für ein verkaufbares Gerät (Prüfbericht, zehnte Fassung), Änderungen 25 und 26, Bestellanleitung `BESTELLUNG.md`. Geprüft und ohne Änderung: Encoder-Ströme (ALPS EC11-Reihe: Drehgeber ≤ 10 mA, Taster 0,5–100 mA), BOOT-Schleife des 5-V-Reglers (etwa 8 mm, unkritisch). Alles ist auf `main` gepusht.
- Platine: bestellfertig. Der Nutzer bestellt selbst in JLCONE nach `BESTELLUNG.md`. Danach „Erster Test“ nach README und Rückmeldung der Messwerte.
- Gehäuse: Antworten auf die offenen Fragen 1 bis 5 abwarten, dann Knopfadapter und Druckteile v2.
- Ohne neue Angaben vom Nutzer gibt es an der Platine nichts zu tun. Nicht von sich aus weiter umbauen.

## Hinweise

- Aus der Cloud nicht erreichbar: amazon.de, holzzuschnitt-shop.de, ebay.de, ti.com, mouser.com, lcsc.com, jlcpcb.com. Erreichbar: GitHub (auch raw.githubusercontent.com). Die Websuche liefert LCSC-Nummern und Datenblattauszüge.
- Belegte GPIOs siehe `README.md`; frei sind nur GPIO14, 15, 20.
