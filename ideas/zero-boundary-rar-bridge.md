# Zero-boundary / RAR bridge candidate

## Why this note exists
The user hoped the 0veld / enriched-zero structure might predict the same recurring gravitational discrepancy currently modeled with dark matter in galaxy rotation curves. This note records the strongest mathematical coincidence found so far without treating it as evidence.

## Empirical target: SPARC radial acceleration relation
A widely used empirical fit to the SPARC radial acceleration relation is

g_obs = g_bar / (1 - exp(-sqrt(g_bar/a0)))

with a0 of order 1.2e-10 m/s^2.

This relation has two important asymptotic regimes:
- high acceleration: g_bar >> a0 -> g_obs ~ g_bar;
- low acceleration: g_bar << a0 -> g_obs ~ sqrt(a0 g_bar).

## Reparameterization
Define

x = sqrt(g_bar/a0).

Then

g_bar = a0 x^2

and

g_obs = a0 x^2 / (1 - exp(-x)).

Now define a near-boundary variable

q = exp(-x).

The discrepancy factor is

D(x) = g_obs/g_bar = 1/(1-q) = 1 + q + q^2 + ...

for |q|<1.

This gives a mathematically interesting coupled limit:

x -> 0,
q -> 1,
g_bar = a0 x^2 -> 0,
D(x) -> infinity,

while

g_obs = g_bar D(x)

remains finite in scaling and behaves as

g_obs ~ a0 x = sqrt(a0 g_bar).

More explicitly, using

1/(1-exp(-x)) = 1/x + 1/2 + x/12 + O(x^3),

we obtain

g_obs = sqrt(a0 g_bar) + g_bar/2 + g_bar^(3/2)/(12 sqrt(a0)) + ...

So the empirical RAR contains exactly the kind of structure the 0veld discussion has emphasized: one factor tends to zero, another diverges, and a finite physically relevant scaling survives because both are controlled by the same limit parameter.

## Why this is NOT yet a prediction
If we simply choose

x = sqrt(g_bar/a0)

because it reproduces the empirical RAR, we have only rewritten an existing fit. That is not new physics.

For a real WijSAmen prediction, the zero-boundary / phase / geometry framework must independently derive at least:

1. Why the dimensionless boundary coordinate should satisfy
   x^2 = g_bar/a0.
2. Why the response factor should be
   1/(1-exp(-x))
   or a uniquely related function.
3. Why a0 is universal and what fundamental quantity sets its value.
4. How the same law predicts gravitational lensing and does not only fit circular rotation.
5. How the law extends consistently to clusters, structure formation and cosmology.

## Most important theoretical task
Try to derive a dimensionless boundary coordinate L from a physical action, phase, geometric invariant or spacetime quantity such that

L^2 = g_bar/a0

emerges rather than being inserted.

Then derive the observable response from the enriched-zero structure.

A candidate theory becomes scientifically interesting only if it fixes the functional form and a0 before a blind SPARC test.

## Connection to the enriched zero idea
The resemblance is structural:
- enriched-zero work uses exponential coordinates exp(-L), directional/phase information and coupled zero/infinity limits;
- the SPARC fit uses exp(-sqrt(g_bar/a0)) and has a low-acceleration zero-times-divergence limit with finite square-root scaling.

This is a reason to investigate a derivation, not evidence that the two describe the same physics.

## Falsification gate
The bridge fails as a fundamental explanation if no independent derivation produces the SPARC-like response, or if a derived law cannot simultaneously pass blind rotation-curve tests and lensing/cluster/cosmological constraints.

## Evidence anchors
- McGaugh, Lelli & Schombert (2016), The Radial Acceleration Relation in Rotationally Supported Galaxies, arXiv:1609.05917.
- Empirical form: g_obs = g_bar/[1-exp(-sqrt(g_bar/a0))], with a0 ~ 1.2e-10 m/s^2.

## Decision log
- 2026-08-31 — Recorded a nontrivial mathematical resemblance between the enriched-zero coupled-limit structure and the empirical SPARC RAR. Classified strictly as a derivation target, not a discovery or prediction.
