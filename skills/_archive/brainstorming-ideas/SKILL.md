---
name: brainstorming-ideas
description: "Use this skill when the user wants to explore a feature idea, frame a problem, or think through options before deciding what to build. Triggers on: 'let's brainstorm', 'help me think through X', 'what should we build', 'I'm not sure what to build', vague or ambitious feature requests, problems with multiple valid solutions, and any prompt where requirements seem unclear or the user is thinking out loud. Trigger proactively whenever a decision is being explored or scope is ambiguous — even if the user does not explicitly say 'brainstorm'."
---
<!-- version: 1.4 | author: chief-of-droids workspace | last_updated: 2026-06-03 -->
<!-- source: EveryInc/compound-engineering-plugin (MIT License, Copyright (c) 2025 Every) -->

# Brainstorm a Feature or Improvement

Date requirements documents as YYYY-MM-DD.

Brainstorming answers **WHAT** to build. Planning answers **HOW**.

The durable output is a **requirements document** — strong enough that planning does not need to invent product behavior, scope boundaries, or success criteria.

This skill does not implement code.

**All file references in generated documents must use repo-relative paths, never absolute paths.**

---

## Reference Files

- `references/universal-brainstorming.md` — load at Phase 0.1b when non-software brainstorm detected
- `references/requirements-capture.md` — load at Phase 3 before writing any requirements document
- `references/handoff.md` — load at Phase 4 before presenting next-step options
- `references/qa-checklist.md` — QA checklist for this skill

If any reference file cannot be read, halt and surface: "[filename] unavailable — [phase] cannot proceed."

---

## Trigger Examples

Should trigger:
- "Let's brainstorm a notification redesign"
- "I'm not sure what to build for the reporting dashboard — help me think it through"
- "What should we do about the onboarding flow?"
- "Help me figure out what the search feature should do"
- "I have an idea for a CSV export"

Should not trigger:
- "Implement the CSV export button" (implementation request — no brainstorm needed)
- "What does the `users` table schema look like?" (factual lookup)
- "Define the acceptance criteria for the login bug fix" (scoped work, not open-ended exploration)

---

## Gotchas

- `docs/brainstorms/` must exist before writing a requirements document — create it via Filesystem MCP if absent
- Phase 0.1 resume logic matches `*-requirements.md` glob — only files following that naming convention are detected
- "Brief alignment" does not produce a file — if the user needs a record, they must say so explicitly
- Phase 1.1 reads `CLAUDE.md` / `AGENTS.md` if present — these files may not exist; treat absence as no constraints, not a failure
- Phase 3 pre-write editor is conditional: render only if a file write is planned. If Phase 3 skips the file, no editor artifact.

---

## Execution Flow

Reason internally before each phase output. Do not surface reasoning steps in responses.

### Phase 0 — Resume, Assess, and Route

**Step 0.0** — If no feature description is provided, ask: "What would you like to explore?" Do not proceed without one.

**Step 0.1 — Resume existing work**
If Filesystem MCP is unavailable, surface: "Filesystem MCP unavailable — context scan, resume check, and requirements document write will not be possible. Brainstorm can continue in chat only." Then proceed without filesystem operations.

Check for a matching `*-requirements.md` in `docs/brainstorms/` using `filesystem:list_directory`. If the directory does not exist, treat as no prior work — not an error.
- If found: read the file. Ask: "Found an existing requirements doc for [topic]. Continue from this, or start fresh?"
- If file cannot be read: surface the error. Ask the user whether to start fresh.
- If resuming: summarise current state, continue from existing decisions, update the existing document in Phase 3.

**Step 0.1b — Classify task domain**

- **Software** — task references code, repos, APIs, databases, or asks to build/modify/debug/deploy software → continue to Step 0.2
- **Non-software brainstorming** — no software signals AND user wants to explore/decide in a non-software domain → read `references/universal-brainstorming.md`; do not follow Steps 0.2–4
- **Neither** — quick-help request, factual question, or single-step task → respond directly; do not enter brainstorm workflow

If classification is ambiguous between Software and Non-software, default to Software.

**Step 0.2 — Assess whether brainstorming is needed**
If requirements are already clear (specific acceptance criteria, referenced patterns, exact expected behavior, constrained scope): confirm understanding, present next-step options, skip to Step 1.3 or Phase 3.

**Step 0.3 — Assess scope**
Classify using the feature description plus a light repo scan:
- **Lightweight** — small, well-bounded, low ambiguity
- **Standard** — normal feature or bounded refactor with decisions to make
- **Deep** — cross-cutting, strategic, or highly ambiguous

Reason: scope classification governs ceremony — over-engineering a lightweight brainstorm produces friction without value.

If scope is unclear after one targeted question, default to Standard.

**Phase 0 output carried to Phase 1:** scope classification (Lightweight / Standard / Deep), resume flag (yes/no), domain classification (Software / Non-software).

---

### Phase 1 — Understand the Idea

**Step 1.1 — Existing context scan**

Match depth to scope:

*Lightweight* — search for the topic, check for duplicates, move on.

*Standard and Deep* — two passes:
- Constraint check: read `CLAUDE.md` / `AGENTS.md` if present. Absent file = no constraints, not an error.
- Topic scan: search relevant terms; read the most relevant existing artifact; skim adjacent examples.

Rules:
1. Verify before claiming — read source files before asserting anything is absent. Label unverified claims explicitly.
   Reason: fabricated absence claims persist into planning as false constraints and are harder to correct than verified ones.
2. Defer design decisions to planning — implementation details belong in planning unless this brainstorm is about a technical/architectural decision.

If the scan yields nothing, surface: "No existing context found — proceeding without constraints."
If the filesystem tool returns an error (not just an absent file), surface: "Context scan failed — [error]. Proceeding without codebase constraints."

**Step 1.2 — Product pressure test**

*Lightweight:*
- Is this solving the real user problem?
- Are we duplicating something that already covers this?
- Is there a clearly better framing with near-zero extra cost?

*Standard:*
- Is this the right problem, or a proxy for a more important one?
- What user or business outcome actually matters?
- What happens if we do nothing?
- What is the single highest-leverage move right now?

*Deep* — Standard plus:
- What durable capability should this create in 6–12 months?
- Does this move toward that, or is it only a local patch?

**Step 1.3 — Collaborative dialogue**

Ask one question at a time. Present options in chat; wait for reply before proceeding.
Reason: batched questions shift cognitive load to the user and reduce the quality of answers.

Use single-select for direction, priority, or next step. Use multi-select only for compatible sets (goals, constraints, non-goals, success criteria).
Reason: multi-select collapses priority signals — when everything is selected, nothing is prioritised.

- Ask what the user is already thinking before offering your own ideas.
- Start broad (problem, users, value), then narrow (constraints, exclusions, edge cases).
- Make requirements concrete enough that planning won't need to invent behavior.
- Bring ideas, alternatives, and challenges — don't just interview.

**Exit condition:** idea is clear OR user explicitly wants to proceed.

**Phase 1 output carried to Phase 2:** problem frame, key constraints, open decisions, scope confirmed or revised.

---

### Phase 2 — Explore Approaches

**Step 2.1** — If multiple plausible directions remain, propose 2–3 concrete approaches. Otherwise state the recommended direction directly.

Use at least one non-obvious angle: inversion, constraint removal, or analogy from another domain.

**Present approaches first, then evaluate.** Leading with a recommendation before the user sees the options anchors the conversation prematurely.

Include one higher-upside alternative when it would meaningfully increase value without disproportionate carrying cost.
Reason: a higher-upside challenger prevents anchoring on the first viable option by forcing explicit comparison.

For each approach:
- Brief description (2–3 sentences)
- Pros and cons
- Key risks or unknowns
- When it's best suited

**Step 2.2** — After presenting all approaches, state your recommendation and explain why.

If the user rejects all approaches: ask what is wrong with each before proposing more. Do not generate a second round until the rejection reason is understood.

If one approach is clearly best, skip the menu and state it directly.

**Phase 2 output carried to Phase 3:** chosen approach, key decisions made, open questions identified.

---

### Phase 3 — Capture the Requirements

**Step 3.1** — Read `references/requirements-capture.md`. Apply the template, formatting rules, and completeness checks from that file.

**Step 3.2 — Decide whether to write.**
- If the conversation produced no durable decisions: skip document creation; summarise shared understanding in chat instead. Phase 3 ends. Do not render the editor.
- If the user declines a document: capture key decisions as inline chat summary. Phase 3 ends. Do not render the editor.
- Otherwise: proceed to Step 3.3 (pre-write editor).

**Step 3.3 — Pre-write editor (mandatory when a write is planned).**

Render an inline `visualize:show_widget` editor artifact containing the drafted requirements document. This replaces the old "display draft + confirm to write" inline chat pattern. The editor is the confirmation gate.

Editor contract:
- Textarea seeded with the full drafted markdown
- Read-only target path header showing the exact filesystem destination
- Buttons: `Reset to draft`, `Copy`, `Send back to Claude ↗`
- Live character + byte counter
- Warn banner when content ≥ 10,240 bytes (10 KB)
- Hard-block the send button when content ≥ 40,960 bytes (40 KB) — surface "Too large to send; reduce content"
- Use `visualize:show_widget` with host CSS variables (`var(--color-*)`) only — no Elevate branding, no hardcoded palette
- The send payload must wrap the edited markdown between sentinels: `<<<EDITED_DOC_START>>>` on the line before the content, `<<<EDITED_DOC_END>>>` on the line after. No fenced code block wrapper. No other wrapper text.

Example send payload:
```
Here is the edited requirements document. Write it to the target path.

<<<EDITED_DOC_START>>>
---
date: YYYY-MM-DD
topic: example
---
(...document body...)
<<<EDITED_DOC_END>>>
```

**Step 3.4 — Receive and parse.**

When the user's next message arrives after the editor is rendered:
- Parse strictly between `<<<EDITED_DOC_START>>>` and `<<<EDITED_DOC_END>>>`
- Exactly one pair must be present; both sentinels on their own lines
- If sentinels are missing, duplicated, nested, or malformed: halt. Surface: "Editor payload malformed — expected exactly one `<<<EDITED_DOC_START>>>` … `<<<EDITED_DOC_END>>>` pair. Resend via editor or paste content directly."
- On malformed payload, do not write. Re-render the editor seeded with the current draft.

**Step 3.5 — Write.**
- If updating (resume flag = yes): update the existing file; do not create a duplicate.
- If creating: write to `docs/brainstorms/YYYY-MM-DD-<topic>-requirements.md`. Create `docs/brainstorms/` via Filesystem MCP if it does not exist.
- If the write fails: surface the error and display the parsed content in chat as fallback. Do not silently discard it.

**Phase 3 output carried to Phase 4:** requirements document path (if written), or inline summary (if no document).

---

### Phase 4 — Handoff

**Step 4.1** — Read `references/handoff.md`. Present next-step options and execute the user's selection.

**Workflow complete** when the closing summary has been displayed (Done / Save and stop) or the user has begun a subsequent phase (planning or direct work) in the current session.

---

## Composes With

| Skill | When |
|:------|:-----|
| `editing-docs` | When the requirements document warrants structured doc formatting or a standalone deliverable |

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.4        |
| Last Updated | 2026-06-03 |
| Status       | Draft      |
