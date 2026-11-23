# CaseFlow living business requirements

Synthetic CaseFlow reference. Authored design hypothesis; no stakeholder acceptance or production performance claim.

## Outcomes

OUT-1: Give a specialist a grounded, reviewable workshop preparation package without repeated manual transcription. Scope is one synthetic case and its clarification, revision, tool failure and final human decision. Production identity and external commitments are excluded. Baseline cycle time, cost and rework are unknown; measure before a pilot.

## Functional requirements

FR-1: Requester answers an attributed question, work resumes, and the answer survives reload. FR-2: Specialist reviews the current package before an approver decides. FR-3: Tool failure stops preparation until specialist retry or cancellation. FR-4: Requester revisions invalidate prior package review. FR-5: Inspection of milestones does not advance work. The BRD is the canonical requirement register.

## Non-functional requirements

NFR-1: Production must reject unauthorized or stale-version writes and deduplicate continuation by operation key. Engineering lead owns executable negative integration tests before release. NFR-2: Users must operate the prototype with keyboard controls at desktop and mobile emulated widths; automated walkthrough is partial accessibility evidence, not WCAG certification. Production latency/cost targets remain Q-1.

## Rules

RULE-1: Agents prepare; a specialist reviews; only an assigned approver decides. RULE-2: Package evidence and review bind to the case revision. RULE-3: One explicit retry is a synthetic exercise limit, not an agreed production policy. Changes to authority need business review.

## Acceptance

EVAL-1: Answer → resumed preparation → reviewable package → specialist review → approver decision. EVAL-2: Tool outage → stopped work → specialist retry → restored context. EVAL-3: Wrong role cannot answer or approve in the visible UI. EVAL-4: Revision invalidates review and phase inspection is read-only. Browser simulation cannot prove server authorization or durable scheduling.
