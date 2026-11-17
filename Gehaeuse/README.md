# Gehäuse

Gehäuse aus 8-mm-Spanplatte Dekor Nussbaum. Vom Originalradio bleiben die Frontplatte (300 × 114 × 3 mm) und die beiden geriffelten Lautsprecherabdeckungen (178 × 112 × 7 mm). Abdeckung, Frontplatte und Abdeckung sitzen stumpf nebeneinander, die Abdeckungen stoßen links und rechts direkt an die Seitenwände. Dahinter liegt über die ganze Breite ein Frontbrett. Links und rechts ist je eine geschlossene Lautsprecherkammer, in der Mitte das Technikfach.

**Außenmaß: 672 × 138 × 210 mm** (Breite × Höhe × Tiefe inkl. Rückwand), dazu 20 mm Füße. Das Originalradio war nach dem Foto etwa 645 × 135 mm groß, die Front wirkt also fast wie früher.

![Vorderansicht](bilder/ansicht_vorne.png)

| Datei | Inhalt |
|---|---|
| `gehaeuse.scad` | 3D-Modell, alle Maße oben als Parameter (OpenSCAD) |
| `zeichnung_gehaeuse.pdf` | Maßzeichnungen, 2 Blätter |
| `zeichnung.py` | erzeugt die Zeichnungen neu, falls sich Maße ändern |
| `bilder/` | Ansichten und Zeichnungen als PNG |

## Aufbau

- **Front:** Die Abdeckungen sitzen 10 mm hinter der Holzvorderkante. Die Frontplatte ist hinten bündig mit den Abdeckungen und liegt deshalb 4 mm tiefer (7 mm Abdeckung − 3 mm Platte). Abdeckungen und Frontplatte liegen beide flach auf dem Frontbrett.
- **Frontbrett:** ein durchgehendes Brett 656 × 122 mm direkt hinter Abdeckungen und Frontplatte. Es trägt die beiden Lautsprecher. Im mittleren Teil kommen später die Löcher für Tasten und Drehgeber dazu, passend zum 3D-gedruckten Träger.
- **Chromleisten:** oben und unten je eine 4 mm hohe Leiste über die ganze Breite (656 mm). Sie füllt den Spalt zwischen Holz und Frontplatte. Aufbau: Trägerleiste 4 × 7 mm, vorne bündig mit den Abdeckungen, darauf eine selbstklebende Chromzierleiste 4 mm.
- **Lautsprecherkammern:** geschlossen, innen 170 × 122 × 177 mm. Das sind 3,7 l brutto und etwa 3,3 l nach Abzug von Lautsprecher und Leisten, also das gleiche Volumen wie vorher. Der Lautsprecher sitzt mittig hinter der Abdeckung.
- **Technikfach:** 300 × 122 mm innen, 177 mm tief, hinten belüftet.
- **Verbindungen:** In 8 mm Spanplatte halten weder Dübel noch Schrauben in der Kante. Deshalb sind alle Ecken innen mit Kiefern-Vierkantleisten 15 × 15 mm verleimt. Die Rückwand wird in diese Leisten geschraubt.
- **Füße:** 4 Chromfüße Ø 25 mm, 20 mm hoch, 60 mm von der Seite und 55 mm von vorne bzw. hinten. Innen sitzt unter jedem Fuß ein verleimtes Holzklötzchen, damit die Schraube Halt hat.

![Offen von hinten](bilder/ansicht_offen.png)
![Explosionsansicht](bilder/explosion.png)

## Ist 8 mm zu dünn?

Es geht, liegt aber an der unteren Grenze.

- **Optik:** Die Front wirkt schlank und kommt dem Original sehr nahe.
- **Stabilität:** Mit den verleimten Leisten in allen Ecken wird der Kasten steif genug. Ohne Leisten geht es nicht.
- **Klang:** Dünne Wände schwingen leichter mit. Die Wandflächen der Kammern sind aber klein (etwa 17 × 18 cm) und an allen Rändern verleimt. Mit Dämmwolle in den Kammern ist das für ein Radio unkritisch.
- **Lautsprecher:** Holzschrauben halten in 8 mm nicht dauerhaft. Deshalb werden die Lautsprecher mit M4-Senkkopfschrauben und Muttern durchgeschraubt.
- **Material:** Spanplatte Dekor gibt es im Baumarkt meist nur in 16 und 19 mm. 8 mm in Nussbaum gibt es eher beim Online-Plattenzuschnitt, vorher prüfen. Passende Kantenumleimer gibt es meist nur breiter; sie werden nach dem Aufbügeln bündig abgeschnitten.
- **Alternative:** 10 oder 12 mm wäre robuster, das Gehäuse würde nur 4 bzw. 8 mm größer. Dafür in `gehaeuse.scad` und `zeichnung.py` nur `t` ändern.

## Zuschnittliste (8 mm Spanplatte Dekor Nussbaum)

| Teil | Anzahl | Maß (mm) | Kanten mit Umleimer |
|---|---|---|---|
| Deckel | 1 | 672 × 202 | vorne, links, rechts |
| Boden | 1 | 672 × 202 | vorne, links, rechts |
| Seitenwand | 2 | 202 × 122 | vorne |
| Frontbrett | 1 | 656 × 122 | – (ganz verdeckt) |
| Zwischenwand | 2 | 177 × 122 | – |
| Rückwand | 1 | 672 × 138 | rundum |

Bei Deckel, Boden, Frontbrett und Rückwand ist die erste Zahl die Breite, bei Seiten- und Zwischenwand die Tiefe. Die Fläche beträgt zusammen etwa 0,54 m². Kantenumleimer Nussbaum braucht es etwa 4,5 m.

**Kiefer-Vierkantleiste 15 × 15 mm**, zusammen etwa 2,9 m (3,5 m kaufen):

| Lage | Anzahl | Länge (mm) |
|---|---|---|
| längs in den Ecken Seite/Deckel und Seite/Boden | 4 | 177 |
| längs an den Zwischenwänden oben und unten (Kammerseite) | 4 | 162 |
| hinten senkrecht an Seiten und Zwischenwänden | 4 | 92 |
| hinten waagerecht im Technikfach | 2 | 300 |
| hinten waagerecht in den Kammern | 4 | 140 |
| Klötzchen unter den Füßen (ca. 30 × 30 × 10, Reststücke) | 4 | – |

## Lautsprecher Sharp VSP0010PBS78A

10 cm, 8 Ω, max. 20 W. Korb 110 × 110 mm, vier Löcher Ø 5 mm im Quadrat mit 84 mm Abstand, Blechring innen 100 mm, Bautiefe etwa 47 mm.

- **Ausschnitt im Frontbrett: Ø 100 mm**, 89 mm von der Seitenwand-Innenseite und mittig in der Höhe (61 mm). Mit Lochsäge 100 mm, Kreisschneider oder Stichsäge.
- **Befestigung:** vier Löcher Ø 4,5 mm im Quadrat 84 mm, vorne angesenkt. M4 × 20 Senkkopf von vorne, hinten Scheibe und Mutter. Der Schraubenkopf liegt bündig, damit die Abdeckung flach aufliegt.

## Warum 210 mm tief

Der Lautsprecher braucht eine geschlossene Kammer von etwa 3 bis 4 l. Für das Sharp-Chassis gibt es keine Datenblattwerte, für 10-cm-Breitbänder ist das der übliche Bereich. Mit 8 mm Wänden ist die Kammer innen breiter, deshalb reichen jetzt 210 mm statt 240 mm für dasselbe Volumen. Jede Kammer locker zu etwa zwei Dritteln mit Polyesterwatte füllen und alle Fugen dicht verleimen.

## Zusammenbau

1. Sichtkanten mit Umleimer bekleben, bündig abschneiden und schleifen.
2. Frontbrett: Lautsprecherlöcher und Schraublöcher bohren und ansenken.
3. Leisten zuschneiden.
4. Kasten: Seitenwände zwischen Deckel und Boden stellen und die Eckleisten längs innen einleimen. Die Leisten beginnen 25 mm hinter der Vorderkante (10 mm Rücksprung + 7 mm Abdeckung + 8 mm Frontbrett) und enden hinten bündig. Mit Zwingen pressen und die Diagonalen prüfen.
5. Frontbrett 17 mm hinter der Vorderkante einleimen. Es liegt hinten an den Stirnseiten der Leisten an. Ein 17 mm breites Holzstück als Abstandslehre hilft.
6. Zwischenwände einleimen: 170 mm von der Seitenwand-Innenseite, vorne stumpf an das Frontbrett. Die Leisten an den Zwischenwänden halten sie an Deckel und Boden.
7. Hintere Leisten einleimen, hinten bündig mit den Kanten. Auf diese wird die Rückwand geschraubt.
8. Klötzchen für die Füße innen auf den Boden leimen.
9. Fugen in den Kammern mit Acryl abdichten. In jede Zwischenwand ein Loch Ø 6 mm für das Lautsprecherkabel, nach dem Durchführen mit Heißkleber verschließen.
10. Lautsprecher anschrauben, Kammern mit Dämmwolle füllen.
11. Trägerleisten für die Chromleiste oben und unten in den Rücksprung kleben, Vorderseite 10 mm hinter der Holzkante. Chromzierleiste aufkleben.
12. Abdeckungen und Frontplatte auf das Frontbrett setzen. Die Abdeckungen mit doppelseitigem Montageband aufkleben. Die Frontplatte wird später vom 3D-Träger gehalten.
13. Rückwand: Lüftungslöcher und Loch für die Netzteilbuchse bohren, Dichtband auf die hinteren Leisten der Kammern kleben. Dann mit Spax 3,5 × 20 in die Leisten schrauben.
14. Füße mit Spax 3,5 × 16 durch den Boden in die Klötzchen schrauben.

## Einkaufsliste

- Spanplatte 8 mm Dekor Nussbaum, Zuschnitt nach Liste
- Kantenumleimer Nussbaum, ca. 4,5 m
- Kiefer-Vierkantleiste 15 × 15 mm, ca. 3,5 m
- 4 Möbelfüße Chrom, ca. Ø 25 mm, 20 mm hoch, zum Anschrauben
- Chromzierleiste selbstklebend, 4 mm breit, ca. 1,5 m
- Material für die Chrom-Trägerleisten 4 × 7 × 656 mm, 2 Stück (Holz oder 3D-Druck)
- 8 × M4 × 20 Senkkopf mit Muttern und Scheiben
- Spax 3,5 × 20 (ca. 30 Stück), Spax 3,5 × 16 (4 Stück)
- Holzleim, Zwingen, Lochsäge Ø 100 mm, Kegelsenker
- Dichtband 9 × 3 mm, ca. 2 m
- Polyesterwatte, ca. 100 g
- doppelseitiges Montageband

Bilder neu erzeugen: `openscad -o bilder/ansicht_vorne.png gehaeuse.scad` und `python3 zeichnung.py`.
