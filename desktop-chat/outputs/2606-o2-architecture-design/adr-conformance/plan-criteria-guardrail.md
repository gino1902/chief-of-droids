# Plan: criteria guardrail and gap analysis

Build plan for the second instrument in this folder. Written to be run cold in a later session by
someone who was not in the one that designed it.

**Status: not started.** Three decisions are still open, listed at the end. Do not start without
them.

---

## What this is, and what it is not

Two instruments live here and merging them would break both.

| | Cases (`cases.md`) | This instrument |
|:--|:--|:--|
| Question | Does the record set answer a situation predictably? | Does a record satisfy what the field says matters? |
| Tests | Internal coherence | External quality |
| Input | A situation | A record |
| Output | Determined, Underspecified, Conflict, Gap | Gap list per record |
| Failure means | The set is ambiguous or contradictory | A record is missing something known to matter |

A record can pass every case and still be poor, and vice versa.

## Inputs

| Input | Path | Role |
|:------|:-----|:-----|
| Criteria register | `criteria-and-provenance.md` | The raw ~40. Source material, not the instrument |
| The records | `../decisions/` | What gets scored |
| Scoring precedent | `../../2607-o2-requirements/use-case-format.md` | Reuse its rules, do not invent a scoring model |
| Method | `README.md` | The self-grading rule applies here too |

---

## Already decided, do not re-litigate

**Reuse the use-case-format rules.** That artefact already solved this exact shape and its three
rules transfer without modification:

- **Fixed set.** One criteria list, the same for every record. Nobody picks which to apply.
- **Declared N/A.** A criterion that genuinely does not apply is marked N/A with a one-line reason,
  visible in the output. Silent omission is forbidden.
- **Prune on frequent N/A.** A criterion marked N/A across most records is wrong, not the records.
  Drop or fold it at the next revision.

**The score is the dangerous part.** A number aggregates incommensurable things, looks objective,
hides which criteria failed, and invites writing records to pass a list rather than to decide well.
If a score exists it is coverage over *applicable* criteria only, and it is never shown without the
failures beside it. The gap list is the deliverable; the score is a summary of it.

**Self-grading is not permitted.** If one party curates the criteria, applies them and rules on the
result, the instrument measures that party's consistency. Derivation is mechanical, the ruling on
whether a gap is real belongs to the user. Same rule as the cases.

---

## Build steps, each with its checkpoint

### 1. Curate

From the register, keep only criteria that are **assertable about a single record by reading it**.
The test: can it be phrased as a question with a yes, no or N/A answer, answerable without running
anything?

Keep, for example: does the record name a stable owner; does it state what it gives up; does its
basis cite a source or say plainly that none mandates it.

Drop, for example: lineage is not preserved across renames. That is a platform fact used *inside*
an argument, not a property of a record.

Expect roughly twelve to survive, not forty.

> **Checkpoint.** Every kept criterion has a question form. Every dropped one has a one-line reason
> recorded. If nothing was dropped, the curation did not happen.

### 2. Define applicability as a rule, not a list

Each criterion states which records it applies to, expressed as a condition rather than an
enumeration, because a list of record numbers goes stale the moment a record is added.

> **Checkpoint.** Run the applicability rules over the twelve existing records. ADR-004 on
> serverless compute should come out with a small applicable set. No record should come out with
> zero, and if one does the criteria set is too narrow.

### 3. Define pass and gap per criterion

For each, what satisfying it looks like and what a gap looks like. Both concrete enough that two
readers agree.

> **Checkpoint.** Two independent passes over one record agree on every verdict. If they disagree,
> the criterion is underspecified and gets tightened before going further. This is the same
> variance test the cases use.

### 4. Dry run on two records, chosen to be different

Run against **ADR-012**, written deliberately against these criteria, and against a thin one such
as **ADR-004**, which is short and single-purpose.

> **Checkpoint.** The instrument distinguishes them. If both come out the same, it is measuring
> nothing and the criteria are too generic. This checkpoint is the one that catches a useless
> instrument early, so do not skip it.

### 5. Full pass

All records in `../decisions/`. Output is a gap list per record, with N/A declared and reasoned.

> **Checkpoint.** The user rules on whether each gap is real. A gap the user rejects means the
> criterion is wrong for this project, not that the record is wrong. Record which, because that
> feedback is what tunes the set.

### 6. Convert to a guardrail

The same criteria, restated as a checklist consumed **while writing** rather than after. It should
be short enough to hold in the head, and it belongs where `making-architecture-decision` can read
it.

> **Checkpoint.** A record written with the checklist produces fewer gaps in step 5 than one written
> without. Until that is observed, it is an audit tool wearing a guardrail's label.

### 7. Mechanism for criteria that appear later

Mirror of the pruning rule, and the thing that makes the set live rather than frozen.

- **Promotion.** A criterion invoked ad hoc in more than one decision gets added to the set.
- **Pruning.** A criterion marked N/A across most records gets dropped or folded.
- **Provenance is mandatory on entry.** Anything joining the set carries its class and source, as
  in the register. A criterion with no provenance is someone's preference.

> **Checkpoint.** The mechanism is written into the instrument's own README, not held in a session.

---

## Scope guards

Do not score the two records that are unwritten, the ownership model and the Unity Catalog
boundary. Score what exists.

Do not use this to decide anything. It measures records; it does not choose between options. That
is what `making-architecture-decision` is for.

Do not merge it into `cases.md`. Different question, different input, different failure meaning.

Do not let the criteria set grow past what fits on one page. Past that it stops being a guardrail
and becomes a compliance exercise, which is the failure mode this whole folder exists to avoid.

---

## Open decisions, needed before step 1

**Guardrail first or audit first.** The guardrail is cheap and shapes new records. The audit needs
every record read and produces a backlog. They use the same criteria but the order changes what you
get in the first hour.

**Does a score exist at all.** The gap list works without one. If yes, confirm it is coverage over
applicable criteria and never shown alone.

**Who rules on a gap.** The user, or the DE lead, or both. The same question as ADR governance, and
the answer decides whether step 5 can complete in one session.

---

## Context a cold reader needs

The register was written after provenance was challenged mid-session. The challenge was fair: a
criterion assembled by someone already holding a view is suspect unless the criterion itself
predates the argument. That is why every entry carries a class and a source, and why four entries
are marked derived with no source at all.

The four derived entries are the ones to treat carefully here. Three are the conformance grading
verdicts, which are method rather than fact. The fourth is the claim that splitting a bundle later
is a state migration, which is untested.

One trap is recorded in the register and worth re-reading before curating: Prakash's product grain
of one denormalised table applies to entities, not to bundles. Confusing the two axes is what
produced the seven-bundle assumption this folder exists to prevent recurring.
