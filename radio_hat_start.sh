#!/bin/bash
# Radio HAT: Verstaerker TAS5805M starten, stoppen und pruefen. Ungetestet, beim ersten Mal leise probieren.
# Einrichtung: siehe README.md (braucht i2c-tools, alsa-utils, python3, pinctrl)
# Registerwerte und Ablauf nach Datenblatt TAS5805M (SLASEH5D), Zusammenfassung in Datenblaetter/TAS5805M.md
#
# Aufruf: radio_hat_start.sh [start [Lautstaerke] | stop | status | clear]
#   start   einschalten nach Kap. 7.5.3.1 (Standard, wenn nichts angegeben ist)
#   stop    abschalten nach Kap. 7.5.3.2: leise rampen, Ausgaenge hochohmig, PDN low. Vor dem Herunterfahren aufrufen.
#   status  Zustand, Takt und Fehlerregister lesbar ausgeben
#   clear   gespeicherte Fehler loeschen (Register 0x78)
#   Lautstaerke: 0x30 = 0 dB, jeder Schritt mehr = 0,5 dB leiser. Standard 0x60 = -24 dB.
#   Werte unter 0x30 (lauter als 0 dB) werden auf 0x30 begrenzt, sonst uebersteuert der Verstaerker
#   und die Lautsprecher bekommen mehr als 19 W.

set -e
BUS=1
ADDR=0x2d                       # 15 kOhm von ADR nach DVDD (Tabelle 7-5)
KARTE=plughw:CARD=sndrpihifiberry
PDN_GPIO=9
FS=48000

# Analogverstaerkung (0x54): 0,5 dB pro Schritt, 0x00 = 29,5 V Spitze. 0x09 = -4,5 dB = 17,5 V Spitze bei
# Vollaussteuerung, das sind 19 W Sinus an 8 Ohm. Nicht verkleinern, sonst werden die 20-W-Lautsprecher ueberlastet.
AGAIN=0x09
# Schaltfrequenz und Modulation (0x02): 0x00 = 768 kHz, BD-Modulation, BTL (Tabelle 7-9).
DEVICE_CTRL_1=0x00
# Regelbandbreite (0x53, Bits 6-5): 0x60 = 175 kHz, laut Tabelle 7-27 die Wahl fuer 768 kHz.
ANA_CTRL=0x60
# Uebertemperatur-Abschaltung (160 Grad) automatisch zuruecknehmen, sobald der Chip abgekuehlt ist (0x76 Bit 4).
MISC_CONTROL=0x10
# Hochpass gegen tiefen Bass, den die kleinen Lautsprecher nicht abstrahlen koennen (Butterworth 2. Ordnung).
HOCHPASS_HZ=50

w() { i2cset -y $BUS $ADDR "$1" "$2"; }
r() { i2cget -y $BUS $ADDR "$1"; }
buch_seite() {  # Buch und Seite waehlen (Kap. 7.5.2.5): erst Seite 0, dann Buch in 0x7F, dann Seite
  w 0x00 0x00; w 0x7f "$1"; w 0x00 "$2"
}
takt_da() {     # 0x39 Bit 2 = Bittakt fehlt, Bit 1 = Bittakt ungueltig
  local s; s=$(r 0x39) || return 1
  (( (s & 0x06) == 0 ))
}

# Hochpass-Koeffizienten im Format 5.27 als 20 Bytes: b0 b1 b2 a1 a2, a1 und a2 mit umgekehrtem Vorzeichen
biquad_bytes() {
  python3 - "$1" "$2" <<'PY'
import math, sys
f0, fs = float(sys.argv[1]), float(sys.argv[2])
w0 = 2 * math.pi * f0 / fs; c = math.cos(w0); alpha = math.sin(w0) / (2 * 0.7071068)
a0 = 1 + alpha
b0 = (1 + c) / 2 / a0; b1 = -(1 + c) / a0; b2 = b0
a1 = -2 * c / a0; a2 = (1 - alpha) / a0
out = []
for v in (b0, b1, b2, -a1, -a2):
    n = round(v * 2**27) & 0xFFFFFFFF
    out += ['0x%02x' % ((n >> s) & 0xFF) for s in (24, 16, 8, 0)]
print(' '.join(out))
PY
}

fehler_text() {  # Fehlerregister lesbar machen (Tabellen 7-43 bis 7-46)
  local c g1 g2 ot
  c=$(r 0x70); g1=$(r 0x71); g2=$(r 0x72); ot=$(r 0x73)
  echo "Fehlerregister 0x70/0x71/0x72/0x73: $c $g1 $g2 $ot"
  (( c & 0x08 )) && echo "  Links: Gleichspannung am Lautsprecher (Ausgang abgeschaltet, erst Ursache suchen, dann 'clear')"
  (( c & 0x04 )) && echo "  Rechts: Gleichspannung am Lautsprecher (Ausgang abgeschaltet, erst Ursache suchen, dann 'clear')"
  (( c & 0x02 )) && echo "  Links: Ueberstrom (Kurzschluss am Lautsprecherkabel?)"
  (( c & 0x01 )) && echo "  Rechts: Ueberstrom (Kurzschluss am Lautsprecherkabel?)"
  (( g1 & 0x80 )) && echo "  OTP-Pruefsummenfehler im Verstaerker"
  (( g1 & 0x40 )) && echo "  Biquad-Koeffizienten nicht uebernommen"
  (( g1 & 0x04 )) && echo "  Takt war unterbrochen (normal, wenn eine Wiedergabe pausiert hat)"
  (( g1 & 0x02 )) && echo "  PVDD zu hoch (ueber 28 V)"
  (( g1 & 0x01 )) && echo "  PVDD zu niedrig (unter 4,2 V)"
  (( g2 & 0x01 )) && echo "  Uebertemperatur-Abschaltung (160 Grad)"
  (( ot & 0x04 )) && echo "  Temperaturwarnung (135 Grad), der Verstaerker regelt leiser"
  (( (c & 0x0f) || (g1 & 0xc3) || (g2 & 0x01) )) && return 1
  return 0
}

start() {
  local VOLUME=${1:-0x60}
  if (( VOLUME < 0x30 )); then
    echo "Lautstaerke $VOLUME ist lauter als 0 dB, begrenzt auf 0x30" >&2
    VOLUME=0x30
  fi
  # 1. PDN high, mindestens 5 ms warten, dann I2S-Takte starten
  pinctrl set $PDN_GPIO op dh
  sleep 0.05
  # 2. Stille abspielen, damit Bit- und Worttakt laufen. Ist die Karte belegt, spielt schon ein Programm.
  aplay -q -D "$KARTE" -c 2 -r $FS -f S32_LE -d 3 /dev/zero 2>/dev/null &
  local STILLE=$!
  sleep 0.5
  # 3. Hi-Z und DSP an, mindestens 5 ms warten
  buch_seite 0x00 0x00
  w 0x03 0x02
  sleep 0.05
  # 4. Einstellungen und DSP-Koeffizienten
  w 0x02 $DEVICE_CTRL_1
  w 0x53 $ANA_CTRL
  w 0x54 $AGAIN
  w 0x76 $MISC_CONTROL
  w 0x4c "$VOLUME"
  # Hochpass in Biquad 1 links (Buch 0xAA, Seite 0x24, ab 0x18). Der rechte Kanal nutzt dieselben
  # Koeffizienten, solange 0x66 Bit 3 = 0 ist (Reset-Wert).
  local BQ; BQ=$(biquad_bytes $HOCHPASS_HZ $FS)
  w 0x5c 0x01
  buch_seite 0xaa 0x24
  i2ctransfer -y $BUS w21@$ADDR 0x18 $BQ
  buch_seite 0x00 0x00
  w 0x5c 0x00
  # Fehler aus der Einschaltphase (z. B. Takt noch nicht da) loeschen, dann spielen
  w 0x78 0x80
  w 0x03 0x03
  sleep 0.2
  echo "Register 0x02/0x53/0x54/0x76/0x4C (soll $DEVICE_CTRL_1/$ANA_CTRL/$AGAIN/$MISC_CONTROL/$VOLUME):" \
       "$(r 0x02)/$(r 0x53)/$(r 0x54)/$(r 0x76)/$(r 0x4c)"
  local ok=0
  fehler_text || ok=1
  wait $STILLE 2>/dev/null || true
  return $ok
}

stop() {
  # Kap. 7.5.3.2: Ausgaenge abschalten, mindestens 6 ms warten, erst dann die Versorgung abschalten.
  if r 0x68 >/dev/null 2>&1; then
    buch_seite 0x00 0x00
    if takt_da; then
      w 0x03 0x0b          # leise rampen (Mute), Lautstaerke sinkt in 0,5-dB-Schritten
      sleep 0.05
    fi
    w 0x03 0x0a            # Ausgaenge hochohmig
    sleep 0.02
  fi
  pinctrl set $PDN_GPIO op dl   # Shutdown: alle internen Regler aus, Register zurueckgesetzt
}

status() {
  if ! r 0x68 >/dev/null 2>&1; then
    echo "Verstaerker antwortet nicht auf I2C (PDN low oder keine Versorgung?)"; return 1
  fi
  buch_seite 0x00 0x00
  local zust fs bck
  zust=$(r 0x68); fs=$(r 0x37); bck=$(r 0x38)
  case $(( zust & 0xff )) in 0) z="Deep Sleep";; 1) z="Sleep";; 2) z="Hi-Z (Ausgaenge aus)";; 3) z="Play";; *) z="?";; esac
  case $(( fs & 0x0f )) in 9) f="48 kHz";; 11) f="96 kHz";; 6) f="32 kHz";; 0) f="kein gueltiger Takt";; *) f="Code $(( fs & 0x0f ))";; esac
  echo "Zustand: $z, Abtastrate: $f, Bittakte je Abtastung: $(( ((fs & 0x30) << 4) | bck ))"
  echo "Einstellungen 0x02/0x53/0x54/0x76/0x4C: $(r 0x02)/$(r 0x53)/$(r 0x54)/$(r 0x76)/$(r 0x4c)"
  fehler_text
}

clear_faults() {
  buch_seite 0x00 0x00
  w 0x78 0x80
  fehler_text
}

case "${1:-start}" in
  start)  shift || true; start "$@" ;;
  stop)   stop ;;
  status) status ;;
  clear)  clear_faults ;;
  0x*|[0-9]*) start "$1" ;;      # alter Aufruf: radio_hat_start.sh 0x50
  *) echo "Aufruf: $0 [start [Lautstaerke] | stop | status | clear]" >&2; exit 2 ;;
esac
