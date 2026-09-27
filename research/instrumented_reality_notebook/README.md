# Instrumented Reality Notebook v0.1

This is an **observation and review instrument**, not permission to activate equipment. It converts an unusual physical report into a reproducible record while keeping observation, interpretation and mechanism separate.

Use it for field, optical, magnetic, acoustic, thermal or mechanical ideas only when the work remains safe, reversible and within the recorder's authority. Unknown apparatus, unknown energy, human/animal exposure, reactive substances, pressure, radiation, mains/high voltage, fire, traffic or public-space risk remain blocked pending competent review.

## What it records

- exact source and provenance status;
- literal observation versus interpretation;
- apparatus identity and configuration confidence;
- complete energy inventory and de-energized state;
- environment and possible ordinary confounders;
- independent observation status;
- comparator or sham plan;
- one predeclared prediction and one alternative explanation;
- stop conditions, authority and readback plan;
- immutable SHA-256 receipt over the record.

The validator never returns physical authorization. Its strongest result is `COMPLETE_FOR_REVIEW / NOT_AUTHORIZED_BY_THIS_TOOL`.

## Run

```bash
python3 validate_record.py record.example.json --receipt receipt.json
python3 -m unittest -v test_validate_record.py
```

## Evidence ladder

1. `SOURCE_PENDING` — a report exists, but the original text, media or hardware identity is absent.
2. `OBSERVATION_ONLY` — literal observation and provenance are recorded; no mechanism claim.
3. `CONTROL_PLAN_FROZEN` — prediction, alternative account, comparator/sham, stop rules and measurement method are committed.
4. `COMPLETE_FOR_REVIEW` — documentation is internally complete enough for a competent reviewer; still no execution permission.
5. `OBSERVED_WITH_CONTROLS` — reserved for a later record containing actual measurements and raw artifacts.
6. `INDEPENDENTLY_REPRODUCED` — reserved for a separate competent reproduction with its own provenance.

No later state may be inferred by enthusiasm, repetition, symbolic fit or assistant confidence.

## Safe workflow

1. Start from a de-energized or simulation-only state.
2. Preserve the original observation exactly; label reconstruction separately.
3. Identify every power, stored-energy, chemical, optical, thermal and mechanical source.
4. Record an ordinary alternative explanation before a preferred mechanism.
5. Freeze a measurable prediction, comparator/sham and disconfirming outcome.
6. Run the validator and preserve its receipt.
7. If any physical action is proposed, obtain separate human authority and competent safety review; this notebook cannot grant either.
8. Preserve failures, null results and raw readback.

## Current portfolio use

The format can support 0Veld/field hypotheses, magnet/optical concepts, lattice observations and other unusual mechanisms without blending a striking event with a causal conclusion. It is deliberately not coupled to any one theory.

Provenance: Map2 chunk `0382`, SHA-256 `6ae2333e0dc5fb464b87fbbf03e4e6a5a325538702ae6b9ba9a5fa1ecf7d0090`. The source's reported circular apparatus is **not approved for reactivation**.
