# Evaluation

Evaluate packetisation on correctness before compression.

## Primary metrics

### Semantic retention

Check whether the packet preserves every source item that can change execution, safety, acceptance or interpretation.

Score each L0 item as:

* retained exactly or canonically;
* safely referenced;
* weakened;
* missing;
* contradicted.

Any missing or contradicted L0 item is a hard failure.

### Ambiguity

Ask two independent decoders or reviewers to reconstruct the required action and constraints.

Fail when plausible interpretations differ on:

* scope;
* authority;
* invariants;
* gaps;
* side effects;
* acceptance evidence;
* stop conditions.

### Reference resolvability

Every decision-critical `REF` must be available to the receiving environment.

A packet that is smaller only because it points to inaccessible context is not valid compression.

### Evidence sufficiency

For RESULT and REVIEW packets, check that the evidence actually supports the claimed status or verdict.

A summary such as `tests passed` is weaker than named test results when the decision depends on a particular failure mode.

## Efficiency metrics

Measure after correctness passes.

Preferred metrics:

* input tokens under the actual target tokenizer;
* bytes;
* characters;
* whitespace-delimited words;
* repeated context avoided through references;
* frontier tokens consumed per accepted outcome.

Do not report model token savings from character counts alone.

## Benchmark design

Compare at least these variants:

1. original natural language;
2. compact structured English;
3. SP/1 semantic packet;
4. extreme symbolic encoding if testing the hypothesis.

Use the same underlying task and evidence.

Judge:

* task success;
* retained invariants;
* missed prohibitions;
* false facts introduced;
* escalation accuracy;
* acceptance accuracy;
* token use;
* decoder effort or extra turns required.

## Recommended acceptance gate

Accept a packetisation approach only when:

1. no L0 semantic regressions are observed in the evaluation set;
2. task and review quality are at least equivalent to the natural-language baseline;
3. references remain resolvable;
4. measured token or context savings are material enough to justify the added protocol complexity.

A smaller packet that causes rediscovery, clarification or incorrect acceptance is a net loss.
