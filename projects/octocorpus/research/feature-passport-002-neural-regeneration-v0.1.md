# Feature Passport 002 — octopus neural regeneration

Status: **ONDERZOEK — V0.1, DESK-ONLY**

## Provenance

- Source marker: user research direction, 2026-10-09, OctoScript/OctoCorpus.
- Literal key passage: “Wat kunnen we bij de octopusjes afkijken. Die kunnen zenuwen bijmaken. Laten we ze als inspiratiebron benutten.”
- Evidence label for the passage: `USER_HYPOTHESIS / RESEARCH_DIRECTION`, not a biological or clinical result.
- Canonical portfolio source remains the Portfolio Hunter Google Doc. This file is a versioned research scaffold.

## Question

Which experimentally observed components of octopus neural repair are strong enough to become comparative research questions, without assuming that they transfer to the mammalian central nervous system or authorize any personal intervention?

## Source-supported results

### 1. A transected pallial nerve can reconnect and regain function

`SOURCE_SUPPORTED_RESULT`

In *Octopus vulgaris*, complete transection of one pallial nerve was followed by axons crossing the lesion, entering the stellate ganglion and restoring functions controlled by that pathway. The 2019 study used the intact contralateral nerve as an internal control. Regrowing fibres crossed the gap by 30–45 days; normal breathing returned in all studied animals in roughly 30–37 days; full skin-pattern control took about 45 days to 5 months. Electrophysiology at 5 months showed activity across the lesion. The regenerated architecture remained less orderly than the original, yet function returned.

Important limits:

- 14 animals in total, with only the 5-month group used for electrophysiology;
- one specific peripheral brain-to-ganglion pathway, not a mammalian brain lesion;
- the study describes recovery and morphology but does not establish one causal molecular switch;
- older studies reported incomplete or variable recovery, so “octopuses always fully regenerate nerves” is too strong.

Primary source: Imperadore et al., *Journal of Experimental Biology* (2019), DOI [10.1242/jeb.209965](https://doi.org/10.1242/jeb.209965).

### 2. Repair includes degeneration, immune-cell activity, scar and guided regrowth

`SOURCE_SUPPORTED_RESULT`

After pallial-nerve transection, studies reported early degeneration in both stumps, hemocyte infiltration, phagocytosis, scar formation, cell proliferation and connective tissue associated with the route followed by regrowing fibres. Both central and peripheral stumps showed regenerative activity. This makes the system interesting because successful regrowth occurs despite a scar response rather than through a simple absence of scarring.

Primary source: Imperadore et al., *Scientific Reports* (2017), DOI [10.1038/srep46564](https://doi.org/10.1038/srep46564).

### 3. Acute arm repair rapidly creates a protected wound environment

`SOURCE_SUPPORTED_RESULT`

After distal arm amputation, wound margins contracted rapidly, wound-edge epithelial cells migrated over the wound bed and a temporary cellular plug covered exposed tissue. At 6 hours, mean closure was reported as 64.0 ± 17.2%. Cell death appeared first in skin and muscle and extended into the nerve cord by 24 hours.

This is evidence about the acute preparation phase, not proof that these events cause later neural regeneration.

Primary source: Shaw et al., *Zoological Letters* (2016), DOI [10.1186/s40851-016-0044-5](https://doi.org/10.1186/s40851-016-0044-5).

### 4. Vascular support may accompany regeneration

`SOURCE_SUPPORTED_RESULT`

The 2019 pallial-nerve study observed more vessels and small capillaries in regenerated nerves than in controls and interpreted this as possible angiogenesis. This is descriptive association; it does not show that added vascular growth is necessary or sufficient for nerve repair.

Primary source: Imperadore et al. (2019), DOI [10.1242/jeb.209965](https://doi.org/10.1242/jeb.209965).

## Enabling molecular resource — not regeneration evidence

`SOURCE_SUPPORTED_RESULT / ENABLING_RESOURCE / BASELINE_COMPARATOR`

Costa et al. (2026) validated a single-cell RNA-sequencing preparation workflow for circulating hemocytes and white-body resident hemocytes in *Octopus vulgaris*. Modified anti-aggregation solution (MAS) maintained more than 90% viability for two hours; a reduced-EDTA variant was compatible with the 10x Genomics workflow; shallow sequencing resolved distinct hemocyte clusters. The raw shallow dataset is public under BioProject `PRJNA1376517`, including run `SRR36345357`.

This resource does **not** contain a nerve-injury condition, regeneration time course or lesion-site spatial context. It therefore cannot identify regeneration-specific cell states or establish that an immune program causes successful neural repair. Its value is narrower and practical: it makes a baseline octopus immune-cell map and a future injury-versus-control design technically more credible.

Primary source: Costa et al., *Scientific Reports* (published 10 April 2026), DOI [10.1038/s41598-026-47700-6](https://doi.org/10.1038/s41598-026-47700-6). Public data: NCBI BioProject [PRJNA1376517](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1376517), run [SRR36345357](https://www.ncbi.nlm.nih.gov/sra/SRR36345357).

### Smallest reversible data test

1. Inspect sample metadata, library composition and quality-control fields.
2. Derive a baseline hemocyte cluster-and-marker map only.
3. Cross-reference candidate markers from the 2017 pallial-nerve histology and earlier bulk immune transcriptomes, explicitly separating cell identity from injury response.
4. Pre-register a future comparison: uninjured versus injured, circulating versus lesion-associated cells, and multiple post-injury time points.
5. Do not label any cluster “regenerative” without an injury contrast and independent validation.

## Conventional baseline

Mammalian peripheral nerves can regenerate to a limited degree, while long-distance, correctly targeted repair in the adult mammalian central nervous system is much more restricted. Differences in cell types, myelination, immune responses, extracellular matrix, lesion geometry and evolutionary history mean that an octopus result cannot be converted directly into a human treatment rule.

## WijSAmen difference

`INFERENCE`

The useful move is not “copy an octopus substance.” It is to compare repair as a coordinated sequence:

1. rapid sealing without permanently blocking the route;
2. controlled degeneration and debris clearance;
3. formation of a permissive physical bridge;
4. axon guidance and target re-entry;
5. vascular/metabolic support;
6. functional verification even when the rebuilt architecture differs from the original.

This sequence creates testable comparative questions across species and separates necessary conditions from attractive but unsupported supplement or stimulation claims.

## Candidate mechanism axes

Each axis remains `HYPOTHESIS` until a causal experiment or stronger molecular dataset supports it.

| Axis | Octopus observation | Comparative question | Required evidence |
|---|---|---|---|
| Scar/bridge | scar and connective tissue coexist with regrowth | Is octopus scar composition permissive rather than merely reduced? | spatial ECM composition plus perturbation |
| Immune response | hemocyte infiltration and phagocytosis | Which immune states clear debris without locking the lesion? | cell-type markers, time course and causal manipulation |
| Guidance | fibres cross the gap and re-enter ganglion | Which local cues maintain direction and target recognition? | spatial expression/protein map plus disruption test |
| Bidirectional repair | central and peripheral stumps regrow | Do distinct neuron locations use shared or different programs? | lineage-resolved expression and tracing |
| Vascular support | increased vessels/capillaries | Is vascular growth causal, supportive or incidental? | temporal coupling plus selective perturbation |
| Functional tolerance | function returns despite disordered architecture | Which connectivity metrics are sufficient for function? | quantitative anatomy–electrophysiology–behaviour linkage |

## Key unknowns

- the regenerative cell populations and their lineage relationships;
- the exact extracellular-matrix composition of the bridge;
- causal gene-regulatory programs across the full time course;
- whether arm axial-nerve-cord regeneration uses the same program as the pallial nerve;
- gene-family age, orthology and regulatory conservation across mollusks;
- which mechanisms are cephalopod-specific and which are deeply conserved;
- whether structural irregularity is stable, compensated or later remodelled;
- any safe translational bridge to human neural repair.

## Cheapest reversible desk test

Build a source-linked regeneration matrix before nominating targets:

`species | tissue/pathway | lesion type | time point | cell type | process | molecular marker | spatial evidence | perturbation | structure outcome | functional outcome | evidence label | uncertainty`

Start with the three primary studies above. Add only claims that can be traced to exact figures, methods or results. Pre-register three alternatives:

1. a cephalopod-specific permissive repair program;
2. a broadly conserved repair program expressed in a different lesion environment;
3. multiple local mechanisms whose apparent unity is a reconstruction artefact.

The 2026 hemocyte dataset satisfies baseline resource availability, but not the injury/time-point contrast needed to distinguish these models. Advance only when at least one regeneration-specific molecular or single-cell/spatial dataset can separate them.

## Disconfirming evidence

Downgrade the broad inspiration claim if:

- successful repair is limited to unusually simple peripheral pathways;
- the arm nerve cord and pallial nerve use materially different programs;
- apparent guidance disappears under quantitative tracing;
- vascular and immune signatures are consequences rather than drivers;
- candidate pathways lack orthologous or functional correspondence outside cephalopods;
- molecular findings fail replication across octopus species, age, injury severity or physiological state;
- functional recovery depends on compensatory circuits rather than true reconnection.

## Safety and welfare boundary

This passport authorizes literature analysis and public-data comparison only. It does not authorize self-experimentation, medical treatment claims, animal injury, capture, invasive work or welfare-sensitive testing. Any later cephalopod research must satisfy applicable welfare law and preserve species-appropriate withdrawal and care.

## Phase-end gate

Advance from `ONDERZOEK` to `ONDERBOUWD` only after:

- a complete evidence matrix for the three starting studies;
- a baseline hemocyte map from the public 2026 single-cell resource;
- at least one regeneration-specific molecular dataset with explicit cell/tissue, injury condition and time-point provenance;
- alternative-model comparison;
- an independent overclaiming review;
- a written mammal-translation boundary that survives contradiction.
