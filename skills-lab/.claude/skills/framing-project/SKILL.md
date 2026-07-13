---
name: framing-project
description: "Create or update FRAMING.md. Use when starting a project, a product, a consultative engagement."
allowed-tools: Read, Write, Edit
---
# Project framing

Note: the current year is 2026. Use this when dating the framing document.

`framing-project` produces and maintains `FRAMING.md` - a short, durable anchor document that captures what is delivered, who it serves, how it succeeds, and where the team is investing. It lives at the repo root as a canonical, well-known file (peer of `README.md`).

It also seeds a companion, `CONCEPTS.md`, the single source of the project's domain language. Framing is where the domain scope, the main terms, and the boundaries are set, so the language is defined here and downstream requirements work references it rather than reinventing terms. Downstream skills read both files as grounding when they exist.

The document is short and structured on purpose. Good answers to a handful of sharp questions produce a better framing than any amount of prose. This skill asks those questions, pushes back on weak answers, and writes the doc.

## Interaction method

Ask the interview questions one at a time and wait for each answer before moving on. For the substantive sections (problem, approach, who it's for, success, tracks), ask in chat and let the user answer free-form. For routing decisions, like which section(s) to revisit on an update run, use the `AskUserQuestion` tool with self-contained option labels. If its schema isn't loaded, call `ToolSearch` with `select:AskUserQuestion` first.

Never silently skip a question, especially the pushback step.

## Core principles

1. This is an anchor, not a plan. Framing describes what the project or product is, for whom, and why. Features belong in `tbd`. Schedules belong in the issue tracker. Do not let either creep into the doc.
2. The rigor is in the questions, not the headings. The section headers are plain English. The interview questions enforce framing discipline.
3. Short is a feature. The template is constrained. Adding sections costs more than it looks like, so push back on expansion.
4. The doc is durable across runs. This skill is rerunnable. On a second run it updates in place, preserves what is working, and only challenges sections that look stale or weak.

## Execution flow

### Phase 0: Route by file state

Every run starts here. Read `FRAMING.md` with the Read tool and route on what you find.

- If `FRAMING.md` does not exist, this is a first run. Go to Phase 1.
- If `FRAMING.md` exists, this is an update run. Ask which section(s) to revisit, then go to Phase 2.

Announce the path in one line: "Framing doc not found - let's write it." or "Found existing framing - let's review and update."

### Phase 1: First-run interview

Read `references/framing-interview.md`. This load is non-optional - the pushback rules, anti-pattern examples, and quality bar for each section live there. Improvising from memory produces a passive transcription instead of a framing doc.

Run the interview in the section order of the final document:

1. Target problem
2. Our approach
3. Who it's for (customer and business)
4. What success means (customer and business)
5. Tracks
6. Not working on (optional)


For each section, ask the opening question, apply the pushback rules, and capture the final answer in the user's own language. Do not skip the pushback step - it is the core of the skill. Two rounds of pushback per section maximum. After that, capture what the user has given and note the section is worth revisiting on the next run.

Ask every section in order, including the optional ones. Never skip a section without asking. For an optional section, ask its opening question once. If the user has nothing to add, leave it out of the written doc and move on, with no pushback.

When the required sections (1-5) are captured, read `references/framing-template.md`. Its sections correspond one to one with the interview sections above, in the same order, so fill each template section from the answer captured for the matching interview section. Before showing anything, run the post-write checklist at the bottom of the template and fix any item that fails. Then present the full draft in chat, offer one round of edits, and write to `FRAMING.md`.

Then seed the domain language. Read `references/concepts-template.md` and write `CONCEPTS.md` at the repo root, capturing the domain terms already surfaced in the framing answers, structured by track (one context block per track) plus a shared core. Do not run a separate vocabulary interview; framing stays short and downstream skills grow the language. Run the concepts post-write checklist before writing.

### Phase 2: Update run

Read the existing `FRAMING.md` thoroughly. Summarize current state in 3-5 lines so the user sees what is on file.

Ask the user which section(s) to revisit with `AskUserQuestion`. Options:

- "Target problem"
- "Our approach"
- "Who it's for"
- "What success means"
- "Tracks or not working on"

For each section the user picks, jump to it in `references/framing-interview.md` and re-interview with full pushback, as if this were a first run - do not rubber-stamp existing weak content just because it is already written. The interview section maps to the same-named template section, so write each captured answer back into its matching section. Preserve every section the user does not pick. Update the `last_updated` value in the YAML frontmatter to today's ISO date.

Run the template's post-write checklist against the updated doc, fix any item that fails, then write the updated doc back to `FRAMING.md`.

If any revisited section changed the domain terms or boundaries, read `references/concepts-template.md` and update `CONCEPTS.md` in place: preserve existing terms, add or refine only where framing changed. Leave `CONCEPTS.md` untouched if no term or boundary moved.

## What this skill does not do

- Does not update the issue tracker or reconcile in-flight work. Framing is the doc, execution lives elsewhere.
- Does not prioritize the backlog. Prioritization is a separate workflow.
- Does not write product requirements or implementation plans - those live in downstream skills (TBD).
- Does not compute metric values. It records which metrics matter and where they live, not what they read today.

## Learn more

The framing structure (target problem, our approach, tracks) is adapted from Richard Rumelt's *Good Strategy Bad Strategy: The Difference and Why It Matters* (Crown Business, New York, 2011, ISBN 978-0307886231), specifically his kernel of diagnosis, guiding policy, and coherent action. The interview questions push past what he calls "bad strategy": fluff, goals dressed up as strategy, and feature lists in place of a guiding choice.

This skill is adapted from the `ce-strategy` skill in Every's compound-engineering-plugin (https://github.com/EveryInc/compound-engineering-plugin), used under the MIT licence. See `LICENSE`.
