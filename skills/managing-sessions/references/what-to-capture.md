<!-- version: 1.2 | author: chief-of-droids workspace | last_updated: 2026-03-28 -->

# What to Capture

Categories of valuable content to scan for during session analysis.
Maintained against Anthropic best practices and workspace conventions.
Read this file at the start of every `analyse sessions` workflow run.

The `search_query` field in each category is the canonical query for Pass 2
of the `analyse sessions` workflow — one `conversation_search` call per
category, using this exact query string.

---

## Contents

1. [Architecture & Design Decisions](#1-architecture--design-decisions)
2. [Tool Behaviour & MCP Quirks](#2-tool-behaviour--mcp-quirks)
3. [Corrections to Training Knowledge](#3-corrections-to-training-knowledge)
4. [Open Items & Parked Decisions](#4-open-items--parked-decisions)
5. [Skill & Workflow Decisions](#5-skill--workflow-decisions)
6. [System Prompt Changes](#6-system-prompt-changes)
7. [Verified External Sources](#7-verified-external-sources)
8. [Update Protocol](#update-protocol)

---

## Category Definitions

### 1. Architecture & Design Decisions

Decisions about how the workspace, framework, or a project is structured.
Includes choices between alternatives, rationale for approaches taken,
and explicit rejections of alternatives with reasons.

**Signal phrases:** "we decided", "the reason we", "instead of", "rejected",
"chosen because", "architecture", "design decision", "ADR"

**search_query:** `"decision architecture chosen rejected rationale"`

**Capture if:** the decision is not recorded in `CLAUDE.md`, a skill file,
or a `docs/` document with a `[DECISION]` marker.

**On-disk verification target:** `CLAUDE.md`, relevant skill `SKILL.md`,
or `docs/` file named for the decision domain.

**Risk if missed:** future sessions may re-litigate settled decisions or
implement the rejected approach without knowing it was evaluated.

---

### 2. Tool Behaviour & MCP Quirks

Confirmed failure modes, workarounds, and non-obvious behaviours of MCP tools,
Claude Desktop, or the WSL2 environment — discovered through actual use, not
assumed from training knowledge.

**Signal phrases:** "silently fails", "workaround", "use X instead of Y",
"always use", "never use", "fails when", "path format", "MCP log", "tool error"

**search_query:** `"silently fails workaround path format MCP tool error"`

**Capture if:** the quirk is not already in `docs/mcp-tool-quirks.md`
(note: this file is a known gap as of 2026-03-28 — does not yet exist).

**On-disk verification target:** `/home/gino/workspace/docs/mcp-tool-quirks.md`
— if file does not exist, all tool quirk findings are `not-on-disk` by default.

**Risk if missed:** future sessions repeat the same debugging cycles.

---

### 3. Corrections to Training Knowledge

Cases where Claude made an incorrect claim based on training knowledge,
the claim was challenged, and the correct behaviour was verified against
live official documentation.

**Signal phrases:** "retracted", "incorrect", "stale", "actually", "verified",
"fetched", "official docs say", "not correct", "correction"

**search_query:** `"retracted incorrect stale verified correction official docs"`

**Capture if:** the correction affects a claim in any workspace `.md` file
or in `userMemories`. Mark corrected files with `⚠️ Stale — verify before use`
if they have not already been updated.

**On-disk verification target:** the specific workspace file the claim appeared
in (e.g. `claude-stack-explainer.md`, `skills-reference.md`). Read that file
and confirm the correction is present with a verification date.

**Risk if missed:** stale training-knowledge claims persist in docs or memory,
get cited as authoritative, and cause downstream errors.

---

### 4. Open Items & Parked Decisions

Explicit decisions to defer, items left unresolved at session end, or
design questions that were raised but not answered.

**Signal phrases:** "parked", "to be defined", "deferred", "next session",
"follow up", "open question", "🔲", "backlog", "not yet"

**search_query:** `"parked deferred open question backlog not yet defined"`

**Capture if:** the item does not appear in `TASKS.md` as a backlog entry.
If it should be a task, compose with `managing-tasks` to add it.

**On-disk verification target:** `/home/gino/workspace/TASKS.md` — read the
Backlog section and confirm the item is present as a TASK entry.

**Risk if missed:** deferred decisions silently disappear and are later
assumed resolved.

---

### 5. Skill & Workflow Decisions

Changes to skill design, trigger logic, write authority rules, composition
patterns, or workflow step ordering — including the rationale.

**Signal phrases:** "skill", "trigger", "description", "pushy", "compose",
"write authority", "workflow", "assessment", "frontmatter"

**search_query:** `"skill trigger description pushy workflow write authority"`

**Capture if:** the decision changed a skill file and the rationale was
stated in session but not written into the skill as a `[DECISION]` marker
or comment.

**On-disk verification target:** the relevant skill's `SKILL.md` — read it
and confirm a `[DECISION]` marker or inline comment documents the rationale.

**Risk if missed:** skill changes look arbitrary when reviewed later; the
`creating-skills` assessment workflow may flag them as unexplained deviations.

---

### 6. System Prompt Changes

Material additions, removals, or rewrites to the Claude Desktop project
system prompt. The system prompt is not version-controlled on disk — any
change made is only recoverable from session history.

**Signal phrases:** "system prompt", "custom instructions", "<rules>",
"<skills>", "<defaults>", "added to prompt", "prompt rule"

**search_query:** `"system prompt rules added custom instructions defaults"`

**Capture if:** the change is not already recorded in a versioned file.
Write a new entry in `docs/system-prompt-changelog.md`
(note: this file is a known gap as of 2026-03-28 — does not yet exist).

**On-disk verification target:** `/home/gino/workspace/docs/system-prompt-changelog.md`
— if file does not exist, all system prompt change findings are `not-on-disk`
by default. This is the highest-risk gap in the workspace.

**Risk if missed:** system prompt corruption or drift has no recovery point.

---

### 7. Verified External Sources

URLs that were successfully fetched and whose content was used to make a
confirmed decision or correction. Needed for re-verification when docs are
next updated.

**Signal phrases:** "fetched", "verified against", "official source",
"docs say", "from the docs", "live verification"

**search_query:** `"fetched verified official source docs live"`

**Capture if:** the URL is not already cited in the relevant workspace file
with a fetch date.

**On-disk verification target:** the workspace file where the decision or
correction was applied — confirm the URL appears as a citation with a date.

**Risk if missed:** verification claims become unverifiable — cannot
distinguish tech-verified facts from training-knowledge claims.

---

## Update Protocol

This file must be updated when:
- A new category of recurring valuable session content is identified
- A canonical search query proves ineffective in practice — replace with
  a query that surfaces the right sessions
- Official Anthropic documentation introduces a new concept relevant
  to session or memory management
- A post-prune retrospective reveals a category that was missed

Update via `creating-skills` skill → `critique skill managing-sessions`.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.2        |
| Last Updated | 2026-03-28 |
| Status       | Draft      |
