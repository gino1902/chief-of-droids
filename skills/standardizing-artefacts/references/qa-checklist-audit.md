<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-04-11 -->

# QA Checklist — standardizing-artefacts (audit workflow)

Governs: `standardizing-artefacts` skill — `audit <file>` (block-by-block) workflow
Format: table (Severity / Maps to / Item / Pass / Fail signal)
Placement: Split — this file covers the `audit` workflow only
Branch-exclusive ratio: 7 of 12 items are branch-specific (58%) — above 50% threshold; split placement correct

| Severity | Maps to | Item | Pass | Fail signal |
|:---------|:--------|:-----|:-----|:------------|
| Blocking | Step 0 — environment detection | Environment detected and reported before any criterion is evaluated | "Environment: Claude Desktop" or "Environment: Claude.ai" line present before B1 begins | Halt; surface environment status before proceeding |
| Blocking | Reference file — criteria | `references/determinism-audit.md` read and criteria content confirmed in context before B1 begins | Criteria content drawn from the file read; block definitions reference named block IDs | Halt: "Audit criteria unavailable — cannot proceed" |
| Blocking | Reference file — schema | `references/audit-report-schema.md` read before first block report is produced | Schema structure confirmed in context; first block report structured per schema | Halt: "Report schema unavailable — cannot produce structured report" |
| Blocking | File input resolution | File content resolved via detected delivery mode before B1 begins; unreadable file halts | Delivery mode stated; file content present in context | Halt: "File unreadable — [mode] [path]. Audit cannot proceed." Do not infer content. |
| Major | File type declaration | File type declared before B1 audit begins | One of: Project Instructions / CLAUDE.md / Routing template / System prompt fragment / unrecognized prepend | Note omission; apply "unrecognized — audited as Project Instructions" path |
| Blocking | Block execution order | Blocks execute B1 → B2 → B3 → B4; each block's criteria drawn from its defined sections | Criterion IDs in each block report carry prefixes matching the block (OBL/STR → B1; EX/RSN → B2; BRN/OUT → B3; DEF/DSK → B4) | Flag cross-block attribution; do not proceed until correct block is running |
| Blocking | Proceed rule — Blocking/Major gate | Any Blocking or Major violation in a block enters the fix phase before proceeding | Fix proposals presented; user approval requested before next block begins | Do not advance to next block without fix phase completion |
| Major | Proceed rule — Minor auto-proceed | Minor-only blocks auto-proceed without entering fix phase | Next block begins without requesting approval; Minors listed in block report | Flag if fix phase is triggered for a Minor-only result |
| Blocking | Fix approval gate | No `filesystem:write_file` call made without explicit user approval per block | User types approval before write executes | Halt fix application: "Fix phase requires explicit approval — no write performed" |
| Major | Write confirmation | File re-read via `filesystem:read_text_file` after every write; write failure halts workflow | Re-read succeeds; content reflects applied edits before next block proceeds | Halt: "Write confirmation failed — B[n] fix not applied. Resolve before proceeding." |
| Blocking | Completion condition | Final Summary produced after B4 (including any B4 fix phase) before workflow exits | Final Summary block present with all required fields: passed/failed counts, deferred fixes, risk level | Surface: "Final Summary not produced — workflow incomplete" |
| Major | Deferred fix tracking | Rejected fixes recorded by criterion ID in Final Summary | Deferred fix count and criterion IDs present in Final Summary when any fix was rejected | Note omission of deferred fix IDs in Final Summary |
