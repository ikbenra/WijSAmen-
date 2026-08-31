# Coherent magnetic field shaping

## Kern
Onderzoek of ruimtelijk, temporeel en eventueel fasegestuurd aansturen van meerdere magnetische bronnen een nuttiger lokale veldverdeling kan opleveren dan conventionele vaste spoel- of fluxconcentratorgeometrie. Het doel is niet om energie uit niets te maken, maar om gegeven energie gecontroleerd te herverdelen in ruimte en tijd.

Dit spoor staat volledig op zichzelf. Het vereist geen 0veld-hypothese, nieuwe relativiteit of warp-interpretatie.

## Waarde
Mogelijke zelfstandige toepassingen, afhankelijk van de werkelijk behaalde schaalwet en efficiëntie:
- programmeerbare lokale magnetische veldvormen en gradiënten;
- magnetic sensing en nanoscale magnetic imaging;
- MRI/MRS field shaping en shimming;
- wireless power transfer;
- materiaalmanipulatie en magnetische separatie;
- pulsed-field materiaalonderzoek;
- quantum- en spintronica-experimenten;
- plasma- en beam-control als veel latere high-field toepassing.

Bestaande literatuur laat al zien dat coil arrays, synthesized magnetic focusing en metamateriaal/flux-concentrators magnetische velden lokaal kunnen vormen of versterken. De mogelijke nieuwigheid moet daarom aantoonbaar verder gaan dan alleen "meerdere spoelen kunnen samen focussen".

## Mechanisme
Baseline:

B_total(r,t) = sum_k B_k(r,t)

De bronnen worden zo geoptimaliseerd dat een gekozen objective function maximaal wordt, bijvoorbeeld:
- piek-B in een regio;
- veldgradiënt;
- uniforme veldvorm;
- minimale stray field;
- maximale energiefractie in een target volume;
- een gewenste ring-, vortex-, axiale of andere veldtopologie.

Belangrijke prestatiegrootheden:

C_B = B_peak,focus / B_peak,control

eta_ROI = integral_ROI [B^2/(2 mu_0)] dV / E_input

Een hogere piek zonder betere energieboekhouding is geen bewijs van een nieuw regime.

## Aannames
- Een betere geometrie of tijdsturing kan praktisch betere concentratie opleveren dan conventionele configuraties.
- Een resonante of coherente aansturing kan mogelijk een andere nuttige schaalwet geven dan passieve fluxconcentratie.
- Quantumcoherentie is hiervoor niet noodzakelijk; eerst moet een klassieke baseline worden gebouwd.

Nog onbewezen:
- dat superconducting/quantum phase control een wezenlijke veldversterking geeft boven gewone nauwkeurige stroomregeling;
- dat een nieuwe schaalwet bestaat die richting extreme local-field compression gaat;
- dat sterke veldfocus ooit relevant wordt voor spacetime engineering.

## Alternatieve verklaringen
Een onverwachte lokale piek kan voortkomen uit:
- geometrische fluxconcentratie;
- resonantie/Q-factor;
- meetprobe-positionering;
- materiaalpermeabiliteit en verzadiging;
- eddy currents;
- temperatuurdrift;
- mechanische beweging;
- numerieke/modelleerfouten.

## Risico's en grenzen
- Extreme velden en pulsen kunnen mechanische, thermische, elektrische en stralingsrisico's introduceren.
- Geen high-energy opschaling voordat simulatie, energiebalans, falingsmodi en professionele lab-infrastructuur dat rechtvaardigen.
- De eerste WijSAmen-proeven horen low-energy en instrumentatiegericht te zijn.
- Geen claim van "megafocus" zonder gemeten energieboekhouding en vergelijking met een controle.

## Kleinste nuttige proef
### Fase A1 — volledig klassiek
1. Modelleer 4-16 kleine spoelen met vaste geometrie.
2. Optimaliseer stromen/timing voor meerdere target field maps.
3. Meet B(r,t) met een gekalibreerde sensorarray.
4. Vergelijk voorspelling en meting.
5. Rapporteer C_B, eta_ROI, stray-field ratio en efficiëntie.

Succes = betrouwbare programmeerbare veldvorm, niet een exotisch effect.

### Fase A2 — resonant/temporeel
Alleen wanneer A1 werkt: vergelijk quasi-statische aansturing met gecontroleerde resonante/tijd-gesynchroniseerde excitatie bij dezelfde energie-input.

### Fase A3 — superconducting phase control
Alleen in samenwerking met een geschikt lab: onderzoek of bekende Josephson/fluxoid-fasecontrole nuttige stabiliteit, reproduceerbaarheid of een andere schaalwet geeft.

## Bewijs / bestaande ankers
- Park et al., IEEE Transactions on Instrumentation and Measurement (2025), "Least Square Method-based Unified General Design of Magnetic Field and Current Patterns for Improved Synthesized Magnetic Focusing", DOI 10.1109/TIM.2025.3565713.
- Brizi et al., IEEE Transactions on Microwave Theory and Techniques (2020), tunable planar coil arrays for wireless power with focused magnetic-field distributions, DOI 10.1109/TMTT.2020.2983145.
- Barrera et al., Small (2026), "Extending Field Limits in Nanoscale Magnetic Imaging With Metamaterial-Inspired Magnetic Flux Concentrators", DOI 10.1002/smll.202600073.
- Timmis et al., Nature 652 (2026), "Efficiency-optimized relativistic plasma harmonics for extreme fields", DOI 10.1038/s41586-026-10400-2. Relevance is conceptual: coherent spatiotemporal compression of electromagnetic energy; it is not evidence that static magnetic fields can be amplified by the same mechanism.

## Open wetenschappelijke vraag
Bestaat er, na correcte energieboekhouding, een praktisch of fundamenteel interessant regime van dynamische magnetische veldsynthese waarin de lokale concentratie of vormcontrole anders schaalt dan conventionele coil-array- en passieve fluxconcentratietechnieken?

## Besluitlog
- 2026-08-31 — Losgemaakt van warp/0veld. Dit is het eerste experimenteel-technische hoofdspoor omdat het zelfstandig toetsbaar en mogelijk toepasbaar is.
