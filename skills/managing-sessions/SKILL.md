---
name: managing-sessions
description: >
  Analyses Claude.ai project session history to extract decisions, ADRs, tool
  quirks, corrections, and open items — then recommends which sessions to prune
  and writes a structured summary log of extracted value to disk. Load this
  skill whenever a user is about to delete sessions, asks what to keep, requests
  session hygiene, or when the bootstrap sentinel check fires. Always use
  before bulk-deleting sessions — never let the user prune blind. Triggers on:
  "manage sessions", "analyse sessions", "prune sessions", "session hygiene",
  "what should I keep", "challenge memories", "check memories".
---
<!-- version: 1.9 | author: chief-of-droids workspace | last_updated: 2026-05-31 -->

# Managing Sessions Skill

Extracts value from session history, recommends pruning, writes structured
output to disk, and challenges userMemories against on-disk sources for
stale or contradicted decisions.

**Scope:** Session analysis, knowledge extraction, pruning recommendations,
and memory integrity checks. Does not delete sessions — deletion is a
manual user action in the claude.ai UI.

**Storage layout:**

| Output | Path | Created when |
| :--- | :--- | :--- |
| Analysis findings | `/Users/gilllesmourgues/Workspace/chief-of-droids/.tasks/sessions-findings/` | Every confirmed run |
| Session removal log | `/Users/gilllesmourgues/Workspace/chief-of-droids/.logs/sessions-removed/` | Only when sessions are confirmed for removal |
| Sentinel | `/Users/gilllesmourgues/Workspace/chief-of-droids/.tasks/sessions-findings/sentinel.md` | Written/overwritten at end of every confirmed run |

**Multi-project note:** This skill is shared across all workspace projects.
Both output directories are centralised at workspace root — findings and
removal logs accumulate across projects. `recent_chats` is project-scoped;
run the skill once per project to build complete cross-project coverage.

**Bootstrap trigger rule (system prompt):**
At bootstrap: call `recent_chats n=1` and read
`.tasks/sessions-findings/sentinel.md`. If sentinel is absent OR
`(recent_chats[0].updated_at - sentinel.last_run_date) > 10 days`, surface
which condition is met and ask the user if they want to run the
`managing-sessions` skill. Run only on explicit yes.

---

## Sentinel File Format

Path: `/Users/gilllesmourgues/Workspace/chief-of-droids/.tasks/sessions-findings/sentinel.md`

```markdown
# Managing Sessions — Sentinel

| Field | Value |
|:------|:------|
| last_run_date | YYYY-MM-DD |
| last_run_project | [project name] |
```

Written or overwritten at the end of every confirmed skill run.
A single file — not date-stamped, not appended. Always reflects the most
recent run across all projects.

---

## Reference Files

- `references/what-to-capture.md` — read at the start of every analysis run;
  defines the 7 capture categories and their canonical `conversation_search`
  queries — mandatory input for Pass 2
- `references/session-log-schema.md` — read before any write operation;
  defines the canonical format for both output files
- `references/memory-contradiction-rules.md` — read before the userMemories
  challenge workflow; defines contradiction patterns to check

---

## Confidence Model

A single pass against session summaries has an unknown false-negative rate —
summaries are lossy, search queries are generic, and on-disk verification is
shallow. Five passes are required for high-confidence extraction.

| Pass | Tool | Purpose |
| :--- | :--- | :--- |
| Pass 1 | `recent_chats n=20` | Baseline inventory — broad session coverage |
| Pass 2 | `conversation_search` × 7 | One targeted search per category using canonical queries from `what-to-capture.md` |
| Pass 3 | `filesystem:read_text_file` per candidate target file | Verify `on-disk` claims by reading the actual file — not TASKS.md done entries |
| Pass 4 | `conversation_search` × N (residual) | Triggered when `not-on-disk` count is 6 or more — confirm each finding is not recorded in a session the summary missed |
| Pass 5 | Full on-disk read of all authoritative sources | Memory challenge: read fresh, apply all rules from `memory-contradiction-rules.md` |

**Known tool limitations:**
- `recent_chats` summaries are lossy — findings not captured in the summary are
  invisible to Pass 1. Pass 2 targeted searches compensate but cannot guarantee
  full coverage.
- `recent_chats` is project-scoped — sessions from other projects are not
  returned. Run separately per project for complete cross-project coverage.
- `conversation_search` can return false positives — sessions that match the
  query string but contain no relevant finding in the target category. Discard
  these; do not count them as confirmed findings or as misses.

Never skip passes. A finding classified `on-disk` from a TASKS.md done entry
alone is not verified — the target file must be read.

---

## Step 0 — Project identity resolution (always first)

Before any other action, resolve the active project name. This determines
filenames, headers, and memory challenge scope.

1. Attempt to read the active repo-level `CLAUDE.md` via Filesystem tool.
   Resolution order:
   - If the session is routed to a named repo: read
     `/Users/gilllesmourgues/Workspace/chief-of-droids/<repo>/CLAUDE.md`
   - Otherwise: read `/Users/gilllesmourgues/Workspace/chief-of-droids/desktop-chat/CLAUDE.md`
2. Extract project name from the file header (first `# ` heading or
   `## Scope` section). Use the heading text as the project identifier.
3. If `CLAUDE.md` is unreadable or contains no identifiable project name:
   ```
   ⚠️ Project name could not be determined.
   Filenames and headers will use "unknown-project".
   Memory challenge scope will default to workspace-level sources only.
   Proceed anyway? (yes / no)
   ```
   — Wait for explicit user response before continuing.
   — If user says no: halt the skill entirely.
   — If user says yes: set project identifier to `unknown-project` and proceed.

The resolved project name is used in all subsequent steps as `<project>`.

---

## Workflow: analyse sessions

Trigger: `manage sessions` | `analyse sessions` | `session hygiene` |
`what should I keep` | bootstrap sentinel check (user confirmed yes)

### Pass 1 — Baseline inventory

1. Run Step 0 — Project identity resolution
2. Read `references/what-to-capture.md` via Filesystem tool
3. Call `recent_chats` with `n=20`
   — If `recent_chats` returns fewer sessions than the project history suggests
     (e.g. returning 5 sessions when the user knows there are 15), flag:
     `⚠️ Partial result — session count may be incomplete; proceeding at Medium confidence`
4. For each session summary, evaluate against all 7 categories in
   `what-to-capture.md` — note hits by category, session title, and date
5. Build initial finding set — mark all as `unclassified`

### Pass 2 — Category-targeted search

6. For each of the 7 categories, call `conversation_search` using the
   canonical query defined in `what-to-capture.md` → `search_query` field
7. For each result returned: confirm the session actually contains a finding
   in the target category before adding it — discard false positives (sessions
   matching the query string but containing no relevant finding)
8. Merge confirmed new hits into the finding set — deduplicate against Pass 1
   results using: session URL + finding category + finding description as the
   deduplication key
9. Any finding present in Pass 2 but absent from Pass 1 is flagged:
   `⚠️ Summary miss — surfaced only by targeted search`

### Pass 3 — On-disk verification

10. For each finding tentatively classified `on-disk`:
    - Identify the named target file (from TASKS.md done entry, skill file,
      or docs/ reference)
    - Read that file via `filesystem:read_text_file`
    - Confirm the specific content is present — do not accept TASKS.md done
      entries as proof; read the target file directly
    - If content confirmed → classify `on-disk`
    - If content absent → reclassify `not-on-disk`
    - If file unreadable → classify `on-disk-unverified`
11. Also check centralised docs files for prior cross-project captures:
    - `/Users/gilllesmourgues/Workspace/chief-of-droids/docs/mcp-tool-quirks.md` (if it exists)
    - `/Users/gilllesmourgues/Workspace/chief-of-droids/docs/system-prompt-changelog.md` (if it exists)
    — A finding already in either file is `on-disk` regardless of source project
12. Findings with no identifiable target file → classify `not-on-disk`

### Pass 4 — Residual search (triggered when `not-on-disk` count is 6 or more)

13. For each `not-on-disk` finding, call `conversation_search` using 2–3
    keywords specific to that finding (not the category query — the finding itself)
14. Apply the same false-positive filter as Pass 2 — confirm the session
    actually contains the finding before reclassifying
15. If confirmed captured → reclassify `on-disk` with source noted
16. If not found → classification confirmed `not-on-disk`

### Pass 5 — Synthesis and output

17. Output extraction table in chat:
    | Session | Date | Category | Finding | Status | Pass surfaced |
18. Produce pruning recommendation:
    - Keep: sessions containing `not-on-disk` findings not yet extracted
    - Prune: sessions where all findings are `on-disk` or `superseded`
    - State the boundary explicitly: e.g. "Prune everything before YYYY-MM-DD"
19. State confidence level:
    - High: Pass 1 returned full expected session count; Pass 3 verified all
      `on-disk` claims; Pass 4 run if triggered
    - Medium: Pass 1 returned partial result, OR Pass 3 partially verified
      (some target files unreadable)
    - Low: Pass 3 skipped — flag explicitly
20. Ask: "Confirm extraction and pruning plan before I write?"
21. On confirmation:
    a. Run **write findings** workflow (always)
    b. Run **write removal log** workflow (only if sessions are confirmed for removal)
    c. Run **write sentinel** workflow (always)
    d. Run **challenge memories** workflow
22. Produce manual deletion checklist (chat only — user executes in UI):
    - List each session to delete by title and date
    - State: "Delete these manually in claude.ai project settings → Sessions"

---

## Workflow: write findings

Trigger: called internally after user confirms analysis output

Steps:
1. Read `references/session-log-schema.md` via Filesystem tool
2. Determine findings file path:
   `/Users/gilllesmourgues/Workspace/chief-of-droids/.tasks/sessions-findings/YYYY-MM-DD-<project>-findings.md`
   — If a file with this name already exists, append `-2`, `-3` etc.
     Never overwrite.
3. Build findings file per **Findings schema** in `session-log-schema.md`:
   - Header: run date, source project, confidence level, session counts
   - Extracted findings table with classification and promotion tracking
   - Net-new content section (verbatim, for `not-on-disk` findings)
   - Known gaps table
   - Memory challenge results (added after challenge memories runs)
4. Write file via Filesystem tool
5. Report path written

---

## Workflow: write removal log

Trigger: called internally after user confirms — **only if at least one
session is confirmed for removal**. Do not create this file if the pruning
recommendation results in zero sessions being removed.

Steps:
1. Read `references/session-log-schema.md` via Filesystem tool
2. Determine removal log path:
   `/Users/gilllesmourgues/Workspace/chief-of-droids/.logs/sessions-removed/YYYY-MM-DD-<project>-removed.md`
   — If a file with this name already exists, append `-2`, `-3` etc.
     Never overwrite.
3. Build removal log per **Removal log schema** in `session-log-schema.md`:
   - Header: run date, source project, session count removed
   - Removed sessions table: title | date | reason | findings reference
4. Write file via Filesystem tool
5. Report path written

---

## Workflow: write sentinel

Trigger: called internally after write findings completes — always

Steps:
1. Build sentinel content:
   ```markdown
   # Managing Sessions — Sentinel

   | Field | Value |
   |:------|:------|
   | last_run_date | YYYY-MM-DD |
   | last_run_project | <project> |
   ```
   Where `YYYY-MM-DD` is today's date and `<project>` is the resolved project name.
2. Write (overwrite) `/Users/gilllesmourgues/Workspace/chief-of-droids/.tasks/sessions-findings/sentinel.md`
   via Filesystem tool — this file is always overwritten, never appended.
3. Report: `Sentinel updated: YYYY-MM-DD`

---

## Workflow: challenge memories

Trigger: `challenge memories` | `check memories` | called automatically
after write workflows complete

Steps:
1. Read `references/memory-contradiction-rules.md` via Filesystem tool
2. Read authoritative on-disk sources fresh — scope depends on active project:

   **Always read (workspace-level):**
   - `/Users/gilllesmourgues/Workspace/chief-of-droids/desktop-chat/CLAUDE.md`
   - `/Users/gilllesmourgues/Workspace/chief-of-droids/.tasks/TASKS.md`
   - `/Users/gilllesmourgues/Workspace/chief-of-droids/skills/HOW-TO-TRIGGER.md`
   - `/Users/gilllesmourgues/Workspace/chief-of-droids/skills/managing-tasks/SKILL.md`
   - `/Users/gilllesmourgues/Workspace/chief-of-droids/skills/managing-sessions/SKILL.md`

   **Also read if project is repo-scoped (not workspace root):**
   - `/Users/gilllesmourgues/Workspace/chief-of-droids/<project>/CLAUDE.md`
   - `/Users/gilllesmourgues/Workspace/chief-of-droids/<project>/TASKS.md`

   **Also read if changed in current session:**
   - Any other skill SKILL.md written or changed in this session
   - Active system prompt `<rules>` block (available in context)

3. Apply all rules from `memory-contradiction-rules.md` against userMemories
4. Output contradiction table in chat:
   | Memory claim | Rule triggered | On-disk state | Risk | Recommendation |
5. Append results to the findings file written in **write findings** workflow
6. Do not modify userMemories — surface findings only.
   Flag: `⚠️ userMemories are managed by Anthropic — corrections require
   the user to edit them via Claude.ai Settings → Memory`

---

## Failure Handling

| Condition | Action |
| :--- | :--- |
| `CLAUDE.md` unreadable or no project name found | Warn user, ask to proceed — halt if user declines |
| `recent_chats` returns empty | Flag: `⚠️ No sessions returned — tool may be unavailable or project has no history` |
| `recent_chats` returns partial result | Flag count discrepancy; proceed at Medium confidence |
| `what-to-capture.md` unreadable | Halt: `⚠️ what-to-capture.md unreadable — cannot run analysis without capture categories` |
| `session-log-schema.md` unreadable | Halt all writes: `⚠️ session-log-schema.md unreadable — no files written; findings available in chat` |
| Target file unreadable in Pass 3 | Flag finding as `on-disk-unverified` — do not classify as confirmed `on-disk` |
| `conversation_search` returns false positives | Discard silently — do not add to finding set |
| Findings filename already exists | Append `-2`, `-3` suffix — never overwrite |
| Removal log filename already exists | Append `-2`, `-3` suffix — never overwrite |
| Zero sessions confirmed for removal | Skip write removal log entirely — do not create an empty file |
| Pass 4 not triggered (`not-on-disk` count < 6) | Proceed to Pass 5 — not a failure |
| Sentinel write fails | Flag: `⚠️ Sentinel not updated — bootstrap trigger will re-fire next session`; do not block other outputs |
| Filesystem tool unavailable | Halt all write operations; deliver findings as chat output only; note confidence is Low |

---

## Composes With

| Skill | When |
| :--- | :--- |
| `managing-tasks` | When a session finding surfaces an untracked task or open item |
| `writing-docs` | When net-new findings warrant a new reference doc (e.g. `mcp-tool-quirks.md`) |

---

## QA Checklist

- [ ] Step 0 run first — project name resolved before any other action
- [ ] Warning issued and user confirmed if project name could not be resolved
- [ ] `what-to-capture.md` read via Filesystem tool — not from memory
- [ ] Pass 1: `recent_chats n=20` called; partial result flagged if count seems low
- [ ] Pass 2: `conversation_search` called once per category (7 calls minimum)
- [ ] Pass 2: false positives discarded before adding to finding set
- [ ] Pass 2: deduplication applied on session URL + category + description
- [ ] Pass 3: every `on-disk` claim verified by reading the target file directly
- [ ] Pass 3: centralised docs files checked for cross-project captures
- [ ] Pass 4: residual search run when `not-on-disk` count is 6 or more
- [ ] Pass 4: false-positive filter applied before reclassifying findings
- [ ] Pass 5: all authoritative sources read fresh — workspace + repo-scoped
- [ ] Confidence level stated explicitly in output
- [ ] Findings file written to `.tasks/sessions-findings/` — always on confirmation
- [ ] Removal log written to `.logs/sessions-removed/` — only if sessions removed
- [ ] Removal log NOT created if zero sessions are confirmed for removal
- [ ] Both filenames include `<project>` identifier
- [ ] Sentinel written/overwritten at end of every confirmed run
- [ ] Pruning recommendation states an explicit date boundary
- [ ] Deletion checklist produced as chat output — not executed by skill
- [ ] No session deleted by the skill under any circumstance

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.9        |
| Last Updated | 2026-05-31 |
| Status       | Draft      |
