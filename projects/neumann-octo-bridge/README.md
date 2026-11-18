# Neumann–Octo Bridge v0: additive experiment

Status: **isolated prototype / not integrated**. This folder is new; existing Neumann and OctoCorpus files remain untouched.

## Purpose
Explore a deterministic mission contract connecting exact rational representations with a future modular agent orchestrator. This does **not** claim the Neumann mission-core API has been located or validated. OctoCorpus currently contains an evolutionary provenance research scaffold, not a verified runtime agent interface.

## Reproduce
From this folder with Python 3.10+ (standard library only):

```sh
python -m unittest -v test_bridge.py
python bridge.py
```

The test mission computes 11/46 in bases 2, 10 and 16, independently decodes each prefix/repeating-cycle expansion to an exact Fraction, checks equality and hashes canonical JSON. Hashes are reproducibility markers, **not** signatures or security guarantees.

## Evidence and boundaries
- SOURCE_SUPPORTED_RESULT: `projects/octocorpus/README.md` documents evidence labels and a desk-only research scaffold.
- INFERENCE: a pure deterministic representation adapter may help later mission orchestration.
- HYPOTHESIS: a future adapter can connect this experiment to the real Neumann mission-core without changing either system.
- UNKNOWN: canonical Neumann module location, function signatures, carry/phase semantics, compatibility with mission-core, agent execution interface and real self-improvement benefit.

## Safety
No network, credentials, file writes, dynamic code execution, autonomous tool calls, deployment, merges or self-modification. No claims about electromagnetic, physical or biological effects. No automatic promotion of variants. Append-only future event logs and review gates are proposed but not implemented.

## Next evidence gate
Locate the canonical Neumann core and its tests; compare `represent/exact_value` with `expansion/fraction_from_digits` for 11/46 in all three bases, preserving field meanings and logging discrepancies. Only after that design an actual Octo agent interface and append-only mission log.
