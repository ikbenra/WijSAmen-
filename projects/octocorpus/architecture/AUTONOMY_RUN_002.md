# OctoCorpus run 002 — post-selection audit

Date: 2026-11-13. Parent: f51dd09c2394e1763b2d04acf88bf8d4948c8027.
The current direction remains C (2 arms), Si (2), SiC+N (2 or 4), shared nodule
and reversible overlays. Workboard/PR summary lag behind the actual code.
Steward's 2026-11-13 handoff assigns implementation to this branch owner.

## Verified prior cloud evidence
Runs 43289216109 (autonomy) and 43289216205 (triad) completed successfully.
Autonomy logs show 6 tests, generation 2, no further accepted improvement.
Artifact 13976532014 was downloaded. ZIP SHA256 matched the provider digest:
39e3b8837f56bb9bf05c633c385cdb7f6478bee49ff05b0c98813f9f3a343951.
The checkpoint contains C=[0,2,0], Si=[2,0,0], SiC_N=[1,2,1]. Its state hash
passes the new integrity check. Private continuity context was read only.

## Question fixed before the first new evaluation
Does the frozen learned policy beat its initial policy on new sensor amplitudes
preserving the same eight latent labels? Pilot criterion: positive paired mean
delta and positive lower descriptive 95% bound. The audit never selects weights.

## Executed locally
20 tests passed (6 optimizer, 8 audit/checkpoint, 6 scripted triad). Resuming
the downloaded state preserved generation 2 and accepted no new changes.
The audit used 20 cohorts of 256 cases, 32 jittered examples per binary pattern.
Jitter is uniform in [-0.2,0.2]; the latent labels use an independent truth table.
The generator was designed with access to existing policies and task semantics.
It is a new post-selection robustness audit, not an external blind benchmark.

| Group | Fixed accuracy | Frozen accuracy | Delta | Approx. 95% interval |
|---|---:|---:|---:|---:|
| C | 62.52% | 62.52% | 0 pp | [0,0] pp |
| Si | 50.21% | 50.21% | 0 pp | [0,0] pp |
| SiC_N | 50.08% | 87.87% | +37.79 pp | [+36.67,+38.91] pp |

No cohort regressed. Constant-one accuracy is 62.5%. Shuffled-label SiC_N
accuracy averaged 50.14%. Only the previously changed SiC_N policy improves.
N is an architectural label here, not a causally tested module. Seeds vary
amplitude noise, not task semantics or training. Energy remains unknown.
No score-dependent tuning was performed after inspecting these results.

## Resume gate
Keep this suite as a regression suite. Implement one versioned temporary overlay
and check actual action outputs before, during and after rollback. Reserve fresh
context-shift evaluation before testing head/N removal and permanent updates.
The legacy two-point gate remains training validation. Preserve both biological
passports. Cloud execution of this commit requires actual run and artifact
readback; local test results alone do not establish it.

## Verified cloud follow-up
Code commit f31b271708a30e8a14f8fa1c531a4066ff104c49 triggered actual PR workflows.
Run 43446884634 completed successfully (14 optimizer/audit tests and evaluation).
Run 43446884585 completed successfully (scripted triad CI, 6 tests).
Artifact 14048137413 contains state and evaluation. Downloaded ZIP digest:
ba624508302d323deea8b1c974078487f11b120e260d28d6ed4ea11270ff730a.
The downloaded evaluation exactly equals the local JSON, including all 20 rows.
The state remains generation 2, with unchanged state hash.
Main readback remains fa51cc566369e177e26368788829bbd9832c87dd.
Steward handoff: this verified checkpoint is the implementation owner's resume
source; the older workboard card and PR initial description must not reset work.
