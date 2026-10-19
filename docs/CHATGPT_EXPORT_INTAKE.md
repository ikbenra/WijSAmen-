# ChatGPT Export Intake Gate

This checklist protects continuity when a new official ChatGPT data export becomes available. It describes verification logic only; it contains no account identifiers, download links, tokens, private chat content or credentials.

## 1. Distinguish request from completion

A request-started confirmation is not proof that an archive is ready.

Accept a completion signal only when all are true:

- it is a new message received after the recorded request time;
- sender and message content are consistent with an official OpenAI/ChatGPT export notice;
- the message explicitly says the export is ready or provides the official retrieval action;
- the expiry time or download window is recorded privately;
- a prior request confirmation is not reused as completion evidence.

If any item is unclear, keep status `REQUESTED / NOT_READY`.

## 2. Private acquisition boundary

The export is a private source artifact.

- Never place its URL, token, ZIP, extracted chats, account data or access logs in this public repository.
- Never forward the message or download link.
- Do not weaken MFA, permissions or browser security.
- Download only through an already authorized session or a user-visible handoff.
- If tools cannot acquire it safely, report `PREPARED_ONLY` and preserve the exact smallest user action.

## 3. Preserve the original

After acquisition:

1. store the original ZIP unchanged in an authorized private archive;
2. record byte size, SHA-256, acquisition time and non-secret source reference in a private manifest;
3. read the stored object back and recompute the hash before claiming preservation;
4. keep older exports immutable; never extract a new export over an older one;
5. create a new dated import workspace for every export.

A successful download without readback remains `UNVERIFIED_ATTEMPT`.

## 4. Safe archive inspection

Before extraction:

- list archive entries without executing files;
- reject absolute paths, parent traversal such as `../`, unexpected device entries and unsafe link targets;
- extract into a fresh bounded directory;
- do not run scripts or HTML/JavaScript from the archive merely to inspect content;
- inventory filenames, counts and timestamps separately from content analysis.

## 5. Continuity import gate

Import into PlanUSje van ALLES / PhaseBridge / Continuity Core only as a new source layer.

- Originals remain unchanged.
- Preserve conversation IDs, message IDs, branches, roles, timestamps and literal empty nodes.
- Label later summaries and reconstructions separately.
- Compare the export boundary with the last verified corpus marker.
- Do not claim a fully live continuity system merely because parsing succeeded.
- Keep private content out of public issues, commits, logs and examples.

## 6. Completion and watcher stop

The export watch may stop only after one of these verified outcomes:

- **SECURED:** original ZIP stored privately, read back and hash-matched; or
- **USER_HANDOFF:** user was given the precise official action and expiry because safe automated acquisition was unavailable.

For `SECURED`, retain one private completion marker with source time, size, digest, storage reference and readback result. Then pause the request-specific watcher so it does not consume a scarce task slot or repeat the same alert.

## Evidence states

`REQUESTED -> COMPLETION_SIGNAL_VERIFIED -> ACQUIRED -> HASHED -> STORED_PRIVATE -> READBACK_VERIFIED -> INTAKE_READY`

Never skip a state silently. Errors and timeouts retain the last verified state.
