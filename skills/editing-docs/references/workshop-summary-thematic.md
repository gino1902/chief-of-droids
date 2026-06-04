# Template, workshop summary, thematic spine

Expression template for a workshop summary on a thematic spine. A workshop
summary has no owning authoring skill, so editing-docs expresses it directly
from two inputs against this template: the preparation analysis (the
convergence, tension, and affinity clusters produced before the room met) and
the workshop discussion notes (what the room decided and left open). The
preparation half is known before the session, the room half is supplied after.
The five expression concerns for this document type follow.

## Mapping

Map the two inputs onto this structure, in this order:

1. Title, the workshop subject, first word capitalised.
2. One meta row as a table: date, attendees, the framing question the workshop
   answered. Infer the date and mark it editable. Never invent attendee names,
   use "to be completed".
3. At a glance, the executive top: the decisions taken, the status of each
   strategic fork surfaced in preparation, and the top moves. Drawn from the
   room notes, never from the preparation half.
4. One block per theme, in workshop order, every block identical in shape:
   - Preparation: the convergence and the unresolved tension for that theme,
     plus a one-line cluster map. From the preparation analysis only.
   - In the room: what was decided, points raised that were not already in the
     preparation clusters, and questions left open. From the room notes only.
5. Cross-cutting, findings that span themes: recurring clusters and the fork
   outcomes, held in one place so they do not fragment across theme blocks.
6. Actions, who does what next, consolidated.

Pull the decisions, the fork outcomes, and the actions from the room notes, and
the convergence and tension from the preparation analysis. Never synthesise a
discussion that did not happen. A theme with no room notes carries
`🔲 To be defined`, it is never back-filled from the preparation half.

## Formatting

- Meta and forks as tables. The fork table is two columns: fork, outcome.
- Decisions, new points, and open questions as bullets written as natural
  sentences, never the "label: value" pattern.
- Actions as a table with three columns: action, owner, status. Unknown owners
  are "to be assigned", never invented.
- Cluster references kept as coordinates where the preparation analysis used
  them, as locators, never re-expanded into prose.
- One footer line, not a table, carrying version, status, date, and a
  relates-to link to the preparation analysis or the source sheet. A table goes
  ragged when a short version sits beside a long filename, so a single line is
  used instead.

## Tone

Neutral, factual, decisional. The reader is a sponsor or a theme owner. The
preparation line states what was found, the room block states what was decided.
No narration of the discussion, no hedging, no restating the debate.

## Verbosity

The executive top under about 120 words. Each theme block tight: the
preparation line is three lines at most, each decision and open question is one
line. Cross-cutting is one short paragraph or a small table. The document scales
with the number of themes, not with the volume of discussion. Raw discussion is
dropped or linked, never transcribed.

## Reading efficiency

The executive top readable in 60 seconds and carrying the whole "so what":
decisions, fork outcomes, next moves. A theme owner jumps to their block and
reads preparation then room in under a minute. Background and raw input sit
behind the relates-to link, never inline.

## Skeleton

```markdown
# <Workshop subject>, summary

| Date | Attendees | Framing question |
| :--- | :--- | :--- |
| YYYY-MM-DD | <names, or to be completed> | <the question the workshop answered> |

## At a glance
- <decision as a natural sentence, with the reason if given>

| Strategic fork | Outcome |
| :--- | :--- |
| <fork surfaced in preparation> | <resolved how, or parked> |

Top moves: <one line, or "see Actions">.

## <Theme>
Preparation: <the convergence>. Tension: <the unresolved split>. Clusters: <coordinate map, one line>.
In the room:
- Decided: <decision, or 🔲 To be defined>
- New: <point raised that was not in the preparation clusters>
- Open: <question left on the table>

## Cross-cutting
<findings that span themes: recurring clusters, fork status. One paragraph or a small table.>

## Actions
| Action | Owner | Status |
| :--- | :--- | :--- |
| <action> | <owner, or to be assigned> | <To do / Done> |

*Version 1.0, Draft, YYYY-MM-DD. Relates to <preparation analysis or source sheet>.*
```

*Version 1.0, Draft, 2026-06-04.*
