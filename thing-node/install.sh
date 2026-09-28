#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
BIN="$PREFIX/bin"
APP="$HOME/.local/lib/wijsamen-thing-node"
mkdir -p "$APP" "$HOME/.local/share/wijSamen-thing-node"

pkg install -y python gh curl jq

cp "$(dirname "$0")/thing-node.py" "$APP/thing-node.py"
chmod 700 "$APP/thing-node.py"
cat > "$BIN/thing-node" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
exec python "$APP/thing-node.py" "\$@"
EOF
chmod 700 "$BIN/thing-node"
chmod +x "$(dirname "$0")/build-a52s-vulkan-rpc.sh" "$(dirname "$0")/node-capabilities.sh" 2>/dev/null || true

if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI is nog niet aangemeld. Voer uit: gh auth login"
fi

echo "Thing contact/control node geïnstalleerd."
thing-node status || true
echo
echo "Contact scan:   thing-node scan"
echo "Continu:        termux-wake-lock 2>/dev/null || true; thing-node watch"
echo "Open verzoeken: thing-node pending"
echo
echo "GPU + RPC bouwen: bash $(dirname "$0")/build-a52s-vulkan-rpc.sh"
echo "Capabilities:     bash $(dirname "$0")/node-capabilities.sh"
