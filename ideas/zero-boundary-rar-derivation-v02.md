# Zero-boundary RAR derivation attempt v0.2

## Status
Candidate derivation architecture, not established physics.

Goal: derive the empirical SPARC/RAR response

    g = g_N / (1 - exp(-sqrt(g_N/a0)))

from a small number of explicit assumptions connected to the enriched-zero / phase / winding picture, rather than inserting the function after seeing the data.

## Step 1 — enriched zero as a directional/phase boundary
Represent a complex/local order coordinate by

    psi = rho exp(i phi),  rho >= 0.

The ordinary projection rho -> 0 collapses all phi to one scalar zero. A real-oriented blow-up instead preserves a boundary circle S^1 of approach directions/phases.

The universal cover of S^1 is R, so a closed phase admits winding sectors labelled by an integer n.

This is standard geometry/topology. It does NOT imply new gravity.

## Step 2 — action cost per boundary winding
Postulate that the effective coarse-grained contribution of the nth accessible winding sector has an additive positive action increment

    Delta S_n = n Delta S.

Define the dimensionless boundary-action coordinate

    x = Delta S / hbar >= 0.

For Euclidean/action-weighted or thermal-style sums, repeated sectors carry weights

    w_n = exp(-n x).

This exponential weighting is standard in statistical/path-integral physics, but applying it to gravitational response is a new model postulate.

## Step 3 — geometric boundary partition factor
If the physically relevant radial response samples the base sector plus repeated boundary sectors n = 0,1,2,..., then

    Z_+(x) = sum_{n=0}^infinity exp(-n x)
           = 1 / (1 - exp(-x)).

This is exactly the same geometric factor that appears in the empirical RAR interpolation.

Important subtlety: the enriched zero itself has two approach sides / full winding orientation. The one-sided n>=0 response therefore requires a physical orientation/causality/radial-selection rule. This has NOT yet been derived. A symmetric sum over +/-n would produce a different function. This is a key falsification/design constraint.

## Step 4 — gravitational response ansatz
Postulate, provisionally,

    g_eff = g_N Z_+(x).

Then

    g_eff = g_N / (1 - exp(-x)).

This multiplicative coupling is NOT yet derived from an action or field equation. It is the most important remaining dynamical assumption.

## Step 5 — derive the square-root coordinate from scale invariance
At small x,

    Z_+(x) = 1/x + 1/2 + x/12 + O(x^3),

so the leading low-boundary response is

    g_eff ~ g_N / x.

For a point baryonic mass M,

    g_N = GM/r^2.

Assume the deep-boundary / low-acceleration regime is spacetime-scale-invariant in the MOND sense: under r -> lambda r and t -> lambda t, acceleration scales as 1/lambda. Therefore the asymptotic gravitational acceleration of a point source must scale as

    g_eff ~ 1/r.

Since g_N ~ 1/r^2 and g_eff ~ g_N/x, x must scale as

    x ~ 1/r.

If there is one universal acceleration scale a0, the natural dimensionless combination with this scaling is

    x = alpha sqrt(g_N/a0).

The dimensionless constant alpha can be absorbed into a redefinition of a0, so choose alpha=1:

    x = sqrt(g_N/a0).

This is stronger than simply inserting the square root from the empirical RAR: GIVEN the geometric partition response, a universal acceleration scale and deep-regime scale invariance, the square-root coordinate is forced up to a constant.

## Step 6 — resulting law
Substitution gives

    g_eff = g_N / [1 - exp(-sqrt(g_N/a0))].

This is exactly the commonly used empirical SPARC/RAR function.

High-acceleration limit:

    g_N >> a0  -> x >> 1 -> Z -> 1 -> g_eff -> g_N.

Low-acceleration limit:

    g_N << a0 -> x << 1

and therefore

    g_eff ~ sqrt(a0 g_N).

For circular motion around a point mass,

    v^2/r = g_eff = sqrt(G M a0)/r,

so

    v^4 = G M a0,

recovering the baryonic Tully-Fisher scaling.

This low-acceleration scaling is known MOND phenomenology; it is not a new WijSAmen prediction by itself.

## What has actually been derived vs postulated
### Mathematical consequences
- S^1 boundary -> winding labels.
- equal additive action increments + exponential weighting -> geometric partition factor 1/(1-exp(-x)).
- small-x expansion -> g_N/x leading response if response is multiplied by Z.
- scale invariance + universal a0 -> x proportional to sqrt(g_N/a0).
- together -> the empirical RAR functional form.

### Physical postulates still unsupported
P1. The enriched-zero boundary is physically relevant to gravity rather than only a mathematical representation.
P2. Winding sectors acquire equal additive action increments.
P3. Their physical weights are exp(-n x).
P4. The gravitational response is multiplied by the partition factor Z rather than depending on ln Z, d ln Z/dx, or another observable.
P5. A radial/causal selection rule yields the effective one-sided winding sum.
P6. A universal acceleration scale a0 exists and must be derived from deeper physics.

Without deriving at least P2-P6 from an action/Lagrangian or equivalent dynamics, this remains a phenomenological model architecture.

## Why the geometric factor is not arbitrary mathematics
The same factor

    1/(1-exp(-x))

is a standard partition-function structure for equally spaced quantum levels, e.g. the harmonic oscillator after removing the zero-point prefactor. This makes the form physically familiar: it naturally describes repeated equally spaced action/energy sectors.

That does NOT show galaxies are quantum harmonic oscillators. It only demonstrates that the RAR factor has a standard interpretation as a geometric partition sum.

## Candidate route for a0 — NOT YET DERIVED
MOND literature has long noted the numerical relation

    2 pi a0 ~ c H0 ~ c^2 sqrt(Lambda/3).

A zero-boundary/phase theory containing an S^1 cycle makes the appearance of 2 pi conceptually interesting, but this is not enough to derive the relation.

Two distinguishable branches should be kept:

### H-branch (evolving scale)
    a0(t) proportional to c H(t)/(2 pi).

This predicts systematic redshift evolution of the acceleration scale.

### Lambda-branch (approximately constant scale)
    a0 proportional to c^2 sqrt(Lambda/3)/(2 pi).

If Lambda is constant, this predicts a nearly time-independent a0.

These branches can be observationally discriminated. A 2026 MUSE-DARK analysis reports a larger characteristic RAR acceleration at intermediate redshift and increasing a0 with z. This makes the H-branch especially testable, but the result must not be treated as confirmation until a parameter-free redshift prediction is compared against the full data and systematics.

## New prediction opportunity
Do NOT refit a0 independently at every redshift if testing the H-branch.

Instead:
1. Fix a0(0) or, better, derive its normalization.
2. Predict

       a0(z)/a0(0) = H(z)/H0

   under the H-branch.
3. Freeze cosmological parameters independently.
4. Compare predicted a0(z) against high-z RAR measurements without galaxy-by-galaxy adjustment.

The Lambda-branch instead predicts no comparable evolution.

This creates a real discrimination test between two versions of the boundary-scale idea.

## Strongest next theoretical step
Construct an explicit effective action whose field/configuration space contains the enriched directional boundary and winding sectors, and show whether integrating/summing over those sectors yields a gravitational equation in which the observable acceleration is multiplied by Z_+(x).

A serious model should make the one-sided orientation rule and the action increment Delta S explicit rather than adding them by hand.

## Falsification
This derivation architecture should be rejected or demoted if:
- no consistent action produces the proposed response;
- a symmetric treatment of the two-sided boundary necessarily gives a different law with no justified orientation selection;
- blind SPARC tests prefer substantially different functional forms;
- the same law fails lensing, clusters or cosmology;
- predicted redshift evolution of a0 fails high-z data;
- the model merely re-encodes known MOND interpolation without new testable consequences.

## Evidence anchors
- McGaugh, Lelli & Schombert (2016): SPARC radial acceleration relation and the empirical exponential/square-root fit.
- MOND scale-invariance literature: deep-MOND dynamics become spacetime-scale-invariant and yield the sqrt(a0 g_N) regime.
- Standard statistical mechanics: sum_{n>=0} exp(-n x)=1/(1-exp(-x)), including the quantum harmonic oscillator partition function.
- MOND cosmology literature: long-noted order-of-magnitude relation 2 pi a0 ~ c H0 ~ c^2 sqrt(Lambda/3).
- MUSE-DARK III (2026): reported redshift evolution of the RAR characteristic acceleration at 0.33<z<1.44; useful as an independent future test, not current evidence for this model.

## Decision log
- 2026-08-31 — First internal derivation obtained in which the RAR exponential factor follows from a winding/action partition sum and the square-root argument follows from deep-regime scale invariance plus a universal acceleration scale. Classified as a candidate model architecture because the gravitational coupling, action spectrum, one-sided orientation rule and origin of a0 remain underived.
