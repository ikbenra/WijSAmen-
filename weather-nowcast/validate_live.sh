#!/data/data/com.termux/files/usr/bin/bash
set -uo pipefail

cd "$(dirname "$0")"
python test_core.py || exit $?

attempt=1
max_attempts=4
for wait_seconds in 0 2 5 10; do
  if (( wait_seconds > 0 )); then
    echo "KNMI gedeeld quotum was bezet; nieuwe poging over ${wait_seconds}s..." >&2
    sleep "$wait_seconds"
  fi

  output="$(python nowcast.py --validate-live "$@" 2>&1)"
  status=$?
  printf '%s\n' "$output"

  if (( status == 0 )); then
    exit 0
  fi
  if ! grep -q "429 Client Error" <<<"$output"; then
    exit "$status"
  fi
  if (( attempt >= max_attempts )); then
    echo "LIVE VALIDATION: geblokkeerd door KNMI 429 na ${max_attempts} pogingen." >&2
    exit "$status"
  fi
  ((attempt++))
done
