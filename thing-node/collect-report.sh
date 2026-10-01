#!/data/data/com.termux/files/usr/bin/bash
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
TS="$(date '+%Y%m%d_%H%M%S')"
DEST="${1:-/sdcard/Download/WijSAmenReports}"
mkdir -p "$DEST" 2>/dev/null || true
OUT="$DEST/a52s_report_${TS}.txt"
TMP="${TMPDIR:-$HOME/.cache}/wijsamen-report-$TS"
mkdir -p "$TMP"

redact(){
  sed -E \
    -e 's/([[:xdigit:]]{2}:){5}[[:xdigit:]]{2}/xx:xx:xx:xx:xx:xx/g' \
    -e 's/\b([0-9]{1,3}\.){3}[0-9]{1,3}\b/x.x.x.x/g' \
    -e 's/(serial|android_id|imei|meid)[=:][^[:space:]]+/\1=<redacted>/Ig'
}

section(){ printf '\n===== %s =====\n' "$1"; }

{
  echo "WIJSAMEN A52S REPORT v2"
  echo "created: $(date -Iseconds)"
  echo "privacy: MAC/IPv4/common device-id patterns redacted before output"

  section "TERMUX"
  id
  printf 'python: '; python --version 2>&1 || true
  printf 'java:\n'; java -version 2>&1 | head -n 3 || true
  printf 'git: '; git --version 2>&1 || true
  printf 'gh authenticated: '; gh auth status >/dev/null 2>&1 && echo true || echo false

  section "DOCTOR"
  bash "$HERE/a52s-doctor.sh" "$TMP/capabilities.json" || true
  cat "$TMP/capabilities.json" 2>/dev/null || true

  if command -v rish >/dev/null 2>&1; then
    for probe in id model battery thermal focus adb-state bluetooth-state asi; do
      section "RISH SAFE: $probe"
      bash "$HERE/rish-safe.sh" "$probe" 2>&1 || true
    done
  else
    section "RISH"
    echo "rish unavailable"
  fi

  section "GUARDIAN"
  bash "$HERE/guardian.sh" status 2>&1 || true

  section "VULKAN ICD FILES"
  find "${PREFIX:-/data/data/com.termux/files/usr}/share/vulkan/icd.d" -maxdepth 1 -type f -name '*.json' -printf '%f\n' 2>/dev/null | sort || true

  section "END"
} | redact > "$OUT"

rm -rf "$TMP"
printf '%s\n' "$OUT"
