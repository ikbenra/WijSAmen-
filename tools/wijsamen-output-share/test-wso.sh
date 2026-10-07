#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
WSO="$ROOT/wso"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

export HOME="$TMP/home"
export WSO_BASE="$TMP/base"
mkdir -p "$HOME/storage/downloads" "$TMP/bin" "$WSO_BASE/logs"
export PATH="$TMP/bin:$PATH"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

assert_file() {
  [ -f "$1" ] || fail "missing file: $1"
}

cat > "$TMP/bin/termux-open" <<'STUB'
#!/usr/bin/env bash
printf '%s\n' "$*" > "$WSO_TEST_TERMUX_OPEN_ARGS"
STUB
chmod +x "$TMP/bin/termux-open"
export WSO_TEST_TERMUX_OPEN_ARGS="$TMP/termux-open.args"

RAW="$WSO_BASE/logs/session_fixture.log"
printf 'regel 1\r\n\033[31mrood\033[0m\rregel 3\n' > "$RAW"
ln -s "$RAW" "$WSO_BASE/current.log"

bash "$WSO" export > "$TMP/export.out"
CLEAN="$WSO_BASE/share/LATEST.txt"
RAW_COPY="$WSO_BASE/share/LATEST_RAW.log"
DOWNLOAD_COPY="$HOME/storage/downloads/WijSAmen_Termux_LATEST.txt"

assert_file "$CLEAN"
assert_file "$RAW_COPY"
assert_file "$DOWNLOAD_COPY"
cmp -s "$RAW" "$RAW_COPY" || fail "raw export changed"
cmp -s "$CLEAN" "$DOWNLOAD_COPY" || fail "Downloads copy differs"

python - "$CLEAN" <<'PY'
from pathlib import Path
import sys
data = Path(sys.argv[1]).read_bytes()
if b"\x1b" in data:
    raise SystemExit("FAIL: ANSI escape remained in clean export")
text = data.decode("utf-8")
if text != "regel 1\nrood\nregel 3\n":
    raise SystemExit(f"FAIL: unexpected clean export: {text!r}")
PY

bash "$WSO" share > "$TMP/share.out"
assert_file "$WSO_TEST_TERMUX_OPEN_ARGS"
ARGS="$(cat "$WSO_TEST_TERMUX_OPEN_ARGS")"
case "$ARGS" in
  *"--send"*"--chooser"*"--content-type text/plain"*) ;;
  *) fail "unexpected termux-open arguments: $ARGS" ;;
esac

set +e
bash "$WSO" run bash -c 'printf "run-ok\n"; exit 7' > "$TMP/run.out" 2>&1
RC=$?
set -e
[ "$RC" -eq 7 ] || fail "wso run did not preserve exit code (got $RC)"
RUN_LOG="$(readlink -f "$WSO_BASE/current.log")"
assert_file "$RUN_LOG"
grep -Fq "run-ok" "$RUN_LOG" || fail "command output absent from run log"
grep -Fq "[exit=7]" "$RUN_LOG" || fail "exit marker absent from run log"

echo "PASS: raw preservation, ANSI-clean export, Downloads mirror, visible share and exit propagation"

