#!/bin/bash
# Rendert Bilder/render_top.png und render_bottom.png aus einem Gerber-Ordner (ohne Innenlagen).
# Aufruf im Repo-Wurzelordner: bash KiCad/werkzeuge/bilder.sh GERBER-ORDNER
# Braucht Node.js, npm-Paket pcb-stackup@4.2.8 und Playwright mit Chromium.
set -e
[ -d "$1" ] || { echo "Gerber-Ordner fehlt"; exit 1; }
G=$(cd "$1" && pwd); R=$(pwd); T=$(mktemp -d); cp KiCad/werkzeuge/render_*.js $T/; cd $T
npm init -y >/dev/null; npm install pcb-stackup@4.2.8 >/dev/null 2>&1
node render_gerber.js "$G" $T/stk && node render_png.js $T/stk "$R/Bilder"
ls -la "$R/Bilder"
