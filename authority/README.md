# WijSAmen Action Authorization Compiler v0.1

Autonomie wordt veiliger wanneer uitvoering niet afhangt van losse tekstinterpretatie, maar van een klein expliciet autorisatiecontract.

`authorize.py` **voert nooit zelf een actie uit**. Het leest een JSON-verzoek en retourneert één van:

- `ALLOW_READ_ONLY` — lokale/read-only actie met provenance en stopconditie;
- `ALLOW_SCOPED` — expliciete menselijke toestemming dekt precies deze scope;
- `PREPARE_ONLY` — analyse/voorbereiding mag, uitvoering niet;
- `HUMAN_GATE` — menselijk besluit is vereist;
- `ABSTAIN_NOT_EXECUTED` — bewijs/bevoegdheid ontbreekt of de actie hoort nooit autonoom uitgevoerd te worden.

## Voorbeeld read-only

```json
{
  "id": "probe-vulkan-001",
  "kind": "probe",
  "target": "local:a52s",
  "impact": "read_only",
  "reversible": true,
  "provenance": ["user-request", "thing-node/README.md"],
  "stop_condition": "probe completed or command error",
  "source_trust": "local"
}
```

```bash
python authority/authorize.py request.json
```

## Voorbeeld externe actie

Een publicatie, betaling, accountwijziging, permissiewijziging of device-write krijgt zonder expliciete scoped toestemming geen uitvoeringsrecht. De agent kan wel voorbereiden wat er nodig is en het menselijke beslispunt tonen.

## Belangrijke scheiding

Een geldige beslissing is **geen bewijs dat uitvoering daadwerkelijk plaatsvond**. Een executor hoort daarnaast execution proof, readback en zo nodig rollback te bewaren. Daardoor blijven intentie, autorisatie, uitvoering en resultaat afzonderlijk controleerbaar.
