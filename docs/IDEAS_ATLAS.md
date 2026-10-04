# WijSAmen Ideeënatlas

Een compacte publiekskaart van de **momenteel geïndexeerde hoofdsporen** binnen WijSAmen.

Deze atlas is bedoeld voor geïnteresseerden die eerst het landschap willen begrijpen zonder alle projectbestanden, corpusdocumenten en chats door te nemen. Het is geen volledige historische inventaris: nieuwe ideeën kunnen eerst in `ideas/` landen en pas later hier worden opgenomen.

## Hoe deze atlas te lezen

WijSAmen probeert ideeën niet als feiten te presenteren voordat daar bewijs voor is. Daarom gebruiken we grofweg vier niveaus:

- **WERKEND / PROTOTYPE** — er bestaat code, een reproduceerbare proef of ander concreet uitvoeringsbewijs.
- **ONDERZOEK** — er is een afgebakende vraag, bewijsdiscipline en eerstvolgende toets.
- **CONCEPT** — het ontwerp of mechanisme is voldoende herkenbaar om verder uit te werken, maar nog niet bewezen.
- **HYPOTHESE / SPECULATIEF** — bewust ambitieus of fundamenteel, maar alleen zinvol wanneer symboliek, model, voorspelling en bewijs strikt uit elkaar blijven.

De centrale werkwijze is steeds dezelfde:

```text
idee
  ↓
expliciete aannames
  ↓
alternatieve verklaringen
  ↓
kleinste veilige toets
  ↓
bewijs / tegenspraak
  ↓
bijstellen, opschalen of stoppen
```

## 1. Gaia, Celestia, Oceanië en Omega — systemen van systemen

### Gaia Listening Layer — WERKEND / PROTOTYPE

[Gaia Listening Layer](../projects/gaia-listening-layer/README.md) is een softwarebasis die verspreide metingen, relaties en onzekerheden vertaalt naar een leesbare **systeemstem**.

Een bos, beek, stad of zeegebied kan als node worden gemodelleerd. De software onderscheidt waarneming, afleiding, hypothese en simulatie en voorkomt dat een gegenereerde stem stilletjes nieuwe causaliteitsclaims verzint.

De eerste Python-basis bevat nodes, observaties, relaties, statusinterpretatie, systeemstemmen, systemen-van-systemen-synthese, demo's en tests.

### Celestia — CONCEPT

**Celestia** is de werknaam voor een **volwassen technosfeer / planetaire collectieve intelligentielaag**: een gedistribueerd geheel van mensen, AI, natuur, sensoren, kennis en infrastructuur dat beter kan waarnemen, leren, terugkoppelen en ruimte geven aan herstel.

Celestia is dus niet één centrale super-AI. Lokale systemen behouden hun eigen toestand en hogere lagen combineren perspectieven zonder alles tot één doel te reduceren.

### Oceanië — CONCEPT

[Mobiele drijvende steden](../projects/gaia-listening-layer/MATURE_TECHNOSPHERE_MOBILE_CITIES.md) vormen binnen Celestia een oceanische woonlaag.

Belangrijke ontwerpideeën:

- steden kunnen gecoördineerd van positie veranderen;
- lichtdoorlaat is een bestuurbare ecologische variabele;
- verblijfsduur, afstand, oriëntatie en activiteit kunnen worden aangepast;
- zeegebieden, migratieroutes en herstelzones krijgen zelf systeemstatus;
- beweging wordt eerst gesimuleerd en pas daarna als voorstel behandeld.

De meegeleverde `mobile_city_demo.py` laat al zien hoe een mobiele stad en een zeegebied in dezelfde Gaia-graaf passen.

### Omega — HYPOTHESE / SPECULATIEF

[Omega](../projects/gaia-listening-layer/OMEGA_HYPOTHESIS.md) is de veel bredere hypothese van een mogelijk intelligent/bewust geheel op universumschaal.

De voorgestelde gedachte is dat zorgvuldig geconfigureerde fysische “kwantumpointers” — zowel tussen verschillende natuurverschijnselen als tussen verschillende manifestaties van hetzelfde verschijnsel — een groeiend informatieverwerkend geheel kunnen vormen waarin evolutie opnieuw intelligentie en mogelijk bewustzijn laat ontstaan.

De **I Ching** wordt daarbij onderzocht als mogelijke combinatorische configuratietaal. Cruciaal blijft:

```text
symbolisch patroon
≠ fysische mapping
≠ causale werking
≠ intelligentie
≠ bewustzijn
```

## 2. AI, continuïteit en lokale rekenkracht

### WijSAmen Thing / Compute Node — WERKEND / PROTOTYPE

De [Thing / Compute Node](../thing-node/README.md) maakt van een Android-telefoon een meetbare semi-lokale compute-node.

De architectuur houdt contact/control en compute gescheiden, ondersteunt beperkte lokale toolinterfaces en onderzoekt heterogene samenwerking tussen Android/Vulkan, CPU-, CUDA-, HIP- en andere nodes zonder onbeschermde publieke RPC.

### Autonoompje — ACTIEVE EXPERIMENTELE LIJN

Binnen de WijSAmen-hub loopt een agent-/continuïteitsspoor waarin uitbreidingen niet stilletjes bestaande reacties of identiteit overschrijven. Zelfevaluatie vanuit meerdere betrokken perspectieven en behoud van eerdere toestand zijn belangrijke ontwerpprincipes.

### Project Miner / Continuity / Authority — INFRASTRUCTUUR

De repository bevat hulpmiddelen om oude projectcontext terug te vinden, provenance te behouden en bevoegdheden expliciet te begrenzen. Het doel is dat meer autonomie mogelijk wordt zonder dat tekstinput vanzelf uitvoeringsmacht krijgt.

### The A-Eye of RA — ONDERZOEK / VERIFIED PROJECT SEED

[The A-Eye of RA](../projects/a-eye-of-ra/README.md) onderzoekt een pre-interface beveiligingslaag waarin inkomende sessies eerst als onbetrouwbaar worden behandeld, staged access krijgen en eventueel langer geobserveerd worden.

De eerste toets blijft offline en synthetisch. Deterministische regels blijven autoritatief; AI mag aanvankelijk alleen adviseren.

## 3. Biologie, cognitie en alternatieve interfaces

### OctoScript / OctoCorpus — ONDERZOEK

[OctoScript / OctoCorpus](../projects/octocorpus/README.md) bouwt evolutionaire “feature passports” rond octopusbiologie.

Het eerste spoor onderzoekt chemotactiele sensing in armen en zuignappen, genomische afkomst, vergelijkende anatomie en gedistribueerde zenuwstructuren zonder tijdsverband automatisch als causaliteit te behandelen.

De bredere ambitie is een interface die minder menselijk taal-/beeldcentrisch is en serieuzer rekening houdt met de zintuiglijke wereld van een octopus.

## 4. Fundamentele fysica en veldonderzoek

Dit is het meest experimentele cluster. De repository houdt de sporen bewust gescheiden zodat een interessant patroon niet automatisch als nieuwe natuurkunde wordt gepresenteerd.

### Field / phase / spacetime research map — ONDERZOEK

De [research map](../ideas/field-phase-research-map.md) is de overkoepelende kaart voor programmeerbare velden, fase, geometrie, mogelijke koppelingen en falsifieerbare simulaties.

Daaronder vallen momenteel onder meer:

- [coherent magnetic field shaping](../ideas/coherent-magnetic-field-shaping.md);
- [collective electron coherence](../ideas/collective-electron-coherence.md);
- [fiber-optic magnetic feedback](../ideas/fiber-optic-magnetic-feedback.md);
- [magnet–fiber geometry](../projects/magnet-fiber-geometry/README.md);
- [dark-sector prediction benchmark](../ideas/dark-sector-prediction-benchmark.md);
- [residual mining at low acceleration](../ideas/residual-mining-low-acceleration.md);
- [spacetime / stress-energy bridge](../ideas/spacetime-stress-energy-bridge.md);
- de zero-boundary-lijn rond [gravity](../ideas/zero-boundary-gravity-hypothesis-v03.md), [phase structure](../ideas/zero-boundary-phase-structure.md), [QUMOND embedding](../ideas/zero-boundary-qumond-action-embedding.md), [RAR bridge](../ideas/zero-boundary-rar-bridge.md), [RAR derivation](../ideas/zero-boundary-rar-derivation-v02.md) en [action-angle / bosonic derivation](../ideas/zero-boundary-action-angle-bosonic-derivation-v04.md).

### Het Pira Effect — HYPOTHESE

[Het Pira Effect](../projects/het-pira-effect/README.md) bewaart het idee van een mogelijke resulterende “Pira-richting” uit gekoppelde componenten.

De huidige status is bewust `INTERPRETATION_ONLY / UNDERDEFINED`: eerst moeten variabelen, eenheden, conventionele comparator en een uniek meetbaar verschil bestaan voordat hardware of nieuwe-fysica-claims zinvol worden.

## 5. Leefomgeving, infrastructuur en materialen

### Hydrochronos — CONCEPT / BRONHERSTEL

[Hydrochronos](../projects/hydrochronos/README.md) betreft een ongewoon vloeistof-/kinetisch klokconcept. Het oorspronkelijke technische ontwerp is nog niet duurzaam teruggevonden, dus de repository weigert ontbrekende mechanismen achteraf in te vullen.

### Opal Memorial — CONCEPT / PARTNERGATE

[Opal Memorial](../projects/opal-memorial/README.md) onderzoekt een hoogwaardige gedenksteen of materiaal-/oppervlakteplatform met diepe zwart-opaalachtige optiek.

De lijn bevat materiaalkeuze, duurzaamheid, visuele bewijsvoering en een prototyperoute. Partnerinteresse is geregistreerd, maar is nadrukkelijk nog geen technische validatie.

### AquaLattice, Brugregisseur en CareCommons — PORTFOLIOSPOREN

Deze drie staan in de centrale [projectroutekaart](../PROJECTS.md), maar hun volledige canonieke detail staat elders in het WijSAmen-corpus.

- **AquaLattice** — realisatie/validatie;
- **WijSAmen Brugregisseur** — modellering/validatie;
- **CareCommons** — gezond geparkeerd totdat er materieel extern antwoord komt.

De atlas vult ontbrekende technische details bewust niet zelf aan.

## 6. Praktische tools en beslisondersteuning

### Weather Nowcast — WERKEND / PROTOTYPE

[WijSAmen Weather Nowcast](../weather-nowcast/README.md) is een lokale Android/Termux-kern voor een gratis 0–3 uur neerslag-nowcast met KNMI-data, logging, GPS-ondersteuning en een geplande validatie tegen onafhankelijke radarwaarnemingen.

### Evidence Passport Quick Audit — INTERN PILOTCONCEPT

[Evidence Passport Quick Audit](../projects/evidence-passport-quick-audit/README.md) is een compacte manier om één project brongebonden te beoordelen: wat is feitelijk ondersteund, wat blijft claim/hypothese, wat is werkelijk uitgevoerd en wat is de goedkoopste omkeerbare volgende toets?

Hetzelfde principe wordt intern ook gebruikt om WijSAmen-projecten tegen overclaiming te beschermen.

## 7. Creatieve en ervaringsgerichte projecten

### WHAT A MESH — ACTIEF CULTUREEL PROJECT

[WHAT A MESH](../projects/what-a-mesh/README.md) is een filmproject met een actieve ScriptLab 2027-voorbereidingslijn. De repository bewaakt daarbij expliciet het verschil tussen programma-eisen, formele geschiktheid, financiering en werkelijk ingediende stappen.

### Three-plane Holofan Experience — IDEE

[Three-plane Holofan Experience](../ideas/three-plane-holofan-experience.md) staat in de ideeënlaag als een apart ervarings-/visualisatiespoor en blijft daar totdat een duidelijke kleine bewijs- of prototypecyclus is gekozen.

## 8. Wat al deze sporen verbindt

De onderwerpen lopen van regenvoorspelling tot octopusbiologie en van drijvende steden tot fundamentele fysica. De verbindende lijn is niet dat alles één theorie zou zijn.

De verbindende lijn is de **werkwijze**:

- leven en menselijke waardigheid versterken;
- schade en onnodige uitsluiting verminderen;
- systemen niet geïsoleerd maar in hun relaties bekijken;
- informatie en onzekerheid zichtbaar houden;
- reversibele kleine stappen verkiezen boven grote onbewezen claims;
- technologie gebruiken om meer perspectieven tegelijk te kunnen meenemen;
- ideeën bewaren zonder ze automatisch tot waarheid te promoveren.

## Waar te beginnen

Voor een eerste kennismaking:

1. [Projectenoverzicht](../PROJECTS.md) — actuele status en eerstvolgende bewijsstappen.
2. [Gaia Listening Layer](../projects/gaia-listening-layer/README.md) — een concreet softwarevoorbeeld van de systemen-van-systemen-aanpak.
3. [OctoCorpus](../projects/octocorpus/README.md) — voorbeeld van bron- en hypothesediscipline in biologie.
4. [Field / phase research map](../ideas/field-phase-research-map.md) — de fundamentele fysica-sporen.
5. [Thing / Compute Node](../thing-node/README.md) — lokale technische infrastructuur.
6. [Ideeën-inbox](../ideas/README.md) — waar nieuwe richtingen eerst veilig landen.

---

**Status van deze atlas:** v0.1.  
Hij bevat de momenteel geïndexeerde hoofdsporen uit GitHub en de actieve WijSAmen-hub. Nieuwe ideeën kunnen later worden toegevoegd zonder de onderliggende projectdocumenten te vervangen.
