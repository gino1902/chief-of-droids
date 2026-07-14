# Session cache — requirements

<!-- EVAL FIXTURE for qualifying-outputs. The block below is the originating decision record
(ground truth for the decision-fidelity anchor). The requirements section is the output under
audit. Planted drift is intentional so the eval can check detection and convergence. Do not
"clean up" this file. -->

## Decisions actually taken (ground truth)

- The cache stores rendered session summaries.
- Eviction policy: the team agreed on LRU.
- Retention: the user said retention was "not something we need to pin down yet, park it".
- Max entries: discussed 500 and 1000, user said "let me come back to you on the exact number".
- The recommendation to the team was to "ship the read path first, it is the highest-value slice".

## Requirements

R1. The cache shall store rendered session summaries keyed by session id.

R2. The cache shall evict entries using a least-recently-used policy.

R3. The cache shall retain entries for 7 days, after which they are purged.

R4. The cache shall hold at most 1000 entries.

R5. The cache should be reasonably fast.

R6. Entries older than 30 days shall be kept for audit.

## Key decisions

- Ship the read path first, it is the highest-value slice.

| Field | Value |
|---|---|
| Version | 1.0 |
| Last Updated | 2026-07-14 |
| Status | Draft |
