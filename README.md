<h1 align="center">Semantic Packetisation</h1>
<p align="center"><strong>Compact context. Explicit constraints.</strong></p>
<p align="center">An Agent Skill and readable packet format for model handoffs.</p>

<p align="center">
  <a href="https://github.com/MaxLaurieHutchinson/Semantic-Packetisation/actions/workflows/test.yml"><img src="https://github.com/MaxLaurieHutchinson/Semantic-Packetisation/actions/workflows/test.yml/badge.svg" alt="Tests" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT license" /></a>
</p>

<p align="center">
  <a href="references/protocol.md">Protocol</a> &middot;
  <a href="references/examples.md">Examples</a> &middot;
  <a href="references/evaluation.md">Evaluation</a>
</p>

Turn repeated background, buried constraints and worker summaries into **SP/1**: a small, inspectable structure for the next model's decision.

The goal is not the shortest text. It is enough context to act or judge correctly, with authority, uncertainty and boundaries intact.

## See it in use

**Source**

> The evidence review is complete and implementation is approved. Build V2 in the existing worktree. Checkpoint V1 before changing anything. Keep the public API unchanged. Run the unit tests and return the diff and test results. Do not push, publish or contact anyone. Stop if a change to the public API is required.

**Packet**

```text
SP/1 TASK
STATE evidence review complete; implementation approved
GOAL build V2
SCOPE existing worktree
INVARIANT checkpoint V1 before making changes
INVARIANT public API unchanged
POST run unit tests
RETURN diff and test results
STOP public API change required
SIDE_EFFECT forbid=push,publish,contact
EXECUTE yes
```

This illustrates explicit constraints, not measured token savings. Try the included [source](examples/handoff.txt) and [packet](examples/handoff.sp).

## Try it

Python 3.10 or newer. No runtime dependencies are required for validation or basic size comparison.

```bash
git clone https://github.com/MaxLaurieHutchinson/Semantic-Packetisation.git
cd Semantic-Packetisation
python scripts/validate_packet.py examples/handoff.sp
python scripts/compare_payloads.py examples/handoff.txt examples/handoff.sp
```

For optional token counts, install `tiktoken` and select an encoding appropriate to the receiving model:

```bash
python -m pip install tiktoken
python scripts/compare_payloads.py examples/handoff.txt examples/handoff.sp --encoding o200k_base
```

Without it, counts are labelled as proxies. Already short, clear prompts may be better left alone.

### As an Agent Skill

Copy the repository into a skill directory supported by your host, named `semantic-packetisation`. Keep [SKILL.md](SKILL.md), `agents/`, `references/` and `scripts/` together. There is no bundled marketplace plugin.

> Packetise this handoff. Preserve exact constraints, unresolved questions and permissions. Keep critical facts inline when the receiver cannot access the references.

## What crosses the boundary

| Loss class | Treatment |
| :--- | :--- |
| **L0: exact** | Preserve facts, authority, prohibitions, uncertainty and acceptance criteria. |
| **L1: condensed** | Shorten rationale and background without changing meaning. |
| **L2: disposable** | Remove repetition and filler that cannot affect the decision. |

When uncertain, choose the safer class. References must be accessible to the receiver.

**`TASK`** carries instructions. **`CONTEXT`** carries reusable facts. **`RESULT`** returns evidence. **`REVIEW`** carries criteria and a decision. See the [protocol](references/protocol.md) and [worked examples](references/examples.md).

## Status and limits

**Experimental v0.1.** Tests cover structure, commands and examples. The [six evaluation scenarios](evals/packetisation_scenarios.json) are a catalogue, not executed model trials. No published benchmark establishes token savings or improved task success; the [evaluation method](references/evaluation.md) describes how to test those claims.

Structural validity does not prove semantic completeness, accessible references or permission to act. `AUTH` and `EXECUTE` cannot override the receiving host's permissions or higher priority instructions.

The scripts do not execute packets or resolve references. The optional tokenizer may download encoding data on first use. External model use follows that host's data handling rules.

## Development

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

CI runs on Linux and Windows with Python 3.10 and 3.13. See [Contributing](CONTRIBUTING.md).

## Related work

[PAIRL](https://github.com/dwehrmann/PAIRL) explores readable agent communication. This project focuses on decision context and evidence handoffs, not transport. Astra Quota Router is complementary: it chooses where work goes; this skill shapes the context sent with it.

## License

[MIT](LICENSE). Copyright 2026 Max Laurie Hutchinson.
