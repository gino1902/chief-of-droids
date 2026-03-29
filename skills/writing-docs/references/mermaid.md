# Mermaid Diagrams Reference

Read this file when the output contains one or more Mermaid diagrams.
Applies regardless of whether the document is an Elevate-themed deliverable or not.

---

## Closing Gate — non-negotiable

After any turn in which a `.mmd` file was read, edited, or produced,
the final line of the response must be:

> QA report available for `<filename>` — want me to run it?

This fires regardless of task type, scope, or skill classification.
If the response ends without this line and a `.mmd` file was touched, the rule was violated.

---

## Diagram Type Selection

Choose the diagram type before writing any code.

| Type | Use when |
| :--- | :--- |
| `flowchart` | System architecture, data flow, decision logic, process steps |
| `sequenceDiagram` | Time-ordered interactions between actors (API calls, event sequences) |
| `classDiagram` | Object/entity relationships, schemas, type hierarchies |
| `erDiagram` | Data model relationships (entities and cardinalities) |
| `stateDiagram-v2` | State machines, lifecycle transitions |
| `gantt` | Project timelines, task scheduling |
| `mindmap` | Concept decomposition, brainstorming structure |

Default to `flowchart` for system and architecture diagrams unless actor
sequencing or data modelling is the primary concern.

---

## Direction Selection

| Direction | Use when |
| :--- | :--- |
| `LR` | Pipelines, left-to-right data flow, system-to-system integrations |
| `TD` or `TB` | Hierarchies, org charts, tree structures, top-down processes |
| `RL` | Rarely used — only when LR creates visual confusion from a specific target node |
| `BT` | Rarely used — inverted hierarchies |

Default to `LR` for integration and architecture diagrams. Default to `TD` for
process flows and decision trees.

---

## Code Structure

Always write Mermaid diagrams in two parts, in this order:

**Part 1 — Declarations:**
- `%%{init}%%` block (if Elevate theme applies)
- `classDef` definitions
- `linkStyle default`
- Standalone node definitions (nodes not belonging to any subgraph) — declared before subgraph blocks
- `subgraph` blocks — containing node definitions only, no connections

**Part 2 — Connections** (after all `end` keywords):
- All `-->`, `-.->`, `<-->` edges
- All `class` assignments

Never define a node for the first time on a connection line. If a node appears
only in connections, declare it explicitly in Part 1 before the subgraph blocks.
Never mix connections into subgraph blocks. Never place `class` assignments
inside subgraphs.

---

## Subgraph Hierarchy

### Main wrapper (unique, always present in Elevate diagrams)

Wrap all content in a single outer `subgraph Main`. This subgraph exists for
layout control only — its border and background are hidden via `class Main main`.

```
subgraph Main
  subgraph "`**Label**`"
    ...nodes...
  end
end
```

### Cluster subgraphs (content grouping)

- Multiple clusters allowed inside `Main`
- Label syntax: `` "`**Label**`" `` — backtick wrapper + markdown bold
- Subgraph ID and display label are independent — always declare a clean ID
  (no spaces): `subgraph CleanID["`**Display Label**`"]`
- `class` assignment uses the ID, not the display label:
  `class CleanID primary_cluster` — not `class Display Label primary_cluster`

### Non-Elevate subgraphs

For diagrams not using the Elevate theme, standard subgraph syntax applies.
The `Main` wrapper is optional but still useful for layout control.

```
subgraph CompanyEnv["Company Environment"]
  ...
end
```

---

## Node Definitions

### Label syntax

- Use real newlines inside `[]` for multi-line labels — do not use `\n`
- Keep labels to two lines maximum; three is the hard limit
- First line: entity name. Second line: role or qualifier

```
PM[Packmind platform
Source of truth]
```

### Bracket types

| Syntax | Shape | Use for |
| :--- | :--- | :--- |
| `[Label]` | Rectangle | Systems, services, components |
| `(Label)` | Rounded rectangle | Processes, actions |
| `{Label}` | Diamond | Decisions |
| `([Label])` | Stadium / pill | Databases, stores |
| `[[Label]]` | Subroutine box | Sub-processes |
| `>Label]` | Asymmetric | Flags, annotations |

Default to `[Label]` (rectangle) for most architecture diagrams.

### Node IDs

- Uppercase or mixed case, no spaces — `PM`, `C_DEV`, `GH`
- Prefix related nodes with a shared token: `C_DEV`, `C_CC` for Customer nodes
- Never use Mermaid reserved keywords as IDs: `end`, `graph`, `subgraph`,
  `classDef`, `class`, `linkStyle`, `click`

---

## Edge Conventions

### Edge types

| Syntax | Renders as | Use for |
| :--- | :--- | :--- |
| `-->` | Solid arrow | Automatic, system-driven, primary flow |
| `-.->` | Dashed arrow | Optional, human-triggered, secondary flow |
| `<-->` | Bidirectional solid | Mutual, read/write, synchronous exchange |
| `<-.->` | Bidirectional dashed | Optional mutual exchange |
| `---` | Solid line, no arrow | Association without direction |

### Edge labels — pipe syntax only

Always use pipe syntax for edge labels. Never use inline dash syntax.

| ✅ Standard | ❌ Never use |
| :---------- | :----------- |
| `A -->|label| B` | `A --label--> B` |
| `A -.->|label| B` | `A -.-label-.-> B` |

Pipe syntax renders consistently across all renderers. Inline dash syntax is
renderer-dependent and produces broken output in some environments.

Additional label rules:
- Label only when the relationship is not self-evident from the node labels
- Keep labels short: 1–5 words
- Use lowercase, no full stop
- For human-triggered flows, append `- human` to the label: `update playbook - human`
- For tool-triggered flows, append `- Toolchain` or the tool name

---

## Elevate Theme Implementation

Read `shared/elevate-theme/elevate-mermaid.md` for the canonical copy-paste block.
Do not hardcode hex values — always copy from that file.

### Pattern summary

The Elevate theme uses three mechanisms in a fixed division of responsibility:

| Mechanism | Controls | What it cannot do |
| :--- | :--- | :--- |
| `%%{init}%%` | `edgeLabelBackground` only | Node fill, text, stroke |
| `classDef` | Node fill, text color, stroke; subgraph containers | Edge label background |
| `linkStyle default` | Edge label text color | Node appearance |

### Cluster depth convention

| Depth | Class | Nesting level |
| :---- | :---- | :------------ |
| 0 | `main` | Outermost wrapper — invisible, no visible border |
| 1 | `primary_cluster` | Top-level named system/domain containers |
| 2 | `secondary_cluster` | Sub-containers nested within a primary cluster |

**Named classes:**

| Class | Role |
| :--- | :--- |
| `main` | Outer layout wrapper — border and background invisible |
| `primary` | Primary brand nodes (highest visual weight) |
| `secondary` | Secondary nodes |
| `tertiary` | Tertiary nodes (lightest) |
| `primary_cluster` | Top-level named system/domain containers |
| `secondary_cluster` | Sub-containers nested within a primary cluster |
| `ytbc` | Yet-to-be-classified nodes |

Additional accent classes (`alt5`, `alt6`) are available for per-node use.
See `shared/elevate-theme/elevate-mermaid.md` for values.

### Class assignment block (always at bottom, after connections)

```
  class PM primary
  class DEV,GH secondary
  class C_DEV,C_CC tertiary
  class TeamA secondary_cluster
  class Company,Customer primary_cluster
  class Main main
```

Group by class on one line each. Comma-separate nodes sharing the same class.

---

## Known Rendering Pitfalls

- **Reserved keyword as node ID** — `end`, `graph`, `subgraph`, `class`, `style`
  will silently break parsing. Rename the node.
- **`\n` in node labels** — renders as literal text in some renderers (Obsidian,
  GitHub). Always use real newlines.
- **Inline dash edge label syntax** — `A --label--> B` is renderer-dependent.
  Always use pipe syntax: `A -->|label| B`.
- **Spaces in subgraph IDs** — `subgraph My Graph` is valid syntax but breaks
  `class My Graph primary_cluster`. Use a clean ID with an alias label:
  `subgraph MyGraph["My Graph"]`, then `class MyGraph primary_cluster`.
- **Subgraph ID vs display label** — `class` assignment always references the
  declared ID, never the display label. Assigning to the display label silently
  fails — the class is not applied.
- **Ghost class ID** — `class X classname` where `X` is not a declared node or
  subgraph ID silently does nothing. Always verify IDs match declared nodes/subgraphs.
- **`transparent` for `edgeLabelBackground`** — collapses the label box and
  causes rendering artefacts. Use `#FFFFFF` or the canvas background color.
- **`labelTextColor` in `%%{init}%%`** — silently ignored in GitHub and Obsidian.
  Use `linkStyle default color:` instead.
- **Bidirectional edges with labels** — `<-->|label|` is valid but label
  placement is renderer-dependent. Test before committing.
- **Deeply nested subgraphs** — more than two levels (Main → Cluster → inner)
  produces unpredictable layout in most renderers. Two levels is the hard limit.
- **FontAwesome icons (`fa:fa-*`)** — not available in GitHub, Obsidian, or VS Code
  by default — the icon name renders as raw text. Replace with emoji.

---

## Self-Check Gate

Before displaying any Mermaid diagram, run every item in the QA Checklist below
against the draft. Fix all failures before outputting. Do not display a diagram
that fails any checklist item.

This is a blocking step — not a post-output review.

---

## QA Checklist

Run each item against the draft diagram before displaying output. Fix failures first.

- [ ] Diagram type explicit
- [ ] Direction explicit — `LR` or `TD` stated, not defaulted
- [ ] All connectors after outer subgraph 'end'
- [ ] No standalone nodes first-defined on a connection line
- [ ] No `\n` in node labels — real newlines only
- [ ] No reserved keyword node IDs
- [ ] Subgraph IDs — no spaces; alias label used if display label needed
- [ ] No ghost class IDs — all `class X classname` IDs match a declared node or subgraph
- [ ] All classnames match declared classDef names
- [ ] Pipe syntax only for edge labels — no inline dash syntax
- [ ] class assignments reference IDs not display labels
- [ ] Replace FontAwesome icons by emoji
- [ ] Edge labels ≤5 words; human-triggered flows labeled `- human`
- [ ] Elevate: `%%{init}%%` block copied from `shared/elevate-theme/elevate-mermaid.md`
- [ ] Elevate: all `classDef` lines present and match canonical source
- [ ] Elevate: `linkStyle default color:#0F0E2B` present
- [ ] Elevate: `class Main main` assignment present
- [ ] Elevate: cluster depth convention applied — `primary_cluster` depth 1, `secondary_cluster` depth 2
- [ ] Elevate: no hardcoded hex values — copied from canonical source

---

## QA Report

### When to emit

Emit the full report only when the user confirms the closing gate offer.
Never emit without being asked.

### Report format

Number rows sequentially from the current QA Checklist — do not hardcode row
count. If the checklist grows, the report grows with it. One row per checklist item.

```
## Mermaid QA Report — <filename or diagram label>

| # | Check | Result |
| :- | :---- | :----- |
| 1  | <first item from QA Checklist> | ✅ Pass / ❌ Fail — <reason> |
| …  | … | … |
| N  | <last item from QA Checklist> | ✅ Pass / ❌ Fail — <reason> |

**Status: PASS / FAIL — <n> issues found**
```

Fail rows must include the specific reason.
If all pass, status is `PASS — 0 issues`.

---

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.4        |
| Last Updated | 2026-03-29 |
| Status       | Draft      |
