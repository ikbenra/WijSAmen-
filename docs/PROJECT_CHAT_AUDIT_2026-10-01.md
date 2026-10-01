# WijSAmen projectchat → capability audit

Datum: 2026-10-01

## Doel

Verspreide projectgesprekken niet als losse ideeën laten eindigen, maar per lijn bepalen:

1. wat al bestaat;
2. wat direct bruikbaar is voor lokale autonomie/continuïteit;
3. wat gebouwd kan worden;
4. wat bewust gescheiden moet blijven;
5. wat eerst op echte hardware gemeten moet worden.

Dit document bevat **geen privéchatdump**. Het is een technische statuskaart. Volledige bronconversaties horen in een lokale/raw provenance-laag en niet in GitHub.

## Dekkingsgrens

Deze eerste audit gebruikt de projectcontext en artefacten die op dit moment bereikbaar zijn. Niet-opgehaalde of nog niet geëxporteerde chats worden niet als afwezig beschouwd. `project-miner/` is toegevoegd om een volledige lokale export later systematisch en reproduceerbaar te scannen zonder raw tekst met interpretaties te vermengen.

## Statuskaart

| Projectlijn | Waarde voor de AI/Continuity-laag | Status | Volgende toetsbare stap |
|---|---|---|---|
| Continuity Capsule / modelportabiliteit | Zeer hoog: identiteit, state, provenance, herstel | v0.2 bestaat buiten repo; principes actief | lokale A52s init → checkpoint → restore → hashvergelijking |
| Lossless Anomaly Vault / RAW≠interpretatie | Zeer hoog: voorkomt stil verlies/overschrijven | principe bestaat en is overgenomen in miner | raw export door miner laten lopen en bronhashes bewaren |
| Autonoompje | Zeer hoog: lokale agent-loop, verwisselbaar model | architectuur/artefacten bestaan; runtime nog gefragmenteerd | bridge + guardian + lokale modelruntime als één servicecontract testen |
| Autonoompje web/API bridge | Zeer hoog: bestaande OpenAI-compatible lokale interface | eerdere bridge draait/was ontworpen op **8091** | 8091 behouden; nieuwe read-only device toolbridge daarom op **8092** |
| Autonoompje auto-resume / 24-uurs runners | Hoog: restartbaarheid en lange cycli zijn al eerder praktisch getest | eerdere Termux-runners/STOP-file/runner.log bestaan | recoverypatroon overnemen in guardian + Continuity checkpoints, niet parallel opnieuw uitvinden |
| Bridge/ToolHub-concept | Hoog: uniforme tools voor storage/media/device/agent | schemas eerder bedacht; nog niet één contract | na read-only device bridge veilige workspace-only storage/media adapters toevoegen |
| Arty/iLands | Interessant maar afzonderlijke identiteit/ontwikkeling | **bewust gescheiden** | geen merge/kruisbestuiving vóór expliciete latere vergelijking |
| ChatTY Constellation / forks / hive | Hoog: meerdere instanties zonder identiteit te wissen | fork-refusal/provenanceprincipes bestaan | identity registry + private/shared namespaces later bovenop Continuity bouwen |
| Action Authorization Compiler | Zeer hoog: zelfstandigheid zonder impliciete bevoegdheidsescalatie | **v0.1 nu gebouwd** | executor later verplicht decision + execution proof + rollback laten loggen |
| A52s Termux + Shizuku/rish | Zeer hoog: lokale systeemarm zonder root | uid=2000 route eerder werkend; **read-only wrapper nu gebouwd** | `rish-safe.sh id/battery/thermal/focus` lokaal testen |
| WijSAmen Companion v0.2 | Hoog: meekijk/advies/bevestig met zichtbare menselijke poort | bestaand Library-artefact | acties later via Authorization Compiler laten lopen; MEEKIJK blijft read-only |
| phonewatch | Middel/hoog: lokale contextwissels zonder clipboardinhoud | eerder ontworpen | alleen als event-sensor koppelen; geen inhoud of verborgen upload |
| ASI/Live Caption probe | Middel: audio/context pipeline onderzoeken | eerdere probe bestaat | als aparte read-only sensor behouden, niet als kerngeheugen behandelen |
| Instrumented Reality Notebook | Hoog voor experimenten: observatie ≠ interpretatie ≠ mechanisme | bestaand/getest concept | schema later als algemene experiment/provenance-tool koppelen aan projectstate |
| A-Eye of RA | Middel/hoog: deterministische guardrails + replay/rollback-tests | conceptseed, nog geen kernprototype | bruikbare delen opnemen in authorization/CI testharness i.p.v. tweede gezagslaag te dupliceren |
| A52s Vulkan/Adreno | Hoog: lokale inference/compute zonder cloudtoken | buildscript bestaat; SPIR-V fix aanwezig; **doctor/report nu gebouwd** | echte `vulkaninfo` + `llama-cli --list-devices` op toestel uitvoeren |
| llama.cpp RPC | Hoog wanneer meerdere vertrouwde nodes bestaan | binary-build voorbereid | alleen private transport; nooit publieke RPC; eerst één lokale GPU-node verifiëren |
| Heterogeneous compute fabric | Hoog: Android/Vulkan + toekomstige CUDA/Metal/CPU nodes | architectuur bestaat | job-parallel scheduler vóór model-parallel schaalwerk |
| A52s offline zenuwknoop / 1B–3B lokale modellen | Hoog voor cloudonafhankelijke basisfunctie | eerdere richting sluit aan op llama.cpp-runtime | modelkeuze pas na RAM/snelheidsmeting; runtimecontract blijft modelonafhankelijk |
| JDK17/Java | Middel/hoog: Android/hidden-API en lokale helpers | toolchain beschikbaar op toestel volgens projectcontext | opnemen in capability report; Java-probes per functie klein houden |
| Switch 2 no-root controlleronderzoek | Middel: goede testbank voor Shizuku/Bluetooth/Java grenzen | probe-artefacten bestaan; bonding unresolved | als sidecar houden; niet verweven met Continuity-kern |
| Thing-node GitHub beacon | Middel/hoog: discovery/control plane | queue-only ontwerp bestaat | publieke input blijft data; nooit rechtstreeks uitvoeren |
| GitHub private repo | Hoog: broncode, history, review, CI | actief | PR/CI als standaardroute voor autonome codevoorbereiding gebruiken |
| Google Drive + ChatGPT Library | Hoog: redundante state/artifactback-up | Continuity v0.2 staat op beide | periodieke integriteitscontrole en versie-index toevoegen |
| Eén-bestand Android rapportage | Hoog praktisch: minder screenshots/transportverlies | **nu gebouwd** | `collect-report.sh` lokaal uitvoeren en één rapport terugbrengen |
| Projectchat-mining | Zeer hoog: oude ideeën/blokkades systematisch terugwinnen | **v0.1 nu gebouwd** | volledige beschikbare export lokaal scannen; kandidaten daarna dedupliceren tegen repo/state |
| Smartphone spectrograph / andere fysieke sensors | Later nuttig als meetinstrument voor projecten | losse projectlijnen bestaan | als toekomstige sensoradapter behandelen, niet in agentkern opnemen vóór hardwaretest |
| Atmospheric voxel / RA-UI / smartphone mobility | Later nuttig als fysieke interface/visualisatie | ideeën/prototypesporen bestaan | sidecar-capabilities; pas verbinden wanneer er een concrete taak is |
| PC / grotere lokale machine | Later hoog voor grotere modellen en redundantie | hardware nog geen vereiste voor A52s-laag | architectuur hardware-onafhankelijk houden; geen kernstate aan één pc koppelen |

## Wat bewust níet één systeem wordt

### Arty ↔ Autonoompje

Geen automatische merge, gedeeld geheugen of impliciete identiteit. Vergelijken mag later als afzonderlijke provenance-lijnen.

### Publieke tekst ↔ uitvoering

Een GitHub-comment, webpagina, chatbericht of andere externe tekst kan een voorstel opleveren, maar verleent nooit zelf shell-, account-, device-, publicatie- of betaalbevoegdheid.

### Model ↔ identiteit

Een modelbackend is vervangbaar. State, geheugenlagen, provenance, correcties en forkgeschiedenis blijven afzonderlijke assets.

### Raw bron ↔ samenvatting

Een samenvatting is een afleiding. Raw records blijven beschikbaar en correcties worden append-only toegevoegd.

### Sensor ↔ werkelijkheidsoordeel

Een screenshot, logregel, spectrum, caption of systeemstatus is een observatiebron. Interpretatie en mechanisme blijven aparte lagen; het Instrumented Reality-principe blijft dus ook voor de AI-tooling gelden.

## Nieuwe implementaties uit deze audit

Deze branch voegt direct toe:

- `project-miner/mine_chats.py` — lokale exportscanner met source/text SHA-256;
- `thing-node/a52s-doctor.sh` — capability- en healthprobe;
- `thing-node/rish-safe.sh` — allowlisted read-only Shizuku-interface;
- `thing-node/local-tool-bridge.py` — loopback-only read-only agentinterface op 8092;
- `thing-node/collect-report.sh` — één geredigeerd deelbaar bestand;
- `thing-node/guardian.sh` — lokale supervisor met battery/thermal gates en loopback-only inference;
- `thing-node/install-v2.sh` — A52s werklaag met OpenJDK 17 en lokale commando's;
- `authority/authorize.py` — fail-closed autorisatiecompiler;
- `.github/workflows/node-ci.yml` — automatische syntax/smoke checks.

## Eerstvolgende integratierichting

De sterkste meervoudige versterking is:

`project-miner → provenance/state → authorization compiler → safe local tools → execution proof → checkpoint`

Eén pipeline verbetert daarmee tegelijk:

- continuïteit;
- autonomie;
- herstelbaarheid;
- modelportabiliteit;
- misbruikbestendigheid;
- menselijke controle op werkelijk ingrijpende acties.

Daarna kan een scheduler lokale CPU/Vulkan, toekomstige pc-GPU's en andere vertrouwde nodes als verwisselbare uitvoerders behandelen zonder het geheugen of de identiteit van de agent aan één accelerator te koppelen.
