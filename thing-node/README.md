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
