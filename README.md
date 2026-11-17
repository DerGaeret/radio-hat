# Radio HAT

Raspberry-Pi-Aufsteckplatine mit Stereo-Verstärker TAS5805M (2 × 19 W an 8 Ω), 5-V-Regler für den Pi, sechs Tasten, drei Drehencodern und Ein/Aus-Schalter. Der 20-V-Eingang ist mit Sicherung, Verpolungsschutz, TVS-Diode und Ferritfilter geschützt.

| Datei | Wofür |
|---|---|
| `JLCPCB/Gerber_RadioHAT.zip` | Platinendaten zum Hochladen bei JLCPCB |
| `JLCPCB/BOM_RadioHAT.csv` | Stückliste für die SMD-Bestückung |
| `JLCPCB/CPL_RadioHAT.csv` | Bauteilpositionen für die SMD-Bestückung |
| `radio_hat_start.sh` | Steuerskript für den Verstärker auf dem Pi (start, stop, status, clear) |
| `Pi/` | systemd-Dienst und ALSA-Einstellung für den Pi |
| `Datenblaetter/TAS5805M.md`, `Datenblaetter/TPS54308.md` | Datenblätter von Verstärker und 5-V-Regler als Text, mit Zusammenfassung, Bildinhalten und Abgleich |
| `KiCad/` | Platine als KiCad-Projekt zum Ändern, dazu das Skript für die Bestückungsdatei |
| `BESTELLUNG.md` | Schritt-für-Schritt-Anleitung für die Bestellung bei JLCPCB |
| `PRUEFBERICHT.md` | Was geprüft und geändert wurde, offene Punkte |
| `REICHELT.md` | Bestellliste für die Teile zum Selbstlöten |
| `Bilder/` | Ober- und Unterseite der Platine als Lötvorlage |
| `Gehaeuse/` | Holzgehäuse: 3D-Modell, Maßzeichnungen, Zuschnittliste |

![Oberseite](Bilder/render_top.png)

Die Bilder zeigen den aktuellen Stand vom 17.11.2026. Sie sind direkt aus den Gerber-Dateien gerendert und zeigen Kupfer, Lötstopp und Bestückungsdruck der Außenseiten, aber keine Bauteilkörper. Die beiden Innenlagen sind nicht zu sehen.

Die Platine ist neu entworfen und ungetestet. Beim ersten Einschalten keine Lautsprecher anschließen und die Spannungen prüfen (siehe unten).

## Bestellen bei JLCPCB

Die vollständige Anleitung mit jedem Feld des Bestellformulars steht in **`BESTELLUNG.md`**. Kurzfassung:

- Dateien im Ordner `JLCPCB`: `Gerber_RadioHAT.zip`, `BOM_RadioHAT.csv`, `CPL_RadioHAT.csv`.
- Platine: FR-4, 4 Lagen (Lagenfolge F.Cu, In1.Cu, In2.Cu, B.Cu, Aufbau JLC04161H-7628), 1,6 mm, grün, 5 Stück. Oberfläche **ENIG** oder **LeadFree HASL**, nicht „HASL (with lead)“ (bleihaltig, für ein verkauftes Gerät nicht zulässig). Via Covering „Epoxy Filled & Capped“, sonst „Plugged“, sonst „Tented“, nie „Untented“ (unter U1 liegen 12 Vias in der Lötpaste).
- Bestückung: Economic, Top Side, 2 Stück, Tooling holes „Added by Customer“ (die Platine hat drei Passbohrungen 1,152 mm), Confirm Parts Placement „Yes“.
- Vor dem Bezahlen: Lagerbestand von U1 (C478472) und U2 (C168839) und die Drehlage von sieben Bauteilen in der Bestückungsvorschau prüfen (Tabelle in `BESTELLUNG.md`, Schritt 4).

Der Web-Preis vom 8.11.2026 (32,66 € für 5 Platinen, 2 davon bestückt) galt für den alten zweilagigen Stand; den aktuellen Preis zeigt das Angebot.

## Selbst zu löten

JLCPCB liefert nur die SMD-Teile. Alle Durchsteckteile lötest du selbst ein:

- **Sockel J1:** von der Unterseite einstecken, auf der Oberseite verlöten (40 Lötstellen). Pin 1 liegt rechts oben, weil die Platine um 180° gedreht auf dem Pi sitzt.
- **Elkos C1, C2 (470 µF, mindestens 35 V, 10 mm Durchmesser, 5 mm Raster):** Der Minus-Streifen des Elkos gehört auf die weiß gefüllte Hälfte des Aufdrucks, das lange Bein (+) ins Loch neben dem „+“.
- **JST-Stecker S1–S6, X1, E1–E3:** Die Gehäuse passen genau in die weißen Umrisse.
- **Schraubklemmen J2, J3, J4:** deine eigenen, Raster 5,0 oder 5,08 mm. Die Kabeleinführung zum Platinenrand drehen. Bei J4 darf das Klemmengehäuse vom Lötstift aus höchstens 4 mm zur Platinenmitte reichen (Aufdruck-Umriss), sonst sitzt es auf der Sicherung F1. Übliche Klemmen mit 7 bis 8 mm Tiefe und mittigen Stiften passen.

Die Massepads der Durchsteckteile haben Wärmefallen (Stege zur Massefläche). Ein Lötkolben mit etwa 60 W und mittlerer Meißelspitze reicht; jede Lötstelle muss rundum glänzend durchfließen, auch die Massepins am Sockel. Für ein Gerät, das verkauft wird, bleifreies Lot verwenden (RoHS).

## Einbau neben dem Pi

Die Platine steckt auf dem GPIO-Stecker und zeigt vom Pi weg. Sie überdeckt nur den 7 mm breiten Streifen am Stecker, der Rest liegt neben dem Pi.

- Die beiden oberen Löcher der Platine liegen genau über den zwei Pi-Löchern an der GPIO-Seite. Dort mit M2,5-Abstandshaltern verschrauben. Der Abstand beträgt 11 mm, bei 10-mm-Bolzen also etwa 1 mm mit Unterlegscheiben ausgleichen.
- Die beiden unteren Löcher hängen frei. Dort die Platine im Gehäuse mit eigenen Abstandshaltern stützen, sonst hebelt sie am GPIO-Stecker.
- Um jedes Loch liegt in 6 mm Durchmesser nur Massefläche unter Lötstopp, keine Leiterbahn. Schraubenköpfe, Muttern, Unterlegscheiben und Bolzen bis 6 mm Durchmesser (M2,5-Sechskant mit 5 mm Schlüsselweite) dürfen aus Metall sein.
- Die drei kleinen Löcher (1,152 mm) sind Passbohrungen für die Bestückung bei JLCPCB und bleiben frei.

## Vor dem ersten Anstecken der Kabel

Pin 1 ist an jedem Stecker das eckige Lötpad. Beim Encoder-Kabel die Reihenfolge aus der Tabelle unten mit dem gelieferten Stecker vergleichen.

## Netzteil

- 20 V Gleichspannung, 3 A oder mehr (60 bis 65 W).
- Ein geregeltes Schaltnetzteil verwenden. Ein ungeregeltes Trafo-Netzteil würde mit 100 Hz brummen; die Elkos auf der Platine sind kein Netzfilter.
- Angeschlossen wird es an der Schraubklemme J4 (+ links, − rechts). Das Kabel also abisolieren oder über einen Hohlbuchsen-Adapter mit Schraubklemme führen.
- Eingangsschutz: Sicherung F1 (5 A träge), P-MOSFET Q2 gegen Verpolung, TVS-Diode D2 (SMBJ22A) gegen Spannungsspitzen, Ferrit FB1 mit C46 gegen Störungen auf dem Netzteilkabel. Bei falscher Polung bleibt die Platine aus, es geht nichts kaputt und die Sicherung bleibt ganz.
- Am besten erst das Netzteil an die Platine stecken und dann in die Steckdose. Beim Einstecken in ein schon laufendes Netzteil fließt ein kurzer hoher Ladestrom in die Elkos.
- Rechnung: Verstärker höchstens 2 × 20 W / 0,88 ≈ 45,5 W, 5-V-Regler für den Pi bis etwa 17 W (3 A am Ausgang), zusammen etwa 62 W.
- Die 5-V-Schiene liefert dauerhaft etwa 2,4 A; mehr lässt die Spule L5 nicht zu (der Regler selbst könnte 3 A). Für einen Pi 4 reicht das, solange keine stromhungrigen USB-Geräte am Pi hängen. Für einen Pi 5 unter Last reicht es nicht.
- Nicht mehr als 22 V anschließen. Darüber beginnt die TVS-Diode D2 zu leiten (Durchbruch ab 24,4 V); der Verstärker selbst verträgt 26,4 V. Die Elkos C1 und C2 müssen mindestens 35 V vertragen.
- Den Pi nie gleichzeitig über USB-C versorgen, er bekommt seine 5 V von der Platine. Die Platine hat bewusst keinen Rückspeiseschutz (Entscheidung vom 17.11.2026: es wird kein USB-Netzteil angesteckt). Zwei Netzteile würden gegeneinander arbeiten, und der 5-V-Regler würde Strom aus USB-C zurück in die 20-V-Schiene pumpen.
- Die Lautsprecher haben 8 Ω. Das Datenblatt verlangt im Stereobetrieb mindestens 6 Ω (Überstromgrenze 5 A je Ausgang).
- Kein Lautsprecheranschluss darf mit Masse verbunden werden, auch nicht über einen Umschalter oder einen Subwoofer-Verstärker mit gemeinsamer Masse. Beide Klemmen führen Signal (Brückenschaltung), eine Verbindung nach Masse schließt den Ausgang kurz.

## Steckverbinder

Alle Taster und Encoder schalten gegen GND. Bei S1 bis S6 kommen die Pull-ups vom Pi und müssen in der Software aktiviert werden. Die Encoder haben Pull-ups auf der Platine (siehe unten).

| Stecker | Bauteil | Pin 1 | Pin 2 | Pin 3 | Pin 4 |
|---|---|---|---|---|---|
| S1 | Taste 1 (XH-2) | GPIO17 | GND | | |
| S2 | Taste 2 (XH-2) | GPIO27 | GND | | |
| S3 | Taste 3 (XH-2) | GPIO22 | GND | | |
| S4 | Taste 4 (XH-2) | GPIO23 | GND | | |
| S5 | Taste 5 (XH-2) | GPIO24 | GND | | |
| S6 | Taste 6 (XH-2) | GPIO25 | GND | | |
| E1 | Encoder 1 (XH-4) | A = GPIO5 | B = GPIO6 | Taster = GPIO12 | GND |
| E2 | Encoder 2 (XH-4) | A = GPIO13 | B = GPIO16 | Taster = GPIO26 | GND |
| E3 | Encoder 3 (XH-4) | A = GPIO11 | B = GPIO8 | Taster = GPIO7 | GND |
| X1 | Ein/Aus-Schalter (XH-2) | Schalter | Schalter | | |
| J2 | Lautsprecher rechts | + | − | | |
| J3 | Lautsprecher links | − | + | | |
| J4 | Netzteil 20 V | + | − | | |

## Deine Bauteile

- **Cherry MX Blue (S1 bis S6):** Die zwei Kontakte sind beliebig tauschbar. In der Software 20 ms entprellen.
- **Ein/Aus-Schalter (X1):** Ein rastender Schalter passt. Über ihn fließen etwa 0,2 mA bei 18 V (höchstens 2 mA, falls das Kabel kurzschließt; R10 begrenzt), er liegt nicht im Hauptstromkreis.
- **ALPS STEC11B (E1 bis E3):** A, C, B liegen in einer Reihe, C in der Mitte. Die beiden Tasterkontakte liegen gegenüber. Pin C und ein Tasterkontakt gehen zusammen auf GND (Pin 4), der andere Tasterkontakt auf Pin 3.

Der Encoder verlangt laut Datenblatt mindestens 1 mA an A/B und 10 mA am Taster. Die Platine liefert deshalb 1,2 mA über 2,7 kΩ und 12 mA über 270 Ω aus dem 3,3-V-Pin 1 des Pi.

Beim Encoder ergeben zwei Rastungen einen vollen Impulszyklus. Üblicher Code wie `gpiozero.RotaryEncoder` zählt nur jede zweite Rastung. Das passende Kernel-Overlay in `/boot/firmware/config.txt`, einmal pro Encoder:

```
dtoverlay=rotary-encoder,pin_a=5,pin_b=6,relative_axis=1,steps-per-period=2
dtoverlay=rotary-encoder,pin_a=13,pin_b=16,relative_axis=1,steps-per-period=2
dtoverlay=rotary-encoder,pin_a=11,pin_b=8,relative_axis=1,steps-per-period=2
```

Stimmt die Drehrichtung nicht, A und B im Overlay tauschen. Die Encoder-Taster liegen auf GPIO12, 26 und 7 und brauchen 20 ms Entprellung.

Vom Pi belegt sind außerdem: GPIO2/3 (I²C), GPIO18/19/21 (I²S), GPIO9 (Verstärker-PDN), GPIO10 (Schalter-Erkennung), GPIO4 (Selbsthaltung). Frei bleiben GPIO14, 15 und 20.

## Pi einrichten

```bash
sudo apt install i2c-tools alsa-utils python3
```

In `/boot/firmware/config.txt` eintragen und neu starten:

```
dtparam=i2c_arm=on
dtparam=i2s=on
dtparam=audio=off
dtoverlay=hifiberry-dac
dtoverlay=gpio-shutdown,gpio_pin=10,active_low=0,gpio_pull=up
dtoverlay=gpio-poweroff,gpiopin=4,active_low=1
```

SPI muss ausgeschaltet bleiben (`dtparam=spi=on` darf nicht aktiv sein), weil GPIO7 bis 11 für Encoder und Verstärker gebraucht werden.

Kontrolle: `i2cdetect -y 1` zeigt `2d` erst, nachdem das Startskript den Verstärker eingeschaltet hat. `aplay -l` zeigt die Karte `sndrpihifiberry`.

Steuerskript, Dienst und ALSA-Einstellung installieren (im Ordner des Repos):

```bash
sudo install -m 755 radio_hat_start.sh /usr/local/bin/
```

```bash
sudo install -m 644 Pi/radio-hat.service /etc/systemd/system/
```

```bash
sudo install -m 644 Pi/asound.conf /etc/asound.conf
```

```bash
sudo systemctl daemon-reload && sudo systemctl enable --now radio-hat.service
```

Der Dienst ruft beim Booten `radio_hat_start.sh start` auf und vor dem Herunterfahren `radio_hat_start.sh stop`. Das Skript hält sich an die Ein- und Abschaltfolge aus dem Datenblatt (Kap. 7.5.3) und

- setzt Schaltfrequenz und Modulation fest (768 kHz, BD) und die passende Regelbandbreite (175 kHz),
- begrenzt die Ausgangsleistung auf etwa 19 W Sinus an 8 Ω (Analogverstärkung 0x09),
- lässt keine Lautstärke über 0 dB zu (Register 0x4C nicht unter 0x30); darüber würde laute Musik übersteuert und die Lautsprecher bekämen bis zu doppelt so viel Leistung,
- setzt einen Hochpass bei 50 Hz (Variable `HOCHPASS_HZ`), damit die kleinen Lautsprecher keinen Bass bekommen, den sie nicht abstrahlen können,
- lässt den Verstärker nach einer Übertemperatur-Abschaltung von selbst wieder anlaufen, sobald er abgekühlt ist,
- schaltet vor dem Herunterfahren erst leise (Rampe), dann die Ausgänge ab und zieht PDN auf low, bevor die Versorgung des Pi wegfällt.

Weitere Aufrufe:

- `sudo radio_hat_start.sh status` zeigt Zustand, erkannte Abtastrate und alle Fehler im Klartext.
- `sudo radio_hat_start.sh clear` löscht gespeicherte Fehler. Nach einem Gleichspannungsfehler am Lautsprecher bleibt der Ausgang aus, bis die Ursache behoben und der Fehler gelöscht ist.
- `sudo radio_hat_start.sh start 0x50` startet mit einer anderen Lautstärke.

Die ALSA-Einstellung `Pi/asound.conf` gibt jede Wiedergabe mit 32 Bit je Kanal aus. Damit läuft der Bittakt immer mit 64 fS und passt zur Voreinstellung des Verstärkers (I²S, 24-Bit-Wörter).

Wer die Lautstärke später aus einem eigenen Programm über Register 0x4C stellt, muss dort ebenfalls bei 0x30 aufhören. Das Skript liest beim Start die gesetzten Register zurück; stehen dort andere Werte, nicht weiter aufdrehen.

Pausen sind kein Problem: Bleibt der I²S-Takt stehen, schaltet der Verstärker die Ausgänge ab und spielt von selbst weiter, sobald der Takt wiederkommt; die Einstellungen bleiben erhalten (Datenblatt Kap. 7.3.4). Nur wenn die 20 V unter 3,5 V fallen, gehen die Einstellungen verloren; dann `radio_hat_start.sh start` erneut ausführen.

## So funktioniert der Schalter

- Schalter ein: Der 5-V-Regler startet, der Pi bootet und hält den Regler danach selbst über GPIO4.
- Schalter aus: GPIO10 geht auf high, der Pi fährt sauber herunter und schaltet am Ende GPIO4 ab. Erst dann geht der Regler aus.
- Wird der Pi per Software heruntergefahren, während der Schalter noch auf Ein steht, bleibt der Regler an. Dann einmal aus- und wieder einschalten.

## Erster Test

1. Pi abziehen, keine Lautsprecher anschließen, Netzteil einstecken, Schalter ein.
2. Am 40-poligen Sockel Pin 2 gegen Pin 6 messen: 4,9 bis 5,2 V. Sonst sofort ausschalten.
3. Spannungsfrei machen, Pi aufstecken, booten. Ist der Dienst eingerichtet, startet der Verstärker von selbst; sonst `sudo radio_hat_start.sh start`. Dann `sudo radio_hat_start.sh status`: Zustand Play, 48 kHz und 64 Bittakte je Abtastung, keine Fehler.
4. Erst dann Lautsprecher anschließen und mit der voreingestellten Lautstärke (−24 dB) probieren.
5. Ohne Musik das Ohr an den Lautsprecher halten, dann bei mittlerer Lautstärke leise Stellen hören: Pfeifen oder Zirpen deutet auf eine Störung durch den 5-V-Regler hin.
6. Wer den Verpolungsschutz prüfen will: ohne Pi und Lautsprecher ein Labornetzteil mit Strombegrenzung (etwa 0,2 A) verpolt anschließen. Es darf kein Strom fließen, am Sockel Pin 2 gegen Pin 6 müssen 0 V anliegen.

Am echten Gerät noch zu prüfen: ob der Hochpass hörbar wirkt (Bass leiser unter etwa 50 Hz). Die Adressen der Klangfilter stehen nicht im Datenblatt, sondern in einer TI-Anwendungsschrift.

## KiCad-Projekt

Im Ordner `KiCad` liegt die Platine als `RadioHAT.kicad_pcb` mit Design-Regeln in `RadioHAT.kicad_pro` und einer Zusatzregel in `RadioHAT.kicad_dru` (Wärmefallen auf der Unterseite, siehe Prüfbericht Änderung 25). Sie wurde aus den Fertigungsdaten vom 8.11.2026 zurückgewonnen, mit allen Netznamen, Bauteilen und Pin-Nummern. Die Dateien im Ordner `JLCPCB` sind aus genau dieser Platine erzeugt.

- Einen Schaltplan gibt es nicht. Änderungen macht man direkt im Platineneditor. „Platine aus Schaltplan aktualisieren“ nicht verwenden.
- Die Datei ist im Format von KiCad 7 gespeichert. KiCad 10 öffnet sie und speichert sie im neuen Format. Nach dem ersten Öffnen einmal die Flächen neu füllen (Taste B) und den DRC starten.
- Der DRC läuft in KiCad 7.0.11 ohne Meldung. Im DRC-Dialog den Abgleich mit dem Schaltplan abgeschaltet lassen. Die Prüfung gegen die Footprint-Bibliothek ist im Projekt abgeschaltet, weil es keine Bibliothek gibt.
- Der Bestückungsdruck besteht aus einzelnen Linien, die Texte sind nicht als Text bearbeitbar. Die Bauteilbezeichner stehen zusätzlich als Text auf der Lage F.Fab.
- Vier Kupferlagen: Oberseite, zwei Masselagen innen (In1.Cu, In2.Cu), Unterseite. In2.Cu ist durchgehend Masse. Auf In1.Cu liegen außer Masse die Doppelbahnen der vier Verstärkerausgänge, ein 4,7 mm langes Stück der 3,3-V-Leitung zwischen den Pins des Sockels und die Leitung HOLD.
- Die vier Masseflächen: Abstand 0,2 mm, Mindestbreite 0,15 mm, SMD-Pads voll angebunden, bedrahtete Pads mit Wärmefallen (Stege 0,5 mm, Spalt 0,3 mm), die 24 Vias im Kühlpad von U1 voll angebunden, Inseln entfernen.
- Um die Befestigungslöcher H1–H4 liegen Sperrflächen mit 6 mm Durchmesser (keine Leiterbahnen, keine Vias; Massefläche erlaubt). TH1–TH3 sind Passbohrungen 1,152 mm für die Bestückung bei JLCPCB.
- Ursprung für Gerber, Bohrdaten und Bestückungsdatei ist die linke untere Platinenecke („Bohr-/Platzierungsursprung verwenden“).

Neue Fertigungsdaten nach einer Änderung:

1. Gerber plotten: F.Cu, In1.Cu, In2.Cu, B.Cu, F.Paste, F.Mask, B.Mask, F.Silkscreen, B.Silkscreen, Edge.Cuts, dazu die Bohrdateien (PTH und NPTH getrennt). Alles in `Gerber_RadioHAT.zip` packen.
2. Bestückungsdatei erzeugen. Das Skript rechnet die Drehwinkel auf die Zählweise von JLCPCB um:

```bash
kicad-cli pcb export pos --format csv --units mm --side front --smd-only --use-drill-file-origin -o pos.csv KiCad/RadioHAT.kicad_pcb
```

```bash
python3 KiCad/jlc_cpl.py pos.csv JLCPCB/CPL_RadioHAT.csv
```

3. Geänderte Bauteilwerte von Hand in `JLCPCB/BOM_RadioHAT.csv` nachtragen.

Schritte 1 und 2 erledigt auch ein Skript, das vorher den DRC mit neu gefüllten Flächen laufen lässt (braucht KiCad 7 mit Python-Anbindung):

```bash
bash KiCad/werkzeuge/fertigungsdaten.sh
```

Weitere Werkzeuge in `KiCad/werkzeuge`:

| Datei | Zweck |
|---|---|
| `verify.py` | misst die Werte aus dem Prüfbericht: Leiterbahnbreiten an den Ausgängen, Abstände der Kondensatoren zu den Pins, 3,3-V-Breite, Vergleich der Netzliste mit einer zweiten Platine. Braucht zusätzlich `shapely`. |
| `drc.py` | DRC auf einer Kopie, mit neu gefüllten Flächen |
| `eingangsschutz.py` | hat am 17.11.2026 den Eingangsschutz (Änderung 17) in die Platine eingebaut; nur zur Nachvollziehbarkeit, nicht erneut ausführen |
| `aenderung_20_21.py`, `aenderung_23.py`, `aenderung_24.py`, `aenderung_25.py` | Änderungen 20 bis 25, ebenso nur zur Nachvollziehbarkeit |
| `bilder.sh` | rendert `Bilder/render_top.png` und `render_bottom.png` aus einem Gerber-Ordner. Braucht Node.js, das npm-Paket `pcb-stackup` und Playwright. |
