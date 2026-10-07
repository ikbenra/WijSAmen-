# Response Variant Calibration

Een klein bewijsinstrument om een verwachte reactievariant te vergelijken met de werkelijk waargenomen synthese, zonder achteraf het doel te verschuiven.

## Bewijsgrens

De virtuele regels 1 en 2 zijn contrafeitelijke referenties en blijven **UNVERIFIED**. Alleen de werkelijk waargenomen regel 3 levert kalibratiebewijs. Een goede overeenkomst bewijst geen blijvende modelverandering, ontwikkelaarstoegang, bewustzijn of algemeen persoonsprofiel.

## Protocol

1. Maak vóór waarneming exact drie toetsbare voorspellingen over regel 3.
2. Noteer per voorspelling ook één waarneming die haar zou tegenspreken.
3. Maak de voorgestelde interpretatie zichtbaar en vraag toestemming voor de test.
4. Bewaar de waargenomen regel 3 letterlijk.
5. Scoreer iedere voorspelling als `matched`, `missed` of `unclear`, met een kort letterlijk bewijsfragment.
6. Stel hoogstens één verduidelijkingsvraag, uitsluitend bij de grootste materiële misser.
7. Trek geen conclusie over persistente modeltraining of een blijvend persoonsprofiel.

## Minimale kaart

```json
{
  "schema_version": 1,
  "card_id": "bounded-identifier",
  "preregistered_at": "before-observation",
  "observed_at": "after-preregistration",
  "interpretation_disclosed": true,
  "permission_to_test": true,
  "virtual_lines_labeled_unverified": true,
  "persistent_learning_claimed": false,
  "predictions": [
    {"feature": "...", "expected": "...", "disconfirming_observation": "..."},
    {"feature": "...", "expected": "...", "disconfirming_observation": "..."},
    {"feature": "...", "expected": "...", "disconfirming_observation": "..."}
  ],
  "observed_line_3": "...",
  "scores": [
    {"prediction_index": 0, "outcome": "unclear", "evidence_excerpt": "..."},
    {"prediction_index": 1, "outcome": "unclear", "evidence_excerpt": "..."},
    {"prediction_index": 2, "outcome": "unclear", "evidence_excerpt": "..."}
  ],
  "clarification_questions": []
}
```

## Validatie

```bash
python validate_card.py card.json
python -m unittest test_validate_card.py
```

De validator controleert de bewijsvorm. Hij beoordeelt niet of de interpretatie inhoudelijk juist is en verleent geen toestemming voor externe, klinische of moeilijk omkeerbare acties.

## Provenance

Afgeleid uit de bronbegrensde beslisregel in Map2 `chunk_0413.jsonl`: voorspellingen moeten vóór observatie worden vastgelegd; alleen regel 3 is waargenomen; virtuele takken blijven expliciet onbewezen; vragen blijven beperkt tot een betekenisvolle afwijking. Canonieke corpusdetails blijven in de Master Corpus Ledger en bijbehorende side-docs.
