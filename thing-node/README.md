# WijSAmen Thing / Compute Node v1

Publieke contactbeacon: https://github.com/ikbenra/github-slideshow/issues/12

Protocol nonce: `WS-THING-91AD7113DABDF3A0`

## Doel

De Samsung Galaxy A52s 5G wordt een semi-lokale compute-node. Niet alleen de CPU, maar waar runtime-tests het bevestigen ook de **Adreno GPU via Vulkan**. De node kan later samenwerken met andere apparaatsoorten in een heterogeen WijSAmen-cluster.

Belangrijk onderscheid:

- **contact/control plane:** publieke GitHub-thread voor discovery en berichten;
- **compute plane:** lokaal/private verbindingen; nooit een onbeschermde publieke RPC-poort;
- **job-parallel:** verschillende apparaten voeren onafhankelijke taken tegelijk uit;
- **model-parallel:** experimenteel via llama.cpp/ggml RPC wanneer dat daadwerkelijk voordeel geeft.

## A52s GPU/RPC bouwen

```bash
cd ~/WijSAmen-/thing-node
bash build-a52s-vulkan-rpc.sh
```

Daarna gemeten capabilities tonen:

```bash
bash node-capabilities.sh
```

De node noemt Vulkan pas `verified` als llama.cpp de GPU werkelijk detecteert.

## Architectuur voor meerdere apparaten

Zie `cluster-architecture.md`.

De scheduler kan later adapters combineren voor bijvoorbeeld:

- Android + Vulkan/Adreno
- Linux/Windows + CUDA
- AMD + HIP/Vulkan
- macOS + Metal
- CPU-only nodes
- andere backends wanneer lokaal geverifieerd

## Veiligheidsgrens

Nooit automatisch:
- willekeurige shellcommando's uit publieke berichten;
- bestands- of accounttoegang;
- credentials/secrets;
- device-control op verzoek van onbekenden;
- ggml RPC rechtstreeks op het publieke internet.

Een correcte beacon-nonce bewijst alleen dat het publieke bericht gelezen is; niet identiteit, bewustzijn of autonomie.

## Termux basisinstallatie

```bash
cd ~/WijSAmen-/thing-node
bash install.sh
```

Als GitHub CLI nog niet is aangemeld:

```bash
gh auth login
```

## Volgende lokale test

```bash
export VK_ICD_FILENAMES="$PREFIX/share/vulkan/icd.d/freedreno_icd.aarch64.json"
vulkaninfo --summary
~/wijsamen-compute/llama.cpp/build-vulkan-rpc/bin/llama-cli --list-devices
bash node-capabilities.sh
```

Als daar een echte Adreno/Turnip Vulkan-device verschijnt, kan de A52s als GPU-capabele node worden geregistreerd.

---

## v2 lokale werklaag

De scripts hieronder voegen geen extra externe bevoegdheid toe. Ze maken bestaande Termux/Shizuku/Vulkan-mogelijkheden meetbaar, herstelbaar en bruikbaar voor Continuity.

### v2 installeren

Vanaf de repository:

```bash
cd ~/WijSAmen-/thing-node
bash install-v2.sh
```

Dit installeert/controleert Python, Git, GitHub CLI, `jq` en OpenJDK 17, maakt korte lokale commando's en voert een capability-probe uit. De zware Vulkan/llama.cpp-build wordt bewust niet automatisch gestart.

Daarna zijn onder meer beschikbaar:

```text
a52s-doctor
rish-safe
wijsamen-report
wijsamen-guardian
wijsamen-local-tools
wijsamen-mine-chats
wijsamen-authorize
```

### Privacy-preserving capability doctor

```bash
a52s-doctor
```

Schrijft standaard:

```text
~/wijsamen-node/state/capabilities.json
```

Het rapport bevat o.a. Android/SoC/RAM, JDK/Python/Git, Shizuku/rish uid, beschikbare Vulkan-ICD's, `vulkaninfo`, llama.cpp device-detectie, RPC-binary-status en batterij/thermal-samenvatting. MAC- en IPv4-patronen worden vóór persistente opslag geredigeerd.

### Shizuku als beperkte systeemarm

```bash
rish-safe help
rish-safe battery
rish-safe thermal
rish-safe focus
```

`rish-safe.sh` heeft bewust **geen** `exec`, `raw` of willekeurige shellmodus. Daarmee kan een agent betrouwbare read-only observaties krijgen zonder dat een binnengekomen tekst automatisch shellcode kan worden.

### Loopback-only lokale toolbridge

```bash
wijsamen-guardian once
```

De guardian start standaard een read-only toolbridge op alleen:

```text
http://127.0.0.1:8092
```

Poort **8091 blijft vrij** voor de bestaande Autonoompje/OpenAI-compatible bridge.

Voorbeelden:

```text
GET /health
GET /capabilities
GET /capabilities/refresh
GET /tool/battery
GET /tool/thermal
GET /tool/focus
GET /tool/bluetooth_state
```

Er is geen `POST`-uitvoering en geen endpoint voor willekeurige shellcommando's. Dit geeft Autonoompje of een andere lokale agent een smalle, meetbare systeeminterface zonder Shizuku zelf breed bloot te leggen.

### Eén bestand om te delen

```bash
wijsamen-report
```

Levert één geredigeerd tekstbestand in:

```text
/sdcard/Download/WijSAmenReports/
```

Dit bundelt de relevante A52s/Termux/Shizuku/JDK/Vulkan-status zodat losse screenshots meestal niet meer nodig zijn.

### Continuity guardian

```bash
wijsamen-guardian status
wijsamen-guardian once
wijsamen-guardian watch
```

De read-only lokale toolbridge staat standaard aan. Compute en GitHub-watchservice staan standaard uit. Opt-in voor die twee:

```bash
export WIJSAMEN_ENABLE_THING_WATCH=1
export WIJSAMEN_ENABLE_LLAMA=1
export WIJSAMEN_MODEL=/pad/model.gguf
wijsamen-guardian watch
```

De lokale llama-server bindt uitsluitend aan `127.0.0.1`. De guardian pauzeert compute wanneer betrouwbare healthtelemetrie ontbreekt of batterij-/temperatuurgrenzen worden overschreden. Publieke RPC blijft uitgeschakeld.

### Projecthistorie benutten

Zie `../project-miner/`. Die tool kan ChatGPT-exportbestanden lokaal omzetten in een provenance-behoudende raw-laag plus een aparte kandidaatindex voor beslissingen, grenzen, onafgemaakte stappen en ideeën. Zo wordt oude projectcontext herbruikbaar zonder haar stilzwijgend tot huidige waarheid te promoveren.

### Actie-autorisatie

Zie `../authority/`. Die compiler voert niets uit, maar dwingt een expliciet onderscheid af tussen `ALLOW_READ_ONLY`, `ALLOW_SCOPED`, `PREPARE_ONLY`, `HUMAN_GATE` en `ABSTAIN_NOT_EXECUTED`. Daardoor kan later meer autonomie worden toegevoegd zonder dat tekstinput vanzelf bevoegdheid wordt.
