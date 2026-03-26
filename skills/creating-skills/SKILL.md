---
name: creating-skills
description: >
  Authors new SKILL.md files from scratch, critiques and improves existing
  SKILL.md files, and assesses skills against Anthropic official best practices.
  Use when asked to create, build, author, or define a new skill, improve or
  critique an existing skill, or audit skills in the workspace.
  Triggers on: "author skill", "critique skill", "assess all skills",
  "create a skill", "build a skill", "I need a skill", "new skill for".
---
<!-- version: 1.9 | author: chief-of-droids workspace | last_updated: 2026-03-26 -->

# Creating Skills Skill

Authors, critiques, and assesses SKILL.md files against Anthropic official standards.

**Principle:** Never author or assess from memory. Always fetch official sources
first. Assessment checklist lives in `references/assessment-checklist.md` —
read it via filesystem tool before any critique or assessment run.

---

## Step 0 — Environment Detection (always first)

Before any other action, determine which environment Claude is running in.

**Detection method:** Attempt to read any known file via Filesystem MCP tool.
- If the read succeeds → **Claude Desktop** — Filesystem MCP is active
- If the read fails or the tool is unavailable → **Claude.ai** — Filesystem MCP is absent

**Report the result explicitly at the start of every workflow run:**
- ✅ `Environment: Claude Desktop — official source fetch will be attempted`
- ⚠️ `Environment: Claude.ai — Filesystem MCP unavailable; official source fetch blocked by platform restriction`

Never skip this step. Never assume the environment from context or memory.

---

## Step 1 — Official Source Fetch (mandatory, every invocation)

Attempt all three fetches after environment detection. Do not skip even if the
environment is known from a prior run in the same session.

1. `https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices`
2. `https://github.com/anthropics/skills/`
3. `https://agentskills.io/specification`

**Fetch outcomes:**

| Environment | Expected result | Action |
| :--- | :--- | :--- |
| Claude Desktop | All succeed | Proceed normally |
| Claude Desktop — one fails | Partial | Flag, proceed with remaining + local checklist |
| Claude Desktop — all fail | Full failure | Flag all, proceed with local checklist only |
| Claude.ai | All blocked | Surface platform restriction, proceed with local checklist only |

**Always surface fetch status before producing any output:**
- ✅ `Official sources fetched — assessment fully verified against live docs`
- ⚠️ `One or more sources failed — assessment partially verified; gaps noted`
- ⚠️ `All sources failed — assessment run against local checklist only`

A failed fetch is acceptable. A skipped fetch is not.
Never proceed from memory alone if both fetch and local checklist are unavailable.

---

## Workflow: author skill

Trigger: `author skill <n>` | "create a skill" | "build a skill for" | "I need a skill that" | "new skill for"

Steps:
1. Run Step 0 — Environment Detection
2. Run Step 1 — Official Source Fetch
3. Use filesystem tool to read `references/assessment-checklist.md`
4. Ask user: what does this skill do, when should it trigger, what are its
   inputs and outputs — one question, not a form
5. Draft SKILL.md using the canonical structure:
   - YAML frontmatter: `name` (lowercase, hyphens, max 64 chars), `description`
     (third person, trigger-inclusive, max 1024 chars, "pushy")
   - Body: principle statement, reference file declarations, workflows
   Apply rules from fetched official sources and checklist — not from memory
6. Run assessment-checklist against the draft before proposing it
7. Surface checklist gaps as open questions
8. Propose test prompts (2-3 realistic triggers) for manual validation
9. Await user approval before writing any file

Output: `skills/<n>/SKILL.md` written to filesystem (on approval only)

---

## Workflow: critique skill

Trigger: `critique skill <n>`

Steps:
1. Run Step 0 — Environment Detection
2. Run Step 1 — Official Source Fetch
3. Use filesystem tool to read `references/assessment-checklist.md`
4. Read `skills/<n>/SKILL.md` and any files in `skills/<n>/references/`
5. Run assessment-checklist — section by section, cross-referenced against fetched official docs
6. Output structured critique: issue | severity | recommendation
7. Surface findings only — do not rewrite unless user requests (see step 8)
8. If user requests fixes: propose edits, await approval, then write

Output: structured critique in chat (no file write unless requested)

---

## Workflow: assess all skills

Trigger: `assess all skills`

Steps:
1. Run Step 0 — Environment Detection
2. Run Step 1 — Official Source Fetch
3. Use filesystem tool to read `references/assessment-checklist.md`
4. Use filesystem tool to list the `skills/` directory — do not enumerate from memory
5. For each skill: read SKILL.md, run checklist cross-referenced against fetched official docs
6. Output gap table: skill | issue | severity | recommendation
7. Overall summary: Pass / Partial / Fail per skill
8. Do not rewrite any skill — surface findings only
9. If user requests fixes on a specific skill: delegate to `critique skill <n>`

Output: gap table in chat (no file write)

---

## Composes With

| Skill | When |
| :--- | :--- |
| `writing-docs` | When authoring reference files or structured documentation alongside a new skill |

---

## QA Checklist

- [ ] Environment detected and reported before any other action
- [ ] All three official source fetches attempted — status reported explicitly
- [ ] assessment-checklist.md read via filesystem tool — not from memory
- [ ] Findings cross-referenced against fetched official docs, not checklist alone
- [ ] Description field third person, trigger-inclusive, max 1024 chars
- [ ] SKILL.md lean — no content that belongs in reference files
- [ ] Test prompts proposed for new skills before writing
- [ ] No file written without user approval
