# Bestellliste Reichelt (Stand 16.11.2026)

Die Liste enthält alles, was JLCPCB nicht bestückt und was laut deiner Angabe noch fehlt. Schraubklemmen J2–J4 und das 20-V-Netzteil hast du schon. Tasten, Encoder und Ein/Aus-Schalter sind laut README ebenfalls vorhanden. Sockel J1 und die Elkos C1/C2 stehen auf der Liste, weil ich annehme, dass sie fehlen; falls du sie hast, streichen.

Die Mengen gelten für eine Platine. Für beide bestückten Platinen alles verdoppeln. Bestellnummern und Links stammen aus Suchtreffern der Reichelt-Seiten; Preis und Lagerbestand vor dem Bestellen im Shop prüfen.

| Menge | Bestellnummer | Bezeichnung | Wofür | Link |
|---|---|---|---|---|
| 1 | BKL 10120963 | Buchsenleiste 2×20, RM 2,54, gerade, 8,5 mm hoch | J1, Sockel zum Pi | [Artikel](https://www.reichelt.com/de/en/shop/product/female_header_2_54mm_straight_2x20-266688) |
| 2 | RAD LXZ 35-470 | Elko radial 470 µF, 35 V, 105 °C, Low ESR, 10 × 20 mm, RM 5 | C1, C2 | [Artikel](https://www.reichelt.com/de/en/elko-radial-470-f-35-v-105-low-esr-10x20-mm-rm-5-rad-lxz-35-470-p166408.html) |
| 7 | JST XH2P ST | Stiftleiste XH gerade, 2-polig (B2B-XH-A) | S1–S6, X1 | [Artikel](https://www.reichelt.com/de/en/jst-pin-header-straight-1x2-pin-xh-jst-xh2p-st-p185073.html) |
| 3 | JST XH4P ST (Artikel 185075) | Stiftleiste XH gerade, 4-polig (B4B-XH-A) | E1–E3 | [Artikel](https://www.reichelt.com/de/en/shop/product/jst_pin_header_straight_1x4-pin_xh-185075) |
| 7 | JST XH2P BU | Buchsengehäuse XH, 2-polig (XHP-2) | Kabel zu Tasten und Schalter | [Artikel](https://www.reichelt.com/de/en/shop/product/jst_socket_housing_1x2-pin_xh-185085) |
| 3 | JST XH4P BU | Buchsengehäuse XH, 4-polig (XHP-4) | Kabel zu den Encodern | [Artikel](https://reichelt.com/de/en/jst-socket-housing-1x4-pin-xh-jst-xh4p-bu-p185087.html) |
| 40 | JST XH CKB | Crimpkontakt XH, Buchse, 28–22 AWG (BXH-001T-P0.6) | 26 Kontakte gebraucht, Rest Reserve | [Artikel](https://www.reichelt.com/de/en/jst-crimp-contact-socket-xh-jst-xh-ckb-p185091.html) |
| 1 | RPI MOUNTINGKIT4 | Abstandshalter-Set M2,5 für Raspberry Pi | Befestigung am Pi und im Gehäuse | [Artikel](https://www.reichelt.com/de/en/shop/product/raspberry_pi_spacer_kit_m2_5-223625) |

## Hinweise

- **Sockel J1:** Der Abstand von 11 mm zwischen Pi und Platine ergibt sich aus 8,5 mm Buchsenhöhe plus dem Kunststoffsockel der Pi-Stiftleiste. Eine höhere „Stacking“-Leiste passt nicht zu den Abstandshaltern.
- **Elkos:** 35 V ist das Minimum bei 20 V Versorgung. Die Bohrungen haben 1,0 mm bei 5 mm Abstand, der Aufdruck 10 mm Durchmesser. Gleichwertig ist `RAD FC 470/35` (Panasonic FC, ebenfalls 10 × 20 mm, RM 5). `RAD FR 470/35` hat 3,5 mm Raster und passt nicht.
- **Stiftleiste 4-polig:** Die Artikelseite 185075 zeigt die Herstellernummer B4B-XH-A. Dass die Bestellnummer dort `JST XH4P ST` lautet, ist aus der Benennung der anderen Polzahlen geschlossen.
- **Crimpkontakte:** Alternative für sehr dünne Litze (30–26 AWG, 0,05–0,13 mm²) ist `JST XH2 CKS`. Zum Crimpen braucht es eine Zange für JST-Kontakte. Wer keine hat, nimmt statt Gehäusen und Kontakten fertig konfektionierte XH-Kabel (2-polig und 4-polig).
- **Abstandshalter:** Das Set enthält 10-mm-Bolzen. Der fehlende Millimeter wird laut README mit Unterlegscheiben ausgeglichen; ob Scheiben im Set liegen, auf der Artikelseite prüfen. Seit der zehnten Fassung (Änderung 25) liegt um die Löcher in 6 mm Durchmesser nur Massefläche; Scheiben und Bolzen aus Metall sind in Ordnung.
- **Lötzinn:** Für ein Gerät, das verkauft wird, bleifreies Lot (zum Beispiel Sn99,3Cu0,7 oder SAC305 mit Flussmittelseele) verwenden; bleihaltiges Lot verstößt gegen RoHS.
- **Nicht geprüft:** Schaltlitze, Lötzinn und ein Gehäuse stehen nicht auf der Liste.
