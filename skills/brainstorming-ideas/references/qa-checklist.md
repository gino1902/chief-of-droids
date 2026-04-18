<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-04-18 -->

# QA Checklist — brainstorming-ideas

Governs: `brainstorming-ideas` skill
Format: table (Severity / Maps to / Item / Pass / Fail signal)
Placement: Unified
Branch-exclusive ratio: 5 of 18 items are branch-specific (28%) — below 50% threshold; unified placement correct

| Severity | Maps to | Item | Pass | Fail signal |
|:---------|:--------|:-----|:-----|:------------|
| Blocking | Step 0.0 — feature description gate | Skill does not proceed without a feature description | Either a feature description is present in the prompt, or Claude asks "What would you like to explore?" before any phase begins | Halt; surface: "No feature description provided — cannot begin brainstorm" |
| Blocking | Step 0.1b — domain classification | Task domain classified before Phase 1 begins | One of Software / Non-software / Neither is stated or implied before Step 0.2 | Halt; surface: "Domain classification required before proceeding" |
| Blocking | Step 0.1b — non-software branch | `references/universal-brainstorming.md` read before non-software facilitation begins | File content confirmed in context; software phases not followed for non-software tasks | Halt; surface: "universal-brainstorming.md unavailable — non-software brainstorm cannot proceed" |
| Blocking | Phase 3 — reference file read | `references/requirements-capture.md` read before any requirements document is written | File content confirmed in context before Step 3.2 executes | Halt; surface: "requirements-capture.md unavailable — Phase 3 cannot proceed" |
| Blocking | Phase 4 — reference file read | `references/handoff.md` read before next-step options are presented | File content confirmed in context before Step 4.1 executes | Halt; surface: "handoff.md unavailable — Phase 4 cannot proceed" |
| Blocking | Phase 3 — write gate | No requirements document written without durable decisions from the brainstorm | Requirements document written only after Phase 1–2 dialogue has produced decisions worth preserving | Do not write; summarise in chat instead |
| Blocking | Workflow completion | Workflow has an explicit completion state | Closing summary displayed (Done / Save and stop) OR user has begun planning or direct work in the session | Halt current phase; re-read Phase 4 handoff to identify which completion condition applies; surface the applicable condition to the user |
| Major | Step 0.1 — resume path | Existing requirements document read before resuming | File content confirmed in context; user asked whether to continue or start fresh | Surface read error; ask user whether to start fresh |
| Major | Step 0.3 — scope classification | Scope classified as Lightweight / Standard / Deep before Phase 1 begins | Scope label present in output or used to govern Phase 1 depth | Default to Standard; flag that scope defaulted |
| Major | Phase 1 — context scan depth | Scan depth matches scope classification | Lightweight: topic search only. Standard/Deep: constraint check + topic scan | Flag mismatch; apply correct depth before proceeding |
| Major | Step 1.3 — one question at a time | Questions asked one at a time in collaborative dialogue | No response contains more than one unrelated question | Revise to single question before sending |
| Major | Phase 1 → Phase 2 handoff | Problem frame, key constraints, and open decisions carried forward | Phase 2 approach proposals reference decisions surfaced in Phase 1 | Surface: "Phase 1 output incomplete — re-run dialogue before proposing approaches" |
| Major | Phase 2 — all-approaches-rejected handler | User rejection of all approaches triggers clarification before new approaches proposed | Claude asks what is wrong with each rejected approach before generating more | Do not generate new approaches until rejection reason is understood |
| Major | Phase 2 → Phase 3 handoff | Chosen approach and key decisions carried to Phase 3 | Requirements document reflects approach chosen in Phase 2 | Surface: "Phase 2 output not captured — confirm chosen approach before writing requirements document" |
| Major | Phase 3 — overwrite vs. create | Resume flag determines whether file is updated or created | Resume flag = yes → existing file updated, not duplicated. Resume flag = no → new file created at canonical path | Surface: "Resume flag ambiguous — confirm whether to update existing document or create new one" |
| Major | Phase 3 — docs/brainstorms/ existence | Directory created before write if absent | Write does not fail due to missing directory | Surface: "docs/brainstorms/ absent — create via Filesystem MCP before writing" |
| Minor | Step 1.1 — absent CLAUDE.md handling | Absent CLAUDE.md / AGENTS.md treated as no constraints, not an error | Workflow continues without surfacing an error when these files are not found | Note absence; proceed without constraints |
| Minor | Context scan null result | Empty context scan result surfaced to user | "No existing context found — proceeding without constraints" present in output when scan yields nothing | Note absence; do not silently assume empty context means no relevant prior work |
