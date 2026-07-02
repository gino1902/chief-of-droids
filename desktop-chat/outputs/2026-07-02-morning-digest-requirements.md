---
date: 2026-07-02
topic: morning-digest
---

# Morning digest and weekly objectives

## Problem frame

At the start of each working day, the previous day's activity and the current week's objectives sit scattered across Outlook, git, and SharePoint. The goal is one start-of-day recap: what happened yesterday, plus the objectives set for the week. Objectives are captured once on the first working day and read back on every following day.

## Requirements

**Daily digest**

- R1. On each working day, produce a recap of the previous working day's activity.
- R2. Digest sources are Outlook sent-items, git commits (chief-of-droids and any in-scope repos), and SharePoint or OneDrive file activity retrieved through the Graph Search API with KQL, not the recent endpoint (deprecated to November 2026) or drive-item date filtering.
- R3. The digest is scannable in about 60 seconds, activity and objectives first, minimal prose.
- R4. The digest shows the current week's objectives alongside the previous day's activity.

**Weekly objectives**

- R5. On the first working day of the week, the session prompts for the week's objectives.
- R6. Objectives are captured through an HTML view that supports add, edit, and reorder, and are persisted to a markdown file.
- R7. The HTML view writes captured changes back to the store. It is not display-only.
- R8. On other working days, objectives are read-only and rendered for reference.

**Surface and schedule**

- R9. The recap is delivered as an interactive session opened in a terminal on schedule.
- R10. A companion HTML view opens in the browser, showing the digest and hosting the objectives editor.
- R11. The first working day of the week is determined with FR bank-holiday awareness, not weekday arithmetic.

## Success criteria

- Gino sees the previous day's activity and the week's objectives at start of day, with no manual collation.
- Objectives captured once on the first working day persist and read back for the rest of the week.
- The digest is readable in about 60 seconds.

## Scope boundaries

- No Teams push in v1. Terminal and browser are the surface. Off-device reach is deferred.
- No digest-item status capture such as done or carry-over. Capture is objectives-only.
- Not headless or unattended. An interactive session preserves the no-write-without-confirmation gate.

## Key decisions

- Interactive session over headless, because it preserves the confirmation gate and avoids unattended token-refresh failures. The default claude invocation is the interactive REPL (verified).
- LaunchAgent over cron, because it gives GUI session access and catch-up on wake (verified against Apple docs). A machine that is off at the scheduled time does not catch up, it runs at the next scheduled time.
- A local server for write-back rather than a file page, because the browser sandbox blocks local writes and the save picker is secure-context only (verified against MDN).
- SharePoint activity through the Graph Search API with KQL, not the filter parameter or the recent endpoint, because recent is deprecated to November 2026 and date filtering on drive items is unreliable. Search API date scoping is verified.

## Dependencies and assumptions

- The Microsoft 365 MCP connector exposes mail read and Graph search. This is the one gating dependency and is currently unverified.
- Node.js is installed. Confirmed.
- The git-workspace MCP is scoped to chief-of-droids, so client repos may be out of scope. Git is a secondary signal, not the primary source.

## Outstanding questions

### Resolve before planning

- [Affects R2][User decision] Include SharePoint or OneDrive file activity in v1 through the Search API, or defer to v2 and ship Outlook plus git first?
- [Affects R9, R10][User decision] Terminal and browser only, or add a Teams post for off-device reach?

### Deferred to planning

- [Affects R2][Needs research] Confirm the Microsoft 365 MCP connector exposes mail read, Graph search, and any Teams write.
- [Affects R9][Technical] The exact interactive-seed mechanism for claude in a terminal launched from a LaunchAgent.
- [Affects R6, R7][Technical] The local server write-back path and its teardown at session end.
- [Affects R11][Needs research] The FR bank-holiday source for the first-working-day check.

## Next steps

- Confirm assumptions where required.
- Settle on v1 scope.
- Execute plan step.
