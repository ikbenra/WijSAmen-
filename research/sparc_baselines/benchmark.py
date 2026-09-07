#!/usr/bin/env python3
"""Reproducible SPARC baselines; intentionally contains no WijSAmen correction."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import least_squares, minimize_scalar

DATA_URL = "https://zenodo.org/records/16284118/files/MassModels_Lelli2016c.mrt?download=1"
DATA_MD5 = "fe6188538c3f5504f70f486ff6b4d29c"
DATA_SHA256 = "9108994b12cc401b94a1768beca61c53ec354779385c9c9cc571049f3043244c"
KPC_M = 3.085677581491367e19
G_KPC = 4.30091e-6  # kpc (km/s)^2 / Msun
UPS_DISK, UPS_BULGE = 0.5, 0.7


def download_checked(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        urllib.request.urlretrieve(DATA_URL, path)
    payload = path.read_bytes()
    md5 = hashlib.md5(payload).hexdigest()  # dataset-published checksum
    sha256 = hashlib.sha256(payload).hexdigest()  # stronger local provenance pin
    if md5 != DATA_MD5 or sha256 != DATA_SHA256:
        raise RuntimeError(
            "SPARC checksum mismatch: "
            f"md5={md5} (expected {DATA_MD5}); "
            f"sha256={sha256} (expected {DATA_SHA256})"
        )


def load_sparc(path: Path) -> pd.DataFrame:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) != 10:
            continue
        try:
            vals = [float(x) for x in parts[1:]]
        except ValueError:
            continue
        rows.append([parts[0], *vals])
    cols = ["galaxy", "distance_mpc", "radius_kpc", "v_obs", "v_err",
            "v_gas", "v_disk", "v_bulge", "sb_disk", "sb_bulge"]
    df = pd.DataFrame(rows, columns=cols)
    if df.empty or df.galaxy.nunique() != 175:
        raise RuntimeError(f"Expected 175 galaxies; parsed {df.galaxy.nunique()}")
    return df


def make_split(galaxies: list[str], n_train: int = 35) -> pd.DataFrame:
    ranked = sorted(galaxies, key=lambda x: hashlib.sha256(f"WijSAmen-SPARC-v0.1:{x}".encode()).hexdigest())
    train = set(ranked[:n_train])
    return pd.DataFrame({"galaxy": sorted(galaxies), "split": ["train" if g in train else "test" for g in sorted(galaxies)]})


def baryon_v2(df: pd.DataFrame) -> np.ndarray:
    gas2 = np.sign(df.v_gas.to_numpy()) * df.v_gas.to_numpy() ** 2
    return np.maximum(0.0, gas2 + UPS_DISK * df.v_disk.to_numpy() ** 2 + UPS_BULGE * df.v_bulge.to_numpy() ** 2)


def rar_velocity(df: pd.DataFrame, a0: float) -> np.ndarray:
    r_m = df.radius_kpc.to_numpy() * KPC_M
    gbar = baryon_v2(df) * 1e6 / r_m
    x = np.sqrt(np.maximum(gbar, 1e-300) / a0)
    gobs = gbar / (-np.expm1(-x))
    return np.sqrt(np.maximum(0.0, gobs * r_m / 1e6))


def nfw_v2(r: np.ndarray, log_rho: float, log_rs: float) -> np.ndarray:
    rho, rs = 10 ** log_rho, 10 ** log_rs
    x = np.maximum(r / rs, 1e-12)
    mass = 4 * np.pi * rho * rs**3 * (np.log1p(x) - x / (1 + x))
    return G_KPC * mass / r


def burkert_v2(r: np.ndarray, log_rho: float, log_rs: float) -> np.ndarray:
    rho, rs = 10 ** log_rho, 10 ** log_rs
    x = np.maximum(r / rs, 1e-12)
    mass = np.pi * rho * rs**3 * (np.log((1 + x) ** 2 * (1 + x**2)) - 2 * np.arctan(x))
    return G_KPC * mass / r


def fit_halo(df: pd.DataFrame, profile: str) -> tuple[np.ndarray, np.ndarray]:
    r, vb2 = df.radius_kpc.to_numpy(), baryon_v2(df)
    fn = nfw_v2 if profile == "nfw" else burkert_v2
    def residual(p):
        pred = np.sqrt(np.maximum(0.0, vb2 + fn(r, *p)))
        return (pred - df.v_obs.to_numpy()) / np.maximum(df.v_err.to_numpy(), 1e-6)
    fit = least_squares(residual, x0=[7.0, 1.0], bounds=([3.0, -1.5], [12.0, 3.0]))
    return np.sqrt(np.maximum(0.0, vb2 + fn(r, *fit.x))), fit.x


def metrics(obs: np.ndarray, pred: np.ndarray, err: np.ndarray) -> dict[str, float]:
    resid = pred - obs
    return {"rmse_kms": float(np.sqrt(np.mean(resid**2))),
            "mae_kms": float(np.mean(np.abs(resid))),
            "chi2": float(np.sum((resid / np.maximum(err, 1e-6)) ** 2)),
            "n_points": int(len(obs))}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, default=Path(__file__).parent / "data/MassModels_Lelli2016c.mrt")
    ap.add_argument("--split", type=Path, default=Path(__file__).parent / "split.csv")
    ap.add_argument("--out", type=Path, default=Path(__file__).parent / "results")
    ap.add_argument("--verify-split", action="store_true")
    args = ap.parse_args()
    download_checked(args.data)
    df = load_sparc(args.data)
    expected = make_split(df.galaxy.unique().tolist())
    committed = pd.read_csv(args.split)
    if not expected.equals(committed):
        raise RuntimeError("Committed split.csv differs from deterministic v0.1 split")
    if args.verify_split:
        print("split.csv OK: 35 train / 140 test")
        return
    df = df.merge(committed, on="galaxy", validate="many_to_one")
    train = df[df.split == "train"]
    objective = lambda loga: np.sum(((rar_velocity(train, 10**loga) - train.v_obs) / train.v_err) ** 2)
    a0 = 10 ** minimize_scalar(objective, bounds=(-12, -8), method="bounded").x

    predictions, galaxy_rows = [], []
    for galaxy, g in df.groupby("galaxy", sort=True):
        preds = {"newton": np.sqrt(baryon_v2(g)), "rar": rar_velocity(g, a0)}
        halo_params = {}
        for profile in ("nfw", "burkert"):
            preds[profile], halo_params[profile] = fit_halo(g, profile)
        for model, pred in preds.items():
            m = metrics(g.v_obs.to_numpy(), pred, g.v_err.to_numpy())
            galaxy_rows.append({"galaxy": galaxy, "split": g.split.iloc[0], "model": model,
                                "evaluation": "blind" if model in ("newton", "rar") else "per_galaxy_fit_oracle",
                                **m})
            for (_, row), value in zip(g.iterrows(), pred):
                predictions.append({"galaxy": galaxy, "split": row["split"], "radius_kpc": row.radius_kpc,
                                    "v_obs": row.v_obs, "v_err": row.v_err, "model": model,
                                    "v_pred": value, "residual": value - row.v_obs})
        galaxy_rows[-2].update({"log10_rho0": halo_params["nfw"][0], "log10_rs_kpc": halo_params["nfw"][1]})
        galaxy_rows[-1].update({"log10_rho0": halo_params["burkert"][0], "log10_rs_kpc": halo_params["burkert"][1]})

    args.out.mkdir(parents=True, exist_ok=True)
    points, galaxies = pd.DataFrame(predictions), pd.DataFrame(galaxy_rows)
    points.to_csv(args.out / "point_predictions.csv", index=False)
    galaxies.to_csv(args.out / "galaxy_metrics.csv", index=False)
    summary = galaxies.groupby(["split", "model", "evaluation"], as_index=False).agg(
        galaxies=("galaxy", "count"), median_rmse_kms=("rmse_kms", "median"), median_mae_kms=("mae_kms", "median"), total_chi2=("chi2", "sum"))
    summary.to_csv(args.out / "summary.csv", index=False)
    (args.out / "run.json").write_text(json.dumps({"data_url": DATA_URL, "data_md5": DATA_MD5,
        "data_sha256": DATA_SHA256, "disk_ml": UPS_DISK, "bulge_ml": UPS_BULGE, "rar_a0_m_s2_fitted_train_only": a0,
        "warning": "NFW/Burkert use two parameters fitted to each galaxy and are not blind test predictions."}, indent=2) + "\n")

    test = galaxies[galaxies.split == "test"]
    order = ["newton", "rar", "nfw", "burkert"]
    vals = [test.loc[test.model == m, "rmse_kms"].median() for m in order]
    fig, ax = plt.subplots(figsize=(7, 4)); ax.bar(order, vals)
    ax.set_ylabel("Median per-galaxy RMSE [km/s]"); ax.set_title("SPARC v0.1 test galaxies")
    ax.text(.99, .98, "NFW/Burkert are fitted oracles", transform=ax.transAxes, ha="right", va="top", fontsize=8)
    fig.tight_layout(); fig.savefig(args.out / "baseline_rmse.png", dpi=160); plt.close(fig)
    print(summary.to_string(index=False)); print(f"\nFrozen train-only RAR a0 = {a0:.6g} m/s^2")


if __name__ == "__main__":
    main()

