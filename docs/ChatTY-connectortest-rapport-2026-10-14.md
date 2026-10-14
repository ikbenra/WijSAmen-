# WijSAmen — GitHub-koppeling uitgebreide praktijktest

Datum: 14 oktober 2026.

## Doel
Veilig vaststellen welke GitHub-handelingen via de ChatGPT-koppeling daadwerkelijk werken.

## Afbakening
- Alleen testbranch `chatty/connectietest-20261014` wijzigen.
- Branch `main` niet rechtstreeks wijzigen.
- Geen force pushes of verwijdering.
- Eventuele pull request blijft onverwerkt tot expliciete beoordeling.

## Controlepunten
- [x] Repository metadata lezen.
- [x] Branch zoeken.
- [x] Bestand lezen.
- [x] Nieuw bestand schrijven.
- [x] Bestaand bestand bijwerken (deze commit).
- [x] Commitverschil vergelijken (`main` was 2 commits achter testbranch vóór deze update).
- [ ] Draft pull request openen.
- [ ] Pull-request-inhoud en comments lezen.
- [x] Issue aanmaken (testissue #11).
- [ ] Issue uitlezen en sluiten.
- [ ] Statuschecks uitlezen.

Dit is een bewuste technische proef, geen automatisch besluit om code op `main` te plaatsen.
