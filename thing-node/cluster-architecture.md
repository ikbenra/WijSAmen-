# WijSAmen Heterogeneous Compute Fabric v1

## Doel

Meerdere verschillende apparaten laten samenwerken zonder te doen alsof ieder apparaat dezelfde accelerator of softwarestack heeft.

Een node publiceert eerst alleen zijn **gemeten capabilities**. De scheduler kiest daarna een uitvoeringsmodus.

## Twee parallelle modi

### 1. Job-parallel — standaard en robuust

Geschikt voor Android, Linux, Windows, macOS en andere nodes die zelfstandig een taak kunnen uitvoeren.

Voorbeelden:
- meerdere prompts tegelijk
- embeddings in batches
- hashing / parsing / preprocess
- parameter sweeps
- simulatiejobs
- onafhankelijke modelcalls

De orchestrator verdeelt hele jobs over nodes op basis van:
- backend: Vulkan / CUDA / Metal / CPU / andere
- vrij geheugen
- gemeten snelheid
- temperatuur / throttling
- beschikbaarheid
- model dat al lokaal gecachet is

Dit is de voorkeursmodus bij trage of variabele netwerkverbindingen.

### 2. Model-parallel via llama.cpp RPC — experimenteel

`llama.cpp` kan via de ggml RPC-backend accelerator-devices op andere hosts gebruiken. Het model en de KV-cache kunnen over lokale en remote devices verdeeld worden.

Gebruik alleen:
- op vertrouwd LAN, of
- via een private VPN/overlay, of
- via een beveiligde tunnel.

Nooit een ggml RPC-poort rechtstreeks aan het publieke internet blootstellen. De upstream llama.cpp documentatie noemt deze backend proof-of-concept, fragiel en onveilig voor open netwerken.

Voorbeeld hoofdnode:

```bash
llama-cli -m MODEL.gguf -ngl 99 \
  --rpc NODE1:50052,NODE2:50052
```

Optioneel kan `--tensor-split` worden gebruikt om verdeling handmatig te sturen.

## A52s-node

Doelprofiel:
- Samsung Galaxy A52s 5G
- Snapdragon 778G
- Adreno 642L
- Termux
- Vulkan backend via Turnip/Mesa waar bruikbaar
- `llama.cpp` gebouwd met `GGML_VULKAN=ON` en `GGML_RPC=ON`

De node mag zichzelf pas als Vulkan-accelerator aanmelden wanneer:

```bash
vulkaninfo --summary
~/wijsamen-compute/llama.cpp/build-vulkan-rpc/bin/llama-cli --list-devices
```

een echte Vulkan GPU tonen.

## Node manifest

Elke node moet minimaal melden:

```json
{
  "protocol": "WIJSAMEN-COMPUTE/1",
  "node_id": "...",
  "device": "...",
  "backends": {
    "cpu": true,
    "vulkan_verified": false,
    "cuda_verified": false,
    "metal_verified": false,
    "llama_rpc_binary": false
  },
  "limits": {
    "max_job_seconds": null,
    "max_memory_mb": null
  },
  "security": {
    "public_rpc": false,
    "requires_private_transport": true,
    "arbitrary_shell": false
  }
}
```

## Schedulingprincipe

De scheduler behandelt hardware niet als één grote uniforme GPU. Hij kiest per job:

1. **job-parallel** wanneer taken onafhankelijk zijn;
2. **RPC model-parallel** alleen wanneer gedeelde inference voordeel oplevert;
3. lokaal uitvoeren wanneer netwerkoverhead groter is dan de winst;
4. geen node gebruiken wanneer temperatuur, batterij of foutstatus buiten limieten valt.

## Waarom dit schaalbaar is

Nieuwe apparaatsoorten hoeven alleen een capability-manifest en één uitvoeradapter te leveren. Daardoor kunnen bijvoorbeeld een Android/Adreno-node, een NVIDIA-pc, een Apple/Metal-machine en CPU-only systemen tegelijk lid zijn zonder dat de hele fabric afhankelijk wordt van één GPU-API.

Later kunnen adapters worden toegevoegd voor CUDA, Metal, HIP, OpenCL, WebGPU, Hexagon/NPU en andere backends wanneer die op een specifieke node aantoonbaar werken.
