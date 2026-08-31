# Magnet–fiber geometry integration

Status: `INCUBATE/P2 — STAGE-1A DESK SCREEN COMPLETE`

Canonical portfolio analysis and corpus provenance remain in the Portfolio Hunter Google Doc. This folder preserves a reviewable, non-sensitive geometry model.

## Recovered source layers

### Original user source — Armillarium conversation

Recovered from exact raw bytes in `chunk_0140.jsonl`:

- conversation `689ba9b0-5e74-8323-8fa7-c1030fef6345`, title `Armillarium uitleg`;
- user message `bbb21f49-3fd5-4fd0-a063-e4f102671c6d`: controlled rotations, changing mutual angles and a proposed 3/6/9 relation;
- user message `bbb21ad0-4dcb-4211-abc8-198d69d83a75`: rings of permanent magnets, optional crystals, exact control of relative angles and speeds;
- user message `bbb21742-d8c8-4cd6-aee7-3b5d2c80cb34`: a proposed “Möbius-strip-like” magnetic field profile without a literal metal Möbius strip.

These are source ideas, not experimental results.

### Later assistant additions

Halbach arrays, particular materials, stationary-wave language and a specific half-twist coil construction were introduced later by the assistant. They remain `LATER_ASSISTANT_PROPOSAL / UNVERIFIED_DESIGN` and are not attributed to Remco.

### Magnet–fiber line

The separately recovered `chunk_0246` source and later magnet–fiber reconstruction remain distinct. The present integration uses the armillary only as a parameterized family of field-source geometries.

## Stage-1A model

`armillary_geometry_screen.py` compares:

1. a coaxial opposed two-coil baseline;
2. three orthogonal, independently phased armillary coils.

The quasi-static Biot–Savart screen normalizes every phase to `sum(I²)=1`. It evaluates field shape on a closed path and the observability of independent coil states with four local 3-axis sensors.

Run:

```bash
python3 projects/magnet-fiber-geometry/armillary_geometry_screen.py
```

## Reproduced result

| Metric | Coaxial pair | Three-ring armillary |
|---|---:|---:|
| Normalized sensor condition number | 1.205 | 1.140 |
| Mean path RMS field | 2.237 µT | 2.304 µT |
| Worst-phase minimum path field | 2.237 µT | 0.591 µT |
| Mean path direction variation | 0.635 rad | 10.269 rad |
| Signed tangential scalar average | effectively zero | effectively zero |

Interpretation:

- The armillary basis creates much richer path-dependent field-direction variation and remains observable with multiple local vector sensors.
- It also creates deeper low-field regions. Any “Möbius-like” metric must therefore disclose path choice, zero crossings and coordinate/sign conventions.
- A single signed or averaging optical loop can still cancel almost completely. Fiber is justified only if distributed/multi-axis optical interrogation adds spatial information, electromagnetic-noise immunity or timing that ordinary local Hall probes cannot deliver.
- The model does **not** show net lift. Geometry may shape gradients, torques, harmonics and coupling to an external reaction path, but a closed apparatus still requires a conservation-complete whole-system force/impulse model.

## Next falsification gate

Compare armillary, conventional multipole/Halbach and coaxial geometries under matched copper, stored energy, bandwidth and thermal limits. Vary ordinary segment counts before any 3/6/9 claim. Exclude crystals in the first pass; later include them only as matched-control transducers.

Stop or demote the special-geometry line if:

- its advantage disappears under equal-resource controls;
- the Möbius-like score depends mainly on arbitrary path choice or near-zero singularities;
- distributed optical sensing adds no information beyond local Hall sensors;
- no external reaction path exists for a force claim;
- 3/6/9 or crystal variants do not outperform matched controls.

## Safety boundary

Simulation and low-energy coil emulation come first. No strong rotating permanent magnets, high stored energy, purchase, hardware build or levitation claim is authorized by this artifact.
