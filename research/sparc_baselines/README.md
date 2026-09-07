# SPARC baseline benchmark v0.1

Smallest reproducible implementation of issue #3. It downloads the pinned SPARC mass-model table, verifies the published MD5 checksum, checks the committed 35/140 galaxy split, fits the single universal RAR acceleration scale on training galaxies only, and writes test predictions and residuals.

No WijSAmen correction is implemented here.

## Run

```bash
cd research/sparc_baselines
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python benchmark.py
```

Outputs in `results/`: `summary.csv`, `galaxy_metrics.csv`, `point_predictions.csv`, `run.json`, and `baseline_rmse.png`.

## Baselines and fairness

- **Newton:** fixed stellar mass-to-light ratios 0.5 (disk), 0.7 (bulge); genuinely blind.
- **RAR:** `g_obs = g_bar / (1-exp(-sqrt(g_bar/a0)))`; one universal `a0`, fitted using only the 35 training galaxies and then frozen; genuinely blind on test.
- **NFW and Burkert:** two halo parameters fitted separately to every galaxy. These are useful conventional fit-quality ceilings but are explicitly reported as `per_galaxy_fit_oracle`, not blind predictions. A later benchmark may add cosmological priors or a training-derived halo-population model for a predictive dark-halo comparison.

The deterministic split ranks galaxy identifiers by SHA-256 of `WijSAmen-SPARC-v0.1:<ID>` and assigns exactly 35 galaxies to training. `split.csv` is committed so model development cannot silently reshuffle it.

Dataset: Lelli, McGaugh & Schombert, SPARC mass models, DOI `10.5281/zenodo.16284118`.
