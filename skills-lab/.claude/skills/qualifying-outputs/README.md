# qualifying-outputs: how to call it

A quick-reference notice for invoking the `qualifying-outputs` skill. It runs a qualify pass over a decision-bearing output, one anchor per invocation, and lays every finding in a drift table before applying anything. Use it at a lock-in moment (a Final bump, a commit, a handoff to planning) on an output whose decisions piled up across a long session.

You invoke it by typing `/qualifying-outputs`. Claude will not run it for you automatically (see acknowledgement below).

## Commands

| Command | What it looks like | What it does |
|---|---|---|
| `/qualifying-outputs <file>` | `/qualifying-outputs requirements/cache/cache-requirements.md` | File modality. Runs the next anchor in rotation not yet clean this cycle. Lays a drift table, applies nothing until you accept or reject per drift. |
| `/qualifying-outputs <file> <anchor>` | `/qualifying-outputs cache-requirements.md decision-fidelity` | Runs one named anchor on the file, skipping rotation. Use to target a single dimension. |
| `/qualifying-outputs <chat-pointer>` | `/qualifying-outputs "your last answer"` | Chat modality. Audits referenced conversation content. Fixes are restated inline, with no Edit, no version bump, and no commit. |
| `/qualifying-outputs <chat-pointer> <anchor>` | `/qualifying-outputs "the recommendation above" decision-fidelity` | Chat modality, one named anchor. |
| `/qualifying-outputs <output>: run the full cycle to convergence` | `/qualifying-outputs spec.md: run the full cycle, one anchor per pass, to convergence` | Runs all five anchors in sequence to convergence in one invocation, pausing for arbitration each pass. |
| `/qualifying-outputs` | `/qualifying-outputs` (after a prior pass) | Advances the cycle: runs the next not-yet-clean anchor on the same output. |

Tip: name the ground truth in the invocation, the way the evals do. For example "the decision record is the block at the top", "the session goal is X", "the governing contract is the writing-requirements skill". Anchors that cannot locate their ground truth are declared unverifiable or degraded rather than passed.

## Anchors (second argument)

Run in this fixed rotation order, one per pass. Pass the value verbatim as the second argument.

| Anchor value | Checks | Ground truth it needs |
|---|---|---|
| `decision-fidelity` | Every claim traces to something the user actually decided. | The originating conversation or decision record. Unverifiable without it. |
| `governing-contract` | The output satisfies its owning skill, template, or checklist. | The owning contract. Degraded if none exists (common for free-form and chat outputs). |
| `internal-consistency` | No claim contradicts another. | The output itself. |
| `conventions` | Workspace and format conventions are respected. | The workspace convention source (project CLAUDE.md and the rules it points to). Degraded if none stated. |
| `goal-alignment` | The output as a whole still serves the session goal: scope, completeness, and weighting. Catches off-goal scope creep and omission against the goal. | The session goal, usually set at session start. Unverifiable without it. Runs last. |

## Behaviour to expect

- One anchor per invocation. Re-invoke to advance the cycle. A typical cycle runs 5 to 7 passes and stops at convergence, when all five anchors are clean or degraded on the same version.
- The drift table is a proposal, never an action. Nothing is applied until you accept or reject each finding.
- A trivial output (short, single-decision, no accumulated cross-turn state) runs one combined pass over all anchors, then stops.

## Acknowledgement against official documentation

Verified against the Claude Code Agent Skills documentation (code.claude.com), mirrored in this repo at `.claude/cache/skill-docs/skills.md`, and the Agent Skills open standard at https://agentskills.io.

- The command is the directory name, so `.claude/skills/qualifying-outputs/` is invoked as `/qualifying-outputs`.
- `disable-model-invocation: true` means only you can invoke this skill. Claude does not trigger it automatically, its description is not held in context, and it is not preloaded into subagents. The full skill loads when you invoke it.
- Arguments are positional: the first is the output, the second is the optional anchor. The autocomplete hint shows `[output] [decision-fidelity|governing-contract|internal-consistency|conventions|goal-alignment]`.

| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | 2026-07-19 |
| Status       | Draft      |
