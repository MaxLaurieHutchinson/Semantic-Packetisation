# Contributing

Keep Semantic Packetisation small. Changes should improve semantic retention, clarity or reliability rather than compression ratio alone.

## Run the checks

Use Python 3.10 or newer from the repository root:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The suite checks the parser, record vocabulary, command behaviour, complete example packets and evaluation catalogue structure. It does not run model trials or prove semantic retention. The optional tokenizer is not required for these checks.

## Useful contributions

Cases that lose an invariant, hide uncertainty, rely on inaccessible references or mislead a reviewer are especially valuable. Include the source, resulting packet and a clear explanation of what changed or went missing.

For protocol or validator changes, include a failing regression test, a before and after example, the semantic property affected and any compatibility implications. Keep the protocol and accepted record vocabulary aligned.

Preserve `evals/` for scenario data and evaluation assets, and `tests/` for deterministic regression checks. A scenario definition is not evidence that a model passed it.

## Claims and scope

Label illustrative examples and distinguish structural checks from semantic or behavioural evidence. Report actual token counts only with a named tokenizer; never relabel character reductions as token savings.

Avoid new dependencies, protocol fields or abstraction layers unless a concrete use case needs them. Keep installation instructions specific to what has actually been packaged or tested.
