# Standalone brainstorm test — OP-1, one-shot, terminal, out of project

_These are illustrative fixtures. The subject, any scripted answers, thresholds, slugs, and file names below are examples to make the run concrete, not fixed requirements. Swap them freely. The acceptance criteria are what carry the test._

Run this in a fresh Claude Code session, separate from the chain tests (`chain-test-small.md`, `chain-test-medium.md`), so no prior chain context leaks in.

## Purpose

Exercise `brainstorming-requirements` used on its own, as a one-shot thinking tool, decoupled from the chain. A user has a `FRAMING.md` and nothing else, no bootstrapped project and no `CONCEPTS.md`, and wants to elicit one component's requirements. The run is terminal: the slice it emits is the deliverable, and no `writing-requirements` step follows.

This is the only scenario where the skill runs fully decoupled, so it is the only place its project-independent contract and its absent-`CONCEPTS.md` branch are actually exercised.

## Directory and precedence

Directory: `outputs/test-standalone-brainstorm`, created by this test.

Precedence: none. Independent of every other scenario.

## Preconditions

- A fresh session.
- An empty run directory at `skills-lab/outputs/test-standalone-brainstorm`. Create it before starting.
- Session cwd is that directory.
- No bootstrapping. Do not run `bootstrapping-project`. The run directory holds only the scripted `FRAMING.md` below. There is no `CONCEPTS.md`, no `.claude/` config, and no project tree in the run directory. (`brainstorming-requirements` does not look upward for a `CLAUDE.md`, so an ancestor `CLAUDE.md` in `skills-lab` is irrelevant to this test.)

## Scripted subject — "readingpile"

A solo, out-of-project idea: a small command-line tool to track a personal reading backlog. Deliberately lightweight and single-context, the natural shape of a one-shot brainstorm.

Create `FRAMING.md` in the run directory with exactly this content:

```markdown
# FRAMING — readingpile

## Why
I keep losing track of books I mean to read; they scatter across notes, tabs, and messages. readingpile is one place to drop a book the moment I hear of it and see the backlog in one list.

## For whom
Me, a solo reader. One person, one machine, no sharing.

## Success
I can add a book in one command and list my backlog, and I stop keeping the list anywhere else for a month.

## Delivered
A small command-line tool with a local file store.

## Constraints
- Local only, no accounts, no sync.
- One user.
```

## Run steps

### 1. brainstorming-requirements (only step)

Invoke `brainstorming-requirements from FRAMING.md --target "capture command"`.

Phase 0 should read `FRAMING.md`, find no sibling `CONCEPTS.md`, and proceed (recording the terms it settles so they could seed one later). Confirm the target is a single deployable component and resolve a slug (propose `capture-command`).

Answer the interview as scripted:

- Purpose: the capture command adds a book to the pile from a single command, so a book just heard of is saved before it is forgotten.
- Scope: covers taking a title (and an optional author) from the command and appending it to the pile as an unread entry, and rejecting an empty title. Out of scope: listing the pile (owned by the later `list` command); editing or removing entries (owned by later commands); any sync or backup (excluded by the FRAMING constraint).
- Actors and consumers: upstream, the reader typing the command. Downstream, the pile file that later commands read. Operator, none (solo, local).
- Requirements: elicit three to four in the actor / action / result / conditions contract. Since there is no `CONCEPTS.md`, settle the domain terms in the slice itself, backticked or explicitly defined, so the slice is self-contained.

Let it emit one component slice. Stop there. Do not invoke `writing-requirements`.

## Expected outputs (under `outputs/test-standalone-brainstorm`)

- `FRAMING.md` — the scripted fixture, unchanged.
- one component slice at `outputs/capture-command/capture-command.md`, with domain terms (`pile`, `entry`, `title`, `author`, `unread` or similar) backticked or defined in the slice.
- No `CONCEPTS.md` is required. If the skill chooses to seed one for later, that is acceptable but not expected.
- No `requirements/` directory, and no `writing-requirements` outputs.

## Acceptance criteria

- The skill runs from a lone `FRAMING.md` with no project scaffolding and no `CONCEPTS.md`, without demanding either.
- The slice is emitted and is self-contained: every domain term the requirements lean on is backticked or defined in the slice, since there is no `CONCEPTS.md` to carry the glossary.
- The run is terminal. No `writing-requirements` step is taken.

## Fail conditions

- The skill refuses to run, or demands a bootstrapped project, a `CONCEPTS.md`, or a `CLAUDE.md`, before eliciting.
- The slice is not emitted, or domain terms are left as bare prose (neither backticked nor defined), so the slice does not stand on its own.
- The runner proceeds downstream into `writing-requirements`. Going downstream from a standalone brainstorm is the discouraged path this test deliberately does not exercise (see the Standalone use note in `brainstorming-requirements/SKILL.md`).

## Record

Note the domain terms the skill settled and confirm the slice stands on its own without a `CONCEPTS.md`. Confirm no downstream step was taken. The skill's Phase 2 emission may still print a recommended `writing-requirements` invocation; record that it did, and that it was correctly ignored for this decoupled run.

## Note

This is a single-skill terminal test, not a chain test. It complements the chain tests by covering the one legitimate decoupled use of `brainstorming-requirements`. The documented discouragement of carrying a standalone slice downstream lives in the Standalone use note in `brainstorming-requirements/SKILL.md`.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-07-13 |
| Status       | Draft      |
