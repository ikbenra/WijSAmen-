#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "=== WijSAmen FraudeVangst Termux setup v0.1.2 ==="

mkdir -p "$HOME/.termux" "$HOME/storage/downloads/WijSAmenFraude" "$PREFIX/bin" "$PREFIX/share/wijfraude"
PROP="$HOME/.termux/termux.properties"
touch "$PROP"

if grep -qE '^[[:space:]]*allow-external-apps=' "$PROP"; then
  sed -i -E 's/^[[:space:]]*allow-external-apps=.*/allow-external-apps=true/' "$PROP"
else
  printf '\nallow-external-apps=true\n' >> "$PROP"
fi

if command -v termux-reload-settings >/dev/null 2>&1; then
  termux-reload-settings || true
fi

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

    curl -fsS --max-time 2 http://127.0.0.1:8765/v1/scene \
      > "$DIR/bridge-scene.json" 2>/dev/null || true
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
      if command -v wijtranscribe >/dev/null 2>&1; then
        (
          INPUT_AUDIO="$AUDIO"
          WAV="$DIR/audio_for_whisper.wav"

          # whisper.cpp/miniaudio could not decode the A52s recorder's M4A.
          # Convert deterministically to mono 16 kHz PCM WAV when ffmpeg exists.
          case "${AUDIO##*.}" in
            m4a|M4A|aac|AAC|mp4|MP4)
              if command -v ffmpeg >/dev/null 2>&1; then
                if ffmpeg -nostdin -hide_banner -loglevel error -y \
                  -i "$AUDIO" -vn -ac 1 -ar 16000 -c:a pcm_s16le "$WAV" \
                  > "$DIR/ffmpeg.log" 2>&1; then
                  INPUT_AUDIO="$WAV"
                  sha256sum "$WAV" > "$DIR/audio_for_whisper.sha256" 2>/dev/null || true
                else
                  printf '%s\n' "ffmpeg conversie van M4A naar WAV mislukt" >> "$DIR/errors.txt"
                  INPUT_AUDIO=""
                fi
              else
                printf '%s\n' "ffmpeg ontbreekt; voer zichtbaar uit: pkg install ffmpeg" >> "$DIR/errors.txt"
                INPUT_AUDIO=""
              fi
              ;;
          esac

          if [ -n "$INPUT_AUDIO" ]; then
            wijtranscribe --no-timestamps "$INPUT_AUDIO" "$OUTBASE" \
              > "$DIR/transcribe.log" 2>&1 || true
          fi

          python "$PREFIX/share/wijfraude/analyze.py" \
            "$OUTBASE.txt" "$DIR/analysis.json" \
            > "$DIR/analyze.log" 2>&1 || true
        ) >/dev/null 2>&1 &
      else
        printf '%s\n' "wijtranscribe niet gevonden" >> "$DIR/errors.txt"
      fi
    else
      printf '%s\n' "Audiofile niet leesbaar via Termux: $AUDIO" >> "$DIR/errors.txt"
    fi
    ;;
esac
EOS
chmod 755 "$PREFIX/bin/wijfraude-event"

cat > "$PREFIX/share/wijfraude/analyze.py" <<'EOS'
import json, re, sys
from pathlib import Path

src = Path(sys.argv[1])
out = Path(sys.argv[2])
text = src.read_text(errors="ignore").strip() if src.exists() else ""
lower = text.lower()

patterns = {
    "authority": [
        r"national police", r"politie", r"police", r"government",
        r"overheid", r"europol", r"interpol"
    ],
    "legal_threat": [
        r"arrest warrant", r"arrestatiebevel", r"warrant",
        r"arrest", r"legal action", r"rechtszaak"
    ],
    "urgency": [
        r"immediately", r"urgent", r"right now", r"direct",
        r"onmiddellijk", r"vandaag"
    ],
    "action_request": [
        r"press 1", r"toets 1", r"transfer", r"overmaken",
        r"bank account", r"bankrekening", r"install", r"download",
        r"gift card", r"crypto", r"bitcoin"
    ],
    "secrecy": [
        r"do not tell", r"don't tell", r"confidential",
        r"geheim", r"vertel niemand"
    ],
}

features = {k: [p for p in ps if re.search(p, lower)] for k, ps in patterns.items()}
score = sum(bool(v) for v in features.values())
transcript_ok = bool(text)

result = {
    "version": "0.1.2",
    "transcript_present": transcript_ok,
    "transcript_chars": len(text),
    "feature_groups_hit": score,
    "features": features,
    "assessment": (
        "transcriptie ontbreekt of is leeg" if not transcript_ok
        else "sterke fraude-indicatoren" if score >= 3
        else "enkele fraude-indicatoren" if score >= 1
        else "onvoldoende tekstsignalen"
    ),
    "note": (
        "Dit is patroonherkenning, geen bewijs van identiteit of schuld. "
        "Caller-ID kan gespoofd zijn."
    )
}

out.write_text(json.dumps(result, ensure_ascii=False, indent=2))
EOS
chmod 644 "$PREFIX/share/wijfraude/analyze.py"

echo
echo "=== CONTROLE ==="
grep -E '^allow-external-apps=' "$PROP" || true
printf 'wijfraude-event: '
command -v wijfraude-event || true
printf 'ffmpeg: '
command -v ffmpeg || echo "niet gevonden; installeer zichtbaar met: pkg install ffmpeg"
printf 'rish: '
command -v rish || echo "niet gevonden (ADB fallback kan nog beschikbaar zijn)"
printf 'wijtranscribe: '
command -v wijtranscribe || echo "niet gevonden"
echo
echo "✅ Setup v0.1.2 klaar."
echo "Cases komen in: $HOME/storage/downloads/WijSAmenFraude"
echo "Open FraudeVangst opnieuw en tik START VANGST."
