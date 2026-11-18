# Einkaufsliste

Stand 18.11.2026. Alles, was für das Radio noch gekauft werden muss. Die Händler sind Vorschläge; Normteile gibt es überall (Reichelt, Conrad, Amazon). Preise und Lagerbestand nicht geprüft (die Shops sind aus der Cloud nicht erreichbar).

## Vorhanden bzw. vom Originalradio

- Frontplatte, 2 Lautsprecherabdeckungen, 4 Originalknöpfe (Bohrung Ø 3 × 17 mm), 6 Originaltasten
- Original-A/E-Schalter (RFT) mit Mutter und Scheibe
- Lautsprecher Sharp VSP0010PBS78A (2 ×), Cherry MX Blue (6 ×), falls noch nicht da: unten mit aufgeführt

## Elektronik

| Anz. | Teil | Hinweis | Bezug (Beispiel) |
|---|---|---|---|
| 1 | Raspberry Pi 4B (2 GB reichen) | | Raspberry-Pi-Händler |
| 1 | microSD-Karte 32 GB, A1 | | |
| 1 | Passiver Kühlkörper für Pi 4 (Aufklebe-Set) | flach, unter dem DigiAMP+ ist wenig Platz | |
| 1 | Raspberry Pi DigiAMP+ | grüne Ausführung, mit Abstandsbolzen | Raspberry-Pi-Händler |
| 1 | Netzteil 19 V, ≥ 3,42 A, Hohlstecker 5,5 × 2,5 mm Mitte Plus | Empfehlung XP Power VEC65US19 | RS, Distrelec, Bürklin |
| 1 | Netzkabel passend zur Buchse des Netzteils (C6, C8 oder C14) | beim Netzteil nachsehen | |
| 1 | Pololu Big MOSFET Slide Switch with Reverse Voltage Protection, **HP** (#2815) | schaltet die 19 V | pololu.com oder Pololu-Händler |
| 1 | Pololu 5V, 3.2A Step-Down Voltage Regulator **D36V28F5** (#3782) | 5 V für die LEDs | pololu.com oder Pololu-Händler |
| 1 | 74AHCT125 im DIP-14-Gehäuse + IC-Sockel DIP-14 | Pegelwandler 3,3 → 5 V | Reichelt |
| 2 | Schottky-Diode BAT85 (DO-34) | A/E-Erkennung | Reichelt |
| 1 | Widerstand 330 Ω, 0,25 W | LED-Datenleitung | |
| 2 | Elko 1000 µF, 10 V oder mehr | an Wandler und Lichtkasten | |
| 1 | Keramikkondensator 100 nF | am 74AHCT125 | |
| 3 | Schraubklemme 2-polig RM 5,08 | EIN, VERST, A/E | |
| 1 | Schraubklemme 3-polig RM 5,08 | LED | |
| 1 | Stiftleiste 2,54 mm, 40-polig, gerade | für Pololu-Module und Steckverbindung zum Pi | |
| 1 | Einbau-Hohlbuchse 5,5 × 2,5 mm, Schraubmontage (M8), Lötanschluss | im Rückwanddeckel | |
| 1 | DC-Kabel mit Hohlstecker 5,5 × 2,5 mm, offenes Ende, ca. 50 cm, 0,75 mm² | Steuerplatine → DigiAMP+ | |
| 1 m | Litze 0,75 mm² rot und schwarz | Buchse → Steuerplatine | |
| 3 | **ALPS STEC11B03** (30 Rastungen, 15 Impulse, Taster, Welle Ø 6 × 25 mm geschlitzt) | Klang, Lautstärke, Sender | Bürklin, Distrelec, RS, Rapid |
| 6 | Widerstand 2,7 kΩ, 0,25 W | Pull-ups Drehgeber A/B | |
| 3 | Widerstand 270 Ω, 0,25 W | Pull-ups Drehgeber-Taster | |
| 6 | Cherry MX Blue (Platten-Montage, 3 Pins) | falls noch nicht vorhanden | |
| 1 | Lochrasterplatine 100 × 160 mm, Punktraster, Epoxyd | daraus 1 × 70 × 50 und 3 × 20 × 25 sägen | Reichelt |
| 1 m | **WS2812B-Streifen 5 V, 144 LEDs/m, 10 mm breit, IP30** (ohne Silikon) | 4 × 28 LEDs | |
| 2 m | Litze 0,5 mm², 3 Farben | LED-Versorgung und Daten | |
| 1 Set | Dupont-Kabel Buchse–Buchse, 20 cm, 40 Stück | GPIO-Stecker → Tasten, Drehgeber, Steuerplatine | |
| 2 × 0,5 m | Lautsprecherkabel 2 × 0,75 mm² | | |
| 1 | Schrumpfschlauch-Sortiment | | |

## Mechanik und Kleinteile

| Anz. | Teil | Hinweis |
|---|---|---|
| 3 | **Zylinderstift ISO 2338 Ø 3 m6 × 30 mm, Stahl** | Achse vom Drehgeber in den Originalknopf |
| 1 | 2-Komponenten-Epoxidkleber | Stift in Kupplung, Kupplung auf Welle, Tasten auf Adapter |
| 10 | Schraube für Kunststoff 2,5 × 8 (z. B. Spax 2,5 × 8) | 6 × Drehgeberplatinen, 2 × A/E-Platte, 2 Reserve |
| 4 | Abstandsbolzen M2,5 × 6 mm, Innen-/Außengewinde, Messing | Pi auf dem Halter; Außengewinde durch den Pi in den Bolzen zum DigiAMP+ |
| 4 | Zylinderschraube M2,5 × 6 | von unten durch den Pi-Halter in die Bolzen |
| 4 | Schraube für Kunststoff 2,2 × 6,5 oder M2 × 6 | Steuerplatine |
| 8 | Spax 3 × 10 | Pi-Halter und Steuerplatinen-Halter in den Boden |
| 4 | Spax 2,5 × 8 | Träger an die Frontbretter |
| 2 | Spax 2,5 × 10 | Lichtkasten |
| 1 | Bohrer 3,0 mm und 6,0 mm | Kupplungen und Lager nachbohren |
| 1 | Kontaktspray | alter A/E-Schalter |

## 3D-Druck

Siehe `Gehaeuse/DRUCKTEILE.md`: Träger links und rechts, Lichtkasten, Pi-Halter, Steuerplatinen-Halter, A/E-Halteplatte, 3 Kupplungen, 6 Tastenadapter. Filament PETG oder PLA schwarz (Träger), weiß (Lichtkasten).

## Gehäuse

Holz, Leisten, Füße, Magnete, Schrauben: Einkaufsliste in `Gehaeuse/README.md`.
