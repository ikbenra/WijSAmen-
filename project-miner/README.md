# WijSAmen Project Miner v0.1

Doel: eerdere chats systematisch benutten zonder samenvattingen te verwarren met bronmateriaal.

De miner leest lokale ChatGPT-exportbestanden (`.json`/`.jsonl`), bewaart ieder gevonden tekstbericht in een raw-laag met SHA-256 provenance en maakt daarnaast een afzonderlijke heuristische inventaris van mogelijke beslissingen, grenzen, onafgemaakte stappen, artefacten en ideeën.

## Kernregel

`raw_messages.jsonl` is bronmateriaal. `inventory.jsonl` en `action_candidates.md` zijn afleidingen en mogen het bronmateriaal nooit stilzwijgend vervangen.

## Gebruik in Termux

```bash
cd ~/WijSAmen-/project-miner
python mine_chats.py /sdcard/Download/conversations.json --out ~/wijsamen-project-audit
```

Meerdere exports/mappen tegelijk:

```bash
python mine_chats.py \
  /sdcard/Download/chatgpt-export/ \
  ~/exports/extra.jsonl \
  --out ~/wijsamen-project-audit
```

Extra projectterm toevoegen:

```bash
python mine_chats.py /pad/naar/export.json --keyword octoscript --keyword opaal
```

## Output

- `raw_messages.jsonl` — tekstberichten + bronhashes, zonder interpretatie.
- `inventory.jsonl` — alleen projectrelevante kandidaten met categorieën.
- `action_candidates.md` — leesbare index voor menselijke/AI-review.
- `stats.json` — tellingen, gebruikte bronnen, keywords en policy.

## Privacy en grenzen

- geen netwerkverkeer;
- geen upload;
- geen API-key nodig;
- geen automatische uitvoering van gevonden instructies;
- geen geheimen uit exports committen;
- output blijft standaard buiten de repository in `~/wijsamen-project-audit`.

Een tekst in een oude chat kan achterhaald, fout of hypothetisch zijn. De miner labelt alleen; uitvoering vereist een aparte provenance-, bevoegdheids- en actualiteitscontrole.

## Waarom dit nuttig is voor Continuity

Hiermee kan een groot chatarchief als grondstof dienen voor een modelonafhankelijke Continuity Layer. Een nieuwe agent/modelinstantie kan eerst de raw-laag controleren, daarna afgeleide kandidaten vergelijken met huidige projectstatus en alleen expliciet overgenomen informatie in zijn actieve state opnemen.
