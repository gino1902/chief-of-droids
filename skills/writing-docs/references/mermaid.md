# Mermaid Diagrams Reference

Read this file when the output contains one or more Mermaid diagrams.
Applies regardless of whether the document is an Elevate-themed deliverable or not.

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
  `class CleanID cluster` — not `class Display Label cluster`

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

### Edge labels

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

**The five fixed classes:**

| Class | Role |
| :--- | :--- |
| `main` | Outer layout wrapper — border and background invisible |
| `primary` | Primary brand nodes (highest visual weight) |
| `secondary` | Secondary nodes |
| `tertiary` | Tertiary nodes (lightest) |
| `cluster` | Inner subgraph container labels |

Additional accent classes (`alt5`, `alt6`) are available for per-node use.
See `shared/elevate-theme/elevate-mermaid.md` for values.

### Class assignment block (always at bottom, after connections)

```
  class PM primary
  class DEV,GH secondary
  class C_DEV,C_CC tertiary
  class Company,Customer cluster
  class Main main
```

Group by class on one line each. Comma-separate nodes sharing the same class.

---

## Known Rendering Pitfalls

- **Reserved keyword as node ID** — `end`, `graph`, `subgraph`, `class`, `style`
  will silently break parsing. Rename the node.
- **`\n` in node labels** — renders as literal text in some renderers (Obsidian,
  GitHub). Always use real newlines.
- **Spaces in subgraph IDs** — `subgraph My Graph` is valid syntax but breaks
  `class My Graph cluster`. Use a clean ID with an alias label:
  `subgraph MyGraph["My Graph"]`, then `class MyGraph cluster`.
- **Subgraph ID vs display label** — `class` assignment always references the
  declared ID, never the display label. Assigning to the display label silently
  fails — the class is not applied.
- **`transparent` for `edgeLabelBackground`** — collapses the label box and
  causes rendering artefacts. Use `#FFFFFF` or the canvas background color.
- **`labelTextColor` in `%%{init}%%`** — silently ignored in GitHub and Obsidian.
  Use `linkStyle default color:` instead.
- **Bidirectional edges with labels** — `<-->|label|` is valid but label
  placement is renderer-dependent. Test before committing.
- **Deeply nested subgraphs** — more than two levels (Main → Cluster → inner)
  produces unpredictable layout in most renderers. Two levels is the hard limit.
- **FontAwesome icons (`fa:fa-*`)** — valid Mermaid syntax but requires the
  FontAwesome CDN to be loaded at render time. Not available in GitHub, Obsidian,
  or VS Code by default — the icon name renders as raw text. Use emoji instead.

---

## QA Checklist

- [ ] Diagram type matches the content model (flowchart for architecture, sequence for actor flows)
- [ ] Direction chosen explicitly — `LR` or `TD` stated, not defaulted
- [ ] Code in two parts: declarations + subgraphs first, connections + class assignments second
- [ ] Standalone nodes declared explicitly in Part 1 — no node first-defined on a connection line
- [ ] No `\n` in node labels — real newlines only
- [ ] No Mermaid reserved keywords used as node IDs
- [ ] Subgraph IDs contain no spaces; display label used via alias syntax if needed
- [ ] `class` assignments reference subgraph IDs, not display labels
- [ ] No FontAwesome `fa:fa-*` icons — use emoji if an icon is needed
- [ ] Edge labels ≤5 words; human-triggered flows labeled `- human`
- [ ] Elevate diagrams: `%%{init}%%` block copied from `shared/elevate-theme/elevate-mermaid.md`
- [ ] Elevate diagrams: all five `classDef` lines present
- [ ] Elevate diagrams: `linkStyle default color:#0F0E2B` present
- [ ] Elevate diagrams: `class Main main` assignment present
- [ ] Elevate diagrams: no hardcoded hex values — copied from canonical source
- [ ] Non-Elevate diagrams: no Elevate-specific classes applied


---

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.1        |
| Last Updated | 2026-03-28 |
| Status       | Draft      |
