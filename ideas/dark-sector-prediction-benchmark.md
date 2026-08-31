# Dark-sector prediction benchmark

## Doel
Test of een toekomstige WijSAmen 0veld/geometrie/gravity-hypothese zelfstandig dezelfde waarnemingen kan voorspellen die in het standaard kosmologische model vooral aan dark matter (en op kosmologische schaal dark energy) worden toegeschreven.

Dit dossier is GEEN claim dat dark matter of dark energy niet bestaan. Het is een falsificatieprogramma: een alternatief model krijgt pas betekenis wanneer het vooraf meerdere onafhankelijke datasets voorspelt met minder of minstens vergelijkbare vrije parameters en zonder per systeem opnieuw af te stemmen.

## Belangrijkste regel
Eerst een expliciete effectieve wet/actie afleiden. Daarna parameters op een beperkte trainingsset vastleggen. Vervolgens voorspellingen maken op data die niet voor de fit zijn gebruikt.

Een fit is geen voorspelling.

## Gate D0 — minimale theorie-eis
Voor observatietesten moet een kandidaatmodel ten minste leveren:
- een potentiaal/metric of veldvergelijking;
- een Newtoniaanse/GR-limiet bij bekende regimes;
- een duidelijke bronterm: welke baryonische/veld/gauge/topologische grootheden veroorzaken het effect?;
- behoudswetten en dimensies;
- maximaal een klein aantal universele parameters;
- een lensing-voorspelling, niet alleen een krachtwet voor massieve deeltjes.

Zonder deze onderdelen kunnen astronomische data hooguit helpen om een gewenste phenomenologische vorm te ontdekken; zij bewijzen het 0veld-spoor dan niet.

## Benchmark ladder

### B1 — SPARC galaxy rotation curves
Public dataset met 175 schijfstelsels, rotatiecurves en baryonische massamodellen.

Input voor model:
- gasdistribution;
- stellar disk/bulge contribution;
- afstand/inclinatie met gepubliceerde onzekerheden.

Output die vooraf voorspeld moet worden:
- g_pred(r) of v_pred(r) voor elk meetpunt.

Hard criterium:
- universele parameters worden niet per galaxy opnieuw gekozen;
- train/test split: bijvoorbeeld 20% voor kalibratie, 80% blind/predictief;
- vergelijk likelihood/BIC/AIC en out-of-sample residuals met baryons-only Newton, een standaard halo-baseline en een MOND/RAR-baseline.

Dit is de eerste praktische benchmark omdat de data openbaar en relatief beheersbaar zijn.

### B2 — radial acceleration relation / baryonic Tully-Fisher
Een kandidaatwet moet niet alleen individuele curves passen, maar de gezamenlijke scaling-relaties voorspellen:
- g_obs versus g_bar;
- asymptotische snelheid versus baryonische massa;
- scatter en eventuele afhankelijkheid van surface density.

Een ad-hoc fit van elke rotation curve afzonderlijk telt niet.

### B3 — local low-acceleration control: Gaia wide binaries
Doel: onderscheid maken tussen "extra graviterende massa op galactische schaal" en "de zwaartekrachtswet verandert bij lage versnelling".

Dark matter hoort binnen een wijde dubbelster op Solar-Neighbourhood schaal normaal geen grote interne snelheidsboost te veroorzaken; low-acceleration modified-gravity models kunnen dat wel.

Deze benchmark is momenteel controversieel: verschillende Gaia DR3 analyses trekken tegengestelde conclusies. Daarom alleen gebruiken met vooraf vastgelegde kwaliteitscuts en meerdere published pipelines.

### B4 — galaxy/cluster gravitational lensing
Een theorie die alleen sterrenrotaties voorspelt is onvoldoende. Licht moet dezelfde metric consistent voelen.

Test:
- galaxy-galaxy lensing;
- strong lensing;
- cluster weak/strong lens-mass maps.

Kernvraag:
Kan de metric afgeleid uit baryonen + kandidaatcorrectie tegelijk dynamics EN lensing voorspellen?

### B5 — merging clusters / Bullet Cluster class
Botsende clusters zijn een belangrijke discriminant omdat de hete baryonische gascomponent, galaxies en lensing-derived mass peaks ruimtelijk uit elkaar kunnen liggen.

Een alternatief zonder particle dark matter moet vooraf voorspellen waar de lensing potential tijdens/na een collision hoort te liggen en hoe groot die is.

Geen succes als achteraf onzichtbare baryonen of extra parameters per cluster worden toegevoegd zonder onafhankelijke voorspelling.

### B6 — CMB acoustic spectrum
Zeer zware gate.

Een serieus alternatief voor cosmological cold dark matter moet de vroege-Universe perturbatie-evolutie en daarmee TT/TE/EE acoustic peaks, lensing en baryon density consistent voorspellen.

Dit vereist een relativistische cosmological implementation (bijv. gewijzigde Einstein-Boltzmann equations / CLASS- of CAMB-achtige solver). Een model dat alleen galaxy rotation curves verklaart heeft dark matter niet vervangen.

### B7 — growth of structure / weak lensing
Test late-time matter clustering, S8/f_sigma8-achtige observables, cluster abundance en cosmic shear.

De 2026 S8-literatuur is nog niet volledig eensluidend tussen late-time surveys, dus modelselectie moet meerdere probes gebruiken en systematics expliciet meenemen.

## Twee-richtingenstrategie
### Route 1 — theory first
Afleiden van een concrete action/field equation uit het zero-boundary/geometric spoor en daarna zonder aanpassing door B1-B7 sturen.

Dit is de wetenschappelijk sterkste route.

### Route 2 — phenomenology first
Gebruik B1/B2 om te bepalen welk soort universele extra acceleratie/metric correction de data minimaal vereisen. Daarna proberen die functionele vorm UIT de 0veld/geometric constructie af te leiden.

Deze route is nuttig voor ontdekking, maar mag niet als bewijs voor 0veld worden gepresenteerd totdat de afleiding onafhankelijk bestaat en nieuwe data voorspelt.

## Eerste concrete challenge
### Dark Prediction Challenge v0.1
1. Download SPARC mass-model data.
2. Implementeer drie baselines:
   - Newton baryons-only;
   - standaard dark-halo fit;
   - MOND/RAR-style low-acceleration baseline.
3. Maak een vaste train/test split vóór modelontwikkeling.
4. Ontwikkel nog GEEN vrije 0veld-fit per galaxy.
5. Leid of parameteriseer één universele WijSAmen correction met maximaal 1-2 nieuwe universele parameters.
6. Fit alleen de trainingssubset.
7. Freeze parameters.
8. Voorspel de testgalaxies blind.
9. Publiceer residuals en failure cases net zo zichtbaar als successes.

## Wat als het model wint?
Een goede SPARC-score betekent alleen dat het galaxy-scale phenomenology verdient om verder te testen. Volgende verplichte gate is lensing/local-control; daarna clusters; pas daarna cosmology.

## Wat als het model verliest?
Dat is informatief:
- verkeerde functional form;
- 0veld heeft geen gravity consequence;
- effect bestaat alleen in een ander regime;
- dark matter blijft de betere verklaring.

Het magnetische field-shaping, fiber-feedback en many-body tracks worden hierdoor niet aangetast.

## Reality anchors
- SPARC database: 175 late-type galaxies with rotation curves and baryonic mass models.
- Planck legacy: Lambda-CDM remains an excellent fit to CMB temperature/polarization/lensing and strongly constrains non-baryonic matter content.
- Merging clusters remain powerful tests because collisional gas and collisionless/lensing components can spatially separate.
- Gaia wide-binary low-acceleration tests remain methodologically disputed; use as discriminant, not sole arbiter.

## Besluitlog
- 2026-08-31 — Dark-sector benchmark created. Goal changed from "explain dark matter" to "force any candidate WijSAmen gravity model to make cross-scale, out-of-sample predictions against the observations usually modeled with dark matter".
