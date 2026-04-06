<!-- version: 1.0 | author: chief-of-droids workspace | last_updated: 2026-04-06 -->

# Workflow: update-comparison-guide

Governed by: `reviewing-tech-claims` skill.
Triggered when the user wants to verify, correct, and/or expand the
Claude Code vs Claude.ai vs Claude Desktop comparison reference guide.

Target file: `my-claude-fmk/claude-desktop/claude-code-vs-claudeai.md`
Target repo: `/home/gino/workspace/my-claude-fmk`

---

## Trigger phrases

- `update comparison guide`
- `tech verify comparison guide`
- `verify and update claude-code-vs-claudeai`
- `refresh comparison guide`
- `check comparison guide against official docs`

---

## Step 0 — Environment check

Attempt to read
`/home/gino/workspace/skills/reviewing-tech-claims/references/verification-workflow.md`
via Filesystem MCP tool.

- Succeeds → ✅ `Environment: Claude Desktop — filesystem reads and web fetches available`
- Fails → halt: `⚠️ verification-workflow.md unreadable — cannot proceed`

Read `references/verification-workflow.md` now. Load the Official Sources table
and the 4-step verification procedure. Both apply in full throughout this workflow.

---

## Step 1 — Read the guide

Read the full current file via `filesystem:read_text_file`:
`/home/gino/workspace/my-claude-fmk/claude-desktop/claude-code-vs-claudeai.md`

If unreadable: halt.
`⚠️ Guide not found at expected path — resolve before continuing.`

Note from the version block:
- Current version number
- Last Updated date — used in Step 4 to scope the gap analysis

---

## Step 2 — Claim inventory (silent)

For every table in the guide, identify each verifiable claim. Do not output
this inventory to chat. It is an internal planning artefact.

Categorise each claim:

| Category | Examples |
| :--- | :--- |
| File path / location | `~/.claude/settings.json`, `.claude/rules/*.md` |
| UI path | `Customize > Skills`, `Settings > Capabilities` |
| CLI flag / command | `--append-system-prompt`, `/memory`, `/compact` |
| Package name / import | `claude-agent-sdk`, `@anthropic-ai/claude-agent-sdk` |
| API parameter / syntax | `container: {skills: [...]}`, beta header names |
| Feature existence / plan availability | "available on free plan", "experimental" |
| Precedence / order rule | `Managed > CLI args > Local > Project > User` |
| Numeric limit | `200 lines`, `25KB`, `250-char description cap` |
| Cross-product statement | "Claude Desktop uses same memory as claude.ai" |

From the inventory, derive the minimum set of source pages needed to cover all
claims. Group claims by page — a single page may cover claims from multiple guide
sections.

Surface only:
- Total claim count
- Source pages required (list of domains/paths, no full URLs yet)
- Any claims with no identifiable source — flag these before fetching

---

## Step 3 — Verify existing claims

For each source page identified in Step 2, use the search-first fetch pattern:

1. `web_search` with a short, specific query to surface the current URL
2. `web_fetch` on the exact URL returned

Do not hardcode URLs. Use `web_search` every time — pages move and paths change.

Apply the 4-step verification procedure from `verification-workflow.md` to every
claim covered by each fetched page before moving to the next page. One page fetch
covers all claims sourced from it — minimise round-trips.

For each claim record one of:

| Outcome | Mark |
| :--- | :--- |
| Claim confirmed against fetched content | ✅ Verified: [source domain], [fetch date] |
| Claim contradicted by fetched content | ❌ Correction: [what it should say] |
| Source not findable or access blocked | ⚠️ Unverified — flag in report |
| Source stale (>12 months) | ⚠️ Stale — attempt one re-fetch; if still stale, flag and stop |

When all source pages are fetched and all claims assessed, surface:

`Verification complete: N ✅ confirmed | N ❌ corrections | N ⚠️ unverified`

---

## Step 4 — Gap analysis

Identify features documented in official sources that are absent from the guide.

**Pass 1 — Feature docs scan (primary)**

For each major Claude Code doc section not yet fetched in Step 3, fetch and scan
for documented capabilities with no corresponding row in the guide. Priority pages:

- Claude Code sub-agents
- Claude Code agent teams
- Claude Code skills
- Claude Code hooks
- Claude Code permissions
- Claude Code memory
- Claude Code settings

Use `web_search` to surface current URLs before fetching each page.
Skip any page already fully fetched in Step 3.

**Pass 2 — Release notes scan (recency)**

Search for: Claude release notes `support.claude.com` and Claude Code changelog
`code.claude.com`. Fetch both. Identify any feature shipped after the guide's
Last Updated date (recorded in Step 1) that touches a comparison category.

This pass confirms recency, not discovery — it catches very recent additions not
yet reflected in feature doc pages.

For each gap found, record:

| Section | Missing concept | Source | Priority |
| :--- | :--- | :--- | :--- |
| §N | [feature + one-line description] | [source domain] | High / Medium / Low |

Priority guidance:
- **High** — documented feature with zero representation in the guide
- **Medium** — documented sub-feature or variant not reflected in any existing row
- **Low** — nuance or minor variant already implied by existing rows

Surface:
`Gap analysis complete: N gaps found (H high, M medium, L low priority)`

---

## Step 5 — Report and approval gate

Produce a structured report in chat. Do not write any file before this report
is explicitly approved.

```
## Update report — v[current] → v[proposed]

### Corrections (N)
| Section | Row | Was | Now | Source |
| :--- | :--- | :--- | :--- | :--- |

### Gaps proposed for addition (N — by priority)
| Section | Concept | Claude.ai | Claude Desktop | Claude Code | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |

### Unverified claims remaining (N)
| Section | Claim | Reason |
| :--- | :--- | :--- |
```

**Version bump** — per workspace CLAUDE.md convention:
- Corrections only, no new rows → increment `1.x` minor
- New rows or sections added → increment `1.x` minor
- Structural rewrite (columns added, sections reorganised) → `2.0`

**Fast exit:** if the report shows zero corrections and zero gaps, state:
`Guide is current — no changes needed.`
Do not proceed to Step 6.

Await explicit approval (`yes`, `approved`, `go ahead`) before writing.
If the user requests changes to the report: revise and re-present.
Do not write until a clean approval is given.

---

## Step 6 — Write the file

On approval:

1. Read the full current file via `filesystem:read_text_file` — mandatory even
   if the file was read in Step 1. Never rewrite from memory or prior context.
2. Apply all approved corrections and gap additions.
3. Update the version block:
   - Increment version number per the rule in Step 5
   - Set Last Updated to today's date
   - Append a Changes entry in the footer changelog
4. Write via `filesystem:write_file`.
5. Read back the first 20 lines via `filesystem:read_text_file` to confirm the
   write succeeded and the version block is correct.

If write fails: retry once. If still fails, surface the full proposed content
to the user for manual write. Do not silently abandon.

---

## Step 7 — Commit

Ask: "Do you want to commit?"

On yes — ask: "Display diffs? (yes/no)"
- Yes → run `git_diff_staged` after staging, display diff, then commit
- No → commit directly

Stage with explicit file path:

```
git_add: ["claude-desktop/claude-code-vs-claudeai.md"]
repo_path: /home/gino/workspace/my-claude-fmk
```

Commit message format:
```
docs(claude-desktop): update claude-code-vs-claudeai.md to vX.Y

- [corrections applied, one line each]
- [gaps added, one line each]
```

Push manually from WSL2 — `git_push` unavailable via MCP.

---

## Failure handling

| Condition | Action |
| :--- | :--- |
| Guide file not readable | Halt at Step 1; flag path; do not proceed |
| `verification-workflow.md` not readable | Halt at Step 0; follow SKILL.md failure handling |
| `web_fetch` blocked (permissions error) | Use `web_search` to surface current URL; retry fetch; if still blocked, mark ⚠️ Unverified |
| Source stale (>12 months) | Flag date; attempt one re-fetch on same domain; if still stale, exclude and flag |
| User does not approve report | Revise per feedback; re-present; do not write |
| Filesystem write fails | Retry once; surface full proposed content to user for manual write |
| Gap analysis page returns 404 | Use `web_search` to find current equivalent path; fetch that; if not found, note in report |

---

| Field        | Value      |
|:------------ |:---------- |
| Version      | 1.0        |
| Last Updated | 2026-04-06 |
| Status       | Final      |
