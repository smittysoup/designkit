# Authoring and readiness

Select one bounded business process with `init --process ... --outcome ...`.
Templates deliberately contain TODO markers. Replace them with concrete evidence,
stable IDs and owned unknowns; do not fill them with invented numbers or acceptance.
The seven guides under `designkit/assets/commands/` define inputs, output ownership,
context loading, preservation, completion and next activity.

## Artifact contract

Each initiative has a manifest (schema 1.0) and four connected packages:

* Transformation + living BRD: current/future work, agent catalog, evaluation plan,
  outcomes, FRs, NFRs, rules, acceptance scenarios, decisions and owned questions.
* Experience: journeys, screen inventory, actual captures, guidance and runnable
  prototype. Capture state, route, fixture, viewport, time and source hash.
* Model: substantive `architecture/data-model.md`, state table, entity/data-flow/
  before-and-after process diagrams and inspected renders. Explain identity,
  cardinality, ownership, source versus derived data, invariants, versions,
  lifecycle and function-to-function inputs, transformations and persistence.
* Contracts: callable or appropriate transport schemas with operation IDs, caller
  authority, input/output, errors, versioning, retries, cancellation and idempotency.

The JSON manifest schema is packaged at `designkit/assets/manifest.schema.json`.
`records` is an initiative-scoped index of stable IDs with canonical `path` and
`refs`. Keep `handoff/traceability.json` equal to that index. Do not reassign IDs
when wording changes. Requirement records link screens and evaluations; flows
link entities and operations; agents link tools and evaluations; current work
links future responsibilities with a disposition and reason. Authority is an
explicit structured boundary as well as a reviewed explanation.

Add authored artifacts to `manifest.artifacts` with a unique ART ID, relative path,
SHA-256 and review_state. After edits, recompute the artifact SHA-256 using Python
`hashlib.sha256(Path(path).read_bytes()).hexdigest()`. Never update an evidence
source hash without rerunning the evidence. The example maintenance script is
scoped to the example and indexes its files; it is not a general customer importer.

## Three independent facts

1. Artifact review state: draft, in_review, accepted.
2. Evidence execution: not_run, passed, failed, stale; level is structural,
   simulation, live_agent or production.
3. Handoff readiness: derived ready/not_ready for the declared scope.

The checker finds schema errors, absent/incomplete required prose, duplicate or
unresolved IDs, incomplete flow coverage, undefined authority, broken captures,
stale hashes, unexecuted evaluations, unowned questions and missing/stale reviews.
It cannot judge whether prose is true or a reviewer is genuine. A malicious or
mistaken record can lie; humans remain accountable for meaning and acceptance.

Required review roles are business, product, experience and engineering. One
person may fill several roles. Reviews include reviewer, evidence path, status,
`synthetic: false`, covered `paths` and `revision` computed by
`designkit.cli.artifact_revision(initiative_root, paths)`. Review scopes must cover
the key artifacts for their role. Updating an unrelated artifact does not
invalidate a scoped review; changing a covered artifact does. Fictional reviews
cannot satisfy readiness. CaseFlow intentionally has no accepted human reviews.

Material open questions block readiness; nonblocking downstream obligations need
owners, acceptance conditions and a verification plan. Exports retain honest gaps.
Structural success is necessary but not sufficient for semantic acceptance.

## Downstream differences

`bridge` creates a frozen `designkit-input/` copy with hashes and target mappings.
Choose a new feature directory/version for a new source snapshot. Planning agents
must explicitly read the input brief and all linked source artifacts; bridge does
not invoke a native agent or assume automatic context loading.

`reconcile` requires a downstream model and contracts and compares them to the
frozen source. Changed bytes remain conflicts until a human reviews them. A
`reconciliation.json` array at the feature root records each accepted refinement:

```json
[{"target":"data-model.md","source_sha256":"<recorded source hash>",
  "target_sha256":"<actual output hash>","status":"accepted",
  "reviewer":"<identified responsible person>","synthetic":false,
  "reason":"<why meaning and authority are preserved or approved to change>",
  "affected_ids":["ENTITY-Case"],"evidence":"reviews/model-change.md"}]
```

Record mappings and reasons in `handoff/reconciliation.md` too. A source hash
change, missing output or unreviewed difference blocks conformance. Identical bytes
prove preservation, not business correctness. Cross-feature shared entities require
the same source meaning or an explicit shared decision. A handoff may remain
not_ready even when downstream copies conform.
