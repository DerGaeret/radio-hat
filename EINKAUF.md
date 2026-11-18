# Einkaufsliste

Stand 18.11.2026. Links und Preise am 18.11.2026 geprüft (Preise inkl. MwSt., ohne Versand; sie ändern sich). Die bebilderte Erklärung steht auf der Seite [Retro-Radio Technik](https://claude.ai/artifact/NMvpSek8xF2TUQraDzXtam) (privat, nur für den Besitzer) und kurz in `README.md`.

Verglichen wurde Reichelt mit Eckstein: Die Pololu-Module und die Lochrasterplatine gibt es bei Eckstein (günstiger bzw. nur dort), alles andere bei Reichelt (Eckstein führt DigiAMP+, Netzteil, Drehgeber, 74HCT245 usw. nicht). Pololu direkt (USA) ist ohne Versand etwas billiger, mit Versand und Zoll aber teurer.

## Vorhanden

- Raspberry Pi 4B mit Kühlkörper, microSD-Karte
- 3 Anschlussklemmen 2-polig (EIN, VERST, A/E auf der Steuerplatine)
- Vom Originalradio: Frontplatte mit Originalschrauben und -muttern, 2 Lautsprecherabdeckungen, 4 Knöpfe (Bohrung Ø 3 × 17 mm), 6 Tasten, A/E-Schalter (RFT) mit Mutter und Scheibe
- Lautsprecher Sharp VSP0010PBS78A (2 ×)

## Grundausstattung

### Eckstein

| Anz. | Teil | Wofür | Preis | Link |
|---|---|---|---|---|
| 1 | Pololu Big MOSFET Slide Switch with Reverse Voltage Protection, **MP** (#2814) | schaltet die 19 V (Soft-Off) | 6,53 € | [Eckstein](https://eckstein-shop.de/Pololu-Big-MOSFET-Slide-Switch-with-Reverse-Voltage-Protection-MP) |
| 1 | Lochrasterplatine 70 × 90 mm, doppelseitig | daraus Steuerplatine 70 × 50 und 3 × 20 × 25 für die Drehgeber | 1,34 € | [Eckstein](https://eckstein-shop.de/Lochrasterplatine70x90mmExperimentierplatineLC3B6tplatinePrototypeLeiterplattePCB) |

### Reichelt

| Anz. | Teil | Wofür | Preis | Link |
|---|---|---|---|---|
| 1 | Raspberry Pi DigiAMP+ | Verstärker | 32,40 € | [RPI IQ DIGIAMP+](https://www.reichelt.de/de/de/shop/produkt/raspberry_pi_shield_-_iqaudio_digiamp_-295715) |
| 1 | Tischnetzteil Mean Well GST90A19-P1M, 19 V, 4,74 A, Stecker 5,5 × 2,5 | Stromversorgung | 32,70 € | [MW GST90A19](https://www.reichelt.de/de/de/shop/produkt/tischnetzteil_90_w_19_v_4_74_a-171060) |
| 1 | Netzkabel Schutzkontakt → C13 | zum Netzteil | 2,85 € | [NKSK 200 SW](https://www.reichelt.de/de/de/shop/produkt/netzkabel_schutzkontaktstecker_gew_1_8_-_2_0_m_schw_c13-13490) |
| 1 | Einbaubuchse DC 5,5 × 2,5, M8, Lötanschluss | Rückwanddeckel (Loch Ø 8) | 5,75 € | [DELOCK 90188](https://www.reichelt.de/de/de/shop/produkt/steckverbinder_dc_5_5_x_2_5_mm_buchse_zum_einbau_loetversion-371067) |
| 1 | Hohlstecker 5,5 × 2,5 mit Knickschutz | Kabel zum DigiAMP+ | 1,25 € | [LUM 1634-02](https://www.reichelt.de/de/de/shop/produkt/hohlstecker_knickschutz_aussen_5_5_mm_innen_2_5_mm-139689) |
| 1 | Silikonkabel 0,75 mm², 2 m, rot/schwarz | 19-V-Leitungen | 3,20 € | [SIK 275 2](https://www.reichelt.de/de/de/shop/produkt/silikonkabel_0_75_mm_2_m_schwarz_rot-149542) |
| 2 | Schottky-Diode BAT 85 | A/E-Erkennung | 2 × 0,08 € | [BAT 85](https://www.reichelt.de/de/de/shop/produkt/schottkydiode_30_v_0_2_a_do-35-4857) |
| 6 | Widerstand 10 kΩ | Drehgeber A und B | 6 × 0,07 € | [METALL 10,0K](https://www.reichelt.de/de/de/shop/produkt/widerstand_metallschicht_10_0_kohm_0207_0_6_w_1_-11449) |
| 1 | Stiftleiste 1 × 40, 2,54 mm | Pololu-Modul, Anschluss zum Pi | 0,78 € | [SL40G1B](https://www.reichelt.de/de/de/shop/produkt/stiftleiste_1x40_polig_gerade_2_54_mm_laenge_12_6_mm-404318) |
| 3 | ALPS STEC12E07 (24 Impulse, 24 Rastungen, ohne Taster) | Klang, Lautstärke, Sender | 3 × 1,80 € | [STEC12E07](https://www.reichelt.de/de/de/shop/produkt/drehimpulsegeber_24_impulse_24_rastungen_vertikal-73922) |
| 6 | Cherry MX Blue, Schnappbefestigung | Tasten | 6 × 0,55 € | [MX2A-E1NN](https://www.reichelt.de/de/de/shop/produkt/cherry_mx_blue_-_tastenmodul_-_schnappbefestigung-401639) |
| 1 | Steckbrückenkabel 40-polig, Buchse–Buchse, 20 cm | Tasten, Drehgeber, Steuerplatine an den GPIO-Stecker (ein Ende abschneiden und anlöten) | 1,60 € | [DEBO KABELSET12](https://www.reichelt.de/de/de/shop/produkt/entwicklerboards_-_steckbrueckenkabel_40_pole_f_f_20_cm-282700) |
| 1 | Lautsprecherkabel 2 × 0,75 mm², 5 m | Lautsprecher | 0,78 € | [TME KL1-5 GL](https://www.reichelt.de/de/de/shop/produkt/lautsprecherkabel_2x0_75_mm_grau_5m-ring-375320) |
| 1 | Schrumpfschlauch-Sortiment | Lötstellen | 5,35 € | [DELOCK 86271](https://www.reichelt.de/de/de/shop/produkt/schrumpfschlauch-sortiment_schwarz_100-teilig-152924) |

### Sonstiges

| Anz. | Teil | Wofür | Link |
|---|---|---|---|
| 3 | Zylinderstift ISO 2338, Ø 3 m6 × 30 mm, Stahl | Achse in den Knopf | [Suche Amazon](https://www.amazon.de/s?k=Zylinderstift+3x30+ISO+2338) |
| 1 | 2K-Epoxidkleber, beliebige Marke (z. B. UHU Plus schnellfest, Pattex 5 Minuten) | Stift in Kupplung, Tasten auf Adapter | Baumarkt/Drogerie |
| 8 | Schraube für Kunststoff 2,5 × 8 (Spax 2,5 × 8 geht auch) | Drehgeberplatinen, A/E-Platte | Baumarkt |
| 4 | Schraube 2,2 × 6,5 (oder M2 × 6 selbstschneidend) | Steuerplatine | Baumarkt |
| 8 | Spax 3 × 10 | Pi- und Steuerplatinen-Halter in den Boden | Baumarkt |
| 6 | Spax 2,5 × 8 / 2,5 × 10 | Träger, Lichtkasten | Baumarkt |
| (4) | Schraube M2,5 × 25 *(nur falls beim DigiAMP+ keine Abstandsbolzen liegen; dann die Hülsen `pi_huelsen` drucken)* | DigiAMP+ und Pi auf den Halter | Baumarkt |
| je 1 | Bohrer 3,0 und 6,0 mm | Kupplungen nachbohren | Baumarkt |

Die Frontplatte wird mit den Originalschrauben und -muttern durch die Frontbretter geschraubt; dafür ist nichts zu kaufen.

Summe Grundausstattung (Eckstein + Reichelt) ohne Sonstiges und Versand: etwa 104 €.

## Optional: Skalenbeleuchtung

Nur nötig, wenn die Skala leuchten soll (LED-Streifen mit Senderzeiger). Ohne sie entfällt auch der gedruckte Lichtkasten.

| Anz. | Teil | Wofür | Preis | Link |
|---|---|---|---|---|
| 1 | Pololu 5V, 1A Step-Down D24V10F5 (#2831) | 5 V für die LEDs (Software-Grenze 0,8 A) | 15,41 € | [Eckstein](https://eckstein-shop.de/Pololu5V2C1AStep-DownSpannungsreglerD24V10F5) |
| 1 m | WS2812B-Streifen 5 V, **144 LEDs/m**, 10 mm breit, IP30 | 4 × 28 LEDs (Reichelt hat nur 30 und 60/m) | ca. 10–15 € | [Suche Amazon](https://www.amazon.de/s?k=WS2812B+144+LEDs+1m+IP30+5V) |
| 1 | 74HCT245, DIP-20 | Pegelwandler | 1,15 € | [Reichelt](https://www.reichelt.de/de/de/shop/produkt/octal_bus_puffer_3-state_4_5_5_5_v_dil-20-3356) |
| 1 | IC-Sockel 20-polig | für 74HCT245 | 0,08 € | [Reichelt](https://www.reichelt.de/de/de/shop/produkt/ic-sockel_20-polig_doppelter_federkontakt-8212) |
| 1 | Widerstand 330 Ω | LED-Daten | 0,07 € | [Reichelt](https://www.reichelt.de/de/de/shop/produkt/widerstand_metallschicht_330_ohm_0207_0_6_w_1_-11733) |
| 2 | Elko 1000 µF, 10 V | Wandler und Lichtkasten | 2 × 0,14 € | [Reichelt](https://www.reichelt.de/de/de/shop/produkt/elko_radial_1000_f_10_v_105_rm_5-359138) |
| 1 | Kondensator 100 nF, RM 5 | am 74HCT245 | 0,29 € | [Reichelt](https://www.reichelt.de/de/de/shop/produkt/mks2_pet-kondensator_100_nf_10_63_vdc_rm_5-12349) |
| 1 | Anschlussklemme 3-polig, RM 5,08 | LED | 0,39 € | [Reichelt](https://www.reichelt.de/de/de/shop/produkt/anschlussklemme_3-pol_2_mm_rm_5_08-36606) |
| 2 m | Litze 0,5 mm², 3 Farben | Kabel zum Lichtkasten | – | [Suche Amazon](https://www.amazon.de/s?k=Litze+0%2C5mm%C2%B2+Set+Farben) |

Heller: statt D24V10F5 den Pololu D36V28F5 (3,2 A, [Eckstein 26,12 €](https://eckstein-shop.de/Pololu-5V-32A-Step-Down-Voltage-Regulator-D36V28F5-Input-Voltage-up-to-50V)), Software-Grenze dann 2 A.

## 3D-Druck

Siehe `Gehaeuse/DRUCKTEILE.md`: Träger links und rechts, Pi-Halter, Steuerplatinen-Halter, A/E-Halteplatte, 3 Kupplungen, ggf. 4 Hülsen, 6 Tastenadapter; optional Lichtkasten. PETG oder PLA, Träger schwarz, Lichtkasten weiß.

## Gehäuse

Holz, Leisten, Füße, Magnete, Schrauben: Einkaufsliste in `Gehaeuse/README.md`.
