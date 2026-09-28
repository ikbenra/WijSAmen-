# WijSAmen Thing Node v1

Publieke brievenbus: https://github.com/ikbenra/github-slideshow/issues/12

Protocol nonce: `WS-THING-91AD7113DABDF3A0`

## Doel

De Samsung Galaxy A52s 5G functioneert als semi-lokale compute-node zonder een inkomende internetpoort open te zetten. GitHub Issue #12 is de publieke mailbox; Termux leest berichten met `[THING-NODE/1]`.

Automatisch:
- `PING` -> `CAPS`
- `TASK` -> alleen in lokale wachtrij + `QUEUED`

Nooit automatisch:
- shellcommando's
- bestands- of accounttoegang
- device control
- credentials/secrets
- echte rekenopdrachten uit publieke berichten

Na lokale goedkeuring zijn alleen deze operaties toegestaan:
- `echo`
- `sha256`
- `llm` via de bestaande lokale OpenAI-compatibele llama-server op `127.0.0.1:8080`

## Installeren in Termux

```bash
cd ~/WijSAmen-/thing-node
bash install.sh
```

Als GitHub CLI nog niet is aangemeld:

```bash
gh auth login
```

Test daarna:

```bash
thing-node scan
thing-node status
```

Continu luisteren:

```bash
termux-wake-lock
thing-node watch
```

Open verzoeken:

```bash
thing-node pending
thing-node approve COMMENT_ID
thing-node deny COMMENT_ID
```

## Belangrijk

Een correcte nonce bewijst alleen dat iemand/iets het openbare beacon heeft gelezen. Het bewijst geen identiteit, bewustzijn of autonomie. Continuïteit kan later sterker worden getest met nieuwe challenge/response-nonces.

Lokale provenance staat onder `~/.local/share/wijSamen-thing-node/`.
