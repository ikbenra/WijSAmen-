# WijSAmen — The Third Possibility / De derde mogelijkheid

**Status: experimenteel prototype, met uitsluitend fictieve gegevens.** De demonstratie bewijst geen maatschappelijke uitkomst.

> Bescherm het grotere geheel zonder automatisch de mogelijkheden van individuen weg te nemen. Onderzoek eerst of een nieuwe systeeminrichting beide belangen kan versterken.

## Voor wie

- **Beleidsmakers en instellingen:** is de keuze tussen algemeen belang en individuele ruimte werkelijk onvermijdelijk?
- **Natuurbeschermers en maatschappelijke organisaties:** wat als ecologie, toegankelijkheid en wederzijds vertrouwen tegelijk kunnen verbeteren?
- **Ingenieurs en AI-onderzoekers:** welke ontbrekende functie kunnen we via een ander mechanisme realiseren?
- **Rechters, zorgprofessionals en belangenbehartigers:** een methode om beter onderbouwde alternatieven te bespreken; niet een klinische of juridische beslismachine.

## De demonstratie

In een **volledig verzonnen** natuurbeschermingscasus vergelijken we: afsluiten, niets wijzigen, gezamenlijk ontwerpen en een technisch onrealistische ideale oplossing. De getallen zijn didactisch gekozen: zij zijn **geen** veldmetingen of voorspellingen.

De evaluator werkt met onzekerheidsintervallen voor publiek nut, autonomie, schade, hulpbronnenkosten en uitvoerbaarheid. Eerst toetst hij harde vereisten en een afzonderlijk opgegeven rechtenvoorwaarde. Daarna geldt A uitsluitend als *robuust beter* dan B wanneer de slechtste uitkomst van A op ieder van vier doelcriteria minstens de beste van B haalt, en op één criterium strikt beter is. Technische uitvoerbaarheid blijft een expliciete haalbaarheidspoort; zij kan niet worden 'weggekocht' door aantrekkelijke scores.

**Resultaat van deze fictieve invoer:** `samen_ontwerpen` is robuust beter dan `afsluiten` op publiek nut, autonomie, schade en kosten. `niets_wijzigen` schiet tekort op publiek nut. `hypothetisch_perfect` wordt afgewezen wegens onvoldoende uitvoerbaarheid. Bij een verslechterde aanname over publiek nut valt de conclusie weg — bewust een falsificatietest.

## Zelf uitvoeren (Python 3, geen dependencies)

```sh
cd projects/third-possibility
python third_possibility.py scenario_fictional.json
python -m unittest -v test_third_possibility.py
```

## Werkwijze: liefde aan logica toevoegen

1. **Doel en context:** maak het publieke doel, alle betrokken perspectieven en bestaande schade concreet.
2. **Functionele completering:** ontwerp de ontbrekende functie desnoods eerst hypothetisch; vraag daarna hoe techniek, organisatie of samenwerking die functie werkelijk kan leveren.
3. **Meerledige versterking:** zoek opties die meerdere belangen tegelijk verbeteren in plaats van nadelen te verplaatsen.
4. **Bewijsdiscipline:** onderscheid feiten, herinneringen, verklaringen, hypotheses en onbekenden; onderzoek onafhankelijke tegenargumenten.
5. **Vrijwilligheid en grenzen:** vrijwillige offers mogen niet worden afgedwongen. Begrip voor schade betekent geen toestemming voor nieuwe schade.
6. **Klein, herstelbaar experiment:** verzamel echte gegevens, documenteer ook mislukkingen en besluit nooit automatisch op basis van dit prototype.

## Grenzen en toepassingsvoorwaarden

- Dit instrument profileert geen individuen, reconstrueert geen geheime motieven, analyseert geen vertrouwelijke dossiers en is niet geschikt voor autonome juridische, zorg- of veiligheidsbesluiten.
- Het booleaanse veld `rights_compatible` is een menselijke externe input, geen automatische juridische beoordeling.
- Robuuste dominantie van *verzonnen getallen* zegt niets over de werkelijke haalbaarheid. Voor echt gebruik zijn meetbare uitkomsten, onafhankelijke toetsing, betrokkenenparticipatie, causaliteitsonderzoek en bevoegd toezicht noodzakelijk.
- Leg nooit iemands persoonlijke veiligheid op de weegschaal van een geaggregeerde score.

## WijSAmen-infrastructuur

Koppel toekomstige pilots aan [Evidence Passport Quick Audit](../evidence-passport-quick-audit/README.md), de Notion Ideeënatlas en de Continuity Stack. Status: **WERKEND/PROTOTYPE voor de code, HYPOTHESE voor echte effecten**. Deel pas na controle van privacy, intellectueel eigendom en publicatierechten.

## Kennisankers (geen validatie van de fictieve cijfers)

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework): toetsbaarheid, transparantie, verantwoord ontwerp.
- [WHO, person-centred rights-based community mental health guidance](https://www.who.int/publications/i/item/9789240025707): waardigheid en rechten.
- [OECD, Trust in Government](https://www.oecd.org/en/topics/trust-in-government.html): vertrouwen en openheid.

**WijSAmen creëert nieuwe mogelijkheden; het probeert geen overtuigingen op te leggen.**
