# Opal Memorial — technical route matrix v0.1

## Provenance en status

- Datum: 12 september 2026.
- Aanleiding: geverifieerde Luciform3D-partneropening en het nog niet verzonden conceptantwoord in [PARTNER_GATE_LUCIFORM3D.md](./PARTNER_GATE_LUCIFORM3D.md).
- Ontwerpbron: [DESIGN_INTENT_V01.md](./DESIGN_INTENT_V01.md).
- Strategische grens: [PLATFORM_BOUNDARY_V01.md](./PLATFORM_BOUNDARY_V01.md).
- Status: `SOURCE_SUPPORTED_BASELINE / PROTOTYPE_SPEC_PREPARED / NOT_FABRICATED`.
- Dit document bewijst geen maakbaarheid, nieuwheid, octrooieerbaarheid, buitenbestendigheid, partnerprijs of klantvraag.

## Beslissende decompositie

Het eerste prototype hoeft niet tegelijk de uiteindelijke steen, de definitieve opaalarchitectuur en buitenbestendigheid te bewijzen. De snelste leerroute splitst het probleem in twee gekoppelde vragen:

1. **Drager- en dieptebewijs:** kan een transparant onderdeel lokale, scherp begrensde letters/inlays op verschillende dieptes zichtbaar houden?
2. **Optisch-effectbewijs:** welke inlay leest in dezelfde geometrie als één samenhangend opaalachtig lichaam in plaats van gekleurd kunststof met losse glitter?

Deze splitsing voorkomt dat slechte transparantie ten onrechte een optisch materiaal afwijst, of dat een mooi los materiaalmonster wordt aangezien voor bewijs dat integratie in een product lukt.

## Conventionele technische baseline

- SLA/MSLA met heldere resin kan transparante, fijn gedetailleerde prototypes maken, maar zichtbare laaglijnen, krasjes en gele verkleuring kunnen het resultaat bepalen. Schuren/polijsten, een dunne resin-coat of geschikte clearcoat verbeteren helderheid; complexe geometrie is lastiger volledig optisch helder af te werken.
- PolyJet heeft bijna kleurloze transparante materialen die PMMA simuleren. Stratasys vermeldt voor VeroUltraClear circa 95% lichttransmissie ten opzichte van PMMA en positioneert deze materialen voor vorm-/passingtests van heldere onderdelen.
- Transparante of gekleurde multi-material printing kan diepte en vorm demonstreren. Een gekleurde transparante inlay is echter geen opalisering en telt alleen als geometrische controle.
- Off-the-shelf dichroïsche polyesterfilm levert een sterke kijkhoekafhankelijke kleurwisseling met lichttransmissie. Het aangehaalde 3M-product is bedoeld voor interieurglas en heeft volgens 3M een levensduur tot vijf jaar; het is daarom bruikbaar als proof-of-look-referentie, niet als onbewezen buitenoplossing.
- Interferentie-/parelmoerpigmenten kunnen in een transparante binder een kleur-/glanseffect geven. Grove mica-effectpigmenten geven juist zichtbare shimmer; dat maakt ze een nuttige maar strenge test van Remco's hypothese dat zeer dicht opeengepakte microflitsen als één grote flits kunnen lezen.
- Polymer-opal photonic-crystal films zijn in onderzoek aangetoond met instelbare structurele kleur, grotere kijkhoekspreiding en industrieel schaalbare filmproductie. Selectieve micro-imprinting kan lokale kleurpatronen maken. Dat ondersteunt technische plausibiliteit op materiaalniveau, maar niet dat Luciform3D deze route bezit, dat zij goedkoop verkrijgbaar is, of dat zij in een transparante 3D-print buitenbestendig integreert.

## Routevergelijking

| Route | Wat zij werkelijk test | Verwachte kracht | Belangrijkste faalroute | Maturiteit voor eerste coupon | Prioriteit |
|---|---|---|---|---|---|
| A. Dunne dichroïsche film/inlay achter transparante cover | diepte, contour, continue kleurshift en integratie | grootste kans op één coherente flits; goedkoop en omkeerbaar | oogt als folie, seam/delaminatie, te directioneel; aangehaalde film is interieurmateriaal | commercieel beschikbaar als visuele referentie | **TEST EERST** |
| B. Hoge dichtheid transparant interferentiepigment in heldere binder | samengestelde-microflitshypothese en gevormde letters | dichter bij verspreide opaalachtige materie; eenvoudig lokaal doseerbaar | leest als glitter, bezinkt/orienteert slecht, waas/bellen, bindercompatibiliteit | gangbare componenten, proces nog te bepalen | **TEST NAAST A** |
| C. Selectief gevormde polymer-opal film | echte structurele kleur en lokale patroonvorming | inhoudelijk sterkste opaalroute; kleur zonder conventioneel pigment | specialistische film/processen, sourcing en integratie onbekend | onderzoek/gespecialiseerde productie | **RESERVE / WATCH** |
| D. Gekleurde transparante of gematteerde printzone | alleen leesbaarheid, diepte en fabricagecontrole | goedkoop referentiepunt | kan visueel aantrekkelijk lijken maar bewijst geen opalisering | gangbaar prototypeproces | **NEGATIEVE CONTROLE** |

## Voorgestelde Luciform-coupon

`PREPARED_SPEC / DIMENSIONS_TO_BE_CONFIRMED_BY_FABRICATOR`

Begin met één vlak transparant paneel in een orde van grootte van circa 90 × 60 × 6–10 mm. Luciform3D mag deze buitenmaten aanpassen aan de goedkoopste betrouwbare print- en nabewerkingsroute; de vergelijkingslogica moet gelijk blijven.

### Geometrie

Gebruik één identieke, eenvoudig leesbare vorm met zowel rechte als gebogen randen — bijvoorbeeld een hoofdletter `R` — in acht zones:

- drie dieptes voor route A;
- dezelfde drie dieptes voor route B;
- één kleurloze/lege transparantiecontrole;
- één gelijkmatig gekleurde of gematteerde geometriecontrole.

Laat Luciform3D de drie werkelijke coverdieptes kiezen op basis van minimale wanddikte, resolutie en nabewerking, maar houd de actieve vorm, het zichtbare oppervlak en de belichting tussen routes gelijk. Gebruik een verwijderbare matzwarte en witte achterplaat zodat contrast niet met materiaalprestatie wordt verward.

### Optische routes

- **A:** identieke uitgesneden dichroïsche film of vergelijkbaar continu interference-element, vlak en zonder digitale nabewerking.
- **B:** hetzelfde volume gevuld met een heldere compatibele binder en één vooraf gemengde hoge dichtheid van iriserende/interferentieplaatjes. Begin niet met meerdere geheime recepturen; deze coupon vraagt alleen of de samengestelde flits überhaupt samenhangend kan lezen.
- **Controles:** helder leeg en gekleurd/gematteerd, zodat opalisering niet wordt verward met gewone kleur of verstrooiing.

### Vast opnameprotocol

Leg iedere zone met dezelfde telefoon, focus, witbalans, afstand en belichting vast:

1. diffuus daglicht bij 0°, 30° en 60°;
2. één puntlicht bij dezelfde drie kijkhoeken;
3. zwarte en witte achterplaat;
4. één korte ononderbroken camerabeweging zonder verzadigings-, glow- of lokale contrastversterking;
5. één beeld op normale kijkafstand en één macro-opname.

Bewaar de ruwe bestanden. De macro-opname mag het mechanisme tonen, maar mag een mislukking op normale kijkafstand niet redden.

## Vooraf vastgelegde succescriteria

De coupon gaat alleen door naar een uitgebreidere A5-lintproef wanneer:

- de vorm op minstens twee dieptes onder diffuus daglicht leesbaar blijft;
- ten minste één actieve route op normale kijkafstand als samenhangende kleurflits leest, niet als effen kleur of losse glitter;
- het effect bij meer dan één kijkhoek bestaat;
- transparantie en diepte zichtbaar blijven zonder dat bellen, naden of waas domineren;
- route A en B met identieke opname-instellingen eerlijk te vergelijken zijn;
- Luciform3D vóór fabricage materiaal, nabewerking, prijsband en doorlooptijd kan specificeren.

## Stop-/herontwerpcriteria

- alleen één exacte puntlicht-/kijkhoek produceert een overtuigende flits;
- alleen de macro-opname oogt opaalachtig;
- pigmentroute B valt uiteen in zichtbare losse deeltjes of maakt de drager melkachtig;
- filmroute A leest uitsluitend als opgeplakte folie of vertoont storende naden;
- diepte veroorzaakt zoveel waas/vervorming dat letters niet reproduceerbaar leesbaar zijn;
- een betaalde fabricage wordt gevraagd zonder vast ontwerpbestand, materiaalomschrijving, kostenband of acceptatiecriteria;
- brede technische disclosure, exclusiviteit of IP-overdracht wordt voor deze eenvoudige coupon verlangd.

Een mislukking van A verwerpt B of C niet; een mislukking van B verwerpt continue-film- of polymer-opalroutes niet. De test is route-discriminerend, geen alles-of-niets-uitspraak over het platform.

## Wat Luciform3D als eerste moet beantwoorden

1. Welk printproces en transparant materiaal zouden zij voor deze vlakke coupon kiezen?
2. Kunnen inlays tijdens het printen worden geïntegreerd, of is een tweedelige drager/latere insluiting betrouwbaarder?
3. Welke drie coverdieptes en minimale featuremaat zijn zonder onnodige meerkosten haalbaar?
4. Welke nabewerking is nodig om beide zijden vergelijkbaar helder te krijgen?
5. Zijn film, pigment/binder en lege controle in één drager te combineren zonder de vergelijking te vervormen?
6. Wat zijn vóór uitvoering de prijsband, doorlooptijd, aantal onderdelen en leverbare ruwe bestanden/foto's?
7. Welke eenvoudige proef zouden zij zelf schrappen of toevoegen om sneller een duidelijke NO-GO te kunnen vinden?

## Portfoliobesluit

**Voorkeursroute voor eerste partnerproef:** A naast B in één gedeelde transparante geometrie.

**Reserve:** C pas onderzoeken wanneer route A bewijst dat een continue structurele-kleurlaag het gewenste visuele lichaam benadert, of wanneer een concrete leverancier/sample beschikbaar komt.

**Geen bewijsroute:** D blijft controle. Een fraaie gekleurde transparante letter mag niet als opaalvalidatie worden gerapporteerd.

Deze volgorde maximaliseert informatiewinst per euro: dezelfde coupon scheidt geometrie/diepte, continue kleurshift en de microflitshypothese zonder een eindproduct te bestellen.

## Bronnen

- Formlabs, *Guide to Transparent 3D Printing*, geraadpleegd 12 september 2026: <https://formlabs.com/blog/3d-printing-transparent-parts-techniques-for-finishing-clear-resin/>
- Stratasys Support, *Transparent 3D Printing Materials*, geraadpleegd 12 september 2026: <https://support.stratasys.com/en/Materials/PolyJet/Transparent>
- Stratasys, *PolyJet Materials*, geraadpleegd 12 september 2026: <https://www.stratasys.com/en/materials/materials-catalog/polyjet-materials/>
- 3M, *Dichroic Glass Finishes*, geraadpleegd 12 september 2026: <https://www.3m.co.uk/3M/en_GB/p/d/b5005018063/>
- Pursiainen et al., “Nanoparticle-tuned structural color from polymer opals,” *Optics Express* 15(15), 2007: <https://doi.org/10.1364/OE.15.009553>
- Zhang et al., “Selectively Patterning Polymer Opal Films via Microimprint Lithography,” 2015: <https://pmc.ncbi.nlm.nih.gov/articles/PMC4497474/>
- Merck/Susonity, Iriodin 163 mica-based pearl-effect pigment product information, geraadpleegd 12 september 2026: <https://surface-portal.merckgroup.com/>
