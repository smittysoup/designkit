# Human-agent journeys

Synthetic CaseFlow reference. Authored design hypothesis; no stakeholder acceptance or production performance claim.

## Journey

SCREEN-Question shows the requester missing information. OP-Answer → SCREEN-Resumed → OP-Prepare → SCREEN-Package. Specialist reviews; SCREEN-Decision permits an approver decision; SCREEN-Complete records the result. All roles share CASE-104 and local fixture state. Reload keeps the answer.

## Alternatives

SCREEN-Error stops on evidence failure. A specialist retries or cancels. Requester requirement revisions invalidate earlier review; approver may return for clarification. Inspecting Intake/Preparation/Decision only changes the inspected phase. Role switch is a demonstration control, not authentication. Launch: python -m http.server 4173 --directory experience/prototype; open http://localhost:4173. Reset synthetic case clears the shared fixture.
