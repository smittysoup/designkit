# Contract package

Synthetic CaseFlow reference. Authored design hypothesis; no stakeholder acceptance or production performance claim.

## Operations

[operations.json](operations.json) defines OP-Answer, OP-Prepare, OP-Review, OP-Decide, OP-Revise, OP-Retry and OP-Cancel. These are logical callable contracts derived from observed UI states, not deployed HTTP APIs. FLOW-Clarify, FLOW-Prepare, FLOW-Decide, FLOW-Recover and FLOW-Revise map inputs to preserved business records.

## Authority

Assigned requester supplies facts; agent reads case-scoped evidence and prepares; specialist reviews/retries/cancels; approver decides reviewed current package. A role selector is not production access control. Server identity and membership enforcement are required acceptance conditions.

## Errors

Reject unauthorized, empty, stale or out-of-state writes without side effects. TOOL_UNAVAILABLE preserves context and stops work. Persist idempotency key and prior receipt atomically; repeat delivery returns prior result without a second run. Cancellation must win against a late continuation.

## Versioning

Version 1.0 logical interfaces. expectedVersion must match authoritative object version. Package derivations retain source case version and evidence references. Breaking meaning or authority changes require an owned decision and reconciliation; additive physical storage details may be refined downstream.
