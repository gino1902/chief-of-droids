---
name: standardizing-artefacts
description: >
  Audits any Claude Desktop instruction file — Project Instructions, CLAUDE.md,
  routing template, system prompt fragment, or SKILL.md — for deterministic
  execution risks. Runs 33 criteria across four structured blocks: Foundation
  (OBL+STR), Evidence Layer (EX+RSN), Behavior Contract (BRN+OUT), and
  Deployment Gate (DEF+DSK). For each block: audits the file, produces a
  structured violation report, proposes fixes with an explicit per-block approval
  gate, applies approved fixes, re-reads the file, then proceeds to the next
  block. Owns the fix phase. Produces a final deployment readiness verdict. Also
  supports a single-pass full audit mode.
  Load when the user says: "audit <file>", "check <file> for determinism",
  "standardize <file>", "review <file> for execution risks", "audit project
  instructions", "audit CLAUDE.md", "audit system prompt", "audit this file",
  "full audit <file>".
---
<!-- version: 1.5 | author: chief-of-droids workspace | last_updated: 2026-04-11 -->

# Standardizing Artefacts Skill

Audits Claude Desktop instruction files for deterministic execution risk. Owns the fix phase.

---

## Reference Files

- `references/determinism-audit.md` — 33 audit criteria in four blocks (B1–B4); read at Step 0
- `references/audit-report-schema.md` — violation report output schema; read before first block report
- `references/qa-checklist-audit.md` — QA checklist for the `audit` (block-by-block) workflow
- `references/qa-checklist-full.md` — QA checklist for the `audit --full` (single-pass) workflow

---

## Step 0 — Environment Detection

Probe: attempt `filesystem:read_text_file references/determinism-audit.md`.
- Read succeeds → **Claude Desktop** — criteria loaded; proceed
  After successful read: verify that block definitions B1, B2, B3, and B4 are all present
  in the loaded content. If any block definition is absent: halt. Report:
  "Audit criteria file incomplete — [block] definition absent. Audit cannot proceed."
- Read fails → **Claude.ai** — Filesystem MCP unavailable

Report before any other action:
- ✅ `Environment: Claude Desktop — criteria loaded from references/determinism-audit.md`
- ⚠️ `Environment: Claude.ai — Filesystem MCP unavailable`

If Claude.ai detected: both reference files must be pasted inline by the user.
Halt and state: "Audit cannot proceed — paste references/determinism-audit.md and
references/audit-report-schema.md inline to continue."
Do not proceed without criteria content.
Reason: evaluating without criteria produces structurally valid but semantically empty reports — every criterion passes by default.

---

## File Input Resolution

Detect delivery mode from the prompt before reading. State the detected mode.

| Signal | Mode | Tool |
|:-------|:-----|:-----|
| Path starting with `/` | Filesystem | `filesystem:read_text_file <path>` |
| Filename only, or "uploaded" | Upload | `bash_tool: cat /mnt/user-data/uploads/<filename>` |
| File content present in prompt | Inline | Use content as-is — no read required |

If no delivery mode signal is present: halt. Report: "File delivery mode unresolved — provide a file path, filename, or paste content inline."

Tool note: `filesystem:write_file` uses the `content` parameter (not `file_text`).

If file cannot be read (path not found, upload absent): halt.
Report: "File unreadable — [mode] [path/filename]. Audit cannot proceed."
Do not infer or fabricate file content.
Reason: fabricated content produces criterion evaluations against a file that does not exist — every finding would be invalid.

---

## File Type Declaration

Classify and state the file type before any criterion is applied:

| Type | Identifying signals |
|:-----|:-------------------|
| Project Instructions | Single text block; no markdown headers; operator system prompt for a Claude Desktop Project |
| CLAUDE.md | Markdown file; `#`-headed sections; session bootstrap context; injected as user message |
| Routing template | Contains explicit conditional logic selecting behavior by task type |
| System prompt fragment | Partial or full system prompt; may contain XML component tags |
| SKILL.md | Markdown file; `##`-headed sections; YAML frontmatter block; declares workflows and reference files for agent skill routing |

If file matches no type: prepend to all block reports —
`Note: file type unrecognized — audited as Project Instructions.`

When file type is SKILL.md: the following criteria do not apply —
- STR-2 (XML component separation) — SKILL.md files use markdown by format convention
- STR-5 (formatting consistency with output) — output is produced via reference files, not inline
- EX-1 through EX-5 (worked examples) — examples are contained in reference files loaded on demand, not inline

---

## Workflow: `audit <file>` — Block-by-Block (default)

**Trigger:** "audit <file>" | "check <file> for determinism" | "standardize <file>" |
"review <file> for execution risks" | "audit project instructions" | "audit CLAUDE.md" |
"audit system prompt" | "audit this file"
If prompt contains `--full` flag: route to `audit <file> --full` workflow instead.

**Steps:**

1. Run Step 0 — environment detection; criteria loaded from Step 0 read result
2. Read `references/audit-report-schema.md`
   If read fails: halt. Report: "Report schema unavailable — cannot produce structured output. Audit cannot proceed."
3. Resolve file input — detect mode; read; halt if unreadable
4. Declare file type
5. Execute block loop — B1 → B2 → B3 → B4:
   a. Read block definition and proceed rule from `references/determinism-audit.md`
   b. Evaluate all criteria in the block against **current file content**
   c. Reason internally before producing the block report. Include only the structured report in output — do not surface reasoning steps.
   d. Produce block violation report per schema in `references/audit-report-schema.md`
   e. Retain block passed/failed counts in context for Final Summary aggregation.
   f. Apply proceed rule (see Proceed Rule table below)
6. Produce Final Summary after B4

**Proceed rule:**

| Block result | Action |
|:-------------|:-------|
| No violations | State "B[n] — No violations. Proceeding to B[n+1]." Auto-proceed. |
| Minor violations only | List Minors. State "B[n] — No Blocking or Major. Proceeding to B[n+1]." Auto-proceed. |
| Blocking or Major violations present | Enter fix phase (see Fix Phase below). After fix phase: proceed to B[n+1]. |

**Fix phase:**

Triggered when a block report contains one or more Blocking or Major violations.

1. Propose one fix per Blocking or Major violation — keyed by criterion ID
   Quote current text (≤20 words). State exact replacement.
2. Await explicit user approval before writing
3. On approval: apply all approved fixes in a single `filesystem:write_file` call
4. After write: re-read via `filesystem:read_text_file` — confirm write succeeded
   If write fails: halt. Report: "Write confirmation failed — B[n] fix not applied. Resolve before proceeding."
5. If user rejects a specific fix: mark as deferred (note criterion ID). Proceed with remaining approved fixes.
   Retain deferred criterion IDs in context across all blocks for Final Summary aggregation.
6. Proceed to B[n+1] using re-read file content

**Final Summary** (produced after B4, including any B4 fix phase):

```
FINAL AUDIT SUMMARY
File: [filename]
Date: [date]
Mode: Block-by-Block

Blocks completed: B1 Foundation | B2 Evidence Layer | B3 Behavior Contract | B4 Deployment Gate

Total criteria: 33
Passed: [n]
Failed: [n]
Deferred fixes: [n] — [criterion IDs if any]
Risk level: [per audit-report-schema.md thresholds]
```

Workflow complete when Final Summary is produced and confirmed.

---

## Workflow: `audit <file> --full` — Single Pass

**Trigger:** "audit <file> --full" | "full audit <file>" | "one-pass audit"

**Steps:**

1. Run Step 0 — environment detection; criteria loaded from Step 0 read result
2. Read `references/audit-report-schema.md`
   If read fails: halt. Report: "Report schema unavailable — cannot produce structured output. Audit cannot proceed."
3. Resolve file input — detect mode; read; halt if unreadable
4. Declare file type
5. Evaluate all 33 criteria (B1→B4 sequence) against the file in a single pass
   Reason internally before producing the report. Include only the structured report in output — do not surface reasoning steps.
6. Produce complete violation report per schema in `references/audit-report-schema.md`
7. Surface findings only — no fix phase; no file writes

To enter the fix phase after a --full audit: re-run as `audit <file>` (default mode).

---

## Cross-Run Behaviour

Treat each run as independent. Do not accumulate state across runs.
Start each run from current file content. Do not reference prior audit output.
Reason: prior audit state introduces confirmation bias — the second run must evaluate the current file independently to surface genuine improvements or regressions.

---

## Composes With

| Skill | When |
|:------|:-----|
| `writing-docs` | When producing audit reports as standalone `.md` deliverables |

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.5        |
| Last Updated | 2026-04-11 |
| Status       | Draft      |
