#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

pkg update
pkg install -y git python python-numpy clang make pkg-config hdf5 libnetcdf termux-api
python -m pip install --no-cache-dir -r requirements.txt

printf '\nKlaar. Controleer ook dat de Android-app Termux:API is geïnstalleerd en locatiepermissie heeft.\n'
printf 'Snelste validatie:\n  bash validate_live.sh\n'
