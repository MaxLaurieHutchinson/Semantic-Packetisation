# Semantic Packetisation

Semantic Packetisation is an Agent Skill for turning verbose prompts, model handoffs and worker results into compact, loss-bounded semantic packets.

The optimisation target is not the shortest text.

It is the smallest payload that still preserves everything required for the next model to execute or judge correctly.

> Route the minimum sufficient semantics.

## Why

Long agentic workflows repeatedly pay for the same context:

* prior decisions are restated in prose;
* large artefacts are copied instead of referenced;
* workers return narrative summaries rather than evidence;
* strong models rediscover work already completed by cheaper models;
* explicit uncertainty and gaps get softened during summarisation.

Semantic Packetisation converts that traffic into a small intermediate representation called `SP/1`.

```text
verbose context
    -> classify loss boundaries
    -> SP/1 task/context packet
    -> worker
    -> SP/1 result packet
    -> reviewer
```

## What makes this project specific

This is not a claim to have invented compact agent communication.

The specific focus is decision-sufficient model routing:

1. preserve invariants, prohibitions and authority as first-class records;
2. preserve genuine gaps and uncertainty rather than smoothing them away;
3. pass durable context by reference when the receiver can resolve it;
4. return evidence packets instead of long worker narratives;
5. optimise frontier-model input around the evidence needed for judgement;
6. make loss policy explicit so compression is bounded and reviewable.

The intended outcome is lower context and quota use without weakening acceptance quality.

## Quick example

Verbose instruction:

```text
The evidence review is complete. The previous read-only instruction no longer applies.
Implement V2 in the existing worktree, but checkpoint V1 first. Do not restart broad
review. Use the approved architecture and evidence ledger as authority. Render and
verify the result. Do not push, publish, submit or contact anyone.
```

Packet:

```text
SP/1 TASK
STATE evidence_review_complete
STATE readonly_superseded
GOAL build_v2
SCOPE existing_worktree
AUTH V2_ARCH
AUTH EVIDENCE_LEDGER
INVARIANT checkpoint_v1_first
INVARIANT no_broad_rediscovery
POST render
POST deterministic_verify
SIDE_EFFECT forbid=push,publish,submit,contact
EXECUTE yes
```

The prose disappeared. The decision-critical semantics did not.

## Loss classes

`L0` means preserve exactly or canonically.

Examples: dates, IDs, paths, invariants, prohibitions, authority, gaps, uncertainty, evidence status, security and consistency constraints.

`L1` means preserve meaning but condense wording.

Examples: rationale, narrative context and implementation history.

`L2` means safe to omit for the next decision.

Examples: pleasantries, repeated explanations and redundant process narration.

If classification is uncertain, use the safer class.

## Packet types

`TASK` carries instructions to a worker.

`CONTEXT` freezes reusable facts, authority, gaps and references.

`RESULT` carries concrete evidence back from execution.

`REVIEW` carries the smallest sufficient evidence set for a consequential judgement.

See `references/protocol.md` for the SP/1 grammar.

## Example result packet

```text
SP/1 RESULT
ID payment_retry_07
STATUS PASS
CHANGED src/payments/callback.py
CHANGED tests/payments/test_callback.py
VERIFIED unit_tests=18/18
VERIFIED integration_tests=6/6
EVIDENCE duplicate_callback_test=PASS
DEVIATION none
REF diff=git:4f92a1c role=evidence
```

The reviewer can spend its context on judgement rather than rediscovery.

## Installation

This repository follows the Agent Skills layout.

The runtime entry point is `SKILL.md`.

Supporting material lives under `references/` and deterministic utilities under `scripts/`.

## Validation

Validate packet structure:

```bash
python scripts/validate_packet.py packet.sp
```

Compare source and packet payload sizes:

```bash
python scripts/compare_payloads.py source.txt packet.sp
```

The comparison script reports token counts only when `tiktoken` is installed. Character and word counts are labelled as proxies.

Structural validation does not prove semantic completeness. A valid packet can still be wrong if it omitted an L0 fact.

## Evaluation

`evals/packetisation_scenarios.json` contains adversarial cases around:

* side-effect preservation;
* genuine gaps;
* inaccessible references;
* evidence sufficiency;
* authority conflicts;
* cases where packetisation should not be used.

See `references/evaluation.md` for the evaluation model.

## Related work

PAIRL is a compact, human-readable, machine-parseable format for agent-to-agent communication. It includes pointer-first state, evidence records and explicit separation between lossy and lossless information. Semantic Packetisation has a narrower boundary: it is an Agent Skill and intermediate representation for decision-sufficient model routing, evidence return and frontier review rather than a general transport format.

PAIRL: https://github.com/dwehrmann/PAIRL

The phrase "semantic packet" also appears in unrelated work on secure semantic communications. This project does not claim ownership of the phrase.

## Relationship to Astra Quota Router

Semantic Packetisation is complementary to Astra Quota Router.

Astra Quota Router decides where reasoning should happen.

Semantic Packetisation decides how much meaning needs to cross the boundary.

Together:

```text
risk-based routing
    +
minimum sufficient semantics
    +
evidence-based acceptance
```

## Status

Experimental v0.1.

The next proof point is empirical: compare natural language, compact structured English, SP/1 and extreme symbolic encoding across multiple models, then measure semantic retention, task success, escalation accuracy, acceptance accuracy and actual token use.

## License

MIT.
