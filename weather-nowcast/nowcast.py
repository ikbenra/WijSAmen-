#!/usr/bin/env python3
"""WijSAmen 0-3h precipitation nowcaster.

Downloads KNMI's latest seamless precipitation probability forecast and extracts
probabilities for one location. Designed to run in Termux first, before an
Android UI is built around the same core.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np
import requests
import xarray as xr

try:
    from pyproj import CRS, Transformer
except Exception:
    CRS = Transformer = None

API_BASE = "https://api.dataplatform.knmi.nl/open-data/v1"
DATASET = "seamless_precipitation_ensemble_forecast_probabilities"
VERSION = "1.0"
ANON_KEY = (
    "eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6"
    "IjUzYTg1ZDBhMmQ5YzRkYzJiYWNlNzQ4NTQ2Zjk4ODExIiwiaCI6Im11cm11cjEyOCJ9"
)
DEFAULT_LAT = 52.1561
DEFAULT_LON = 5.3878


@dataclass
class GridPoint:
    indexers: dict[str, int]
    latitude: float | None
    longitude: float | None


class KnmiClient:
    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.session.headers.update({"Authorization": api_key, "User-Agent": "WijSAmen-nowcast/0.1"})

    def latest_filename(self) -> str:
        url = f"{API_BASE}/datasets/{DATASET}/versions/{VERSION}/files"
        r = self.session.get(
            url,
            params={"maxKeys": 1, "orderBy": "created", "sorting": "desc"},
            timeout=30,
        )
        r.raise_for_status()
        files = r.json().get("files") or []
        if not files:
            raise RuntimeError("KNMI gaf geen bestanden terug voor de seamless forecast-dataset.")
        return files[0]["filename"]

    def download(self, filename: str, target: Path) -> Path:
        url = f"{API_BASE}/datasets/{DATASET}/versions/{VERSION}/files/{filename}/url"
        r = self.session.get(url, timeout=30)
        r.raise_for_status()
        dl = r.json().get("temporaryDownloadUrl")
        if not dl:
            raise RuntimeError("KNMI gaf geen tijdelijke download-URL terug.")
        with requests.get(dl, stream=True, timeout=120) as src:
            src.raise_for_status()
            with target.open("wb") as out:
                for chunk in src.iter_content(1024 * 1024):
                    if chunk:
                        out.write(chunk)
        return target


def gps_from_termux() -> tuple[float, float] | None:
    exe = shutil.which("termux-location")
    if not exe:
        return None
    for provider in ("gps", "network"):
        try:
            p = subprocess.run(
                [exe, "-p", provider, "-r", "once"],
                capture_output=True,
                text=True,
                timeout=25,
                check=True,
            )
            obj = json.loads(p.stdout)
            return float(obj["latitude"]), float(obj["longitude"])
        except Exception:
            continue
    return None


def _name_score(name: str, attrs: dict, needles: Iterable[str]) -> int:
    text = " ".join([name, str(attrs.get("standard_name", "")), str(attrs.get("long_name", ""))]).lower()
    return sum(1 for n in needles if n in text)


def find_probability_var(ds: xr.Dataset) -> str:
    ranked: list[tuple[int, int, str]] = []
    for name, da in ds.data_vars.items():
        score = _name_score(name, da.attrs, ("probab", "precip", "rain", "threshold", "exceed"))
        if score:
            ranked.append((score, da.ndim, name))
    if not ranked:
        raise RuntimeError("Geen waarschijnlijke neerslagkans-variabele gevonden.")
    ranked.sort(reverse=True)
    return ranked[0][2]


def _find_lat_lon(ds: xr.Dataset):
    lat_names = [n for n in ds.variables if n.lower() in {"lat", "latitude"} or "latitude" in n.lower()]
    lon_names = [n for n in ds.variables if n.lower() in {"lon", "longitude"} or "longitude" in n.lower()]
    for lat_name in lat_names:
        for lon_name in lon_names:
            lat = ds[lat_name]
            lon = ds[lon_name]
            if lat.shape == lon.shape and lat.ndim in (1, 2):
                return lat_name, lon_name
    return None


def nearest_gridpoint(ds: xr.Dataset, da: xr.DataArray, lat: float, lon: float) -> GridPoint:
    ll = _find_lat_lon(ds)
    if ll:
        lat_name, lon_name = ll
        latv = np.asarray(ds[lat_name].values, dtype=float)
        lonv = np.asarray(ds[lon_name].values, dtype=float)
        if latv.ndim == 2:
            d2 = (latv - lat) ** 2 + ((lonv - lon) * math.cos(math.radians(lat))) ** 2
            flat = int(np.nanargmin(d2))
            ij = np.unravel_index(flat, latv.shape)
            dims = ds[lat_name].dims
            idx = {dims[k]: int(ij[k]) for k in range(len(dims)) if dims[k] in da.dims}
            return GridPoint(idx, float(latv[ij]), float(lonv[ij]))
        if latv.ndim == 1:
            ilat = int(np.nanargmin(np.abs(latv - lat)))
            ilon = int(np.nanargmin(np.abs(lonv - lon)))
            idx = {}
            if ds[lat_name].dims[0] in da.dims:
                idx[ds[lat_name].dims[0]] = ilat
            if ds[lon_name].dims[0] in da.dims:
                idx[ds[lon_name].dims[0]] = ilon
            return GridPoint(idx, float(latv[ilat]), float(lonv[ilon]))

    spatial_dims = [d for d in da.dims if d.lower() in {"x", "y", "projection_x_coordinate", "projection_y_coordinate"}]
    if len(spatial_dims) >= 2 and CRS and Transformer:
        mapping_name = da.attrs.get("grid_mapping")
        if mapping_name and mapping_name in ds.variables:
            crs = CRS.from_cf(ds[mapping_name].attrs)
            tr = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
            tx, ty = tr.transform(lon, lat)
            xname = next((d for d in da.dims if d.lower().startswith("x") or "projection_x" in d.lower()), None)
            yname = next((d for d in da.dims if d.lower().startswith("y") or "projection_y" in d.lower()), None)
            if xname and yname and xname in ds.coords and yname in ds.coords:
                ix = int(np.nanargmin(np.abs(np.asarray(ds[xname].values, float) - tx)))
                iy = int(np.nanargmin(np.abs(np.asarray(ds[yname].values, float) - ty)))
                return GridPoint({xname: ix, yname: iy}, None, None)

    raise RuntimeError("Kon de opgegeven GPS-locatie niet aan het KNMI-raster koppelen.")


def find_dim(da: xr.DataArray, keywords: tuple[str, ...]) -> str | None:
    for d in da.dims:
        low = d.lower()
        if any(k in low for k in keywords):
            return d
    return None


def threshold_values(ds: xr.Dataset, da: xr.DataArray, dim: str | None) -> list[float] | None:
    if not dim:
        return None
    if dim in ds.coords:
        vals = np.asarray(ds[dim].values).reshape(-1)
        try:
            return [float(v) for v in vals]
        except Exception:
            pass
    return None


def as_percent(v: float) -> float:
    if not np.isfinite(v):
        return float("nan")
    return float(v * 100.0 if -0.001 <= v <= 1.001 else v)


def format_time(v) -> str:
    try:
        return str(np.datetime64(v, "m")).replace("T", " ")
    except Exception:
        return str(v)


def extract_rows(ds: xr.Dataset, lat: float, lon: float, horizon_minutes: int = 180):
    var_name = find_probability_var(ds)
    da = ds[var_name]
    point = nearest_gridpoint(ds, da, lat, lon)
    da = da.isel(**point.indexers)

    time_dim = find_dim(da, ("time", "forecast", "lead"))
    threshold_dim = find_dim(da, ("threshold", "thresh"))
    thresholds = threshold_values(ds, da, threshold_dim)

    known = {d for d in (time_dim, threshold_dim) if d}
    for dim in list(da.dims):
        if dim not in known:
            da = da.isel({dim: 0})

    if not time_dim:
        raise RuntimeError(f"Geen tijdsdimensie gevonden in variabele {var_name!r} met dimensies {da.dims}.")

    times = ds[time_dim].values if time_dim in ds.variables else np.arange(da.sizes[time_dim])
    count = min(da.sizes[time_dim], max(1, horizon_minutes // 5))
    rows = []
    for ti in range(count):
        slice_t = da.isel({time_dim: ti})
        probs: dict[str, float] = {}
        if threshold_dim and threshold_dim in slice_t.dims:
            vals = np.asarray(slice_t.values, dtype=float).reshape(-1)
            if thresholds is None or len(thresholds) != len(vals):
                thresholds = list(range(len(vals)))
            for th, value in zip(thresholds, vals):
                probs[f">={th:g} mm/h"] = round(as_percent(float(value)), 1)
        else:
            value = float(np.asarray(slice_t.values).reshape(-1)[0])
            probs["precipitation"] = round(as_percent(value), 1)
        rows.append({"time": format_time(times[ti]) if ti < len(times) else f"+{(ti+1)*5}m", "probabilities": probs})
    return var_name, point, rows


def print_forecast(rows: list[dict]):
    print("\nWijSAmen 0–3 uur neerslagkans")
    print("-" * 78)
    if not rows:
        print("Geen forecastregels gevonden.")
        return
    keys = list(rows[0]["probabilities"].keys())
    show_keys = keys[:6]
    print("tijd".ljust(18) + "  " + "  ".join(k.rjust(11) for k in show_keys))
    print("-" * 78)
    for row in rows:
        probs = row["probabilities"]
        values = [f"{probs.get(k, float('nan')):>9.1f}%" for k in show_keys]
        print(row["time"][:16].ljust(18) + "  " + "  ".join(values))


def log_snapshot(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, default=str) + "\n")


def diagnostic(ds: xr.Dataset):
    print("\n--- KNMI NetCDF diagnose ---")
    print("dimensions:", dict(ds.sizes))
    print("coordinates:", list(ds.coords))
    print("data variables:")
    for name, da in ds.data_vars.items():
        print(f"  {name}: dims={da.dims} shape={da.shape} units={da.attrs.get('units')} long_name={da.attrs.get('long_name')}")


def main() -> int:
    p = argparse.ArgumentParser(description="KNMI seamless 0-3h nowcast for one location")
    p.add_argument("--lat", type=float)
    p.add_argument("--lon", type=float)
    p.add_argument("--gps", action="store_true", help="use termux-location if available")
    p.add_argument("--hours", type=float, default=3.0)
    p.add_argument("--keep", action="store_true", help="keep downloaded NetCDF file")
    p.add_argument("--diagnose", action="store_true", help="print dataset structure")
    p.add_argument("--no-log", action="store_true")
    args = p.parse_args()

    lat, lon = args.lat, args.lon
    if args.gps:
        gps = gps_from_termux()
        if gps:
            lat, lon = gps
        else:
            print("Geen Termux GPS-resultaat; gebruik --lat en --lon.", file=sys.stderr)
    if lat is None or lon is None:
        lat, lon = DEFAULT_LAT, DEFAULT_LON
        print(f"Geen locatie opgegeven: tijdelijke fallback {lat:.4f}, {lon:.4f} (Amersfoort).")

    api_key = os.environ.get("KNMI_API_KEY", ANON_KEY).strip()
    client = KnmiClient(api_key)
    workdir = Path.cwd() / "data"
    workdir.mkdir(exist_ok=True)

    try:
        filename = client.latest_filename()
        target = workdir / filename
        if not target.exists():
            print(f"Download nieuwste KNMI-forecast: {filename}")
            client.download(filename, target)
        else:
            print(f"Gebruik al gedownload bestand: {filename}")

        ds = xr.open_dataset(target, decode_times=True)
        if args.diagnose:
            diagnostic(ds)
        var_name, point, rows = extract_rows(ds, lat, lon, int(args.hours * 60))
        print(f"Locatie gevraagd: {lat:.5f}, {lon:.5f}")
        if point.latitude is not None:
            print(f"Rasterpunt gebruikt: {point.latitude:.5f}, {point.longitude:.5f}")
        print(f"KNMI variabele: {var_name}")
        print_forecast(rows)

        payload = {
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "source": "KNMI seamless precipitation ensemble forecast probabilities 1.0",
            "filename": filename,
            "requested_location": {"lat": lat, "lon": lon},
            "grid_location": {"lat": point.latitude, "lon": point.longitude, "indexers": point.indexers},
            "variable": var_name,
            "forecast": rows,
        }
        if not args.no_log:
            log_snapshot(Path("logs/forecast_history.jsonl"), payload)
            print("\nSnapshot gelogd in logs/forecast_history.jsonl")
        if not args.keep:
            try:
                ds.close()
                target.unlink(missing_ok=True)
            except Exception:
                pass
        return 0
    except Exception as e:
        print(f"\nFOUT: {e}", file=sys.stderr)
        print("Tip: voer dezelfde opdracht uit met --diagnose en stuur de uitvoer aan ChatGPT.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
