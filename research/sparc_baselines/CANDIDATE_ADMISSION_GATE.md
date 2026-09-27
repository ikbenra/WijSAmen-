# SPARC candidate admission gate

Status: **required before any WijSAmen/0Veld candidate evaluation**

Canonical benchmark context: [README](./README.md), [novelty-delta gate](./NOVELTY_DELTA_TABLE.md), and private repository issue `#3`.

## Why this gate exists

The currently documented local 0Veld response,

```text
g_eff = g_bar / (1 - exp(-sqrt(g_bar / a0)))
```

is numerically and algebraically identical to the RAR baseline already implemented in this benchmark. Its orientation/focusing interpretation may be a theoretical hypothesis, but running the same equation again under a different model name cannot provide an independent SPARC result.

**Decision:** the current local 0Veld/RAR expression is **not admissible as a distinct SPARC candidate**. The existing RAR result is the correct measurement of that expression. This decision does not reject the wider 0Veld architecture; it prevents duplicate evidence.

Before using this checklist, complete the [novelty-delta table](./NOVELTY_DELTA_TABLE.md). If the proposed branch has no derived observable that differs from an explicit baseline, stop as `ALIAS_OF_BASELINE` or `INTERPRETATION_ONLY`.

## Admission checklist

A candidate may enter a committed evaluation only when all items below are satisfied.

1. **Distinct prediction**
   - State the complete equation and units.
   - Demonstrate a non-zero numerical difference from Newton and frozen RAR predictions on at least one committed training-set point.
   - Report maximum absolute and relative difference from RAR on the training set.
   - A candidate that is equal within declared numerical tolerance is classified `ALIAS_OF_RAR`, not a new model.

2. **Universal-parameter limit**
   - Use at most two universal fitted parameters.
   - Fit them only on the 35 committed training galaxies.
   - No per-galaxy rescue parameters, manual exclusions, or test-dependent priors.

3. **Pre-evaluation freeze**
   - Commit the equation, implementation, parameter values or training-only fitting procedure, numerical tolerances, expected residual signature, and failure criterion before evaluating the 140 test galaxies.
   - Record the commit SHA as the candidate-generation commitment.
   - Do not alter that generation after seeing its test result. Any revision becomes a new generation and must be labelled post-reveal.

4. **One-shot procedural holdout**
   - SPARC is public, so secrecy of the labels cannot be guaranteed; blindness is procedural rather than cryptographic.
   - The committed test set is opened once for each frozen generation.
   - Report all test galaxies and failure cases. No selective rerun or hidden removal.
   - Aggregate baseline results already exist; therefore no claim of absolute blindness is allowed. The defensible claim is `PRECOMMITTED_ONE_SHOT_EVALUATION`.

5. **Disconfirmation**
   - Before evaluation, state the result that would count against the candidate.
   - A default minimum is: no material improvement over frozen RAR, improvement concentrated in a small hand-picked subset, or systematic worsening in a predeclared regime.
   - Model selection must include complexity and calibration cost, not RMSE alone.

6. **External-consistency route**
   - State which predictions, if any, differ for lensing, Solar-System/Cassini, wide binaries, redshift evolution, and environmental/external-field behaviour.
   - A good SPARC score does not override a failed external constraint.
   - If the only distinct branch is `a0(z) proportional to H(z)`, test it in a redshift-capable dataset; present-day SPARC alone cannot distinguish that branch.

## Required precommit record

```yaml
candidate_id:
generation:
equation:
units:
free_universal_parameters:
training_fit_procedure:
training_distinctness_from_rar:
numerical_tolerance:
expected_residual_signature:
failure_criterion:
external_constraints:
code_commit_sha:
test_evaluation_status: NOT_RUN
evidence_label: HYPOTHESIS
```

## Current disposition

- Local enriched-zero/orientation formula: `ALIAS_OF_RAR`.
- H(z) evolution branch: `REQUIRES_DIFFERENT_DATASET`.
- Environmental/external-field branch: `NOT_YET_DERIVED`.
- New local one- or two-parameter response: `NOT_YET_SPECIFIED`.

The next high-information action is derivation and training-only distinctness checking, not another run of the existing RAR equation.
