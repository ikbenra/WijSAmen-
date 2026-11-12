# OctoCorpus autonomous laboratory — checkpoint v1
This is a **bounded deterministic software optimization experiment**, not a generative AI agent, consciousness test, or a biological RNA-editing model.

## How it works
The C, Si and SiC+N subsystems have separate small policies. A shared evaluator proposes one-step policy variations, selects improvements on a synthetic training split and rejects holdout regressions. Each accepted change is logged; the stable baseline remains available in source code. The head/nodule is represented by the evaluator and shared checkpoint.

## Cloud execution
Run the **OctoCorpus autonomous bounded research** workflow on branch `octocorpus/triad-consciousness-v01` via GitHub Actions > Run workflow. The workflow restores the most recent branch-scoped checkpoint through GitHub Actions cache, runs six unit tests, continues bounded optimization, and saves a new checkpoint to cache and an inspectable artifact.

Important: cache eviction can reset state. Artifacts are retained for 30 days. This is **best-effort persistence**, not an archival database. There is no paid external model, no secrets, no remote publishing, no automatic merge, no unattended physical control, and no scheduled continuous execution. Each run has a 15-minute ceiling and stops early at convergence.

## Evaluation limitations
Only eight toy stimuli, of which two are held out. No real-world transfer, self-awareness, functional structural growth or scientifically meaningful meta-learning has been established. The held-out split is repeatedly observed during selection, so it is a regression gate, not an independent final test. Next build: independent unseen evaluation, energy budget, versioned structural edits, ablation and richer tasks. Never present the synthetic score as proof of consciousness.

## Recovery
Download the latest artifact `octocorpus-autonomy-state` or rerun workflow (cache restore). For hard reset, run on a fresh branch or clear cache. Branch review is required before merging to main.
