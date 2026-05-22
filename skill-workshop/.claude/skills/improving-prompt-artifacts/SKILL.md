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
  Target environments supported: claude-code, claude-desktop, both. Use when
  the user says "audit this prompt", "review this artifact for prompting
  quality", "check this SKILL.md", "improve this CLAUDE.md", "fix this artifact
  using <audit-report>", or pastes prompting content and asks whether it
  follows best practices.
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

## Report destination

Every audit workflow writes its report to disk. Resolve the destination at audit start.

| Artifact source | Destination directory | Report stem |
|:----------------|:----------------------|:------------|
| On-disk, filename is `SKILL.md` or `CLAUDE.md` | parent directory of the artifact | parent directory name |
| On-disk, any other filename | parent directory of the artifact | artifact filename without extension |
| Inline (no on-disk path) | requires explicit `--out <dir>` argument | requires explicit `--stem <name>` argument |

Filename: `<report-stem>-audit-<YYYYMMDD-HHMM>.md` using local time at write.

If the source is inline and `--out` is absent: halt. Report: "Report destination unresolved — inline artifact requires --out <dir> and --stem <name>."

If the destination directory is not writable: halt. Report: "Report destination not writable — [path]. Audit cannot proceed."

The report file must end with the version block defined in `audit-report-schema.md`.

---

## Workflow: `audit <artifact>`

**Trigger:** "audit X", "review X for prompting quality", "check X against best practices", "audit this artifact", or user pastes prompting content and asks whether it follows best practices.

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
7. Resolve the destination per `Report destination`.
8. Write the report to `<destination-dir>/<report-stem>-audit-<YYYYMMDD-HHMM>.md` using `Write`. Leave the audited artifact unchanged. Do not propose fixes inline.
9. Emit exactly one line of chat output: the absolute report path. No summary, no headline counts, no risk-level mention, no commentary, no follow-up question. The run ends on that line.
   Correct:   `/Users/foo/.claude/skills/bar/bar-audit-20260518-0713.md`
   Incorrect: `Report written: ...path... Headline: 28/41 passed, Risk High.`
   Incorrect: `...path... — want me to run the fix workflow?`
   Reason: the report file is the canonical artifact; chat restatement duplicates content, drifts wording, and invites interactive follow-up the audit workflow does not own. The fix workflow is invoked separately by the user when ready.

---

## Workflow: `fix <artifact> --report <path>` — interactive fix application

**Trigger:** `fix <artifact> --report <report>`, "apply audit fixes to X using Y", "fix X based on the audit report".

**Steps:** See `references/fix-workflow.md`. Read that file at workflow start.

Summary of behavior: filters to Blocking and Major violations from the supplied report; for each violation, displays the verbatim block from the report, then surfaces every iteration of the proposed replacement (iter-1, iter-2, iter-3, and any further iterations triggered by a Drifting verdict) with self-challenge notes on each against fix-intent and predictability-intent (see `## Predictability intent` in `references/fix-workflow.md`); after the iterations, surfaces a trajectory verdict (Stable / Drifting / Divergent) and then prompts the user — `Proceed (y/n)?` on Stable, run more iterations on Drifting (cap iter-5), `Proceed with no-change (y/n)?` on Divergent. Approved fixes are applied via `Edit` (or `Write` for structural rewrites). On completion, the revision metadata block (VER-2) is appended at the bottom of the artifact.

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
| Version      | 1.5        |
| Last Updated | 2026-05-18 |
| Status       | Draft      |
