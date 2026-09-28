#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
BIN="$PREFIX/bin"
APP="$HOME/.local/lib/wijsamen-thing-node"
mkdir -p "$APP" "$HOME/.local/share/wijSamen-thing-node"

echo "[1/4] Benodigde Termux-pakketten"
pkg install -y python gh curl jq

if command -v termux-notification >/dev/null 2>&1; then
  echo "Termux:API command gevonden."
else
  echo "Optioneel: installeer de Termux:API app + 'pkg install termux-api' voor Android-meldingen."
fi

echo "[2/4] Node installeren"
cp "$(dirname "$0")/thing-node.py" "$APP/thing-node.py"
chmod 700 "$APP/thing-node.py"
cat > "$BIN/thing-node" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
exec python "$APP/thing-node.py" "\$@"
EOF
chmod 700 "$BIN/thing-node"

echo "[3/4] GitHub-login controleren"
if ! gh auth status >/dev/null 2>&1; then
  echo "Voer nu eenmalig uit: gh auth login"
  echo "Daarna: thing-node scan"
else
  echo "GitHub-login aanwezig."
fi

echo "[4/4] Klaar"
thing-node status
echo
echo "Test:        thing-node scan"
echo "Wachtrij:    thing-node pending"
echo "Continu:     termux-wake-lock 2>/dev/null || true; thing-node watch"
echo "Goedkeuren:  thing-node approve COMMENT_ID"
echo "Weigeren:    thing-node deny COMMENT_ID"
