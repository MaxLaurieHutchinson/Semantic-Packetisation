# Contributing

Semantic Packetisation is experimental. Contributions are most useful when they include evidence about semantic retention and model behaviour rather than compression ratio alone.

## Good contributions

* adversarial examples where SP/1 loses an invariant;
* cases where a reference becomes unsafe or stale;
* model comparisons showing different decoding behaviour;
* measured token comparisons under named tokenizers;
* RESULT packets that improve or harm review quality;
* simpler protocol constructs that preserve the same semantics.

## Protocol changes

For a protocol change, include:

1. the problem in the current format;
2. a before and after example;
3. the semantic property preserved or improved;
4. any added ambiguity or token overhead;
5. at least one evaluation case.

Do not optimise the grammar solely for character count.
