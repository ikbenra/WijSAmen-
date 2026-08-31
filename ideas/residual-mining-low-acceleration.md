# Residual mining for overlooked low-acceleration effects

## Status
Research reconnaissance. This file collects places where a small, coherent physical effect could plausibly be hidden inside what is currently treated as noise, nuisance parameters, calibration drift, or unexplained systematics. It also records cases where ordinary systematics are already strong enough to explain apparent anomalies.

The goal is not to cherry-pick anomalies. The goal is to ask whether residuals from very different experiments collapse onto one predeclared scaling law.

## Core principle
An individual residual can be below the precision floor while a coherent trend across many observations is statistically detectable. Random noise falls approximately as 1/sqrt(N) under averaging, whereas a reproducible model-dependent residual does not. Systematic errors also do not average away, so any candidate effect must be distinguished from instrumental/environmental systematics using changes of method, geometry and scale.

The key control variable suggested by the current WijSAmen/RAR candidate is not physical size by itself but acceleration relative to a characteristic scale a0.

## Candidate law currently under test
For the empirical RAR-like branch:

    x = sqrt(g_N/a0)
    D = g_eff/g_N = 1/(1-exp(-x))

The fractional excess is

    delta = D-1 = 1/(exp(x)-1).

This is mathematically identical to a Bose/Planck occupation factor. This identity is not new; the empirical RAR has previously been noted to resemble the Planck law.

Useful asymptotics:

High acceleration:

    delta ~ exp(-sqrt(g_N/a0)).

Low acceleration:

    g_eff ~ sqrt(a0 g_N) + g_N/2 + ...

Therefore a direct unscreened version of this law predicts exponentially tiny deviations at high acceleration and large deviations only when g_N approaches a0.

## Candidate archive A — measurements of Newton's G
### Why interesting
Precision measurements of G have a spread larger than their stated individual uncertainties. Reviews describe G as exceptionally difficult to measure and report significant inter-experiment inconsistency. The standard expectation is unaccounted systematic error(s).

A 2020 paper by Norbert Klein proposed that some discrepancies among Cavendish-type experiments could instead be interpreted through MOND-like corrections depending on source acceleration and experimental operating mode. A 2026 MNRAS paper revisited a possible common low-acceleration interpretation across G experiments, wide binaries and galaxies.

### Crucial negative result for OUR current RAR branch
The exact exponential RAR function is much more strongly suppressed at laboratory accelerations than Klein's flexible interpolation.

Example from Klein's reconstruction of the Quinn torsion experiment:

    g_source ~ 396 a0.

Our direct RAR branch predicts

    sqrt(396) ~ 19.9
    delta = 1/(exp(19.9)-1) ~ 2.3e-9

or only about

    0.0023 ppm.

This is far below the tens-to-thousands of ppm discrepancies discussed for G measurements.

Therefore:

**The naive universal local application of the current RAR function does NOT explain the historical G scatter.**

This is a valuable falsification result.

If a future WijSAmen action theory predicts laboratory effects, it must either:
- contain a different observable/coupling than the galactic RAR branch;
- predict a justified environment or boundary-condition dependence;
- or accept that G scatter is unrelated conventional systematics.

No environment/screening factor may be added merely to save the hypothesis after the fact.

### Ordinary-systematic alternatives
Known plausible error mechanisms include:
- torsion-fibre anelasticity;
- deviations from Hooke's law;
- magnetic damping corrections;
- thermal gradients;
- electrostatic couplings;
- geometry/source-mass characterization;
- feedback/calibration details.

These must remain the default explanation unless a new model predicts a method-independent residual pattern in advance.

## Candidate archive B — wide binary stars
### Why interesting
Wide binaries can reach internal accelerations near or below a0 at separations of several thousand AU while containing essentially no dark-matter halo of their own. They are therefore conceptually powerful discriminants between extra-mass explanations and modified-gravity-like effects.

### Current observational status is conflicted
Recent studies disagree. A 2024 critical review argued that several analyses find a low-acceleration enhancement consistent with MOND and that some Newtonian-preferring analyses are biased by sample/statistical choices. A rigorous 2026 framework using Gaia DR3 instead finds no ~20% MOND velocity enhancement and reports that increasingly strict quality control reduces apparent anomalies.

Therefore wide binaries are not confirmation; they are an adversarial test.

### Prediction of the naive current RAR branch
At g_N=a0:

    D = 1/(1-e^-1) = 1.582

so circular/orbital speed would scale roughly as sqrt(D), implying a velocity boost of about 25.8% in an isolated algebraic application.

At 10 a0:

    D ~ 1.044

so speed boost is about 2.19%.

The 2026 clean-sample null result therefore places real pressure on a naive isolated two-body version of the formula.

A future field theory could produce environment dependence, but that dependence must emerge from the action and must also survive Solar-System constraints.

## Candidate archive C — Cassini / Solar-System residuals
A July 2026 Phys. Rev. D analysis using planetary ephemeris/Cassini tracking constrains the MOND external-field quadrupole parameter to

    Q2 = (1.6 +/- 1.8)e-27 s^-2.

The authors find strong tension between this Solar-System bound and several classical modified-gravity MOND implementations, including galaxy-scale expectations.

Importance for WijSAmen:
- our present algebraic RAR fit does not yet specify an external-field effect or relativistic field equation;
- therefore Cassini does not directly falsify the algebraic fit;
- but any completed gravitational action MUST be run through this constraint before it can be considered viable.

Cassini should be a hard gate, not an optional later check.

## Candidate archive D — distant Solar System / Oort Cloud scale
For the Sun, the Newtonian acceleration falls to a0 at approximately

    r_M = sqrt(G M_sun/a0) ~ 7,000 AU.

NASA places the inner Oort Cloud at roughly 2,000-5,000 AU and the outer cloud out to tens of thousands of AU. Thus the natural a0 transition scale for the Sun lies in the Oort-Cloud distance range.

This is conceptually attractive because it tests the same acceleration scale without a galaxy-sized system.

Complication:
- the Galactic external gravitational field near the Sun is itself of order a0;
- Oort-cloud dynamics are strongly perturbed by Galactic tides and passing stars;
- individual orbital solutions are extremely poor.

Therefore this is a future statistical/dynamical target, not a clean present confirmation.

## Candidate archive E — galaxy residuals hidden as nuisance parameters
SPARC/RAR inference depends on distance, inclination, stellar mass-to-light ratio, gas mass and non-circular motions. Modern joint-inference work finds the underlying intrinsic RAR scatter can be extremely small (~0.034 dex in one 2023 analysis), and plausible additional uncertainties can reduce it further.

This is directly relevant to the user's idea: some variation that looks like measurement uncertainty may be structured. But the reverse is equally important: fitting nuisance parameters can artificially tighten a relation if the assumed law is wrong.

The correct test is therefore:
1. predeclare the candidate force law;
2. independently constrain distance/inclination/M/L where possible;
3. predict residual signs from the law;
4. test whether residuals correlate with those signs rather than merely shrinking after refitting nuisance parameters.

## Candidate archive F — Renzo's rule / local baryon-dynamics correspondence
Renzo's rule is the claim that features in a galaxy's baryonic/luminosity profile correspond to features in its rotation curve. If universally true, it would be striking evidence for a tight local baryon-dynamics coupling.

A 2025 statistical reanalysis finds some strong individual examples, especially NGC 1560, but does NOT find clear universal support across SPARC; current spatial resolution limits the test and both MOND and LambdaCDM mocks show tensions in some feature statistics.

Therefore this is useful precisely because it is not a clean success: a real WijSAmen field law should predict when local features propagate into dynamics and when they are smoothed/suppressed.

## Candidate archive G — laboratory/atom-interferometer residuals as methodological lesson
Precision atom-interferometer literature contains examples where a previously underappreciated gravity-gradient contribution produced a systematic bias. This is an established example of the general lesson that a tiny neglected term can masquerade as measurement error.

It is not evidence for new gravity. It demonstrates why residual mining must model conventional cross-couplings before interpreting a coherent signal as fundamental physics.

## Cross-scale test matrix
A good theory must explain BOTH detections and nulls.

| Regime | Approx acceleration | Current status | Role |
|---|---:|---|---|
| Galaxy outer disks | <= a0 | strong recurring RAR discrepancy | primary target |
| High-z galaxies | <= a0 | RAR persists; a0 may evolve | time-evolution test |
| Wide binaries | ~0.1-10 a0 | disputed / 2026 rigorous null | adversarial discriminator |
| Solar System planets | >> a0 internally | extremely Newtonian; strong EFE limits | hard null constraint |
| Oort-cloud distances | ~a0 for Sun | poorly measured, environment-dominated | future target |
| Cavendish G tests | tens-hundreds-thousands a0 | G scatter beyond error bars | residual archive; naive RAR fails |

## Frozen no-cheating rules
1. A residual counts only if its sign and scale dependence were predicted before inspecting that subset.
2. One universal parameter set per theory branch; no per-experiment rescue parameters unless independently measurable.
3. Failed scales remain in the scorecard.
4. Conventional systematics are modeled first.
5. A new environment/screening term must be derived from an action or independent principle, not invented after a contradiction.
6. Prefer cross-method residual correlation over single-experiment significance.

## Immediate implications for the current hypothesis family
### What is strengthened
- A recurring low-acceleration transition near a0 across galaxy data is real and exceptionally regular.
- The high-acceleration exponential suppression of the empirical RAR naturally explains why ordinary inner-Solar-System measurements would see essentially nothing in a simple local version.
- High-redshift evolution of a0 is now an independent testable direction.

### What is weakened / constrained
- The same exact exponential RAR law cannot simply be used to explain the historical laboratory-G scatter at source accelerations of hundreds of a0.
- A naive isolated-law prediction for wide binaries is in tension with a high-quality 2026 Gaia analysis.
- Classical external-field implementations of MOND face stronger Cassini constraints as of July 2026.

These are not reasons to abandon the enriched-zero hypothesis. They tell us that a genuine theory must specify WHAT physical quantity the boundary action couples to and HOW environmental boundary conditions enter.

## Strongest next theoretical question
Instead of asking only

    g_eff = g_N Z(x) ?

we need an action producing a field equation in which:
- the galaxy RAR appears in the appropriate weak/low-acceleration limit;
- high-acceleration Solar-System corrections are exponentially or otherwise strongly suppressed;
- lensing is predicted;
- environmental dependence is fixed rather than fitted;
- the wide-binary and Cassini outcomes follow from the same equations.

## Evidence anchors
- Rothleitner & Schlamminger review of G measurements: G results scatter beyond quoted uncertainties.
- CODATA-2022 G remains unusually imprecise relative to other fundamental constants.
- Klein (2020), CQG 37 065002: MOND interpretation of Cavendish G discrepancies.
- Scarpa, Falomo & Treves (2026), MNRAS 548 stag548: laboratory-to-astrophysics low-acceleration comparison.
- Clarke (2026), MNRAS 547 stag342: rigorous wide-binary framework finding no MOND velocity boost.
- Hernandez, Chae & Aguayo-Ortiz (2024), MNRAS 533: contrary critical review arguing for a low-acceleration anomaly.
- Hees et al. (2026), PRD 114 024066: improved Cassini/ephemeris constraints on MOND external-field quadrupole.
- Desmond (2023), MNRAS 526: underlying SPARC RAR with very small inferred intrinsic scatter.
- Ko et al. (2025), MNRAS 544: statistical re-test of Renzo's rule.
- Nobili et al. (2020), PR Research 2 012036: overlooked gravity-gradient systematic in atom interferometry.

## Decision log
- 2026-08-31 — Started residual-mining track. Found G-measurement scatter as a direct example of unexplained residuals, but also found that the current exponential RAR branch predicts far too small a correction at representative Cavendish accelerations. Wide binaries and Cassini added as mandatory adversarial gates rather than supportive anecdotes.
