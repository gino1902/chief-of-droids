<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-03-30 -->

# Workflow: add-source

Governed by: `creating-skills` skill.
Triggered when the user wants to evaluate and add a new external source to `skill-sources.md`.

---

## Trigger phrases

- "add [URL] to skill sources"
- "add [URL] to the skills catalog"
- "I want to add X to the skills catalog sources"
- "add source to skill-sources"
- "evaluate [URL] as a skill source"
- "add source: [URL]"

---

## Step 0 — Environment Detection

Attempt to read `references/assessment-checklist.md` via Filesystem MCP tool.
- Succeeds → **Claude Desktop** — filesystem reads and web fetches will be attempted
- Fails / tool unavailable → **Claude.ai** — Filesystem MCP unavailable

Report result:
- ✅ `Environment: Claude Desktop — fetch and filesystem writes will be attempted`
- ⚠️ `Environment: Claude.ai — Filesystem MCP unavailable; cannot write skill-sources.md`

If Claude.ai detected: this workflow can run fetch and scoring steps in chat, but
the final write to skill-sources.md must be performed manually. Surface this once; do not repeat.

---

## Step 1 — Criterion 1: Fetch

Fetch the provided URL via `web_fetch`.

| Outcome | Action |
|:--------|:-------|
| Content returned, non-empty | ✅ Criterion 1 pass — proceed to Step 2 |
| 404 / auth wall / robots block | ❌ Criterion 1 fail — stop; add to Exclusion Log; report to user |
| Partial content (directory listing empty but page loads) | ⚠️ Partial fetch — flag; attempt targeted sub-path fetches before deciding |

If partial: attempt up to two sub-path fetches to locate SKILL.md files (e.g. append `/skills/`, `/plugins/`).
If all sub-path fetches fail to return SKILL.md content: treat as Criterion 1 fail.

---

## Step 2 — Criterion 2: SKILL.md check

From the fetched content, confirm the source contains **individually addressable SKILL.md files**
with explicit trigger/scope definition (YAML frontmatter `name` + `description` fields).

Individually addressable = each skill lives in its own named directory containing SKILL.md,
not embedded in a config file or concatenated into a single monolith.

| Outcome | Action |
|:--------|:-------|
| SKILL.md files confirmed, frontmatter visible | ✅ Criterion 2 pass — proceed to Step 3 |
| Files present but not individually addressable (aggregator, config harness, monolith) | ❌ Criterion 2 fail — stop; add to Exclusion Log; report to user |
| Directory structure confirmed but SKILL.md content not directly fetchable | ⚠️ Partial — note fetch limitation; proceed with available content, flag in catalog |

Report SKILL.md count found (or estimated from directory listing).

---

## Step 3 — Criterion 3: Stratified sampling and scoring

Sample 2–3 skills from the catalog. For catalogs with >10 skills, stratify:
- 1 simple skill (single-file, narrow scope)
- 1 workflow skill (multi-step, conditional logic)
- 1 tool-integration skill (explicit tool calls)

For each sampled skill, score the five criteria on a 1–5 scale:

| Criterion | Weight | 1 | 3 | 5 |
|:----------|:-------|:--|:--|:--|
| Reusability | 25% | Heavy project-context dependencies | Some deps, mostly portable | No project-context or sibling-skill dependencies |
| Context-awareness | 20% | Breaks on trigger variants | Adapts to most variants | Graceful across all trigger variants |
| Tool integration | 20% | No tool guidance | Some tool guidance | Explicit when/why/how per tool |
| Determinism | 15% | Output varies across runs | Mostly consistent | Consistent output structure |
| Security | 20% | Blind exec, unconstrained fetch | Some scoping | Scoped calls, no blind exec |

**Score = Σ(rating × weight)** — computed as a weighted decimal.
**Worst-case sampled skill** governs the Security rating (same rule as existing catalog).

Exclusion threshold: score < 3.00 → add to Exclusion Log, do not add to catalog.

---

## Step 4 — Gather catalog fields

For sources that pass all three criteria:

| Field | How to obtain |
|:------|:-------------|
| Name | Human-readable label — derive from repo name or publisher |
| Address | Full URL as provided |
| Repo | `owner/repo` format for GitHub repos; n/a otherwise |
| Reusability / Context-awareness / Tool integration / Determinism / Security | From Step 3 scoring |
| Score | Computed weighted decimal from Step 3 |
| Stars | From fetched page — use `~` prefix if from search snippet, not direct repo page |
| Engineer signal | Strong / Weak / None + one-line evidence. Strong = named practitioner citation. |

If any field cannot be determined from fetched content: record as `n/a` and note the gap.

---

## Step 5 — Propose and write

Present the proposed catalog row to the user:

```
Proposed addition to skill-sources.md:

| [Name] | [Address] | [Repo] | [Reusability] | [Context-awareness] | [Tool integration] | [Determinism] | [Security] | [Score] | [Stars] | [Engineer signal] |
```

Also state:
- Whether any fetch limitations were encountered (Criterion 1 partial)
- Insertion position (sorted by Score desc, Stars desc within ties)
- Whether the "Adding a New Source" section in skill-sources.md had content to remove (it should have been removed — if still present, flag)

Await explicit approval before writing.

On approval:
1. Read `references/skill-sources.md` via filesystem tool
2. Insert the new row in the correct sort position in the Catalog table
3. Update `last_updated` in the header comment
4. Write the file via `filesystem:write_file`
5. Read the file back immediately to confirm write succeeded

If any source was rejected at Criterion 1, 2, or 3: add it to the Exclusion Log table
before writing, with `Reason` and `Criterion failed` columns populated.

---

## Failure handling

| Condition | Action |
|:----------|:-------|
| Criterion 1 fail (fetch blocked) | Add to Exclusion Log; report criterion and reason; stop |
| Criterion 2 fail (no addressable SKILL.md) | Add to Exclusion Log; report criterion and reason; stop |
| Criterion 3 fail (score < 3.00) | Add to Exclusion Log with score; report criterion; stop |
| Partial fetch (some content, not full SKILL.md text) | Flag in catalog entry; proceed with available evidence; note reduced confidence |
| Filesystem write fails | Retry once; if still fails, surface content to user for manual addition |
| Skill-sources.md not found | Flag: `⚠️ skill-sources.md not found at expected path` — do not proceed; verify path |

---

| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | 2026-03-30 |
| Status       | Final      |
