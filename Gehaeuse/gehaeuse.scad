// Radio-Gehäuse aus 19-mm-Spanplatte – alle Maße in mm
// Achsen: x = Breite (links -> rechts), y = Tiefe (vorne 0 -> hinten), z = Höhe (unten 0 -> oben)
// Ansicht wählen: ansicht = "zusammen" | "explosion" | "ohne_deckel"
ansicht = "zusammen";

/* ---------- Eingaben ---------- */
t        = 19;     // Plattenstärke Spanplatte
// Teile aus dem Originalradio
platte_b = 300;  platte_h = 114;  platte_t = 3;    // Frontplatte (Skala)
abd_b    = 178;  abd_h    = 112;  abd_t    = 8;    // Lautsprecherabdeckung (Stärke geschätzt!)
ueberl   = 19;     // so weit verdecken die Abdeckungen die Frontplattenkante (aus dem Foto)
// Lautsprecher Sharp VSP0010PBS78A (aus Fotos geschätzt)
ls_korb  = 112;    // Korb außen (quadratisch mit Fasen)
ls_tiefe = 47;     // Flansch bis Magnetrückseite
ls_loch  = 95;     // Ausschnitt in der Schallwand (Montage von hinten)
// Gestaltung
rueck    = 10;     // Abdeckungen sitzen so weit hinter der Holzvorderkante
spalt    = 6;      // Luft oben/unten zwischen Holz und Frontplatte (Chromleiste deckt ab)
tiefe    = 180;    // Außentiefe inkl. Rückwand
ls_x     = 70;     // Lautsprechermitte ab Innenseite Seitenwand
alu      = 10;     // Alu-Winkel 10 x 10 x 1
alu_s    = 1;

/* ---------- abgeleitete Maße ---------- */
kammer_b = abd_b - ueberl - t;          // 140: Innenbreite einer Lautsprecherkammer
schall_b = abd_b - ueberl;              // 159: Breite Schallwand
innen_b  = 2*schall_b + platte_b;       // 618
innen_h  = platte_h + 2*spalt;          // 126
B = innen_b + 2*t;                      // 656
H = innen_h + 2*t;                      // 164
korpus_t = tiefe - t;                   // 161: Tiefe von Deckel, Boden, Seiten
y_schall = rueck + abd_t;               // 18: Vorderkante Schallwand
y_wand   = y_schall + t;                // 37: Vorderkante Zwischenwand

echo(str("Außenmaß B x H x T = ", B, " x ", H, " x ", tiefe));

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
    brett([x, y_wand+40*ex, t], [t, korpus_t-y_wand, innen_h], "Wheat");
}

module schallwand(links=true) {
  x0 = links ? t : B-t-schall_b;
  lx = links ? t+ls_x : B-t-ls_x;
  color("SandyBrown") difference() {
    translate([x0, y_schall-40*ex, t]) cube([schall_b, t, innen_h]);
    translate([lx, y_schall-1-40*ex, H/2]) rotate([-90,0,0]) cylinder(d=ls_loch, h=t+2, $fn=96);
  }
}

module lautsprecher(links=true) {
  lx = links ? t+ls_x : B-t-ls_x;
  translate([lx, y_wand+20*ex, H/2]) rotate([-90,0,0]) {
    color("Goldenrod") linear_extrude(1.5) offset(delta=0) 
      intersection(){ square(ls_korb, center=true); rotate(45) square(ls_korb*1.25, center=true); }
    color("DarkGoldenrod") cylinder(d1=100, d2=60, h=ls_tiefe-18, $fn=64);
    color("DimGray") translate([0,0,ls_tiefe-18]) cylinder(d=78, h=18, $fn=64);
  }
}

module front() {
  // Abdeckungen
  for (x=[t, B-t-abd_b])
    color([0.15,0.15,0.15]) translate([x, rueck-130*ex, t+(innen_h-abd_h)/2])
      difference(){ cube([abd_b, abd_t, abd_h]);
        for (z=[4:4:abd_h-4]) translate([-1,-0.01,z]) cube([abd_b+2, 1.5, 1.6]); }
  // Frontplatte
  translate([t+schall_b, y_schall-80*ex, t+spalt]) {
    color("Silver") cube([platte_b, platte_t, platte_h]);
    color([0.1,0.1,0.1]) translate([12,-0.1,8]) cube([platte_b-24, 0.2, platte_h-16]);
  }
  // Chromleisten: Alu-Winkel 10x10x1, waagerechter Schenkel am Holz, senkrechter zeigt nach vorn
  for (oben=[true,false]) {
    z0 = oben ? H-t-alu_s : t;
    zv = oben ? H-t-alu : t;
    color("WhiteSmoke") translate([t, -200*ex, 0]) {
      translate([0,0,z0]) cube([innen_b, alu, alu_s]);
      translate([0,alu-alu_s,zv]) cube([innen_b, alu_s, alu]);
    }
  }
}

module technik_platzhalter() {   // nur zur Orientierung, wird im nächsten Schritt 3D-gedruckt
  %translate([t+schall_b+10, y_schall+platte_t+30, t+5]) cube([platte_b-20, 95, 30]);
}

korpus();
schallwand(true); schallwand(false);
lautsprecher(true); lautsprecher(false);
front();
technik_platzhalter();
