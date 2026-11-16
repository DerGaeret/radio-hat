# Prüfbericht Radio HAT (Stand 16.11.2026)

## Was geprüft wurde und was nicht

Im Repository liegen nur die Fertigungsdaten (Gerber, Bohrdateien, BOM, CPL), keine KiCad-Projektdateien (`.kicad_pcb`, `.kicad_sch`). Ein DRC/ERC in KiCad war deshalb nicht möglich. Stattdessen wurde aus den Gerber-Daten die Verdrahtung rekonstruiert (Kupferlagen gerastert mit 50 px/mm, über die Bohrungen verbunden) und gegen README, BOM und CPL geprüft. Das ersetzt keinen KiCad-DRC: Fehler im Schaltplan, die sich im Layout genauso wiederfinden, fallen so nur auf, wenn sie der README oder dem Datenblatt widersprechen.

Ein JLCONE-Projekt wurde nicht angelegt. JLCONE läuft auf dem eigenen Rechner und war aus der Cloud-Sitzung nicht erreichbar.

## Ergebnis in Kürze

Die Fertigungsdaten sind in sich stimmig und bestellbar. Es gibt keinen Verdrahtungsfehler gegenüber der README. Vor der Bestellung sind die Befunde 1, 3 und 4 zu beachten.

## Befunde

| Nr. | Gewicht | Befund | Empfehlung |
|---|---|---|---|
| 1 | hoch | C23 (22 µF, 25 V, Eingang des 5-V-Reglers) liegt direkt an der Netzteilspannung. Die README erlaubt bis 26 V, das liegt über der Nennspannung. Bei 20 V bleibt wegen der Spannungsabhängigkeit von X5R nur ein Bruchteil der 22 µF wirksam. | Entweder die Obergrenze in der README auf 24 V senken oder C23 gegen einen 1206-Typ mit 35 V oder 50 V tauschen (z. B. 10 µF 50 V). |
| 2 | hoch | Der 5-V-Regler TPS54302 liefert höchstens 3 A, die Spule L5 ist für 2,45 A Dauerstrom angegeben (Sättigung 3,5 A). Die README rechnet mit „Pi bis etwa 17 W“, das wären 3,4 A. | Geklärt: Es wird ein Pi 4 verwendet. Das passt, solange keine stromhungrigen USB-Geräte (z. B. Festplatten ohne eigenes Netzteil) am Pi hängen. Für einen Pi 5 unter Last würde der Regler nicht reichen. |
| 3 | mittel | LCSC-Nummer C377117 (680 nF 50 V X7R 1206, C15–C18) ließ sich online nicht bestätigen. | Beim BOM-Abgleich in JLCONE prüfen, ob 680 nF / 50 V / 1206 angezeigt wird. Ersatz: FH 1206B684K500NT (C1881). |
| 4 | mittel | Drehlage von U1, U2, Q1 und D1 in der CPL ist offline nicht prüfbar, weil JLCPCB je Bauteil eine eigene Nulllage hat. Die CPL enthält bereits Korrekturen (U1 und U2 jeweils +270° gegenüber KiCad, Q1 +180°). | In der Bestückungsvorschau von JLCONE die Pin-1-Markierung prüfen: U1 Pin 1 oben rechts, U2 Pin 1 (GND) oben rechts, D1 Kathode unten (zu R8/R9). |
| 5 | niedrig | `radio_hat_start.sh` verwies auf `ANLEITUNG.md`, die Datei heißt `README.md`. | Im Skript korrigiert. |
| 6 | niedrig | C7 (4,7 µF 25 V) sitzt an 3,3 V, C26/C27 (22 µF 25 V) an 5 V. | In Ordnung, keine Änderung. |
| 7 | Hinweis | Um die vier Befestigungslöcher (2,75 mm) reicht die Kupferfläche bis auf 0,2 bis 0,6 mm an den Lochrand. Schraubenköpfe liegen auf lackiertem Kupfer. | Kunststoff-Unterlegscheiben oder Kunststoff-Abstandshalter verwenden. |

## Platine (aus Gerber und Bohrdaten)

| Merkmal | Wert | JLCPCB Standard | Urteil |
|---|---|---|---|
| Größe | 65 × 65 mm, Ecken R 3 mm, 2 Lagen | | in Ordnung |
| Erzeugt mit | KiCad 10.0.7, 8.11.2026 | | |
| Kleinste Leiterbahn | 0,25 mm | ≥ 0,127 mm | in Ordnung |
| Kleinster Kupferabstand | 0,18 mm (gemessen, ±0,02 mm) | ≥ 0,127 mm | in Ordnung |
| Durchkontaktierungen | 166 × 0,3 mm Bohrung / 0,6 mm Pad, 3 × 0,4 / 0,8 mm | ≥ 0,3 / 0,5 mm | in Ordnung |
| Bauteilbohrungen | 0,95 mm (XH-4), 1,0 mm (Sockel, XH-2, Elkos), 1,4 mm (Klemmen) | | in Ordnung |
| Befestigung | 4 × 2,75 mm unbeschichtet, Raster 58 × 49 mm | | passt zum Pi-Lochbild |
| Kupfer zum Platinenrand | > 0,3 mm | ≥ 0,2 mm | in Ordnung |
| Dateien im ZIP | 2 Kupfer, 2 Lötstopp, 2 Bestückungsdruck, Paste oben, Umriss, PTH, NPTH | | vollständig |

Der 40-polige Sockel liegt mittig zwischen den oberen Löchern auf deren Höhe, Pin 1 rechts oben in der äußeren Reihe. Das passt zur um 180° gedrehten Montage aus der README.

## BOM gegen CPL

- 86 Bauteile in der BOM, 86 in der CPL, dieselben Bezeichner, keiner doppelt.
- Alle 204 Lötpasten-Pads liegen auf Bauteilen der CPL. Bei jedem Bauteil stimmt der Mittelpunkt der Pads mit der CPL-Koordinate überein (Abweichung 0,00 mm; Q1 hat bauartbedingt einen unsymmetrischen Pad-Schwerpunkt).
- Ursprung und Y-Richtung von CPL und Gerber sind gleich.
- Lücken in der Nummerierung (C29, C30, R13–R20, R36–R40) sind unkritisch, diese Bezeichner kommen auf der Platine nicht vor.
- Nicht in BOM/CPL und selbst zu löten: J1, J2, J3, J4, C1, C2, S1–S6, X1, E1–E3.

## Verdrahtung gegen README

Alle Angaben der README wurden in den Gerber-Daten wiedergefunden:

- GND an den Pi-Pins 6, 9, 14, 20, 25, 30, 34, 39. 5 V an Pin 2 und 4. 3,3 V von Pin 1 (Encoder-Pull-ups) und Pin 17 (Verstärker-Logik).
- Tasten S1–S6 über 1 kΩ und 10 nF an GPIO17, 27, 22, 23, 24, 25.
- Encoder E1: GPIO5, 6, 12. E2: GPIO13, 16, 26. E3: GPIO11, 8, 7. Jeweils 2,7 kΩ an A/B und 270 Ω am Taster nach 3,3 V.
- I²C an GPIO2/3, I²S an GPIO18 (Takt), 19 (LR), 21 (Daten) über je 33 Ω, PDN an GPIO9 mit 10 kΩ nach GND.
- Schalter: GPIO10 am Kollektor von Q1, GPIO4 über D1 am EN-Eingang des Reglers. Frei: GPIO14, 15, 20 sowie ID-Pins 27/28.
- 5-V-Regler: Spannungsteiler 75 kΩ / 10 kΩ ergibt 5,07 V. EN-Spannung bei 20 V etwa 3,4 V (zulässig bis 7 V).
- TAS5805M: Versorgung, Bootstrap-Kondensatoren (220 nF), Ausgangsfilter (10 µH + 680 nF) und Massepins passen zur Pinbelegung laut Datenblatt-Auszügen. Kanal A geht an J3 „LINKS“, Kanal B an J2 „RECHTS“, Polung wie in der README. Adresswiderstand 15 kΩ nach 3,3 V passt zur Adresse 0x2D im Skript. Die Reihenfolge der Pins 6 bis 12 (I²S, I²C, PDN) konnte nicht aus dem Original-Datenblatt bestätigt werden, die TI-Seite war nicht abrufbar.

## LCSC-Nummern

Quelle: Suchmaschinen-Auszüge der Seiten von LCSC und JLCPCB vom 16.11.2026. Die Seiten selbst waren nicht direkt abrufbar, Lagerbestand und Preise deshalb in JLCONE prüfen.

| LCSC | BOM-Angabe | Gefunden | Urteil |
|---|---|---|---|
| C478472 | TAS5805MPWPR | TI TAS5805MPWPR, HTSSOP-28-EP | passt, Bestand knapp (2.000–3.500) |
| C15849 | 1 µF 50 V X5R 0603 | Samsung CL10A105KB8NNNC | passt |
| C14663 | 100 nF 50 V X7R 0603 | Yageo CC0603KRX7R9BB104, Basic | passt |
| C1779 | 4,7 µF 25 V X5R 0805 | Samsung CL21A475KAQNNNE | passt |
| C21120 | 220 nF 25 V X7R 0603 | Samsung CL10B224KA8NNNC | passt |
| C79272 | 10 µH 3,5 A | Sunlord SWPA6045S100MT, 2,45 A Dauer, 3,5 A Sättigung, Extended | passt, siehe Befund 2 |
| C377117 | 680 nF 50 V X7R 1206 | nicht gefunden | nicht bestätigt, siehe Befund 3 |
| C1588 | 1 nF 50 V X7R 0603 | Samsung CL10B102KB8NNNC, Basic | passt |
| C22809 | 15 kΩ 1 % | Uniroyal 0603WAF1502T5E, Basic | passt |
| C25804 | 10 kΩ 1 % | Uniroyal 0603WAF1002T5E, Basic | passt |
| C23140 | 33 Ω 1 % | Uniroyal 0603WAF330JT5E, Basic | passt |
| C311983 | TPS54302DDCR | TI TPS54302DDCR, TSOT-23-6, Extended | passt |
| C12891 | 22 µF 25 V X5R 1206 | Samsung CL31A226KAHNNNE | passt, siehe Befund 1 |
| C23242 | 75 kΩ 1 % | nicht direkt gefunden (Nachbarnummern derselben Reihe passen) | nicht bestätigt |
| C14858 | 100 pF 50 V C0G | Samsung CL10C101JB8NNNC, Basic | passt |
| C25803 | 100 kΩ 1 % | Uniroyal 0603WAF1003T5E, Basic | passt |
| C23178 | 470 kΩ 1 % | Uniroyal 0603WAF4703T5E | passt |
| C191023 | 1N5819WS | Hottech 1N5819WS, SOD-323, 40 V 1 A, Basic | passt |
| C20526 | MMBT3904 | Changjing MMBT3904, SOT-23, Basic | passt |
| C21190 | 1 kΩ 1 % | Uniroyal 0603WAF1001T5E, Basic | passt |
| C57112 | 10 nF 50 V X7R | FH 0603B103K500NT, Basic | passt |
| C13167 | 2,7 kΩ 1 % | Uniroyal 0603WAF2701T5E, Basic | passt |
| C22966 | 270 Ω 1 % | Uniroyal 0603WAF2700T5E | passt |

## In JLCONE zu prüfen

1. `JLCPCB/Gerber_RadioHAT.zip` hochladen. Erkannte Größe 65 × 65 mm, 2 Lagen.
2. Einstellungen aus der README wählen, dann `BOM_RadioHAT.csv` und `CPL_RadioHAT.csv` hochladen.
3. Im BOM-Abgleich: 23 Zeilen, alle zugeordnet, C377117 und C23242 auf Wert und Bauform prüfen, Bestand von C478472.
4. In der Bestückungsvorschau: Pin 1 von U1, U2, Q1, D1 (Befund 4). Alle Teile müssen deckungsgleich auf ihren Pads sitzen.
