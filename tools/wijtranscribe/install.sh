#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

APP_NAME="wijtranscribe"
APP_HOME="${WIJTRANSCRIBE_HOME:-$HOME/.local/share/$APP_NAME}"
BIN_DIR="${PREFIX:-/data/data/com.termux/files/usr}/bin"
MODEL="${WIJTRANSCRIBE_MODEL:-base}"
WHISPER_REPO="https://github.com/ggml-org/whisper.cpp.git"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

say() { printf '\n[%s] %s\n' "$APP_NAME" "$*"; }
die() { printf '\n[%s] FOUT: %s\n' "$APP_NAME" "$*" >&2; exit 1; }

command -v pkg >/dev/null 2>&1 || die "Dit installatieprogramma is bedoeld voor Termux."

say "Pakketten installeren/bijwerken"
pkg update -y
pkg install -y git cmake clang make ffmpeg curl coreutils

if command -v termux-setup-storage >/dev/null 2>&1 && [ ! -d "$HOME/storage/shared" ]; then
  say "Android-opslagtoegang aanvragen"
  termux-setup-storage || true
fi

mkdir -p "$APP_HOME" "$APP_HOME/models" "$APP_HOME/tmp"

if [ -d "$APP_HOME/whisper.cpp/.git" ]; then
  say "whisper.cpp bijwerken"
  git -C "$APP_HOME/whisper.cpp" fetch --depth 1 origin master
  git -C "$APP_HOME/whisper.cpp" reset --hard origin/master
else
  say "whisper.cpp ophalen"
  rm -rf "$APP_HOME/whisper.cpp"
  git clone --depth 1 "$WHISPER_REPO" "$APP_HOME/whisper.cpp"
fi

NPROC="$(nproc 2>/dev/null || echo 2)"
JOBS="${WIJTRANSCRIBE_BUILD_JOBS:-$NPROC}"
if [ "$JOBS" -gt 4 ] 2>/dev/null; then JOBS=4; fi
if [ "$JOBS" -lt 1 ] 2>/dev/null; then JOBS=1; fi

say "whisper.cpp bouwen met $JOBS parallelle taak/taken"
cmake -S "$APP_HOME/whisper.cpp" -B "$APP_HOME/whisper.cpp/build" -DCMAKE_BUILD_TYPE=Release
cmake --build "$APP_HOME/whisper.cpp/build" -j "$JOBS" --config Release

CLI="$APP_HOME/whisper.cpp/build/bin/whisper-cli"
[ -x "$CLI" ] || die "whisper-cli is na het bouwen niet gevonden."

MODEL_TARGET="$APP_HOME/models/ggml-$MODEL.bin"
if [ ! -f "$MODEL_TARGET" ]; then
  say "Whisper-model '$MODEL' downloaden"
  sh "$APP_HOME/whisper.cpp/models/download-ggml-model.sh" "$MODEL" "$APP_HOME/models"
fi

say "commando installeren als $BIN_DIR/wijtranscribe"
install -m 0755 "$SCRIPT_DIR/bin/wijtranscribe" "$BIN_DIR/wijtranscribe"
install -m 0644 "$SCRIPT_DIR/VERSION" "$APP_HOME/VERSION"

cat > "$APP_HOME/config" <<CFG
WIJTRANSCRIBE_MODEL=$MODEL
CFG

say "zelftest"
WIJTRANSCRIBE_HOME="$APP_HOME" "$BIN_DIR/wijtranscribe" doctor

printf '\nKlaar. Gebruik bijvoorbeeld:\n  wijtranscribe ~/storage/downloads/funghi\n\n'
