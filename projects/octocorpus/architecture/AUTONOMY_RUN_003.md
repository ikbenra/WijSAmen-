# Run 003 — temporary context overlay and behavioral rollback

Date 2026-11-20. Parent commit 5d31dfc18c4dce0de71a18ba662c6f2645e48c85.
This additive step follows OVERLAY_PROTOCOL_V01.md. All older files remain intact.
The current workboard, private canonical portfolio, direction V02, lab and
prior runs were read. Steward's latest owner handoff reserves this branch for
OctoCorpus. The separate Neumann bridge PR17 remains with its existing owner.

## Verified input
Prior Actions runs 43447130594 and 43447130706 completed/success. Artifact
14048326890 was downloaded; its archive SHA256 was independently checked:
78d18d0142f305a5dbe5634ebefe71b47f5044241dfbb22086a64f475e01cb89.
OVERLAY_INPUT_V01.json preserves its synthetic checkpoint, generation 2,
state hash ccede089c5c48c9f020001c1786564f5fcfdfdb6204a68fda1f5e6132269d188.

## Implemented and executed locally
Versioned immutable rules, context-scoped overlays, parent validation, retained
history and retirement tombstones. Retired versions cannot be replayed through
the same registry. A finite learner fits only calibration data. Three variants
use the same held-out inputs: frozen, context overlay and permanent update.
There is also a shuffled-calibration negative control. A dedicated new workflow
runs all tests and exports the evaluation; actual cloud execution needs readback.

28 tests passed, including eight lifecycle/split tests. Twenty seeds each used
64 calibration and 128 final observations. Each test split has fresh continuous
inputs; eight known latent patterns underlie all seeds. The checkpoint base
weights are preserved. There was no score-driven tuning after the pilot run.

| Group | Fixed B | Overlay B | Overlay return A | Permanent return A |
|---|---:|---:|---:|---:|
| C | 36.76% | 87.58% | 63.24% | 12.42% |
| Si | 49.02% | 87.58% | 50.98% | 12.42% |
| SiC_N | 12.73% | 87.58% | 87.27% | 12.42% |

All 60 seed/group checks restored the exact original outputs, both in A and
when re-querying retired context B. Normal A behavior also stayed isolated
while B was active. All per-seed B gains were positive. Shuffled-calibration
accuracy in B averaged 57.66%. Learned overlay and permanent policies have
identical B accuracy, isolating context scoping as the return-stage difference.
Local full report SHA256:
a8fb36568d4bf291a49efe43aea2457bee3a1eb9ef537446ecf8e233c28c425d.

## Boundaries and falsifiers
The reversal is engineered and context labels are explicit. This supports a
local software lifecycle contract. It does not establish real-world transfer,
context inference, head-mediated transfer, N synergy, material consciousness or
RNA biophysics. No energy was measured. Learning searches 875 candidates per fit,
so fixed inference and adaptation do not consume equal compute. Once observed,
this suite is regression data. Future choices need a fresh reserved evaluation.

The registry retains retired rule content. It blocks reactivation by version,
not semantically equivalent rules installed under another context or agent.
This gap is intentionally visible rather than described as global revocation.

## Owner resume gate
Model exactly one transfer from one arm to the shared nodule and a second arm.
Preserve the originating version through that transfer. In a fresh predeclared
test compare local retirement with propagated retirement while keeping healthy
base behavior available. A revoked derived effect reachable at the second arm
falsifies system-wide rollback. Leave other owners' implementations separate.
