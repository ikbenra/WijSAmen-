# Geometry-to-Evidence Harness v0.1

This small, dependency-free preprocessor creates a reproducible **equal-proxy-mass geometry receipt** for one proposed lattice and one comparator. It is intended to keep geometry claims honest before FEA, fabrication, optical integration, or vehicle-scale discussion.

## Evidence boundary

The harness does **not** calculate stiffness, strength, buckling, fatigue, impact resistance, printability, optical effect, buoyancy, safety, or commercial value. Its cylinder-sum volume model ignores node overlap. Orientation and connectivity are descriptors, not performance claims.

The purpose is narrower:

- require explicit node and member coordinates instead of a name-only geometry;
- normalize both geometries to the same target proxy mass;
- record material density, cell dimensions, topology and manufacturing threshold;
- compute transparent geometry descriptors;
- hash inputs and the resulting receipt;
- freeze load-case labels without pretending they were simulated;
- expose mismatched materials, cell dimensions, disconnected members and sub-resolution diameters before costly work.

## Input shape

Each input is JSON:

```json
{
  "name": "candidate-or-comparator",
  "material": {"name": "reference polymer", "density_g_cm3": 1.2},
  "cell": {"dimensions_mm": [10, 10, 10]},
  "nodes": [[0, 0, 0], [10, 0, 0]],
  "edges": [[0, 1]],
  "manufacturing": {"minimum_feature_mm": 0.2},
  "load_cases": [{"id": "compression_z", "status": "FROZEN_NOT_RUN"}]
}
```

Coordinates and cell dimensions use millimetres. Density uses grams per cubic centimetre. Edges contain zero-based node indices.

## Run

```bash
python3 harness.py candidate.json comparator.json \
  --target-mass-g 0.6 \
  --out receipt.json
```

Run the tests:

```bash
python3 -m unittest -v test_harness.py
```

## Honest comparison sequence

1. Recover or define exact coordinates for the proposed cell.
2. Choose at least one conventional comparator for the same boundary volume.
3. Use identical material and target proxy mass unless the receipt explicitly flags otherwise.
4. Freeze load directions, supports, tolerances, mesh/convergence rules and failure metrics.
5. Generate and commit the preprocessor receipt.
6. Connect a separately validated FEA route; preserve solver version, mesh and convergence evidence.
7. Fabricate equal-material/equal-mass coupons only after digital sanity checks.
8. Compare measured results with the frozen predictions and keep failures.

## Current portfolio use

- **Opal Memorial:** determine whether any micro-lattice backing can justify further optical integration work without confusing geometry novelty with visual effect.
- **AquaLattice:** compare a recovered candidate cell with conventional cells under identical normalization before serviceability claims.
- **Amphibious vehicle concepts:** only after geometry and coupon evidence; this tool does not address buoyancy, road legality or vehicle safety.

No Fivefold Triad, quasicrystal, honeycomb, or other named geometry is treated as superior by default. A candidate is admitted only once its coordinates, comparator, boundary conditions and falsification criteria are explicit.
