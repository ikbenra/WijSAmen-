#!/data/data/com.termux/files/usr/bin/bash
set -u

HOME_STATE="$HOME/wijsamen-node"
LOG="$HOME_STATE/guardian.log"
PIDDIR="$HOME_STATE/pids"
mkdir -p "$HOME_STATE" "$PIDDIR"

CHECK_INTERVAL="${WIJSAMEN_CHECK_INTERVAL:-60}"
MIN_BATTERY="${WIJSAMEN_MIN_BATTERY:-20}"
MAX_TEMP_TENTHS_C="${WIJSAMEN_MAX_TEMP_TENTHS_C:-420}"
ENABLE_THING_WATCH="${WIJSAMEN_ENABLE_THING_WATCH:-0}"
ENABLE_LLAMA="${WIJSAMEN_ENABLE_LLAMA:-0}"
LLAMA_PORT="${WIJSAMEN_LLAMA_PORT:-8080}"
LLAMA_MODEL="${WIJSAMEN_MODEL:-}"
LLAMA_BIN="${WIJSAMEN_LLAMA_SERVER:-$HOME/wijsamen-compute/llama.cpp/build-vulkan-rpc/bin/llama-server}"

log(){ printf '%s | %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" | tee -a "$LOG"; }

rish_read(){
  command -v rish >/dev/null 2>&1 || return 1
  rish -c "$1" 2>/dev/null
}

battery_level(){
  rish_read 'dumpsys battery' | awk '/level:/ {print $2; exit}'
}

battery_temp(){
  rish_read 'dumpsys battery' | awk '/temperature:/ {print $2; exit}'
}

is_powered(){
  rish_read 'dumpsys battery' | awk '/AC powered: true|USB powered: true|Wireless powered: true/ {x=1} END{exit !x}'
}

healthy_for_compute(){
  local level temp
  level="$(battery_level || true)"
  temp="$(battery_temp || true)"
  [ -z "$level" ] && level=100
  [ -z "$temp" ] && temp=0

  if [ "$temp" -ge "$MAX_TEMP_TENTHS_C" ] 2>/dev/null; then
    log "compute gate CLOSED: battery temperature=${temp} tenths C"
    return 1
  fi
  if [ "$level" -le "$MIN_BATTERY" ] 2>/dev/null && ! is_powered; then
    log "compute gate CLOSED: battery=${level}% and not charging"
    return 1
  fi
  return 0
}

pidfile(){ printf '%s/%s.pid\n' "$PIDDIR" "$1"; }

alive(){
  local pf pid
  pf="$(pidfile "$1")"
  [ -f "$pf" ] || return 1
  pid="$(cat "$pf" 2>/dev/null || true)"
  [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null
}

stop_service(){
  local name="$1" pf pid
  pf="$(pidfile "$name")"
  if [ -f "$pf" ]; then
    pid="$(cat "$pf" 2>/dev/null || true)"
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
      sleep 2
      kill -9 "$pid" 2>/dev/null || true
      log "stopped $name pid=$pid"
    fi
    rm -f "$pf"
  fi
}

start_thing(){
  [ "$ENABLE_THING_WATCH" = "1" ] || return 0
  command -v thing-node >/dev/null 2>&1 || { log "thing-node unavailable"; return 0; }
  alive thing && return 0
  nohup thing-node watch >>"$HOME_STATE/thing-watch.log" 2>&1 &
  echo $! > "$(pidfile thing)"
  log "started thing-node watch pid=$!"
}

start_llama(){
  [ "$ENABLE_LLAMA" = "1" ] || return 0
  [ -x "$LLAMA_BIN" ] || { log "llama-server unavailable: $LLAMA_BIN"; return 0; }
  [ -n "$LLAMA_MODEL" ] && [ -f "$LLAMA_MODEL" ] || { log "WIJSAMEN_MODEL is missing or not a file; llama stays stopped"; return 0; }
  healthy_for_compute || { stop_service llama; return 0; }
  alive llama && return 0
  # Bind only to loopback. Remote exposure requires a separate explicit private transport.
  nohup "$LLAMA_BIN" -m "$LLAMA_MODEL" --host 127.0.0.1 --port "$LLAMA_PORT" >>"$HOME_STATE/llama.log" 2>&1 &
  echo $! > "$(pidfile llama)"
  log "started llama-server on 127.0.0.1:$LLAMA_PORT pid=$!"
}

status(){
  printf 'guardian log: %s\n' "$LOG"
  printf 'thing enabled=%s alive=' "$ENABLE_THING_WATCH"; alive thing && echo true || echo false
  printf 'llama enabled=%s alive=' "$ENABLE_LLAMA"; alive llama && echo true || echo false
  printf 'battery='; battery_level || true; printf '%%\n'
  printf 'battery_temp_tenths_c='; battery_temp || true; printf '\n'
}

once(){
  start_thing
  if healthy_for_compute; then start_llama; else stop_service llama; fi
}

watch(){
  termux-wake-lock 2>/dev/null || true
  trap 'stop_service thing; stop_service llama; termux-wake-unlock 2>/dev/null || true; exit 0' INT TERM
  log "guardian started interval=${CHECK_INTERVAL}s"
  while true; do
    once
    sleep "$CHECK_INTERVAL"
  done
}

case "${1:-status}" in
  once) once ;;
  watch) watch ;;
  status) status ;;
  stop) stop_service thing; stop_service llama ;;
  *) echo "Gebruik: $0 once|watch|status|stop" >&2; exit 2 ;;
esac
