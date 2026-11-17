# Bestellung bei JLCPCB (Stand 17.11.2026, Platine Rev. 1.0, zehnte Fassung)

Die Feldnamen stammen aus dem Bestellformular von JLCPCB bzw. JLCONE. JLCPCB benennt Felder gelegentlich um. Steht ein Feld nicht da oder heißt es anders, die Auswahl mit der gleichen Bedeutung nehmen. Was nicht in der Liste steht, auf dem Standardwert lassen.

Hochzuladen sind drei Dateien aus dem Ordner `JLCPCB`:

| Datei | Wofür |
|---|---|
| `Gerber_RadioHAT.zip` | Platine (12 Dateien: 4 Kupferlagen, Lötstopp, Paste, Bestückungsdruck, Umriss, Bohrungen) |
| `BOM_RadioHAT.csv` | Stückliste, 31 Zeilen, 96 Bauteile |
| `CPL_RadioHAT.csv` | Bauteilpositionen und Drehlagen |

## Schritt 1: Platine

`Gerber_RadioHAT.zip` hochladen. JLCPCB muss danach **4 Lagen** und **65 × 65 mm** anzeigen. Wenn nicht: abbrechen, die ZIP ist dann nicht die aus diesem Stand.

| Feld | Auswahl | Warum |
|---|---|---|
| Base Material | FR-4 | |
| Layers | 4 | aus der ZIP erkannt |
| Dimensions | 65 × 65 mm | aus der ZIP erkannt |
| PCB Qty | 5 | kleinste Menge; davon werden 2 bestückt |
| Product Type | Industrial/Consumer electronics | |
| Different Design | 1 | |
| Delivery Format | Single PCB | Die Economic-Bestückung arbeitet mit Einzelplatinen; ein Nutzen mit V-Ritzung würde auf Standard-Bestückung umstellen |
| PCB Thickness | 1.6 mm | Sockelhöhe und Abstandsbolzen sind darauf gerechnet |
| PCB Color | Green | Bei 4 Lagen bietet die Economic-Bestückung nur Grün an |
| Silkscreen | White | |
| Material Type | Standardwert (FR4 TG 135–140 oder TG155) | |
| Surface Finish | **ENIG**, Gold Thickness 1 U" | Bleifrei (RoHS) und eben. Die ebene Fläche hilft beim Verstärker U1 (Pinraster 0,65 mm, Kühlpad). Billiger, aber ebenfalls bleifrei: **LeadFree HASL**. Nicht „HASL (with lead)“: bleihaltig, ein Gerät damit darf in der EU nicht verkauft werden |
| Outer Copper Weight | 1 oz | |
| Inner Copper Weight | 0.5 oz | Innenlagen sind Masse; 1 oz kostet nur mehr |
| Layer Stackup / Specify Stackup | Standard **JLC04161H-7628** | Masselage etwa 0,2 mm unter der Oberseite, so ist die Platine ausgelegt |
| Layer Sequence | F.Cu → In1.Cu → In2.Cu → B.Cu | In der ZIP: `.gtl` → `.g2` → `.g3` → `.gbl`. JLCPCB übernimmt das aus den Dateinamen; in der Vorschau kontrollieren, dass Lage 2 die mit den Ausgangsleitungen ist (In1) und Lage 3 die fast geschlossene Masse (In2) |
| Impedance Control | No | |
| Via Covering | **Epoxy Filled & Capped**, wenn der Aufpreis vertretbar ist; sonst **Plugged**; sonst **Tented**. Nie **Untented** | Unter dem Kühlpad von U1 liegen 12 Vias in der Lötpaste. Gefüllt und überkupfert ist für TI am besten; „Plugged“ und „Tented“ sind nach TI zulässig. „Untented“ ließe Lot auf die Unterseite laufen |
| Min via hole size/diameter | 0.3 mm/(0.4/0.45 mm) (Standard) | kleinste Bohrung ist 0,3 mm |
| Board Outline Tolerance | ±0.2 mm (Standard) | |
| Confirm Production file | **Yes** | JLCPCB zeigt die aufbereiteten Daten vor der Fertigung; dort kontrollieren, dass keine zusätzlichen Löcher oder Randstreifen eingefügt wurden |
| Mark on PCB / Order Number | Remove bzw. keine Nummer, falls das Feld noch erscheint | Laut JLCPCB druckt es seit Mai 2026 ohnehin keine Bestellnummer mehr. Die Platine trägt selbst „Rev. 1.0 11/2026“ |
| Electrical Test | Flying Probe Fully Test (Standard) | |
| Gold Fingers, Castellated Holes, Edge Plating, Press-fit, UL Marking | No | |

## Schritt 2: Bestückung (PCB Assembly einschalten)

| Feld | Auswahl | Warum |
|---|---|---|
| PCBA Type | **Economic** | Kleinere Rüstkosten; keine Randstreifen nötig. Standard-Bestückung verlangt mindestens 70 × 70 mm und würde Randstreifen anfügen |
| Assembly Side | Top Side | alle SMD-Teile oben |
| PCBA Qty | 2 | erst zwei Muster prüfen (README, „Erster Test“), dann Serie |
| Tooling holes | **Added by Customer** | Die Platine hat drei Passbohrungen 1,152 mm (TH1–TH3: links unten, rechts unten, rechts oben). Mit „Added by JLCPCB“ würde JLCPCB eigene Löcher bohren, notfalls in Kupferflächen |
| Confirm Parts Placement | **Yes** | Ein JLCPCB-Ingenieur prüft die Drehlagen und schickt ein Bild zur Freigabe; zweite Sicherung für Schritt 4 |
| Edge Rails / Fiducials | keine | bei Economic nicht nötig |

Dann **Next** und die beiden Dateien hochladen: `BOM_RadioHAT.csv` als BOM, `CPL_RadioHAT.csv` als CPL (Pick and Place).

## Schritt 3: Stückliste abgleichen

JLCPCB ordnet jede Zeile über die LCSC-Nummer einem Bauteil zu. Kontrollieren:

1. **31 Zeilen, 96 Bauteile, alle zugeordnet**, keine Zeile „not found“ oder „not selected“.
2. **Lagerbestand** zuerst bei den Teilen, für die es keinen gleichwertigen Ersatz gibt:
   - U1 TAS5805MPWPR (C478472), Verstärker
   - U2 TPS54308DDCR (C168839), 5-V-Regler. Fehlt er, notfalls TPS54302 (C311983) eintragen; der liegt aber mit seiner Frequenzspreizung nahe an der Verstärkerfrequenz (Prüfbericht, Rückmeldung Punkt 4).
3. Bei den übrigen Teilen ist Ersatz mit gleichen Daten möglich, falls eines fehlt:

   | Teil | LCSC | Ersatz muss haben |
   |---|---|---|
   | L1–L5 | C79272 | 10 µH, Sättigung ≥ 3,5 A, Dauerstrom ≥ 2,45 A, Bauform 6045 (6 × 6 mm) |
   | C15–C18 | C1881 | 680 nF, ≥ 50 V, X7R, 1206 |
   | C47, C48 | C2932476 | 10 µF, ≥ 50 V, X5R/X7R, 0805 |
   | C23, C46 | C13585 | 10 µF, ≥ 50 V, X5R/X7R, 1206 |
   | Q2 | C16072 | AO4407A oder gleichwertig: P-Kanal, ≥ 30 V, ≤ 15 mΩ, SOIC-8 mit gleicher Pinfolge |
   | F1 | C553937 | 5 A träge, ≥ 32 V, 1206 |
   | D2 | C10214 | SMBJ22A, unidirektional, SMB |
   | D3 | C2104 | Z-Diode 15 V, SOD-123 |
   | FB1 | C337884 | Ferrit 1206, ≥ 6 A, etwa 120 Ω bei 100 MHz |

4. **Extended-Teile** kosten je Teileart eine einmalige Rüstgebühr (zuletzt etwa 3 US-$). Das ist normal; ein Ersatz durch ein Basic-Teil lohnt nur, wenn die Daten gleich sind.

## Schritt 4: Bestückungsvorschau

Die Platine liegt so wie im Bild `Bilder/render_top.png`: 40-poliger Sockel oben, Schraubklemmen unten. Jedes Bauteil muss deckungsgleich auf seinen Pads liegen. Ein Fehler um 90° fällt sofort auf, weil das Teil quer liegt. Ein Fehler um 180° fällt nur an der Markierung auf; deshalb diese sieben Teile einzeln ansehen:

| Bauteil | Wo | So muss es aussehen | Folge, wenn falsch |
|---|---|---|---|
| U1 Verstärker (HTSSOP-28) | Mitte | Pinreihen oben und unten, **Pin-1-Punkt oben rechts** | Verstärker zerstört |
| U2 5-V-Regler (SOT-23-6) | links Mitte | Pinreihen oben und unten, **Pin 1 oben rechts** | Regler zerstört; deshalb beim ersten Test den Pi erst nach der 5-V-Messung aufstecken |
| Q1 Transistor (SOT-23) | links | **zwei Pins links, ein Pin rechts** | Pi fährt nach dem Booten sofort wieder herunter |
| D1 Diode (SOD-323) | links neben dem linken Elko | **Kathodenstrich unten** (zu den Schraubklemmen) | Ein/Aus und Selbsthaltung arbeiten falsch |
| Q2 Verpolungsschutz (SOIC-8) | links unten | Pinreihen links und rechts, **Pin-1-Punkt oben links** | keine Spannung auf der Platine |
| D2 TVS-Diode (SMB) | links unten | **Kathodenstrich unten** (zu J4) | Kurzschluss am Netzteil, Sicherung löst aus |
| D3 Z-Diode (SOD-123) | über J4 | **Kathodenstrich links** (zum Loch H3) | Q2 schaltet nicht durch, der Strom fließt über seine interne Diode und erhitzt ihn |

Liegt eines anders: in der Vorschau drehen (Rotate), bis es stimmt. Die übrigen Teile (Widerstände, Kondensatoren, Spulen, Sicherung, Ferrit) haben keine Polung.

Außerdem prüfen: Die drei kleinen Passbohrungen und die vier Befestigungslöcher sind frei, kein Bauteil sitzt darauf.

## Schritt 5: Angebot kontrollieren und bestellen

Vor dem Bezahlen in der Zusammenfassung nachsehen:

- 4 Lagen, 1,6 mm, Grün, ENIG (oder LeadFree HASL), Via Covering wie gewählt
- PCBA: Economic, Top Side, 2 Stück, Tooling holes „Added by Customer“
- keine Randstreifen (Edge Rails) und kein Nutzen (Panel)
- Stückliste vollständig, keine fehlenden Teile

Bei „Product Description“ für den Zoll passt „Audio and Video Appliance / Audio Amplifiers“. Bei Lieferung in die EU erhebt JLCPCB die Einfuhrumsatzsteuer meist schon beim Bezahlen; sonst kommt sie bei der Zustellung dazu.

## Danach

- **Durchsteckteile selbst löten** (README, „Selbst zu löten“, Teile in `REICHELT.md`). Für ein Gerät, das verkauft wird, bleifreies Lot verwenden. Die Massepads haben Wärmefallen; ein Lötkolben mit etwa 60 W und mittlerer Spitze reicht.
- **Erster Test** nach README, erst ohne Pi, dann ohne Lautsprecher.
- **Vor einer Serie:** Muster vollständig testen (Hörtest, Volllast, Fehlerregister), dann dieselben Dateien mit größerer Menge bestellen. Für den Verkauf in der EU braucht das fertige Gerät außerdem CE (EMV-Messung; der Pi funkt, damit gilt die Funkanlagenrichtlinie), RoHS-Konformität, WEEE-Registrierung und ein CE-gekennzeichnetes Netzteil. Das betrifft das Gerät, nicht die Platinenbestellung.
