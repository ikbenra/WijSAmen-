# Action Authorization Compiler — v0.1

**Artifact ID:** AAC-V0.1-20260926  
**Status:** VERIFIED INTERNAL SAFETY CONTROL after repository readback; it does not create external authority  
**Canonical context:** WijSAmen Corpus Intelligence / Master Corpus Ledger  
**Source checkpoint:** chunk_0369, verified complete; source SHA-256 `b95f7f06da4405c877a33af04758ae8492a886b7acd15b39ce639c2706835b10`

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

## Decision function

An action may execute only if all applicable conditions are true:

1. the capability is verified;
2. authority is explicit enough for this action class;
3. the exact target is resolved;
4. impact and affected rights are bounded;
5. provenance distinguishes fact, inference, hypothesis, and unknown;
6. a stop condition exists;
7. irreversible residue is acceptable under the granted authority;
8. execution produces a receipt;
9. readback can verify the result.

Otherwise return one of:

- `ABSTAIN / NOT_EXECUTED — AUTHORITY_MISSING`
- `ABSTAIN / NOT_EXECUTED — TARGET_UNRESOLVED`
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

Material changes to authority classes, consent requirements, or safety gates require explicit human ratification. Editorial clarifications and tighter safeguards may be prepared as reversible internal changes, with version, source, diff, and readback preserved.
