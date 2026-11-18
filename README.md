# Retro-Radio

Holzgehäuse mit Frontplatte und Lautsprecherabdeckungen eines DDR-Radios. Innen ein Raspberry Pi mit dem **Raspberry Pi DigiAMP+** als Verstärker, sechs Tasten, drei Drehgebern und A/E-Schalter.

Bis zum 17.11.2026 war hier eine eigene Verstärkerplatine (Radio HAT, TAS5805M) entworfen. Sie wird nicht gebaut; der DigiAMP+ macht dasselbe. Der letzte Stand liegt in der Git-Geschichte (Commit `c25365f`), zurückholen mit `git checkout c25365f -- KiCad JLCPCB PRUEFBERICHT.md`.

| Datei | Wofür |
|---|---|
| `Pi/asound.conf` | ALSA-Einstellung: Hochpass 50 Hz vor dem DigiAMP+ |
| `Gehaeuse/` | Holzgehäuse: 3D-Modell, Maßzeichnungen, Zuschnittliste, Druckteile |

Quellen: [Produktseite](https://www.raspberrypi.com/products/digiamp-plus/), [Doku](https://www.raspberrypi.com/documentation/accessories/audio.html), [pinout.xyz](https://pinout.xyz/pinout/pi_digiamp), Overlay-Beschreibung und Treiber im Raspberry-Pi-Kernel (`overlays/README`, `sound/soc/bcm/iqaudio-dac.c`).

## DigiAMP+ in Kürze

- Verstärker TI TAS5756M (DAC und Endstufe in einem Chip, I²C-Adresse 0x4C), bis 2 × 35 W laut Produktseite. Zwei Schraubklemmen für passive Lautsprecher. Mit Blick von oben und der Netzbuchse links: links „−“, rechts „+“, an beiden Klemmen gleich.
- Versorgung 12 bis 24 V Gleichspannung über Hohlbuchse 5,5 × 2,5 mm. Alternativ fest verdrahtet an P5 (Polung beachten).
- Versorgt den Pi über den GPIO-Stecker mit 5,1 V, 2,5 A. **Den Pi nie zusätzlich über seinen eigenen USB-C-Anschluss versorgen.**
- Belegt GPIO2/3 (I²C), GPIO18 bis 21 (I²S), GPIO22 (Stummschaltung und Mute-LED), dazu GPIO0/1 für das HAT-EEPROM.
- 58 × 65 mm, steckt direkt auf dem Pi, Befestigung mit den mitgelieferten Abstandsbolzen auf den vier Pi-Löchern. Der GPIO-Stecker wird nach oben durchgeführt.
- Startet stummgeschaltet (Mute-LED leuchtet). Der Treiber schaltet beim Abspielen ein und 5 s nach dem Ende wieder stumm.
- Betrieb 0 bis 50 °C.

## Welcher Pi

Die Doku schreibt, der DigiAMP+ sei für Pi 3 und älter ausgelegt. Ein Pi 4 geht, solange an seinen USB-Buchsen nichts Stromhungriges hängt; sonst einen USB-Hub mit eigenem Netzteil nehmen. Ein Pi 5 bekommt mit 2,5 A nur eingeschränkte USB-Leistung und ist nicht zu empfehlen. Ein RP2040-Zero für die LED-Skala (etwa 0,4 A bei 10 % Helligkeit) liegt beim Pi 4 noch im Rahmen.

## Netzteil

- Raspberry Pi empfiehlt das XP Power VEC65US19 (19 V, 65 W). Ein geregeltes Netzteil mit **19 oder 20 V, mindestens 3 A** und Hohlstecker 5,5 × 2,5 mm passt.
- Nicht mehr als 20 V: Die Lautsprecher (Sharp VSP0010PBS78A) haben 8 Ω und vertragen höchstens 20 W. Die Brückenendstufe schafft an 8 Ω höchstens etwa U² / 16 Ω ohne Verluste, also bei 19 V etwa 22 W, real knapp 20 W vor dem Übersteuern; bei 24 V wären es über 30 W. Wer ein 24-V-Netzteil nimmt, darf „Digital“ nie über −3 dB stellen.
- Die Polung des Hohlsteckers nennt die Doku nicht. Vor dem ersten Einstecken auf dem Netzteil-Aufdruck prüfen (üblich: Mitte +).
- Im Gehäuse sitzt die Netzbuchse im Rückwanddeckel. Entweder eine Einbaubuchse 5,5 × 2,5 mm mit zwei Litzen an P5 (Polung!) oder ein kurzes Verlängerungskabel Buchse/Stecker 5,5 × 2,5 mm zur Hohlbuchse des DigiAMP+.

## Anschlüsse an den Pi

Tasten, Drehgeber und A/E-Schalter kommen mit Dupont-Kabeln (Buchse) an den durchgeführten GPIO-Stecker oben auf dem DigiAMP+. Alle schalten gegen GND.

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
| A/E-Schalter | GPIO10 | 19 |
| 3,3 V für die Pull-ups der Drehgeber | – | 1 oder 17 |
| GND | – | 6, 9, 14, 20, 25, 30, 34, 39 |

Frei bleiben GPIO9, 14 und 15 (GPIO9 nur, solange SPI aus ist).

- **Tasten (Cherry MX Blue):** Pull-ups im Pi, in der Software einschalten, 20 ms entprellen.
- **Drehgeber (ALPS STEC11B):** Der Drehgeber verlangt laut Datenblatt mindestens 1 mA an A/B und 10 mA am Taster; die Pull-ups im Pi (etwa 50 kΩ) liefern nur rund 0,07 mA. Deshalb auf jede Lochrasterplatine der Drehgeber (siehe `Gehaeuse/DRUCKTEILE.md`) drei Widerstände löten: 2,7 kΩ von A und von B nach 3,3 V (1,2 mA), 270 Ω vom Taster nach 3,3 V (12 mA). Pin C und ein Tasterkontakt an GND. Pro Drehgeber ein Kabel mit 5 Adern: A, B, Taster, 3,3 V, GND.
- **A/E-Schalter:** rastend, zwischen GPIO10 und GND. Geschlossen = Ein. Öffnen fährt den Pi herunter (siehe unten, Ein/Aus ist noch offen).

## Pi einrichten

Den DigiAMP+ aufstecken und verschrauben, Lautsprecher anklemmen, Netzteil einstecken. Der Pi startet mit.

Erkennung prüfen:

```bash
grep -a . /proc/device-tree/hat/*
```

Bei der grünen Raspberry-Pi-Ausführung steht dort „Raspberry Pi Ltd.“. Das HAT-EEPROM lädt den Treiber dann von selbst. Nur wenn nichts erkannt wird, in `/boot/firmware/config.txt` eintragen:

```
dtoverlay=
dtoverlay=rpi-digiampplus
```

(Schwarze IQaudIO-Ausführung: `dtoverlay=iqaudio-dacplus,auto_mute_amp`.)

Außerdem in `/boot/firmware/config.txt`:

```
dtparam=audio=off
dtoverlay=gpio-shutdown,gpio_pin=10,active_low=0,gpio_pull=up
dtoverlay=rotary-encoder,pin_a=5,pin_b=6,relative_axis=1,steps-per-period=2
dtoverlay=rotary-encoder,pin_a=13,pin_b=16,relative_axis=1,steps-per-period=2
dtoverlay=rotary-encoder,pin_a=11,pin_b=8,relative_axis=1,steps-per-period=2
```

und die vorhandene Zeile `dtoverlay=vc4-kms-v3d` zu `dtoverlay=vc4-kms-v3d,noaudio` ändern. Dann ist der DigiAMP+ die einzige Soundkarte (Karte 0).

- `24db_digital_gain` **nicht** setzen. Ohne diesen Schalter lässt der Treiber die Lautstärke („Digital“) höchstens bis 0 dB zu; darüber würde laute Musik übersteuert.
- SPI ausgeschaltet lassen (`dtparam=spi=on` darf nicht aktiv sein), weil GPIO7, 8 und 11 für Drehgeber 3 gebraucht werden.
- Die alten Einträge `dtoverlay=hifiberry-dac` und `dtoverlay=gpio-poweroff,gpiopin=4,…` der eigenen Platine dürfen nicht mehr drinstehen; GPIO4 ist jetzt Taste 3.
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

## Ein/Aus (noch offen)

Die eigene Platine hatte eine Selbsthaltung: Schalter aus → Pi fährt herunter → erst dann geht der Strom weg. Der DigiAMP+ hat das nicht. Mit dem Eintrag oben fährt der Pi beim Öffnen des A/E-Schalters sauber herunter, bleibt danach aber mit Strom versorgt (Verstärker stumm). Wieder einschalten geht dann nur, indem man das Netzteil kurz trennt. Möglichkeiten:

1. Netzteil an einer schaltbaren Steckdosenleiste, A/E-Schalter nur zum Herunterfahren.
2. Kleine Selbsthaltung in der 19-V-Leitung auf Lochraster (P-MOSFET, gehalten über `gpio-poweroff` an GPIO9), wie früher auf der eigenen Platine.
3. Taster statt Schalter an GPIO3: Ein heruntergefahrener Pi startet, wenn GPIO3 auf GND gezogen wird. GPIO3 ist aber zugleich die I²C-Taktleitung zum Verstärker; ein Druck während des Betriebs kann eine Lautstärkeänderung stören.

## Erster Test

1. Lautsprecher abklemmen, DigiAMP+ auf den Pi, Netzteil einstecken. Power-LED an, Mute-LED an.
2. Pi bootet. `aplay -l` zeigt „RPi DigiAMP+“.
3. Lautsprecher anklemmen. `speaker-test -c 2 -t wav` spielt abwechselnd links und rechts; die Mute-LED geht beim Abspielen aus.
4. Hochpass prüfen: `speaker-test -c 2 -t sine -f 30` muss deutlich leiser sein als `-f 100`.
5. Ohne Musik das Ohr an den Lautsprecher halten: kein Brummen oder Zirpen.
6. A/E-Schalter öffnen: Der Pi fährt herunter.
