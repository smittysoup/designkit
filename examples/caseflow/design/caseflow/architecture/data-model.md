# Logical data model

Synthetic CaseFlow reference. Authored design hypothesis; no stakeholder acceptance or production performance claim.

## Entities

ENTITY-Case: caseId, requesterId, specialistId, approverId, version, state and requirement. ENTITY-Question: questionId, caseId, assignedRequesterId, version, status. ENTITY-Response: responseId, questionId, authorId, text and expectedVersion. ENTITY-Package: packageId, caseId, sourceVersion, evidenceRefs, reviewStatus. ENTITY-Decision: decisionId, packageId, approverId, outcome. ENTITY-Work: WorkDefinition defines stable milestone; WorkItem binds it to a case; AgentRun is one execution; ToolReceipt records call outcome. Optional decision is absent until authorized judgment.

## Relationships

One Case has many Questions, Packages and WorkItems. A Question has at most one accepted Response per question version. Package revisions never reuse prior approvals. Each WorkItem has many AgentRuns; each run may have many ToolReceipts. Decisions bind exactly one package revision. See diagrams/entity-model.mmd and rendered companion.

## Ownership

Case service is the logical source of truth. People own their attributed responses and decisions; agent owns derived package preparation. Conversation text and ephemeral reasoning are not business records. The demo stores one aggregate in localStorage; production retention and access policy must be decided. Case membership controls reads; assigned role and expected version control writes.

## Invariants

Only assigned requester answers; only specialist reviews/retries/cancels; only approver decides a current reviewed package. Revised requirements invalidate package review. TOOL_UNAVAILABLE cannot produce success. Duplicate operation keys must not schedule two continuations. These production invariants exceed the client-side demonstration.

## Lifecycle

question → resumed → package → reviewed → complete. question/resumed → error → retry to question/resumed or cancelled. package/reviewed → revised requirement → resumed. reviewed → returned → question. Final decision has an attributable actor and immutable package revision. See state-transitions.md.

## Data movement

FLOW-Clarify: requester → OP-Answer(questionId,text,expectedVersion,key) → validate role/version, preserve Response → eligible WorkItem → AgentRun. FLOW-Prepare: AgentRun + Case/Response → TOOL-Evidence → ToolReceipt → OP-Prepare → versioned Package → specialist. FLOW-Decide: specialist OP-Review → reviewed Package → approver OP-Decide → Decision + Case completion. FLOW-Recover: unavailable receipt → stopped WorkItem → specialist OP-Retry → new AgentRun using saved Response, or OP-Cancel → terminal state. FLOW-Revise: requester OP-Revise → new Case version → invalidate Package review → new preparation run. Payloads and allowed effects are in contracts/operations.json; named arrows in diagrams/data-flow.mmd distinguish state from messages.

| Trigger / caller | Input | Responsible transformation | Output / persistence | Contract and authority |
|---|---|---|---|---|
| Requester answer | questionId, text, version, key | Validate assignment; preserve response; resume work | Response, eligible WorkItem, AgentRun | OP-Answer / requester |
| Agent preparation | Case, Response, permitted evidence | Gather evidence and derive package | ToolReceipt, Package(sourceVersion) | OP-Prepare / AGENT-Prepare |
| Specialist review | current Package revision | Judge completeness | Review bound to package | OP-Review / specialist |
| Approver decision | reviewed Package, outcome | Retain human business judgment | Decision; completed Case | OP-Decide / approver |
| Requester change | Case, revised requirement, version | Invalidate review; resume preparation | revised Case; new AgentRun | OP-Revise / requester |
| Tool unavailable | failed ToolReceipt, WorkItem | Stop, retain context, request intervention | error state; retry or cancellation | OP-Retry / OP-Cancel / specialist |
