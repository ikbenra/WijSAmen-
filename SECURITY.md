# Veiligheid en privacy

Deze repository mag kennis bewaren, maar geen geheimen of onnodig gevoelige persoonsgegevens.

## Nooit committen

- wachtwoorden, passkeys, herstelcodes of toegangstokens;
- API-sleutels, privésleutels of volledige configuratiebestanden met geheimen;
- medische dossiers, identiteitsdocumenten of adressen;
- privéberichten of persoonsgegevens van anderen zonder duidelijke noodzaak en toestemming.

## Bij een mogelijk lek

1. Deel het geheim niet opnieuw in een issue of commit.
2. Trek het betrokken wachtwoord, token of sleutel onmiddellijk in.
3. Maak een nieuw geheim aan.
4. Verwijder het lek zorgvuldig uit de geschiedenis als dat nodig is.
5. Noteer alleen de herstelactie, niet het geheim zelf.

## Technische experimenten

Leg vooraf de veiligheidsgrens, stopvoorwaarde en verwachte waarneming vast. Experimenten die mensen, dieren, infrastructuur, accounts of onvervangbare gegevens kunnen schaden worden niet zonder passende deskundigheid en beheersmaatregelen uitgevoerd.

## Misbruikbestendig ontwerpen

Bij nieuwe projectfuncties hoort vóór uitvoering een korte misbruik- en hersteltoets:

- geef iedere component alleen de minimaal noodzakelijke bevoegdheid;
- scheid voorbereiden, simuleren, uitvoeren en extern verzenden als afzonderlijke staten;
- leg bron, actor, toestemming, uitvoering, fout en rollback controleerbaar vast;
- ontwerp veilige standaardinstellingen, begrensde invoer en een duidelijke stopmogelijkheid;
- test ten minste één plausibel misbruikscenario en één fout- of herstelpad;
- bewaar geen gevoelige gegevens alleen omdat dat technisch mogelijk is;
- laat onzekere of onbevoegde acties eindigen in `ABSTAIN / NOT_EXECUTED`;
- maak geen functie breder of autonomer voordat de bestaande grens aantoonbaar werkt.

Veiligheidsmaatregelen moeten legitiem nuttig gebruik ondersteunen, terwijl ongewenste bevoegdheidsuitbreiding vroeg zichtbaar en omkeerbaar blijft.
