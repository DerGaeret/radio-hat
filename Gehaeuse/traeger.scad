// 3D-Druckteile für das Technikfach – alle Maße in mm
// Koordinaten der Frontteile: px = ab linker Kante der Frontplatte, pz = ab Unterkante der Frontplatte,
// y = Tiefe wie im Gehäuse (Frontplatte vorne y=7, hinten y=10).
// Ansicht/Export: teil = "alle" | "traeger_links" | "traeger_rechts" | "lichtkasten" | "pi_halter" | "tastenadapter"
//                  | "kupplung" | "ae_platte" | "steuer_halter"
teil = "alle";
$fn = 40;

/* ---------- Frontplatte (gemessen) ---------- */
pl_b = 300;  pl_h = 114;  pl_vorne = 7;  pl_hinten = 10;
knoepfe   = [[29,33],[54,33],[104,33],[264,33]];   // A/E, Klang, Lautstärke, Sender
loch_d    = 10;
fenster   = 13;                                      // Tastenfenster 13 x 13
tasten_x  = [for (i=[0:5]) 126 + fenster/2 + i*20];  // 132.5 ... 232.5
tasten_z  = 7 + fenster/2;                           // 13.5
// durchsichtige Stellen (aus dem Foto, ±1,5 mm): Unterkante, Oberkante
schlitze  = [[56.5,61.5],[69,74.5],[79.5,89],[94,99.5]];  // U, K, Stationen, L
schlitz_x = [33, 222.5];

/* ---------- Original-Befestigung der Frontplatte ---------- */
// Untere Eckbohrungen (aus dem Foto: 19 mm vom Rand, pz ca. 11): Originalschraube durch Frontplatte und
// Frontbrett, Mutter hinten. Der Flansch des Trägers bekommt dort eine Aussparung.
fp_schraube = [19, 11];
fp_mutter_d = 10;    // Platz für Mutter (bis M4) und Scheibe

/* ---------- Gehäuse-Bezug ---------- */
fb_kante  = 22;     // Frontbretter reichen 22 mm hinter die Frontplatte
fb_hinten = 18;     // Rückseite der Frontbretter
boden_pz  = -4;     // Innenseite Boden (z = 8) in Frontplatten-Koordinaten
deckel_pz = 118;    // Innenseite Deckel

/* ---------- Bauteile ---------- */
// Originalknöpfe: 19 mm lang + 3 mm Nase, Bohrung Ø 3 x 17 mm tief (Nutzer, 18.11.2026).
knopf_hinten = pl_vorne - 0.5;          // 6.5: Rückseite des Knopfs, 0,5 mm vor der Frontplatte
knopf_bohr   = 17;
stift_tief   = 16;                      // so weit steckt die Achse im Knopf (1 mm Reserve)
stift_spitze = knopf_hinten - stift_tief;   // -9.5
// Drehgeber ALPS STEC11B03: Körper 11,6 x 12 x 6,5, runde geschlitzte Welle Ø 6 x 25 mm ab Montagefläche
enc_welle  = 25;
enc_tief   = 6.5;
// Kupplung: Zylinderstift ISO 2338 Ø 3 x 30 (Stahl) vorne, Drehgeberwelle hinten
stift_l    = 30;
kup_d      = 11;  kup_vorne = 13.8;  kup_l = 16;
kup_stift  = stift_spitze + stift_l - kup_vorne + 0.5;   // 7.2: Tiefe der Stiftbohrung
kup_welle_tief = 8;                                       // Welle steckt 8 mm in der Kupplung
enc_vorne  = kup_vorne + kup_l - kup_welle_tief + enc_welle;   // 46.8: Montagefläche Drehgeber
lr_b = 20;  lr_h = 25;  lr_t = 1.6;      // Lochrasterplatine je Drehgeber
// Original-A/E-Schalter (RFT): Maße aus dem Foto GESCHÄTZT, vor dem Druck nachmessen.
rft_a       = 41;    // Anlagefläche (Flansch) bis Wellenende
rft_buchse  = 8;     // Gewindebuchse ab Flansch
rft_loch    = 10.5;  // Loch in der Halteplatte (passt für Gewinde M8 bis M10)
rft_koerper = 25;    // Gehäuse-Ø
rft_tief    = 13;    // Gehäusetiefe hinter dem Flansch
ae_platte_t = 3;
ae_flansch_y = stift_spitze + rft_a;          // 31.5: Flansch liegt an der Rückseite der Halteplatte
ae_platte_y  = ae_flansch_y - ae_platte_t;    // 28.5
ae_saeulen   = [[0,-13],[13,0]];             // Schraubsäulen relativ zur Achse (dx, dz)
// Cherry MX: Montageplatte 1,5 mm, Ausschnitt 14 x 14
mx_ausschnitt = 14;  mx_platte = 1.5;
// Tastenkappe 18 lang, 1 mm vor der Holzkante; Adapter: Platte 2 mm + Stößel 6 mm
kappe_l   = 18;  kappe_vor = 8;                     // ragt 8 mm vor die Frontplatte
kappe_hinten = pl_vorne - kappe_vor + kappe_l;      // 17
adapter_platte = 2;  adapter_stoessel = 6;
mx_schieber = kappe_hinten + adapter_platte + adapter_stoessel;  // 25: Oberkante Schieber
mx_platte_y = mx_schieber + 1 + 6.6;                // 32.6: Vorderseite der Schalterplatte

/* ---------- Träger ---------- */
wand_y0 = pl_hinten + 0.3;  wand_t = 3;  wand_y1 = wand_y0 + wand_t;
tr_unten = boden_pz + 0.5;  tr_oben = 49.3;
teilung  = 118;             // Trennung linker/rechter Träger
tiefe_tr = 40;              // Träger reicht bis y = 40

module frontwand(x0, x1) {
  difference() {
    translate([x0, wand_y0, tr_unten]) cube([x1-x0, wand_t, tr_oben-tr_unten]);
    for (i=[0:3]) translate([knoepfe[i][0], wand_y0-1, knoepfe[i][1]]) rotate([-90,0,0])
      cylinder(d=(i==0 ? 6 : 3.4), h=wand_t+2);   // A/E: Welle frei; Drehgeber: Lager für den 3-mm-Stift
    for (x=tasten_x) translate([x-(fenster+0.6)/2, wand_y0-1, tasten_z-(fenster+0.6)/2]) cube([fenster+0.6, wand_t+2, fenster+0.6]);
  }
}

module drehgeber_turm(k) {   // Rohr für die Kupplung, zwei Säulen für die Lochrasterplatine
  x = k[0]; z = k[1];
  difference() {
    union() {
      translate([x-8, wand_y1, z-8]) cube([16, enc_vorne-wand_y1, 16]);
      for (dz=[-9.5,9.5]) translate([x, wand_y1, z+dz]) rotate([-90,0,0])
        cylinder(d=6, h=enc_vorne+enc_tief-wand_y1);
    }
    translate([x, wand_y1-0.01, z]) rotate([-90,0,0]) cylinder(d=kup_d+0.8, h=60);
    for (dz=[-9.5,9.5]) translate([x, enc_vorne, z+dz]) rotate([-90,0,0]) cylinder(d=2.2, h=20);
  }
}

module ae_turm(k) {   // zwei Säulen für die Halteplatte des Original-A/E-Schalters
  for (d=ae_saeulen) difference() {
    translate([k[0]+d[0], wand_y1, k[1]+d[1]]) rotate([-90,0,0]) cylinder(d=6, h=ae_platte_y-wand_y1);
    translate([k[0]+d[0], wand_y1+2, k[1]+d[1]]) rotate([-90,0,0]) cylinder(d=2.2, h=40);
  }
}

module ae_platte() {   // in Gehäusekoordinaten um die A/E-Achse; Schalter mit seiner Mutter festschrauben
  k = knoepfe[0];
  difference() {
    translate([k[0]-12, ae_platte_y, k[1]-18]) cube([28, ae_platte_t, 31]);
    translate([k[0], ae_platte_y-1, k[1]]) rotate([-90,0,0]) cylinder(d=rft_loch, h=10);
    for (d=ae_saeulen) translate([k[0]+d[0], ae_platte_y-1, k[1]+d[1]]) rotate([-90,0,0]) cylinder(d=2.8, h=10);
  }
}

module kupplung() {   // Achse z: vorne (z=0) Stiftbohrung Ø 3, hinten Bohrung Ø 6 für die Drehgeberwelle
  difference() {
    cylinder(d=kup_d, h=kup_l);
    translate([0,0,-1]) cylinder(d=3.0, h=kup_stift+1);
    translate([0,0,kup_l-kup_welle_tief]) cylinder(d=6.0, h=kup_welle_tief+1);
  }
}

module leiste_oben(x0, x1) { translate([x0, wand_y0, tr_oben-3]) cube([x1-x0, tiefe_tr-wand_y0, 3]); }
module leiste_unten(x0, x1) { translate([x0, wand_y0, tr_unten]) cube([x1-x0, 22, 2.5]); }

module flansch(links=true) {   // wird hinten an das Frontbrett geschraubt (2 Spax 2,5 x 8)
  x0 = links ? 2 : pl_b-fb_kante;
  difference() {
    union() {
      translate([x0, fb_hinten+0.3, tr_unten+4]) cube([fb_kante-2, 3, 40]);
      translate([links ? fb_kante-0.5 : pl_b-fb_kante-2, wand_y0, tr_unten+4]) cube([2.5, fb_hinten+3.3-wand_y0, 40]);
    }
    for (z=[tr_unten+22, tr_unten+38]) translate([links ? 11 : pl_b-11, fb_hinten-1, z]) rotate([-90,0,0]) {
      cylinder(d=3, h=10); translate([0,0,4.3]) cylinder(d1=3, d2=6, h=1.5);
    }
    // Aussparung für Mutter und Schraubenende der unteren Original-Frontplattenschraube
    translate([(links ? fp_schraube[0] : pl_b-fp_schraube[0]) - fp_mutter_d/2 - 0.1, fb_hinten-1, fp_schraube[1] - fp_mutter_d/2]) cube([fp_mutter_d+0.2, 6.3, fp_mutter_d]);
  }
}

module traeger_links() {
  x0 = fb_kante + 0.5; x1 = teilung - 0.2;
  difference() {
    union() {
      frontwand(x0, x1);
      ae_turm(knoepfe[0]);
      for (i=[1:2]) drehgeber_turm(knoepfe[i]);
      leiste_oben(x0, x1); leiste_unten(x0, x1);
      flansch(true);
      translate([x1-10, wand_y1, 0]) cube([16, 3, 9]);              // Lasche zum rechten Träger
      translate([55, wand_y0, tr_oben-3]) cube([20, 32-wand_y0+8, 3]); // Auflage Lichtkasten
    }
    translate([x1+3, wand_y1-1, 4.5]) rotate([-90,0,0]) cylinder(d=2.5, h=10);
    translate([65, 35, tr_oben-10]) cylinder(d=2.5, h=20);         // Schraube Lichtkasten
  }
}

module tastenschacht() {   // Halter für 6 Cherry MX
  x0 = tasten_x[0]-11; x1 = tasten_x[5]+11; z0 = tr_unten; z1 = 28;
  difference() {
    union() {
      translate([x0, mx_platte_y, z0]) cube([x1-x0, mx_platte, z1-z0]);
      for (x=[x0, x1-2]) translate([x, wand_y1, z0]) cube([2, mx_platte_y+mx_platte-wand_y1, z1-z0]);
      translate([x0, wand_y1, z1-2]) cube([x1-x0, mx_platte_y+mx_platte-wand_y1, 2]);
    }
    for (x=tasten_x) translate([x-mx_ausschnitt/2, mx_platte_y-1, tasten_z-mx_ausschnitt/2]) cube([mx_ausschnitt, 5, mx_ausschnitt]);
  }
}

module traeger_rechts() {
  x0 = teilung + 0.2; x1 = pl_b - fb_kante - 0.5;
  difference() {
    union() {
      frontwand(x0, x1);
      tastenschacht();
      drehgeber_turm(knoepfe[3]);
      leiste_oben(x0, x1); leiste_unten(x0, x1);
      flansch(false);
      translate([185, wand_y0, tr_oben-3]) cube([20, 32-wand_y0+8, 3]);
    }
    translate([teilung+3, wand_y0-1, 4.5]) rotate([-90,0,0]) cylinder(d=2.5, h=10);
    translate([195, 35, tr_oben-10]) cylinder(d=2.5, h=20);
  }
}

/* ---------- Lichtkasten hinter der Skala ---------- */
lk_x0 = 28;  lk_x1 = 228;  lk_z0 = 49.5;  lk_z1 = 105.5;
lk_diffusor = 0.8;  lk_wand = 1.6;  lk_hinten = 30;
lk_trenn = [65, 78, 91.5];      // Trennwände zwischen den Reihen

module lichtkasten() {
  difference() {
    union() {
      translate([lk_x0, wand_y0, lk_z0]) cube([lk_x1-lk_x0, lk_hinten-wand_y0, lk_z1-lk_z0]);
      for (x=[65, 195]) translate([x-10, lk_hinten-2, lk_z0]) cube([20, 10, 3]);   // Schraublaschen
    }
    // Kammern: vorne bleibt der Diffusor stehen, hinten die Rückwand für die LED-Streifen
    zs = concat([lk_z0+lk_wand], lk_trenn, [lk_z1-lk_wand]);
    for (i=[0:3]) {
      za = i==0 ? zs[0] : zs[i]+0.6;  zb = i==3 ? zs[4] : zs[i+1]-0.6;
      translate([lk_x0+lk_wand, wand_y0+lk_diffusor, za]) cube([lk_x1-lk_x0-2*lk_wand, lk_hinten-2-wand_y0-lk_diffusor, zb-za]);
    }
    for (x=[65, 195]) translate([x, lk_hinten+3, lk_z0-1]) cylinder(d=3.2, h=6);
    translate([lk_x1-12, lk_hinten-3, lk_z0+8]) cube([8, 4, lk_z1-lk_z0-16]);    // Kabeldurchführung
  }
}

/* ---------- Halter für Raspberry Pi + DigiAMP+ (Gehäusekoordinaten) ---------- */
// Der DigiAMP+ (58 x 65 mm) sitzt direkt auf dem Pi, mit den Abstandsbolzen aus seinem Lieferumfang
// auf den vier Pi-Löchern. Der Halter trägt nur den Pi: auf jedem Sockel ein Abstandsbolzen M2,5 x 6
// Innen/Außen, von unten mit M2,5 x 8 angeschraubt; sein Außengewinde geht durch den Pi in den Bolzen zum DigiAMP+.
// Der Pi liegt mit der GPIO-Kante nach vorne: Hohlbuchse und Lautsprecherklemmen des DigiAMP+ sitzen
// an der gegenüberliegenden Kante und zeigen so zur Rückwand. USB/Ethernet zeigen nach links (-x).
pi_gpio_y = 65;    // GPIO-Kante des Pi (Gehäuse-y), Pi reicht nach hinten bis y = 121 (hinter den Drehgebern)
pi_x0     = 290;   // linke Kante des Pi (Gehäuse-x, USB-Seite)
boden_z   = 8;
sockel_h  = 3;     // Sockel auf der Halterplatte
bolzen_h  = 6;     // Abstandsbolzen M2,5 x 6 Innen/Außen
pi_hoehe  = sockel_h + bolzen_h;   // Pi-Unterseite über der Halterplatte
amp_abst  = 9;     // Abstand Pi-Platine zu DigiAMP+-Platine, nur für die Vorschau (Bolzen aus dem Lieferumfang)
ph_t      = 2.5;
pi_loecher  = [[3.5,3.5],[61.5,3.5],[3.5,52.5],[61.5,52.5]];   // Pi-Koordinaten (y ab GPIO-Kante Richtung Pi)
function pi2g(p) = [pi_x0 + 85 - p[0], pi_gpio_y + p[1]];   // um 180° gedreht

module pi_halter() {
  x0 = pi_x0-6; x1 = pi_x0+91; y0 = pi_gpio_y-6; y1 = pi_gpio_y+62;
  difference() {
    union() {
      translate([x0, y0, boden_z]) cube([x1-x0, y1-y0, ph_t]);
      for (p=pi_loecher) translate([pi2g(p)[0], pi2g(p)[1], boden_z]) cylinder(d=8, h=ph_t+sockel_h);
    }
    for (p=pi_loecher) translate([pi2g(p)[0], pi2g(p)[1], boden_z-1]) {      // M2,5 x 8 von unten
      cylinder(d=2.8, h=20); cylinder(d=5.5, h=1+2.5);
    }
    for (x=[x0+5, x1-5], y=[y0+5, y1-5]) translate([x, y, boden_z-1]) {   // Spax 3 x 10 in den Boden
      cylinder(d=3.2, h=10); translate([0,0,ph_t-0.5]) cylinder(d=6.5, h=10);
    }
    translate([x0+20, y0+14, boden_z-1]) cube([x1-x0-40, y1-y0-28, 5]);       // Material sparen
  }
}

/* ---------- Halter für die Steuerplatine (Lochraster 50 x 70) ---------- */
// Trägt Pololu-Schaltmodul, 5-V-Wandler, Pegelwandler und Anschlüsse. Lochabstand nachmessen.
st_x0 = 392;  st_y0 = 78;          // linke vordere Ecke der Lochrasterplatine (Gehäuse)
st_gr = [70, 50];  st_loch = [66, 46];
module steuer_halter() {
  x0 = st_x0-6; y0 = st_y0-6; x1 = st_x0+st_gr[0]+6; y1 = st_y0+st_gr[1]+6;
  lp = [for (i=[0,1], j=[0,1]) [st_x0+(st_gr[0]-st_loch[0])/2+i*st_loch[0], st_y0+(st_gr[1]-st_loch[1])/2+j*st_loch[1]]];
  difference() {
    union() {
      translate([x0, y0, boden_z]) cube([x1-x0, y1-y0, ph_t]);
      for (p=lp) translate([p[0], p[1], boden_z]) cylinder(d=6, h=ph_t+8);
    }
    for (p=lp) translate([p[0], p[1], boden_z+1]) cylinder(d=1.8, h=20);   // M2 selbstschneidend
    for (x=[x0+5, x1-5], y=[y0+5, y1-5]) translate([x, y, boden_z-1]) {
      cylinder(d=3.2, h=10); translate([0,0,ph_t-0.5]) cylinder(d=6.5, h=10);
    }
    translate([x0+16, y0+14, boden_z-1]) cube([x1-x0-32, y1-y0-28, 5]);
  }
}

/* ---------- Tastenadapter: Cherry-MX-Kreuz -> Tastenkappe (wird angeklebt) ---------- */
module tastenadapter() {
  difference() {
    union() {
      translate([-5.5, -5.5, 0]) cube([11, 11, adapter_platte]);
      cylinder(d=5.5, h=adapter_platte+adapter_stoessel);
    }
    // Kreuz 4,1 x 1,3 mm mit 0,1 mm Spiel, 4 mm tief
    translate([0,0,adapter_platte+adapter_stoessel-4]) {
      translate([-2.1,-0.7,0]) cube([4.2,1.4,5]); translate([-0.7,-2.1,0]) cube([1.4,4.2,5]);
    }
  }
}

/* ---------- Platzhalter (nur Ansicht) ---------- */
module bauteile_vorschau() {
  for (i=[0:3]) { k = knoepfe[i];
    color("Silver") translate([k[0], knopf_hinten, k[1]]) rotate([90,0,0]) cylinder(d1=16, d2=15, h=19);
    if (i > 0) {
      color("LightGray") translate([k[0], stift_spitze, k[1]]) rotate([-90,0,0]) cylinder(d=3, h=stift_l);
      color("Orange") translate([k[0], kup_vorne, k[1]]) rotate([-90,0,0]) kupplung();
      color("DarkSlateGray") translate([k[0]-6, enc_vorne, k[1]-6]) cube([12, enc_tief, 12]);
      color("SeaGreen") translate([k[0]-lr_b/2, enc_vorne+enc_tief, k[1]-lr_h/2]) cube([lr_b, lr_t, lr_h]);
    }
  }
  k = knoepfe[0];
  color("LightGray") translate([k[0], stift_spitze, k[1]]) rotate([-90,0,0]) cylinder(d=3.5, h=rft_a);
  color("DimGray") translate([k[0], ae_flansch_y-rft_buchse, k[1]]) rotate([-90,0,0]) cylinder(d=9, h=rft_buchse);
  color([0.1,0.1,0.1]) translate([k[0], ae_flansch_y, k[1]]) rotate([-90,0,0]) cylinder(d=rft_koerper, h=rft_tief);
  color("Orange") ae_platte();
  for (x=tasten_x) {
    color([0.1,0.1,0.1]) translate([x-6, pl_vorne-kappe_vor, tasten_z-6]) cube([12, kappe_l, 12]);
    color("Black") translate([x-7, mx_platte_y-6.6, tasten_z-7]) cube([14, 6.6+mx_platte+5, 14]);
  }
}

module pi_vorschau() {
  pz = boden_z + ph_t + pi_hoehe;
  color("Green") translate([pi_x0, pi_gpio_y, pz]) cube([85, 56, 1.6]);
  color("Silver") translate([pi_x0-2, pi_gpio_y+2, pz+1.6]) cube([21, 52, 16]);      // USB/Ethernet
  // DigiAMP+ 65 x 58 mm über dem Pi, Hohlbuchse und Klemmen an der hinteren Kante
  az = pz+1.6+amp_abst;
  color("DarkGreen") translate([pi_x0+20, pi_gpio_y, az]) cube([65, 58, 1.6]);
  color("Black") translate([pi_x0+85-17, pi_gpio_y+44, az+1.6]) cube([9, 16, 11]);     // Hohlbuchse
  for (dx=[30, 49]) color("RoyalBlue") translate([pi_x0+85-dx-13, pi_gpio_y+48, az+1.6]) cube([13, 9, 10]);
}

/* ---------- Einbau ins Gehäuse ---------- */
// Frontplatte liegt im Gehäuse bei x = 186, z = 12
module traeger_einbau(mit_bauteilen=true) {
  translate([186, 0, 12]) {
    color("LightGray") traeger_links();
    color("Gainsboro") traeger_rechts();
    color("White") lichtkasten();
    if (mit_bauteilen) bauteile_vorschau();
  }
  color("LightSteelBlue") pi_halter();
  color("LightSteelBlue") steuer_halter();
  if (mit_bauteilen) {
    pi_vorschau();
    color("SeaGreen") translate([st_x0, st_y0, boden_z+ph_t+8]) cube([st_gr[0], st_gr[1], 1.6]);
  }
}

/* ---------- Druckausrichtung ---------- */
if (teil == "alle") traeger_einbau();
if (teil == "traeger_links")  rotate([90,0,0]) translate([0,-wand_y0,0]) traeger_links();
if (teil == "traeger_rechts") rotate([90,0,0]) translate([0,-wand_y0,0]) traeger_rechts();
if (teil == "lichtkasten")    rotate([90,0,0]) translate([0,-wand_y0,0]) lichtkasten();
if (teil == "pi_halter")      translate([0,0,-boden_z]) pi_halter();
if (teil == "kupplung")       for (i=[0:2]) translate([i*15,0,0]) kupplung();
if (teil == "ae_platte")      rotate([90,0,0]) translate([0,-ae_platte_y,0]) ae_platte();
if (teil == "steuer_halter")  translate([0,0,-boden_z]) steuer_halter();
if (teil == "tastenadapter")  for (i=[0:5]) translate([i*15,0,0]) tastenadapter();
