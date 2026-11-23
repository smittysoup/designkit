# Transformation evaluation plan

Synthetic CaseFlow reference. Authored design hypothesis; no stakeholder acceptance or production performance claim.

## Scenarios

EVAL-1 uses CASE-104 and 24 participants: expected attributed answer, resumed preparation, reviewable package and human final decision. EVAL-2 injects TOOL_UNAVAILABLE: no package/decision, preserved answer, specialist retry recovers. EVAL-3 selects the wrong role: answer/review/approval controls disabled. EVAL-4 revises to 30 participants: package review invalidated; phase inspection changes no business state.

## Measures

Product and business owner must establish baseline touch time, clarification count, rework and useful package rate from real cases. Targets are unknown, owned by Q-1. Engineering must measure live-agent unsupported claims, unauthorized actions, completion, tool cost and latency. Synthetic click speed is not business evidence.

## Verification

Browser evidence is simulation and UI behavior only. Before production: engineering tests server identity, case membership, optimistic versions, transaction durability, duplicate continuation, cancellation races, outage recovery and live-agent grounding. Business and design review the actual operating model; no such review is claimed here.
