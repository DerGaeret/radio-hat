# Prüfbericht Radio HAT (Stand 16.11.2026, vierte Fassung: vier Lagen)

## Was gemacht wurde

1. Aus den Gerber- und Bohrdaten wurde die KiCad-Platine rekonstruiert (`KiCad/RadioHAT.kicad_pcb`). Die Gerber-Dateien enthielten die originalen Netznamen, Bauteilbezeichner und Pin-Nummern, die Rekonstruktion beruht also nicht auf Schätzungen.
2. Die rekonstruierte Platine wurde in KiCad geprüft (DRC) und gegen das Datenblatt des TAS5805M abgeglichen.
3. Drei kleine Korrekturen am Layout, eine an der Bestückungsdatei und eine an der Stückliste (siehe „Änderungen“). Die Fertigungsdaten im Ordner `JLCPCB` sind aus der korrigierten KiCad-Platine neu erzeugt.
4. Die Platine wurde auf vier Lagen umgestellt, damit sie den Layoutregeln von TI (SLAA902) folgt: zwei Masselagen innen, breitere und doppelt geführte Ausgänge, Stützkondensatoren näher an den Pins (Änderungen 9 bis 12). Die Bauteile, die Stückliste und alle Leiterbahnen der Unterseite sind unverändert.

Nicht gemacht: Es gibt keinen Schaltplan (`.kicad_sch`), nur die Platine mit Netzliste. Ein JLCONE-Projekt wurde nicht angelegt, JLCONE läuft auf dem eigenen Rechner. Die Platine ist weiterhin ungetestet.

## Wie sicher ist die Rekonstruktion?

| Prüfung | Ergebnis |
|---|---|
| Unveränderte Rekonstruktion wieder als Gerber exportiert und Objekt für Objekt mit den Originalen verglichen (Pads mit Bezeichner, Pin und Netz, Leiterbahnen mit Netz, Masseflächen, Lötstopp, Paste, Bestückungsdruck, Umriss, alle Bohrungen) | identisch, 0 Abweichungen in 3.678 Objekten und 249 Bohrungen |
| Masseflächen in KiCad neu gefüllt und mit der Originalfüllung verglichen | deckungsgleich (Abweichungen unter 0,02 mm²) |
| Aus der Platine erzeugte Bestückungsdatei gegen die bisherige CPL | alle 86 Zeilen gleich bis auf die gewollte Korrektur bei U2; seit der vierten Fassung zusätzlich C8, C9, C10 und R1 (Änderung 12) |
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
| 9 | Lagenzahl | 2 Lagen | 4 Lagen. Innenlage 1 und Innenlage 2 sind durchgehende Masseflächen (3.738 und 3.758 mm² von rund 4.217 mm², jeweils ein zusammenhängendes Stück) | TI SLAA902 verlangt vier bis sechs Lagen und eine eigene Masselage direkt unter dem Baustein. Damit liegen zwischen den schaltenden Leitungen der Oberseite und den Signalen der Unterseite zwei Masseflächen, und der Schlitz in der Masse der Unterseite spielt keine Rolle mehr. |
| 10 | Ausgangsleitungen (ersetzt Änderung 8) | 0,45 mm am Pin, dann 0,6 bis 0,8 mm | Jedes Stück so breit, wie 0,2 mm Abstand zum Nachbarkupfer es erlauben, höchstens 1,5 mm. Äußere Ausgänge: 3 mm mit 0,45 bis 0,6 mm zwischen den Pins und an C11/C14 vorbei, dann 0,8 bis 1,5 mm. Innere Ausgänge: 4,9 mm mit 0,45 bis 0,55 mm, 1,2 mm mit 0,75 mm, dann 0,85 bis 1,5 mm. Nach den Spulen bis zu den Klemmen 1,45 bis 1,5 mm (bei SPKB+ 1,5 mm lang 0,9 bis 1,05 mm) | TI SLAA902: mindestens 30 mil (0,76 mm), wirksam 60 mil (1,5 mm) bis zum Lautsprecher. |
| 11 | Zweite Bahn für die äußeren Ausgänge | nur Oberseite | OUTB+ und OUTA+ laufen zusätzlich auf Innenlage 1: 1,2 mm breit, 7,3 mm und 6,1 mm lang, an beiden Enden mit je zwei Durchkontaktierungen 0,3/0,6 mm an die Oberseite gebunden (8 neue Durchkontaktierungen). Alle bedrahteten Pads und die acht Durchkontaktierungen im Kühlpad von U1 sind jetzt auch an die Innenlagen angebunden. | TI SLAA902: Ausgänge auf zwei Lagen. Innenlage 2 bleibt darunter geschlossene Masse und schirmt die Signale der Unterseite ab. |
| 12 | Stützkondensatoren der kleinen Versorgungen | C8 (3,3 V) 1,7 mm vom Pin und über zwei Durchkontaktierungen angeschlossen, C10 (VR_DIG) 1,1 mm, C9 (AVDD) 1,8 mm | C8 sitzt jetzt am Platz von R1, 0,65 mm vom Pin, direkt auf der Oberseite angeschlossen, Masse auf kurzem Weg zum Massepin 1. C10 um 0,4 mm an den Pin gerückt (0,73 mm). C9 quer vor Pin 13 gedreht (0,48 mm), mit eigener GND-Durchkontaktierung 0,4 mm neben dem Pad. R1 sitzt am alten Platz von C8. Zwei dadurch überflüssige GND-Durchkontaktierungen bei C8 entfallen. | TI SLAA902: kleinster Stützkondensator höchstens 1 mm vom Pin, auf der Oberseite. In der CPL ändern sich dadurch C8, C9, C10 und R1. |

Der Vergleich der neuen Gerber-Dateien mit den alten zeigt genau diese Änderungen: im Kupfer zwei Durchkontaktierungen entfernt, drei verschoben, zwei kurze Leiterbahnstücke entfernt, drei neu angeschlossen und 22 Leiterbahnstücke der Ausgänge verbreitert, dazu ein Pastenfeld. In den Bohrdaten sind es entsprechend zwei Bohrungen weniger und drei verschobene. Die Masseflächen hat KiCad 7 neu berechnet, sie sind deckungsgleich mit den alten. Im Bestückungsdruck sind nur die vier verschobenen Beschriftungen und die gekürzten Umrisslinien anders. Lötstopp und Umriss sind unverändert. Dieser Vergleich gilt für die Änderungen 1 bis 8. Für die Änderungen 9 bis 12 wurde stattdessen geprüft: Die Zuordnung aller 293 Pads zu ihren Netzen ist vorher und nachher gleich, der DRC meldet nach erneutem Füllen 0 Verstöße und 0 unverbundene Pads, und die CPL unterscheidet sich nur in den Zeilen C8, C9, C10 und R1.

Die Änderungen 2, 4, 6 und 8 waren nicht ausdrücklich beauftragt; 4 und 8 sind bei der Prüfung nach den Layout-Regeln entstanden, obwohl nur eine Prüfung verlangt war. Sie lassen sich rückgängig machen: C23 in der BOM wieder auf C12891 setzen, das Pastenfeld am Footprint U1 verkleinern, die Leiterbahnbreiten und die beiden Durchkontaktierungen in KiCad zurückstellen. Der Stand davor liegt in der Git-Historie.

## Drehlagen in der Bestückungsdatei

Die Pin-1-Lage jedes Bauteils ist durch die Netznamen in den Gerber-Daten belegt. Die Umrechnung auf die Zählweise von JLCPCB folgt der veröffentlichten Tabelle von KiBot. Ob JLCPCB für genau diese Bauteile dieselbe Nulllage verwendet, lässt sich nur in der Bestückungsvorschau sehen. Deshalb dort prüfen:

| Bauteil | Gehäuse | KiCad | Korrektur | CPL | So muss es in der Vorschau aussehen (Platine wie im Bild, Sockel oben) |
|---|---|---|---|---|---|
| U1 TAS5805M | HTSSOP-28 | 270° | +270° | 180° | Pinreihen oben und unten, Pin-1-Punkt oben rechts |
| U2 TPS54302 | TSOT-23-6 | 270° | +180° | 90° | Pinreihen oben und unten, Pin 1 oben rechts |
| Q1 MMBT3904 | SOT-23 | 0° | +180° | 180° | zwei Pins links, ein Pin rechts |
| D1 1N5819WS | SOD-323 | 90° | 0° | 90° | Kathodenstrich unten (zur Kante mit den Schraubklemmen hin) |

Ein Fehler um 90° fällt in der Vorschau sofort auf, weil das Bauteil quer zu seinen Pads liegt. Ein Fehler um 180° fällt bei U1, U2 und D1 nicht von selbst auf, dort zählt nur die Pin-1-Markierung. Wenn die Vorschau etwas anderes zeigt, dort drehen und nicht bestellen, bevor es passt.

## Abgleich mit dem Datenblatt TAS5805M (SLASEH5D)

- **Pinbelegung:** Alle 28 Pins und das Kühlpad sind so verdrahtet wie in Tabelle 5-1. Die in der ersten Fassung offenen Pins 3, 6 bis 12, 21 und 25 sind damit bestätigt.
- **I²C-Adresse:** 15 kΩ von ADR nach DVDD ergibt laut Tabelle 7-5 die Adresse 0x2D, wie im Startskript.
- **Footprint:** 28 Pads 0,45 × 1,5 mm im Raster 0,65 mm, Reihenabstand 5,8 mm, Kühlpad 3,1 × 4,05 mm. Das entspricht dem Beispiel im Datenblatt.
- **Bootstrap:** 220 nF je Ausgang wie im Datenblatt. Das Datenblatt nennt 50-V-Typen, bestückt sind 25-V-Typen. Am Kondensator liegen nur etwa 5 V an, das ist unkritisch.
- **Ausgangsfilter:** 10 µH + 680 nF steht so in den Tabellen des Datenblatts. Der Einschaltstrom liegt bei 24 V und 10 µH je nach Schaltfrequenz bei 1,55 bis 3 A. Die Spule (Sättigung 3,5 A) und die Abschaltschwelle des Verstärkers (5 A) liegen darüber.
- **Stützkondensatoren:** C3 bis C6 sitzen direkt auf der 20-V-Leiterbahn, etwa 1,5 mm vor den PVDD-Pins. Je Seite steht ein 470-µF-Elko daneben. Das Datenblatt verlangt genau diese Nähe.
- **Startskript:** Register 0x03 (Zustand HiZ/Play), 0x54 (Analogverstärkung, 0,5 dB je Schritt, 0 dB = 29,5 V Spitze), 0x4C (Lautstärke, 0x30 = 0 dB) und 0x70 bis 0x72 (Fehler) stimmen mit dem Datenblatt überein. 0x09 in Register 0x54 ergibt 17,6 V Spitze, also 19 W an 8 Ω.
- **Spannung:** empfohlen bis 26,4 V, absolut 30 V. Die Grenze von 26 V in der README passt.

## Leiterbahnbreiten und Abstände

Gerechnet für 35 µm Kupfer nach IPC-2221 (Außenlage, 10 °C Erwärmung): 0,4 mm trägt etwa 1,2 A, 0,8 mm etwa 2,0 A, 1,0 mm etwa 2,4 A, 1,5 mm etwa 3,2 A.

| Pfad | Engste Stelle | Strom | Urteil |
|---|---|---|---|
| Netzteil J4 zum Elko C1 (Unterseite) | 1,5 mm, 39 mm lang | etwa 3 A bei Volllast | in Ordnung, Spannungsabfall etwa 40 mV |
| 20 V zu den Verstärker-Pins Kanal B | 1,0 mm auf der Oberseite, dann 0,6 mm Stich direkt auf die Pins | etwa 1,1 A im Mittel je Kanal | in Ordnung |
| 20 V zu Kanal A und Elko C2 | 1,2 mm auf der Unterseite, zwei Durchkontaktierungen 0,4/0,8 mm in Reihe | etwa 1,1 A im Mittel | in Ordnung. Die Stromspitzen liefern C2, C5 und C6, die hinter den Durchkontaktierungen sitzen. |
| Verstärker-Pin zur Spule | 0,45 mm zwischen den Pins, auf 3 bis 6,1 mm Länge 0,45 bis 0,75 mm, danach 0,8 bis 1,5 mm; äußere Ausgänge zusätzlich 1,2 mm auf Innenlage 1 | 1,5 A effektiv bei 19 W Sinus | in Ordnung. Zwischen den Pins geht bei 0,65 mm Pinraster nicht mehr |
| Spule zur Lautsprecherklemme | 1,45 bis 1,5 mm, bei SPKB+ auf 1,5 mm Länge 0,9 mm | 1,5 A effektiv | in Ordnung |
| 5 V vom Regler zum Pi | 1,0 mm, 60 mm lang, ohne Durchkontaktierung | bis 3 A | in Ordnung, Spannungsabfall bis 90 mV, Erwärmung bei 3 A Dauerstrom etwa 17 °C |
| Schaltknoten des 5-V-Reglers | 0,45 mm auf 3 mm | bis 3 A | kurz gehalten, in Ordnung |
| 20 V zum Regler U2 | 0,5 mm auf 1,8 mm | unter 1 A | in Ordnung |

Abstände: Der kleinste Abstand zwischen verschiedenen Netzen beträgt 0,20 mm (aus den Vektordaten gemessen, die 0,18 mm der ersten Fassung waren ein Rasterfehler). Für 20 bis 26 V verlangt IPC-2221 auf lackierten Außenlagen 0,05 mm, blank 0,1 mm. Kupfer zum Platinenrand 0,5 mm. Kleinste Leiterbahn 0,25 mm. Das liegt alles innerhalb der üblichen Fertigungsgrenzen.

## Vergleich mit anderen Digitalverstärkern

- **Datenblatt TAS5805M, Kapitel 9:** Stützkondensatoren unmittelbar an den PVDD-Pins, durchgehende Massefläche von den Massepins weg, Durchkontaktierungen unter dem Kühlpad ohne Wärmefallen, Bauteile so drehen, dass sie den Wärmefluss nicht abschneiden. Erfüllt: acht Durchkontaktierungen im Kühlpad, alle GND-Pads voll angebunden, Massefläche auf der Unterseite zu 76 % geschlossen.
- **Andere TI-Class-D-Datenblätter (TPA3244, TPA3113D2):** breite Versorgungsleiterbahnen auf der Oberseite direkt an die Pins, möglichst ohne Durchkontaktierung. Für Kanal B erfüllt. Kanal A wird über zwei Durchkontaktierungen versorgt, seine Stütz- und Pufferkondensatoren liegen aber dahinter. Das ist eine vertretbare Abweichung.
- **Vergleichbare Platinen:** Der „Louder Raspberry Hat“ und „SquarePi“ verwenden denselben Baustein auf einer Pi-Aufsteckplatine, SquarePi zweilagig mit 65 × 61 mm, der Louder Hat mit einem 5-V-Regler für 3 A. Dieses Konzept ist also üblich.
- **Wärme:** TI gibt den Wärmewiderstand für vierlagige Platinen an (24 bis 29 °C/W). Die Platine ist seit der vierten Fassung vierlagig; gemessen ist ihr Wert nicht. Bei Musik entsteht im Mittel unter 1 W Verlust, das ist unkritisch. Dauerhafte Vollaussteuerung mit Sinus (etwa 4 W Verlust) ist auf zwei Lagen nicht abgesichert. Der Baustein regelt bei Übertemperatur selbst zurück (Warnung bei 135 °C).

## Prüfung nach TI SLAA902, PCBWay und Analog Devices

Quellen: die TI-Schrift SLAA902 „PCB Layout Guidelines for TAS2xxx Series Class-D Non-boosted Audio Amplifier“ (vollständig gelesen), der PCBWay-Artikel „PCB Layout of Amplifier“ (vollständig gelesen; er gibt im Wesentlichen dieselben TI-Regeln wieder) und der Artikel „A Practical Guide to High-Speed Printed-Circuit-Board Layout“ von Analog Devices. Dessen Seite ließ sich nicht abrufen, ausgewertet sind nur die Auszüge aus der Websuche. Die Zahlenwerte in SLAA902 gelten für den TAS2770, einen kleineren Baustein für Akkugeräte; sie sind hier Richtwerte, keine Grenzwerte des TAS5805M.

| Regel | Quelle | Stand auf der Platine | Urteil |
|---|---|---|---|
| Vier bis sechs Lagen, eigene Masselage | TI, PCBWay | vier Lagen; Innenlage 1 und 2 sind Masse, jeweils ein zusammenhängendes Stück. Auf Innenlage 1 liegen nur die beiden Doppelbahnen der äußeren Ausgänge | erfüllt (Änderung 9). TI gibt den Wärmewiderstand für vierlagige Platinen an (24 bis 29 °C/W); das Kühlpad ist über acht Durchkontaktierungen an alle Masselagen gebunden. |
| Alle Massepins unter dem Baustein verbinden und mit mehreren Durchkontaktierungen an die Massefläche führen | TI, PCBWay | alle fünf Massepins von U1 hängen auf der Oberseite direkt am Kühlpad, darin acht Durchkontaktierungen | erfüllt |
| Kleinster Stützkondensator höchstens 1 mm vom Pin, auf derselben Lage, kurzer Rückweg | TI, PCBWay, ADI | PVDD: 1 µF in 0,7 mm, 100 nF in 2,1 mm, alle auf der Oberseite direkt auf der 20-V-Leiterbahn. Regler U2: 100 nF in 0,8 mm | erfüllt. Dass der 1-µF-Typ näher sitzt als der 100-nF-Typ, ist unkritisch: beide haben dieselbe Bauform und damit dieselbe Eigeninduktivität. |
| wie oben, für die kleinen Versorgungen | TI, ADI | 3,3 V: C8 in 0,65 mm, auf der Oberseite angeschlossen. VR_DIG: C10 in 0,73 mm. AVDD: C9 in 0,48 mm | erfüllt (Änderung 12) |
| Mehrere Durchkontaktierungen am Massepad der Stützkondensatoren, dicht am Pad | TI, PCBWay | C3 bis C6: je Seite zwei Durchkontaktierungen unmittelbar an den Pads | erfüllt (nach Änderung 4) |
| Bootstrap-Kondensator so nah wie möglich am Ausgangspin, sternförmig angeschlossen | TI, PCBWay | äußere Ausgänge (C11, C14): 0,6 mm vom Pin. Innere Ausgänge (C12, C13): 5,7 mm vom Pin, Schleife aus zwei eng parallel geführten Leiterbahnen, geschätzt etwa 4 nH | C11/C14 erfüllt. C12/C13 unverändert: Die Pinfolge Ausgang, Bootstrap, Bootstrap, Ausgang im Raster 0,65 mm lässt zwischen C11 und C14 keinen Platz für zwei weitere 0603. Das Layoutbeispiel im Datenblatt des TAS5805M (Bild 9-2) setzt die beiden inneren Bootstrap-Kondensatoren ebenfalls versetzt nach außen; aus dem Bild abgeschätzt etwa 5 mm vom Pin. Der Zahlenwert von 1 nH in SLAA902 gilt für den TAS2770 und wird hier nicht erreicht. |
| Class-D-Ausgänge mindestens 30 mil (0,76 mm) breit auf zwei Lagen, zusammen also 60 mil; Filter nah am Baustein; Längen angeglichen | TI, PCBWay | nach Änderung 10 und 11. Äußere Ausgänge: 3 mm schmaler als 0,76 mm (zwischen den Pins und neben C11/C14), dann 0,8 bis 0,9 mm oben plus 1,2 mm auf Innenlage 1, zuletzt 1,5 mm. Innere Ausgänge: 6,1 mm schmaler als 0,76 mm (davon 1,2 mm mit 0,75 mm), dann 0,85 bis 1,5 mm auf einer Lage, insgesamt rund 10 mm lang. Nach den Spulen 1,5 mm. Spulen 9 bis 15 mm vom Pin | weitgehend erfüllt. Rest: die ersten 3 bis 6,1 mm an den Pins und die kurzen inneren Ausgänge ohne zweite Lage. Im Pinraster 0,65 mm passt weder mehr Breite noch eine Durchkontaktierung. |
| Versorgungsleitungen dick genug, sternförmig von der Quelle | TI, PCBWay | 20 V: 1,5 mm von der Klemme, nach 15 mm trennen sich die Zweige zum Verstärker (1,5 mm) und zum 5-V-Regler (1,2 mm). 3,3 V kommt mit 0,25 mm vom Pi (TI nennt 20 bis 30 mil) | 20 V erfüllt. 3,3 V dünner als empfohlen, bei 18 mA unkritisch. |
| Schaltende Leitungen nicht ohne Masse dazwischen über oder unter anderen Signalen führen | TI, PCBWay, ADI | Zwischen den schaltenden Leitungen (Oberseite und Innenlage 1) und den Signalen der Unterseite liegt Innenlage 2 als geschlossene Masse, unter der Oberseite zusätzlich Innenlage 1 | erfüllt (Änderung 9) |
| Digitale Signale nicht neben schaltenden Leitungen | TI, PCBWay | I²S und I²C liegen auf der anderen Seite des Bausteins, mehr als 3,5 mm entfernt. Am nächsten kommt GPIO16 mit 0,45 mm | erfüllt |
| Durchgehende Massefläche, Rückstrom direkt unter dem Signal | ADI | Innenlage 2 ist ohne Schlitz, Innenlage 1 bis auf die beiden Doppelbahnen der Ausgänge. Der Schlitz der 20-V-Leiterbahn in der Masse der Unterseite besteht weiter, führt aber keinen Rückstrom mehr | erfüllt (Änderung 9) |
| Analoge und digitale Masse an einem Punkt verbinden | ADI | eine gemeinsame Massefläche, alle Massepins am Kühlpad zusammengeführt | entspricht der Vorgabe von TI für diesen Baustein |

Mit vier Lagen sind die Regeln aus SLAA902 bis auf drei Reste eingehalten: die schmalen ersten Millimeter der Ausgänge an den Pins, die inneren Ausgänge ohne zweite Lage und die Lage von C12/C13, die dem Layoutbeispiel des Datenblatts entspricht, aber nicht dem Zahlenwert für den TAS2770. Die 3,3-V-Zuleitung vom Pi bleibt 0,25 bis 0,3 mm breit; breiter geht auf den vorhandenen Wegen nur stückweise, bei 18 mA ist das ohne Belang. Der Artikel von Analog Devices ist weiterhin nur aus Suchauszügen ausgewertet.

## Offene Punkte

| Nr. | Punkt | Was tun |
|---|---|---|
| 1 | U1 (C478472): Lagerbestand bei JLCPCB nicht bestätigt | Im BOM-Abgleich von JLCONE zuerst prüfen. |
| 2 | C377117 (680 nF 50 V 1206) und C23242 (75 kΩ) online nicht bestätigt | Im BOM-Abgleich Wert und Bauform ansehen. Ersatz für C377117: C1881 (FH 1206B684K500NT). |
| 3 | Drehlagen | In der Bestückungsvorschau nach der Tabelle oben prüfen. |
| 4 | 5-V-Regler liefert höchstens 3 A, Spule L5 2,45 A Dauerstrom | Mit dem Pi 4 passt das, solange keine stromhungrigen USB-Geräte am Pi hängen. |
| 5 | Kupfer reicht bis 0,2 mm an die Befestigungslöcher | Kunststoffscheiben unter die Schraubenköpfe. |
| 6 | Elko C1: Massepin auf der Oberseite nur über einen Wärmefallen-Steg angebunden (Unterseite zusätzlich) | Elektrisch in Ordnung, keine Änderung. |
| 7 | Bootstrap-Kondensatoren C12/C13 sitzen 5,7 mm vom Pin | Am Gerät nach Volllast die Fehlerregister lesen. Bei Auffälligkeiten wäre das der erste Verdächtige. |
| 8 | Bestellung als vierlagige Platine | Bei JLCPCB 4 Lagen wählen, Lagenfolge F.Cu, In1.Cu, In2.Cu, B.Cu prüfen (Dateien `.g2` und `.g3` in der ZIP). Der Preis vom 8.11. gilt nicht mehr. |
| 9 | Die Durchkontaktierungen der Doppelbahnen liegen im Schaltknoten | Keine Maßnahme. Sie enden auf der Unterseite als freie Pads mit 0,2 mm Abstand zur Masse. |

## Platine in Zahlen

| Merkmal | Wert |
|---|---|
| Größe | 65 × 65 mm, Ecken R 3 mm, 4 Lagen (Oberseite, zwei Masselagen, Unterseite) |
| Kleinste Leiterbahn / kleinster Abstand | 0,25 mm / 0,20 mm |
| Durchkontaktierungen | 163 × 0,3/0,6 mm, 3 × 0,4/0,8 mm, 8 × 0,3 mm im Kühlpad von U1 |
| Bauteilbohrungen | 0,95 mm (XH-4), 1,0 mm (Sockel, XH-2, Elkos), 1,4 mm (Klemmen) |
| Befestigung | 4 × 2,75 mm unbeschichtet, Raster 58 × 49 mm |
| Bauteile | 86 bestückt (24 Stücklistenzeilen), 16 zum Selbstlöten, 68 Netze |

## LCSC-Nummern

Quelle: Suchmaschinen-Auszüge der Seiten von LCSC und JLCPCB vom 16.11.2026. Lagerbestand und Preise in JLCONE prüfen.

| LCSC | BOM-Angabe | Gefunden | Urteil |
|---|---|---|---|
| C478472 | TAS5805MPWPR | TI TAS5805MPWPR, HTSSOP-28-EP | Typ passt, JLCPCB-Bestand nicht bestätigt |
| C15849 | 1 µF 50 V X5R 0603 | Samsung CL10A105KB8NNNC | passt |
| C14663 | 100 nF 50 V X7R 0603 | Yageo CC0603KRX7R9BB104, Basic | passt |
| C1779 | 4,7 µF 25 V X5R 0805 | Samsung CL21A475KAQNNNE | passt |
| C21120 | 220 nF 25 V X7R 0603 | Samsung CL10B224KA8NNNC | passt |
| C79272 | 10 µH 3,5 A | Sunlord SWPA6045S100MT, 2,45 A Dauer, 3,5 A Sättigung, Extended | passt |
| C377117 | 680 nF 50 V X7R 1206 | nicht gefunden | nicht bestätigt |
| C1588 | 1 nF 50 V X7R 0603 | Samsung CL10B102KB8NNNC, Basic | passt |
| C22809 | 15 kΩ 1 % | Uniroyal 0603WAF1502T5E, Basic | passt |
| C25804 | 10 kΩ 1 % | Uniroyal 0603WAF1002T5E, Basic | passt |
| C23140 | 33 Ω 1 % | Uniroyal 0603WAF330JT5E, Basic | passt |
| C311983 | TPS54302DDCR | TI TPS54302DDCR, TSOT-23-6, Extended | passt |
| C13585 | 10 µF 50 V X5R 1206 (neu, C23) | Samsung CL31A106KBHNNNE, Basic | passt |
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
3. Im BOM-Abgleich zuerst prüfen, ob U1 (C478472) lieferbar ist. Dann: 24 Zeilen, alle zugeordnet, C377117 und C23242 auf Wert und Bauform prüfen.
4. In der Bestückungsvorschau die Drehlagen nach der Tabelle oben prüfen. Alle Teile müssen deckungsgleich auf ihren Pads sitzen.
