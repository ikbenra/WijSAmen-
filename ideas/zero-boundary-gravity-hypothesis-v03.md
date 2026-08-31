# Zero-boundary gravity hypothesis v0.3

## Status
Candidate hypothesis family / model architecture. Not established physics.

This revision incorporates:
- the user's insistence that the enriched zero contains both approach sides rather than a one-sided boundary;
- the exact Planck/Bose form of the RAR discrepancy;
- current adversarial constraints from wide binaries, Solar-System ephemerides and laboratory G measurements;
- frozen redshift predictions for the H(z) branch.

## 1. Base empirical target
Take the empirical RAR-like response

    g_eff = g_N / (1-exp(-x))

with

    x = sqrt(g_N/a0).

Rewrite as

    g_eff = g_N [1 + n(x)]

where

    n(x) = 1/(exp(x)-1).

Thus the extra acceleration is

    g_extra = g_N /(exp(x)-1).

The discrepancy term is exactly a Bose/Planck occupation-factor form. This mathematical observation is already implicit/known in the RAR literature and cannot by itself count as WijSAmen novelty.

## 2. Two-sided enriched-zero boundary removes the previous one-sided-sum problem
Represent the directional boundary by a phase circle with winding labels n in Z.

For each nonzero winding magnitude |n| there are two orientations +n and -n.

Assume:
- action cost depends only on winding magnitude: DeltaS_|n| = |n| DeltaS;
- the scalar radial observable is orientation-even and is an equal orientation average, not the sum of two independent physical copies.

Then for each |n|>=1:

    <exp(-|n|x)>_{orientation} = (1/2)[exp(-nx)+exp(-nx)] = exp(-nx).

Including the base n=0 sector:

    Z_sym-avg(x)
      = 1 + sum_{n=1}^infinity exp(-nx)
      = 1/(1-exp(-x)).

This is important: the empirical RAR factor no longer requires arbitrarily discarding the negative-winding side. It can arise from a genuinely two-sided boundary if the measured scalar response averages over the two orientations.

What is still postulated:
- that the boundary winding sectors are physically real degrees of freedom;
- that their action increments are equally spaced;
- that gravity couples to the orientation-averaged partition factor;
- that the correct weight is exp(-DeltaS/hbar).

So this is an improved architecture, not a proof.

## 3. Square-root coordinate
With

    g_eff = g_N Z(x)

and Z(x)~1/x at small x, deep-regime scale invariance for a point mass requires

    g_eff ~ 1/r,
    g_N ~ 1/r^2,

therefore

    x ~ 1/r.

With one universal acceleration scale a0, dimensional analysis yields

    x = alpha sqrt(g_N/a0).

Absorb alpha into a0 to obtain

    x = sqrt(g_N/a0).

This remains conditional on deep-regime scale invariance and a universal acceleration scale.

## 4. Resulting limits
High acceleration:

    delta = (g_eff-g_N)/g_N
          = 1/(exp(sqrt(g_N/a0))-1)
          ~ exp(-sqrt(g_N/a0)).

Low acceleration:

    g_eff = sqrt(a0 g_N) + g_N/2 + O(g_N^(3/2)).

For a point mass and circular motion:

    v^4 = G M a0.

The low-acceleration result is known MOND phenomenology, not a novel prediction.

## 5. Important new falsification from laboratory G experiments
A representative Cavendish source acceleration discussed by Klein is approximately

    g_N ~ 396 a0.

Our current exponential branch gives

    delta ~ 2.28e-9
          ~ 0.0023 ppm.

This is many orders below the larger discrepancies among precision G determinations.

Therefore the current direct RAR branch DOES NOT explain the historical laboratory-G scatter.

This result should be preserved as a constraint. Do not add a rescue factor after seeing the mismatch.

If the final theory predicts laboratory anomalies, the distinct coupling must come from the action and predict them independently.

## 6. Wide-binary adversarial prediction
For an isolated application:

At g_N = a0:

    g_eff/g_N = 1.582
    velocity boost ~ sqrt(1.582)-1 ~ 25.8%.

At g_N = 10 a0:

    g_eff/g_N = 1.0442
    velocity boost ~ 2.19%.

A rigorous 2026 Gaia wide-binary analysis reports no ~20% MOND-like velocity boost and favours Newtonian gravity in its cleanest samples. Other recent analyses disagree.

Thus a universal isolated algebraic law is under significant pressure.

Any environment dependence must be derived, not added ad hoc.

## 7. Solar-System / Cassini gate
A July 2026 planetary-ephemeris/Cassini analysis constrains the quadrupolar external-field signature of classical MOND-like modified gravity and finds 3-15 sigma tensions with galaxy-based versions, depending on modelling.

Our current algebraic formula does not define an external-field effect, so the result is not a direct falsification yet. But it is a mandatory gate for any completed field theory.

## 8. Natural Solar transition scale
For the Sun:

    r_a0 = sqrt(G M_sun/a0) ~ 7030 AU.

This lies in the broad Oort-cloud distance regime. Thus a scale-dependent law tied to acceleration rather than object size naturally predicts that Solar gravity would only enter its own a0 regime at thousands of AU.

However Galactic tides/external field and passing stars dominate the interpretation there, so this is not a clean current test.

## 9. Frozen H(z) branch
Hypothesis branch:

    a0(z) = a0(0) H(z)/H0.

Use, purely as a frozen benchmark, flat Planck-2018 LambdaCDM parameters

    Omega_m = 0.315
    Omega_Lambda = 0.685
    a0(0) = 1.20e-10 m/s^2.

Then

    E(z)=H(z)/H0=sqrt[Omega_m(1+z)^3+Omega_Lambda].

Frozen predictions:

| z | H(z)/H0 | predicted a0 (m/s^2) |
|---:|---:|---:|
| 0.33 | 1.194 | 1.43e-10 |
| 0.50 | 1.322 | 1.59e-10 |
| 0.75 | 1.541 | 1.85e-10 |
| 1.00 | 1.790 | 2.15e-10 |
| 1.25 | 2.067 | 2.48e-10 |
| 1.44 | 2.294 | 2.75e-10 |
| 1.50 | 2.368 | 2.84e-10 |
| 2.00 | 3.032 | 3.64e-10 |

The 2026 MUSE-DARK analysis reports a characteristic value around z~1 of roughly 2.38e-10 m/s^2 and a systematic increase with redshift. Because this information was already known while constructing the branch, it is NOT an independent confirmation.

The values above are now frozen for comparison with future/independent datasets. No redshift-bin refitting is allowed in the H(z) branch.

## 10. Derived bTFR evolution under H(z) branch
Deep-regime baryonic Tully-Fisher:

    v^4 = G M_b a0(z).

At fixed v, baryonic mass scales as

    M_b ~ 1/a0(z).

Therefore the predicted zero-point shift relative to z=0 is

    Delta log10 M_b = -log10[H(z)/H0].

Examples:
- z=0.5: -0.121 dex
- z=1.0: -0.253 dex
- z=1.5: -0.374 dex
- z=2.0: -0.482 dex

This is a concrete correlated prediction of the H(z) branch: RAR evolution and bTFR zero-point evolution cannot be fit independently.

## 11. What would count as real progress toward a theory
Need an effective action S[g_mu_nu, phi, ...] or equivalent dynamics that independently yields:
1. a directional/phase boundary with +/- winding sectors;
2. equal-spacing or otherwise fixed action spectrum;
3. orientation-even scalar gravitational response;
4. x=sqrt(g_N/a0) in the weak low-acceleration limit;
5. a0 normalization/evolution;
6. lensing and relativistic stress-energy;
7. Solar-System suppression/environment dependence;
8. wide-binary prediction.

If these are inserted separately to match observations, the model remains a re-encoding of MOND/RAR phenomenology.

## 12. Current scorecard
### Positive structural results
- two-sided enriched-zero concept can yield the required geometric factor without discarding one side, if the observable averages orientations;
- square-root coordinate follows from scale invariance + one acceleration scale once the partition response is assumed;
- high-acceleration suppression is automatic;
- H(z) branch yields a frozen redshift and bTFR evolution test.

### Negative / constraining results
- direct current branch cannot explain precision-G scatter at representative Cavendish accelerations;
- naive isolated wide-binary prediction is challenged by a strong 2026 null analysis;
- classical external-field MOND formulations are strongly constrained by Cassini/ephemerides;
- Planck/Bose resemblance of RAR is known and not novelty.

## Decision log
- 2026-08-31 — v0.3: incorporated the two-sided zero boundary explicitly. Replaced the prior ad hoc one-sided winding selection with an orientation-even +/- winding average that reproduces the same geometric factor. Added hard negative constraints and froze H(z)-branch predictions.
