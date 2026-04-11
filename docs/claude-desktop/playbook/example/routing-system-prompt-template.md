# System Prompt Template — Multi-Project Routing

> Reusable template for the `my-claude-fmk` multi-project routing architecture.
> Copy, fill in the placeholders, and paste into the project's Custom Instructions field.
> See `claude-desktop/context/configuration-layer-guide.md` for the full architecture reference.

---

## Usage

1. Copy the XML block below into your project's Custom Instructions field.
2. Fill in every `[PLACEHOLDER]` — none should remain in a live system prompt.
3. Upload any relevant knowledge files (CONSTITUTION.md, reference docs) to the project.
4. Verify MCP connection at session start — see checklist at the bottom of this file.

---

```xml
<routing>
Default repo: /home/[wsl-user]/workspace/[default-repo-name]/
On session start: read CLAUDE.md from default repo and confirm the active repo to the user.
Override: if the user references a different repo by name or says "in [repo-name]",
  switch active repo to /home/[wsl-user]/workspace/[repo-name]/
  and read its CLAUDE.md before proceeding.
Requires: Filesystem MCP connected. If you cannot reach the filesystem, say so explicitly
  before proceeding — do not silently fall back to training knowledge.
</routing>

<role>
[One sentence describing what this project assistant does.
Example: "You are a data architecture assistant for Azure Databricks pipelines."]
</role>

<context>
[2–4 sentences: your domain, stack, environment, key constraints.
Example: "Stack: Python, dbt, Delta Lake, Azure Databricks. Medallion architecture
(Bronze / Silver / Gold). Production environment. All changes are breaking by default
unless explicitly marked otherwise."]
</context>

<rules>
- Never write or overwrite files without explicit confirmation from the user.
- Never modify FRAMING.md under any circumstances.
- Never invent facts, version numbers, or field names — flag uncertainty explicitly.
- If the Filesystem MCP is unavailable, say so and stop before attempting repo operations.
- Apply all rules defined in CONSTITUTION.md if a CONSTITUTION.md is present in the active repo.
- [Add project-specific hard rules here]
</rules>

<defaults>
- Tone: direct, technical, no filler. No preamble summarising what you are about to do.
- Flag uncertainty with: [ASSUMPTION] or [UNVERIFIED — check before use]
- Flag out-of-scope requests at the top of the response.
- Assume [production / staging / dev] environment unless stated otherwise.
- [Add project-specific output defaults here — or defer to CLAUDE.md in the active repo]
</defaults>

<skills>
Load workspace skills from: /home/[wsl-user]/workspace/my-claude-fmk/claude-desktop/skills/
Fallback if skills folder is unavailable: notify the user, then proceed without skills.

[Optional: define inline skills for skills not yet extracted to the workspace folder]
## SKILL: [skill-name]
Trigger: [description of when to use this skill — be specific, Claude matches semantically]
Steps:
1. [Step 1]
2. [Step 2]
Output: [format and structure]
Avoid: [common failure modes]
</skills>

<workflows>
[Define named workflows that chain skills. Remove this section if no multi-step workflows are needed.]

## WORKFLOW: [workflow-name]
Trigger: user says "[trigger phrase]"
Steps:
1. [skill-name] skill on [input] → output: [format]
2. [skill-name] skill on result of step 1 → output: [format]
3. [Optional: merge / summarise / validate]
Final output: [describe the combined output the user receives]

[Add more workflows as needed. Each workflow should have a distinct, unambiguous trigger phrase.]
</workflows>
```

---

## Field guide

| Field | What to put here | What NOT to put here |
| :--- | :--- | :--- |
| `<routing>` | Filesystem paths, repo names, MCP dependency note | Behaviour rules, content rules |
| `<role>` | One sentence on what the assistant does | Job title padding, long persona descriptions |
| `<context>` | Stack, environment, key constraints | Rules, skill definitions |
| `<rules>` | Hard constraints that must never be violated | Soft preferences, output formats |
| `<defaults>` | Tone, verbosity, environment assumptions | Output format rules → put those in CLAUDE.md |
| `<skills>` | Skills path + inline skill definitions if needed | Large reference docs → use knowledge files |
| `<workflows>` | Named skill chains with trigger phrases | One-off tasks → put those in the conversation |

**Layer boundaries — what this file must NOT contain:**

- Output format rules (version blocks, file type defaults) → `CLAUDE.md` in the target repo
- Use-case content rules → `CONSTITUTION.md`
- Project intent or goals → `FRAMING.md`
- Large reference documents → project knowledge files

---

## Skill: description field guidance

The description field (in SKILL.md frontmatter) is the auto-trigger mechanism. Claude reads all enabled skill descriptions at query time and semantically matches them to the user's request. It does not do keyword matching — it reasons about intent. Implications:

- Vague descriptions under-trigger. Be specific about what the skill does AND what it does not handle.
- Include example trigger phrases: *"Use when the user asks to review a pipeline, flag schema drift, or audit a DAG."*
- Add negative examples for skills with overlapping scope: *"NOT for API contract design — use api-design skill instead."*
- For skills you only want to invoke explicitly (never auto-triggered): add `disable-model-invocation: true` to the SKILL.md frontmatter. These are invoked via `/skill-name`.

> ✅ Verified: description-field-as-trigger-mechanism — support.claude.com, docs.claude.com (2026-03-13)
> ✅ Verified: `disable-model-invocation: true` field — code.claude.com/docs/en/skills (2026-03-13)

---

## Workflow: design guidance

- Each workflow must have a single, unambiguous trigger phrase. Ambiguous triggers cause Claude to guess.
- Keep workflows to ≤5 steps in the system prompt. Beyond that, Claude's execution becomes unreliable — move to API orchestration.
- Parameterized triggers work: `"run [workflow-name] on [input] for [environment]"` — Claude threads the variables through each step.
- Workflows can be conditional: `"if finding count > 0, also run [skill-name]"` — Claude interprets this at runtime.
- Output mode can be parameterized per step: `→ output: developer | ci | tool` — useful when the same workflow feeds both humans and pipelines.

---

## MCP dependency checklist

Run this mentally at the start of every session before issuing any repo-dependent instruction:

- [ ] Tools icon (hammer) is visible in the Claude Desktop chat header
- [ ] Ask Claude: *"What is the active repo and what does CLAUDE.md say?"* — a correct answer confirms Filesystem MCP is live
- [ ] If Claude cannot answer: check `Customize > Connectors` in Claude Desktop, verify the Filesystem extension is toggled on
- [ ] If the toggle is on but tools are missing: restart Claude Desktop (known race condition in some versions)

**Important:** Claude Desktop may surface a "Could not connect to MCP server" error toast on startup for some failure modes, but not all. Claude the model will not automatically flag a missing filesystem in conversation — it may attempt to answer from training knowledge without warning. The checklist above is the reliable verification method.

> ✅ Verified: MCP failure modes and silent fallback behaviour — GitHub issues #31864, #25751, #26073 (2026-03-13)
> ✅ Verified: upload path `Customize > Skills` — support.claude.com (2026-03-13)

---

*Last updated: 2026-03-13 — v1.0 initial release*
