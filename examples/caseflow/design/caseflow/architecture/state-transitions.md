# State transitions

Synthetic CaseFlow reference. Authored design hypothesis; no stakeholder acceptance or production performance claim.

## Transitions

| From | Trigger / authority | To | Effect / alternate |
|---|---|---|---|
| question | OP-Answer / assigned requester | resumed | Persist nonempty Response; reject stale or unauthorized |
| resumed | OP-Prepare / bounded agent | package | Evidence receipt + current Package; unavailable → error |
| package | OP-Review / specialist | reviewed | Bind review to revision |
| reviewed | OP-Decide / approver | complete | Decision recorded; return → question |
| package/reviewed | OP-Revise / requester | resumed | Invalidate review; new case version |
| question/resumed | tool unavailable | error | Preserve answer; no success |
| error | OP-Retry / specialist | question or resumed | One demo retry; further failure requires intervention |
| error | OP-Cancel / specialist | cancelled | No continuation |
| any | inspect phase / participant | unchanged | Navigation has no business effect |
