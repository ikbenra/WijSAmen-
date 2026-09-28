#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT="$HOME/wijsamen-compute"
SRC="$ROOT/llama.cpp"
BUILD="$SRC/build-vulkan-rpc"

pkg update -y
pkg install -y git cmake clang ninja python curl jq gh x11-repo tur-repo || true

# Vulkan + shader/SPIR-V toolchain. llama.cpp's Vulkan backend needs
# SPIRV-Headers explicitly; having libvulkan + glslc alone is not enough.
pkg install -y vulkan-headers shaderc spirv-headers spirv-tools glslang || true

# Prefer the generic loader + Freedreno/Turnip stack on the A52s where available.
# Fall back to Android loader naming if the generic package is unavailable.
pkg install -y vulkan-loader-generic vulkan-tools mesa-vulkan-icd-freedreno || \
  pkg install -y vulkan-loader-android vulkan-tools mesa-vulkan-icd-freedreno || true

mkdir -p "$ROOT"
if [ ! -d "$SRC/.git" ]; then
  git clone https://github.com/ggml-org/llama.cpp.git "$SRC"
else
  git -C "$SRC" fetch --all --prune
  git -C "$SRC" pull --ff-only || true
fi

# Override with e.g. LLAMA_REF=<commit-or-tag> bash build-a52s-vulkan-rpc.sh
if [ -n "${LLAMA_REF:-}" ]; then
  git -C "$SRC" checkout "$LLAMA_REF"
fi

export VK_ICD_FILENAMES="${VK_ICD_FILENAMES:-$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json}"
export ASAN_OPTIONS="${ASAN_OPTIONS:-detect_leaks=0}"

# A failed CMake configure may leave an incomplete cache; clean only the build dir.
rm -rf "$BUILD"

cmake -S "$SRC" -B "$BUILD" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_VULKAN=ON \
  -DGGML_RPC=ON \
  -DGGML_OPENMP=ON

cmake --build "$BUILD" --config Release --parallel "$(nproc)"

echo
echo '=== Vulkan ==='
vulkaninfo --summary 2>/dev/null || true

echo
echo '=== llama.cpp devices ==='
"$BUILD/bin/llama-cli" --list-devices || true

echo
echo '=== binaries ==='
for f in llama-cli llama-server ggml-rpc-server; do
  if [ -x "$BUILD/bin/$f" ]; then echo "OK $BUILD/bin/$f"; else echo "MISSING $f"; fi
done

echo
echo 'Build complete.'
echo 'Do NOT expose ggml-rpc-server directly to the public Internet.'
echo 'Use a private LAN/VPN/SSH tunnel and verify the device list first.'
