# SP/1 Protocol

## Purpose

SP/1 is a compact, readable intermediate representation for carrying the minimum sufficient semantics between models, agents or workflow stages.

It is deliberately narrower than a general agent messaging protocol. Its primary use is task handoff, context reuse, evidence return and consequential review.

## Design principles

1. Preserve decision-critical meaning before optimising size.
2. Prefer stable words over opaque symbols.
3. Separate facts from interpretation.
4. Preserve uncertainty explicitly.
5. Reference large reusable context instead of resending it.
6. Return evidence rather than narrative when the next stage is acceptance.
7. Keep the format easy for both humans and models to inspect.

## Grammar

A packet begins with:

```text
SP/1 <TYPE>
```

`TYPE` must be one of:

* `TASK`
* `CONTEXT`
* `RESULT`
* `REVIEW`

Every subsequent non-empty line is a record:

```text
KEY value
```

A key may appear more than once unless noted otherwise.

Values remain plain text. Use `name=value` inside a value when a small amount of local structure improves clarity.

Avoid quoting unless whitespace or punctuation would otherwise be ambiguous.

## Common records

### ID

Stable packet or task identifier.

```text
ID oxford_v2_17
```

### GOAL

The outcome required from the receiver.

```text
GOAL rebuild_cv_as_three_pages
```

### STATE

Relevant workflow state or transition.

```text
STATE evidence_review_complete
STATE readonly_superseded
```

### ACTION

The operation to perform.

```text
ACTION implement_v2
```

### SCOPE

Files, components or conceptual scope the receiver may touch.

```text
SCOPE cv+dossier+evidence_artifacts
```

### AUTH

A source that has decision authority. List higher-priority authority first unless the value declares precedence explicitly.

```text
AUTH V2_ARCH role=design_authority
AUTH CAREER_EVIDENCE role=evidence_authority
```

### CASE

The intended thesis, framing or target interpretation.

```text
CASE senior_engineer=distributed_systems+python_orchestration+evaluation+retrieval
```

### FACT

A lossless fact.

```text
FACT official_start_date=2021-12-20
```

### INVARIANT

A condition that must remain true.

```text
INVARIANT no_unverified_claims
```

### GAP

A known absence that must remain an absence rather than being filled by inference.

```text
GAP production_multiagent_ownership
```

### UNCERTAIN

A claim whose status is unresolved.

```text
UNCERTAIN historical_dv_status
```

### VERIFY

A fact or claim requiring resolution if it becomes necessary to the task.

```text
VERIFY historical_dv unless=authoritative_source_available
```

### REF

A resolvable pointer to durable context or evidence.

```text
REF V2_ARCH=repo:docs/v2_architecture.md role=authority
REF TEST_LOG=file:artifacts/test.log role=evidence
```

Use a version, commit or hash when stale references would be dangerous.

### EVIDENCE

Evidence required or returned.

```text
EVIDENCE targeted_tests
EVIDENCE diff
EVIDENCE render_review
```

### STOP

A condition that must stop local execution and trigger escalation or clarification.

```text
STOP architecture_change_required
```

### SIDE_EFFECT

External effects that are allowed or forbidden.

```text
SIDE_EFFECT forbid=push,publish,submit,contact
```

### POST

Required operation after the primary action.

```text
POST render
POST deterministic_verify
```

### RETURN

Required output field or artefact.

```text
RETURN cv_path
RETURN verification_status
```

### EXECUTE

Whether the packet authorises execution rather than analysis only.

Treat as singular.

```text
EXECUTE yes
```

### STATUS

RESULT status. Treat as singular.

Allowed values are `PASS`, `PARTIAL`, `FAIL`, `ESCALATE`.

```text
STATUS PASS
```

### CHANGED

Changed artefact or file.

```text
CHANGED src/payments/callback.py
```

### VERIFIED

Verification action and outcome.

```text
VERIFIED unit_tests=18/18
```

### METRIC

Measured result.

```text
METRIC prompt_tokens=812
```

### ASSUMPTION

Assumption introduced during execution.

```text
ASSUMPTION existing_schema_supports_idempotency_key
```

### DEVIATION

Any departure from scope, requested design or expected workflow.

```text
DEVIATION none
```

### RISK

Remaining risk.

```text
RISK migration_not_load_tested
```

### UNRESOLVED

Outstanding issue not resolved by the worker.

```text
UNRESOLVED historical_dv
```

### DECISION

Decision made or requested.

```text
DECISION page3_material_gain=yes
```

### CRITERION

Acceptance or review criterion.

```text
CRITERION no_duplicate_external_effects
```

### VERDICT

REVIEW outcome. Treat as singular.

Recommended values are `ACCEPT`, `REVISE`, `ESCALATE`.

```text
VERDICT ACCEPT
```

### REVISION

Required revision after a `REVISE` verdict.

```text
REVISION add_failure_path_test
```

### LOSS

Optional declaration of the applied loss policy.

```text
LOSS L0=exact L1=condensed L2=discarded
```

## Required fields

### TASK

Require `GOAL`.

Use `EXECUTE yes` when the packet grants permission to act.

### CONTEXT

Require at least one of `FACT`, `REF`, `AUTH`, `INVARIANT`, `GAP`, `UNCERTAIN`.

### RESULT

Require `STATUS`.

For work claimed complete, require concrete `EVIDENCE` or `VERIFIED` records where verification is applicable.

### REVIEW

Require at least one `CRITERION` or `GOAL` and at least one `EVIDENCE` or `REF` when a judgement depends on evidence.

## Authority precedence

Preserve the source order supplied by the author unless explicit precedence is provided.

Never merge conflicting authorities silently.

When authorities conflict:

```text
UNCERTAIN authority_conflict=<summary>
STOP authority_resolution_required
```

## Reference safety

A `REF` is useful only if the receiver can resolve it.

If resolution is not guaranteed:

1. keep the `REF` for provenance;
2. inline the minimum necessary L0 facts;
3. never rely on an inaccessible pointer for an invariant, prohibition or acceptance criterion.

## Canonical packet order

Use this order when it improves readability. Omit unused records.

### TASK

```text
SP/1 TASK
ID
STATE
GOAL
ACTION
SCOPE
AUTH
CASE
INVARIANT
FACT
REF
GAP
UNCERTAIN
VERIFY
EVIDENCE
STOP
SIDE_EFFECT
POST
RETURN
LOSS
EXECUTE
```

### RESULT

```text
SP/1 RESULT
ID
STATUS
CHANGED
VERIFIED
EVIDENCE
METRIC
ASSUMPTION
DEVIATION
RISK
UNRESOLVED
REF
DECISION
```

### REVIEW

```text
SP/1 REVIEW
ID
GOAL
CRITERION
EVIDENCE
REF
RISK
UNCERTAIN
DECISION
VERDICT
REVISION
```

## Non-goals

SP/1 is not:

* a replacement for transport protocols;
* an attempt to expose or transmit model latent states;
* a universal ontology;
* a guarantee of token savings;
* a justification for removing provenance or uncertainty;
* a reason to encode natural language into unreadable symbols.
