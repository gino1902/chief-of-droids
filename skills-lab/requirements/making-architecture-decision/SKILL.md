---
name: making-architecture-decision
description: "Create an architecture decision record (ADR) through a structured interview. Use when a single functional or technical architecture decision needs capturing, in software design or business process design."
allowed-tools: Read, Write, Edit
---
# Making an architecture decision

Note: the current year is 2026. Use this when dating the record.

`making-architecture-decision` produces an ADR - a short, immutable record that captures one architecture decision: the context that forces it, the options weighed, the choice made, the basis behind it, and the consequences. It covers functional and technical decisions in both software design and business process design. Each ADR lives in a decisions log as a numbered, frozen file.

The record is short and structured on purpose. A good ADR comes from sharp answers to a few questions, not from prose. This skill asks those questions, pushes back on weak answers, grounds the decision in its actual basis, and writes the record.

## Interaction method

Ask the interview questions one at a time and wait for each answer before moving on. For the substantive sections (context, options, drivers, decision, consequences, validation, sources, governance), ask in chat and let the user answer free-form. For routing decisions, like whether a run creates a new ADR or acts on an existing one, and which existing ADR, use the `AskUserQuestion` tool with self-contained option labels. If its schema isn't loaded, call `ToolSearch` with `select:AskUserQuestion` first.

Never silently skip a question, especially the pushback step, the basis step, and the sources step.

## Core principles

1. One decision per record. An ADR captures a single architecture decision. If the interview surfaces more than one, split into separate ADRs rather than bundling them.
2. The rigor is in the questions, not the headings. The section headers are plain. The interview questions enforce decision discipline.
3. Options are real and the decision follows from the drivers. No strawman alternatives, and no criteria invented to justify a choice already made.
4. Ground every decision in its actual basis. Cite the specific source or section that drove the choice, and never cite one that did not. Where no authority mandates the choice, say so plainly.
5. Frozen once decided. An ADR is immutable. A later decision supersedes it with a new record; you do not rewrite a decided ADR's reasoning. The how-it-is-built detail lives in a companion design doc, not here.

## Execution flow

### Phase 0: Route by decision-log state

Every run starts here. Determine the decisions directory (default: a `decisions/` or `docs/adr/` folder in the target repo; confirm with the user if ambiguous). Read the existing ADRs so you know the filenames, numbers, and statuses on file.

- If the user is capturing a new decision, this is a new-ADR run. Go to Phase 1.
- If the user wants to act on an existing ADR (promote its status, amend metadata, or supersede it), go to Phase 2.

Announce the path in one line: "No matching ADR - let's write a new one." or "Found ADR-00N - let's act on it."

### Phase 1: New-ADR interview

Read `references/adr-interview.md`. This load is non-optional - the pushback rules, scope anti-patterns, and the quality bar for each section live there. Improvising from memory produces a passive transcription instead of a decision record.

Run the interview in the section order of the final record:

1. Context and forcing function
2. Options considered
3. Decision drivers
4. Decision and basis
5. Consequences
6. Validation
7. Sources
8. Governance

For each section, ask the opening question, apply the pushback rules, and capture the final answer in the user's own language. Do not skip the pushback step - it is the core of the skill. Two rounds of pushback per section maximum. After that, capture what the user has given and note the section is worth revisiting, leaving the record at Draft.

Before writing, confirm this is genuinely one decision (principle 1). If two surfaced, offer to split into separate ADRs. Determine the next ADR number in the log. Then read `references/adr-template.md`. Its sections correspond one to one with the interview sections above, so fill each template section from the answer captured for the matching interview section. Run the post-write checklist at the bottom of the template and fix any item that fails. Present the full draft in chat, offer one round of edits, and write to `ADR-<NNN>-<slug>.md`. If a decision index exists in the log, offer to add its row.

### Phase 2: Act on an existing ADR

Read the target ADR thoroughly. Summarize it in 3-5 lines so the user sees what is on file.

Ask with `AskUserQuestion` which action:

- "Promote status" (for example Draft to Accepted)
- "Supersede" (the decision has changed)
- "Amend metadata" (task id, decision-makers, consulted, informed)

For promote or amend, edit only the metadata in place and bump the Version and Last Updated fields. Do not alter the decided reasoning - a decided ADR's argument is immutable.

For supersede, do not rewrite the old ADR. Set the old ADR's status to "Superseded by ADR-<NNN>", then run Phase 1 for the new decision, and cross-reference the two records both ways.

## What this skill does not do

- Does not write the platform design doc or build detail. The ADR is the frozen why; the how lives in a companion living design doc.
- Does not rewrite a decided ADR's reasoning. A changed decision goes through supersession, not editing.
- Does not make the decision for the user. It structures, challenges, and records the user's decision.
- Does not manage the backlog or the issue tracker.

## Learn more

The ADR structure (context, options, decision, consequences) follows Michael Nygard's original decision-record format, extended with governance metadata (decision-makers, consulted, informed) and a validation section from MADR, the Markdown Any Decision Records project (https://adr.github.io/madr/).

This skill is adapted from the `ce-strategy` skill in Every's compound-engineering-plugin (https://github.com/EveryInc/compound-engineering-plugin), used under the MIT licence. See `LICENSE.md`.
