#!/data/data/com.termux/files/usr/bin/bash
set -e

pkg update
pkg upgrade -y
pkg install -y git python python-numpy clang make pkg-config hdf5 libnetcdf
python -m pip install --no-cache-dir requests xarray h5netcdf pyproj

printf '\nKlaar. Test met:\n  python nowcast.py --gps --hours 3\n'
