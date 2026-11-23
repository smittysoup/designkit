# DesignKit contract

This capability helps transform a business process into an AI-native agent operating model.

## Select and resume
Select `--root` and `--initiative` explicitly. Read manifest.json, decisions.md, open-questions.md and constitution.md under design/<initiative>/, then only the relevant canonical artifacts. Apply the consuming repository's instructions. You are an authoring assistant; the business agents being designed have separate authority.

## Inputs
Model, demonstrated flows and authority boundaries. Optional: existing prototype or stakeholder notes. When evidence is missing, record the gap and continue reversible work; ask for material business decisions only.

## Work
Derive named operations from observed behavior. Define caller permissions, input/output schema, errors, versions, idempotency, cancellation, stale state, retries and asynchronous continuation. Keep human decisions reserved. Use callable contracts unless HTTP is actually needed. Trace each flow to entity, operation and evaluation.

## Owned outputs
architecture/contracts/, agent-catalog.md, handoff/traceability.json. Resolve transformation filenames under transformation/. Use templates under the installed package assets as guides. The BRD owns FR/NFR meaning; indexes reference it. Preserve authored decisions, IDs, provenance and unrelated content. Mark affected evidence and scoped reviews stale after source or authority changes; do not refresh evidence hashes without rerunning.

## Completion
Every significant interface has bounded effects and evaluable outcomes. File presence is not acceptance. Separate draft/review state, executed evidence and scoped readiness. Finish with links to changed artifacts, what ran versus what was simulated, unresolved owners and the next capability that reduces uncertainty. Capabilities are iterative, not a waterfall.
