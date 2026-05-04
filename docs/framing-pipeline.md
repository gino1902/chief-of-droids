# Framing Pipeline

Process flow for the chief-of-droids framing lifecycle: ideation through to a validated `Framing.md`. Captures the iterative loops at ideation (A↔B) and at validation (D↔E), and the role of skill-triggered transitions vs prompt-and-answer turns.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"edgeLabelBackground": "#FFFFFF"}, "flowchart": {"defaultRenderer": "elk"}}}%%

flowchart TD
  classDef main              fill:#FFFAF0,color:#FFFAF0,stroke:#C5D8F6
  classDef primary           fill:#1F24E9,color:#FFFAF0,stroke:#425F8B
  classDef secondary         fill:#6DA5FF,color:#FFFFFF,stroke:#425F8B
  classDef tertiary          fill:#C5D8F6,color:#000000,stroke:#425F8B
  classDef primary_cluster   fill:#FFFFFF,color:#0F0E2B,stroke:#0F0E2B
  classDef secondary_cluster fill:#FFFAF0,color:#0F0E2B,stroke:#6DA5FF
  linkStyle default color:#0F0E2B

  subgraph Main
    subgraph FramingPipeline["`**Framing Pipeline**`"]
      A[Ideate]
      B(Project Outline)
      C([Framing.md
draft])
      D[Challenge
Framing]
      E{Framing
OK?}
      F([Framing.md
validated])
    end
  end

  A -->|P&A| B
  B --> A
  B -->|skill| C
  C -->|skill| D
  D -->|P&A| E
  E -->|no| D
  E -->|yes| F

  class E primary
  class A,B,D secondary
  class C,F tertiary
  class FramingPipeline primary_cluster
  class Main main
```

## Class mapping

| Node(s) | Class | Reason |
| :--- | :--- | :--- |
| E | `primary` | Sole decision gate — highest visual weight |
| A, B, D | `secondary` | Process steps |
| C, F | `tertiary` | Document artifacts |
| FramingPipeline | `primary_cluster` | Single named container |
| Main | `main` | Mandatory invisible wrapper |

## Edge labels

| Label | Meaning |
| :--- | :--- |
| `P&A` | Prompt & answer — user prompts, model responds |
| `skill` | Skill-triggered transition (`project-bootstrapping` for B→C, `analyzing-business-cases` challenge for C→D) |
| `no` / `yes` | Decision branches from the validation gate |

## Notes

The two `Framing.md` nodes (C and F) represent the same artifact at two states — `draft` (input to the challenge phase) and `validated` (output, gate passed). They are visually distinct via the `draft` / `validated` qualifiers in the labels.

The `B → A` back-edge is unlabelled — implied iteration continues until the outline stabilises and routes to the framing skill.

Theme assets sourced from `shared/elevate-theme/elevate-mermaid.md` (canonical Elevate Mermaid block, v1.8). Init block deduplicated relative to canonical source — see TASKS.md TBD if filed.

| Field | Value |
| :--- | :--- |
| Version | 1.0 |
| Last Updated | 2026-05-04 |
| Status | Draft |
