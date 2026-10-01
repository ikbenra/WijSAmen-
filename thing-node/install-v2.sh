#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
BIN="${PREFIX:-/data/data/com.termux/files/usr}/bin"

pkg update -y
pkg install -y python git gh jq openjdk-17 curl

chmod +x \
  "$HERE/a52s-doctor.sh" \
  "$HERE/rish-safe.sh" \
  "$HERE/guardian.sh" \
  "$HERE/collect-report.sh" \
  "$HERE/local-tool-bridge.py" \
  "$HERE/install.sh" \
  "$HERE/build-a52s-vulkan-rpc.sh" \
  "$HERE/node-capabilities.sh"

# Existing thing-node installer provides the queue/watch CLI.
bash "$HERE/install.sh"

link(){
  local src="$1" name="$2"
  ln -sf "$src" "$BIN/$name"
}

link "$HERE/a52s-doctor.sh" a52s-doctor
link "$HERE/rish-safe.sh" rish-safe
link "$HERE/guardian.sh" wijsamen-guardian
link "$HERE/collect-report.sh" wijsamen-report
link "$HERE/local-tool-bridge.py" wijsamen-local-tools

# Project-miner and authorization compiler live one directory above thing-node.
if [ -f "$HERE/../project-miner/mine_chats.py" ]; then
  chmod +x "$HERE/../project-miner/mine_chats.py"
  link "$HERE/../project-miner/mine_chats.py" wijsamen-mine-chats
fi
if [ -f "$HERE/../authority/authorize.py" ]; then
  chmod +x "$HERE/../authority/authorize.py"
  link "$HERE/../authority/authorize.py" wijsamen-authorize
fi

mkdir -p "$HOME/wijsamen-node/state"

echo
echo '=== WijSAmen A52s v2 geïnstalleerd ==='
echo 'Read-only systeemarm:  rish-safe help'
echo 'Capability probe:       a52s-doctor'
echo 'Eén rapportbestand:      wijsamen-report'
echo 'Guardian status:         wijsamen-guardian status'
echo 'Lokale toolbridge:       wijsamen-guardian once'
echo 'Chat-export miner:       wijsamen-mine-chats <export.json>'
echo 'Actie-autorisatie:       wijsamen-authorize request.json'
echo
echo 'Vulkan/llama.cpp build is bewust NIET automatisch gestart.'
echo 'Start die zware test afzonderlijk met:'
echo "  bash $HERE/build-a52s-vulkan-rpc.sh"
echo

bash "$HERE/a52s-doctor.sh" || true
