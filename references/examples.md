# Examples

## Example 1: implementation handoff

### Verbose intent

A reviewer has completed discovery. Implementation can now begin. Preserve the existing version first, use the previously approved architecture and evidence as authority, avoid reopening broad discovery, implement the new version, verify it, compare it with the previous version, and do not publish or contact anyone.

### SP/1

```text
SP/1 TASK
ID v2_build_01
STATE evidence_review_complete
STATE readonly_superseded
GOAL build_v2
ACTION implement
SCOPE existing_worktree
AUTH V1_REVIEW
AUTH V2_ARCH
AUTH EVIDENCE_LEDGER
INVARIANT checkpoint_v1_first
INVARIANT no_broad_rediscovery
REF V1_REVIEW=repo:artifacts/v1_review.md role=authority
REF V2_ARCH=repo:artifacts/v2_architecture.md role=authority
REF EVIDENCE_LEDGER=repo:artifacts/evidence_ledger.json role=evidence
POST render
POST visual_inspect
POST deterministic_verify
POST compare_v1_v2
SIDE_EFFECT forbid=push,publish,submit,contact
RETURN v1_checkpoint
RETURN v2_paths
RETURN changes_with_reason
RETURN evidence_delta
RETURN excluded_claims
RETURN hard_gaps
RETURN v1_v2_judgement
RETURN verification_status
EXECUTE yes
```

What was removed:

* conversational transition wording;
* repeated explanation that implementation should proceed;
* prose already represented by `STATE`, `INVARIANT`, `POST` and `RETURN`.

What remained exact:

* state transition;
* authority;
* checkpoint requirement;
* prohibition on broad rediscovery;
* side-effect boundary;
* verification and return contract.

## Example 2: evidence-sensitive claim policy

### Source intent

Use the verified evaluation project as substantive Python engineering evidence. Keep the defence project bounded to its verified training, data, cloud and edge-resilience maturity. Do not imply production multi-agent ownership, air-gapped AI deployment or active clearance. Historical clearance is unresolved and should be omitted unless it becomes necessary or authoritative evidence resolves it.

### SP/1

```text
SP/1 CONTEXT
ID candidate_evidence_04
FACT eval_project=python+evaluation substantive
FACT defence_project=training+data+cloud+edge_resilience bounded
GAP production_multiagent_ownership
GAP airgapped_ai_deployment
GAP active_clearance
UNCERTAIN historical_clearance
VERIFY historical_clearance if=necessary_or_authoritative_source_available
INVARIANT no_gap_inflation
```

The gaps remain explicit. Compression must not convert them into weaker wording that could later be mistaken for partial experience.

## Example 3: worker result

```text
SP/1 RESULT
ID payment_retry_07
STATUS PASS
CHANGED src/payments/callback.py
CHANGED tests/payments/test_callback.py
VERIFIED unit_tests=18/18
VERIFIED integration_tests=6/6
EVIDENCE duplicate_callback_test=PASS
EVIDENCE public_contract_unchanged=PASS
EVIDENCE audit_events_preserved=PASS
ASSUMPTION none
DEVIATION none
RISK none_known
REF diff=git:4f92a1c role=evidence
```

This is preferable to a long worker narrative when the next model only needs to decide whether the implementation satisfies the acceptance criteria.

## Example 4: frontier review

```text
SP/1 REVIEW
ID payment_retry_review_07
GOAL judge_callback_retry_change
CRITERION no_duplicate_external_effects
CRITERION public_contract_unchanged
CRITERION audit_events_preserved
EVIDENCE duplicate_callback_test=PASS
EVIDENCE unit_tests=18/18
EVIDENCE integration_tests=6/6
REF diff=git:4f92a1c role=evidence
VERDICT ACCEPT
```

If the evidence is insufficient, do not infer success:

```text
SP/1 REVIEW
ID payment_retry_review_08
GOAL judge_callback_retry_change
CRITERION no_duplicate_external_effects
EVIDENCE duplicate_callback_test=missing
UNCERTAIN duplicate_effect_safety
VERDICT REVISE
REVISION add_failure_path_test_for_duplicate_callback
```

## Example 5: when not to packetise

Source:

```text
Rename `foo` to `bar` in `config.json` and run the unit tests.
```

Do not convert this into a packet unless a larger orchestration protocol requires one. The original is already compact and unambiguous.
