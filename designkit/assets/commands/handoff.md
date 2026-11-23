# DesignKit handoff

This capability helps transform a business process into an AI-native agent operating model.

## Select and resume
Select `--root` and `--initiative` explicitly. Read manifest.json, decisions.md, open-questions.md and constitution.md under design/<initiative>/, then only the relevant canonical artifacts. Apply the consuming repository's instructions. You are an authoring assistant; the business agents being designed have separate authority.

## Inputs
Scoped artifacts, reviews, evidence, open questions and target version. Optional: existing prototype or stakeholder notes. When evidence is missing, record the gap and continue reversible work; ask for material business decisions only.

## Work
Run designkit check with explicit root and initiative. Export a versioned snapshot even if partial, preserving not_ready gaps. Bridge into an explicit feature directory, instruct the downstream assistant to read every input, then reconcile downstream data-model.md and contracts. Never overwrite accepted source or equate hashes with semantic approval.

## Owned outputs
handoff/, manifest.json. Resolve transformation filenames under transformation/. Use templates under the installed package assets as guides. The BRD owns FR/NFR meaning; indexes reference it. Preserve authored decisions, IDs, provenance and unrelated content. Mark affected evidence and scoped reviews stale after source or authority changes; do not refresh evidence hashes without rerunning.

## Completion
Portable evidence, explicit readiness and reviewed downstream differences. File presence is not acceptance. Separate draft/review state, executed evidence and scoped readiness. Finish with links to changed artifacts, what ran versus what was simulated, unresolved owners and the next capability that reduces uncertainty. Capabilities are iterative, not a waterfall.
