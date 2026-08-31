# Zero-boundary phase structure (0veld-mathematiek)

## Kern
Onderzoek een verrijkte nulgrens waarin niet alleen de scalaire waarde 0 wordt bewaard, maar ook informatie over hoe een toestand 0 nadert: richting, fase, winding en logschaal. Dit is in eerste instantie een wiskundig/fysisch interpretatiespoor, geen claim van een nieuw veld of nieuwe energiebron.

Een nuttige representatie is:

Psi(L,phi) = Psi_0 exp(-L) exp(i phi),   L -> +infinity.

De amplitude gaat naar nul, terwijl fase/richting in de verrijkte beschrijving niet automatisch wordt weggegooid.

## Wiskundige ankers
### Twee zijden van nul
Voor een reële grootheid:

x = s x_0 exp(-L),  s in {-1,+1}.

Dan x -> 0 terwijl s de benaderingsrichting bewaart.

### Nul als grens met richtingen
In twee dimensies kan z = r exp(i phi) worden gebruikt. De gewone complexe vlakbeschrijving klapt alle phi samen zodra r=0. Een real-oriented blow-up vervangt het oorsprongspunt juist door de cirkel van naderingsrichtingen. Dit is bestaande wiskunde en biedt een passende taal voor de gebruikersintuïtie dat "de verzameling van 0 plus de limieten van verschillende kanten" meer structuur kan bevatten dan alleen het getal 0.

### pi, plus/min oneindig en nul-plus/min
Met de half-angle coordinate:

u = tan(phi/2)

geeft phi -> pi^- : u -> +infinity en phi -> -pi^+ : u -> -infinity, terwijl +pi en -pi dezelfde positie op de fasecirkel representeren. Met v=1/u worden dezelfde twee benaderingen v -> 0+ en v -> 0-. Dit laat zien dat oneindigheid soms een coordinatensingulariteit is en niet een singulariteit van het onderliggende geometrische object.

### Gekoppelde limieten, niet willekeurig "oneindig wegstrepen"
Als

x = a exp(-L), y = b exp(-L), L -> infinity,

dan x,y -> 0 maar x/y -> a/b. De gedeelde divergente logschaal valt exact weg omdat beide grootheden door dezelfde parameter worden gestuurd. Dit is de mathematisch legitieme versie van het idee dat een eindig praktisch resultaat uit gekoppelde nul/oneindig-limieten kan overblijven.

## Relatie met bestaande quantumfysica
Bekende natuurkunde bevat al sterke analogieën:
- E = hbar omega geeft E/omega = hbar, ook wanneer E en omega samen naar nul gaan.
- Voor een volledige cyclus T=2pi/omega blijft E*T=2pi hbar eindig terwijl E->0 en T->infinity.
- Aharonov-Bohm-fase laat zien dat lokaal B=0 langs een deeltjespad niet betekent dat alle gauge-invariante globale fase-informatie verdwijnt.
- Berry/geometrische fase bewaart informatie over een gesloten pad in parameter-/toestandsruimte.
- Superconducting vortices combineren nul/suppressie van de ordeparameter in de kern met niet-triviale fasewinding rondom die kern.

Deze bestaande effecten zijn geen bewijs voor een nieuw 0veld. Ze zijn de baseline die een nieuwe hypothese eerst moet overtreffen.

## Wetenschappelijk waardevolle vraag
Kan de verrijkte nulgrens worden gebruikt om een gauge-invariante, fysisch meetbare invariant te definiëren die NIET al volledig samenvalt met bekende winding, holonomy, Berry phase, Aharonov-Bohm phase, fluxoid quantization of standaard topologische quantumfysica?

## Minimale falsifieerbare eis
Definieer een residu:

Delta_0 = wrap(Gamma_meas - Gamma_standard)

waar Gamma_standard alle bekende dynamische, geometrische, AB-, fluxoid-, device- en control-fasebijdragen bevat.

Nulhypothese:

H0: Delta_0 = 0 binnen onzekerheid.

Een nieuwe 0veld-theorie mag pas als fysica gelden wanneer zij VOORAF een niet-nul Delta_0 voorspelt met:
- teken;
- dimensie/eenheid waar relevant;
- grootteorde;
- schaalwet;
- symmetrie;
- afhankelijkheid van winding/oriëntatie/control parameters.

Zonder zo'n voorspelling is dit een nuttig mathematisch/interpretatief raamwerk, geen nieuwe natuurwet.

## Waarde als er geen nieuwe fysica uitkomt
Ook als Delta_0 altijd nul blijkt:
- kan de verrijkte nulgrens helpen om fase-/topologische informatie intuïtief te structureren;
- kan de representatie bruikbaar zijn voor numeriek stabiele behandeling van nulpunten/singulariteiten;
- kan de koppeling met fasewinding nuttig zijn in superconducting/quantum-control-ontwerp;
- blijft het een zelfstandig wiskundig onderzoeksspoor.

## Risico's en grenzen
- Nooit 0/0, infinity-infinity of 0*infinity als gewone algebra behandelen zonder een gedeelde limietparameter.
- Pi is eindig; het oneindige aantal decimalen is geen oneindige waarde.
- Geen dark-energy, dark-matter of gravity claim afleiden uit E/omega=hbar alleen.
- Een nieuwe naam voor bekende Berry/AB/topologische fysica is geen nieuwe ontdekking.

## Bewijs / bestaande ankers
- Cohen et al., Nature Reviews Physics 1 (2019), "Geometric phase from Aharonov-Bohm to Pancharatnam-Berry and beyond", DOI 10.1038/s42254-019-0071-1.
- Li, Hansson & Ku, Physical Review A 106 (2022), "Gauge-independent description of the Aharonov-Bohm effect", DOI 10.1103/PhysRevA.106.032217.
- Zhang et al. (2017), Berry phase measurement in a superconducting phase qubit, arXiv:1704.00894.
- Standard real-oriented blow-up construction: the origin of C can be replaced by the circle of directions at the origin; this is a known geometric construction, not a new WijSAmen invention.

## Besluitlog
- 2026-08-31 — 0veld herzien: niet "nul is energie", maar "de gewone nulprojectie kan naderings-, fase- en topologische structuur weggooien". Nieuwe fysica blijft onbewezen en krijgt een harde falsificatie-eis.
