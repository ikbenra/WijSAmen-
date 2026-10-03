# Speed Insights package snapshot

## Why this file exists

The first Vercel Agent run installed `@vercel/speed-insights@2.0.0` and, as a side effect of running `npm install`, initially added the generated `node_modules` tree to its PR.

Those generated files were removed from Git history in the follow-up cleanup. Their **utility was not discarded**:

- `package.json` records the intended dependency.
- `package-lock.json` pins the exact resolved dependency graph.
- `npm ci` reconstructs the install deterministically.
- this document preserves the architectural information we learned by inspecting the generated package.

So the generated files remain recoverable without being permanently versioned.

## Reconstruct the original dependency tree

```bash
cd vercel-smoke-test
npm ci
```

The generated directory is intentionally ignored by Git.

## What the generated package revealed

The installed Speed Insights package contained multiple integration surfaces, not only the static HTML path we currently use.

| Surface | What it tells us |
| --- | --- |
| Generic browser bundle | Supports vanilla/static sites like this smoke test. |
| Astro | A future Astro dashboard can use a native integration. |
| Next.js | A future Next.js UI can use the framework-specific entry point. |
| Nuxt + Nuxt runtime | Vue/Nuxt applications have a dedicated integration path. |
| React | A React interface can use the React component/API. |
| Remix | Remix has a dedicated entry point. |
| SvelteKit | SvelteKit has a dedicated integration. |
| Vue | Vue has a dedicated integration. |
| Type declarations | The package exposes typed APIs for supported environments. |
| Source maps | Debugging can map bundled behavior back to source. |
| README + LICENSE | Usage and licensing information travel with the package. |
| Test/build configuration | The package itself is built and tested across multiple framework targets. |

## Perspective gained

The original generated footprint was roughly 58 files in the PR (plus directory entries). Most were compiled framework bundles, type declarations, source maps, and package metadata.

For the current static test page, committing those files adds noise and duplication. But inspecting them showed something useful: **Speed Insights is not a dead-end experiment tied to this one HTML page.** The same observability layer can follow us if this test evolves into a richer framework-based WijSAmen dashboard.

That is the part worth preserving.

## Current implementation choice

The current static page uses:

```html
<script>
  window.si = window.si || function () {
    (window.siq = window.siq || []).push(arguments);
  };
</script>
<script defer src="/_vercel/speed-insights/script.js"></script>
```

This keeps the smoke test simple while leaving the framework-specific paths available later.

## Rule for future agent runs

Generated dependency trees may be inspected freely when useful, but normally should not be committed. Preserve their meaning through the lockfile plus a concise map like this one when that information broadens the project context.
