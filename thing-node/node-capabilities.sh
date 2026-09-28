#!/data/data/com.termux/files/usr/bin/bash
set -u
ROOT="$HOME/wijsamen-compute"
BUILD="$ROOT/llama.cpp/build-vulkan-rpc"
export VK_ICD_FILENAMES="${VK_ICD_FILENAMES:-$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json}"

json_escape(){ python -c 'import json,sys; print(json.dumps(sys.stdin.read()))'; }

DEVICE="$(getprop ro.product.model 2>/dev/null || echo Android)"
SOC="$(getprop ro.soc.model 2>/dev/null || true)"
ANDROID="$(getprop ro.build.version.release 2>/dev/null || true)"
RAM_KB="$(awk '/MemTotal/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)"
VULKAN_SUMMARY="$(vulkaninfo --summary 2>/dev/null | head -n 120 || true)"
LLAMA_DEVICES="$("$BUILD/bin/llama-cli" --list-devices 2>&1 || true)"
RPC_OK=false
[ -x "$BUILD/bin/ggml-rpc-server" ] && RPC_OK=true
VULKAN_OK=false
printf '%s' "$LLAMA_DEVICES" | grep -qi 'Vulkan' && VULKAN_OK=true

cat <<EOF
{
  "protocol": "WIJSAMEN-COMPUTE/1",
  "node_id": "a52s-termux-local",
  "device": $(printf '%s' "$DEVICE" | json_escape),
  "soc": $(printf '%s' "$SOC" | json_escape),
  "android": $(printf '%s' "$ANDROID" | json_escape),
  "ram_kb": $RAM_KB,
  "backends": {
    "cpu": true,
    "vulkan_verified": $VULKAN_OK,
    "llama_rpc_binary": $RPC_OK
  },
  "security": {
    "public_rpc": false,
    "requires_private_transport": true,
    "arbitrary_shell": false
  },
  "vulkan_summary": $(printf '%s' "$VULKAN_SUMMARY" | json_escape),
  "llama_devices": $(printf '%s' "$LLAMA_DEVICES" | json_escape)
}
EOF
