#!/bin/bash
# Startet den TAS5805M auf dem Radio HAT. Ungetestet, beim ersten Mal leise probieren.
# Einrichtung: siehe README.md
#
# Aufruf: radio_hat_start.sh [Lautstaerke]
#   Lautstaerke: 0x30 = 0 dB, jeder Schritt mehr = 0,5 dB leiser. Standard 0x60 = -24 dB.

set -e
BUS=1
ADDR=0x2d
KARTE=plughw:CARD=sndrpihifiberry
PDN_GPIO=9
VOLUME=${1:-0x60}

# Analogverstaerkung: 0,5 dB pro Schritt. 0x09 = -4,5 dB = 17,4 V Spitze bei Vollaussteuerung,
# das sind 19 W an 8 Ohm. Nicht verkleinern, sonst werden die 20-W-Lautsprecher ueberlastet.
AGAIN=0x09

# Verstaerker aus dem Shutdown holen
pinctrl set $PDN_GPIO op dh
sleep 0.05

# Der Verstaerker braucht laufende I2S-Takte, bevor er per I2C gestartet wird.
aplay -q -D "$KARTE" -c 2 -r 48000 -f S32_LE -d 3 /dev/zero &
STILLE=$!
sleep 1

i2cset -y $BUS $ADDR 0x03 0x02   # HiZ, DSP an
sleep 0.1
i2cset -y $BUS $ADDR 0x54 $AGAIN
i2cset -y $BUS $ADDR 0x4C "$VOLUME"
i2cset -y $BUS $ADDR 0x03 0x03   # Play
sleep 0.1

echo "Fehlerregister 0x70/0x71/0x72 (0x00 = ok):"
i2cget -y $BUS $ADDR 0x70
i2cget -y $BUS $ADDR 0x71
i2cget -y $BUS $ADDR 0x72

wait $STILLE
