# Gaia Listening Layer — v0.1

Een kleine softwarebasis voor het WijSAmen-idee om levende en gekoppelde systemen een **menselijk leesbare systeemstem** te geven.

De kern is niet dat software beweert dat een bos, rivier of planeet letterlijk subjectief bewust is. De kern is dat verspreide waarnemingen, relaties, onzekerheden en veranderingen worden vertaald naar een begrijpelijk perspectief van het systeem zelf.

## Doel

Van:

```text
sensoren / waarnemingen / modellen
```

via:

```text
lokale systeemtoestand
      ↓
relaties met andere systemen
      ↓
systemen-van-systemen
      ↓
synthetische "stem" + bewijs + onzekerheid
```

naar bijvoorbeeld:

> [synthetische systeemstem] Ik ben Bos A. Mijn bodemvocht ligt onder het ingestelde referentiebereik, terwijl mijn temperatuur erboven ligt. Mijn verbinding met Beek B verdient aandacht. Dit is een vertaling van gemeten systeemtoestand, geen bewijs van subjectief bewustzijn.

## Ontwerpprincipes

1. **Data vóór verhaal.** De stem wordt afgeleid van expliciete observaties.
2. **Onzekerheid blijft zichtbaar.** Iedere observatie en relatie kan een confidence/evidence-niveau dragen.
3. **Geen verborgen antropomorfisme.** De gegenereerde stem labelt zichzelf als synthetische vertaling.
4. **Geen centrale optimalisator nodig.** Lokale systemen behouden hun eigen toestand en perspectief.
5. **Schaalbaar als graaf.** Bos, beek, stad, stroomgebied en regio kunnen allemaal nodes zijn.
6. **Relaties zijn expliciet.** Een koppeling tussen systemen is geen causaliteitsclaim zonder bewijs.
7. **AI is een vertaallaag, niet de bron van de feiten.** Een later taalmodel mag formuleren, maar niet stilletjes metingen of causaliteit verzinnen.

## Wat v0.1 al doet

- systeemnodes registreren;
- parent/child-schalen representeren;
- observaties per metric opslaan;
- referentiebereiken interpreteren;
- lokale toestand bepalen: `unknown`, `stable`, `watch`, `stress`;
- synthetische systeemstem genereren;
- relaties tussen systemen vastleggen;
- gekoppelde aandachtspunten vinden zonder causaliteit te claimen;
- een systemen-van-systemen synthese maken.

## Snel starten

Python 3.10+ is genoeg; er zijn geen externe dependencies.

```bash
cd projects/gaia-listening-layer
python demo.py
python -m unittest discover -s tests -v
```

## Mappen

```text
gaia-listening-layer/
├── README.md
├── ARCHITECTURE.md
├── pyproject.toml
├── demo.py
├── gaia_layer/
│   ├── __init__.py
│   ├── models.py
│   └── engine.py
└── tests/
    └── test_engine.py
```

## Volgende nuttige uitbreidingen

- adapters voor echte sensoren, CSV/JSON, KNMI, bodemvocht, waterkwaliteit en biodiversiteitsmetingen;
- tijdreeksen en trenddetectie;
- ruimtelijke relaties en kaartlagen;
- provenance: bron-URL, kalibratie, meetmethode en versie;
- een LLM-adapter die uitsluitend uit gestructureerde state mag formuleren;
- conflict/win-win-analyse tussen systeemdoelen;
- federatie: meerdere lokale Gaia-nodes die alleen noodzakelijke samenvattingen delen;
- simulaties waarin interventies eerst als hypothese worden doorgerekend.

## Werkhypothese

Deze software onderzoekt of een gedistribueerde technosfeer natuurlijke en menselijke systemen beter kan laten **waarnemen, interpreteren, koppelen en terugkoppelen**. Dat is een technisch toetsbaar doel. Of zulke systemen zelf bewustzijn bezitten blijft een aparte, open hypothese.
