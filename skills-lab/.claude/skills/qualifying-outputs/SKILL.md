---
name: qualifying-outputs
description: Run a multi-anchor qualify pass over a decision-bearing output to eliminate drift and drive it to a verifiable converged state. The output can be a file on disk (requirements doc, design note, proposal, SAD section) or a chat answer (a recommendation or proposal stated in the conversation). Auto-rotates through five anchors, one per invocation, in order: decision fidelity, governing contract, internal consistency, conventions, goal alignment. Audits against the current anchor only, lays every finding in a drift table, and applies nothing until you accept or reject per drift. Re-invoke to advance the cycle; stops at convergence. Use at a lock-in moment such as a Final bump, a commit, or a handoff to planning, on an output whose decisions accumulated across turns.
disable-model-invocation: true
argument-hint: "[output] [decision-fidelity|governing-contract|internal-consistency|conventions|goal-alignment]"
arguments: [output, anchor]
allowed-tools:
  - Read
  - Grep
  - Glob
  - Edit
---

# qualifying-outputs

Run one qualify pass over `$output` on a single anchor. This eliminates drift between what was decided in the conversation and what the output records, and drives the output toward a converged state where every claim traces to a decision, satisfies its governing contract, is internally consistent, respects workspace conventions, and shows no unmanaged drift from the session goal. The drift tables are the audit trail.

`$anchor`, if given, names the anchor to run this pass. If empty, take the next anchor in `<anchor-rotation>` order not yet clean this cycle.

<the-pass>

```
Qualify pass on $output.
Anchor: [decision fidelity | governing contract | internal consistency | conventions | goal alignment]
— one per pass, not yet used this cycle. Trivial output → single combined pass.

- Audit against the anchor only.
- Drift table: # | location | says | ground truth | Genuine/Churn | fix
- Apply nothing; await accept/reject per drift.
- Zero Genuine drifts → anchor clean. All five clean → converged, stop.
```

</the-pass>

<modality>

Resolve `$output` to one of two modalities before auditing. This changes only how you read the output and how you apply accepted fixes. Every other rule below is identical across modalities.

- File modality. `$output` names or points to a file on disk. Read it. Drift-table `location` cites a section, heading, or line. Accepted fixes are applied as an Edit, a single full-output revision. Convergence, version bump, and commit apply.
- Chat modality. `$output` points to conversation content, for example "your last answer", "the recommendation above", or a quoted passage. There is no file. Drift-table `location` cites the claim or passage. Accepted fixes are applied by restating the corrected answer inline in the next turn. There is no Edit, no version bump, and no commit; say so rather than implying a persisted change.

If `$output` is ambiguous (a path that does not resolve, or a chat pointer that matches more than one prior answer), ask which output before auditing. Do not guess.

</modality>

<setup>

Do this once, on the first pass of a cycle only:

1. Identify the output and its modality per `<modality>`.
2. Identify the governing contract: the owning skill, template, or checklist that defines what a valid instance of this output looks like. If none exists, declare the governing-contract anchor degraded and skip it during rotation. Reason: inventing a contract for a free-form output manufactures findings that trace to nothing. Chat-modality outputs are usually degraded on this anchor.
3. Apply the triviality valve. A trivial output (short, single-decision, no accumulated cross-turn state) runs one combined pass over all anchors at once, then stops. Do not run five passes on a trivial output.
4. Locate the decision-fidelity ground truth: the originating conversation or decision record the output's claims must trace to. In chat modality this is the current conversation. In file modality it is the session or record that produced the file. If no such record is available, the decision-fidelity anchor is unverifiable: say so, do not mark it clean, and do not declare convergence. Ask the user to point to or paste the record before running that anchor. Reason: decision fidelity is checkable only against what was actually decided, so without the record the anchor cannot be certified and must not be assumed clean.
5. Locate the goal-alignment ground truth: the session goal, meaning the originating intent the session set out to achieve, not the local task of any one turn. Sources, in order of preference: an explicit goal statement in the session, a FRAMING.md if the project has one, otherwise the first substantive request. In a long session, restate the goal back to the user and get confirmation before running the goal-alignment anchor. If no goal is recoverable, that anchor is unverifiable: say so, do not mark it clean, and do not declare convergence. Ask the user to state the session goal before running it. Reason: alignment is checkable only against a known goal, and in a long session the goal set many turns ago is buried under everything since and is exactly what the output tends to drift from. Restating it here lifts it back to the top of the pile, which is the point of this anchor: make the drift visible so it can be managed, not shipped silently.
6. Locate the conventions ground truth: the workspace's own convention source, meaning the project CLAUDE.md or its equivalent plus the format rules it points to, for example the house style and the version-block requirement. If the workspace states no conventions, declare the conventions anchor degraded rather than inventing format rules. Reason: this anchor is checkable only against stated workspace rules; without a located source, flagging format manufactures findings that trace to nothing, the same failure the governing-contract degradation prevents.

</setup>

<anchor-rotation>

Anchors run in this fixed order, one per invocation:

1. decision fidelity — every claim traces to something the user actually decided.
2. governing contract — the output satisfies its owning skill, template, or checklist.
3. internal consistency — no claim contradicts another.
4. conventions — the output respects the workspace and format conventions located in `<setup>`.
5. goal alignment — resurface the session goal set at the outset, now buried deep in the conversation, and test the output as a whole against it. Its job is to make drift the session accumulated explicit, so it is named and managed rather than shipped silently. Whole-output altitude only: scope, completeness, and weighting against the goal. Per-claim provenance stays with decision fidelity, and quality against decisions, contract, consistency, and conventions stays with anchors 1 to 4. Because this anchor runs last, any drift that is also a per-claim failure has already been filed under an earlier anchor, so its residual is exactly the top-down gaps no earlier anchor tests: off-goal scope creep and omission against the goal.

Track which anchors are already clean this cycle in conversational memory, not a bookkeeping file. On each invocation, run `$anchor` if given, otherwise the lowest-numbered anchor not yet clean. Reason: one anchor per pass is load-bearing. Without rotation the next pass re-audits the previous anchor's ground and manufactures churn instead of signal.

When one drift fails more than one anchor, file it under the first anchor in rotation whose test it fails, and do not re-file it on a later anchor. For example, a requirement that both traces to no decision and is untestable is filed under decision fidelity, not held for the governing-contract pass. Reason: one owner per finding keeps attribution deterministic and stops the same issue reappearing pass to pass.

A degraded anchor (declared in `<setup>`) counts as handled for rotation and convergence. Name it as degraded rather than silently skipping it.

</anchor-rotation>

<classify>

Classify every finding in the drift table:

- Genuine — changes meaning, scope, or a decision.
- Churn — cosmetic, with near-zero risk either way.

Boundary case, a detail present in the output that was never decided. If it fixes a deferred or contested decision (a number, a date, a retention policy, an eviction rule), it is Genuine, however small it looks. If it is a low-risk natural elaboration that commits to nothing contested (a field name, a label, an obvious key), it is Churn. Reason: the risk is in silently resolving something the user still owns, not in the size of the edit.

The split keeps each accept or reject decision cheap. Do not dress a cosmetic finding as a drift to satisfy the request. An anchor is clean when it surfaces zero Genuine drifts on the current output version.

</classify>

<example>

Three worked passes, spanning anchors and both modalities.

Decision-fidelity pass, file modality. Fixes the shape of a pass end to end.

Output under audit, a two-line proposal:

```
Rollout: we ship on 1 March.
Owner: Priya.
```

Ground truth from the originating conversation: the user said "let's not fix the date yet", and named Priya as owner.

Drift table:

| # | location | says | ground truth | Genuine/Churn | fix |
|---|---|---|---|---|---|
| 1 | line 1 | "we ship on 1 March" | date was deferred, not decided | Genuine | replace with "Rollout date: open, deferred" |
| 2 | line 2 | "Owner: Priya." | Priya named as owner | Churn | leave |

Arbitration by the user: accept 1, reject 2. Apply the accepted fix as a revision, so line 1 becomes "Rollout date: open, deferred". The anchor now surfaces zero Genuine drifts, so decision fidelity is clean for this version. Note what the fix may have dirtied (nothing here) and move to the next anchor.

Goal-alignment pass, file modality. Catches what the earlier anchors leave.

Output under audit, an on-call runbook whose session goal is a runbook covering the migration and the rollback path. It has sections for migration steps, paging, and a launch announcement. Every section traces to a decision, so decision fidelity, internal consistency, and conventions were already clean, and there is no owning template, so governing contract is degraded.

Drift table:

| # | location | says | ground truth | Genuine/Churn | fix |
|---|---|---|---|---|---|
| 1 | Launch announcement section | draft the marketing announcement | goal is an on-call migration and rollback runbook; marketing sits outside it | Genuine | move it out of this runbook |
| 2 | runbook, absent | no rollback section | goal requires the rollback path, decided as flipping the read flag back | Genuine | add a Rollback section |

Both findings trace to real decisions, so no earlier anchor flagged them. Off-goal scope creep (1) and omission against the goal (2) are exactly this anchor's residual, and absence is invisible to every other anchor. This is the drift a long session accumulates while each single edit looked reasonable.

Chat-modality pass, decision fidelity. No file, so fixes are restated inline.

Output under audit, a recommendation stated in the conversation: "We should adopt trunk-based development, the team already agreed, and we will cut releases every Friday." Ground truth from the chat: the team discussed trunk-based development but did not agree, and no cadence was decided.

Drift table:

| # | location | says | ground truth | Genuine/Churn | fix |
|---|---|---|---|---|---|
| 1 | the recommendation | "the team already agreed" | discussed, not agreed | Genuine | restate: the team discussed trunk-based development, no decision yet |
| 2 | the recommendation | "releases every Friday" | no cadence decided | Genuine | restate: release cadence open |

Arbitration: accept both. Apply by restating the corrected recommendation inline on the next turn, with no Edit, no version bump, and no commit, and say so rather than implying a persisted change. The governing-contract anchor is degraded for a free-form chat answer.

</example>

<apply-nothing>

The drift table is a proposal, never an action. Apply nothing during the audit turn, even fixes that look obviously correct.

After you present the table, the user accepts or rejects per drift. Then apply the accepted fixes as a single full-output revision (an Edit in file modality, a restated answer in chat modality). After applying, name the anchors the fixes plausibly dirtied so a later invocation can re-run them.

Reason: user arbitration per drift prevents the reviewer silently re-resolving tensions the user should own.

</apply-nothing>

<watch-for>

Recurring drift shapes, each a Genuine finding when present:

- A user deferral is not a decision. "Not required at this stage" is a deferral recorded as one, not permission to fix the answer.
- Review rhetoric is not a decision. A phrase from a recommendation, for example "highest-value 20% first", does not belong in a Key decisions section.
- Conflicting user answers are not resolved silently. When two answers conflict, record the resolution as a visible decision, not a quiet edit.
- A governing contract is not invented for a free-form output. Declare the anchor degraded and run the rest.
- A stale version block is Genuine on the conventions anchor when the workspace requires the increment. If material fixes were applied and the repo's rules mandate a version bump, a version left unchanged is a Genuine drift, not cosmetic bookkeeping. Bump it.
- Scope creep is not progress. An output that grew past the session goal is a Genuine goal-alignment drift even when every addition was individually decided. So is a goal-required point the output never states: absence is invisible to every other anchor, so goal alignment is where it must be caught.

</watch-for>

<convergence>

An anchor is clean when it surfaces zero Genuine drifts on the current output version. The cycle has converged when all five anchors are clean (or declared degraded) on the same version. Say so and stop. Further passes are churn by definition.

An unverifiable anchor is neither clean nor degraded: decision fidelity with no originating record (per `<setup>` step 4), or goal alignment with no recoverable session goal (per `<setup>` step 5). It blocks convergence: run the other anchors, but do not declare the cycle converged until the missing ground truth is supplied and the anchor is checked.

A typical cycle runs 5 to 7 passes. A cycle still finding Genuine drifts past 7 passes signals an upstream problem, not a review problem. Flag that rather than looping on.

</convergence>

<target>

This skill is version-neutral and targets claude-code. It depends on no single Claude model version.

</target>

| Field        | Value      |
|--------------|------------|
| Version      | 1.5        |
| Last Updated | 2026-07-19 |
| Status       | Draft      |
