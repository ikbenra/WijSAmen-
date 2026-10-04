# Architectuur — Gaia Listening Layer

## 1. Kleinste bouwsteen: SystemNode

Alles wat een eigen toestand kan hebben wordt als node behandeld:

- organisme of populatie;
- bodemgebied;
- bos;
- rivier of beek;
- landbouwgebied;
- wijk of stad;
- energie- of watersysteem;
- stroomgebied;
- regio;
- biosfeer/technosfeerlaag.

Een node kan een `parent_id` hebben. Daardoor ontstaat hiërarchie zonder dat lagere niveaus verdwijnen.

## 2. Observaties

Een `Observation` bevat minimaal:

- node;
- metric;
- waarde en eenheid;
- tijdstip;
- bron;
- confidence.

Optioneel bevat hij een geconfigureerd referentiebereik. De engine zegt alleen *onder*, *binnen* of *boven* dat bereik. Zij doet in v0.1 geen algemene ecologische diagnose.

## 3. Relaties

Een `Relation` beschrijft een mogelijke of aangetoonde koppeling tussen twee nodes.

Belangrijk: het veld `evidence_level` maakt onderscheid tussen:

- `observed` — direct waargenomen/gemeten relatie;
- `derived` — afgeleid uit data of model;
- `hypothesis` — plausibele maar nog te toetsen koppeling;
- `simulated` — alleen in een simulatiemodel.

Een relation edge mag daarom nooit automatisch als bewezen causaliteit worden uitgesproken.

## 4. Lokale toestand

Per node neemt de engine de laatste waarneming per metric.

- geen interpreteerbare referentiemetrics → `unknown`
- alle interpreteerbare metrics binnen bereik → `stable`
- een minderheid buiten bereik → `watch`
- minstens de helft buiten bereik → `stress`

Dit is bewust een eenvoudig baseline-algoritme. Domeinspecifieke modellen horen later als plug-in erbovenop.

## 5. Synthetische stem

De stem heeft twee lagen:

1. **feitlaag** — gestructureerde state;
2. **vertaallaag** — menselijk leesbare taal.

De vertaallaag mag de feitlaag niet uitbreiden met nieuwe observaties of causaliteitsclaims.

## 6. Systemen-van-systemen

De graaf kan nodes op meerdere schalen verbinden. Een synthese kijkt welke verbonden nodes tegelijk `watch` of `stress` zijn.

Dat levert een **attention candidate**, geen conclusie:

```text
Bos A (stress)
  │ relatie: afvoer / vochtuitwisseling
  ▼
Beek B (watch)

=> gekoppeld aandachtspunt
=> nog geen bewijs dat A de toestand van B veroorzaakt
```

## 7. Toekomstige federatie

Een volwassen versie hoeft geen centrale databak te zijn.

```text
lokale node ─┐
lokale node ─┼─> regionale synthese ─┐
lokale node ─┘                       │
                                    ├─> hogere synthese
lokale node ─┐                       │
lokale node ─┼─> stroomgebied ──────┘
lokale node ─┘
```

Iedere laag kan alleen delen wat hogerop werkelijk nodig is. Dat helpt privacy, robuustheid, lokale autonomie en schaalbaarheid tegelijk.

## 8. Epistemische regel

De software moet altijd onderscheid blijven maken tussen:

```text
meting ≠ interpretatie ≠ model ≠ hypothese ≠ bewustzijnsclaim
```

Juist daardoor kunnen we vrij experimenteren met een communicatieve "stem" zonder wetenschap en metafoor door elkaar te halen.
