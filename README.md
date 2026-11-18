# Retro-Radio

Holzgehäuse mit Frontplatte und Lautsprecherabdeckungen eines DDR-Radios. Innen ein Raspberry Pi mit dem **Raspberry Pi DigiAMP+** als Verstärker, sechs Tasten, drei Drehgebern und A/E-Schalter.

Bis zum 17.11.2026 war hier eine eigene Verstärkerplatine (Radio HAT, TAS5805M) entworfen. Sie wird nicht gebaut; der DigiAMP+ macht dasselbe. Der letzte Stand liegt in der Git-Geschichte (Commit `c25365f`), zurückholen mit `git checkout c25365f -- KiCad JLCPCB PRUEFBERICHT.md`.

| Datei | Wofür |
|---|---|
| `Pi/asound.conf` | ALSA-Einstellung: Hochpass 50 Hz vor dem DigiAMP+ |
| `Bilder/digiamp_plus.jpg` | Lageplan des DigiAMP+ aus der Raspberry-Pi-Doku |
| `Gehaeuse/` | Holzgehäuse: 3D-Modell, Maßzeichnungen, Zuschnittliste, Druckteile |

Quellen: [Produktseite](https://www.raspberrypi.com/products/digiamp-plus/), [Doku](https://www.raspberrypi.com/documentation/accessories/audio.html), [pinout.xyz](https://pinout.xyz/pinout/pi_digiamp), Overlay-Beschreibung und Treiber im Raspberry-Pi-Kernel (`overlays/README`, `sound/soc/bcm/iqaudio-dac.c`).

## DigiAMP+ in Kürze

- Verstärker TI TAS5756M (DAC und Endstufe in einem Chip, I²C-Adresse 0x4C), bis 2 × 35 W laut Produktseite. Zwei Schraubklemmen für passive Lautsprecher. Mit Blick von oben und der Netzbuchse links: links „−“, rechts „+“, an beiden Klemmen gleich.
- Versorgung 12 bis 24 V Gleichspannung, 3 A, über Hohlbuchse 5,5 × 2,5 mm (Stecker 2,5 mm innen, 5,5 mm außen, 11 mm lang). Alternativ fest verdrahtet an P5 (Polung beachten).
- Versorgt den Pi über den GPIO-Stecker mit 5,1 V, 2,5 A. **Den Pi nie zusätzlich über seinen eigenen USB-C-Anschluss versorgen.**
- Belegt GPIO2/3 (I²C), GPIO18 bis 21 (I²S), GPIO22 (Stummschaltung und Mute-LED), dazu GPIO0/1 für das HAT-EEPROM.
- 58 × 65 mm, steckt direkt auf dem Pi, Befestigung mit den mitgelieferten Abstandsbolzen auf den vier Pi-Löchern. Der GPIO-Stecker wird nach oben durchgeführt.
- Startet stummgeschaltet (Mute-LED leuchtet). Der Treiber schaltet beim Abspielen ein und 5 s nach dem Ende wieder stumm.
- Betrieb 0 bis 50 °C.
- Lage (Bild in der Doku, GPIO-Stecker oben): Hohlbuchse links unten an der Kante gegenüber dem GPIO-Stecker, rechts daneben die Klemmen LEFT und RIGHT, ganz links P5 (2 Pins, „−“ „+“). Diese Kante liegt über der USB-C/HDMI-Seite des Pi; die Hohlbuchse sitzt auf der Seite von Pin 1 (SD-Karten-Ende).

![DigiAMP+](Bilder/digiamp_plus.jpg)

Bild: Raspberry Pi Ltd., Dokumentation (github.com/raspberrypi/documentation), CC BY-SA 4.0.

## Pi

Raspberry Pi 4B. Die Doku schreibt, der DigiAMP+ sei für Pi 3 und älter ausgelegt; am Pi 4 soll stromhungriges USB-Zubehör an einen USB-Hub mit eigenem Netzteil, sonst kommt die Unterspannungswarnung. Tastatur, USB-Stick oder der RP2040-Zero für die LED-Skala (etwa 0,4 A bei 10 % Helligkeit) gehen direkt. Der USB-C-Anschluss des Pi bleibt immer frei.

## Netzteil (kaufen)

Gesucht ist ein geregeltes Steckernetzteil (Tischnetzteil wie bei Laptops):

| Merkmal | Wert |
|---|---|
| Spannung | **19 V** (20 V geht auch) |
| Strom | mindestens 3,42 A (65 W) |
| Stecker | Hohlstecker 5,5 × 2,5 mm, Mitte Plus |
| Art | geregeltes Schaltnetzteil, CE-Zeichen |

Empfehlung von Raspberry Pi: **XP Power VEC65US19** (19 V, 3,42 A, 65 W, Stecker 5,5 × 2,5 × 11 mm Mitte Plus, Eingang 90–264 V). Das Netzkabel wird laut Händlern separat verkauft; vor dem Kauf nachsehen, welche Buchse das Netzteil hat (C6, C8 oder C14), und das passende Kabel mit Euro- bzw. Schukostecker mitbestellen. Ein gleichwertiges 19-V-Laptopnetzteil mit 5,5 × 2,5 mm tut es genauso.

Warum 19 V und nicht 24 V: Die Lautsprecher (Sharp VSP0010PBS78A) haben 8 Ω und vertragen höchstens 20 W. Die Brückenendstufe schafft an 8 Ω höchstens etwa U² / 16 Ω ohne Verluste, bei 19 V also etwa 22 W, real knapp 20 W vor dem Übersteuern; bei 24 V wären es über 30 W. 12 V würde gehen, gibt aber nur etwa 8 W.

## Stromweg und A/E-Schalter

Das Netzteil wird hinten am Radio eingesteckt, nicht direkt am DigiAMP+. Der A/E-Schalter trennt die 19 V hart:

```
Netzteil → Einbaubuchse im Rückwanddeckel → A/E-Schalter (Plusleitung) → Kabel mit Hohlstecker → Hohlbuchse DigiAMP+
                                   └────────────── Minusleitung ──────────────┘
```

- **Einbaubuchse:** Hohlbuchse 5,5 × 2,5 mm zum Einschrauben (Gewinde M8, im Modell ist dafür ein Loch Ø 8 mm im Rückwanddeckel vorgesehen; Lochmaß an der gekauften Buchse prüfen), mit Lötanschlüssen.
- **Zum DigiAMP+:** ein DC-Kabel mit Hohlstecker 5,5 × 2,5 mm und offenem Ende (etwa 50 cm, mindestens 0,5 mm², besser 0,75 mm²). Der Hohlstecker steckt in der Buchse des DigiAMP+. Alternativ die zwei Adern direkt an P5 löten; dann auf den Aufdruck „−“ und „+“ achten.
- **A/E-Schalter:** in die Plusleitung (Mitte des Steckers). Er muss Gleichstrom schalten können: **mindestens 4 A bei 24 V DC** (nicht nur AC-Angabe lesen; viele Poti-Schalter können nur 0,5 bis 2 A). Bauteil noch offen (Gehäuse, offene Frage 2).
- Polung an der Einbaubuchse: Mittelstift = Plus. Vor dem ersten Einschalten ohne Pi mit dem Messgerät an der Hohlbuchse des Kabels nachmessen: innen +19 V.

**Hartes Ausschalten und die SD-Karte:** Der Pi wird ohne Herunterfahren abgeschaltet. Das verträgt das Linux-Dateisystem auf der SD-Karte auf Dauer schlecht. Deshalb nach der Einrichtung das Overlay-Dateisystem einschalten (`sudo raspi-config` → Performance Options → Overlay File System → Ja, Boot-Partition schreibgeschützt → Ja). Dann schreibt der Pi nichts mehr auf die Karte, alle Änderungen gehen beim Ausschalten verloren. Vorher alles fertig einrichten und die Lautstärke speichern; für spätere Änderungen das Overlay vorübergehend wieder ausschalten. Gespeicherte Senderwahl oder Lautstärke nach dem Ausschalten bräuchte dann einen eigenen beschreibbaren Bereich (z. B. zweite Partition); das kann später kommen.

## Einkaufsliste Elektronik

- Raspberry Pi 4B mit microSD-Karte (16 GB oder mehr)
- Raspberry Pi DigiAMP+ (grün)
- Netzteil 19 V, mindestens 3,42 A, Hohlstecker 5,5 × 2,5 mm Mitte Plus (siehe oben), dazu Netzkabel
- Einbau-Hohlbuchse 5,5 × 2,5 mm zum Einschrauben, Lötanschluss
- DC-Kabel mit Hohlstecker 5,5 × 2,5 mm, offenes Ende, etwa 50 cm, 0,75 mm²
- A/E-Schalter, mindestens 4 A bei 24 V DC
- Lautsprecherkabel 2 × 0,75 mm², etwa 2 × 40 cm
- Dupont-Kabel Buchse (für den GPIO-Stecker), Lochraster, Widerstände 6 × 2,7 kΩ und 3 × 270 Ω (je 0,25 W)

## Anschlüsse an den Pi

Tasten und Drehgeber kommen mit Dupont-Kabeln (Buchse) an den durchgeführten GPIO-Stecker oben auf dem DigiAMP+. Alle schalten gegen GND.

| Bauteil | GPIO | Pin am Stecker |
|---|---|---|
| Taste 1 | GPIO17 | 11 |
| Taste 2 | GPIO27 | 13 |
| Taste 3 | GPIO4 (früher GPIO22, das braucht jetzt der DigiAMP+) | 7 |
| Taste 4 | GPIO23 | 16 |
| Taste 5 | GPIO24 | 18 |
| Taste 6 | GPIO25 | 22 |
| Drehgeber 1 (A, B, Taster) | GPIO5, GPIO6, GPIO12 | 29, 31, 32 |
| Drehgeber 2 (A, B, Taster) | GPIO13, GPIO16, GPIO26 | 33, 36, 37 |
| Drehgeber 3 (A, B, Taster) | GPIO11, GPIO8, GPIO7 | 23, 24, 26 |
| 3,3 V für die Pull-ups der Drehgeber | – | 1 oder 17 |
| GND | – | 6, 9, 14, 20, 25, 30, 34, 39 |

Frei bleiben GPIO9, 10, 14 und 15 (GPIO9 und 10 nur, solange SPI aus ist).

- **Tasten (Cherry MX Blue):** Pull-ups im Pi, in der Software einschalten, 20 ms entprellen.
- **Drehgeber (ALPS STEC11B):** Der Drehgeber verlangt laut Datenblatt mindestens 1 mA an A/B und 10 mA am Taster; die Pull-ups im Pi (etwa 50 kΩ) liefern nur rund 0,07 mA. Deshalb auf jede Lochrasterplatine der Drehgeber (siehe `Gehaeuse/DRUCKTEILE.md`) drei Widerstände löten: 2,7 kΩ von A und von B nach 3,3 V (1,2 mA), 270 Ω vom Taster nach 3,3 V (12 mA). Pin C und ein Tasterkontakt an GND. Pro Drehgeber ein Kabel mit 5 Adern: A, B, Taster, 3,3 V, GND.

## Pi einrichten

Den DigiAMP+ (grüne Ausführung) aufstecken und verschrauben, Lautsprecher anklemmen, Strom ein. Der Pi startet mit.

Erkennung prüfen:

```bash
grep -a . /proc/device-tree/hat/*
```

Dort muss „Raspberry Pi Ltd.“ stehen. Das HAT-EEPROM lädt den Treiber dann von selbst. Nur wenn nichts erkannt wird, in `/boot/firmware/config.txt` eintragen:

```
dtoverlay=
dtoverlay=rpi-digiampplus
```

Außerdem in `/boot/firmware/config.txt`:

```
dtparam=audio=off
dtoverlay=rotary-encoder,pin_a=5,pin_b=6,relative_axis=1,steps-per-period=2
dtoverlay=rotary-encoder,pin_a=13,pin_b=16,relative_axis=1,steps-per-period=2
dtoverlay=rotary-encoder,pin_a=11,pin_b=8,relative_axis=1,steps-per-period=2
```

und die vorhandene Zeile `dtoverlay=vc4-kms-v3d` zu `dtoverlay=vc4-kms-v3d,noaudio` ändern. Dann ist der DigiAMP+ die einzige Soundkarte (Karte 0).

- `24db_digital_gain` **nicht** setzen. Ohne diesen Schalter lässt der Treiber die Lautstärke („Digital“) höchstens bis 0 dB zu; darüber würde laute Musik übersteuert.
- SPI ausgeschaltet lassen (`dtparam=spi=on` darf nicht aktiv sein), weil GPIO7, 8 und 11 für Drehgeber 3 gebraucht werden.
- Kein `gpio-shutdown` und kein `gpio-poweroff`: Der A/E-Schalter trennt den Strom direkt.
- Die alten Einträge der eigenen Platine (`hifiberry-dac`, `gpio-shutdown`, `gpio-poweroff`) dürfen nicht mehr drinstehen; GPIO4 ist jetzt Taste 3.
- Beim Drehgeber ergeben zwei Rastungen einen vollen Impulszyklus, daher `steps-per-period=2`. Stimmt die Drehrichtung nicht, A und B tauschen.

Neu starten und prüfen:

```bash
aplay -l
```

zeigt Karte 0 „RPi DigiAMP+“.

Hochpass einrichten (optional, empfohlen für die kleinen Lautsprecher):

```bash
sudo apt install libasound2-plugins swh-plugins alsa-utils
```

```bash
sudo install -m 644 Pi/asound.conf /etc/asound.conf
```

Grundlautstärke setzen und speichern:

```bash
amixer -c 0 sset Digital -- -24dB
```

```bash
sudo alsactl store
```

Eigene Programme stellen die Lautstärke über das ALSA-Element „Digital“ ein (in MPD: `mixer_type "hardware"`, `mixer_control "Digital"`).

## Erster Test

1. Ohne Pi und DigiAMP+: Netzteil hinten einstecken, A/E ein, am Hohlstecker des Innenkabels messen: innen +19 V, außen Minus. A/E aus: 0 V.
2. Lautsprecher abklemmen, DigiAMP+ auf den Pi, Hohlstecker einstecken, A/E ein. Power-LED an, Mute-LED an.
3. Pi bootet. `aplay -l` zeigt „RPi DigiAMP+“.
4. Lautsprecher anklemmen. `speaker-test -c 2 -t wav` spielt abwechselnd links und rechts; die Mute-LED geht beim Abspielen aus.
5. Hochpass prüfen: `speaker-test -c 2 -t sine -f 30` muss deutlich leiser sein als `-f 100`.
6. Ohne Musik das Ohr an den Lautsprecher halten: kein Brummen oder Zirpen.
7. Zum Schluss Overlay-Dateisystem einschalten (siehe „Stromweg und A/E-Schalter“).
