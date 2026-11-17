#!/usr/bin/env python3
"""Erzeugt die JLCPCB-Bestueckungsdatei (CPL) aus der KiCad-Positionsdatei.

Aufruf:
  kicad-cli pcb export pos --format csv --units mm --side front --smd-only \\
      --use-drill-file-origin -o pos.csv KiCad/RadioHAT.kicad_pcb
  python3 KiCad/jlc_cpl.py pos.csv JLCPCB/CPL_RadioHAT.csv

JLCPCB zaehlt die Drehung je Gehaeuse von einer anderen Nulllage als KiCad.
Die Korrekturen stammen aus der Tabelle von KiBot (kibot/misc.py, DEFAULT_ROTATIONS):
  SOT-23, TSOT-23: +180 Grad    HTSSOP/TSSOP, SOIC: +270 Grad    alles andere: 0 Grad
"""
import csv, re, sys

CORRECTIONS = [(r'^TSOT-23', 180), (r'^SOT-23', 180), (r'^(H?TSSOP-|TAS5805M_PWP28)', 270), (r'^SOIC-', 270)]

def correction(package):
    for pattern, angle in CORRECTIONS:
        if re.match(pattern, package):
            return angle
    return 0

def key(ref):
    return (re.sub(r'\d', '', ref), int(re.sub(r'\D', '', ref)))

rows = sorted(csv.DictReader(open(sys.argv[1])), key=lambda r: key(r['Ref']))
with open(sys.argv[2], 'w', newline='') as out:
    out.write('Designator,Mid X,Mid Y,Layer,Rotation\n')
    for r in rows:
        rot = round(float(r['Rot']) + correction(r['Package'])) % 360
        out.write(f"{r['Ref']},{float(r['PosX']):.3f}mm,{float(r['PosY']):.3f}mm,Top,{rot}\n")
print(len(rows), 'Bauteile geschrieben')
