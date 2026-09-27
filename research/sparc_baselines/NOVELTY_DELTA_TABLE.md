# 0Veld novelty-delta gate

Status: **required before a new model name, SPARC test-set evaluation, secrecy decision, or external claim**

This table asks a narrow question: *what prediction is genuinely new compared with an explicit baseline?* Interpretation, imagery, or a new name is not a numerical delta.

## Current verified disposition

| Candidate branch | Baseline | New axiom or mechanism | Derived equation | Dataset | Universal fitted parameters | Numerically differing prediction | Predeclared disconfirmation | Status |
|---|---|---|---|---|---:|---|---|---|
| Local enriched-zero / orientation response | Frozen RAR | Orientation/focusing interpretation proposed; no independently derived local law recorded | `g_bar / (1-exp(-sqrt(g_bar/a0)))` | SPARC | 1 (`a0`) | None: algebraically identical to RAR | Any claimed independent SPARC result is duplicate evidence | `ALIAS_OF_RAR` |
| `a0(z)` / `H(z)` evolution | Present-day RAR | Redshift-dependent acceleration scale proposed | Not yet frozen | Redshift-capable dataset required | Not yet fixed | Not testable with present-day SPARC alone | No stable out-of-sample improvement or conflict with external constraints | `REQUIRES_DIFFERENT_DATASET` |
| Environmental / external-field branch | RAR plus declared external-field comparator | Mechanism not yet derived | Not yet specified | Dataset with environment/external-field observables required | Not yet fixed | None demonstrated | No distinct preregistered environmental signature | `NOT_YET_DERIVED` |
| New local response | Newton and frozen RAR | Not yet specified | Not yet specified | Committed SPARC training split first | Maximum 2 | Must differ beyond frozen numerical tolerance on training data | No material gain after complexity cost, subset-only gain, or systematic regime failure | `NOT_YET_SPECIFIED` |

## Admission record for any new generation

Complete every field and commit it **before** opening the corresponding holdout result.

| Field | Required content |
|---|---|
| Candidate identity | Stable ID, generation, date, author/source provenance and code commit |
| Baseline | Exact comparator equation, implementation commit and frozen parameters |
| New axiom | One explicit statement absent from the baseline; label interpretation separately |
| Derivation | Equation-by-equation path, units and established-regime recovery |
| Dataset | Training/holdout split, inclusion rules, checksums and observational domain |
| Complexity | Number of universal fitted parameters and every calibration choice |
| Delta | Maximum absolute/relative training difference plus the regime where signs differ |
| Unique prediction | Observable that the baseline does not already predict |
| Failure rule | Quantitative result that counts against this generation |
| External constraints | Lensing, Solar System/Cassini, wide binaries, redshift evolution and environment where applicable |
| Reveal state | `NOT_RUN`, `PRECOMMITTED_ONE_SHOT_EVALUATION`, or `POST_REVEAL_REVISION` |

## Stop rules

- `ALIAS_OF_BASELINE`: predictions are equal within the frozen tolerance. Reuse the baseline result; do not rename it as independent evidence.
- `INTERPRETATION_ONLY`: a physical story changed but no derived observable changed. Preserve it as a hypothesis, not as a tested model.
- `UNDERDEFINED`: units, dynamics, parameters, dataset, or failure rule are missing. Do not run the holdout.
- `DATASET_MISMATCH`: the claimed delta depends on redshift, environment, lensing, or another variable absent from the dataset. Select a capable dataset first.
- `ADMISSIBLE_FOR_TRAINING_ONLY_CHECK`: a complete, dimensionally explicit candidate differs on committed training data and uses no more than two universal fitted parameters.
- `FROZEN_FOR_ONE_SHOT_EVALUATION`: implementation, tolerances, expected signature and failure rule are commit-bound; only then may the procedural holdout run once.

## Evidence boundary

This gate does not validate 0Veld, MOND/RAR, dark matter, modified gravity, or any mechanism. It prevents duplicate evidence and converts a broad idea into a falsifiable comparison. The existing SPARC aggregate results are already known, so future evaluation can be precommitted and one-shot, but not absolutely blind.

Provenance: Map2 chunks `0379` (SHA-256 `87379c5531296d4d3dfe3d38eb30de43cd23ea0652e9fa313b8a5ede6e2f0e90`) and `0380` (SHA-256 `eca1c8d5a8b7b4df3a2e62b02425652f1837c96939a8f31eb6fc1c43e294b1ac`), combined with the existing SPARC candidate-admission gate and verified RAR-equivalence result.
