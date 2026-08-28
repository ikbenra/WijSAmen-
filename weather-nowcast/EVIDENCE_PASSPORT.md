# Evidence Passport — persoonlijke 0–3 uur weernowcast

**Datum:** 28 augustus 2026  
**Fase:** PROTOTYPE — CODE AANWEZIG, LIVE TELEFOONVALIDATIE NOG NIET GEVERIFIEERD  
**Canonieke code:** deze map in GitHub  
**Canonieke portfoliobeoordeling:** `WijSAmen Corpus Intelligence — Portfolio Hunter`

## Gewenst resultaat

Een gratis, lokaal bruikbare nowcast voor de komende 0–3 uur die niet alleen een voorspelling toont, maar ook zichtbaar maakt waar die vandaan komt, hoe oud de bron is, hoe onzeker de uitkomst is en hoe goed eerdere voorspellingen werkelijk waren.

## Vijf onafhankelijke bewijsassen

| As | Huidige status | Wat nog nodig is |
|---|---|---|
| Herkomst | KNMI-dataset, versie en bestandsnaam worden gelogd | publicatietijd en bronouderdom expliciet tonen |
| Kennisstatus | kansen per neerslagdrempel, geen schijnexacte enkelvoudige uitkomst | onzekerheid begrijpelijk samenvatten zonder die weg te poetsen |
| Artifactverificatie | code en synthetische test staan in GitHub | actuele KNMI-file op echte Termux-installatie openen en output bewaren |
| Workflowstatus | ophalen, extraheren en lokaal loggen zijn geïmplementeerd | uitvoering op telefoon en radarvergelijking zijn nog niet geverifieerd |
| Bevoegdheid/privacy | logs en downloads worden niet gecommit | bewaartermijn en verwijderoptie voor exacte GPS-locaties toevoegen vóór breder gebruik |

## Source-supported core

- De gebruikte KNMI-dataset publiceert 5-minutenstappen tot 6 uur vooruit op een raster van 1×1 km.
- Zij levert overschrijdingskansen voor zes neerslagdrempels en combineert radarwaarnemingen met een ensembleverwachting.
- De catalogus noemt de dataset `onGoing`, maar de begeleidende tekst noemt haar ook een pilot die kon veranderen of stoppen. De actuele beschikbaarheid moet daarom bij iedere echte validatie worden gecontroleerd.
- De anonieme KNMI Open Data API-sleutel is publiek en geldig tot 1 augustus 2027; het gedeelde quotum maakt haar geschikt voor een persoonlijke proef, niet automatisch voor schaal.

Bronnen: [KNMI datasetcatalogus](https://dataplatform.knmi.nl/dataset/seamless-precipitation-ensemble-forecast-probabilities-1-0) en [KNMI Open Data API](https://developer.dataplatform.knmi.nl/open-data-api).

## Conventional baseline

Een gewone weerapp toont een verwachting of regenkans. Een degelijke technische baseline kiest de nieuwste geldige bron, verwerkt locatie en tijdzone correct, meldt storingen en bewaart genoeg data om prestaties achteraf te meten.

## WijSAmen difference

De nowcast wordt de eerste concrete **Evidence-Preserving Environmental Interface**:

```text
bron → bestand → publicatietijd → bronouderdom → rasterpunt
     → kans per drempel en lead time → latere radarwaarneming
     → foutmaat en geleerde lokale kalibratie
```

De interface mag een eenvoudige conclusie geven, maar iedere conclusie blijft terug te voeren op bron, tijd, onzekerheid en latere verificatie. Bronconflict en ontbrekende data worden getoond, niet stil gladgestreken.

## Potential benefit

- direct praktisch nut voor korte wandelingen, fietsen en buitenwerk;
- een meetbaar leerpad naar lokale kalibratie;
- een herbruikbare provenance- en onzekerheidslaag voor Forest Voice, ecologisch herstel en andere milieudata;
- een echte, effectarme proef voor de bredere WijSAmen-betrouwbaarheidsarchitectuur.

## Key unknown

Levert de combinatie van KNMI-nowcast, bronouderdom en lokale kalibratie aantoonbaar betere beslissingen dan de onbewerkte KNMI-kans of een gangbare weerapp?

## Most likely failure modes

1. De pilotdataset wijzigt of verdwijnt.
2. De nieuwste bestandsnaam is niet hetzelfde als de meteorologisch nieuwste geldige run.
3. Een synthetische test slaagt terwijl de echte NetCDF-dimensies of projectie afwijken.
4. Lokale kalibratie overfit één plek, seizoen of buientype.
5. De interface wekt door nette percentages meer zekerheid dan de data dragen.
6. Exacte locatiehistorie blijft onnodig lang op het toestel staan.
7. Te vaak pollen belast het gedeelde anonieme KNMI-quotum.

## Cheapest reversible evidence-producing cycle

1. Voer `test_core.py` uit en bewaar de exacte uitvoer plus commit-SHA.
2. Open één actuele KNMI-file op Termux met `--diagnose`; bewaar bestandsnaam, retrievaltijd, datasettijd, rasterpunt en dimensies.
3. Maak gedurende een vooraf begrensde periode voorspelsnapshots zonder de parameters tussentijds te veranderen.
4. Koppel iedere voorspelling aan RTCOR-5m-waarnemingen.
5. Rapporteer per lead time en drempel: Brier score, reliability, regen-start/stopfout, bronouderdom en uitval.
6. Vergelijk met minimaal één vooraf gekozen baseline: de ruwe laagste-drempelkans zonder lokale correctie.

## Disconfirming evidence

Parkeer of herontwerp wanneer echte files structureel niet betrouwbaar openen, de bron te vaak te oud/afwezig is, de gekalibreerde variant buiten de trainingsperiode niet beter presteert dan de vooraf gekozen baseline, of bruikbare communicatie alleen mogelijk blijkt door onzekerheid te verbergen.

## Dependencies and boundaries

- KNMI Data Platform en veranderlijke pilotdataset;
- Termux/Android, netwerk en optionele locatiepermissie;
- RTCOR-5m of een andere onafhankelijke waarnemingsbron voor verificatie;
- geen betaalde dienst, externe boodschap of publicatie nodig voor de eerste cyclus;
- geen exacte GPS-logs committen; voeg vóór breder gebruik bewaartermijn en lokale verwijdering toe.

## Portfolio priority

**NOW/P1–P2 — EMBEDDED REALIZATION PROOF.** Dit vraagt nu geen extra gepland agentslot: de gebruiker is al actief met het prototype en GitHub bewaart de uitvoering. Als de live-filevalidatie slaagt, is dit de beste eerste praktische drager van de Evidence-Preserving Environmental Interface; de ecologische restauratievariant blijft de tweede toepassing.
