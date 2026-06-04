# Template, exploratory workshop summary, thematic spine

Expression template for a workshop summary on a thematic spine, exploratory mode.
This serves a workshop run to surface ideas, issues, facts, risks and
clarifications, not to take decisions. A decision-meeting is expressed elsewhere,
through the meeting-minutes template, never through this one. A workshop summary
has no owning authoring skill, so editing-docs expresses it directly from two
inputs against this template: the preparation analysis (the convergence, tension
and affinity clusters produced before the room met) and the workshop discussion
notes (the ideas and issues the room raised). The preparation half is known
before the session, the room half is supplied after. The five expression
concerns for this document type follow.

## Mapping

Map the two inputs onto this structure, in this order:

1. Title, the workshop subject, first word capitalised.
2. One meta row as a table: date, attendees, the framing question the workshop
   explored. Infer the date and mark it editable. Never invent attendee names,
   use "to be completed".
3. At a glance, the landscape: the headline ideas and issues, and the forks left
   open. No decisions, this workshop took none. Say so in one line.
4. One block per theme, in workshop order, plus one block for any gravity that
   emerged in the room without a preparation theme. Every block identical in
   shape:
   - Preparation: the convergence and the unresolved tension for that theme,
     plus a one-line cluster map. From the preparation analysis only.
   - In the room: the ideas, issues, risks and clarifications raised, marking
     what was new against the preparation clusters, and the questions left open.
     From the room notes only.
5. Cross-cutting, findings that span themes: recurring clusters and the open
   forks, held in one place so they do not fragment across blocks.
6. Next steps, the study and analysis tracks to run after the workshop. These
   are what to study, not work assigned. The workshop assigned none.

Pull the ideas, issues and open forks from the room notes, and the convergence
and tension from the preparation analysis. Never record a decision, an owner or
a commitment the room did not make, the exploratory mode has no slot for them by
design. A theme with no room notes carries `🔲 To be defined`, it is never
back-filled from the preparation half.

## Formatting

- Meta and forks as tables. The fork table is two columns: fork, where it stands.
- Ideas, issues, risks and open questions as bullets written as natural
  sentences, never the "label: value" pattern.
- Next steps as a table with two columns: track, what to study. No owner column
  and no status, nothing was assigned.
- Cluster references kept as coordinates where the preparation analysis used
  them, as locators, never re-expanded into prose.
- One footer line, not a table, carrying version, status, date, and a
  relates-to link to the preparation analysis or the source sheet. A table goes
  ragged when a short version sits beside a long filename, so a single line is
  used instead.

## Tone

Neutral, factual, exploratory. The reader is a sponsor or a theme owner. The
preparation line states what was found, the room block states what was raised.
No narration of the discussion, no hedging, and no decisions or commitments the
room did not make.

## Verbosity

At a glance under about 120 words. Each theme block tight: the preparation line
is three lines at most, each idea and open question is one line. Cross-cutting is
one short paragraph or a small table. Next steps is one line per track. The
document scales with the number of themes, not with the volume of discussion.
Raw discussion is dropped or linked, never transcribed.

## Reading efficiency

At a glance readable in 60 seconds and carrying the whole landscape: the
headline ideas, the open forks, and the fact that no decisions were taken. A
theme owner jumps to their block and reads preparation then room in under a
minute. Background and raw input sit behind the relates-to link, never inline.

## Skeleton

```markdown
# <Workshop subject>, summary

| Date | Attendees | Framing question |
| :--- | :--- | :--- |
| YYYY-MM-DD | <names, or to be completed> | <the question the workshop explored> |

This was an ideas and issues workshop. No decisions were taken.

## At a glance
- <headline idea or issue, one line>

| Open fork | Where it stands |
| :--- | :--- |
| <fork surfaced> | <the two poles, unresolved> |

## <Theme>
Preparation: <the convergence>. Tension: <the unresolved split>. Clusters: <coordinate map, one line>.
In the room:
- <idea, issue, risk or clarification raised, marked new if not in the prep clusters>
- Open: <question left on the table>

## <Gravity without a preparation theme>
In the room:
- <idea, issue or risk raised>
- Open: <question left on the table>

## Cross-cutting
<findings that span themes: recurring clusters, the open forks. One paragraph or a small table.>

## Next steps
| Track | What to study |
| :--- | :--- |
| <study track> | <how to adapt to or take the AI opportunity> |

*Version 1.0, Draft, YYYY-MM-DD. Relates to <preparation analysis or source sheet>.*
```

*Version 1.2, Draft, 2026-06-04.*
