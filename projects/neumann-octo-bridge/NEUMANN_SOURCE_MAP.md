# Neumann source discovery (2026-11-18)

Read-only inspection identified an existing candidate implementation on branch `feature/neumann-bin-dec-hex-v02` at `projects/neumann-bin-dec-hex/core.py` with `represent(value, base, max_digits=10000)`, `Representation.exact_value()`, and fields `sign`, `integer`, `prefix`, `cycle`. This branch is not the bridge's base branch; **do not silently import or merge it**.

A separate historical Neumann branch `chatty/neumann-mission-core-v0-1` contains `projects/neumann-mission-core/README.md`, which describes exact rational expansion, remainder states and carry primitives as experimental research. The actual canonical `expansion`/`fraction_from_digits` source location has not yet been verified in this inspection. Existing earlier PR #14 comparison evidence should be reviewed before making compatibility claims.

## Required parity gate

1. Locate and read the canonical mission-core implementation and test files at the exact branch/commit used for PR #14.
2. Run 11/46 for bases 2, 10 and 16 with both original APIs, preserving `cycle` vs `repetend` and sign semantics.
3. Compare each to the bridge's independent `Fraction` reconstruction.
4. Record command, branch SHAs, exact outputs and failures in a **new** append-only evidence file.
5. Keep all integrations disabled until a review explicitly approves them.

No source files outside this new bridge directory were changed.
