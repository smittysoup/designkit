# ADR 001: standalone core and explicit versioned bridge

Status: implemented for 0.1.0. Evidence: [mechanics audit](../spec-kit-mechanics.md).

Choose a small Python CLI, portable Markdown/JSON assets, two thin skill renderers
and a manual/file Spec Kit bridge. Python 3.11+ works without a shell-specific
installer. JSON Schema provides structural validation. No global config changes,
network service, workflow runtime or agent orchestration is introduced.

Considered an upstream extension/preset: attractive distribution hooks, but not
necessary for portable transformation authoring and introduces version/lifecycle
coupling. Presets can affect plan generation; the audit observed that forced core
reinit overwrites a custom template. We avoid depending on that behavior. A fork
or CLI clone adds excessive maintenance and does not solve semantic reconciliation.

Generated instructions have a hash ledger; update refuses edits or unowned
collisions after preflight. Initiative artifacts are never regenerated. Removal
only deletes unchanged generated files. The existing AGENTS.md, `.specify` and
unrelated files are untouched. Consumer guidance is a separate suggested file.

The bridge freezes an explicit initiative under a selected feature's
`designkit-input/`, maps the logical model and contracts, and never overwrites
downstream artifacts. Differing downstream bytes are conservatively conflicts
until a named reviewer records a reason, evidence, affected IDs and both hashes.
This may flag harmless formatting changes; that is preferable to silently losing
authority or business meaning. Human semantic review remains necessary.

Without Spec Kit, the same guides, manifest, checker and ZIP snapshot remain useful.
The tradeoff is manual context invocation and explicit reconciliation, not a
promise of automatic agent loading. Update the pinned mechanics evidence when
upstream behavior changes; do not silently widen support. Package distribution
name `designkit-process` is local/Git installation only; no PyPI namespace or
publication is claimed.
