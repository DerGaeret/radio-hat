// Radio-Gehäuse aus 19-mm-Spanplatte – alle Maße in mm
// Achsen: x = Breite (links -> rechts), y = Tiefe (vorne 0 -> hinten), z = Höhe (unten 0 -> oben)
// Ansicht wählen: ansicht = "zusammen" | "explosion" | "ohne_deckel"
ansicht = "zusammen";

/* ---------- Eingaben ---------- */
t        = 19;     // Plattenstärke Spanplatte
// Teile aus dem Originalradio (gemessen)
platte_b = 300;  platte_h = 114;  platte_t = 3;    // Frontplatte (Skala)
abd_b    = 178;  abd_h    = 112;  abd_t    = 7;    // Lautsprecherabdeckung (2 mm Rahmen + 5 mm Riffelung)
// Lautsprecher Sharp VSP0010PBS78A (gemessen)
ls_korb  = 110;    // Korb quadratisch, gerade Seite zu gerade Seite
ls_lochabst = 84;  // Schraublöcher, Mitte zu Mitte (Quadrat)
ls_schraube = 5;   // Durchmesser der Schraublöcher im Korb
ls_ring  = 100;    // Innendurchmesser Blechring (Ende der Sicke)
ls_tiefe = 47;     // Flansch bis Magnetrückseite (aus Foto)
ls_loch  = 100;    // Ausschnitt in der Schallwand = Ring-Innendurchmesser
// Gestaltung
rueck    = 10;     // Abdeckungen und Frontplatte sitzen so weit hinter der Holzvorderkante
chrom_h  = 4;      // sichtbare Höhe der Chromleiste oben und unten (wie Original)
tiefe    = 240;    // Außentiefe inkl. Rückwand -> ca. 3,3 l netto je Lautsprecher

/* ---------- abgeleitete Maße ---------- */
innen_b  = 2*abd_b + platte_b;          // 656: Abdeckung | Frontplatte | Abdeckung, stumpf aneinander
innen_h  = platte_h + 2*chrom_h;        // 122
B = innen_b + 2*t;                      // 694
H = innen_h + 2*t;                      // 160
korpus_t = tiefe - t;                   // 221: Tiefe von Deckel, Boden, Seiten
schall_b = abd_b;                       // 178: Schallwand genau hinter der Abdeckung
kammer_b = schall_b - t;                // 159: Innenbreite Lautsprecherkammer
ls_x     = abd_b/2;                     // Lautsprecher mittig hinter der Abdeckung
y_schall = rueck + abd_t;               // 17: Vorderkante Schallwand
y_wand   = y_schall + t;                // 36: Vorderkante Zwischenwand
kammer_t = korpus_t - y_wand;           // 185

echo(str("Außenmaß B x H x T = ", B, " x ", H, " x ", tiefe));
echo(str("Kammer innen ", kammer_b, " x ", innen_h, " x ", kammer_t, " = ",
         kammer_b*innen_h*kammer_t/1e6, " l brutto"));

ex = ansicht == "explosion" ? 1 : 0;

module brett(p, s, f="BurlyWood") color(f) translate(p) cube(s);

module korpus() {
  brett([0,0,-60*ex], [B, korpus_t, t]);                          // Boden
  if (ansicht != "ohne_deckel")
    brett([0,0,H-t+60*ex], [B, korpus_t, t]);                     // Deckel
  brett([-60*ex,0,t], [t, korpus_t, innen_h], "Tan");              // Seite links
  brett([B-t+60*ex,0,t], [t, korpus_t, innen_h], "Tan");           // Seite rechts
  if (ansicht != "ohne_deckel")
    brett([0,tiefe-t+80*ex,0], [B, t, H], "Peru");                // Rückwand (aufgesetzt)
  for (x=[t+kammer_b, B-t-kammer_b-t])                            // Zwischenwände
    brett([x, y_wand+40*ex, t], [t, kammer_t, innen_h], "Wheat");
}

module schallwand(links=true) {
  x0 = links ? t : B-t-schall_b;
  lx = links ? t+ls_x : B-t-ls_x;
  color("SandyBrown") difference() {
    translate([x0, y_schall-40*ex, t]) cube([schall_b, t, innen_h]);
    translate([lx, y_schall-1-40*ex, H/2]) rotate([-90,0,0]) {
      cylinder(d=ls_loch, h=t+2, $fn=96);
      for (dx=[-1,1], dz=[-1,1]) translate([dx*ls_lochabst/2, dz*ls_lochabst/2, 0]) cylinder(d=2.5, h=t+2, $fn=16);
    }
  }
}

module lautsprecher(links=true) {
  lx = links ? t+ls_x : B-t-ls_x;
  translate([lx, y_wand+20*ex, H/2]) rotate([-90,0,0]) {
    color("Goldenrod") difference() {
      linear_extrude(1.5) intersection(){ square(ls_korb, center=true); rotate(45) square(ls_korb*1.3, center=true); }
      for (dx=[-1,1], dz=[-1,1]) translate([dx*ls_lochabst/2, dz*ls_lochabst/2, -1]) cylinder(d=ls_schraube, h=4, $fn=16);
    }
    color("DarkGoldenrod") cylinder(d1=ls_ring, d2=60, h=ls_tiefe-18, $fn=64);
    color("DimGray") translate([0,0,ls_tiefe-18]) cylinder(d=78, h=18, $fn=64);
  }
}

module front() {
  // Abdeckungen, vertikal mittig
  for (x=[t, B-t-abd_b])
    color([0.15,0.15,0.15]) translate([x, rueck-130*ex, t+(innen_h-abd_h)/2])
      difference(){ cube([abd_b, abd_t, abd_h]);
        for (z=[4:4:abd_h-4]) translate([-1,-0.01,z]) cube([abd_b+2, 1.5, 1.6]); }
  // Frontplatte, Vorderseite bündig mit den Abdeckungen
  translate([t+abd_b, rueck-80*ex, t+chrom_h]) {
    color("Silver") cube([platte_b, platte_t, platte_h]);
    color([0.1,0.1,0.1]) translate([12,-0.1,8]) cube([platte_b-24, 0.2, platte_h-16]);
  }
  // Chromleisten: Trägerleiste 4 x 7 mm, vorne mit 4-mm-Chromzierleiste beklebt
  for (z=[t, H-t-chrom_h])
    color("WhiteSmoke") translate([t, rueck-200*ex, z]) cube([innen_b, abd_t, chrom_h]);
}

module technik_platzhalter() {   // nur zur Orientierung, wird im nächsten Schritt 3D-gedruckt
  %translate([t+abd_b+10, rueck+platte_t+30, t+5]) cube([platte_b-20, 95, 30]);
}

korpus();
schallwand(true); schallwand(false);
lautsprecher(true); lautsprecher(false);
front();
technik_platzhalter();
