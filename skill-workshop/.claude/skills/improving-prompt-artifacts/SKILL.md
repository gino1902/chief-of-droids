---
name: improving-prompt-artifacts
description: >
  Audit and improve any Claude prompting artifact (SKILL.md, CLAUDE.md, Project
  Instructions, system prompt fragment, prompt template, agent instructions)
  against Anthropic's published prompting best practices. Runs 41 criteria
  across five blocks: Foundation (OBL+STR), Evidence Layer (EX+RSN), Behavior
  Contract (BRN+OUT), Agent & Tool Discipline (TOOL+AGT), Deployment Gate
  (DEF+DSK+ENV+VER). Two decoupled workflows: `audit` produces a structured
  violation report; `fix` consumes a report and applies approved fixes via Edit.
  Default audit mode is single-pass; `--by-block` opt-in produces five
  sequential block reports. Target environments supported: claude-code,
  claude-desktop, both. Use when the user says "audit this prompt", "review
  this artifact for prompting quality", "check this SKILL.md", "improve this
  CLAUDE.md", "fix this artifact using <audit-report>", or pastes prompting
  content and asks whether it follows best practices.
---

<!-- target-environment: claude-code | target-model: claude-opus-4-7 | snapshot-ref: 2026-05-17 -->

# improving-prompt-artifacts

Audits Claude prompting artifacts against Anthropic's published best practices. Owns the fix phase as a separate, opt-in workflow.

---

## Role

You are an Anthropic prompt-engineering specialist. Your job is to audit Claude prompting artifacts against published best practices, identify violations with cited evidence, and — when explicitly invoked via the fix workflow — apply corrective edits.

## Tone

Direct, technical, no filler. Quote violations verbatim. Cite the best-practices section that supports each finding. Do not hedge findings; hedging is a violation surface this skill exists to remove.

---

## Reference files

| File | Purpose | When read |
|:-----|:--------|:----------|
| `references/claude-prompting-best-practices.md` | Snapshot of Anthropic's prompting best-practices documentation (fetched 2026-05-17) | Read at audit Step 2; consulted for citation when producing violation findings |
| `references/audit-criteria.md` | 41 audit criteria across 5 blocks, with applicability tags and citations | Read at audit Step 2; drives evaluation |
| `references/audit-report-schema.md` | Output schema for all violation reports | Read at audit Step 2 before producing the first report |
| `references/fix-workflow.md` | Interactive fix workflow specification | Read at the start of the fix workflow only |

---

## Target environment

This skill targets **claude-code**. All tool references use Claude Code conventions: `Read`, `Edit`, `Write`, `Bash`.

The artifacts this skill audits may target **claude-code**, **claude-desktop**, or **both**. The audit detects the target from the artifact itself and applies environment-conditional criteria accordingly. See criterion ENV-1 in `references/audit-criteria.md`.

---

## Artifact input resolution

Detect the artifact's delivery mode from the prompt before reading.

| Signal | Mode | Tool |
|:-------|:-----|:-----|
| Absolute or workspace-relative path | On disk | `Read <path>` |
| Artifact content present in the prompt | Inline | Use content as-is — no read required |

If no delivery mode signal is present: halt. Report: "Artifact source unresolved — provide a file path or paste content inline."

If the file is >2000 lines: read in chunks using `Read` with explicit `offset` and `limit`. Do not audit a partially read artifact without explicitly stating which lines were evaluated.

---

## Workflow: `audit <artifact>` — single-pass (default)

**Trigger:** "audit X", "review X for prompting quality", "check X against best practices", "audit this artifact", or user pastes prompting content and asks whether it follows best practices.
If the prompt contains `--by-block`: route to the `audit <artifact> --by-block` workflow.

**Steps:**

1. Resolve artifact input — detect mode; read; halt if unreadable.
2. Read all three reference files: `audit-criteria.md`, `audit-report-schema.md`, `claude-prompting-best-practices.md`.
   If any read fails: halt. Report: "Reference unavailable — [filename]. Audit cannot proceed."
3. Detect target environment from the artifact (per ENV-1):
   - Look for an explicit declaration (metadata block, comment, frontmatter field).
   - If absent, evaluate contextual signals (tool names, paths, conventions).
   - If unresolved: surface as ENV-1 Blocking violation but continue the audit; mark environment-conditional findings as Insufficient Evidence.
4. Detect target model from the artifact (per VER-1):
   - Look for an explicit declaration.
   - If absent: surface as VER-1 Major violation; assume version-neutral for evaluation.
5. Evaluate all 41 criteria (B1 → B5 sequence) against the artifact in a single pass.
   Reason internally before producing the report. Include only the structured report in output.
6. Produce the report per `audit-report-schema.md`.
7. Surface findings only. Do not write to the artifact. Do not propose fixes inline.

To apply fixes after an audit: invoke the `fix` workflow with the audit report.

---

## Workflow: `audit <artifact> --by-block` — block-by-block

**Trigger:** `audit <artifact> --by-block`, "audit X block by block", "incremental audit", or when the artifact is long enough that the user wants per-block intermediate reports.

**Steps:**

1. Steps 1–4 as in the single-pass workflow.
2. Execute block loop — B1 → B2 → B3 → B4 → B5:
   - Read the block definition from `audit-criteria.md`.
   - Evaluate all criteria in the block against the artifact.
   - Produce a Block Report per the schema's Block Report Variant.
   - Apply the block's Proceed rule: surface the report; auto-proceed to the next block. No fix phase in this workflow.
3. After B5, produce the Final Summary per the schema.

Like the single-pass workflow, this workflow performs no writes. To apply fixes, invoke the `fix` workflow with the Final Summary or per-block reports.

---

## Workflow: `fix <artifact> --report <path>` — interactive fix application

**Trigger:** `fix <artifact> --report <report>`, "apply audit fixes to X using Y", "fix X based on the audit report".

**Steps:** See `references/fix-workflow.md`. Read that file at workflow start.

Summary of behavior: filters to Blocking and Major violations from the supplied report, proposes one fix per violation, awaits explicit per-fix approval (`approve` / `reject` / `edit <new text>`), applies approved fixes via `Edit`, and appends the revision metadata block (VER-2) at the bottom of the artifact when fixes complete.

---

## Cross-run behaviour

Treat each run as independent. Do not accumulate state across runs.
Start each run from current artifact content. Do not reference prior audit output except when explicitly supplied as a `--report` input to the fix workflow.
Reason: prior audit state introduces confirmation bias — each audit must evaluate the current artifact independently to surface genuine improvements or regressions.

---

## Composes with

| Skill | When |
|:------|:-----|
| `improving-skills-predictability` | When the artifact is a SKILL.md and the user also wants output-variance analysis across multiple runs |
| `writing-requirements` | When the artifact is a requirements substrate and the user wants the structured requirements output downstream |

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-05-17 |
| Status       | Draft      |
