# How to Create a Skill in the Chief of Droids Workspace

A step-by-step account of how the `managing-sessions` skill was designed,
challenged, built, and assessed — in a single session lasting approximately
3–4 hours on 2026-03-28.

The session began at 9:08 am with a one-line intent statement. It ended with
a committed, assessed, and rated skill with four reference files, two output
directories, a findings file from a live run, and a session removal log.
Nothing was skipped. Nothing was done without challenge first.

This document preserves the logic and philosophy of that process so it can be
repeated for any new skill.

---

## What the process looks like, end to end

The user opened at 9:08 am with a single statement of intent:

> "My intent is to build a skill to manage session history for a project."

Seven numbered requirements followed. That was the entire brief. No file
structure, no reference files, no workflow steps. Just intent.

What followed over the next 3–4 hours was:

1. Challenge the intent against platform constraints
2. Resolve design decisions before writing anything
3. Build the skill incrementally with challenge rounds at each stage
4. Run the skill for real (live session analysis)
5. Critique the skill against the assessment checklist
6. Apply all findings
7. Critique again — and confirm Pass

The output was not written in one pass. It was written, challenged, patched,
challenged again, and patched again. That is the expected pattern, not a sign
that something went wrong.

---

## Phase 1 — Challenge before designing

The first thing that happened after the intent was stated was not a design
proposal. It was a challenge of the requirements against what is actually
possible.

Three hard constraints surfaced immediately:

- **`recent_chats` is project-scoped.** It returns sessions from the current
  project only. A single skill invocation cannot analyse sessions across all
  projects. This killed the "centralised cross-project analysis in one run"
  idea — replaced with "run once per project, logs accumulate centrally."
- **Claude cannot delete sessions.** The skill can recommend deletions and
  produce a checklist, but execution is always manual in the claude.ai UI.
  Any design that implied the skill would delete sessions was wrong.
- **`userMemories` is not readable as a file.** The memory challenge workflow
  had to work by reading on-disk sources and comparing them against whatever
  was in context — not by accessing a memories file directly.

These constraints were surfaced before any file was written. The user then
answered three design questions that resolved the remaining ambiguities:
auto-trigger mechanism, log file fidelity, and memory challenge scope.

**The principle:** challenge requirements against real platform behaviour
before designing anything. Constraints discovered during build are expensive.
Constraints discovered during the challenge phase cost nothing.

---

## Phase 2 — Design decisions, confirmed before build

With constraints established, three design decisions were locked:

| Decision | Choice made | Rationale |
| :--- | :--- | :--- |
| Auto-trigger mechanism | System prompt rule: if `recent_chats` ≥10 at bootstrap, invoke skill | Skill system cannot monitor passively; only mechanism available |
| Session log fidelity | Structured summary: title, date, decisions extracted — written to disk | Full transcripts not exportable; this is the maximum achievable fidelity |
| userMemories challenge | Skill reads on-disk sources only; flags what *could* be contradicted | userMemories not accessible as a file; context-visible only |

These were not guesses. They were the output of a structured question
presented to the user before any implementation began.

**The principle:** for any skill with conditional branching or design
alternatives, resolve the decisions before writing. A skill built on
unresolved design questions will be patched repeatedly after build.

---

## Phase 3 — Incremental build with challenge at each stage

The skill was not written in one pass. It was built in layers, with a
challenge round after each layer:

**Layer 1 — SKILL.md and reference file stubs**

Initial structure: frontmatter, reference file declarations, workflow
outlines. No reference file content yet. The challenge after this layer
surfaced the first design gap: the skill had no project identity resolution.
Running from different projects would produce filename collisions and
incorrect memory challenge scope. Step 0 was added.

**Layer 2 — Storage layout**

Initial design: single log file in `logs/`. Challenge surfaced that
findings (extracted value) and removal records (which sessions were deleted)
are categorically different — one is an asset, the other is an audit trail.
Keeping them in one file conflated their purpose and made the removal log
mandatory even when nothing was removed. Split into two output paths:
`.tasks/sessions-findings/` and `.logs/sessions-removed/`.

**Layer 3 — Confidence model**

The skill initially used a single `recent_chats` call and one
`conversation_search` call. A challenge round asked: what is the actual
confidence of a single pass? Answer: unknown and low — summaries are lossy,
queries are generic, on-disk verification was by reference not by file read.
The 5-pass model was designed in response: baseline inventory, 7 targeted
category searches, target file reads, residual search, memory challenge.
Each pass has a specific role. None is redundant.

**Layer 4 — Reference files**

`what-to-capture.md`: 7 categories, each with signal phrases, a canonical
`search_query` for Pass 2, a capture condition, an on-disk verification
target, and a risk-if-missed statement. The canonical query per category
is what makes Pass 2 deterministic across runs rather than ad-hoc.

`session-log-schema.md`: two schemas — findings file and removal log — with
write rules and the rule that a removal log is only created when at least one
session is confirmed for removal. An empty removal log was explicitly rejected.

`memory-contradiction-rules.md`: 7 rules, each checking a specific class
of memory claim against a specific on-disk source. Rules cover path format,
skill name staleness, write authority, tool availability, superseded design
decisions, missing known gaps, and plan gating claims.

**The principle:** build in layers. Challenge after each layer. Do not
try to get the whole skill right in one pass — the structure will surface
issues that were invisible during design.

---

## Phase 4 — Live run before assessment

Before formal assessment, the skill was run for real against the actual
project session history — approximately 20 sessions accumulated over
two weeks.

Running the skill live before assessing it served two purposes:

1. It validated that the workflow actually executes correctly against
   real data — not just that it reads correctly on paper.
2. It produced useful output: a findings file with 11 `not-on-disk`
   findings and a removal log for 9 sessions. The run was not a test —
   it was real work.

The live run also surfaced one real-data behaviour that the skill design
had not accounted for: `conversation_search` can return false positives —
sessions that match the query string but contain no relevant finding.
This was added to the Confidence Model and the Pass 2 workflow before
assessment began.

**The principle:** run the skill for real before assessing it. A skill
that passes checklist assessment but fails on real data is not a pass.
The live run is the highest-confidence test available — it costs little
and reveals what inspection cannot.

---

## Phase 5 — Formal assessment with the `creating-skills` skill

After the live run, `critique skill managing-sessions` was invoked.
The assessment checklist was read from disk. Official sources were fetched.
All four skill files were read fresh.

The first assessment (v1.5) produced:

| Severity | Count | Items |
| :--- | :--- | :--- |
| Blocking | 3 | Reference files >100 lines with no ToC |
| Major | 4 | Pass 4 boundary ambiguous; dedup key unspecified; partial result unhandled; false positives unhandled |
| Minor | 3 | Description framing; Rule 7 hardcoded path; HOW-TO-TRIGGER.md stale path |

All 10 findings were applied in a single fix pass. The second assessment
(v1.6) produced 4 Minor findings only — all maintenance items, none
affecting current execution correctness.

**Final rating: Pass.**

**The principle:** assessment is not rubber-stamping. The checklist exists
to surface real issues. Expect Blocking and Major findings on a first
assessment of a complex skill — they are normal, not a sign of failure.
Fix them and re-assess. A skill that passes on the first assessment of
a complex workflow probably wasn't assessed rigorously enough.

---

## The philosophy in three sentences

Challenge before building — every design assumption that is not challenged
before implementation becomes a defect discovered during build or after
deployment.

Build in layers, not in one pass — each layer is cheap to challenge and
patch; a completed skill is expensive to restructure.

Run before assessing — a live run against real data reveals what no
checklist can: whether the workflow actually does what it claims to do
in the conditions it will actually face.

---

## Checklist for creating a new skill

Use this as a gate before starting implementation.

**Pre-build:**

- [ ] Intent stated in plain language — what does the skill do, when does it
  trigger, what are its inputs and outputs
- [ ] Requirements challenged against platform constraints — what cannot be
  done, what must be approximated, what is the correct scope
- [ ] Design decisions resolved — branching conditions, output format,
  write authority, trigger mechanism
- [ ] `creating-skills` skill loaded — reads `references/assessment-checklist.md`
  and fetches official sources before any file is written

**Build:**

- [ ] SKILL.md frontmatter complete — name (gerund form), description (third
  person, trigger-inclusive, pushy, under 1024 chars)
- [ ] Reference files declared with when-to-read guidance
- [ ] Workflows written in numbered imperative steps
- [ ] Failure handling covers missing files AND runtime conditions
- [ ] If workflow-class: classification criteria exhaustive, all branches
  defined, pass outputs explicitly consumed by next pass, "done" defined,
  confidence level surfaced
- [ ] Each reference file >100 lines has a ToC
- [ ] HOW-TO-TRIGGER.md updated with new skill entry and combining table row

**Before assessment:**

- [ ] Live run executed against real data — not a synthetic test
- [ ] Any real-data issues found during the run incorporated before assessment

**Assessment:**

- [ ] `critique skill <name>` invoked — reads checklist from disk, fetches
  official sources, reads all skill files fresh
- [ ] All Blocking and Major findings fixed before declaring done
- [ ] Re-assessment run after fixes — confirm rating is Pass
- [ ] Commit staged for tracked files: SKILL.md, reference files,
  HOW-TO-TRIGGER.md, any directories created

---

## File and directory conventions

| Item | Convention |
| :--- | :--- |
| Skill folder name | Gerund form: `managing-sessions`, `writing-docs`, `creating-skills` |
| SKILL.md frontmatter `name` | Same as folder name — lowercase, hyphens, max 64 chars |
| Reference files | `references/<noun>.md` — one concept per file |
| Output files (findings) | `.tasks/sessions-findings/YYYY-MM-DD-<project>-<type>.md` |
| Output files (removal logs) | `.logs/sessions-removed/YYYY-MM-DD-<project>-removed.md` |
| HOW-TO-TRIGGER.md | Updated via `creating-skills` workflow — never edited directly from a project |
| Version block | Every `.md` written to disk includes version, date, status |

---

## What made this session work

The skill took 3–4 hours from first prompt to committed Pass rating.
That is not slow — it is the correct pace for a skill of this complexity.

What made it work:

- The user challenged every output before approving it. Multiple rounds
  of challenge were the norm, not the exception. The final skill is
  substantially different from the initial design because of those challenges.
- No file was written without a confirmed design. The gap between "intent
  stated" and "first file written" was approximately 45 minutes of challenge
  and decision-making.
- The live run was treated as real work, not a test. The findings file and
  removal log it produced are genuine workspace assets.
- Assessment was taken seriously. 10 findings on a first assessment is not
  a failure — it is evidence that the checklist is working. The correct
  response is to fix them, not to argue with them.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-03-28 |
| Status       | Final      |
