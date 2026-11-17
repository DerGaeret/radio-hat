#!/bin/bash
# Erzeugt aus KiCad/RadioHAT.kicad_pcb die Bestelldateien neu und prueft die Platine.
# Aufruf im Repo-Wurzelordner: bash KiCad/werkzeuge/fertigungsdaten.sh
# Braucht KiCad 7 (kicad-cli, pcbnew-Python) und zip. Ergebnis: JLCPCB/Gerber_RadioHAT.zip (12 Dateien), JLCPCB/CPL_RadioHAT.csv
set -e
cd "$(dirname "$0")/../.."
B=KiCad/RadioHAT.kicad_pcb; T=$(mktemp -d); mkdir -p $T/g
python3 KiCad/werkzeuge/drc.py $B $T/drc refill | tail -2
kicad-cli pcb export gerbers -o $T/g/ -l F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.Paste,F.SilkS,B.SilkS,Edge.Cuts --use-drill-file-origin --no-x2 $B >/dev/null
kicad-cli pcb export drill -o $T/g/ --drill-origin plot --excellon-separate-th $B >/dev/null
rm -f $T/g/*.gbrjob JLCPCB/Gerber_RadioHAT.zip
(cd $T/g && zip -q -X "$OLDPWD/JLCPCB/Gerber_RadioHAT.zip" *)
kicad-cli pcb export pos --format csv --units mm --side front --smd-only --use-drill-file-origin -o $T/pos.csv $B >/dev/null
python3 KiCad/jlc_cpl.py $T/pos.csv JLCPCB/CPL_RadioHAT.csv
unzip -l JLCPCB/Gerber_RadioHAT.zip | tail -1
echo "Gerber in $T/g (fuer die Bilder: bash KiCad/werkzeuge/bilder.sh $T/g)"
