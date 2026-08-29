#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

cd "$(dirname "$0")"
python test_core.py
python nowcast.py --validate-live "$@"
