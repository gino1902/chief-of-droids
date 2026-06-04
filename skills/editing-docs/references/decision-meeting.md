# Template, decision meeting, problem solving and solutioning

Expression template for a problem-solving decision meeting. This serves a meeting run to decide, by aligning on a diagnostic, working a solution, or agreeing its execution, not to explore openly. An exploratory workshop is expressed through `workshop-summary-thematic`, general meeting outcomes through `60s-meeting-minutes`. The diagnostic, and sometimes the candidate solutions, are prepared before the meeting and live in their own files. This template references them and never reproduces them. A meeting record has no owning authoring skill, so editing-docs expresses it directly against this template. The five expression concerns for this document type follow.

## Mapping

Map the prepared inputs and the meeting outcome onto this structure, in this order:

1. Title, the meeting subject, first word capitalised, marked as a decision record.
2. A header of three lines: Date, Attendees, and Under decision. Under decision introduces a bulleted list of the problems or risks being decided, one or several. Infer the date and mark it editable. Never invent attendee names, use "to be completed".
3. A purpose line naming which of the three orientations this meeting served, align on the diagnostic, work the solution, agree execution, one or more.
4. A references block linking the issue or risk file and, if prepared, the solution or mitigation file. The template references these, it never reproduces their content.
5. One section per served purpose, in the order diagnostic, solution, execution, omitting any purpose the meeting did not serve:
   - Diagnostic, only if alignment was a purpose: the state before, shared or contested, and the diagnostic the meeting aligned on, or what stays contested and how it will be resolved.
   - Solution, only if solutioning was a purpose: the option set referenced, the direction chosen with its reason, and any open design question.
   - Execution, only if planning was a purpose: the commitments as a bulleted list, each line carrying what was committed, the owner, and the date.
6. Carried forward, what could not be closed and moves to a follow-up meeting.

Record what the meeting decided about the issue, risk and solution, never their content, that detail lives in the linked files. Never invent a decision, an owner, a date or an agreed diagnostic the meeting did not produce. A purpose the meeting did not serve has no section, it is omitted.

## Formatting

- Lines and lists only, no tables. The header is three lines, Date, Attendees, Under decision, the last introducing a bulleted list of the items being decided.
- The commitments are a bulleted list, each a natural sentence carrying what was committed, the owner, and the date. Unknown owners are "to be assigned" and unknown dates "to be set", never invented.
- The purpose line and the references as natural sentences and links, never reproduced content, never a bare URL.
- Diagnostic and solution outcomes as bullets written as natural sentences, never the "label: value" pattern.
- One footer line carrying version, status, date, and relates-to links to the issue, risk and solution files.

## Tone

Neutral, factual, decisional. The reader is an attendee or an owner picking up a commitment. Record what was decided and committed, not the debate. Where a purpose did not reach closure, say so plainly and point to the follow-up.

## Verbosity

Tight. The diagnostic is the agreed statement, not the discussion that produced it. The solution section names the chosen direction and links the option set, it does not reproduce the options. Execution is one line per commitment. Prepared inputs are linked, never copied. The record scales with the number of decisions and commitments, not the length of the meeting.

## Reading efficiency

An attendee reads the purpose line and knows what the meeting was for. An owner finds their commitment in the execution list in seconds. Decisions and commitments come before anything carried forward. Detail on the issue, risk or solution sits one link away.

## Skeleton

```markdown
# <Meeting subject>, decision record

Date: YYYY-MM-DD
Attendees: <names, or to be completed>
Under decision:

- <problem or risk being decided>
- <another, if several>

This meeting served to <align on the diagnostic, work the solution, agree execution>, one or more.

References:

- Issue or risk: [<title>](<link>)
- Solution or mitigation: [<title>](<link>), if prepared

## Diagnostic

- Before the meeting the diagnostic was <shared, or contested because opinions differed or facts conflicted>.
- The meeting aligned on <the agreed diagnostic>, or <what stays contested and how it will be resolved>.

## Solution

- The options considered are held in [<reference>](<link>).
- The meeting chose <the direction or option> because <reason>.
- Still open, <the design question not yet resolved>.

## Execution

- <what was committed>, owner <owner, or to be assigned>, by <date, or to be set>.

## Carried forward

- <what could not be closed and moves to a follow-up meeting>

*Version 1.0, Draft, YYYY-MM-DD. Relates to the issue, risk and solution files referenced above.*
```

*Version 1.0, Draft, 2026-06-04.*
