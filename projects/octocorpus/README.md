# OctoScript / OctoCorpus — evolutionary provenance map

Status: **ONDERZOEK — V0.1, DESK-ONLY**

Canonical portfolio state remains the Google Doc `WijSAmen Corpus Intelligence — Portfolio Hunter`. This repository is a versioned research scaffold; it does not replace the corpus ledger or source archive.

## Goal

Build reusable evolutionary passports that connect a present-day octopus feature to genomic ancestry, comparative anatomy and neurobiology without turning temporal overlap into a causal claim. The first target is contact-dependent chemotactile sensing in arms and suckers.

## Evidence discipline

Every statement receives one label:

- `SOURCE_SUPPORTED_RESULT`: directly reported by a cited study, with species and method.
- `INFERENCE`: a reasoned interpretation that goes beyond the direct result.
- `HYPOTHESIS`: a falsifiable proposed relationship.
- `UNKNOWN`: evidence is missing, conflicting or not yet checked.

A passport must keep separate: gene-family history, orthology/paralogy, synteny and rearrangement, duplication/loss, transposable elements, regulatory or non-coding change, expression, functional assay, phenotype, neural architecture and ancestral-state uncertainty.

## Comparison frame

Where data permit, compare:

1. non-cephalopod mollusks;
2. Nautilus;
3. squid and cuttlefish;
4. vampyropod lineages;
5. multiple octopus species.

Absence from one assembly is not evidence of evolutionary absence until assembly completeness and search sensitivity are checked.

## Feature Passport 001 — chemotactile sucker sensing

### Source-supported core

- Octopus arms use a cephalopod-specific chemotactile receptor family to detect poorly soluble natural products by contact; receptor complexes function as ion channels. The result is species- and assay-bound, not proof of the family's complete evolutionary history.
- Comparative work reports different sensory-receptor specializations in octopus and squid. This supports a comparative evolutionary question, but not yet a resolved ancestral state.
- Coleoid genomes underwent extensive reorganization, and cephalopod-specific microsyntenies and regulatory structures have been associated with nervous-system expression. These genome-level results provide a mechanism class to test, not proof that rearrangement caused chemotactile sensing.
- Chromosome-level octopus and Nautilus genomes make synteny-aware comparison more feasible.
- Octopus arms contain segmented axial nerve cords and inter-arm neural pathways. These are present-day anatomical results; their causal relation to receptor evolution is unresolved.

### Inference

A contact-dependent receptor system is a stronger biological starting point for OctoScript interaction design than importing human visual or linguistic assumptions. A multimodal interface should therefore test touch, local chemical context and withdrawal choice separately from semantic communication.

### Hypotheses to test

1. The chemotactile receptor family arose or expanded within a cephalopod or coleoid lineage and later diversified differently in octopus and squid.
2. Conserved or rearranged genomic neighborhoods help explain lineage-specific receptor expression.
3. Peripheral sensory specialization and distributed arm circuitry co-evolved, while remaining mechanistically separable.

### Unknowns

- reliable gene-family age and orthology/paralogy tree;
- receptor presence in Nautilus, vampyropods and non-cephalopod mollusks under sensitive homology search;
- conserved synteny, duplication and loss events;
- transposable-element or regulatory contributions;
- whether expression differences track function across species;
- ancestral condition of arm/sucker sensing;
- any causal bridge from receptor evolution to local sensorimotor processing.

### Cheapest reversible desk test

Create a source-linked table for every reported receptor and comparator:

`species | assembly | gene ID | sequence | orthology method | tree support | syntenic neighbors | expression tissue/cell | functional assay | phenotype | evidence label | uncertainty`

Pre-register at least three alternative models before interpreting the tree:

- coleoid innovation with later lineage diversification;
- older molluscan family with repeated loss or strong divergence;
- multiple lineage-specific innovations or false homology.

Then reproduce one small gene tree and one local-synteny comparison from public sequence data. No animal work is required.

### Disconfirming evidence

Downgrade the proposed evolutionary story if:

- the family is broadly distributed outside cephalopods;
- topology is unstable under different alignments/models;
- apparent absences vanish with better assemblies or profile searches;
- synteny is not conserved enough to distinguish orthology;
- receptor expression does not localize to relevant sensory cells;
- functional assays show unrelated primary roles;
- neuroanatomical and receptor changes cannot be temporally or mechanistically linked.

### Welfare and safety boundary

This phase is computational and literature-based. It authorizes no capture, invasive procedure, forced conditioning or welfare-sensitive experiment. Later behavioural work must preserve choice, withdrawal and species-appropriate welfare criteria.

## Primary sources

- Albertin et al., *The octopus genome and the evolution of cephalopod neural and morphological novelties*, Nature (2015), DOI: [10.1038/nature14668](https://doi.org/10.1038/nature14668)
- Albertin et al., *Genome and transcriptome mechanisms driving cephalopod evolution*, Nature Communications (2022), DOI: [10.1038/s41467-022-29748-w](https://doi.org/10.1038/s41467-022-29748-w)
- Schmidbaur et al., *Emergence of novel cephalopod gene regulation and expression through large-scale genome reorganization*, Nature Communications (2022), DOI: [10.1038/s41467-022-29694-7](https://doi.org/10.1038/s41467-022-29694-7)
- Zhang et al., *The genome of Nautilus pompilius illuminates eye evolution and biomineralization*, Nature Ecology & Evolution (2021), DOI: [10.1038/s41559-021-01448-6](https://doi.org/10.1038/s41559-021-01448-6)
- van Giesen et al., *Molecular Basis of Chemotactile Sensation in Octopus*, Cell (2020), PMID: [33125889](https://pubmed.ncbi.nlm.nih.gov/33125889/)
- Kuuspalu et al., *Multiple nerve cords connect the arms of octopuses*, Current Biology (2022), DOI: [10.1016/j.cub.2022.11.007](https://doi.org/10.1016/j.cub.2022.11.007)
- Olson et al., *Neuronal segmentation in cephalopod arms*, Nature Communications (2025), DOI: [10.1038/s41467-024-55475-5](https://doi.org/10.1038/s41467-024-55475-5)

## Next evidence gate

Feature Passport 001 advances from `ONDERZOEK` to `ONDERBOUWD` only after the receptor-gene inventory, alternative-model preregistration and at least one reproducible phylogeny plus synteny check are present and independently reviewed for overclaiming.
