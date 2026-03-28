<!-- version: 1.5 | author: chief-of-droids workspace | last_updated: 2026-03-28 -->

# Session Log Schema

Defines the canonical format for the two output files written by the
`managing-sessions` skill. Read this file before any write operation.

---

## Contents

1. [Output 1 — Findings file](#output-1--findings-file)
2. [Output 2 — Removal log](#output-2--removal-log)
3. [Write Rules](#write-rules-both-files)

---

## Output 1 — Findings file

**Path:** `/home/gino/workspace/.tasks/sessions-findings/YYYY-MM-DD-<project>-findings.md`

Written on every confirmed analysis run. Contains all extracted value:
classifications, net-new content, gaps, and memory challenge results.
Never contains the removal record — that lives in Output 2.

```markdown
# Session Analysis Findings — YYYY-MM-DD

## Summary

| Field | Value |
|:------|:------|
| Run date | YYYY-MM-DD |
| Source project | [resolved from CLAUDE.md, or "unknown-project"] |
| Sessions analysed | N |
| Sessions recommended for removal | N |
| Confidence level | High / Medium / Low |
| Net-new findings | N |
| Known gaps identified | N |
| Removal log | [path to removal log, or "none — no sessions removed"] |

---

## Extracted Findings

| Category | Finding | Source session | Status | On-disk location | Promoted to |
|:---------|:--------|:---------------|:-------|:-----------------|:------------|
| Architecture decision | [description] | [title] (YYYY-MM-DD) | on-disk | [path] | — |
| Tool quirk | [description] | [title] (YYYY-MM-DD) | not-on-disk | — | — |
| Correction | [description] | [title] (YYYY-MM-DD) | superseded | [newer source] | — |

Status values:
- `on-disk` — confirmed present in target file (Pass 3 verified)
- `on-disk-unverified` — target file unreadable; classified by reference only
- `not-on-disk` — valuable; written verbatim in Net-New Content below
- `superseded` — contradicted by a newer on-disk source or session

Promoted to: fill in after promoting to a centralised doc; leave `—` at write time.

---

## Net-New Content

Findings classified `not-on-disk`, written verbatim. Authoritative record
until promoted to a centralised workspace doc.

### [Category — e.g. Tool Quirks]

[Content written in the style of the target doc it will be promoted to.]

> Promote to: [target file path] — not yet written

---

## Known Gaps

| Gap | Recommended action | Priority |
|:----|:-------------------|:---------|
| [description] | [action] | High / Medium / Low |

---

## Memory Challenge Results

| Memory claim | Rule triggered | On-disk state | Risk | Recommendation |
|:-------------|:---------------|:--------------|:-----|:---------------|
| [claim] | Rule N — [name] | [on-disk value] | High/Med/Low | [action] |

If no contradictions found: "No contradictions detected against on-disk sources."
If memory challenge not yet run: "Pending — appended after challenge memories."
```

---

## Output 2 — Removal log

**Path:** `/home/gino/workspace/.logs/sessions-removed/YYYY-MM-DD-<project>-removed.md`

Written **only when at least one session is confirmed for removal**.
Do not create this file if the pruning recommendation results in zero removals.
Contains only the removal record — no findings, no net-new content.

```markdown
# Session Removal Log — YYYY-MM-DD

## Summary

| Field | Value |
|:------|:------|
| Run date | YYYY-MM-DD |
| Source project | [resolved from CLAUDE.md, or "unknown-project"] |
| Sessions removed | N |
| Findings reference | [path to corresponding findings file] |

---

## Removed Sessions

| Title | Date | Reason | Findings reference |
|:------|:-----|:-------|:-------------------|
| [session title] | YYYY-MM-DD | All findings on-disk | [findings file path] |
| [session title] | YYYY-MM-DD | Superseded by later session | [findings file path] |
| [session title] | YYYY-MM-DD | Bootstrap/test — no extractable value | [findings file path] |
```

---

## Write Rules (both files)

- Never overwrite an existing file — append `-2`, `-3` suffix if needed
- `source project` is mandatory — `unknown-project` acceptable, blank never acceptable
- Findings file: `not-on-disk` content written in full — never summarised or truncated
- Removal log: created only when sessions are confirmed for removal — no empty files
- Removal log `findings reference` column always links to the corresponding findings file
- `Promoted to` column in findings: starts as `—`; update manually after promotion

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.5        |
| Last Updated | 2026-03-28 |
| Status       | Draft      |
