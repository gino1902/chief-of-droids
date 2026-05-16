<!-- version: 1.1 | author: chief-of-droids workspace | last_updated: 2026-04-11 -->

# QA Checklist — standardizing-artefacts (audit --full workflow)

Governs: `standardizing-artefacts` skill — `audit <file> --full` (single-pass) workflow
Format: table (Severity / Maps to / Item / Pass / Fail signal)
Placement: Split — this file covers the `audit --full` workflow only
Branch-exclusive ratio: all 7 items are exclusive to the `audit --full` workflow — split placement correct

| Severity | Maps to | Item | Pass | Fail signal |
|:---------|:--------|:-----|:-----|:------------|
| Blocking | Step 0 — environment detection | Environment detected and reported before any criterion is evaluated | "Environment: Claude Desktop" or "Environment: Claude.ai" line present before evaluation begins | Halt; surface environment status |
| Blocking | Reference file — criteria | `references/determinism-audit.md` read and all 33 criteria confirmed in context | Criteria content present; all 33 criterion IDs covered in evaluation | Halt: "Audit criteria unavailable — cannot proceed" |
| Blocking | Reference file — schema | `references/audit-report-schema.md` read before the report is produced | Schema structure present in context before output begins | Halt: "Report schema unavailable — cannot produce structured report" |
| Blocking | File input resolution | File content resolved before evaluation begins; unreadable file halts | Delivery mode stated; file content present | Halt: "File unreadable — [mode] [path]. Audit cannot proceed." |
| Major | File type declaration | File type declared before evaluation begins | One of supported types or "unrecognized" prepend | Apply "unrecognized" path if absent |
| Major | No fix phase | --full mode produces no `filesystem:write_file` calls | No write operations initiated during --full run | Flag write attempt: "--full mode does not own the fix phase. Re-run as `audit <file>` to enter fix phase." |
| Blocking | Completion condition | Complete 33-criterion report produced and structured per schema | Report covers all 33 criteria; Summary block present with passed/failed counts and risk level | Surface: "Full audit report incomplete — workflow incomplete" |
