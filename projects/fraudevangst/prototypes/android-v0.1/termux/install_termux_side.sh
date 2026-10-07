#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

mkdir -p "$HOME/.termux" "$HOME/storage/downloads/WijSAmenFraude" "$PREFIX/bin"
command -v ffmpeg >/dev/null 2>&1 || pkg install -y ffmpeg
PROP="$HOME/.termux/termux.properties"
touch "$PROP"
if grep -q '^allow-external-apps=' "$PROP"; then
  sed -i 's/^allow-external-apps=.*/allow-external-apps=true/' "$PROP"
else
  printf '\nallow-external-apps=true\n' >> "$PROP"
fi
command -v termux-reload-settings >/dev/null 2>&1 && termux-reload-settings || true

cat > "$PREFIX/bin/wijfraude-event" <<'EOS'
#!/data/data/com.termux/files/usr/bin/bash
set -u
EVENT="${1:-unknown}"
AUDIO="${2:-}"
NAME="${3:-audio.m4a}"
CASE="${4:-$(date +%Y%m%d_%H%M%S)}"
ROOT="$HOME/storage/downloads/WijSAmenFraude"
DIR="$ROOT/$CASE"
mkdir -p "$DIR"
LOG="$DIR/events.log"
printf '%s\t%s\t%s\n' "$(date -Iseconds)" "$EVENT" "$AUDIO" >> "$LOG"

shellcap() {
  local out="$1"; shift
  if command -v rish >/dev/null 2>&1; then
    rish -c "$*" > "$DIR/$out" 2>&1 || true
  elif command -v adb >/dev/null 2>&1; then
    adb shell "$@" > "$DIR/$out" 2>&1 || true
  fi
}

case "$EVENT" in
  start)
    printf '%s\n' "case=$CASE" "audio=$AUDIO" "started=$(date -Iseconds)" > "$DIR/meta.txt"
    shellcap telecom.txt dumpsys telecom
    shellcap connectivity.txt dumpsys connectivity
    shellcap telephony_registry.txt dumpsys telephony.registry
    if command -v wsb-live-status >/dev/null 2>&1; then
      wsb-live-status > "$DIR/wsb-live-status.txt" 2>&1 || true
    fi
    if command -v wsb >/dev/null 2>&1; then
      wsb --backend rish observe > "$DIR/wsb-observe.txt" 2>&1 || true
    fi
    curl -fsS --max-time 2 http://127.0.0.1:8765/v1/scene > "$DIR/bridge-scene.json" 2>/dev/null || true
    ;;
  snapshot:*)
    printf '%s\n' "$EVENT" >> "$DIR/snapshots.txt"
    ;;
  record_error:*)
    printf '%s\n' "$EVENT" >> "$DIR/errors.txt"
    ;;
  stop)
    printf '%s\n' "stopped=$(date -Iseconds)" >> "$DIR/meta.txt"
    for _ in $(seq 1 25); do
      [ -s "$AUDIO" ] && break
      sleep 0.2
    done
    if [ -s "$AUDIO" ]; then
      cp -f "$AUDIO" "$DIR/$NAME" 2>/dev/null || true
      sha256sum "$AUDIO" > "$DIR/audio.sha256" 2>/dev/null || true
      OUTBASE="$DIR/transcript"
      WAV="$DIR/audio-16k-mono.wav"
      if command -v wijtranscribe >/dev/null 2>&1; then
        (
          if command -v ffmpeg >/dev/null 2>&1; then
            if ffmpeg -hide_banner -loglevel error -y -i "$AUDIO" -ar 16000 -ac 1 -c:a pcm_s16le "$WAV" > "$DIR/ffmpeg.log" 2>&1; then
              TRANSCRIBE_INPUT="$WAV"
            else
              printf '%s\n' "ffmpeg kon de M4A niet converteren; probeer bronbestand direct" >> "$DIR/errors.txt"
              TRANSCRIBE_INPUT="$AUDIO"
            fi
          else
            printf '%s\n' "ffmpeg ontbreekt; probeer bronbestand direct" >> "$DIR/errors.txt"
            TRANSCRIBE_INPUT="$AUDIO"
          fi

          if wijtranscribe --no-timestamps "$TRANSCRIBE_INPUT" "$OUTBASE" > "$DIR/transcribe.log" 2>&1; then
            :
          else
            printf '%s\n' "wijtranscribe gaf een fout; zie transcribe.log" >> "$DIR/errors.txt"
          fi

          python "$PREFIX/share/wijfraude/analyze.py" "$OUTBASE.txt" "$DIR/analysis.json" > "$DIR/analyze.log" 2>&1 || true
        ) >/dev/null 2>&1 &
      else
        printf '%s\n' "wijtranscribe ontbreekt" >> "$DIR/errors.txt"
      fi
    else
      printf '%s\n' "Audiofile niet leesbaar via Termux: $AUDIO" >> "$DIR/errors.txt"
    fi
    ;;
esac
EOS
chmod 755 "$PREFIX/bin/wijfraude-event"

mkdir -p "$PREFIX/share/wijfraude"
cat > "$PREFIX/share/wijfraude/analyze.py" <<'EOS'
import json, re, sys
from pathlib import Path
src = Path(sys.argv[1])
out = Path(sys.argv[2])
text = src.read_text(errors="ignore").lower() if src.exists() else ""
if not text.strip():
  result = {
    "version": "0.1.3",
    "status": "transcription_missing_or_empty",
    "feature_groups_hit": None,
    "features": {},
    "assessment": "geen bruikbaar transcript; fraude-indicatoren niet beoordeeld",
    "note": "Geen inhoudelijke score maken zonder transcript. Controleer ffmpeg.log en transcribe.log."
  }
  out.write_text(json.dumps(result, ensure_ascii=False, indent=2))
  raise SystemExit(0)

patterns = {
  "authority": [r"national police", r"politie", r"police", r"government", r"overheid", r"europol", r"interpol"],
  "legal_threat": [r"arrest warrant", r"arrestatiebevel", r"warrant", r"arrest", r"legal action", r"rechtszaak"],
  "urgency": [r"immediately", r"urgent", r"right now", r"direct", r"onmiddellijk", r"vandaag"],
  "action_request": [r"press 1", r"toets 1", r"transfer", r"overmaken", r"bank account", r"bankrekening", r"install", r"download", r"gift card", r"crypto", r"bitcoin"],
  "secrecy": [r"do not tell", r"don't tell", r"confidential", r"geheim", r"vertel niemand"],
}
features = {k: [p for p in ps if re.search(p, text)] for k, ps in patterns.items()}
score = sum(bool(v) for v in features.values())
result = {
  "version": "0.1.3",
  "feature_groups_hit": score,
  "features": features,
  "assessment": "sterke fraude-indicatoren" if score >= 3 else "enkele fraude-indicatoren" if score >= 1 else "onvoldoende tekstsignalen",
  "note": "Dit is patroonherkenning, geen bewijs van identiteit of schuld. Caller-ID kan gespoofd zijn."
}
out.write_text(json.dumps(result, ensure_ascii=False, indent=2))
EOS
chmod 644 "$PREFIX/share/wijfraude/analyze.py"

printf '\n✅ Termux-kant geïnstalleerd.\n'
printf 'Commando: %s\n' "$PREFIX/bin/wijfraude-event"
printf 'Cases: %s\n' "$HOME/storage/downloads/WijSAmenFraude"
printf 'Belangrijk: Android moet de app-toestemming “Opnemen” krijgen.\n'
