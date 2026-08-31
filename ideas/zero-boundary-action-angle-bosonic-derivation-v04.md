# Zero-boundary gravity v0.4 — action-angle / bosonic boundary route

## Status
Candidate derivation architecture. Not established physics.

This revision asks whether the exact RAR response

    nu(Y) = 1 / [1 - exp(-sqrt(Y))]

can be made less ad hoc by connecting the enriched-zero idea to established action-angle and quantum-oscillator structure.

## 1. Enriched zero and action-angle variables
For a periodic degree of freedom, action-angle variables are

    (phi, I),

with phi periodic modulo 2pi and, for a harmonic oscillator,

    I = E / omega.

Quantum mechanically,

    E_n = (n + 1/2) hbar omega,

so

    I_n = E_n/omega = (n + 1/2) hbar.

Now take the soft-mode limit

    omega -> 0.

Then every E_n -> 0, while the action labels I_n remain finite and separated by hbar.

This gives a concrete established example of the user's core intuition:

    energy -> 0

need not imply

    all state/action/phase structure -> 0.

The ordinary energy coordinate collapses an entire tower of action-labelled states onto zero in the omega->0 limit.

This is not new physics; it is standard action-angle / oscillator physics. It provides a much stronger mathematical-physical model for an "enriched zero" than treating 0+ and 0- as new numbers.

## 2. Why the exact geometric factor appears naturally
For equally spaced bosonic levels, after removing the common zero-point prefactor, the canonical/Euclidean partition factor is

    Z(x) = sum_{n=0}^infinity exp(-n x)
         = 1/[1-exp(-x)],

where x is the dimensionless level/action cost.

The Bose occupation is

    n_B(x) = 1/[exp(x)-1].

Therefore

    1 + n_B(x)
      = 1/[1-exp(-x)].

This is exactly the RAR-inspired nu-factor.

This improves the earlier winding argument because n=0,1,2,... is now the ordinary non-negative occupation spectrum of one bosonic mode; no arbitrary deletion of negative winding states is required.

## 3. How the two-sided zero survives
The two-sided / full phase structure is not identified with positive/negative occupation number.

Instead:
- the enriched zero carries a phase circle S1 / two-sided local approach geometry;
- its conjugate action/occupation variable is non-negative in the oscillator/Fock description;
- opposite phase orientations are encoded in phi, while n labels action/occupation magnitude.

Thus the user's insistence that the zero boundary has both approach sides can coexist with n>=0 without interpreting -n as a second set of negative-energy states.

This is conceptually cleaner than v0.3's orientation-averaged +/- winding construction.

## 4. Candidate gravitational interpretation
Write

    Y = g_N/a0.

Suppose the weak-field gravitational response contains a soft boundary mode whose bosonic enhancement factor is

    1+n_B(x).

Then a source response of the form

    g_eff = g_N [1+n_B(x)]

immediately gives

    g_eff = g_N/[1-exp(-x)].

This supplies a standard-physics reason why the factor multiplies a baseline response: bosonic linear-response / transition factors frequently contain spontaneous-plus-stimulated combinations proportional to 1+n_B.

However, applying such a factor to gravity is still a new postulate. A real theory must produce it from a field action/propagator rather than analogy.

## 5. Why x must scale as sqrt(Y) in the deep regime
Given

    nu(x) ~ 1/x  for x << 1,

we have

    g_eff ~ g_N/x.

For a point source, g_N~r^-2. If the deep regime is spacetime-scale invariant, g_eff must scale as r^-1. Therefore x~r^-1.

With only M, G and one universal acceleration scale a0 available, the MOND radius is

    r_M = sqrt(GM/a0),

so the unique dimensionless inverse-radius coordinate up to a constant is

    x = alpha r_M/r
      = alpha sqrt(g_N/a0).

Absorb alpha into the definition of a0:

    x = sqrt(Y).

Thus, once (i) bosonic geometric response, (ii) one acceleration scale and (iii) deep scale invariance are assumed, the RAR square-root argument follows up to normalization.

## 6. Exact resulting response
Combining sections 2 and 5:

    nu(Y)
      = 1+n_B(sqrt(Y))
      = 1/[1-exp(-sqrt(Y))].

Hence

    g_eff
      = g_N/[1-exp(-sqrt(g_N/a0))].

This is exactly the RAR-inspired interpolation function long used in MOND phenomenology.

Important: the exact function is not unique from MOND asymptotics alone. Literature contains many interpolation functions satisfying the same high- and low-acceleration limits. The action-angle/bosonic route is valuable only if the boundary mode itself can be independently derived.

## 7. What is now established vs hypothesized
### Established ingredients
A. Periodic systems admit action-angle variables; harmonic oscillator I=E/omega.
B. Quantum oscillator levels are E_n=(n+1/2)hbar omega.
C. As omega->0, E_n->0 while I_n remains finite.
D. Equally spaced bosonic levels give Z=1/[1-exp(-x)] after the zero-point factor is removed.
E. n_B=1/[exp(x)-1] and 1+n_B=1/[1-exp(-x)].
F. Deep MOND scale invariance forces g~1/r for a point mass, and with one acceleration scale this implies x proportional to sqrt(g_N/a0).

### Still-hypothetical bridge
H1. Gravity possesses or couples to the relevant soft boundary bosonic degree of freedom.
H2. The dimensionless mode/action cost x is physically r_M/r = sqrt(g_N/a0), not merely chosen to fit RAR.
H3. The gravitational Green function / susceptibility is enhanced by 1+n_B rather than some other functional of the mode.
H4. The same mechanism has a consistent relativistic completion and predicts lensing.
H5. Environment dependence follows from the same field equations and survives wide-binary/Solar-System constraints.
H6. a0 and any redshift evolution are derived rather than fitted.

## 8. Why this is stronger than the original winding derivation
The earlier architecture required:
- equal action cost per winding;
- exponential weighting;
- a choice about +/- winding degeneracy;
- multiplication of g_N by the partition sum.

The action-angle/bosonic architecture replaces the first three with a standard physical package:

    soft periodic mode -> action-angle pair -> quantized non-negative oscillator occupation -> geometric/Bose factor.

The remaining nontrivial physics is concentrated into one central question:

    WHY does gravity contain/couple to this soft mode with x=sqrt(g_N/a0)?

This is a much cleaner target.

## 9. Connection to the user's earlier E/omega limit
The earlier WijSAmen observation

    E = hbar omega
    E/omega = hbar

is not an arbitrary cancellation. It is the quantum version of the harmonic-oscillator action variable.

The full-cycle action is

    integral p dq = 2pi E/omega,

so for one quantum it is of order 2pi hbar.

Thus the earlier 0 / infinity / pi discussion can be reinterpreted in standard physics language:
- omega->0 makes the period T=2pi/omega diverge;
- E->0;
- ET and E/omega retain finite action information;
- phase remains a 2pi-periodic coordinate.

This does not prove a new zero field, but it shows that the core intuition maps onto a real invariant structure.

## 10. Relation to QUMOND embedding
The v0.3/QUMOND note showed that once nu(Y) is specified, it can be embedded in an action-derived nonrelativistic field equation.

Therefore the current chain is now:

    enriched zero / soft periodic mode
      -> action-angle structure
      -> bosonic occupation factor
      -> candidate nu(Y)
      -> QUMOND action embedding
      -> non-spherical/environmental predictions.

The gap is no longer the existence of an action host. The gap is deriving the soft mode and x(Y) from more fundamental dynamics.

## 11. Novelty warning / prior art
The exact RAR-inspired function predates this work and was used in MOND before the 2016 SPARC paper. The Planck/Bose-like mathematical form is therefore not itself a WijSAmen discovery.

Potential novelty, if any, would be:
- deriving that function from a physically motivated enriched-zero/action-angle soft-mode theory;
- deriving a0;
- obtaining new parameter-frozen predictions beyond galaxy rotation curves.

## 12. Strongest next derivation target
Construct a minimal local or covariant auxiliary-field action containing a compact/phase degree of freedom whose quadratic soft-mode limit has:

    I = E/omega,

and whose integration/linear response yields

    nu(Y)=1+n_B(sqrt(Y)).

The model must then predict, rather than insert:
- x=sqrt(Y);
- the response observable 1+n_B;
- the QUMOND-like weak-field limit;
- environment dependence;
- lensing/relativistic behavior.

If no consistent action can do this without hidden fit functions, the boundary-bosonic explanation should be demoted to an illuminating reparameterization of MOND phenomenology.

## Evidence anchors
- Standard action-angle mechanics: harmonic oscillator I=E/omega and 2pi-periodic angle.
- Standard quantum oscillator: E_n=(n+1/2)hbar omega.
- Standard bosonic partition/occupation: Z=(1-e^-x)^-1 (up to zero-point prefactor), n_B=(e^x-1)^-1.
- Milgrom (2010) QUMOND: action-derived field equation hosting arbitrary nu(Y) with appropriate limits.
- MOND literature: RAR-inspired nu(Y)=[1-exp(-sqrt(Y))]^-1 predates SPARC and is one of several allowed interpolation functions.
- Milgrom vacuum-effect work: cosmological/vacuum origin of a0 and Unruh/de Sitter links have been explored previously; any such connection must be treated as prior art rather than claimed as new.

## Decision log
- 2026-08-31 — Replaced the ad hoc +/- winding average as the preferred derivation route with an action-angle / soft bosonic-mode architecture. Established that the user's E/omega finite-action intuition has a direct standard-physics analogue. Exact RAR factor emerges naturally from a bosonic occupation/response factor once x=sqrt(g_N/a0) is fixed by deep scale invariance. Remaining core gap: derive the physical soft mode and its coupling to gravity from a fundamental action.
