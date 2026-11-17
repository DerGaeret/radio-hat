// Radio-Gehäuse aus 8-mm-Spanplatte Dekor Nussbaum – alle Maße in mm
// Achsen: x = Breite (links -> rechts), y = Tiefe (vorne 0 -> hinten), z = Höhe (Unterkante Boden = 0)
// Ansicht: "zusammen" | "explosion" | "ohne_deckel"
ansicht = "zusammen";

/* ---------- Eingaben ---------- */
t        = 8;      // Plattenstärke (alle Bretter)
leiste   = 15;     // Kiefer-Vierkantleisten 15 x 15 innen in den Ecken
// Teile aus dem Originalradio (gemessen)
platte_b = 300;  platte_h = 114;  platte_t = 3;    // Frontplatte (Skala)
abd_b    = 178;  abd_h    = 112;  abd_t    = 7;    // Lautsprecherabdeckung (2 mm Rahmen + 5 mm Riffelung)
// Lautsprecher Sharp VSP0010PBS78A (gemessen)
ls_korb  = 110;  ls_lochabst = 84;  ls_ring = 100;  ls_tiefe = 47;
ls_loch  = 100;    // Ausschnitt im Frontbrett
// Gestaltung
rueck    = 3;      // Abdeckungen sitzen so weit hinter der Holzvorderkante
chrom_h  = 4;      // sichtbare Höhe der Chromleiste oben und unten
tiefe    = 210;    // Außentiefe inkl. Rückwand -> ca. 3,3 l netto je Lautsprecher
fuss_d   = 25;  fuss_h = 20;   // Chromfüße
// Magnete für abnehmbare Abdeckungen: je 4 pro Abdeckung, im Frontbrett eingelassen
mag_d    = 10;  mag_h = 3;     // Neodym-Scheibenmagnet 10 x 3
mag_tasche = 12;  mag_tiefe = 4;   // Bohrung im Frontbrett (Forstner 12 mm, 4 tief)
mag_rand = 15;                 // Magnetmitte ab Außenkante der Abdeckung bzw. Frontbrett-Kante oben/unten
fuss_x   = 60;  fuss_y = 55;   // Abstand Fußmitte von Seite bzw. Vorder-/Hinterkante

/* ---------- abgeleitete Maße ---------- */
innen_b  = 2*abd_b + platte_b;          // 656
innen_h  = platte_h + 2*chrom_h;        // 122
B = innen_b + 2*t;                      // 672
H = innen_h + 2*t;                      // 138
korpus_t = tiefe - t;                   // 202: Tiefe von Deckel, Boden, Seiten
y_front  = rueck + abd_t;               // 17: Vorderseite Frontbrett = Rückseite Abdeckungen und Frontplatte
y_wand   = y_front + t;                 // 25: Rückseite Frontbrett
kammer_b = abd_b - t;                   // 170: Zwischenwand steht hinter der Fuge Abdeckung/Frontplatte
kammer_t = korpus_t - y_wand;           // 177
ls_x     = abd_b/2;                     // Lautsprecher mittig hinter der Abdeckung
xw       = [t+kammer_b, B-t-abd_b];     // linke Kante der Zwischenwände

echo(str("Außenmaß B x H x T = ", B, " x ", H, " x ", tiefe, "  (+ ", fuss_h, " Füße)"));
echo(str("Kammer innen ", kammer_b, " x ", innen_h, " x ", kammer_t, " = ",
         kammer_b*innen_h*kammer_t/1e6, " l brutto"));

ex = ansicht == "explosion" ? 1 : 0;
NUSS = [0.42,0.27,0.16]; NUSS2 = [0.50,0.33,0.20]; KIEFER = [0.93,0.82,0.6];

module brett(p, s, f=NUSS) color(f) translate(p) cube(s);

module korpus() {
  brett([0,0,-60*ex], [B, korpus_t, t]);                                  // Boden
  if (ansicht != "ohne_deckel") brett([0,0,H-t+60*ex], [B, korpus_t, t]); // Deckel
  brett([-60*ex,0,t], [t, korpus_t, innen_h], NUSS2);                      // Seiten
  brett([B-t+60*ex,0,t], [t, korpus_t, innen_h], NUSS2);
  if (ansicht != "ohne_deckel") brett([0,tiefe-t+80*ex,0], [B, t, H]);    // Rückwand
  for (x=xw) brett([x, y_wand+40*ex, t], [t, kammer_t, innen_h], NUSS2);  // Zwischenwände
}

module frontbrett() {
  color(NUSS2) difference() {
    translate([t, y_front-40*ex, t]) cube([innen_b, t, innen_h]);
    for (lx=[t+ls_x, B-t-ls_x]) translate([lx, y_front-1-40*ex, H/2]) rotate([-90,0,0]) {
      cylinder(d=ls_loch, h=t+2, $fn=96);
      for (dx=[-1,1], dz=[-1,1]) translate([dx*ls_lochabst/2, dz*ls_lochabst/2, 0]) cylinder(d=4.5, h=t+2, $fn=16);
    }
    for (p=mag_pos()) translate([p[0], y_front-1-40*ex, p[1]]) rotate([-90,0,0]) cylinder(d=mag_tasche, h=mag_tiefe+1, $fn=32);
  }
  for (p=mag_pos()) color("SlateGray") translate([p[0], y_front+mag_tiefe-mag_h-40*ex, p[1]]) rotate([-90,0,0]) cylinder(d=mag_d, h=mag_h, $fn=32);
}

function mag_pos() = [ for (x0=[t, B-t-abd_b], dx=[mag_rand, abd_b-mag_rand], z=[t+mag_rand, H-t-mag_rand]) [x0+dx, z] ];

module leisten() {   // Kiefer 15x15, innen verleimt
  L = leiste;
  color(KIEFER) translate([0, 20*ex, 0]) {
    // längs in die Ecken Seite/Deckel und Seite/Boden
    for (x=[t, B-t-L], z=[t, H-t-L]) translate([x, y_wand, z]) cube([L, kammer_t, L]);
    // längs an den Zwischenwänden (Kammerseite), oben und unten
    for (x=[xw[0]-L, xw[1]+t], z=[t, H-t-L]) translate([x, y_wand, z]) cube([L, kammer_t-L, L]);
    // hinten senkrecht an Seiten und Zwischenwänden (Rückwand wird hier verschraubt)
    for (x=[t, B-t-L, xw[0]-L, xw[1]+t]) translate([x, korpus_t-L, t+L]) cube([L, L, innen_h-2*L]);
    // hinten waagerecht, oben und unten (Kammern und Technikfach)
    for (z=[t, H-t-L]) {
      translate([xw[0]+t, korpus_t-L, z]) cube([xw[1]-xw[0]-t, L, L]);
      for (x=[t+L, xw[1]+t+L]) translate([x, korpus_t-L, z]) cube([kammer_b-2*L, L, L]);
    }
    // Klötze für die Fußschrauben
    for (x=[fuss_x, B-fuss_x], y=[fuss_y, tiefe-fuss_y]) translate([x-15, y-15, t]) cube([30, 30, 10]);
  }
}

module lautsprecher(links=true) {
  lx = links ? t+ls_x : B-t-ls_x;
  translate([lx, y_wand+20*ex, H/2]) rotate([-90,0,0]) {
    color("Goldenrod") linear_extrude(1.5)
      intersection(){ square(ls_korb, center=true); rotate(45) square(ls_korb*1.3, center=true); }
    color("DarkGoldenrod") cylinder(d1=ls_ring, d2=60, h=ls_tiefe-18, $fn=64);
    color("DimGray") translate([0,0,ls_tiefe-18]) cylinder(d=78, h=18, $fn=64);
  }
}

module front() {
  for (x=[t, B-t-abd_b])   // Abdeckungen, liegen auf dem Frontbrett
    color([0.13,0.13,0.13]) translate([x, rueck-130*ex, t+(innen_h-abd_h)/2])
      difference(){ cube([abd_b, abd_t, abd_h]);
        for (z=[4:4:abd_h-4]) translate([-1,-0.01,z]) cube([abd_b+2, 1.5, 1.6]); }
  // Frontplatte: Rückseite bündig mit Rückseite der Abdeckungen
  translate([t+abd_b, y_front-platte_t-80*ex, t+chrom_h]) {
    color("Silver") cube([platte_b, platte_t, platte_h]);
    color([0.1,0.1,0.1]) translate([12,-0.1,8]) cube([platte_b-24, 0.2, platte_h-16]);
  }
  // Chromleisten 4 x 7, Vorderseite bündig mit den Abdeckungen
  for (z=[t, H-t-chrom_h])
    color("WhiteSmoke") translate([t, rueck-200*ex, z]) cube([innen_b, abd_t, chrom_h]);
}

module fuesse() {
  for (x=[fuss_x, B-fuss_x], y=[fuss_y, tiefe-fuss_y])
    color("Gainsboro") translate([x, y, -100*ex]) mirror([0,0,1])
      cylinder(d1=fuss_d, d2=fuss_d*0.7, h=fuss_h, $fn=48);
}

module technik_platzhalter() {
  %translate([t+abd_b+10, y_wand+5, t+5]) cube([platte_b-20, 120, 30]);
}

korpus(); frontbrett(); leisten();
lautsprecher(true); lautsprecher(false);
front(); fuesse(); technik_platzhalter();
