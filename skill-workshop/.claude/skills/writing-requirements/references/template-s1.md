# Template — Generic (S1)

Nine sections, always rendered. `N/A` if substrate signal absent.

| # | Section | ID prefix | Syntax |
|:--|:--|:--|:--|
| 1 | Title + Purpose | — | Prose |
| 2 | Scope | — | In/Out lists or `N/A` |
| 3 | Actors & Consumers | — | Table |
| 4 | Glossary | — | Definition list |
| 5 | Functional Requirements | `FR-NNN` | EARS |
| 6 | Constraints | `FR-NNN` (continues FR sequence) | EARS |
| 7 | Acceptance Criteria | — | Per-requirement |
| 8 | Quality Criteria scorecard | — | Per-requirement table |
| 9 | Version block | — | Table |

---

## §1 Title + Purpose

```markdown
# <component name>

## Purpose
<one paragraph>
```

---

## §2 Scope

```markdown
## Scope

### In Scope
- <item>

### Out of Scope
- <item>
```

Both subsections render even if one is `N/A`.

---

## §3 Actors & Consumers

Table with columns: Actor | Role | Direction.

Direction values: `upstream`, `downstream`, `user`.

---

## §4 Glossary

```markdown
**Term** — definition. *(auto-derived — verify)*
```

One entry per term. Auto-derived entries flagged with `(auto-derived — verify)`.

---

## §5 Functional Requirements

```markdown
**FR-NNN** — [EARS statement]
```

Group by logical area if more than five entries; no sub-headings required for five or fewer.

---

## §6 Constraints

Same entry format as §5. ID sequence continues from §5 — no reset.

```markdown
**FR-NNN** — [EARS statement]
```

---

## §7 Acceptance Criteria

See `references/verification.md`.

---

## §8 Quality Criteria scorecard

See `references/verification.md`.

---

## §9 Version block

```markdown
| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.x        |
| Last Updated | YYYY-MM-DD |
| Status       | Draft      |
```
