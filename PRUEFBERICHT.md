# Prüfbericht Radio HAT (Stand 17.11.2026, neunte Fassung: Kühlfläche unter U1 nach dem TI-Land-Pattern)

## Was gemacht wurde

1. Aus den Gerber- und Bohrdaten wurde die KiCad-Platine rekonstruiert (`KiCad/RadioHAT.kicad_pcb`). Die Gerber-Dateien enthielten die originalen Netznamen, Bauteilbezeichner und Pin-Nummern, die Rekonstruktion beruht also nicht auf Schätzungen.
2. Die rekonstruierte Platine wurde in KiCad geprüft (DRC) und gegen das Datenblatt des TAS5805M abgeglichen.
3. Drei kleine Korrekturen am Layout, eine an der Bestückungsdatei und eine an der Stückliste (siehe „Änderungen“). Die Fertigungsdaten im Ordner `JLCPCB` sind aus der korrigierten KiCad-Platine neu erzeugt.
4. Die Platine wurde auf vier Lagen umgestellt, damit sie den Layoutregeln von TI (SLAA902) folgt: zwei Masselagen innen, breitere und doppelt geführte Ausgänge, Stützkondensatoren näher an den Pins (Änderungen 9 bis 12). Die Bauteile, die Stückliste und alle Leiterbahnen der Unterseite sind dabei unverändert geblieben.
5. In der fünften Fassung wurden die verbliebenen Abweichungen von SLAA902 behoben (Änderungen 13 bis 16): Die vier Bootstrap-Kondensatoren sind jetzt 0402-Bauteile direkt unter ihren Pins, alle Ausgänge sind ab 0,55 mm unter dem Pin mindestens 0,78 mm breit, die inneren Ausgänge laufen zusätzlich auf Innenlage 1, und die 3,3-V-Zuleitung ist breiter. Danach wurde alles erneut geprüft (Abschnitt „Prüfung nach TI SLAA902, PCBWay und Analog Devices“). Der Artikel von Analog Devices liegt jetzt als PDF vor und ist vollständig ausgewertet.

6. In der sechsten Fassung wurde eine Rückmeldung von außen abgearbeitet (Abschnitt „Rückmeldung vom 17.11.2026“): Eingangsschutz an J4 (Änderung 17), 5-V-Regler TPS54308 statt TPS54302 (Änderung 18), Startskript mit fester Schaltfrequenz, Lautstärkegrenze und Hochpass (Änderung 19). Danach wurde alles erneut geprüft.

7. In der siebten Fassung wurde alles gegen das vollständige Datenblatt des TAS5805M (SLASEH5D, Rev. D, als PDF vom Nutzer) geprüft. Der Text des Datenblatts steht jetzt in `Datenblaetter/TAS5805M.md`, mit Zusammenfassung und Abgleich (Abschnitt 1.11 dort). Daraus folgten die Änderungen 20 bis 22: je Seite ein 10-µF-Keramikkondensator an PVDD, Lötpaste unter dem Kühlpad als Raster, Abschaltfolge und Fehlerauswertung in der Software.

8. In der achten Fassung wurden beide Datenblätter (TAS5805M und TPS54308, als PDF vom Nutzer) vollständig gelesen, einschließlich aller Bilder. Text und Bildinhalte stehen in `Datenblaetter/TAS5805M.md` und `Datenblaetter/TPS54308.md`. Daraus folgte Änderung 23 (R14 in Reihe zum Vorkopplungskondensator des 5-V-Reglers). Der Nutzer hat entschieden, dass es keinen Rückspeiseschutz gibt: Am Pi wird nie ein USB-Netzteil angesteckt.

9. In der neunten Fassung wurde auf Wunsch des Nutzers die Kühlfläche unter U1 auf das Land Pattern von TI vergrößert (Änderung 24): 3,4 × 9,7 mm Kupfer und 24 Durchkontaktierungen. Dafür sind HOLD, GPIO12, GPIO6 und GPIO7 neu verlegt; unter U1 läuft auf keiner Lage mehr eine Signalleitung. Die Platine bleibt 65 × 65 mm (Begründung bei Änderung 24), die Analogverstärkung bleibt 0x09.

Nicht gemacht: Es gibt keinen Schaltplan (`.kicad_sch`), nur die Platine mit Netzliste. Ein JLCONE-Projekt wurde nicht angelegt, JLCONE läuft auf dem eigenen Rechner. Die Platine ist weiterhin ungetestet.

## Wie sicher ist die Rekonstruktion?

| Prüfung | Ergebnis |
|---|---|
| Unveränderte Rekonstruktion wieder als Gerber exportiert und Objekt für Objekt mit den Originalen verglichen (Pads mit Bezeichner, Pin und Netz, Leiterbahnen mit Netz, Masseflächen, Lötstopp, Paste, Bestückungsdruck, Umriss, alle Bohrungen) | identisch, 0 Abweichungen in 3.678 Objekten und 249 Bohrungen |
| Masseflächen in KiCad neu gefüllt und mit der Originalfüllung verglichen | deckungsgleich (Abweichungen unter 0,02 mm²) |
| Aus der Platine erzeugte Bestückungsdatei gegen die bisherige CPL | alle 86 Zeilen gleich bis auf die gewollte Korrektur bei U2; seit der vierten Fassung zusätzlich C8, C9, C10 und R1 (Änderung 12), seit der fünften C11 bis C14 (Änderung 13) |
| DRC der korrigierten Platine in KiCad 7.0.11 | 0 Meldungen, 0 unverbundene Pads, auch nach erneutem Füllen der Flächen. Die Prüfung „Footprint weicht von der Bibliothek ab“ ist im Projekt abgeschaltet, weil es zu dieser Platine keine Footprint-Bibliothek gibt. |

Geprüft wurde mit KiCad 7.0.11, weil hier keine neuere Version verfügbar war. Die Datei lässt sich in KiCad 10 öffnen und wird dabei ins neue Format übernommen. Nach dem ersten Öffnen in KiCad 10 einmal die Flächen neu füllen (Taste B) und den DRC laufen lassen, weil KiCad 10 Flächen geringfügig anders berechnet und zusätzliche Prüfungen kennt, die hier nicht getestet werden konnten. Im DRC-Dialog den Abgleich mit dem Schaltplan abgeschaltet lassen, es gibt keinen Schaltplan.

## Änderungen gegenüber dem Stand vom 8.11.2026

| Nr. | Was | Vorher | Nachher | Grund |
|---|---|---|---|---|
| 1 | Drehlage U2 (TPS54302) in der CPL | 180° | 90° | Laut der Korrekturtabelle von KiBot gilt für TSOT-23 bei JLCPCB dieselbe Korrektur wie für SOT-23 (+180°), nicht die für SOIC/TSSOP (+270°). Die Tabelle selbst merkt an, dass JLCPCB die Zählweise über die Zeit geändert hat. Deshalb in der Vorschau prüfen. |
| 2 | C23, Eingangskondensator des 5-V-Reglers | 22 µF 25 V (C12891) | 10 µF 50 V X5R 1206 (C13585, Samsung CL31A106KBHNNNE, Basic) | C23 liegt an der Netzteilspannung, die README erlaubt bis 26 V. |
| 3 | Zwei doppelt gesetzte GND-Durchkontaktierungen bei C9 und C10 | je zwei Bohrungen 0,025 mm und 0,225 mm nebeneinander, überlappend | je eine | Überlappende Bohrungen sind ein Fertigungsfehler (DRC „hole_near_hole“). |
| 4 | Zwei GND-Durchkontaktierungen zwischen C5 und C6 | beide in der Lücke zwischen den Pads, Steg zwischen den Bohrungen 0,10 mm | eine rechts von C5 (um 0,05 mm verschoben), die zweite links von C5 | Mindestabstand Bohrung zu Bohrung 0,25 mm. Die Anordnung ist jetzt spiegelbildlich zu C3/C4 auf der anderen Seite; jeder Stützkondensator behält seine eigene Durchkontaktierung zur Massefläche. |
| 5 | GND-Durchkontaktierung bei C7 | Steg zur Nachbarbohrung 0,21 mm | 0,33 mm | Um 0,1 mm verschoben, die Bohrung bleibt außerhalb des Pads von C7. |
| 6 | Lötpaste unter dem Kühlpad von U1 | 3,5 × 1,9 mm (53 % der Padfläche) | 3,65 × 2,6 mm (76 %) | Das Datenblatt verlangt 70 bis 80 % Pastenfläche unter dem Kühlpad. |
| 7 | Bestückungsdruck | Beschriftungen E1 und E2 ragten über den Platinenrand, E3 und X1 lagen auf Pads, 15 Umrisslinien liefen in Pads hinein (17 DRC-Meldungen) | E1 und E2 stehen jetzt innerhalb ihres Steckerumrisses, E3 rechts neben R35, X1 unterhalb des Steckers; die Umrisslinien enden vor den Pads | Damit ist der DRC ohne Meldung. E1 und E2 werden vom eingelöteten Stecker verdeckt, die Zuordnung steht auch in der README. |
| 8 | Ausgangsleitungen vom Verstärker zu den Spulen | 0,4 mm am Pin, dann 0,5 bis 0,6 mm | 0,45 mm am Pin (Padbreite), dann 0,6 bis 0,8 mm, die inneren Ausgänge 0,7 mm | TI SLAA902 verlangt für Class-D-Ausgänge mindestens 30 mil (0,76 mm). Am Pin geht wegen des Rasters von 0,65 mm nicht mehr. |
| 9 | Lagenzahl | 2 Lagen | 4 Lagen. Innenlage 1 und Innenlage 2 sind durchgehende Masseflächen (damals 3.738 und 3.758 mm², nach den Änderungen 13 bis 16 noch 3.712 und 3.747 mm², nach Änderung 17 3.710 und 3.745 mm² von rund 4.217 mm², jeweils ein zusammenhängendes Stück) | TI SLAA902 verlangt vier bis sechs Lagen und eine eigene Masselage direkt unter dem Baustein. Damit liegen zwischen den schaltenden Leitungen der Oberseite und den Signalen der Unterseite zwei Masseflächen, und der Schlitz in der Masse der Unterseite spielt keine Rolle mehr. |
| 10 | Ausgangsleitungen (ersetzt Änderung 8) | 0,45 mm am Pin, dann 0,6 bis 0,8 mm | Jedes Stück so breit, wie 0,2 mm Abstand zum Nachbarkupfer es erlauben, höchstens 1,5 mm. Äußere Ausgänge: 3 mm mit 0,45 bis 0,6 mm zwischen den Pins und an C11/C14 vorbei, dann 0,8 bis 1,5 mm. Innere Ausgänge: 4,9 mm mit 0,45 bis 0,55 mm, 1,2 mm mit 0,75 mm, dann 0,85 bis 1,5 mm. Nach den Spulen bis zu den Klemmen 1,45 bis 1,5 mm (bei SPKB+ 1,5 mm lang 0,9 bis 1,05 mm) | TI SLAA902: mindestens 30 mil (0,76 mm), wirksam 60 mil (1,5 mm) bis zum Lautsprecher. |
| 11 | Zweite Bahn für die äußeren Ausgänge | nur Oberseite | OUTB+ und OUTA+ laufen zusätzlich auf Innenlage 1: 1,2 mm breit, 7,3 mm und 6,1 mm lang, an beiden Enden mit je zwei Durchkontaktierungen 0,3/0,6 mm an die Oberseite gebunden (8 neue Durchkontaktierungen). Alle bedrahteten Pads und die acht Durchkontaktierungen im Kühlpad von U1 sind jetzt auch an die Innenlagen angebunden. | TI SLAA902: Ausgänge auf zwei Lagen. Innenlage 2 bleibt darunter geschlossene Masse und schirmt die Signale der Unterseite ab. |
| 12 | Stützkondensatoren der kleinen Versorgungen | C8 (3,3 V) 1,7 mm vom Pin und über zwei Durchkontaktierungen angeschlossen, C10 (VR_DIG) 1,1 mm, C9 (AVDD) 1,8 mm | C8 sitzt jetzt am Platz von R1, 0,65 mm vom Pin, direkt auf der Oberseite angeschlossen, Masse auf kurzem Weg zum Massepin 1. C10 um 0,4 mm an den Pin gerückt (0,73 mm). C9 quer vor Pin 13 gedreht (0,48 mm), mit eigener GND-Durchkontaktierung 0,4 mm neben dem Pad. R1 sitzt am alten Platz von C8. Zwei dadurch überflüssige GND-Durchkontaktierungen bei C8 entfallen. | TI SLAA902: kleinster Stützkondensator höchstens 1 mm vom Pin, auf der Oberseite. In der CPL ändern sich dadurch C8, C9, C10 und R1. |
| 13 | Bootstrap-Kondensatoren C11 bis C14 | 220 nF 25 V 0603 (C21120). C11/C14 0,6 mm vom BST-Pin, aber mit dem Ausgangsende 3,4 mm vom Pin auf der breiten Ausgangsleitung. C12/C13 5,7 mm vom Pin | 220 nF 16 V X7R 0402 (C16772, Samsung CL05B224KO5NNNC, Basic), alle vier senkrecht direkt unter ihrem BST-Pin. BST-Pad 0,47 mm vom Pin, kurze Leitung direkt vom Pin. Das Ausgangspad hängt über eine eigene Stichleitung an der Ausgangsleitung 1,4 mm unter dem Ausgangspin. Die Schleife BST-Pin → Kondensator → Ausgangspin ist damit etwa 2,5 mm lang statt bis zu 12 mm. Die alten Leitungen der BST-Netze sind entfernt. | TI SLAA902 2.6: so nah wie möglich, sternförmig am Ausgangspin, nicht irgendwo auf der breiten Ausgangsleitung. In 0603 passten die beiden mittleren Kondensatoren nicht nebeneinander unter die Pins 21 und 22. Am Kondensator liegen nur die 5 V des Gate-Treibers, 16 V reichen. |
| 14 | Ausgänge am Pin (ersetzt Änderung 10 für die ersten Millimeter) | äußere Ausgänge 3 mm, innere 6,1 mm schmaler als 0,76 mm | Nach dem Pinaustritt (0,55 mm lang, außen 0,4 bis 0,45 mm, innen 0,3 mm breit) sind alle vier Ausgänge mindestens 0,78 mm breit, danach wie bisher bis 1,5 mm. Dafür sind die beiden PVDD-Durchkontaktierungen neben den Pins 15/16 und 27/28 um 0,25 mm nach außen gerückt. | TI SLAA902 2.7: mindestens 30 mil. Breiter als das Pad (0,45 mm) kann die Leitung erst unterhalb der Pinreihe werden. |
| 15 | Zweite Lage ab dem Pin | OUTB- und OUTA- nur auf der Oberseite; OUTB+ und OUTA+ erst 3,7 mm unter dem Pin auf Innenlage 1 | Alle vier Ausgänge haben 1,5 mm unter der Pinkante eine Durchkontaktierung 0,3/0,6 mm zur Innenlage 1. Die inneren Ausgänge laufen dort 0,78 bis 0,8 mm breit 6,4 mm bis zur Spule, mit zwei weiteren Durchkontaktierungen unter dem Kondensator und zwei an der Spule. Die äußeren laufen 0,78 mm bis zur bisherigen Doppelbahn mit 1,2 mm (insgesamt 9,5 und 8,3 mm). Das sind 12 neue Durchkontaktierungen. | TI SLAA902 2.7: Ausgänge auf zwei Lagen. Der Platz ist durch die Verlegung von C12/C13 frei geworden. |
| 16 | 3,3-V-Zuleitung vom Pi (J1 Pin 17) | 0,25 bis 0,3 mm | Jedes Stück so breit, wie 0,2 mm Abstand es erlauben, höchstens 0,6 mm. Der Lauf am Platinenrand ist 0,15 mm vom Sockel weggerückt, die Oberseite bei C7 0,15 mm von SDA. Zwischen den Pinreihen des Sockels passen nur 0,4 mm; dort läuft die Leitung zusätzlich 0,43 mm breit auf Innenlage 1 (zwei neue Durchkontaktierungen). Das Masse-Via von C7 sitzt jetzt auf der anderen Seite seines Pads. | TI SLAA902: 20 bis 30 mil von der Quelle. Ergebnis siehe Prüftabelle. |
| 17 | Eingangsschutz an J4 | J4 direkt auf PVDD, ohne Sicherung, Verpolungsschutz und Filter | J4+ → F1 (Sicherung 5 A träge, 63 V, 1206) → Q2 (P-MOSFET AO4407A, SO-8, 11 mΩ) → FB1 (Ferrit BLM31KN121SN1L, 6 A, 120 Ω bei 100 MHz) → PVDD. Hinter Q2 nach Masse: D2 (TVS SMBJ22A) und C46 (10 µF 50 V). Gate von Q2 über R13 (10 kΩ) an Masse, D3 (Z-Diode 15 V) begrenzt die Gate-Source-Spannung. Die Bauteile sitzen in der Ecke zwischen J4, H3 und X1; PVDD geht hinter FB1 über zwei Durchkontaktierungen 0,4/0,8 mm auf die bisherige Leitung der Unterseite. Dafür ist GPIO11 vom Diagonalweg an den Platinenrand verlegt, die Texte „EIN/AUS“ und „+20V“ sind verschoben, vier Masse-Durchkontaktierungen entfallen, drei kommen dazu. Neue Netze: VIN, VIN_F, VIN_P, Q2G (Netzklasse Power). | Rückmeldung Punkt 1 und 5. Verpolung hätte U1, U2, die Elkos und über die 5 V auch den Pi zerstört. |
| 18 | 5-V-Regler U2 | TPS54302 (C311983), 400 kHz mit Frequenz-Spreizung ±6 % und Eco-Mode | TPS54308 (C168839), gleiches Gehäuse und gleiche Pinbelegung, gleiche Referenzspannung 0,596 V, feste 350 kHz, FCCM (keine Pulsauslassung). Spule und Kondensatoren bleiben: Das Datenblatt des TPS54308 wählt für 5 V selbst 10 µH und 2 × 22 µF. EN-Schwelle 1,21 V steigend, 1,1 V fallend; der Teiler R9/R8 liefert 3,5 V, die Selbsthaltung über D1 etwa 3 V. | Rückmeldung Punkt 4. Mit Spreizung läuft die zweite Oberwelle des TPS54302 über 752 bis 848 kHz und damit durch die 768 kHz des Verstärkers; die Differenz fällt dabei zeitweise in den Hörbereich. Beim TPS54308 liegt das nächste Mischprodukt bei 768 − 2 × 350 = 68 kHz. |
| 19 | Startskript | Register 0x02 und 0x53 nicht gesetzt, Lautstärke unbegrenzt | 0x02 = 0x00 (768 kHz, BD, BTL), 0x53 = 0x60 (Regelbandbreite 175 kHz), Lautstärke nie über 0 dB (0x4C ≥ 0x30), Hochpass 50 Hz (Butterworth 2. Ordnung) in Biquad 1 beider Kanäle, Rücklesen der Register | Rückmeldung Punkt 2 und 3, tiefe Frequenzen |
| 20 | Keramische Stützkondensatoren an PVDD | je Seite 470 µF Elko, 1 µF und 100 nF | zusätzlich C47 und C48, 10 µF 50 V X5R 0805 (C2932476), je Seite direkt über der PVDD-Leitung, 1,3 mm (rechts) und 2,5 mm (links) neben den PVDD-Pins, Masseseite mit eigener Durchkontaktierung | Datenblatt 8.1.3: Versorgung mit Kondensatoren > 22 µF mit niedrigem ESL/ESR entkoppeln; die TI-Stückliste (Tabelle 8-4) hat zusätzlich zum Elko 22 µF keramisch je Seite. Ein 1206 passte rechts wegen des Elkos C2 nicht. |
| 21 | Lötpaste unter dem Kühlpad von U1 | eine Öffnung 3,65 × 2,6 mm (76 %) | vier Öffnungen 1,75 × 1,35 mm mit 0,25/0,2 mm Steg, zusammen 9,45 mm² = 75 % | Datenblatt 9.1.3.2.2: mehrere Öffnungen, zusammen 70 bis 80 % der Padfläche, damit die Paste ausgasen kann |
| 22 | Software | Startskript ohne Abschaltung | `radio_hat_start.sh` mit `start`, `stop`, `status`, `clear`; systemd-Dienst `Pi/radio-hat.service` ruft `stop` vor dem Herunterfahren auf (Mute-Rampe, Hi-Z, PDN low); Fehler aus der Einschaltphase werden gelöscht, danach Fehlerregister im Klartext; automatische Rückkehr nach Übertemperatur (0x76 = 0x10); Hochpass nur noch links geschrieben (rechts nutzt laut 0x66 dieselben Koeffizienten); `Pi/asound.conf` gibt immer 32 Bit je Kanal aus | Datenblatt 7.5.3.2 (Endstufe vor dem Abschalten der Versorgung abschalten), 7.5.3.3 (Fehler bleiben gespeichert), Tabelle 7-49, Tabelle 7-33, Tabelle 7-16 (24-Bit-Wort) |
| 23 | Vorkopplung am 5-V-Regler | C28 100 pF direkt von +5V an FB (parallel zu R6) | R14 2 kΩ 0603 (C22975) in Reihe: +5V → R14 → C28 → FB (neues Netz FB_FF). Damit R14 Platz hat, läuft die EN-Leitung zwischen U2 und R8 über zwei Durchkontaktierungen auf der Unterseite | Datenblatt TPS54308, Kap. 7.2.3.6.3 und Tabelle 7-2: 2 kΩ in Reihe zum Vorkopplungskondensator für besseres Verhalten bei hoher Eingangsspannung und hoher Last. Die Nullstelle (21 kHz) entspricht schon jetzt der TI-Empfehlung (75 pF an 100 kΩ). |
| 24 | Kühlfläche unter U1 nach dem TI-Land-Pattern | Kühlpad 3,1 × 4,05 mm mit 8 Durchkontaktierungen 0,3 mm. Unter dem IC liefen HOLD, GPIO12 und GPIO7 auf Ober- und Unterseite. | Kupfer 3,4 × 9,7 mm unter dem IC: frei bleibt wie bisher 3,1 × 4,05 mm, der Rest liegt unter Lötstopp. Dazu 24 Durchkontaktierungen 0,3/0,6 mm im Raster 1,2 mm (3 × 8), alle ohne Wärmefallen an alle vier Lagen. Neu verlegt (Skript `aenderung_24.py`): <ul><li>HOLD auf Innenlage 1 direkt vom Sockelpin 7 bis zu einer Durchkontaktierung bei D1, 39 mm. Die Leitung liegt nicht unter I²S oder I²C. Sie kreuzt nur langsame Leitungen (GPIO7, GPIO22, GPIO25, IN22_C, PDN) und läuft 6 mm unter der 5-V-Leitung.</li><li>GPIO12 und GPIO6 (Encoder 1) nebeneinander auf der Unterseite am Nordrand des Via-Felds.</li><li>GPIO7 auf der Oberseite links neben U1.</li></ul> Unter dem Kühlkupfer liegt auf keiner Lage mehr eine Signalleitung. Die 3,3-V-Leitung auf der Unterseite ist am früheren Umweg zwischen GPIO24 und HOLD jetzt 0,5 statt 0,35 mm breit. | Datenblatt Kap. 9.1.3.2.1 und Land Pattern Seite 99: <ul><li>Das Kühlpad darf nicht kleiner sein als im Gehäuseanhang.</li><li>Mehr Vias senken den Wärmewiderstand.</li><li>Leiterbahnen sollen den Wärmefluss nicht abschneiden.</li></ul> Die Vias haben 0,3 statt 0,2 mm Bohrung, das ist die Standardbohrung bei JLCPCB (TI erlaubt bis 0,8 mm). Die Platine bleibt 65 × 65 mm: Eine größere brächte nur bei Dauer-Sinus mit Vollaussteuerung etwas und würde Änderungen an Pi-Halter und Gehäuse verlangen. |

Der Vergleich der neuen Gerber-Dateien mit den alten zeigt genau diese Änderungen: im Kupfer zwei Durchkontaktierungen entfernt, drei verschoben, zwei kurze Leiterbahnstücke entfernt, drei neu angeschlossen und 22 Leiterbahnstücke der Ausgänge verbreitert, dazu ein Pastenfeld. In den Bohrdaten sind es entsprechend zwei Bohrungen weniger und drei verschobene. Die Masseflächen hat KiCad 7 neu berechnet, sie sind deckungsgleich mit den alten. Im Bestückungsdruck sind nur die vier verschobenen Beschriftungen und die gekürzten Umrisslinien anders. Lötstopp und Umriss sind unverändert. Dieser Vergleich gilt für die Änderungen 1 bis 8. Für die Änderungen 9 bis 16 wurde stattdessen geprüft: Die Zuordnung aller 293 Pads zu ihren Netzen ist vorher und nachher gleich, der DRC meldet nach erneutem Füllen 0 Verstöße und 0 unverbundene Pads, und die CPL unterscheidet sich nur in den Zeilen C8, C9, C10, R1 und C11 bis C14. In der Stückliste ändert sich nur die Zeile der Bootstrap-Kondensatoren. Für die Änderungen 17 und 18 gilt: Der Netzlistenvergleich vorher/nachher (`verify.py` mit der alten Platine) zeigt nur die 21 Pads der sieben neuen Bauteile und J4 Pin 1 (jetzt VIN statt PVDD). Alle Messwerte von `verify.py` zu Ausgängen, Stützkondensatoren und 3,3 V sind unverändert. Der DRC meldet nach erneutem Füllen 0 Verstöße und 0 unverbundene Pads. Die CPL hat sieben neue Zeilen, alle alten Zeilen sind gleich. In der Stückliste kommen fünf Zeilen dazu, R13 und C46 stehen in bestehenden Zeilen, U2 hat eine neue LCSC-Nummer. Für Änderung 23: Der Netzlistenvergleich zeigt nur R14 und das neue Netz FB_FF an C28, `verify.py` sonst unverändert (zwei Durchkontaktierungen mehr), DRC 0/0, CPL und Stückliste je eine neue Zeile. Für Änderung 24: Der Netzlistenvergleich zeigt nur die 17 zusätzlichen Pads 29 von U1 (Kühlkupfer und 16 Vias mehr). `verify.py` ist sonst unverändert bis auf 182 statt 185 Durchkontaktierungen (sechs entfernt, drei neu) und 3,3 V auf der Unterseite mit mindestens 0,4 statt 0,35 mm. DRC 0/0, CPL und Stückliste unverändert. Innenlage 1 und Innenlage 2 sind weiterhin je eine zusammenhängende Fläche (3.686 und 3.745 mm²). Für die Änderungen 20 und 21: Der Netzlistenvergleich mit der sechsten Fassung zeigt nur die vier Pads von C47 und C48 und die drei zusätzlichen Pastenöffnungen von U1, `verify.py` sonst keine Änderung außer zwei zusätzlichen Durchkontaktierungen, DRC 0 Verstöße und 0 unverbundene Pads, CPL zwei neue Zeilen, Stückliste eine neue Zeile.

Die Änderungen 2, 4, 6 und 8 waren nicht ausdrücklich beauftragt; 4 und 8 sind bei der Prüfung nach den Layout-Regeln entstanden, obwohl nur eine Prüfung verlangt war. Sie lassen sich rückgängig machen: C23 in der BOM wieder auf C12891 setzen, das Pastenfeld am Footprint U1 verkleinern, die Leiterbahnbreiten und die beiden Durchkontaktierungen in KiCad zurückstellen. Der Stand davor liegt in der Git-Historie. Ebenfalls nicht beauftragt war die breitere 3,3-V-Leitung in Änderung 24; sie war möglich, weil HOLD dort nicht mehr verläuft.

## Rückmeldung vom 17.11.2026

Eine zweite Meinung hat die Platine bewertet. Jeder Punkt mit dem, was daraus geworden ist. Die Angaben zum TAS5805M und zum TPS54308 sind inzwischen an den vollständigen Datenblättern geprüft (siebte und achte Fassung); die Angaben zum TPS54302 (Frequenzspreizung ±6 %) stammen aus Suchauszügen der TI-Seiten.

| Nr. | Punkt | Bewertung | Ergebnis |
|---|---|---|---|
| 1 | Kein Schutz am 20-V-Eingang | stimmt | Änderung 17. Q2 sperrt bei Verpolung, die Sicherung bleibt dabei ganz. F1 ist träge, damit der Ladestrom der Elkos beim Einstecken sie nicht auslöst. Spannungsabfall bei 3 A etwa 0,1 V, Verlust in Q2 etwa 0,1 W. |
| 2 | 19 W gelten nur ohne Übersteuerung | stimmt | Das Skript begrenzt die Lautstärke auf höchstens 0 dB. Damit erreicht ein voll ausgesteuertes Signal genau die 17,5 V Spitze, aber nicht mehr. Einen DSP-Limiter (DRC) setzt das Skript nicht: Seine Koeffizienten sind nur mit TIs PPC3 sinnvoll zu erzeugen und hier nicht prüfbar. Musik mit 0 dBFS hat einen Scheitelfaktor von mindestens 6 dB, die mittlere Leistung bleibt damit unter 5 W je Kanal. |
| 3 | Schaltfrequenz und Modulation nicht festgelegt | Der Reset-Wert von 0x02 ist laut Registerbeschreibung 0x00 = 768 kHz, BD. Die Platine lief also schon richtig, aber nur zufällig. | Änderung 19: 0x02 wird ausdrücklich geschrieben, dazu 0x53 = 0x60 (175 kHz; Kodierung 00/01/10/11 = 80/100/120/175 kHz, Tabelle 7-27; dasselbe steht als Beispiel 1 in Kap. 7.5.2.6). Mindestinduktivität bei 768 kHz und BD nach Tabelle 8-2: 10 µH × 384/768 = 5 µH. Die Spulen haben damit doppelte Reserve, auch wenn sie beim Spitzenstrom 20 bis 30 % verlieren. 384 kHz und 1SPW/Hybrid werden nicht verwendet. |
| 4 | 5-V-Regler schaltet nahe der Verstärkerfrequenz | stimmt, sogar deutlicher als beschrieben: Wegen der Spreizung des TPS54302 liegt die Differenz bei 768 kHz nicht fest bei 32 kHz, sondern wandert durch 0 | Änderung 18: TPS54308. Rückwirkung: Im FCCM kann der Regler Strom aufnehmen. Wird der Pi zusätzlich über USB-C versorgt, pumpt er Strom zurück in die 20-V-Schiene. Das ist ohnehin verboten (README). |
| 5 | Kein EMV-Filter am Eingang | stimmt | Änderung 17: FB1 und C46. Der Ferrit wirkt vor allem oberhalb von etwa 10 MHz (UKW-Bereich). Bei 350 und 768 kHz hat er nur wenige Ohm; dort sorgen C46 und die Elkos dafür, dass der Wechselstrom auf der Platine bleibt. Eine echte Drossel für 150 kHz bis 30 MHz würde mit den 940 µF bei einigen Kilohertz schwingen und wurde deshalb nicht eingebaut. Gemessen ist die Störabstrahlung nicht. |
| 6a | Kein Rückspeiseschutz an 5 V | stimmt | Nicht eingebaut, vom Nutzer so entschieden (17.11.2026): Am Pi wird nie ein USB-Netzteil angesteckt. Ein Schutz für 3 A (Ideal-Dioden-Controller mit MOSFET) braucht Platz an der 5-V-Leitung, den es neben dem Sockel nicht gibt. Der Pi sitzt im Gehäuse, USB-C ist nicht zugänglich. Die Warnung in der README ist verschärft. |
| 6b | X7R im Ausgangsfilter | stimmt, Wirkung klein | Keine Änderung. 680 nF in C0G gibt es in 1206 nicht, Folie passt nicht auf die Platine. Bei 10 V Gleichspannung verliert der 50-V-Typ einen Teil seiner Kapazität, die Eckfrequenz steigt von 61 auf etwa 70 kHz. Das liegt weit über dem Hörbereich. |
| 6c | Kein Schaltplan | stimmt | Bleibt so (siehe „Was gemacht wurde“). Die Netzliste der neuen Bauteile steht in Änderung 17 und im Skript `KiCad/werkzeuge/eingangsschutz.py`. |
| – | Frequenzgang oben | Rechnung nachvollzogen: 10 µH und 680 nF ergeben 61 kHz | keine Änderung nötig |
| – | Hochpass für die Lautsprecher | sinnvoll | Änderung 19: 50 Hz, nachgerechnet −3,0 dB bei 50 Hz, −16 dB bei 20 Hz, −0,3 dB bei 100 Hz (bei 48 kHz Abtastrate). Buch 0xAA und die Schreibregel stehen im Datenblatt (7.5.2.5); Seite und Register des ersten Biquads sowie das Format (5.27, a1/a2 mit umgekehrtem Vorzeichen) stammen aus TI SLOA263 und einem veröffentlichten Treiber; am Gerät nicht getestet. |
| – | 50/100 Hz Brumm | stimmt | README: nur geregeltes Schaltnetzteil. Hinweis ergänzt, dass kein Lautsprecheranschluss an Masse darf. |
| – | Hörtest am fertigen Gerät | sinnvoll | In „Erster Test“ der README aufgenommen. |

## Drehlagen in der Bestückungsdatei

Die Pin-1-Lage jedes Bauteils ist durch die Netznamen in den Gerber-Daten belegt. Die Umrechnung auf die Zählweise von JLCPCB folgt der veröffentlichten Tabelle von KiBot. Ob JLCPCB für genau diese Bauteile dieselbe Nulllage verwendet, lässt sich nur in der Bestückungsvorschau sehen. Deshalb dort prüfen:

| Bauteil | Gehäuse | KiCad | Korrektur | CPL | So muss es in der Vorschau aussehen (Platine wie im Bild, Sockel oben) |
|---|---|---|---|---|---|
| U1 TAS5805M | HTSSOP-28 | 270° | +270° | 180° | Pinreihen oben und unten, Pin-1-Punkt oben rechts |
| U2 TPS54308 | TSOT-23-6 | 270° | +180° | 90° | Pinreihen oben und unten, Pin 1 oben rechts |
| Q1 MMBT3904 | SOT-23 | 0° | +180° | 180° | zwei Pins links, ein Pin rechts |
| D1 1N5819WS | SOD-323 | 90° | 0° | 90° | Kathodenstrich unten (zur Kante mit den Schraubklemmen hin) |
| Q2 AO4407A | SOIC-8 | 0° | +270° | 270° | Pinreihen links und rechts, Pin-1-Punkt oben links |
| D2 SMBJ22A | SMB | 90° | 0° | 90° | Kathodenstrich unten (zu J4 hin) |
| D3 BZT52C15 | SOD-123 | 0° | 0° | 0° | Kathodenstrich links (zu H3 hin) |

Ein Fehler um 90° fällt in der Vorschau sofort auf, weil das Bauteil quer zu seinen Pads liegt. Ein Fehler um 180° fällt bei U1, U2, Q2 und den Dioden nicht von selbst auf, dort zählt nur die Pin-1- oder Kathodenmarkierung. Für SOIC-8 und die Dioden-Gehäuse SMB/SOD-123 ist die Korrektur von KiBot übernommen, aber für diese Bauteile nicht bestätigt; ein falsch gedrehter Q2 wäre wirkungslos, eine falsch gedrehte D2 würde das Netzteil kurzschließen. Wenn die Vorschau etwas anderes zeigt, dort drehen und nicht bestellen, bevor es passt.

## Abgleich mit dem Datenblatt TAS5805M (SLASEH5D, Rev. D)

Vollständig gelesen; Werte, Registerbeschreibung und Abgleich Punkt für Punkt in `Datenblaetter/TAS5805M.md` (Abschnitt 1.11). Kurzfassung:

- **Pinbelegung:** Ein Skript hat alle 28 Pins und das Kühlpad gegen Tabelle 5-1 geprüft, keine Abweichung. SDOUT (Pin 9) ist ein Ausgang und bleibt offen.
- **I²C-Adresse:** 15 kΩ von ADR nach DVDD ergibt laut Tabelle 7-5 die Adresse 0x2D.
- **Footprint:** 28 Pads 0,45 × 1,5 mm im Raster 0,65 mm, Reihenabstand 5,8 mm. Das Kühlpad entspricht seit Änderung 24 dem Land Pattern des Gehäuseanhangs: Kupfer 3,4 × 9,7 mm, davon 3,1 × 4,05 mm frei, 24 Vias im Raster 1,2 mm. Lötpaste seit Änderung 21 als Raster mit 75 % (Kap. 9.1.3.2.2). Die Vias sind einfach durchkontaktiert. TI hält gefüllte Vias für am besten, einfache für zulässig (9.1.3.2.1). Auf der Unterseite sind sie mit Lötstopp abgedeckt (Anm. 10: gefüllt, verschlossen oder abgedeckt). 12 davon liegen im freien Bereich unter der Lötpaste (offener Punkt 17).
- **Kleine Versorgungen:** DVDD 4,7 µF + 100 nF, AVDD und VR_DIG je 1 µF, PDN 10 kΩ nach Masse wie in Tabelle 8-4.
- **Bootstrap:** 220 nF je Ausgang wie in 8.1.1. TI verwendet 50-V-Typen in 0603, bestückt sind seit Änderung 13 16-V-Typen in 0402. Am Kondensator liegen nur etwa 5 V (AVDD).
- **Ausgangsfilter:** 10 µH + 680 nF ist bei 768 kHz und BD erlaubt (8.2.1.1, Mindestwert 5 µH nach Tabelle 8-2). Spitzenströme nach 8.1.2 bei 20 V: Einschalten etwa 1,3 A (Tabelle 8-1: 1,55 A bei 24 V), Clipping 1,3 A, 19 W an 8 Ω 2,2 A. Die Spule (Sättigung 3,5 A) liegt darüber, die 80-%-Regel ist mit doppelter Reserve erfüllt.
- **PVDD-Entkopplung:** je Seite 470 µF Low-ESR, seit Änderung 20 10 µF keramisch, 1 µF und 100 nF direkt an den Pins (8.1.3, 9.1.2).
- **Ein- und Abschalten:** Startskript folgt 7.5.3.1; das Abschalten nach 7.5.3.2 übernimmt seit Änderung 22 der systemd-Dienst.
- **Takt:** I²S mit 64 fS und 24-Bit-Wörtern; bei Taktausfall geht der Baustein in Hi-Z und kehrt von selbst zurück (7.3.4). Damit ist die frühere offene Frage nach Pausen ohne Takt beantwortet.
- **Startskript:** Register 0x02, 0x03, 0x4C, 0x53, 0x54, 0x5C, 0x66, 0x70 bis 0x73, 0x76 und 0x78 stimmen mit Kap. 7.6 überein. 0x09 in Register 0x54 ergibt 29,5 V × 10^(−4,5/20) = 17,5 V Spitze, also 19,2 W an 8 Ω.
- **Spannung:** empfohlen bis 26,4 V, absolut 30 V, Überspannungsabschaltung 28 V. Seit Änderung 17 begrenzt die TVS-Diode D2 (Sperrspannung 22 V, Durchbruch ab 24,4 V) die erlaubte Eingangsspannung auf 22 V.
- **Last:** mindestens 6 Ω im Stereobetrieb (Tabelle 6.3, Überstromgrenze 5 A); die Lautsprecher haben 8 Ω.
- **Störfestigkeit:** PSRR 72 dB bei 1 kHz (Tabelle 6.5). Damit ist die Frage aus der Rückmeldung beantwortet.
- **PDN:** TI zieht PDN in allen Schaltbildern mit 10 kΩ nach DVDD hoch; auf dem Radio HAT zieht R2 10 kΩ nach Masse, damit der Verstärker aus bleibt, bis der Pi ihn nach der Einschaltfolge startet. Bewusst so.
- **Leistung und Wärme (Bilder 6-50, 6-54):** bei 20 V an 8 Ω in BD etwa 20 W bei 1 % THD+N, noch nicht thermisch begrenzt; eingestellt sind 19,2 W, etwa 0,2 dB darunter. Wirkungsgrad etwa 85–90 %. Die Kühlfläche entspricht seit Änderung 24 dem TI-Land-Pattern. RθJA laut Datenblatt: 29,1 °C/W auf der JEDEC-Platine (4 Lagen, 76 × 114 mm), 24 °C/W auf dem EVM.
- **EMV:** TI misst mit Spulenfilter mindestens 15 dB Abstand zu EN 55022 Klasse B; der Radio HAT hat dieselbe Filterart (nicht gemessen).

## Abgleich mit dem Datenblatt TPS54308 (SLUSCV2B, Rev. B)

Vollständig gelesen, einschließlich aller Bilder; Werte, Formeln und Abgleich in `Datenblaetter/TPS54308.md` (Abschnitt 1.7). Kurzfassung:

- **Pins und Footprint:** Pinbelegung wie TPS54302 (1 GND, 2 SW, 3 VIN, 4 FB, 5 EN, 6 BOOT). Der KiCad-Footprint TSOT-23-6 weicht leicht vom TI-Land-Pattern ab (IPC-7351-Variante, nach Anm. 4 zulässig).
- **Spannungen:** VIN 20 V (höchstens 22 V durch D2), empfohlen bis 28 V, absolut 30 V. EN höchstens etwa 3,6 V (absolut 7 V).
- **Ausgangsspannung:** R6 75 k / R7 10 k → 5,07 V, mit Toleranzen 4,92–5,21 V.
- **Kondensatoren:** Eingang 10 µF 50 V + 100 nF direkt am VIN-Pin, 470 µF Elko an PVDD; BOOT 100 nF; Ausgang 2 × 22 µF 25 V. Durchtrittsfrequenz nach Gl. 14 etwa 23–34 kHz (< 40 kHz), Welligkeit etwa 13 mV.
- **Vorkopplung:** C28 100 pF an R6 ergibt dieselbe Nullstelle wie TIs 75 pF an 100 kΩ (21 kHz). Der von TI empfohlene 2-kΩ-Reihenwiderstand ist seit Änderung 23 als R14 eingebaut.
- **Spule:** 10 µH statt der in Tabelle 7-2 genannten 15 µH; nach Gl. 8 mit Keramik-Ausgangskondensatoren zulässig. Die Spule begrenzt die Dauerlast auf etwa 2,4 A (offener Punkt 4).
- **Ein/Aus:** Start bei etwa 7,4 V PVDD, Stopp bei etwa 6,4 V (Hysterese etwa 1 V, TI verlangt mehr als 0,5 V).
- **Betriebsart:** FCCM ohne Pulsauslassung, also kein hörbares Pfeifen bei kleiner Last. Im FCCM kann der Regler bis 2,8 A aufnehmen; deshalb nie zusätzlich USB-C am Pi (Entscheidung des Nutzers, kein Schutz eingebaut).
- **Wärme:** RθJA 87 °C/W, bei 1,5 A etwa +26 °C, bei 2,4 A etwa +52 °C.
- **Layout:** Eingangskondensatoren 0,8 und 1,9 mm vom VIN-Pin, Spule 1,2 mm vom SW-Pin, Rückführung auf der abgewandten Seite mit eigener +5V-Leitung. Abweichung vom TI-Beispiel: Die Masseseiten der Eingangskondensatoren liegen 4,3–4,6 mm vom GND-Pin; die Masselage direkt darunter hält die Schleife klein.

## Leiterbahnbreiten und Abstände

Gerechnet für 35 µm Kupfer nach IPC-2221 (Außenlage, 10 °C Erwärmung): 0,4 mm trägt etwa 1,2 A, 0,8 mm etwa 2,0 A, 1,0 mm etwa 2,4 A, 1,5 mm etwa 3,2 A.

| Pfad | Engste Stelle | Strom | Urteil |
|---|---|---|---|
| Netzteil J4 über F1, Q2, FB1 zur Unterseite | Oberseite 1,5 mm, zwei Durchkontaktierungen 0,4/0,8 mm, dann 1,5 mm zu C1 | etwa 3 A bei Volllast | in Ordnung, Spannungsabfall etwa 0,1 V, fast alles in F1, Q2 und FB1 |
| 20 V zu den Verstärker-Pins Kanal B | 1,0 mm auf der Oberseite, dann 0,6 mm Stich direkt auf die Pins | etwa 1,1 A im Mittel je Kanal | in Ordnung |
| 20 V zu Kanal A und Elko C2 | 1,2 mm auf der Unterseite, zwei Durchkontaktierungen 0,4/0,8 mm in Reihe | etwa 1,1 A im Mittel | in Ordnung. Die Stromspitzen liefern C2, C5 und C6, die hinter den Durchkontaktierungen sitzen. |
| Verstärker-Pin zur Spule | 0,3 bis 0,45 mm auf den ersten 0,55 mm unter dem Pin, danach mindestens 0,78 mm bis 1,5 mm; zusätzlich auf Innenlage 1 die äußeren Ausgänge mit 1,2 mm, die inneren mit 0,8 mm | 1,5 A effektiv bei 19 W Sinus | in Ordnung. Zwischen den Pins geht bei 0,65 mm Pinraster nicht mehr |
| Spule zur Lautsprecherklemme | 1,45 bis 1,5 mm, bei SPKB+ auf 1,5 mm Länge 0,9 mm | 1,5 A effektiv | in Ordnung |
| 5 V vom Regler zum Pi | 1,0 mm, 60 mm lang, ohne Durchkontaktierung | bis 3 A | in Ordnung, Spannungsabfall bis 90 mV, Erwärmung bei 3 A Dauerstrom etwa 17 °C |
| Schaltknoten des 5-V-Reglers | 0,45 mm auf 3 mm | bis 3 A | kurz gehalten, in Ordnung |
| 20 V zum Regler U2 | 0,5 mm auf 1,8 mm | unter 1 A | in Ordnung |
| Gate von Q2, Z-Diode D3 | 0,4 mm | unter 1 mA | in Ordnung |

Abstände: Der kleinste Abstand zwischen verschiedenen Netzen beträgt 0,20 mm (aus den Vektordaten gemessen, die 0,18 mm der ersten Fassung waren ein Rasterfehler). Für 20 bis 26 V verlangt IPC-2221 auf lackierten Außenlagen 0,05 mm, blank 0,1 mm. Kupfer zum Platinenrand 0,5 mm. Kleinste Leiterbahn 0,25 mm. Das liegt alles innerhalb der üblichen Fertigungsgrenzen.

## Vergleich mit anderen Digitalverstärkern

- **Datenblatt TAS5805M, Kapitel 9:** Stützkondensatoren unmittelbar an den PVDD-Pins, durchgehende Massefläche von den Massepins weg, Durchkontaktierungen unter dem Kühlpad ohne Wärmefallen, Bauteile so drehen, dass sie den Wärmefluss nicht abschneiden. Erfüllt: Kühlfläche und 24 Durchkontaktierungen wie im TI-Land-Pattern (Änderung 24), unter U1 keine Signalleitung, alle GND-Pads voll angebunden, Massefläche auf der Unterseite zu 77 % geschlossen.
- **Andere TI-Class-D-Datenblätter (TPA3244, TPA3113D2):** breite Versorgungsleiterbahnen auf der Oberseite direkt an die Pins, möglichst ohne Durchkontaktierung. Für Kanal B erfüllt. Kanal A wird über zwei Durchkontaktierungen versorgt, seine Stütz- und Pufferkondensatoren liegen aber dahinter. Das ist eine vertretbare Abweichung.
- **Vergleichbare Platinen:** Der „Louder Raspberry Hat“ und „SquarePi“ verwenden denselben Baustein auf einer Pi-Aufsteckplatine, SquarePi zweilagig mit 65 × 61 mm, der Louder Hat mit einem 5-V-Regler für 3 A. Dieses Konzept ist also üblich.
- **Wärme:** TI gibt den Wärmewiderstand für vierlagige Platinen mit diesem Land Pattern an (24 bis 29 °C/W). Die Platine ist vierlagig und hat seit Änderung 24 dieselbe Kühlfläche, ist aber kleiner als die JEDEC-Testplatine (65 × 65 statt 76 × 114 mm). Gemessen ist ihr Wert nicht.
  - Bei Musik entstehen im Mittel unter 1 W Verlust, also weniger als 30 °C über der Umgebung. Das ist unkritisch.
  - Bei Dauer-Sinus mit Vollaussteuerung (2 × 19 W, etwa 5 W Verlust) wären es 110 bis 140 °C über der Umgebung. Dann regelt der Baustein selbst zurück (Warnung bei 135 °C, Abschaltung bei 160 °C mit automatischer Rückkehr).
  - Eine größere Platine würde diese Grenze nur verschieben, nicht aufheben.

## Prüfung nach TI SLAA902, PCBWay und Analog Devices

Quellen:
- die TI-Schrift SLAA902 „PCB Layout Guidelines for TAS2xxx Series Class-D Non-boosted Audio Amplifier“;
- der PCBWay-Artikel „PCB Layout of Amplifier“, der im Wesentlichen dieselben TI-Regeln wiedergibt;
- der Artikel „A Practical Guide to High-Speed Printed-Circuit-Board Layout“ von John Ardizzoni (Analog Dialogue 39-09, 2005), jetzt als PDF.

Alle drei sind vollständig gelesen. Die Zahlenwerte in SLAA902 gelten für den TAS2770, einen kleineren Baustein für Akkugeräte; sie sind hier Richtwerte, keine Grenzwerte des TAS5805M. Der ADI-Artikel behandelt schnelle Operationsverstärker; Regeln, die nur dafür gelten, sind unten als solche gekennzeichnet.

Die Messwerte stammen aus der fertigen Platine (Skript über die KiCad-Daten, nach dem letzten Füllen der Flächen).

### TI SLAA902 und PCBWay

| Regel | Stand auf der Platine | Urteil |
|---|---|---|
| Vier bis sechs Lagen, eigene Masselage | vier Lagen. Innenlage 2 ist durchgehend Masse (3.745 mm², ein Stück). Innenlage 1 ist Masse (3.686 mm², ein Stück). Darauf liegen die Doppelbahnen der vier Ausgänge, ein Stück 3,3 V am Sockel und seit Änderung 24 die Leitung HOLD (39 mm, nicht unter Takt- und Datenleitungen). Das Kühlpad ist über 24 Durchkontaktierungen an beide Innenlagen gebunden | erfüllt |
| Alle Massepins unter dem Baustein verbinden, mehrere Durchkontaktierungen zur Massefläche | alle fünf Massepins von U1 hängen auf der Oberseite am Kühlpad, darin 24 Durchkontaktierungen | erfüllt |
| Kleinster Stützkondensator höchstens 1 mm vom Pin, auf derselben Lage, kurzer Rückweg | PVDD: 1 µF in 0,7 mm. 3,3 V: C8 in 0,65 mm. VR_DIG: C10 in 0,72 mm. AVDD: C9 in 0,47 mm. Regler U2: 100 nF in 0,8 mm. Alle auf der Oberseite | erfüllt |
| Mehrere Durchkontaktierungen am Massepad der Stützkondensatoren | C3 bis C6: je Seite zwei Durchkontaktierungen unmittelbar an den Pads | erfüllt |
| Bootstrap-Kondensator so nah wie möglich, sternförmig am Ausgangspin, nicht auf der breiten Ausgangsleitung | C11 bis C14 (Änderung 13): BST-Pad 0,47 mm vom BST-Pin. Das Ausgangspad hat eine eigene Stichleitung zur Ausgangsleitung 1,4 mm unter dem Pin. Schleife etwa 2,5 mm statt bis zu 12 mm. Abschätzung nach ADI-Gleichung 2 für einen Streifen ohne Massefläche: etwa 2 nH statt etwa 10 nH. Mit der Masselage etwa 0,2 mm darunter (JLCPCB-Standardaufbau) liegt der echte Wert darunter | erfüllt. Ob die 1 nH aus SLAA902 (Wert für den TAS2770) unterschritten werden, ist ohne Feldberechnung nicht belegt. |
| Class-D-Ausgänge mindestens 30 mil (0,76 mm) auf zwei Lagen, wirksam 60 mil | Änderungen 10, 11, 14, 15. Hauptpfad: nur der Pinaustritt (0,55 mm lang, 0,3 bis 0,45 mm) ist schmaler als 0,76 mm, danach überall mindestens 0,78 mm. Zweite Lage auf Innenlage 1 ab 1,5 mm unter der Pinkante: äußere Ausgänge 9,5 und 8,3 mm mit 0,78 bis 1,2 mm, innere 6,4 mm mit 0,78 bis 0,8 mm. Nach den Spulen 1,45 bis 1,5 mm, bei SPKB+ auf 1,5 mm Länge 0,9 mm | erfüllt bis auf drei kurze Stücke. Die ersten 1,5 mm ab der Pinkante laufen einlagig, davon 0,55 mm schmaler als 0,76 mm: breiter als das Pad (0,45 mm) geht im Raster 0,65 mm nicht, und eine Durchkontaktierung passt erst unterhalb der Pinreihe und der PVDD-Leitung der Unterseite. Einlagig ist auch das letzte Stück in die Spulenpads. Bei SPKB+ ist die Leitung nach der Spule auf 1,5 mm Länge nur 0,9 bis 1,05 mm breit. |
| Filter nah am Baustein, Längen angeglichen | Spulen 9 bis 15 mm vom Pin. Der Weg ist innen kürzer als außen, je Kanal also ungleich lang. Der Unterschied liegt bei wenigen Millimetern mit 0,8 bis 1,5 mm Breite, also bei rund 1 mΩ | erfüllt; der Längenunterschied ist ohne messbare Wirkung. |
| Versorgungen als dicke Leitungen, sternförmig von der Quelle (AVDD/VDD 20 bis 30 mil) | 20 V: 1,5 mm von der Klemme, Zweige mit 1,5 und 1,2 mm. 3,3 V (Änderung 16): 38,6 mm mit 0,5 bis 0,6 mm. Darunter liegen: <ul><li>zwischen den Pinreihen des Sockels 0,4 mm, dort parallel 0,43 mm auf Innenlage 1;</li><li>der Pinaustritt an U1 mit 0,4 bis 0,45 mm auf 1,2 mm.</li></ul> Den früheren Umweg zwischen GPIO24 und HOLD (0,35 bis 0,45 mm auf 2,9 mm) gibt es seit Änderung 24 nicht mehr, dort ist die Leitung 0,5 mm breit. Ohne das doppelt geführte Stück am Sockel ist nur noch der Pinaustritt (1,2 mm) schmaler als 0,5 mm. Einziger Verbraucher ist U1, die Leitung ist also sternförmig | 20 V erfüllt. 3,3 V nur noch am Pinaustritt von U1 einlagig unter 20 mil, sonst erfüllt. Breiter geht dort nur mit Umverlegung der Nachbarleitungen; bei 18 mA beträgt der Spannungsabfall unter 0,1 mV. |
| Schaltende Leitungen nicht ohne Masse dazwischen über oder unter anderen Signalen | Zwischen Oberseite und Innenlage 1 (Ausgänge) und den Signalen der Unterseite liegt Innenlage 2 als geschlossene Masse. Die neuen Durchkontaktierungen der Ausgänge enden auf der Unterseite als freie Pads mit mindestens 0,2 mm Abstand zu den Signalleitungen | erfüllt |
| Digitale Signale nicht neben schaltenden Leitungen | I²S und I²C liegen auf der anderen Seite des Bausteins, mehr als 3,5 mm entfernt. Am nächsten kommt GPIO7 auf der Unterseite mit 0,23 mm zu einer Ausgangs-Durchkontaktierung, getrennt durch die Masselagen | erfüllt |

### Analog Devices (Ardizzoni)

| Regel | Stand auf der Platine | Urteil |
|---|---|---|
| Kleinster Kondensator mit der kleinsten Bauform auf derselben Seite am nächsten am Pin, Masseseite auf kürzestem Weg in die Massefläche | siehe Stützkondensatoren oben; C9 mit eigener Durchkontaktierung 0,4 mm neben dem Pad, C3 bis C6 mit je einer direkt am Pad | erfüllt |
| Mehrere Kondensatorwerte parallel (Schiene nach Masse) | PVDD: 100 nF, 1 µF und 470 µF je Seite | erfüllt |
| Parasitäre Induktivität klein halten: kurze Leitungen, wenige Durchkontaktierungen im kritischen Pfad (Gleichung 3: eine Durchkontaktierung durch 1,6 mm etwa 1,3 nH) | Die Ausgänge haben keine Durchkontaktierung in Reihe; die Durchkontaktierungen der Doppelbahnen liegen parallel zur Oberseite. Bootstrap-Schleifen ohne Durchkontaktierung | erfüllt |
| Eine Lage ganz als Massefläche, ohne Aussparungen für Leitungen | Innenlage 2 | erfüllt. Innenlage 1 ist für die Doppelbahnen bewusst unterbrochen, Innenlage 2 bleibt dafür geschlossen. |
| Massefläche unter Ein- und Ausgangspads entfernen | gilt für schnelle Operationsverstärker (Eingangskapazität). Für den TAS5805M verlangt TI die Massefläche unter dem Baustein | nicht anwendbar |
| Analoge und digitale Masse getrennt, an einem Punkt verbinden | eine gemeinsame Massefläche, alle Massepins am Kühlpad zusammengeführt | entspricht der Vorgabe von TI für diesen Baustein; die Trennung nach ADI ist hier nicht vorgesehen |
| Lange parallele Leitungen und lange Leitungen auf benachbarten Lagen vermeiden; wenn nötig rechtwinklig mit Masse dazwischen | Oberseite und Unterseite sind durch zwei Masselagen getrennt. Auf benachbarten Lagen liegen nur die Doppelbahnen unter ihrer eigenen Oberseitenbahn und das 3,3-V-Stück auf Innenlage 1, das GPIO25 und 5 V auf der Oberseite rechtwinklig kreuzt. Seit Änderung 24 liegt dort auch HOLD (ein Gleichspannungssignal): Es läuft 6 mm unter der 5-V-Leitung und kreuzt GPIO7, GPIO22, GPIO25, IN22_C und PDN, alles langsame Signale. Unter I²S und I²C hat Innenlage 1 keinen Schlitz | erfüllt |
| Skineffekt (Gleichung 5) | Eindringtiefe bei 384 kHz etwa 0,1 mm, größer als die Kupferdicke von 0,035 mm | ohne Einfluss |
| Gehäuse mit freiliegendem Kühlpad senkt den Wärmewiderstand | Kühlfläche nach dem TI-Land-Pattern mit 24 Durchkontaktierungen an drei Masselagen, 75 % Lötpaste | erfüllt |
| Impedanzkontrollierte Leitungen, Schutzringe (Guard Rings) | gilt für HF-Leitungen und hochohmige Operationsverstärker-Eingänge; auf dieser Platine gibt es keine | nicht anwendbar |
| Schaltplan mit allen Layoutangaben, Absprache mit dem Layouter | Es gibt keinen Schaltplan, nur die Platine mit Netzliste (siehe oben) | nicht erfüllt, für die Fertigung ohne Belang |

### Ergebnis

Die Regeln aus SLAA902 und PCBWay sind eingehalten. Ausgenommen sind kurze Stellen, an denen die Geometrie keine Wahl lässt:
- An den Ausgängen sind die ersten 1,5 mm ab der Pinkante einlagig, davon 0,55 mm schmaler als 0,76 mm.
- SPKB+ hat nach der Spule auf 1,5 mm Länge 0,9 bis 1,05 mm statt 1,5 mm.
- Die 3,3-V-Zuleitung hat eine einlagige Engstelle mit 0,4 bis 0,45 mm statt 0,5 mm: den Pinaustritt an U1 (1,2 mm). Der frühere Umweg zwischen GPIO24 und HOLD ist seit Änderung 24 0,5 mm breit. Die Engstelle zwischen den Sockelpins (0,4 mm) ist auf Innenlage 1 doppelt geführt, zusammen 0,83 mm.

Der Wert von 1 nH für die Bootstrap-Schleife ist eine TAS2770-Zahl; er ist nach der Verlegung plausibel, aber nicht nachgerechnet. Die Regeln von Analog Devices, die für diese Schaltung gelten, sind erfüllt. Nicht anwendbar sind die Regeln für Operationsverstärker-Eingänge, getrennte Massen und HF-Leitungen.

## Offene Punkte

| Nr. | Punkt | Was tun |
|---|---|---|
| 1 | U1 (C478472) und U2 (TPS54308, C168839): Lagerbestand bei JLCPCB nicht bestätigt | Im BOM-Abgleich von JLCONE zuerst prüfen. Wenn der TPS54308 fehlt, notfalls wieder TPS54302 (C311983) eintragen; dann liegt der Regler wie vorher nahe an der Verstärkerfrequenz (siehe Rückmeldung Punkt 4). |
| 2 | C377117 (680 nF 50 V 1206) und C23242 (75 kΩ) online nicht bestätigt | Im BOM-Abgleich Wert und Bauform ansehen. Ersatz für C377117: C1881 (FH 1206B684K500NT). |
| 3 | Drehlagen | In der Bestückungsvorschau nach der Tabelle oben prüfen. |
| 4 | 5-V-Schiene: Regler 3 A, aber Spule L5 (10 µH, 2,45 A Dauerstrom, 3,5 A Sättigung) begrenzt auf etwa 2,4 A Dauerlast; ab etwa 2,8 A Last sättigt sie (Datenblatt TPS54308, Gl. 9 und 10) | Mit dem Pi 4 (etwa 0,6–1,5 A) passt das, solange keine stromhungrigen USB-Geräte am Pi hängen. TI empfiehlt für 5 V 15 µH (Tabelle 7-2); eine 15-µH-Spule in derselben Größe hätte weniger Strom, eine größere passt nicht. 10 µH ist nach Gl. 8 zulässig (K_IND 0,37). |
| 5 | Kupfer reicht bis 0,2 mm an die Befestigungslöcher | Kunststoffscheiben unter die Schraubenköpfe. |
| 6 | Elko C1: Massepin auf der Oberseite nur über einen Wärmefallen-Steg angebunden (Unterseite zusätzlich) | Elektrisch in Ordnung, keine Änderung. |
| 7 | Bootstrap-Kondensatoren C11 bis C14 sind jetzt 0402 mit 16 V | Im BOM-Abgleich C16772 prüfen. Am Gerät nach Volllast die Fehlerregister lesen. |
| 8 | Bestellung als vierlagige Platine | Bei JLCPCB 4 Lagen wählen, Lagenfolge F.Cu, In1.Cu, In2.Cu, B.Cu prüfen (Dateien `.g2` und `.g3` in der ZIP). Der Preis vom 8.11. gilt nicht mehr. |
| 9 | Die 20 Durchkontaktierungen der Doppelbahnen liegen im Schaltknoten | Keine Maßnahme. Sie enden auf der Unterseite als freie Pads mit mindestens 0,2 mm Abstand zu Masse und Signalen. |
| 10 | Bestückungsdruck von C11 bis C14 entfernt | Für Umrisse ist zwischen den Pins kein Platz. Die Lage zeigen die Bilder und die Bestückungsvorschau. Dasselbe gilt seit Änderung 17 für Q2, F1, FB1, D2, D3, R13 und C46. |
| 11 | Neue Bauteile aus Änderung 17 und 18 sind bei JLCPCB „Extended“ (Q2, F1, D2, D3, FB1, U2) | Je Extended-Teil verlangt JLCPCB eine Rüstgebühr (zuletzt etwa 3 US-$). Im BOM-Abgleich Bestand prüfen; Ersatz mit gleichen Daten ist möglich (D3: jede BZT52C15 in SOD-123, D2: jede SMBJ22A, F1: 5 A, mindestens 32 V, träge, 1206). |
| 12 | Startskript: Die Adressen des Hochpass-Biquads stehen nicht im Datenblatt (nur Buch 0xAA), sondern in TI SLOA263 | Am Gerät: Das Skript prüft das Fehlerbit „Biquad nicht übernommen“ (0x71 Bit 6). Klingt der Bass falsch oder gar nicht, den Abschnitt mit dem Hochpass im Skript auskommentieren. Alle übrigen Register sind am Datenblatt geprüft. |
| 13 | Kein Rückspeiseschutz zwischen USB-C und 5 V | entschieden (Nutzer, 17.11.2026): kein Schutz, am Pi wird nie ein USB-Netzteil angesteckt. Der TPS54308 kann im FCCM bis 2,8 A zurückspeisen. |
| 14 | C47/C48 (C2932476, 10 µF 50 V 0805): JLCPCB-Klasse und Bestand nicht bestätigt | Im BOM-Abgleich prüfen. Ersatz: jeder 10 µF X5R/X7R mit mindestens 50 V in 0805. |
| 15 | TPS54308 am Datenblatt geprüft (achte Fassung) | erledigt, siehe Abschnitt „Abgleich mit dem Datenblatt TPS54308“ und `Datenblaetter/TPS54308.md`, Abschnitt 1.7. |
| 16 | Kühlfläche unter U1 kleiner als im TI-Land-Pattern | erledigt mit Änderung 24 (neunte Fassung): Kühlfläche und 24 Vias wie im TI-Land-Pattern, unter U1 keine Signalleitung mehr. Die Platine bleibt 65 × 65 mm. |
| 17 | Via-Abdeckung bei der Bestellung: 12 der 24 Vias im Kühlpad liegen im freien Bereich unter der Lötpaste | „Tented“ (Standard) wählen, nie „Untented“. Dann sind die Vias unten mit Lötstopp abgedeckt: Anm. 10 ist erfüllt, und TI lässt einfache Vias zu (9.1.3.2.1). Besser ist „Epoxy Filled & Capped“. Bei 4 Lagen kostet das Aufpreis (laut JLCPCB nur ab 6 Lagen kostenlos), den Preis im Angebot prüfen. |

## Platine in Zahlen

| Merkmal | Wert |
|---|---|
| Größe | 65 × 65 mm, Ecken R 3 mm, 4 Lagen (Oberseite, zwei Masselagen, Unterseite) |
| Kleinste Leiterbahn / kleinster Abstand | 0,25 mm / 0,20 mm |
| Durchkontaktierungen | 177 × 0,3/0,6 mm, 5 × 0,4/0,8 mm, 24 × 0,3/0,6 mm im Kühlpad von U1 |
| Bauteilbohrungen | 0,95 mm (XH-4), 1,0 mm (Sockel, XH-2, Elkos), 1,4 mm (Klemmen) |
| Befestigung | 4 × 2,75 mm unbeschichtet, Raster 58 × 49 mm |
| Bauteile | 96 bestückt (31 Stücklistenzeilen), 16 zum Selbstlöten, 73 Netze |

## LCSC-Nummern

Quelle: Suchmaschinen-Auszüge der Seiten von LCSC und JLCPCB vom 16.11.2026. Lagerbestand und Preise in JLCONE prüfen.

| LCSC | BOM-Angabe | Gefunden | Urteil |
|---|---|---|---|
| C478472 | TAS5805MPWPR | TI TAS5805MPWPR, HTSSOP-28-EP | Typ passt, JLCPCB-Bestand nicht bestätigt |
| C15849 | 1 µF 50 V X5R 0603 | Samsung CL10A105KB8NNNC | passt |
| C14663 | 100 nF 50 V X7R 0603 | Yageo CC0603KRX7R9BB104, Basic | passt |
| C1779 | 4,7 µF 25 V X5R 0805 | Samsung CL21A475KAQNNNE | passt |
| C16772 | 220 nF 16 V X7R 0402 (neu, C11 bis C14) | Samsung CL05B224KO5NNNC, Basic | passt |
| C79272 | 10 µH 3,5 A | Sunlord SWPA6045S100MT, 2,45 A Dauer, 3,5 A Sättigung, Extended | passt |
| C377117 | 680 nF 50 V X7R 1206 | nicht gefunden | nicht bestätigt |
| C1588 | 1 nF 50 V X7R 0603 | Samsung CL10B102KB8NNNC, Basic | passt |
| C22809 | 15 kΩ 1 % | Uniroyal 0603WAF1502T5E, Basic | passt |
| C25804 | 10 kΩ 1 % | Uniroyal 0603WAF1002T5E, Basic | passt |
| C23140 | 33 Ω 1 % | Uniroyal 0603WAF330JT5E, Basic | passt |
| C168839 | TPS54308DDCR (neu, U2) | TI TPS54308DDCR, SOT-23-6, 350 kHz, Extended | passt |
| C16072 | AO4407A (neu, Q2) | AOS AO4407A, SOIC-8, P-Kanal 30 V 12 A | passt, JLCPCB-Klasse nicht bestätigt |
| C553937 | Sicherung 5 A 63 V 1206 träge (neu, F1) | SART S1206-SD-5.0A, als „Slow Blow“ gelistet | passt |
| C10214 | SMBJ22A (neu, D2) | RUILON SMBJ22A, SMB, 22 V / 24,4 V / 35,5 V | passt |
| C2104 | BZT52C15 (neu, D3) | JSCJ BZT52C15, SOD-123, Extended | passt |
| C337884 | BLM31KN121SN1L (neu, FB1) | Murata, 1206, 6 A, 120 Ω bei 100 MHz | passt, JLCPCB-Klasse nicht bestätigt |
| C22975 | 2 kΩ 1 % 0603 (neu, R14) | UNI-ROYAL 0603WAF2001T5E, Basic | passt |
| C2932476 | 10 µF 50 V X5R 0805 (neu, C47, C48) | Samsung CL21A106KBYQNNE, großer Lagerbestand | passt, JLCPCB-Klasse nicht bestätigt |
| C13585 | 10 µF 50 V X5R 1206 (C23, neu auch C46) | Samsung CL31A106KBHNNNE, Basic | passt |
| C12891 | 22 µF 25 V X5R 1206 (C26, C27 an 5 V) | Samsung CL31A226KAHNNNE | passt |
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

1. `JLCPCB/Gerber_RadioHAT.zip` hochladen. Erkannte Größe 65 × 65 mm, 4 Lagen.
2. Einstellungen aus der README wählen, dann `BOM_RadioHAT.csv` und `CPL_RadioHAT.csv` hochladen.
3. Im BOM-Abgleich zuerst prüfen, ob U1 (C478472) und U2 (C168839) lieferbar sind. Dann: 31 Zeilen, alle zugeordnet (C11 bis C14 jetzt C16772 in 0402), C377117 und C23242 auf Wert und Bauform prüfen.
4. In der Bestückungsvorschau die Drehlagen nach der Tabelle oben prüfen. Alle Teile müssen deckungsgleich auf ihren Pads sitzen.
