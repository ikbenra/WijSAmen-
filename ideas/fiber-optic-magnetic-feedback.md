# Fiber-optic magnetic sensing and feedback

## Kern
Gebruik optische vezels als gedistribueerde, elektromagnetisch robuuste meetlaag rond een magnetisch veldvormingsapparaat. Dit spoor komt voort uit eerdere WijSAmen-ideeën met spiraal-/lusvormige glasvezels van verschillende diameters rond geometrisch gerangschikte magneten of spoelen, waarbij fase, polarisatie, Faraday-rotatie, interferometrie of fiber Bragg gratings (FBG) informatie over de lokale toestand leveren.

Dit is zelfstandig waardevol als sensing/control-technologie en hoeft geen exotische fysica te veronderstellen.

## Waarde
- quasi-gedistribueerde veldmeting met weinig elektrische bekabeling in het meetgebied;
- sensoren die relatief immuun zijn voor elektromagnetische storing;
- gelijktijdige meting van veldgerelateerde strain/temperatuur/mechanische respons;
- closed-loop field shaping;
- monitoring van magnetische installaties, vermogenselektronica en hoogveldsystemen;
- mogelijk compacte sensorarrays voor onderzoek naar vortex-/fluxdynamiek.

## Mechanismen uit bestaande techniek
Optische vezels kunnen magnetische velden indirect of direct detecteren via onder meer:
- Faraday-rotatie in magneto-optische materialen/vezelsecties;
- FBG + magnetostrictief materiaal;
- interferometers gekoppeld aan magnetische vloeistoffen of magnetostrictieve elementen;
- polarisatie- en faseverschuiving;
- multiplexed FBG-netwerken voor meerdere meetpunten.

## WijSAmen-variant
Historische projectelementen die bewaard moeten blijven als ontwerpruimte:
- spiraalgewonden fiber loops;
- loops van verschillende diameter en optische padlengte;
- plaatsing rondom/tussen magnetische elementen;
- rood/groen of meerdere golflengten als mogelijke meetkanalen (niet als bewezen noodzakelijk mechanisme);
- combinatie van optische sensing met lokale regelbare elektromagneten;
- feedback die een gemeten field-state vergelijkt met een target field-map en lokaal corrigeert.

Eerdere reconstructie noemde ook een geometrische magnetische 'skeleton' met veel losse staaf-/bolmagneten. Dat geometrische idee moet alleen als parameteriseerbare testgeometrie worden behandeld, niet als bewezen optimale vorm.

## Aannames
- Multiplexed fiber sensing kan voldoende bandbreedte en ruimtelijke resolutie leveren voor een deel van de control-loop.
- Temperatuur/strain cross-sensitivity kan worden gekalibreerd of apart gemeten.
- De optische laag kan aanvullend zijn op Hall, AMR/GMR/TMR, fluxgate, pickup coils of SQUID-instrumentatie; zij hoeft die niet allemaal te vervangen.

## Alternatieve verklaringen / meetartefacten
- FBG wavelength shift door temperatuur in plaats van magnetisme;
- mechanische strain door Lorentz-krachten;
- birefringence door buiging/druk;
- laser/source drift;
- connector- en polarisatiedrift;
- magnetostrictieve hysterese.

## Kleinste nuttige proef
1. Bouw geen hoogveldsysteem; begin met één veilige elektromagneet/permanente magneet.
2. Meet hetzelfde veld parallel met een conventionele referentiesensor en één optische meetmethode.
3. Varieer veld, temperatuur en mechanische strain afzonderlijk.
4. Fit een kalibratiemodel en bepaal cross-sensitivity.
5. Voeg daarna 4-8 optische meetpunten toe en reconstrueer een eenvoudige field-map.
6. Gebruik die field-map pas daarna in een feedbacklus met meerdere kleine spoelen.

Succes = betrouwbare, gekalibreerde veld/state-feedback. Geen exotisch effect nodig.

## Bewijs / bestaande ankers
- Rostami et al., Measurement 221 (2023), "Advances in fibre Bragg grating technology for magnetic field sensing: A review", article 113482.
- Fiber-optic magnetic sensors based on Faraday effect, magnetostrictive materials and magnetic fluids are established research fields; reviews emphasize compact size, multiplexing and electromagnetic immunity, while also noting temperature, nonlinearity and calibration challenges.
- Frontiers of Optoelectronics review (2022), "Fiber structures and material science in optical fiber magnetic field sensors", DOI 10.1007/s12200-022-00037-0.

## Koppeling met andere sporen
- Primair instrumentatie-/feedbacklaag voor `coherent-magnetic-field-shaping.md`.
- Kan later superconducting vortex/flux research ondersteunen, maar alleen wanneer de sensorbandbreedte en gevoeligheid geschikt zijn.
- Heeft geen wetenschappelijke afhankelijkheid van `zero-boundary-phase-structure.md` of spacetime-hypotheses.

## Besluitlog
- 2026-08-31 — Oud glasvezel/magnetisme-idee losgetrokken als zelfstandige sensing/control-track; koppeling aan field shaping behouden waar nuttig.
