#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

if ! command -v rish >/dev/null 2>&1; then
  echo "rish is niet beschikbaar. Start Shizuku en configureer 'Use Shizuku in terminal apps'." >&2
  exit 1
fi

cmd="${1:-help}"

run() {
  # Commands are fixed strings below; user input is never concatenated into shell code.
  rish -c "$1"
}

case "$cmd" in
  id)
    run 'id'
    ;;
  model)
    run 'getprop ro.product.model; getprop ro.soc.model; getprop ro.build.version.release; getprop ro.build.version.sdk'
    ;;
  battery)
    run "dumpsys battery | grep -E 'level:|status:|temperature:|AC powered:|USB powered:|Wireless powered:'"
    ;;
  thermal)
    run "dumpsys thermalservice 2>/dev/null | grep -E 'Thermal Status|mStatus|Current temperatures|Temperature\\{' | head -n 100"
    ;;
  focus)
    run "dumpsys activity activities 2>/dev/null | grep -E 'topResumedActivity|mResumedActivity' | head -n 8"
    ;;
  visible)
    run "dumpsys activity activities 2>/dev/null | grep -E 'ResumedActivity|mResumedActivity|visible=true' | head -n 80"
    ;;
  wm)
    run 'wm size; wm density'
    ;;
  adb-state)
    run 'settings get global adb_enabled; settings get global adb_wifi_enabled'
    ;;
  bluetooth-state)
    run "dumpsys bluetooth_manager 2>/dev/null | grep -E 'State:|ConnectionState:|Name:' | head -n 40"
    ;;
  media)
    run "dumpsys media_session 2>/dev/null | head -n 160"
    ;;
  asi)
    run "dumpsys package com.google.android.as 2>/dev/null | grep -E 'stopped=|enabled=|versionName=|versionCode=' | head -n 40"
    ;;
  processes)
    run "ps -A -o USER,PID,NAME 2>/dev/null | head -n 100"
    ;;
  help|-h|--help|'')
    cat <<'EOF'
WijSAmen rish-safe — vaste read-only Shizuku probes

  rish-safe id
  rish-safe model
  rish-safe battery
  rish-safe thermal
  rish-safe focus
  rish-safe visible
  rish-safe wm
  rish-safe adb-state
  rish-safe bluetooth-state
  rish-safe media
  rish-safe asi
  rish-safe processes

Er bestaat bewust geen 'raw', 'exec' of willekeurige shellmodus.
Schrijfacties horen in een aparte, expliciet geautoriseerde laag.
EOF
    ;;
  *)
    echo "Niet-toegestaan commando: $cmd" >&2
    echo "Gebruik: $0 help" >&2
    exit 2
    ;;
esac
