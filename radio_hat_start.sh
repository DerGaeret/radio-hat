#!/bin/bash
# Startet den TAS5805M auf dem Radio HAT. Ungetestet, beim ersten Mal leise probieren.
# Einrichtung: siehe README.md (braucht i2c-tools, alsa-utils, python3)
#
# Aufruf: radio_hat_start.sh [Lautstaerke]
#   Lautstaerke: 0x30 = 0 dB, jeder Schritt mehr = 0,5 dB leiser. Standard 0x60 = -24 dB.
#   Werte unter 0x30 (lauter als 0 dB) werden auf 0x30 begrenzt, sonst uebersteuert der Verstaerker
#   und die Lautsprecher bekommen mehr als 19 W.

set -e
BUS=1
ADDR=0x2d
KARTE=plughw:CARD=sndrpihifiberry
PDN_GPIO=9
VOLUME=${1:-0x60}

# Analogverstaerkung: 0,5 dB pro Schritt, 0x00 = 29,5 V Spitze. 0x09 = -4,5 dB = 17,5 V Spitze bei
# Vollaussteuerung, das sind 19 W Sinus an 8 Ohm. Nicht verkleinern, sonst werden die 20-W-Lautsprecher ueberlastet.
AGAIN=0x09

# Schaltfrequenz und Modulation (Register 0x02): 0x00 = 768 kHz, BD-Modulation, BTL.
# Das ist zwar der Reset-Wert, wird aber ausdruecklich gesetzt: Die Spulen (10 uH) sind fuer BD bei
# 768 kHz ausgelegt, und der Abstand zum 5-V-Regler (350 kHz) ist so am groessten.
DEVICE_CTRL_1=0x00
# Regelbandbreite (Register 0x53, Bits 6-5): 0x60 = 175 kHz, die Empfehlung von TI fuer 768 kHz.
ANA_CTRL=0x60

# Hochpass gegen tiefen Bass, den die kleinen Lautsprecher nicht abstrahlen koennen (Butterworth 2. Ordnung).
HOCHPASS_HZ=50
FS=48000

if (( VOLUME < 0x30 )); then
  echo "Lautstaerke $VOLUME ist lauter als 0 dB, begrenzt auf 0x30" >&2
  VOLUME=0x30
fi

# 32-Bit-Wert im Format 5.27 als vier Bytes (hoechstwertiges zuerst)
biquad_bytes() {
  python3 - "$1" "$2" <<'PY'
import math, sys
f0, fs = float(sys.argv[1]), float(sys.argv[2])
w0 = 2 * math.pi * f0 / fs; c = math.cos(w0); alpha = math.sin(w0) / (2 * 0.7071068)
a0 = 1 + alpha
b0 = (1 + c) / 2 / a0; b1 = -(1 + c) / a0; b2 = b0
a1 = -2 * c / a0; a2 = (1 - alpha) / a0
# TAS5805M: Reihenfolge b0 b1 b2 a1 a2, a1 und a2 mit umgekehrtem Vorzeichen
out = []
for v in (b0, b1, b2, -a1, -a2):
    n = round(v * 2**27) & 0xFFFFFFFF
    out += ['0x%02x' % ((n >> s) & 0xFF) for s in (24, 16, 8, 0)]
print(' '.join(out))
PY
}

seite() {  # Buch und Seite waehlen
  i2cset -y $BUS $ADDR 0x00 0x00
  i2cset -y $BUS $ADDR 0x7f "$1"
  i2cset -y $BUS $ADDR 0x00 "$2"
}

# Verstaerker aus dem Shutdown holen
pinctrl set $PDN_GPIO op dh
sleep 0.05

# Der Verstaerker braucht laufende I2S-Takte, bevor er per I2C gestartet wird.
aplay -q -D "$KARTE" -c 2 -r $FS -f S32_LE -d 3 /dev/zero &
STILLE=$!
sleep 1

seite 0x00 0x00
i2cset -y $BUS $ADDR 0x03 0x02   # HiZ, DSP an
sleep 0.1
i2cset -y $BUS $ADDR 0x02 $DEVICE_CTRL_1
i2cset -y $BUS $ADDR 0x53 $ANA_CTRL
i2cset -y $BUS $ADDR 0x54 $AGAIN
i2cset -y $BUS $ADDR 0x4C "$VOLUME"

# Hochpass in Biquad 1 links (Buch 0xAA, Seite 0x24, ab 0x18) und rechts (Seite 0x26, ab 0x54)
BQ=$(biquad_bytes $HOCHPASS_HZ $FS)
i2cset -y $BUS $ADDR 0x5c 0x01   # Beginn eines Biquad-Satzes
seite 0xaa 0x24
i2ctransfer -y $BUS w21@$ADDR 0x18 $BQ
seite 0xaa 0x26
i2ctransfer -y $BUS w21@$ADDR 0x54 $BQ
seite 0x00 0x00
i2cset -y $BUS $ADDR 0x5c 0x00

i2cset -y $BUS $ADDR 0x03 0x03   # Play
sleep 0.1

echo "Register 0x02/0x53/0x54/0x4C (soll $DEVICE_CTRL_1/$ANA_CTRL/$AGAIN/$VOLUME):"
for r in 0x02 0x53 0x54 0x4c; do i2cget -y $BUS $ADDR $r; done
echo "Fehlerregister 0x70/0x71/0x72 (0x00 = ok):"
i2cget -y $BUS $ADDR 0x70
i2cget -y $BUS $ADDR 0x71
i2cget -y $BUS $ADDR 0x72

wait $STILLE
