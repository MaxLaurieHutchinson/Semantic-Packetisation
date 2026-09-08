---
name: semantic-packetisation
description: Compile verbose prompts, handoffs, context and worker results into compact, loss-bounded semantic packets for model-to-model communication and quota-aware orchestration. Use when reducing repeated context, creating task or evidence packets, passing large artefacts by reference, preparing frontier-model review inputs, comparing verbose versus packetised instructions, or preserving decision-critical facts, invariants, uncertainty, provenance and side-effect boundaries while removing redundant prose.
---

# Semantic Packetisation

Convert verbose natural-language context into a compact intermediate representation without discarding information required for a correct decision.

Optimise for semantic density, not character density.

Read `references/protocol.md` when constructing or validating packets.
Read `references/examples.md` when a concrete transformation example would help.
Read `references/evaluation.md` when comparing packet quality or token efficiency.

## Core rule

Preserve the minimum sufficient semantics for the next decision.

Never compress away:

* exact facts that affect correctness;
* authority and provenance;
* invariants and prohibitions;
* uncertainty and unresolved gaps;
* evidence required for acceptance;
* stop or escalation conditions;
* external side-effect boundaries.

Prefer references to repeated payloads when the receiving model can resolve them.

## Workflow

1. Identify the packet consumer and the decision it must make.
2. Classify source information by loss policy.
3. Extract decision-critical fields.
4. Replace reusable large context with resolvable references.
5. Emit the smallest readable SP/1 packet that remains sufficient.
6. Check semantic completeness before returning it.
7. For delegated work, request a compact RESULT packet rather than a prose narrative.
8. For consequential review, give the frontier model the packet plus only the evidence it needs to judge.

## Loss policy

Classify source information into three classes.

### L0 exact

Preserve exactly or in a canonical equivalent form:

* names, dates, numbers, IDs, paths and versions;
* hard constraints, prohibitions and side-effect limits;
* invariants and acceptance criteria;
* explicit gaps and uncertainty;
* evidence status and provenance;
* authority ordering;
* security, consistency, concurrency and trust-boundary facts.

### L1 condensed

Preserve meaning but shorten wording:

* rationale;
* narrative background;
* implementation history;
* explanatory context;
* repeated descriptions whose detail is not required downstream.

### L2 disposable

Omit when it does not alter interpretation:

* pleasantries;
* repeated instructions;
* conversational filler;
* restatements already represented structurally;
* process commentary that does not affect execution or acceptance.

When uncertain between two classes, choose the safer class.

## Packet forms

Use four packet types.

### TASK

Use for implementation, investigation, transformation or delegation.

Include only fields needed for execution. Common records:

`GOAL`, `STATE`, `ACTION`, `SCOPE`, `AUTH`, `CASE`, `INVARIANT`, `FACT`, `REF`, `EVIDENCE`, `GAP`, `UNCERTAIN`, `VERIFY`, `STOP`, `SIDE_EFFECT`, `POST`, `RETURN`, `EXECUTE`.

### CONTEXT

Use to freeze reusable context once and reference it from later packets.

Common records:

`FACT`, `AUTH`, `INVARIANT`, `GAP`, `UNCERTAIN`, `REF`.

### RESULT

Use for worker-to-reviewer evidence return.

Prefer evidence over narrative. Common records:

`STATUS`, `CHANGED`, `VERIFIED`, `EVIDENCE`, `METRIC`, `ASSUMPTION`, `DEVIATION`, `RISK`, `UNRESOLVED`, `REF`, `DECISION`.

### REVIEW

Use when a stronger model must judge evidence rather than redo the work.

Common records:

`GOAL`, `CRITERION`, `EVIDENCE`, `RISK`, `UNCERTAIN`, `REF`, `VERDICT`, `REVISION`.

## Reference policy

Use `REF` only when the receiver can resolve the target.

Prefer a stable artefact ID, content-addressed reference, repository path, file path, connector ID or other durable pointer.

Do not replace critical content with an inaccessible reference. If resolution is uncertain, inline the minimum required L0 content and include the reference as provenance.

When integrity matters, include a version, commit or content hash where available.

## Compression discipline

Keep keywords short and stable.

Keep unique evidence readable.

Do not invent symbolic shorthand such as arbitrary glyphs merely to reduce characters. Opaque encodings increase decoding cost and ambiguity.

Do not assume fewer characters means fewer model tokens. Measure when token efficiency matters.

Do not compress an instruction if the compressed form requires more reasoning to reconstruct than the original saves.

Do not force packetisation for already-short prompts.

## Semantic completeness check

Before returning a packet, verify:

1. Can the receiver state the goal without consulting omitted prose?
2. Are all L0 facts present or safely referenced?
3. Are authority and precedence unambiguous?
4. Are genuine gaps still visible as gaps?
5. Are unresolved claims marked rather than silently promoted to fact?
6. Are stop conditions and side effects preserved?
7. Is the required evidence explicit?
8. Could two reasonable models decode the packet differently in a way that changes the outcome?

If the answer to 8 is yes, expand the ambiguous field.

## Handoff rule

For expensive model routing, separate planning from execution and execution from acceptance.

Use this shape when appropriate:

```text
Human intent
    -> TASK packet
    -> cheaper capable worker
    -> RESULT packet
    -> frontier REVIEW packet
    -> decision
```

Pass the frontier reviewer actual evidence or resolvable evidence references. Do not ask it to repeat broad discovery merely because the worker returned a summary.

## Output rules

When the user asks to packetise content, return:

1. the packet;
2. a brief note listing any semantics deliberately omitted or downgraded from L0 to L1, only when that distinction is material;
3. a warning if references cannot be guaranteed resolvable.

When the user asks for maximum compactness, compress L1 aggressively but keep L0 explicit.

When the user asks for a human-readable handoff, favour meaningful words such as `AUTH`, `GAP`, `VERIFY` and `SIDE_EFFECT` over cryptic abbreviations.

When validating an existing packet, use `scripts/validate_packet.py` if executable tools are available. Treat structural validity as necessary but not sufficient: still perform the semantic completeness check.

When comparing a source prompt with a packet, use `scripts/compare_payloads.py` if executable tools are available and report token counts only when a compatible tokenizer is available. Otherwise label character and word reductions as proxies.
