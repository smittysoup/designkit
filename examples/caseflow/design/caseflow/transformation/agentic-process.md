# Redesigned operating model

Synthetic CaseFlow reference. Authored design hypothesis; no stakeholder acceptance or production performance claim.

## Redesign

FUT-1 combines clarification and evidence preparation into AGENT-Prepare responsibility for a reviewable package. Eliminate duplicate email transcription; retain deterministic validation/version checks. FUT-2 simplifies review coordination with a shared versioned package and retains specialist and approver human judgments. FUT-3 preserves explicit intervention on unavailable tools. Variable evidence and missing information justify one bounded preparation agent, not an agent per screen.

## Authority

AGENT-Prepare may read permitted case facts, ask a question, consume the assigned response and prepare a package. It cannot approve, purchase or communicate externally. HUMAN-Requester may answer and propose revisions; HUMAN-Specialist may review/retry/cancel; HUMAN-Approver decides only a specialist-reviewed current package.

## Recovery

FLOW-Recover stops on tool failure, retains answer/context, and permits one specialist-triggered simulated retry. A second failure requires cancellation/investigation. Requirement changes invalidate review before resumed preparation. No automatic final decisions. Unknown production deadlines and retry budgets are Q-1.
