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


@dataclass
class SourceFile:
    filename: str
    created: str | None = None
    last_modified: str | None = None
    size: int | None = None
    deprecation: str | None = None


@dataclass
class TermuxLocation:
    latitude: float
    longitude: float
    provider: str


class KnmiClient:
    def __init__(self, api_key: str):
        self.session = requests.Session()
        self.session.headers.update({"Authorization": api_key, "User-Agent": "WijSAmen-nowcast/0.2"})

    @staticmethod
    def _deprecation(response: requests.Response) -> str | None:
        return response.headers.get("X-KNMI-Deprecation")

    def latest_file(self) -> SourceFile:
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
        item = files[0]
        filename = item.get("filename")
        if not filename:
            raise RuntimeError("KNMI latest-file antwoord bevat geen bestandsnaam.")
        size = item.get("size")
        try:
            size = int(size) if size is not None else None
        except (TypeError, ValueError):
            size = None
        return SourceFile(
            filename=filename,
            created=item.get("created"),
            last_modified=item.get("lastModified"),
            size=size,
            deprecation=self._deprecation(r),
        )

    def download(self, source: SourceFile, target: Path) -> tuple[Path, str | None]:
        url = f"{API_BASE}/datasets/{DATASET}/versions/{VERSION}/files/{source.filename}/url"
        r = self.session.get(url, timeout=30)
        r.raise_for_status()
        deprecation = self._deprecation(r) or source.deprecation
        dl = r.json().get("temporaryDownloadUrl")
        if not dl:
            raise RuntimeError("KNMI gaf geen tijdelijke download-URL terug.")
        # A KNMI temporary URL is already signed; do not send the API key to it.
        with requests.get(dl, stream=True, timeout=120) as src:
            src.raise_for_status()
            with target.open("wb") as out:
                for chunk in src.iter_content(1024 * 1024):
                    if chunk:
                        out.write(chunk)
        return target, deprecation


def gps_from_termux() -> TermuxLocation | None:
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
            return TermuxLocation(float(obj["latitude"]), float(obj["longitude"]), provider)
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
    ranked: list[tuple[int, int, int, str]] = []
    for pos, dim in enumerate(da.dims):
        low = dim.lower()
        score = sum(1 for k in keywords if k in low)
        if score:
            exact = 1 if low in keywords else 0
            ranked.append((exact, score, -pos, dim))
    if not ranked:
        return None
    ranked.sort(reverse=True)
    return ranked[0][3]


def _coord_for_dim(ds: xr.Dataset, da: xr.DataArray, dim: str) -> xr.DataArray | None:
    if dim in da.coords:
        return da.coords[dim]
    if dim in ds.coords:
        return ds.coords[dim]
    if dim in ds.variables and ds[dim].dims == (dim,):
        return ds[dim]

    candidates: list[tuple[int, str]] = []
    for name, coord in ds.coords.items():
        if coord.dims == (dim,):
            score = _name_score(name, coord.attrs, ("time", "forecast", "lead", "threshold"))
            candidates.append((score, name))
    if candidates:
        candidates.sort(reverse=True)
        return ds.coords[candidates[0][1]]
    return None


def threshold_values(ds: xr.Dataset, da: xr.DataArray, dim: str | None) -> list[float] | None:
    if not dim:
        return None
    coord = _coord_for_dim(ds, da, dim)
    if coord is None:
        return None
    vals = np.asarray(coord.values).reshape(-1)
    try:
        return [float(v) for v in vals]
    except Exception:
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


def _unit_factor_minutes(units: str) -> float | None:
    low = units.lower()
    if "second" in low:
        return 1.0 / 60.0
    if "minute" in low:
        return 1.0
    if "hour" in low:
        return 60.0
    if "day" in low:
        return 1440.0
    return None


def _time_axis(ds: xr.Dataset, da: xr.DataArray, time_dim: str) -> tuple[list[object], np.ndarray, str]:
    coord = _coord_for_dim(ds, da, time_dim)
    n = da.sizes[time_dim]
    if coord is None:
        leads = np.arange(n, dtype=float) * 5.0
        labels = [f"+{int(v)}m" for v in leads]
        return labels, leads, "fallback_5_min"

    vals = np.asarray(coord.values).reshape(-1)
    if vals.size != n:
        leads = np.arange(n, dtype=float) * 5.0
        labels = [f"+{int(v)}m" for v in leads]
        return labels, leads, "fallback_5_min"

    if np.issubdtype(vals.dtype, np.datetime64):
        leads = (vals.astype("datetime64[s]") - vals[0].astype("datetime64[s]")) / np.timedelta64(1, "m")
        return list(vals), np.asarray(leads, dtype=float), f"datetime:{coord.name or time_dim}"

    if np.issubdtype(vals.dtype, np.timedelta64):
        leads = vals / np.timedelta64(1, "m")
        leads = np.asarray(leads, dtype=float)
        labels = [f"+{v:g}m" for v in leads]
        return labels, leads, f"timedelta:{coord.name or time_dim}"

    try:
        numeric = vals.astype(float)
    except (TypeError, ValueError):
        leads = np.arange(n, dtype=float) * 5.0
        labels = [str(v) for v in vals]
        return labels, leads, "fallback_5_min"

    factor = _unit_factor_minutes(str(coord.attrs.get("units", "")))
    if factor is not None:
        numeric = numeric * factor
        low_name = str(coord.name or time_dim).lower()
        standard_name = str(coord.attrs.get("standard_name", "")).lower()
        is_lead = any(k in low_name or k in standard_name for k in ("lead", "forecast_period", "forecastperiod"))
        leads = numeric if is_lead and np.nanmin(numeric) >= 0 else numeric - numeric[0]
        labels = [f"+{v:g}m" for v in leads]
        return labels, np.asarray(leads, dtype=float), f"numeric:{coord.name or time_dim}"

    leads = np.arange(n, dtype=float) * 5.0
    labels = [str(v) for v in vals]
    return labels, leads, "fallback_5_min"


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

    times, leads, axis_mode = _time_axis(ds, da, time_dim)
    if leads.size != da.sizes[time_dim]:
        raise RuntimeError("Tijdas en forecastvariabele hebben verschillende lengtes.")
    if not np.all(np.isfinite(leads)):
        raise RuntimeError("Tijdas bevat ongeldige lead times.")

    valid_indices = [i for i, lead in enumerate(leads) if -1e-6 <= float(lead) <= horizon_minutes + 1e-6]
    if not valid_indices:
        raise RuntimeError(f"Geen forecastpunten binnen 0–{horizon_minutes} minuten gevonden.")

    rows = []
    for ti in valid_indices:
        slice_t = da.isel({time_dim: ti})
        probs: dict[str, float] = {}
        if threshold_dim and threshold_dim in slice_t.dims:
            vals = np.asarray(slice_t.values, dtype=float).reshape(-1)
            local_thresholds = thresholds
            if local_thresholds is None or len(local_thresholds) != len(vals):
                local_thresholds = list(range(len(vals)))
            for th, value in zip(local_thresholds, vals):
                probs[f">={th:g} mm/h"] = round(as_percent(float(value)), 1)
        else:
            value = float(np.asarray(slice_t.values).reshape(-1)[0])
            probs["precipitation"] = round(as_percent(value), 1)
        raw_time = times[ti]
        if isinstance(raw_time, str) and raw_time.startswith("+"):
            shown_time = raw_time
        else:
            shown_time = format_time(raw_time)
        rows.append(
            {
                "time": shown_time,
                "lead_minutes": round(float(leads[ti]), 3),
                "probabilities": probs,
                "time_axis_mode": axis_mode,
            }
        )
    return var_name, point, rows


def validate_forecast_rows(rows: list[dict], horizon_minutes: int) -> tuple[bool, list[str]]:
    problems: list[str] = []
    if not rows:
        return False, ["geen forecastregels"]
    leads = np.asarray([float(row.get("lead_minutes", float("nan"))) for row in rows], dtype=float)
    if not np.all(np.isfinite(leads)):
        problems.append("ongeldige lead times")
    if np.any(np.diff(leads) <= 0):
        problems.append("lead times zijn niet strikt oplopend")
    if abs(float(leads[0])) > 5.1:
        problems.append(f"eerste forecastpunt ligt pas op +{leads[0]:g} min")
    if float(leads[-1]) < horizon_minutes - 0.1:
        problems.append(f"forecast stopt op +{leads[-1]:g} min in plaats van +{horizon_minutes} min")
    if not any(row.get("probabilities") for row in rows):
        problems.append("geen neerslagkansen gevonden")
    return not problems, problems


def print_forecast(rows: list[dict]):
    print("\nWijSAmen 0–3 uur neerslagkans")
    print("-" * 92)
    if not rows:
        print("Geen forecastregels gevonden.")
        return
    keys = list(rows[0]["probabilities"].keys())
    show_keys = keys[:6]
    print("lead".ljust(8) + "tijd".ljust(18) + "  " + "  ".join(k.rjust(11) for k in show_keys))
    print("-" * 92)
    for row in rows:
        probs = row["probabilities"]
        values = [f"{probs.get(k, float('nan')):>9.1f}%" for k in show_keys]
        lead = f"+{row.get('lead_minutes', float('nan')):g}m".ljust(8)
        print(lead + row["time"][:16].ljust(18) + "  " + "  ".join(values))


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
        print(
            f"  {name}: dims={da.dims} shape={da.shape} units={da.attrs.get('units')} "
            f"standard_name={da.attrs.get('standard_name')} long_name={da.attrs.get('long_name')}"
        )


def _parse_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        normalized = value.replace("Z", "+00:00")
        dt = datetime.fromisoformat(normalized)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def _source_age_minutes(source: SourceFile) -> float | None:
    dt = _parse_utc(source.created or source.last_modified)
    if dt is None:
        return None
    return (datetime.now(timezone.utc) - dt).total_seconds() / 60.0


def main() -> int:
    p = argparse.ArgumentParser(description="KNMI seamless 0-3h nowcast for one location")
    p.add_argument("--lat", type=float)
    p.add_argument("--lon", type=float)
    p.add_argument("--gps", action="store_true", help="use termux-location; fail rather than silently using the default location")
    p.add_argument("--hours", type=float, default=3.0)
    p.add_argument("--keep", action="store_true", help="keep downloaded NetCDF file")
    p.add_argument("--diagnose", action="store_true", help="print dataset structure")
    p.add_argument("--no-log", action="store_true")
    p.add_argument(
        "--validate-live",
        action="store_true",
        help="run the first-milestone phone validation and print an explicit PASS/FAIL",
    )
    args = p.parse_args()

    if args.hours <= 0 or args.hours > 6:
        print("FOUT: --hours moet groter dan 0 en maximaal 6 zijn.", file=sys.stderr)
        return 2
    if (args.lat is None) ^ (args.lon is None):
        print("FOUT: geef --lat en --lon samen op.", file=sys.stderr)
        return 2
    if args.validate_live:
        args.hours = 3.0
        args.diagnose = True
        if args.no_log:
            print("FOUT: --validate-live vereist logging; laat --no-log weg.", file=sys.stderr)
            return 2
        if args.lat is None and args.lon is None:
            args.gps = True

    lat, lon = args.lat, args.lon
    location_source = "explicit"
    gps_provider = None
    if args.gps:
        gps = gps_from_termux()
        if gps:
            lat, lon = gps.latitude, gps.longitude
            location_source = "termux-gps"
            gps_provider = gps.provider
        elif lat is None or lon is None:
            print(
                "FOUT: --gps gevraagd maar termux-location leverde geen locatie. "
                "Controleer Termux:API en Android-locatiepermissie.",
                file=sys.stderr,
            )
            return 2
        else:
            print("WAARSCHUWING: GPS mislukte; expliciete --lat/--lon worden gebruikt.", file=sys.stderr)
            location_source = "explicit-after-gps-failure"
    if lat is None or lon is None:
        lat, lon = DEFAULT_LAT, DEFAULT_LON
        location_source = "default-amersfoort"
        print(f"Geen locatie opgegeven: tijdelijke fallback {lat:.4f}, {lon:.4f} (Amersfoort).")

    api_key = os.environ.get("KNMI_API_KEY", ANON_KEY).strip()
    client = KnmiClient(api_key)
    workdir = Path.cwd() / "data"
    workdir.mkdir(exist_ok=True)
    ds = None
    target = None

    try:
        source = client.latest_file()
        target = workdir / source.filename
        deprecation = source.deprecation
        if not target.exists():
            print(f"Download nieuwste KNMI-forecast: {source.filename}")
            _, download_deprecation = client.download(source, target)
            deprecation = download_deprecation or deprecation
        else:
            print(f"Gebruik al gedownload bestand: {source.filename}")

        age_minutes = _source_age_minutes(source)
        print(f"KNMI bronbestand: {source.filename}")
        if source.created:
            print(f"KNMI created: {source.created}")
        if age_minutes is not None:
            print(f"Bronouderdom bij ophalen: {age_minutes:.1f} min")
        if deprecation:
            print(f"WAARSCHUWING KNMI deprecatie: {deprecation}", file=sys.stderr)

        ds = xr.open_dataset(target, decode_times=True)
        if args.diagnose:
            diagnostic(ds)
        horizon_minutes = int(round(args.hours * 60))
        var_name, point, rows = extract_rows(ds, lat, lon, horizon_minutes)
        print(f"Locatie gevraagd: {lat:.5f}, {lon:.5f} ({location_source})")
        if gps_provider:
            print(f"Termux locatieprovider: {gps_provider}")
        if point.latitude is not None:
            print(f"Rasterpunt gebruikt: {point.latitude:.5f}, {point.longitude:.5f}")
        print(f"KNMI variabele: {var_name}")
        print_forecast(rows)

        valid, validation_problems = validate_forecast_rows(rows, horizon_minutes)
        payload = {
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "source": {
                "dataset": DATASET,
                "version": VERSION,
                "filename": source.filename,
                "created": source.created,
                "last_modified": source.last_modified,
                "size": source.size,
                "age_minutes_at_retrieval": round(age_minutes, 2) if age_minutes is not None else None,
                "deprecation": deprecation,
            },
            "location": {
                "requested": {"lat": lat, "lon": lon},
                "source": location_source,
                "gps_provider": gps_provider,
                "grid": {"lat": point.latitude, "lon": point.longitude, "indexers": point.indexers},
            },
            "variable": var_name,
            "horizon_minutes": horizon_minutes,
            "validation": {"structural_pass": valid, "problems": validation_problems},
            "forecast": rows,
        }
        log_path = Path("logs/forecast_history.jsonl")
        if not args.no_log:
            log_snapshot(log_path, payload)
            print(f"\nSnapshot gelogd in {log_path}")

        if args.validate_live:
            if not valid:
                print("\nLIVE VALIDATION: FAIL", file=sys.stderr)
                for problem in validation_problems:
                    print(f"  - {problem}", file=sys.stderr)
                return 3
            if location_source == "default-amersfoort":
                print("\nLIVE VALIDATION: FAIL — validatie mag niet op de stille defaultlocatie draaien.", file=sys.stderr)
                return 3
            print("\nLIVE VALIDATION: PASS")
            print(f"  actuele bron: {source.filename}")
            print(f"  forecastpunten: {len(rows)}")
            print(f"  bereik: +{rows[0]['lead_minutes']:g} t/m +{rows[-1]['lead_minutes']:g} min")
            print(f"  log: {log_path}")
        return 0
    except Exception as e:
        print(f"\nFOUT: {e}", file=sys.stderr)
        print("Tip: voer dezelfde opdracht uit met --diagnose voor de actuele NetCDF-structuur.", file=sys.stderr)
        return 2
    finally:
        if ds is not None:
            try:
                ds.close()
            except Exception:
                pass
        if target is not None and not args.keep:
            try:
                target.unlink(missing_ok=True)
            except Exception:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
