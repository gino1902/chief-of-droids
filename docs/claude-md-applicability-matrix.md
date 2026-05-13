# CLAUDE.md Applicability Matrix — Chat vs Code

Twenty-seven atomic claims about CLAUDE.md and project-instruction mechanics, mapped to each runtime: Claude Desktop chat (Chat) and Claude Code (Code).

## Environments

- **Chat** — Claude Desktop chat (claude.ai web app or desktop client). Two configuration slots per Project: Project Instructions (system-prompt-equivalent) and Project Knowledge (uploaded files, RAG-scaled). No native hierarchical instruction-file mechanism.
- **Code** — Claude Code, Anthropic's agentic coding CLI/tool. Auto-loads CLAUDE.md files from a directory hierarchy at session start; four official scopes (managed policy, project, user, local) concatenate into context.

This matrix excludes other Claude surfaces (API, Cowork, in-product agents) — they are governed by different mechanisms.

## Sources

Verified 2026-05-13 against fetched content.

- `code.claude.com/docs/en/memory` — Claude Code CLAUDE.md mechanics. Live page has no last-updated date.
  > ⚠️ Unverified — re-fetch before locking conventions (workspace `CLAUDE.md` tone convention).
- `support.claude.com/en/articles/9517075-what-are-projects` — Claude Desktop Projects definition. Page dated 2026-03-16.
- Workspace `CLAUDE.md` v1.0 (2026-05-12) — bespoke loader translation claims (workspace-internal).

## Claims

| # | Claim | Chat | Code |
|---|---|---|---|
| 1 | CLAUDE.md content is loaded as a user message after the system prompt, not as part of the system prompt itself | 🔶 | ✅ |
| 2 | CLAUDE.md is context, not enforced configuration | ✅ | ✅ |
| 3 | The official model defines four CLAUDE.md scopes: managed policy, project, user, and local | ❌ | ✅ |
| 4 | Multiple CLAUDE.md files concatenate into context; they do not override each other | ❌ | ✅ |
| 5 | Each official scope corresponds to a distinct audience (org / team / user-all-projects / user-one-project) | ❌ | ✅ |
| 6 | Load order is root-to-working-directory; within a directory, `CLAUDE.local.md` loads after `CLAUDE.md` | ❌ | ✅ |
| 7 | Project-root CLAUDE.md survives `/compact` and is re-injected from disk; nested CLAUDE.md files do not auto-reload after compaction | ❌ | ✅ |
| 8 | Target size is under 200 lines per CLAUDE.md file | 🔶 | ✅ |
| 9 | CLAUDE.md files are loaded in full regardless of length, though shorter files produce better adherence | 🔶 | ✅ |
| 10 | `@path` imports reduce file size but do not reduce token cost; imported files load in full at launch | ❌ | ✅ |
| 11 | Path-scoped rules (`.claude/rules/` with `paths:` frontmatter) load on-demand when matching files are read, not at launch | ❌ | ✅ |
| 12 | Contradictory rules across CLAUDE.md files cause Claude to pick one arbitrarily | 🔶 | ✅ |
| 13 | Specific, verifiable instructions outperform abstract ones for adherence | ✅ | ✅ |
| 14 | Multi-step procedures and partial-codebase content belong in skills or path-scoped rules, not CLAUDE.md | 🔶 | ✅ |
| 15 | Block-level HTML comments in CLAUDE.md are stripped before context injection | ❌ | ✅ |
| 16 | In Claude Code, hooks are the technical enforcement layer; CLAUDE.md is the behavioral guidance layer | ❌ | ✅ |
| 17 | Managed settings (`permissions.deny`, sandbox) enforce technically; managed CLAUDE.md guides behaviorally — they are not interchangeable | ❌ | ✅ |
| 18 | Claude Desktop Projects expose exactly two slots: Project Instructions (one per project, system-prompt-equivalent) and Project Knowledge (uploaded files, RAG-scaled) | ✅ | ❌ |
| 19 | Claude Desktop has no native hierarchical CLAUDE.md mechanism, no per-user scope, and no concatenation across projects | ✅ | ❌ |
| 20 | A rule belongs at the broadest scope where it is universally true for that scope's audience | ✅ | ✅ |
| 21 | Duplicate non-contradictory rules waste context tokens and create drift risk | ✅ | ✅ |
| 22 | Conditional or trigger-based loading mechanisms reduce always-on context cost | 🔶 | ✅ |
| 23 | In a non-Claude-Code environment, the loader mechanism for always-on context must itself live in a layer guaranteed to fire first | ✅ | ❌ |
| 24 | This workspace's `CLAUDE.md` is the functional equivalent of the official user-scope CLAUDE.md (`~/.claude/CLAUDE.md`) | ✅ | ❌ |
| 25 | This workspace's `skills/` + `HOW-TO-TRIGGER.md` is the functional equivalent of `.claude/rules/` with explicit triggers replacing `paths:` frontmatter | ✅ | ❌ |
| 26 | This workspace currently has no equivalent of `CLAUDE.local.md` — a structural gap, not a stylistic one | ✅ | ❌ |
| 27 | This workspace has no equivalent of Claude Code hooks; "must always happen" rules rely entirely on instructional framing | ✅ | ❌ |

## Legend

| Symbol | Meaning | Operational reading |
|---|---|---|
| ✅ | Applies natively | The mechanism or principle is documented for this runtime, or it is a universal cognitive / governance principle that holds without translation. No workspace-specific adaptation needed. |
| 🔶 | Translatable / analog exists | The underlying principle holds but the literal mechanism in the claim is runtime-specific. The other runtime requires a workspace-built equivalent. Cluster 23–27 documents the Chat-side analogs to Code-native mechanisms. |
| ❌ | Does not apply | Neither the mechanism nor the principle has a native or translatable form in this runtime. |

## Notes on row pairs

- Rows 18 and 19 are complementary, not duplicate: row 18 asserts what Chat *has*; row 19 asserts what Chat *lacks*. Both are needed for a reader to bound the Chat model.
- Rows 23–27 cluster the workspace-bespoke translation claims; they have no Code-side applicability because Code has the native mechanism the workspace builds an analog for.

---

| Field        | Value       |
|--------------|-------------|
| Version      | 1.1         |
| Last Updated | 2026-05-13  |
| Status       | Draft       |
