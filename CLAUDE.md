# Projektstand für neue Sessions

Retro-Radio: Holzgehäuse mit Original-Frontplatte und -Lautsprecherabdeckungen eines DDR-Radios, innen Raspberry Pi mit **Raspberry Pi DigiAMP+** als Verstärker (seit 18.11.2026; vorher eigene Platine „Radio HAT“, siehe unten). Kommunikation mit dem Nutzer auf Deutsch, kurze Antworten, bei Unklarheiten nachfragen. Direkt auf `main` arbeiten und pushen (vom Nutzer so gewünscht). Gibt die Umgebung einen eigenen Session-Branch vor, zusätzlich dorthin pushen.

Der Nutzer achtet auf Nutzungslimits: PDFs mit `pdftotext -layout` als Text auslesen; Bilder nur von den Seiten lesen, die welche enthalten (`pdftoppm -r 110 -f N -l N -png`). Keine Subagenten ohne Grund. Neue Datenblätter muss der Nutzer hochladen (ti.com, mouser.com, lcsc.com sind gesperrt).

## Einstieg in eine neue Sitzung

1. Diese Datei lesen.
2. Elektronik und Pi: `README.md` (DigiAMP+, Netzteil, GPIO-Belegung, Pi-Einrichtung, Ein/Aus, erster Test).
3. Gehäuse: `Gehaeuse/README.md`, `Gehaeuse/DRUCKTEILE.md`.

## Was wo liegt

| Pfad | Inhalt |
|---|---|
| `README.md` | DigiAMP+ (Kurzdaten, Lage der Anschlüsse), Pi 4B, Netzteil, Soft-Off mit Original-A/E und Pololu-Modul, Steuerplatine (Verdrahtungstabelle), LED-Strom, GPIO-Tabelle, `config.txt`, Lautstärke, LEDs, erster Test |
| `Bilder/digiamp_plus.jpg` | Lageplan DigiAMP+ aus der RPi-Doku (CC BY-SA 4.0) |
| `Schaltplan/` | Schaltplan als PDF/PNG aus `schaltplan.py` (schemdraw + matplotlib; `pip install schemdraw matplotlib`). Blatt 1 Versorgung/Soft-Off/LEDs, Blatt 2 Pi-GPIO/Tasten/Drehgeber. Bei Änderungen an Verdrahtung oder GPIOs mit anpassen |
| `EINKAUF.md` | vollständige Bestellliste (Elektronik, Kleinteile; Holz in `Gehaeuse/README.md`) |
| `Pi/asound.conf` | ALSA: Hochpass 50 Hz (LADSPA `butthigh_iir` aus swh-plugins) vor Karte 0, ungetestet |
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
- STL: `cd Gehaeuse && openscad -o stl/TEIL.stl -D 'teil="TEIL"' traeger.scad` (TEIL = traeger_links, traeger_rechts, lichtkasten, pi_halter, steuer_halter, ae_platte, kupplung, tastenadapter)
- Renderings: `cd Gehaeuse/render && python3 render.py 1600 1000 gut` (ca. 1 min)
- Maße stehen doppelt in `gehaeuse.scad` und `zeichnung.py` (und teils `render.py`) – bei Änderungen alle anpassen.

## Stand Elektronik (18.11.2026)

Der Nutzer verwendet den fertigen Raspberry Pi DigiAMP+ statt der eigenen Platine. Die eigene Platine (Radio HAT Rev. 1.1, TAS5805M, KiCad, JLCPCB-Daten, Prüfbericht, Datenblatt-Auszüge) ist aus dem Repo entfernt; letzter Stand Commit `c25365f`.

DigiAMP+ (Quellen: raspberrypi.com Produktseite und Audio-Doku, pinout.xyz, Kernel `overlays/README` und `sound/soc/bcm/iqaudio-dac.c`, rpi-6.12.y):

- TAS5756M, I²C 0x4C (Overlay `iqaudio-dacplus`, eingebunden von `rpi-digiampplus`), bis 2 × 35 W laut Produktseite (Doku-Tabelle sagt 2 × 25 W). 58 × 65 mm, steckt auf dem Pi, GPIO-Stecker durchgeführt.
- 12–24 V über Hohlbuchse 5,5 × 2,5 mm oder P5; versorgt den Pi mit 5,1 V / 2,5 A über GPIO, Pi-eigener Stromanschluss verboten. Doku: ausgelegt für Pi 3 und älter, Pi 4 mit wenig USB-Last.
- Belegt GPIO0/1 (EEPROM), 2/3 (I²C), 18–21 (I²S), 22 (Mute, Treiber steuert sie; `auto_mute_amp` ist bei `rpi-digiampplus` Standard).
- Lautstärke: ALSA-Element „Digital“, ohne `24db_digital_gain` vom Treiber auf 0 dB (Wert 207) begrenzt.
- Card-Name „RPi DigiAMP+“; mit `dtparam=audio=off` und `vc4-kms-v3d,noaudio` ist er Karte 0 (darauf baut `Pi/asound.conf`).

Vom Nutzer festgelegt (18.11.2026): Raspberry Pi 4B, grüner DigiAMP+, Netzteil hinten am Radio (nicht direkt am DigiAMP+), Netzteil gebe ich vor; Original-RFT-A/E-Schalter mit softem Ausschalten; Skala WS2812B mit Senderzeiger; Originalknöpfe Bohrung Ø 3 × 17 mm; Tasten werden aufgeklebt.

Umgesetzt (18.11.2026, dritter Teil):

- Netzteil Mean Well GST90A19-P1M (19 V, 4,74 A, 5,5 × 2,5, C14; Reichelt), Netzkabel NKSK 200 SW. Alternative XP VEC65US19. Einbaubuchse Delock 90188 (M8 × 0,75), Hohlstecker Lumberg 1634 02 an Silikonlitze 0,75 mm². Bestelllinks in `EINKAUF.md` (fast alles Reichelt, geprüft 18.11.2026).
- Soft-Off: Einbaubuchse hinten → Pololu Big MOSFET Slide Switch HP (#2815; SW-Pin über Schalter auf GND = an, ON-Pin > 1 V = an; Bordschalter auf OFF) → VOUT an DigiAMP+ (DC-Kabel mit Hohlstecker) und Pololu D36V28F5 (5 V für LEDs). A/E (Original, nur ~0,4 mA) zwischen Punkt X und GND; BAT85 SW→X und GPIO10→X. `gpio-shutdown` GPIO10 (active_low=0, pull-up), `gpio-poweroff` GPIO9 active_low=1 an ON. Schaltplan des Moduls geprüft (pololu.com).
- LEDs: 112 × WS2812B, 5 V vom D36V28F5, Daten GPIO12 (PWM0, `rpi_ws281x`) über 74HCT245, Software-Begrenzung ≤ 2 A. RP2040 entfällt, USB des Pi bleibt frei.
- GPIO: Taste 3 → GPIO4; Taster Drehgeber Klang GPIO12 → GPIO14 (UART aus). Frei nur GPIO15.
- Drehgeber ALPS STEC11B03 (30 Rastungen/15 Impulse, Taster, Welle Ø 6 × 25 geschlitzt), Pull-ups 2,7 kΩ/270 Ω auf ihren Lochrasterplatinen; gedruckte Kupplung Ø 11 × 16 mit Zylinderstift Ø 3 × 30 in den Originalknopf; Lager Ø 3,4 in der Trägerwand.
- A/E-Halteplatte mit Loch Ø 10,5 an zwei Säulen; Maße des RFT-Schalters (`rft_a` 41, Buchse 8, Ø 25, Tiefe 13) nur aus dem Foto geschätzt.
- Pi-Halter: Pi 65 mm hinter der Frontplatte (hinter den Drehgebern), GPIO-Kante vorne, 4 Sockel mit Bolzen M2,5 × 6 I/A von unten verschraubt. Neuer Steuerplatinen-Halter (Lochraster 70 × 50) rechts daneben.
- Hochpass 50 Hz per ALSA/LADSPA.

Nichts davon ist am Gerät getestet.

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
- Originalknöpfe: 19 mm lang + 3 mm Nase, Ø vorne 15 / hinten 16, Bohrung Ø 3 × 17 mm mit Metallhülse. Originaltasten: 18 lang, hinten 12, vorne 11 breit.

## Stand 3D-Druck

Entwurf v2 (18.11.2026, siehe `Gehaeuse/DRUCKTEILE.md`), noch nicht gedruckt: Träger mit Kupplungsrohren und A/E-Säulen, Kupplungen, A/E-Platte, Pi- und Steuerplatinen-Halter. Tasten 8 mm vor der Frontplatte, Adapter flach zum Aufkleben.

## Offene Fragen an den Nutzer (Antworten stehen noch aus)

1. Maße des Original-A/E-Schalters: Flansch bis Wellenende, Länge und Ø der Gewindebuchse, Gehäuse-Ø und -tiefe, Ø des dünnen Wellenendes.
2. Druckbettgröße (Teile sind auf ≤ 200 mm ausgelegt).

## Nächste Schritte (Stand 18.11.2026)

- 18.11.2026: Umstellung auf DigiAMP+ (eigene Platine entfernt, README neu, `Pi/asound.conf` neu, Pi-Halter und Bilder `ansicht_offen.png`/`ansicht_hinten.png` neu, `DRUCKTEILE.md` angepasst).
- 18.11.2026, zweiter Teil: Pi 4B, grün, harte Trennung über A/E, Netzteilvorgabe, Buchse hinten, Pi im Halter gedreht, Einkaufsliste Elektronik in README.
- 18.11.2026, dritter Teil: Soft-Off mit Original-A/E und Pololu-Modulen, LEDs mit eigenem 5-V-Wandler an GPIO12, Kupplungen für die Originalknöpfe, `EINKAUF.md`, Druckteile v2.
- Maße des A/E-Schalters abwarten, Parameter `rft_*` anpassen, STL neu.

## Hinweise

- Aus der Cloud nicht erreichbar: amazon.de, holzzuschnitt-shop.de, ebay.de, ti.com, mouser.com, lcsc.com, jlcpcb.com. Erreichbar: GitHub (auch raw.githubusercontent.com). Die Websuche liefert LCSC-Nummern und Datenblattauszüge.
- Belegte GPIOs siehe `README.md`; frei ist nur GPIO15.
