# WijSAmen Output Share

Termux helper for preserving and sharing the latest complete terminal output.

## Purpose

`wso` keeps a complete Termux session log, creates both raw and ANSI-clean exports, and opens Android's share flow so the result can be attached to ChatGPT or another app in one action.

It is intended to work alongside WijSAmen Device Bridge / Schoenbrug.

## Install

Build the Debian package:

```bash
cd tools/wijsamen-output-share
bash build-deb.sh
pkg install -y ./dist/wijsamen-output-share_0.1.2_all.deb
```

GitHub Actions also builds the package and exposes it as a workflow artifact.

Before packaging, the workflow runs `test-wso.sh`. The acceptance test verifies raw-log preservation, ANSI-clean export, the Downloads mirror, the user-visible Android share invocation, and command exit-code propagation.

## Commands

```text
wso session
wso run <command...>
wso latest
wso export
wso share
wso default
wso chatgpt
wso show
wso status
```

### Typical use

```bash
wso session
# work normally in Termux
wso chatgpt
```

`wso chatgpt` exports the newest complete log, removes terminal escape sequences from the readable copy, preserves a raw copy, and opens Android's share chooser. Version 0.1.2 prefers `termux-open` so sharing does not hang when the Termux:API companion is unavailable.

The package deliberately does **not** attempt to guess or silently address a specific existing ChatGPT conversation. That final step can later be handled by Schoenbrug / Device Bridge with live scene validation.

## Files

Runtime data defaults to:

```text
~/ai/termux-output/
├── current.log
├── logs/
└── share/
    ├── LATEST.txt
    └── LATEST_RAW.log
```

## Safety design

- no arbitrary network upload;
- no stored credentials;
- sharing uses Android's user-visible share mechanism;
- raw output is preserved separately from the cleaned readable export;
- explicit command required before sharing.
