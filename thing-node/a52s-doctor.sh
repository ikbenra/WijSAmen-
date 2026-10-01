#!/data/data/com.termux/files/usr/bin/bash
set -u

OUT="${1:-$HOME/wijsamen-node/state/capabilities.json}"
ROOT="$HOME/wijsamen-compute"
BUILD="$ROOT/llama.cpp/build-vulkan-rpc"
mkdir -p "$(dirname "$OUT")"

safe_cmd() {
  "$@" 2>&1 || true
}

redact() {
  # Redact common MAC and IPv4 forms before persisting diagnostic text.
  sed -E \
    -e 's/([[:xdigit:]]{2}:){5}[[:xdigit:]]{2}/xx:xx:xx:xx:xx:xx/g' \
    -e 's/\b([0-9]{1,3}\.){3}[0-9]{1,3}\b/x.x.x.x/g'
}

MODEL="$(getprop ro.product.model 2>/dev/null || true)"
SOC="$(getprop ro.soc.model 2>/dev/null || true)"
ANDROID="$(getprop ro.build.version.release 2>/dev/null || true)"
SDK="$(getprop ro.build.version.sdk 2>/dev/null || true)"
RAM_KB="$(awk '/MemTotal/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)"
HOME_FREE_KB="$(df -Pk "$HOME" 2>/dev/null | awk 'NR==2 {print $4}' || echo 0)"

RISH_ID=""
if command -v rish >/dev/null 2>&1; then
  RISH_ID="$(rish -c 'id' 2>/dev/null | redact)"
fi

BATTERY=""
THERMAL=""
if command -v rish >/dev/null 2>&1; then
  BATTERY="$(rish -c 'dumpsys battery' 2>/dev/null | grep -E 'level:|status:|temperature:|AC powered:|USB powered:|Wireless powered:' | redact)"
  THERMAL="$(rish -c 'dumpsys thermalservice' 2>/dev/null | grep -E 'Thermal Status|mStatus|Current temperatures|Temperature\{' | head -n 80 | redact)"
fi

JAVA_VERSION="$(java -version 2>&1 | head -n 3 | redact)"
PYTHON_VERSION="$(python --version 2>&1 | head -n 1 | redact)"
GIT_VERSION="$(git --version 2>&1 | head -n 1 | redact)"
GH_AUTH=false
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then GH_AUTH=true; fi

ICD_DIR="${PREFIX:-/data/data/com.termux/files/usr}/share/vulkan/icd.d"
ICDS="$(find "$ICD_DIR" -maxdepth 1 -type f -name '*.json' -printf '%f\n' 2>/dev/null | sort | redact)"
VULKAN_SUMMARY="$(vulkaninfo --summary 2>/dev/null | head -n 160 | redact || true)"
LLAMA_DEVICES=""
if [ -x "$BUILD/bin/llama-cli" ]; then
  LLAMA_DEVICES="$("$BUILD/bin/llama-cli" --list-devices 2>&1 | head -n 160 | redact || true)"
fi

VULKAN_VERIFIED=false
printf '%s\n' "$LLAMA_DEVICES" | grep -qi 'Vulkan' && VULKAN_VERIFIED=true
ADRENO_SEEN=false
printf '%s\n%s\n' "$VULKAN_SUMMARY" "$LLAMA_DEVICES" | grep -qi 'Adreno' && ADRENO_SEEN=true
RPC_BINARY=false
[ -x "$BUILD/bin/ggml-rpc-server" ] && RPC_BINARY=true

export MODEL SOC ANDROID SDK RAM_KB HOME_FREE_KB RISH_ID BATTERY THERMAL JAVA_VERSION PYTHON_VERSION GIT_VERSION
export GH_AUTH ICDS VULKAN_SUMMARY LLAMA_DEVICES VULKAN_VERIFIED ADRENO_SEEN RPC_BINARY OUT
python - <<'PY'
import json, os
from pathlib import Path

def n(name, default=0):
    try: return int(os.environ.get(name, str(default)) or default)
    except Exception: return default

def b(name):
    return os.environ.get(name, "false").lower() == "true"

obj = {
  "protocol": "WIJSAMEN-NODE-CAPABILITIES/2",
  "node_id": "a52s-termux-local",
  "device": {
    "model": os.environ.get("MODEL", ""),
    "soc": os.environ.get("SOC", ""),
    "android": os.environ.get("ANDROID", ""),
    "sdk": os.environ.get("SDK", ""),
    "ram_kb": n("RAM_KB"),
    "home_free_kb": n("HOME_FREE_KB"),
  },
  "privilege_bridge": {
    "rish_present": bool(os.environ.get("RISH_ID")),
    "rish_identity": os.environ.get("RISH_ID", ""),
    "shell_uid_2000": "uid=2000" in os.environ.get("RISH_ID", ""),
  },
  "toolchain": {
    "java": os.environ.get("JAVA_VERSION", ""),
    "python": os.environ.get("PYTHON_VERSION", ""),
    "git": os.environ.get("GIT_VERSION", ""),
    "github_cli_authenticated": b("GH_AUTH"),
  },
  "compute": {
    "vulkan_icds": [x for x in os.environ.get("ICDS", "").splitlines() if x],
    "vulkan_verified_by_llama": b("VULKAN_VERIFIED"),
    "adreno_name_seen": b("ADRENO_SEEN"),
    "llama_rpc_binary": b("RPC_BINARY"),
    "vulkan_summary": os.environ.get("VULKAN_SUMMARY", ""),
    "llama_devices": os.environ.get("LLAMA_DEVICES", ""),
  },
  "health": {
    "battery_summary": os.environ.get("BATTERY", ""),
    "thermal_summary": os.environ.get("THERMAL", ""),
  },
  "security": {
    "public_rpc": False,
    "arbitrary_shell_from_remote": False,
    "redacts_mac_and_ipv4_before_persist": True,
    "probe_is_read_only": True,
  },
}
path = Path(os.environ["OUT"]).expanduser()
path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(path)
print(json.dumps({
    "shell_uid_2000": obj["privilege_bridge"]["shell_uid_2000"],
    "vulkan_verified_by_llama": obj["compute"]["vulkan_verified_by_llama"],
    "adreno_name_seen": obj["compute"]["adreno_name_seen"],
    "llama_rpc_binary": obj["compute"]["llama_rpc_binary"],
    "github_cli_authenticated": obj["toolchain"]["github_cli_authenticated"],
}, indent=2))
PY
