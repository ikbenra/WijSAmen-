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
            ffmpeg -hide_banner -i "$AUDIO" -af volumedetect -f null - > "$DIR/audio-evidence.txt" 2>&1 || true
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

          python "$PREFIX/share/wijfraude/analyze.py" "$OUTBASE.txt" "$DIR/analysis.json" "$DIR/audio-evidence.txt" "$DIR/transcript-channels.json" > "$DIR/analyze.log" 2>&1 || true
          python "$PREFIX/share/wijfraude/opaalview.py" "$DIR/transcript-channels.json" "$DIR/transcript-opaal.html" > "$DIR/opaalview.log" 2>&1 || true
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
import json, re, sys, math
from pathlib import Path

src = Path(sys.argv[1])
out = Path(sys.argv[2])
audio_evidence = Path(sys.argv[3]) if len(sys.argv) > 3 else None
channels_out = Path(sys.argv[4]) if len(sys.argv) > 4 else out.with_name("transcript-channels.json")

raw = src.read_text(errors="ignore") if src.exists() else ""
text = raw.lower()

def parse_db(label, default=-120.0):
    if not audio_evidence or not audio_evidence.exists():
        return default
    s = audio_evidence.read_text(errors="ignore")
    m = re.search(rf"{re.escape(label)}:\s*(-?inf|-?\d+(?:\.\d+)?)\s*dB", s, re.I)
    if not m: return default
    if m.group(1).lower() in ("-inf","inf"): return -120.0
    try: return float(m.group(1))
    except: return default

mean_db = parse_db("mean_volume")
max_db = parse_db("max_volume")

lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
norms = [re.sub(r"\W+"," ",ln.lower()).strip() for ln in lines]
counts = {n:norms.count(n) for n in set(norms) if n}

# Acoustic support is deliberately conservative around near-silence.
# 1.0 means strong acoustic support; 0.0 means effectively none.
if max_db <= -80:
    acoustic = 0.0
elif max_db <= -60:
    acoustic = (max_db + 80.0) / 20.0 * 0.35
elif max_db <= -35:
    acoustic = 0.35 + (max_db + 60.0) / 25.0 * 0.45
else:
    acoustic = min(1.0, 0.80 + (max_db + 35.0) / 35.0 * 0.20)

segments=[]
for i, line in enumerate(lines):
    n = norms[i]
    repetition = max(0, counts.get(n,1)-1)
    repetition_penalty = min(0.35, repetition * 0.12)
    short_penalty = 0.12 if len(n.split()) <= 1 else 0.0
    support = max(0.0, acoustic - repetition_penalty - short_penalty)

    # UI has intentionally only two visible channels.
    # Lower half of the uncertain region belongs to hallucination channel.
    channel = "white" if support >= 0.50 else "purple"
    reason=[]
    if acoustic == 0.0: reason.append("near_digital_silence")
    elif acoustic < 0.50: reason.append("weak_acoustic_support")
    if repetition: reason.append("repetition")
    if short_penalty: reason.append("very_short_model_output")
    if channel == "purple" and not reason: reason.append("insufficient_combined_support")

    segments.append({
      "index": i,
      "text": line,
      "channel": channel,
      "support": round(support,3),
      "internal": {
        "acoustic_support": round(acoustic,3),
        "mean_db": mean_db,
        "max_db": max_db,
        "repetition_count": repetition + 1,
        "reason": reason
      }
    })

white_text = "\n".join(s["text"] for s in segments if s["channel"]=="white").lower()

patterns = {
  "authority": [r"national police", r"politie", r"police", r"government", r"overheid", r"europol", r"interpol"],
  "legal_threat": [r"arrest warrant", r"arrestatiebevel", r"warrant", r"arrest", r"legal action", r"rechtszaak"],
  "urgency": [r"immediately", r"urgent", r"right now", r"direct", r"onmiddellijk", r"vandaag"],
  "action_request": [r"press 1", r"toets 1", r"transfer", r"overmaken", r"bank account", r"bankrekening", r"install", r"download", r"gift card", r"crypto", r"bitcoin"],
  "secrecy": [r"do not tell", r"don't tell", r"confidential", r"geheim", r"vertel niemand"],
}
features = {k:[p for p in ps if re.search(p, white_text)] for k,ps in patterns.items()}
score = sum(bool(v) for v in features.values())

if not lines:
    status="transcription_missing_or_empty"
    assessment="geen bruikbaar transcript; fraude-indicatoren niet beoordeeld"
elif not white_text.strip():
    status="hallucination_channel_only"
    assessment="alle modeltekst mist voldoende akoestische steun; geen fraude-score"
    score=None
    features={}
else:
    status="ok"
    assessment="sterke fraude-indicatoren" if score >= 3 else "enkele fraude-indicatoren" if score >= 1 else "onvoldoende tekstsignalen"

channels = {
  "version":"0.2.0",
  "display_policy":{
    "white":"akoestisch voldoende gedragen",
    "purple":"hallucinatiekanaal: onvoldoende akoestische steun",
    "visible_colors_only":["white","purple"],
    "threshold":0.50
  },
  "audio":{"mean_db":mean_db,"max_db":max_db,"acoustic_support":round(acoustic,3)},
  "segments":segments
}
channels_out.write_text(json.dumps(channels, ensure_ascii=False, indent=2))

result={
  "version":"0.2.0",
  "status":status,
  "feature_groups_hit":score,
  "features":features,
  "assessment":assessment,
  "hallucination_segments":sum(1 for s in segments if s["channel"]=="purple"),
  "white_segments":sum(1 for s in segments if s["channel"]=="white"),
  "channels_file":str(channels_out),
  "note":"Fraudeanalyse gebruikt uitsluitend witte segmenten. Paars blijft bewaard als afzonderlijk hallucinatiekanaal en is geen bewijs van externe communicatie of gesproken inhoud."
}
out.write_text(json.dumps(result, ensure_ascii=False, indent=2))
EOS
chmod 644 "$PREFIX/share/wijfraude/analyze.py"

printf '\n✅ Termux-kant geïnstalleerd.\n'
printf 'Commando: %s\n' "$PREFIX/bin/wijfraude-event"
printf 'Cases: %s\n' "$HOME/storage/downloads/WijSAmenFraude"
printf 'Belangrijk: Android moet de app-toestemming “Opnemen” krijgen.\n'
