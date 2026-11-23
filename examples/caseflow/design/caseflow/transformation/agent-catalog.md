# Business agent catalog

Synthetic CaseFlow reference. Authored design hypothesis; no stakeholder acceptance or production performance claim.

## Outcome

AGENT-Prepare owns preparation of a grounded package for OUT-1. Trigger: incomplete case intake or a changed requirement. It produces a package, never a business commitment. Stable milestone TASK-Prepare is distinct from WORK-104 and each RUN instance.

## Knowledge

Read the synthetic case brief, participant response and permitted evidence. Do not infer missing participant count. An unavailable or ambiguous source causes a question or escalation. Case records remain authoritative; temporary model context is disposable.

## Tools

TOOL-Evidence reads permitted evidence and returns a receipt or TOOL_UNAVAILABLE. OP-Answer records a requester response; OP-Prepare assembles a package. OP-Review and OP-Decide are human-only. Tool effects must be attributable and versioned.

## State

Persist case version, Question, Response, WorkItem, AgentRun, ToolReceipt and Package. Waiting survives a browser reload in the demonstration; a real service must persist atomically. Cancellation stops continuation.

## Completion

Stop at package ready for specialist review. Business completion occurs only after HUMAN-Approver records a decision. Package must name evidence and current case revision. EVAL-1 covers the loop; EVAL-2 recovery; EVAL-3 limits; EVAL-4 revision.

## Intervention

Ask HUMAN-Requester for missing information. Wait without repeated side effects. HUMAN-Specialist handles tool outages and may retry once in this demo or cancel. Never reinterpret a response as approval. Production retry/time budgets require an owned decision.
