# PH-060 — FraudeVangst M4A transcription repair

Date: 2026-10-08

## Durable-state status

- GitHub preservation: **VERIFIED**
- ChatGPT Library artifact: **VERIFIED**
- Portfolio Hunter write: **NOT_ATTEMPTED**
- Reason: the prior native Google Docs write returned `403 PERMISSION_DENIED`, and current read-only metadata still does not expose unambiguous `canEdit` evidence. No permission, sharing, account or security setting was changed.
- Portfolio Hunter therefore still ends at `PH-058-OUTPUT-SHARE-ACCEPTANCE-GATE`; `PH-059` and this capsule remain explicit fallback records.

## Verified corpus boundary

`COMPLETE 413/511 → NEXT chunk_0414.jsonl`.

Map2 remains the sole owner of sequential ledger advancement. This steward did not advance the ledger.

## Source checkpoint — FraudeVangst test 20261008_003128

Source: Library file `FraudeVangst-latest-report.txt`, `libfile_7c0d7d96154c8191affa8beff2e20a1b`.

Verified observations:

- recording started at 2026-10-08 00:31:29 +02:00 and stopped at 00:32:26;
- the M4A exists and is nonempty (reported 668 KiB);
- Whisper loaded the `ggml-base.bin` model;
- miniaudio failed to decode the A52s-generated M4A;
- no transcript was produced;
- the analyzer consequently reported `onvoldoende tekstsignalen`.

Interpretation: the quick-settings recording path worked; the immediate failure is the M4A decode boundary, not evidence that recording or model loading failed.

## Implemented reversible improvement

Created `FraudeVangst-Termux-setup-v0.1.2.sh`.

The new version:

- preserves the original M4A and its SHA-256;
- converts M4A/AAC/MP4 audio to mono 16 kHz PCM WAV when `ffmpeg` is already present;
- hashes the derived WAV separately;
- sends the derived WAV to `wijtranscribe`;
- records a clear error if conversion fails or `ffmpeg` is absent;
- does not install packages, start a recording or change permissions by itself;
- distinguishes an absent/empty transcript from a genuine zero-hit text analysis.

Verification:

- Bash syntax: **PASS**
- analyzer byte-compilation: **PASS**
- synthetic four-signal analysis fixture: **PASS**
- synthetic AAC/M4A → mono 16 kHz PCM WAV conversion: **PASS**
- on-device execution: **NOT YET VERIFIED**

Library artifact:

- `FraudeVangst-Termux-setup-v0.1.2.sh`
- `libfile_f687770b8f648191b62e9da8f884ef62`
- readback: 6,399 bytes / 202 lines; version and conversion logic present.

Repository:

- commit `6147ec7dc0b29c455901d8a65e9717e30bf4c8b0`
- blob `78927dbc143a8b654132e81e3426345ab3651dea`
- path `tools/fraudevangst/FraudeVangst-Termux-setup-v0.1.2.sh`

## Evidence and safety boundary

This repair addresses local decoding only. It does not establish caller identity, guilt, fraud or legal status. Caller ID can be spoofed. No audio or transcript was published or sent externally. No app installation, package installation, recording, permission change, security change, external communication, payment or task rotation occurred.

## Decision queue / next verification

Human-visible device action is still required to install or run v0.1.2. If `ffmpeg` is absent, the script reports the exact visible prerequisite instead of installing it automatically. Success requires a new case containing:

1. nonempty `audio_for_whisper.wav`;
2. nonempty `transcript.txt`;
3. `analysis.json` with `transcript_present: true`;
4. no decode failure in `transcribe.log`.

MARKER: PH-060-FRAUDEVANGST-M4A-TRANSCRIPTION-REPAIR
PREVIOUS_PRIMARY_DOC_MARKER: PH-058-OUTPUT-SHARE-ACCEPTANCE-GATE
PREVIOUS_FALLBACK_MARKER: PH-059-RESPONSE-VARIANT-CALIBRATION-GATE
