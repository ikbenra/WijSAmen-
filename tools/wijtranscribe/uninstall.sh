#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
APP_HOME="${WIJTRANSCRIBE_HOME:-$HOME/.local/share/wijtranscribe}"
BIN_DIR="${PREFIX:-/data/data/com.termux/files/usr}/bin"
rm -f "$BIN_DIR/wijtranscribe"
rm -rf "$APP_HOME"
printf 'wijtranscribe verwijderd. Bestaande transcripties zijn niet verwijderd.\n'
