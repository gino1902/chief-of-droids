# Skills Reference

> Lookup reference for Claude skills — spec, install, platform differences, templates, troubleshooting.
> Stable. Consult when you need to verify a spec, find a field definition, or diagnose an install problem.

**Companion doc:** `skills-playbook.md` — commission, build, describe, install, maintain.
Go there when you are executing a task. Come here when you need to look something up.

---

## Contents

1. What skills are
2. SKILL.md spec
3. Install and manage — claude.ai and Claude Desktop
4. Install and manage — Claude Code
5. Platform comparison
6. Templates
7. Packaging checklist
8. Troubleshooting
9. Verified claims log

---

## 1. What Skills Are

Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialised tasks. They teach Claude how to complete specific tasks in a repeatable, consistent way without re-explaining your standards every conversation.

**Progressive disclosure — three loading levels:**

| Level | What loads | When |
| :--- | :--- | :--- |
| Metadata | `name` + `description` (~100 tokens per skill) | Always, every conversation |
| SKILL.md body | Full instructions | When Claude determines the skill is relevant |
| Bundled resources | `references/`, `scripts/`, `assets/` | On demand, as referenced from the body |

This keeps context window pressure low even with many skills installed. Claude scans metadata at query time and semantically matches descriptions to the user's request — it reasons about intent, not keywords. For how to write descriptions that trigger reliably, see `skills-playbook.md` → Section 3.

⚠️ Only install skills from trusted sources. Primary risks: prompt injection and data exfiltration from malicious skill content.

---

## 2. SKILL.md Spec

Every skill requires a `SKILL.md` at the root of the skill folder. The file has two parts: YAML frontmatter and a markdown body.

### Frontmatter fields

```markdown
---
name: your-skill-name
description: >
  What this skill does and when to use it. Include trigger phrases.
  Claude uses this to decide when to invoke the skill automatically.
---
```

| Field | Required | Limit | Notes |
| :--- | :---: | :--- | :--- |
| `name` | ✅ | 64 chars | Lowercase, hyphens only — confirmed for Claude Code; unverified for claude.ai/Desktop |
| `description` | ✅ | 200 chars (claude.ai/Desktop) · 1024 chars (Claude Code) | Use 200 as safe cross-surface limit. Primary trigger mechanism. |
| `disable-model-invocation` | ❌ | — | `true` prevents auto-trigger; skill invoked only via `/skill-name`. Claude Code only. |
| `context` | ❌ | — | `fork` spawns an isolated subagent. Claude Code only. |
| `agent` | ❌ | — | Agent type for forked context (e.g. `Explore`). Claude Code only. |
| `allowed-tools` | ❌ | — | Restricts subagent tool access (e.g. `Bash, Read, Glob`). Claude Code only. |
| `dependencies` | ❌ | — | Software packages required by the skill. |

### Body structure

```markdown
# Skill Name

## Instructions
Step-by-step guidance Claude follows when the skill is active.
Keep SKILL.md body under 500 lines. If approaching that limit, split content
into references/ with explicit pointers from the body.

## Examples
Concrete examples of inputs and expected outputs.
```

### Folder structure

```
your-skill/
├── SKILL.md              ← required
├── references/           ← optional — loaded into context as needed
│   └── checklist.md
├── scripts/              ← optional — execute without entering context
│   └── analyse.py
└── assets/               ← optional — templates, icons, fonts
    └── template.docx
```

For large reference files (>300 lines), include a table of contents inside the file. When a skill supports multiple domains, organise by variant:

```
cloud-deploy/
├── SKILL.md              ← workflow + variant selection logic
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

Claude reads only the relevant reference file per invocation.

---

## 3. Install and Manage — claude.ai and Claude Desktop

Anthropic does not document a separate install flow for Claude Desktop. Both surfaces use **Customize > Skills**.

### Prerequisites

- **Settings > Capabilities** → Code execution and file creation must be enabled
- Team/Enterprise: Owner must also enable Skills in **Organization settings > Skills**

**Plan availability:**

| Skill type | Plans |
| :--- | :--- |
| Anthropic-provided skills (PowerPoint, Excel, Word, PDF) | All plans including free |
| Custom skills (upload your own) | All plans including free ✱ |

> ✱ Custom skills are available on all plans including free. The earlier restriction to Pro+ has been lifted. Verified: support.claude.com/use-skills-in-claude, 2026-03-26.

### Install a custom skill

1. Create your skill folder locally with `SKILL.md` inside
2. ZIP the folder — root of ZIP must be the skill folder, not loose files:

   ```
   your-skill.zip
   └── your-skill/
       └── SKILL.md
   ```

   ⚠️ Loose files at ZIP root will fail on upload.

3. Navigate to **Customize > Skills**
4. Click **"+"** → **"Upload a skill"**
5. Upload the ZIP → toggle on

### Update a skill

Skills cannot be edited in place:

1. Edit `SKILL.md` in your local source folder
2. Re-ZIP the folder
3. **Customize > Skills** → click skill → "..." → Delete
4. Upload new ZIP → toggle on

### Manage skills

| Action | Where |
| :--- | :--- |
| Enable / disable | **Customize > Skills** → toggle |
| Delete | Click skill → "..." → Delete |
| View installed skills | **Customize > Skills** |

**Sharing:** Custom skills are private to your account. For org-wide provisioning (Team/Enterprise), use **Organization settings > Skills** — Owner access required. Skills cannot be shared peer-to-peer.

> ✅ Install path, per-user scope: support.claude.com (2026-03-13)
> ✅ Plan availability updated (all plans incl. free): support.claude.com (2026-03-26)

---

## 4. Install and Manage — Claude Code

Skills are filesystem-based in Claude Code — no UI upload required.

### Skill locations (priority order)

| Scope | Path | Use for |
| :--- | :--- | :--- |
| Personal | `~/.claude/skills/your-skill/` | Individual workflows, all projects |
| Project | `.claude/skills/your-skill/` | Team workflows, committed to git |
| Plugin | Bundled with plugin | Plugin marketplace installs |

When the same skill name exists at multiple levels, priority is: **enterprise > personal > project**.

### Create a personal skill

```bash
mkdir -p ~/.claude/skills/your-skill-name
# create SKILL.md inside
```

### Create a project skill

```bash
mkdir -p .claude/skills/your-skill-name
# create SKILL.md inside
# commit to git — team members get it on pull
```

### Invocation

- **Auto-trigger:** Claude decides based on the `description` field
- **Explicit:** `/your-skill-name` in the prompt
- **Disable auto-trigger:** add `disable-model-invocation: true` to frontmatter

### Monorepo support

Claude Code discovers skills from nested `.claude/skills/` directories. Editing a file in `packages/frontend/` causes Claude Code to also check `packages/frontend/.claude/skills/`.

### Live change detection

Skills in directories added via `--add-dir` are picked up without restarting the session.

---

## 5. Platform Comparison

| | claude.ai | Claude Desktop | Claude Code |
| :--- | :---: | :---: | :---: |
| Install method | ZIP via **Customize > Skills** | ZIP via **Customize > Skills** | Filesystem directory |
| Personal scope | ✅ | ✅ | `~/.claude/skills/` |
| Project/team scope | Via org provisioning | Via org provisioning | `.claude/skills/` + git |
| Auto-invocation | ✅ | ✅ | ✅ |
| Explicit `/skill-name` | ❌ | ❌ | ✅ |
| `disable-model-invocation` | ❌ | ❌ | ✅ |
| `context: fork` (subagent) | ❌ | ❌ | ✅ |
| Code execution required | ✅ | ✅ | ❌ |
| Description limit | 200 chars | 200 chars | 1024 chars |
| Skills sync across surfaces | ❌ | ❌ | ❌ (separate from claude.ai) |

Skills do not sync across surfaces. A skill uploaded to claude.ai is not available in Claude Code, and vice versa.

**Workspace pattern (Claude Desktop + Filesystem MCP):** This workspace does not use ZIP uploads as the primary delivery model. Skills live in the repo at `workspace/skills/` and are loaded via system prompt path declaration + Filesystem MCP reads — no upload cycle, no toggle, git is the version log. The ZIP upload model (Section 3) is the fallback for environments without MCP or for skills with no MCP dependency. See `skills-playbook.md` → Section 6 for setup, tradeoffs, and failure mode.

---

## 6. Templates

Three templates covering the main structural patterns. For description writing and triggering strategy, see `skills-playbook.md` → Section 3.

A note on co-triggering: a prompt can match more than one skill. Claude loads all matching skills and composes their instructions. This is usually harmless when skills have non-overlapping scope. If two skills have overlapping descriptions and their instructions conflict, results are unpredictable. Keep descriptions mutually exclusive when skills are in the same domain.

---

### Template A — Simple (reference content only)

Inline rules and conventions. No scripts or supporting files. Works on all surfaces.

```
output-format/
└── SKILL.md
```

```markdown
---
name: output-format
description: >
  Apply standard output formatting rules. Use when the user says
  'format this', 'apply output rules', 'add a version block', or asks
  to standardise the structure of any document or report.
---

# Output Format

## Rules
- Begin with a one-line summary
- Use Markdown headers for sections
- Use tables for structured comparisons — not bullet lists
- End every document with a version block
- Flag assumptions explicitly with [ASSUMPTION]

## Version Block Template

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.0        |
| Last Updated | YYYY-MM-DD |
| Status       | Draft      |
```

---

### Template B — Medium (instructions + supporting file)

Multi-step instructions that reference a template or supplemental file loaded on demand. Works on all surfaces.

```
doc-formatter/
├── SKILL.md
└── references/
    └── templates.md
```

```markdown
---
name: doc-formatter
description: >
  Format documents to team standards. Use when asked to 'format this
  document', 'write this up as meeting notes', 'make this a decision
  record', 'turn this into a spec', or 'write a project brief'.
  NOT for output formatting rules — use output-format skill instead.
---

# Document Formatter

## Instructions
1. Identify the document type from the user's content
2. Load [references/templates.md](references/templates.md) for the correct structure
3. Rewrite the content using the matching template
4. Apply output-format rules: headers, tables, version block
5. Flag any section where source content was ambiguous or missing

## Supported Types
- Technical specification
- Meeting notes
- Decision record
- Project brief
```

```markdown
<!-- references/templates.md -->

# Document Templates

## Technical Specification
### Context / Problem / Proposed Solution / Constraints / Open Questions

## Meeting Notes
### Date · Attendees / Decisions / Actions (owner, due date) / Parking Lot

## Decision Record
### Decision / Context / Alternatives Considered / Consequences

## Project Brief
### Objective / Scope / Success Criteria / Timeline
```

---

### Template C — Complex (script + forked subagent)

> ⚠️ **Claude Code only.** `context: fork`, `agent`, and `allowed-tools` are not available in claude.ai or Claude Desktop.

Isolated execution with tool restrictions. Script output enters context; script source does not.

```
codebase-report/
├── SKILL.md
├── references/
│   └── thresholds.md
└── scripts/
    └── collect_stats.py
```

```markdown
---
name: codebase-report
description: >
  Analyse the codebase and generate a structured health report covering
  file count, language breakdown, and largest files. Use when asked to
  'analyse the codebase', 'run a codebase report', 'health check', or
  'give me an overview of the repo'.
context: fork
agent: Explore
allowed-tools: Bash, Read, Glob, Grep
---

# Codebase Report

## Instructions
1. Run the stats script: `python scripts/collect_stats.py .`
2. Read [references/thresholds.md](references/thresholds.md) for report structure and thresholds
3. Analyse script output against thresholds
4. Produce a structured report following the format in thresholds.md
5. Flag any files or directories exceeding defined thresholds
6. Return the completed report to the main conversation

## Notes
- Read-only skill — do not modify any files
- If the script fails, report the error and working directory path
```

**Runtime behaviour:** `context: fork` spawns an isolated Explore subagent. `allowed-tools` restricts it to read-only tools. Only script output enters context — not the script source. Results are returned to the main conversation on completion.

---

## 7. Packaging Checklist (claude.ai and Claude Desktop)

Before uploading:

- [ ] Folder name matches the `name` field in SKILL.md frontmatter
- [ ] `SKILL.md` is at the root of the skill folder
- [ ] YAML frontmatter is valid — `name` and `description` present, wrapped in `---`
- [ ] ZIP contains the skill folder as its root — not loose files
- [ ] Description is 200 characters or fewer
- [ ] No hardcoded API keys, passwords, or credentials
- [ ] All referenced scripts and resource files exist inside the folder

---

## 8. Troubleshooting

| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| Skills section not visible | Code execution disabled | **Settings > Capabilities** → enable Code execution |
| Skills greyed out (Team/Enterprise) | Org-level code execution disabled | Contact org Owner |
| Skill not auto-triggered | Description too vague | Rewrite — see `skills-playbook.md` Section 3 |
| Two skills triggering together unexpectedly | Overlapping description scope | Add exclusions to both descriptions |
| YAML parse error on upload | Frontmatter formatting issue | Check `---` delimiters, no tabs, valid indentation |
| Upload fails silently | Loose files at ZIP root | Re-ZIP with skill folder as root |
| Claude Code skill not found | Wrong directory path | Verify path is `~/.claude/skills/` or `.claude/skills/` |
| Subagent not spawning | `context: fork` used outside Claude Code | Remove — this field is Claude Code only |
| MCP connected but tools missing | Silent connection failure (known race condition) | Restart Claude Desktop; check tools icon in chat header |

---

## 9. Verified Claims Log

| Claim | Source | Date | Status |
| :--- | :--- | :--- | :--- |
| Anthropic-provided skills available to all plans incl. free | support.claude.com/use-skills-in-claude | 2026-03-13 | ✅ Confirmed |
| Custom skills available to all plans incl. free | support.claude.com/use-skills-in-claude | 2026-03-26 | ✅ Confirmed — corrected from prior "Pro+ only" claim |
| Install path: ZIP via Customize > Skills | support.claude.com/use-skills-in-claude | 2026-03-13 | ✅ Confirmed |
| Old path "Settings → Extensions → Install Extension" + .skill file | — | 2026-03-13 | ❌ Stale — corrected |
| Custom skills on claude.ai/Desktop are per-user, not org-wide | support.claude.com/use-skills-in-claude | 2026-03-26 | ✅ Confirmed — Team/Enterprise org provisioning via settings exists; individual peer-to-peer sharing not supported |
| Description limit: 200 chars (claude.ai/Desktop) | support.claude.com/how-to-create-custom-skills | 2026-03-13 | ✅ Confirmed |
| Description limit: 1024 chars (Claude Code) | code.claude.com/docs/en/skills | 2026-03-13 | ✅ Confirmed |
| `name` lowercase/hyphens-only scoped to Claude Code only | code.claude.com/docs/en/skills | 2026-03-13 | ✅ Confirmed |
| `context: fork`, `disable-model-invocation`: Claude Code only | code.claude.com/docs/en/skills | 2026-03-13 | ✅ Confirmed |
| ZIP must contain skill folder as root — not loose files | support.claude.com/how-to-create-custom-skills | 2026-03-13 | ✅ Confirmed |
| Code execution required for skills on claude.ai/Desktop | support.claude.com/use-skills-in-claude | 2026-03-13 | ✅ Confirmed |
| Skills do not sync across surfaces | support.claude.com/use-skills-in-claude | 2026-03-13 | ✅ Confirmed |
| MCP failure: silent in-conversation, UI toast not always raised | GitHub issues #31864, #25751 | 2026-03-13 | ✅ Confirmed |
| Claude Code native Windows install — no WSL, no Node.js required | code.claude.com/docs/en/setup | 2026-03-26 | ✅ Confirmed |

---

*See `skills-playbook.md` for: commission, build loop, description discipline, archetypes, install/commit workflow.*

---

| Field | Value |
| :--- | :--- |
| Version | 1.2 |
| Last Updated | 2026-03-26 |
| Status | Final |

*v1.1 — Section 5: MCP filesystem pattern positioned as primary model for this workspace.*
*v1.2 — Section 3: Plan availability corrected — custom skills available on all plans including free (was incorrectly listed as Pro+ only). Verified claims log updated accordingly. Windows/Node.js verified claim added.*
