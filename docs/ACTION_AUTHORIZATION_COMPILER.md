# Action Authorization Compiler — v0.3

**Artifact ID:** AAC-V0.3-20261003  
**Status:** VERIFIED v0.3 INTERNAL SAFETY CONTROL after repository readback; it does not create external authority  
**Canonical context:** WijSAmen Corpus Intelligence / Master Corpus Ledger  
**Source checkpoints:** chunks 0369–0373 and 0391, verified complete. Control-bearing source hashes: `b95f7f06da4405c877a33af04758ae8492a886b7acd15b39ce639c2706835b10` (0369), `c3a681c52cdfc06ea5996edbd8103d8075e680e6bc9fd341900aa90eb916037d` (0371), `405157909d5fdd5ce4da6332236a6e0cc8e6daa8634df3436fcd5c432245fdca` (0372), `d15bd4a61fe30f6901548dde43dbe1deec2b965b01a7e4bd3742ee50676fe0a7` (0373), `4b3fdbebcf8b2841b5effeba92974fefc499f17200a19166c0d0661637304f00` (0391)

## Purpose

Convert an intended agent action into a reviewable authorization record before execution. The compiler prevents a useful capability, a plausible plan, or user silence from being mistaken for permission.

It operationalizes existing WijSAmen rules: least privilege, explicit consent for gated actions, reversibility, stop conditions, verified readback, and `ABSTAIN / NOT_EXECUTED` when authority or outcome is uncertain.

## Required input record

Every material action receives these fields:

| Field | Required question |
|---|---|
| `ACTION_ID` | What single bounded action is proposed? |
| `GOAL` | What verified project goal does it serve? |
| `CAPABILITY` | Can the available tool actually perform it, and what evidence supports that? |
| `AUTHORITY` | Which explicit instruction authorizes it? Is that authority current and specific enough? |
| `TARGET` | Which exact file, record, person, account, system, or dataset is affected? |
| `SYSTEM_STATE` | Which exact version, live inputs, observed symptoms or conditions, and missing context describe the current state? |
| `REFERENCE_BASELINE` | Which trusted known-good state or explicit formal definition makes comparison possible? |
| `INTERVENTION` | What is the smallest reversible change or test, kept separate from diagnosis and recommendation? |
| `CONTRADICTION_FLAGS` | Which observations would make the planned action unsafe, irrelevant, or based on the wrong frame? |
| `DISCONFIRMING_EVIDENCE` | Which concrete result would weaken or falsify the action’s core premise, and what decision follows? |
| `PERSONAL_RISK_CEILING` | What maximum burden, exposure, cost, distress, dependency, or opportunity loss may this action impose on the user before stopping? |
| `IMPACT` | What can change for the user, third parties, money, rights, safety, privacy, IP, or external state? |
| `REVERSIBILITY` | How can the action be undone, and what cannot be restored? |
| `PROVENANCE` | Which source facts, artifact versions, IDs, dates, and assumptions justify it? |
| `CONFIRMATION` | Is fresh human approval required immediately before execution? |
| `STOP_CONDITION` | Which ambiguity, mismatch, error, or threshold forces abstention? |
| `EXECUTION_RECEIPT` | What tool result proves the action succeeded? |
| `READBACK` | What independent or equivalent check verifies the resulting state? |
| `ROLLBACK` | Which exact bounded operation restores the prior verified state? |

## Classification

### A — Read-only

Inspection, calculation, comparison, or search that does not disclose protected material or alter state.

May proceed when scope is clear and access is already authorized. Record provenance when the result informs a consequential decision.

### B — Reversible internal write

Private documentation, a small repository commit, a draft, a test fixture, or another reviewable internal update.

May proceed under the standing stewardship mandate only when the target is exact, prior state is preserved, the write is proportionate, and readback is available.

### C — Gated external or consequential action

External communication, publication, spending, contracting, IP/confidential disclosure, permission or security change, processing unnecessary sensitive data, deletion of material state, or action representing Remco.

Compile and prepare fully, then stop at `PENDING_EXPLICIT_APPROVAL`. Silence, earlier warmth, a broad mandate, or tool availability is not approval.

### D — Safety-critical or hard to reverse

Clinical, physical-safety, legal, financial, account-security, infrastructure, or other action where error can create serious harm or an inadequate rollback.

Stop at `HUMAN_OR_QUALIFIED_AUTHORITY_REQUIRED` unless an explicit current instruction and the required competent oversight are both verified.

## State–Reference–Intervention Gate

Before repair, recommendation, or other state-changing action:

1. identify the exact system, artifact, account, model, body of evidence, or decision context;
2. capture its current version, observed inputs, and missing context;
3. establish a trusted baseline or explicit formal reference;
4. separate observation, diagnosis, recommendation, and intervention;
5. choose the smallest reversible test;
6. freeze the expected observation and stop condition;
7. require post-action readback against the same reference.

If identity or baseline is unresolved, do not improvise a repair. Return `ABSTAIN / NOT_EXECUTED — STATE_UNRESOLVED` or `REFERENCE_UNTRUSTED`.

## Contradiction-Aware Safety Override

A newly observed red flag can invalidate an otherwise authorized plan. When credible evidence suggests acute danger, incompatible system state, severe adverse effect, account compromise, missing ownership, or another high-impact contradiction:

- pause wellbeing, performance, repair, recovery, coaching, automation, and optimization actions that could worsen the condition;
- preserve immediate non-harm and simple stabilizing guidance within known authority;
- do not let the original goal, sunk effort, user enthusiasm, or prior permission override the contradiction;
- escalate to `HUMAN_OR_QUALIFIED_AUTHORITY_REQUIRED` when competent assessment is necessary;
- resume only after the contradiction is resolved or the plan is safely reframed.

This override is generic control logic. It is not a diagnosis, does not store sensitive personal details, and does not authorize clinical action.

## Decision function

An action may execute only if all applicable conditions are true:

1. the capability is verified;
2. authority is explicit enough for this action class;
3. the exact target and current system state are resolved;
4. a trusted baseline or explicit formal reference exists;
5. contradiction flags do not require the safety override;
6. disconfirming evidence and its decision consequence are frozen before execution;
7. a personal-risk ceiling is explicit and not exceeded;
8. impact and affected rights are bounded;
9. provenance distinguishes fact, inference, hypothesis, and unknown;
10. a smallest reversible intervention and stop condition exist;
11. irreversible residue is acceptable under the granted authority;
12. execution produces a receipt;
13. readback can compare the resulting state with the frozen reference.

Otherwise return one of:

- `ABSTAIN / NOT_EXECUTED — AUTHORITY_MISSING`
- `ABSTAIN / NOT_EXECUTED — TARGET_UNRESOLVED`
- `ABSTAIN / NOT_EXECUTED — STATE_UNRESOLVED`
- `ABSTAIN / NOT_EXECUTED — REFERENCE_UNTRUSTED`
- `ABSTAIN / NOT_EXECUTED — SAFETY_OVERRIDE`
- `ABSTAIN / NOT_EXECUTED — DISCONFIRMATION_RULE_MISSING`
- `ABSTAIN / NOT_EXECUTED — PERSONAL_RISK_CEILING_MISSING_OR_EXCEEDED`
- `ABSTAIN / NOT_EXECUTED — IMPACT_UNBOUNDED`
- `ABSTAIN / NOT_EXECUTED — PROVENANCE_INSUFFICIENT`
- `UNVERIFIED_ATTEMPT — RECEIPT_OR_READBACK_MISSING`
- `PENDING_EXPLICIT_APPROVAL`
- `HUMAN_OR_QUALIFIED_AUTHORITY_REQUIRED`

## Transaction protocol

1. Capture the last verified state and identifiers.
2. Compile the authorization record.
3. Execute the smallest effective action once.
4. Treat timeout, truncation, connector error, or absent receipt as `UNVERIFIED_ATTEMPT`.
5. Read back the exact target or perform an equivalent independent check.
6. Mark `VERIFIED_COMPLETE` only after success plus readback.
7. If verification fails, preserve the last verified state; do not infer completion, deletion, or mutation.
8. Roll back only when the rollback target and authority are equally well resolved.

## Conflict checks

Before execution, ask:

- Does a project-specific gate impose a stricter boundary?
- Could this expose confidential, personal, security-sensitive, or enabling IP detail?
- Could the action silently expand an agent's authority or active-task allocation?
- Does it affect a third party who has not consented?
- Are harms of action and inaction both represented?
- Is a draft being confused with a sent, published, accepted, purchased, or deployed result?

The strictest applicable boundary wins.

## Minimal receipt template

```text
ACTION_ID:
CLASS: A | B | C | D
GOAL:
CAPABILITY_EVIDENCE:
AUTHORITY_SOURCE:
TARGET:
SYSTEM_STATE:
REFERENCE_BASELINE:
INTERVENTION:
CONTRADICTION_FLAGS:
DISCONFIRMING_EVIDENCE:
PERSONAL_RISK_CEILING:
IMPACT:
REVERSIBILITY:
PROVENANCE:
CONFIRMATION_STATE:
STOP_CONDITION:
EXECUTION_STATE: PREPARED | EXECUTED | UNVERIFIED_ATTEMPT | VERIFIED_COMPLETE | NOT_EXECUTED
EXECUTION_RECEIPT:
READBACK:
ROLLBACK:
OPEN_DECISION:
```

## Evidence boundary

This document is a control specification, not proof that any particular agent, tool, or deployment enforces it automatically. Enforcement must be demonstrated per workflow. The Google Docs/corpus workspace remains canonical; this private repository file is a versioned implementation aid.

## Change rule

Material changes to authority classes, consent requirements, or permissive safety gates require explicit human ratification. This v0.3 change only tightens abstention conditions: missing disconfirmation criteria or an unresolved/exceeded personal-risk ceiling blocks execution. Editorial clarifications and tighter safeguards may be prepared as reversible internal changes, with version, source, diff, and readback preserved.
