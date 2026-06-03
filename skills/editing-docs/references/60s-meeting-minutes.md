# Template, 60-second meeting minutes

Expression template for meeting minutes. Minutes have no owning authoring skill,
so editing-docs expresses them directly from the raw notes against this template.
The five expression concerns for this document type follow.

## Mapping

Map raw notes onto this structure, in this order:

1. Title, the subject, first word capitalised.
2. One meta row as a table: date, attendees, what was reviewed. Infer the date
   and mark it editable. Never invent attendee names, use "to be completed".
3. Decisions, the choices made.
4. Requirements, only if any were raised.
5. Actions, who does what next.

Pull the decisions and the actions out of the notes. Everything else is dropped
or linked, never summarised.

## Formatting

- Decisions and requirements as bullets written as natural sentences, never the
  "label: value" pattern.
- Actions as a table with three columns: action, owner, status.
- Unknown owners are "to be assigned", never invented.
- One footer line, not a table, carrying version, status, date, and a
  relates-to link. A table goes ragged when a short version sits beside a long
  filename, so a single line is used instead.

## Tone

Neutral and factual. The reader is a busy stakeholder who was in the room or
needs the outcome. No narration, no hedging, no restating the discussion.

## Verbosity

Under about 150 words of body. Every decision and every action is one line.
Context or a related document is a one-line link, never a paragraph.

## Reading efficiency

Readable in 60 seconds. Decisions and actions first, because that is what the
reader came for. No prose summary of the meeting. If the reader needs the
background, the relates-to link carries it.

## Skeleton

```markdown
# <Subject>, minutes

| Date | Attendees | Reviewed |
| :--- | :--- | :--- |
| YYYY-MM-DD | <names, or to be completed> | <one line> |

## Decisions
- <decision as a natural sentence, with the reason if given>

## Requirement
- <requirement, only if raised>

## Actions
| Action | Owner | Status |
| :--- | :--- | :--- |
| <action> | <owner, or to be assigned> | <To do / Done> |

*Version 1.0, Draft, YYYY-MM-DD. Relates to <file, if any>.*
```

*Version 1.0, Draft, 2026-06-03.*
