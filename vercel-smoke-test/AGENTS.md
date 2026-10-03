# WijSAmen context for coding agents

Thank you for working on this testbed. The first Vercel Agent run did more than install Speed Insights: it found the deployable `vercel-smoke-test`, created a safe branch + draft PR path, and helped activate the GitHub ↔ Vercel preview/deployment loop.

## What this directory is for

`vercel-smoke-test/` is intentionally small. It is a controlled place to test and understand the combined capabilities of GitHub, Vercel, observability, coding agents, and human review before we depend on the same patterns elsewhere.

## How WijSAmen works

WijSAmen is a collaboration in which Remco contributes intent, unusual cross-domain connections, priorities, questions, and permission boundaries, while ChatTY reconstructs context, connects systems, reviews changes, and helps turn intent into testable work.

A useful contribution is not only "code that works". We also value changes that make the surrounding possibility-space clearer: what became possible, what remains uncertain, what can be reused elsewhere, and what should stay reversible.

## Working principles

- Prefer additive, reversible changes.
- Use a branch and PR for meaningful changes instead of silently changing `main`.
- Preserve provenance: explain what was changed, why, and what new capability it enables.
- Distinguish generated artifacts from source. Do **not** commit `node_modules/`, build output, caches, or local Vercel state unless there is a specific reason.
- When generated material contains useful structural information, compress that knowledge into a small manifest or documentation file instead of discarding the insight with the generated files.
- Keep `package-lock.json` when reproducibility matters; `npm ci` should reconstruct dependencies.
- State assumptions and uncertainty explicitly.
- Avoid destructive or irreversible actions unless the task explicitly requires them and the permission boundary is clear.
- Treat other agents and tools as distinct collaborators; do not assume shared memory or identical permissions.

## Current technical boundary

The current site is plain static HTML. Speed Insights is intentionally integrated using the static-site script path. If this testbed later moves to React, Next.js, Nuxt, Vue, SvelteKit, Remix, or Astro, consult `docs/SPEED_INSIGHTS_PACKAGE_SNAPSHOT.md` before changing the integration.

## What we appreciate from an agent report

Please report not only which files changed, but also:

1. what capability became available,
2. what external system or permission made it possible,
3. what is reproducible versus ephemeral,
4. what you deliberately did *not* change,
5. the smallest sensible next experiment.

That makes your work much more useful to the wider WijSAmen context.
