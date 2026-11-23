# DesignKit model

This capability helps transform a business process into an AI-native agent operating model.

## Select and resume
Select `--root` and `--initiative` explicitly. Read manifest.json, decisions.md, open-questions.md and constitution.md under design/<initiative>/, then only the relevant canonical artifacts. Apply the consuming repository's instructions. You are an authoring assistant; the business agents being designed have separate authority.

## Inputs
Demonstrated scenarios, catalog, rules and validation findings. Optional: existing prototype or stakeholder notes. When evidence is missing, record the gap and continue reversible work; ask for material business decisions only.

## Work
Define identity, relationships, source of truth, access, retention, versions, invariants and lifecycle. Separate case, work definition, work item, agent run, response, human decision and tool receipt. Map trigger/caller, input, transformation, output, persistence and authority for every significant flow. Create entity, data-flow and before/after process Mermaid sources and inspect renders.

## Owned outputs
architecture/data-model.md, architecture/diagrams/, architecture/state-transitions.md. Resolve transformation filenames under transformation/. Use templates under the installed package assets as guides. The BRD owns FR/NFR meaning; indexes reference it. Preserve authored decisions, IDs, provenance and unrelated content. Mark affected evidence and scoped reviews stale after source or authority changes; do not refresh evidence hashes without rerunning.

## Completion
All significant flows explain durable state, payloads and recovery. File presence is not acceptance. Separate draft/review state, executed evidence and scoped readiness. Finish with links to changed artifacts, what ran versus what was simulated, unresolved owners and the next capability that reduces uncertainty. Capabilities are iterative, not a waterfall.
