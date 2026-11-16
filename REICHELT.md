# Bestellliste Reichelt (Stand 16.11.2026)

Die Liste enthält alles, was JLCPCB nicht bestückt und was laut deiner Angabe noch fehlt. Schraubklemmen J2–J4 und das 20-V-Netzteil hast du schon, sie stehen nicht auf der Liste. Tasten, Encoder und Ein/Aus-Schalter sind laut README ebenfalls vorhanden. Sockel J1 und die Elkos C1/C2 stehen auf der Liste, weil ich annehme, dass sie fehlen; falls du sie hast, streichen.

Die Mengen gelten für eine Platine. Für beide bestückten Platinen alles verdoppeln. Artikelnummern stammen aus Suchtreffern der Reichelt-Seiten; Preis und Lagerbestand vor dem Bestellen im Shop prüfen.

| Menge | Reichelt-Bestellnummer | Bezeichnung | Wofür |
|---|---|---|---|
| 1 | BKL 10120963 | Buchsenleiste 2×20, RM 2,54, gerade, 8,5 mm hoch | J1, Sockel zum Pi |
| 2 | RAD FC 470/35 | Elko radial 470 µF, 35 V, 105 °C, 10 × 20 mm, RM 5 (Panasonic FC) | C1, C2 |
| 7 | JST XH2P ST | Stiftleiste XH gerade, 2-polig (B2B-XH-A) | S1–S6, X1 |
| 3 | Reichelt-Artikel 185075 (voraussichtlich JST XH4P ST) | Stiftleiste XH gerade, 4-polig (B4B-XH-A) | E1–E3 |
| 7 | JST XH2P BU | Buchsengehäuse XH, 2-polig (XHP-2) | Kabel zu Tasten und Schalter |
| 3 | JST XH4P BU | Buchsengehäuse XH, 4-polig (XHP-4) | Kabel zu den Encodern |
| 40 | JST XH CKB | Crimpkontakt XH, Buchse, 28–22 AWG (BXH-001T-P0.6) | 26 Kontakte gebraucht, Rest Reserve |
| 1 | RPI MOUNTINGKIT4 | Abstandshalter-Set M2,5 für Raspberry Pi | Befestigung am Pi und im Gehäuse |

## Hinweise

- **Sockel J1:** Der Abstand von 11 mm zwischen Pi und Platine ergibt sich aus 8,5 mm Buchsenhöhe plus dem Kunststoffsockel der Pi-Stiftleiste. Eine höhere „Stacking“-Leiste passt nicht zu den Abstandshaltern.
- **Elkos:** 35 V ist das Minimum bei 20 V Versorgung. Die Bohrungen haben 1,0 mm bei 5 mm Abstand, der Aufdruck 10 mm Durchmesser. Die Bestellnummer `RAD FR 470/35` hat 3,5 mm Raster und passt nicht. Gleichwertig mit bestätigten Maßen (10 × 20 mm, RM 5): `RAD LXZ 35-470`, https://www.reichelt.com/de/en/elko-radial-470-f-35-v-105-low-esr-10x20-mm-rm-5-rad-lxz-35-470-p166408.html
- **Crimpkontakte:** Alternative für sehr dünne Litze (30–26 AWG, 0,05–0,13 mm²) ist `JST XH2 CKS`. Zum Crimpen braucht es eine Zange für JST-Kontakte. Wer keine hat, nimmt statt Gehäusen und Kontakten fertig konfektionierte XH-Kabel (2-polig und 4-polig).
- **Abstandshalter:** Das Set enthält 10-mm-Bolzen. Der fehlende Millimeter wird laut README mit Unterlegscheiben ausgeglichen; ob Scheiben im Set liegen, auf der Artikelseite prüfen. Wegen der Kupferfläche nahe an den Löchern am besten Kunststoffscheiben verwenden.
- **Nicht geprüft:** Schaltlitze, Lötzinn und ein Gehäuse stehen nicht auf der Liste.

## Quellen

- https://www.reichelt.com/de/en/shop/product/female_header_2_54mm_straight_2x20-266688
- https://www.reichelt.com/de/en/jst-pin-header-straight-1x2-pin-xh-jst-xh2p-st-p185073.html
- https://www.reichelt.com/de/en/shop/product/jst_pin_header_straight_1x4-pin_xh-185075
- https://www.reichelt.com/de/en/shop/product/jst_socket_housing_1x2-pin_xh-185085
- https://reichelt.com/de/en/jst-socket-housing-1x4-pin-xh-jst-xh4p-bu-p185087.html
- https://www.reichelt.com/de/en/jst-crimp-contact-socket-xh-jst-xh-ckb-p185091.html
- https://www.reichelt.com/de/en/shop/product/raspberry_pi_spacer_kit_m2_5-223625
