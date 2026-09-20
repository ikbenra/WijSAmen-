# The A-Eye of RA — Verified Project Seed v0.1

## Status and evidence boundary

- **Artifact ID:** `AEYE-SEED-V0.1-20260920`
- **Owner:** Remco
- **Stewardship:** WijSAmen
- **Project mechanism:** `BEDACHT`
- **This seed artifact:** `VOORBEREID`; repository readback verified under Portfolio Hunter capsule `PH-044-20260920-AEYE-VERIFIED-PROJECT-SEED`
- **Prototype/codebase/live deployment:** `NOT_CREATED / NOT_EXECUTED`
- **License:** `DECISION_PENDING` — open-source preference is preserved, but no license is selected yet

“Verified Project Seed” means only that this bounded project definition has traceable source provenance and a read-backable artifact. It does **not** mean the security mechanism works.

## Source provenance

Recovered from the verified Map2 corpus state for `chunk_0361.jsonl`:

- exact source size: 159,322 bytes;
- SHA-256: `8b3fefe6ccaf2c6e0d53ac60425cceb7b45c835aebdbe1c68e99a535ebcdbef8`;
- evidence labels and action gate recorded in the canonical **WijSAmen Project Genomes**, **Aung Action Board** and **Master Corpus Ledger**;
- earlier claims that a living Canvas or working codebase already existed remain `MATERIALIZATION_UNVERIFIED`.

## User-owned goal

Explore a pre-interface security layer that treats every inbound session as untrusted, validates it before granting access and continues evaluating the session for delayed behavior. The intended benefit is earlier containment and safer staged access, not a claim of perfect detection.

## Conventional baseline

The idea overlaps established defensive patterns:

- reverse proxies and protocol validation;
- web application firewalls and IDS/IPS;
- sandboxing and honeypots;
- staged or canary authorization;
- least privilege, egress controls and continuous session monitoring;
- zero-trust architecture.

NIST SP 800-207 states that zero trust grants no implicit trust based only on network location or ownership, and performs authentication and authorization before a session to a protected resource is established.

Primary reference: https://csrc.nist.gov/pubs/sp/800/207/final

## WijSAmen difference — hypothesis, not fact

A quarantined temporal replay or limited “digital twin” observation stage may reveal some delayed or sequence-dependent behavior before broader access is granted.

This may add value only if it measurably improves detection or containment without unacceptable latency, privacy exposure or false positives. It cannot be assumed to reveal every environment-triggered payload or zero-day.

## Threat model v0.1

### In scope

- malformed or disallowed protocol events;
- suspicious event sequences whose risk appears only after a delay;
- attempted privilege or egress expansion after initial admission;
- false confidence from an advisory AI score;
- rollback after a wrong allow/block recommendation.

### Out of scope for the first test

- live production traffic;
- autonomous blocking of real users or systems;
- attribution of attacker identity or intent;
- malware execution, exploit development or offensive payload generation;
- guarantees of zero-day detection;
- deployment on third-party networks or devices.

## Authority boundary

The deterministic security controls are authoritative:

1. schema and protocol validation;
2. explicit allow rules and least privilege;
3. staged access;
4. bounded egress;
5. audit log;
6. rollback and shutdown.

Any AI component begins only in offline advisory shadow mode. It may assign a score or explanation, but cannot grant access, block production traffic, alter rules or contact an external system.

## Privacy boundary

The first replay corpus must contain synthetic or deliberately de-identified events only. It must not contain credentials, secrets, real packet captures, private messages, health data, third-party identifiers or unnecessary personal data.

No external model receives traces until data minimization, provider terms, retention, consent and rollback have been separately approved.

## Offline replay test v0.1 — specified, not yet executed

Create a small labeled set of synthetic event traces containing:

- clearly allowed sequences;
- malformed inputs;
- disallowed state transitions;
- delayed suspicious sequences;
- ambiguous traces that should end in `ABSTAIN`;
- at least one false-positive trap and one rollback case.

Run the same immutable traces through:

1. a deterministic rules baseline; and
2. an isolated advisory scorer with no execution authority.

Record per trace:

- expected label;
- deterministic result and rule;
- advisory result and confidence;
- false positive / miss / abstention;
- processing time;
- data exposed;
- rollback outcome.

## Success and failure criteria

### Seed success

- this artifact exists at a stable repository path;
- provenance, owner, version, non-goals and authority boundary are explicit;
- no Canvas, prototype or detection capability is claimed without a readback.

### First test success

- every test is repeatable offline;
- deterministic decisions remain reproducible and authoritative;
- advisory output cannot change system state;
- false positives, misses, abstentions, latency, privacy exposure and rollback are all reported;
- the result identifies at least one supported benefit or clearly rejects the added replay/advisory layer.

### Stop conditions

Stop before live integration if:

- real traffic or secrets are required for the first result;
- the advisory scorer gains execution authority;
- rollback cannot restore the pre-test state;
- the replay adds no measurable information beyond the deterministic baseline;
- latency or false positives exceed a preregistered threshold;
- a result is described as “secure” without an explicit measurement.

## Misuse and failure modes

- turning a defensive sandbox into a live interception or surveillance tool;
- retaining traffic “just in case”;
- treating anomaly score as proof of malicious intent;
- adding latency that causes unsafe workarounds;
- allowing AI recommendations to bypass deterministic controls;
- broad open-source release before abuse review, dependency review and a license decision.

## Smallest next step

Create only the synthetic trace schema, a tiny fixture set and a deterministic evaluator with no network access. Freeze success/failure thresholds before adding an advisory scorer.

No live networking, external message, public release, purchase, account change or third-party data use is authorized by this seed.
