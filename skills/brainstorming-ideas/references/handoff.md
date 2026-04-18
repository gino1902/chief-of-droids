<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-04-18 -->

# Handoff

This content is loaded when Phase 4 begins — after the requirements document is written.

---

<options>

#### 4.1 Present Next-Step Options

Present the numbered options in chat and wait for the user's reply before proceeding.
Reason internally when evaluating which options to present. Do not surface option-selection reasoning in output.

If `Resolve Before Planning` contains any items:
- Ask the blocking questions now, one at a time, by default
- If the user explicitly wants to proceed anyway, convert each remaining item into an explicit decision, assumption, or `Deferred to Planning` question
- If the user chooses to pause instead, present the handoff as paused or blocked
- Do not offer **Proceed to planning** or **Proceed directly to work** while `Resolve Before Planning` remains non-empty

If no options qualify (all gates are blocked), present only **Continue the brainstorm** and **Save and stop**.

**Question when no blocking questions remain:** "Brainstorm complete. What would you like to do next?"

**Question when blocking questions remain and user wants to pause:** "Brainstorm paused. Planning is blocked until the remaining questions are resolved. What would you like to do next?"

Present only the options that apply. Limit to 4 options maximum:

- **Proceed to planning (Recommended)** — Outline a structured implementation plan in the current session. Shown only when `Resolve Before Planning` is empty.
- **Proceed directly to work** — Start implementation now; suited to lightweight, well-defined changes where scope and success criteria are fully resolved. Shown only when `Resolve Before Planning` is empty **and** scope is lightweight, success criteria are clear, scope boundaries are clear, and no meaningful technical or research questions remain.
  Reason: skipping planning is safe only when scope and success criteria are fully resolved — unresolved scope makes direct-to-work a risk.
- **Continue the brainstorm** — Answer more clarifying questions to tighten scope, edge cases, and preferences. Always shown.
- **Save and stop** — Write the requirements document to `docs/brainstorms/` (if Filesystem MCP available) or display in chat for manual saving, then end the session. Always shown.

</options>

<dispatch>

#### 4.2 Handle the Selected Option

**If user selects "Proceed to planning (Recommended)":**

Produce a structured implementation plan in the current session. Reference the requirements document path when one exists; otherwise use the finalized brainstorm decisions as context. Do not print the closing summary first.
Reason: printing the summary before executing the next phase breaks workflow continuity and signals completion when work is still in progress.

Example output opening:
```
Planning: CSV Export for Report View

Phase breakdown:
1. Add Export CSV button to Report View toolbar (frontend)
2. Wire button to filtered dataset serializer (backend)
3. Set filename to report-YYYY-MM-DD.csv at download time
...
```

**If user selects "Proceed directly to work":**

Begin implementation in the current session using the finalized brainstorm output as context. If a compact requirements document exists, reference its path. Do not print the closing summary first.
Reason: printing the summary before executing the next phase breaks workflow continuity and signals completion when work is still in progress.

**If user selects "Continue the brainstorm":**

Return to Phase 1.3 (Collaborative Dialogue) and continue asking clarifying questions one at a time. Continue until the user is satisfied, then return to Phase 4. Do not show the closing summary yet.

Example:
```
Let's keep going. One question: have you defined what "active filters" means for the export — does it include search terms, column filters, or both?
```

**If user selects "Save and stop":**

If Filesystem MCP is connected, write the requirements document to `docs/brainstorms/YYYY-MM-DD-<topic>-requirements.md`. If the write fails, surface the error and display the full requirements document in chat as fallback. If Filesystem MCP is unavailable, display the full requirements document in chat so the user can copy it. Then display the closing summary (see 4.3) and end the turn.

**If the user's selection does not match any option:**

Ask: "Which option did you mean?" and re-present the list.

</dispatch>

<closing-summary>

#### 4.3 Closing Summary

Use the closing summary only when this run of the workflow is ending, not when returning to the Phase 4 options.

When complete and ready for planning, display:

```text
Brainstorm complete!

Requirements doc: docs/brainstorms/YYYY-MM-DD-<topic>-requirements.md  # if one was created

Key decisions:
- [Decision 1]
- [Decision 2]

Recommended next step: outline a planning breakdown in this session, or start a new session with the requirements doc as context.
```

If the user pauses with `Resolve Before Planning` still populated, display:

```text
Brainstorm paused.

Requirements doc: docs/brainstorms/YYYY-MM-DD-<topic>-requirements.md  # if one was created

Planning is blocked by:
- [Blocking question 1]
- [Blocking question 2]

Resume this brainstorm when ready to resolve these before planning.
```

</closing-summary>

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-04-18 |
| Status       | Draft      |
