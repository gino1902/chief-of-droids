# Elevate — Mermaid Theme

Canonical source: `shared/elevate-theme/tokens.json`  
Derived from: `shared/Elevate-theme-colors.md`

---

## Approach

Elevate Mermaid theming uses a **hybrid pattern**:

- `%%{init}%%` — minimal block, used only for `edgeLabelBackground` (not controllable via `classDef`)
- `classDef` — all node and subgraph container styling
- `linkStyle default` — edge label text color

**Why not `%%{init}%%` only:** `labelTextColor` is unreliable across renderers
(GitHub, Obsidian, VS Code) — it is often silently ignored and edge label text
renders white. `classDef` applied to subgraph IDs is the verified, renderer-stable
approach for container styling.

**Correction:** subgraph containers do accept `class <subgraph-id> <classname>` —
this is valid Mermaid syntax and renderer-stable as of v10+.

---

## Canonical pattern — copy-paste

```mermaid
%%{init: {"theme": "base", "themeVariables": {"edgeLabelBackground": "#FFFFFF"}}}%%
flowchart LR
  classDef main      fill:#FFFAF0,color:#FFFAF0,stroke:#C5D8F6
  classDef primary   fill:#1F24E9,color:#FFFAF0,stroke:#425F8B
  classDef secondary fill:#6DA5FF,color:#FFFFFF,stroke:#425F8B
  classDef tertiary  fill:#C5D8F6,color:#000000,stroke:#425F8B
  classDef cluster   fill:#FFFFFF,color:#0F0E2B,stroke:#0F0E2B
  classDef ytbc      fill:#D9E4F0,color:#3A3A4A,stroke:#425F8B
  linkStyle default color:#0F0E2B

  subgraph Main
    subgraph "`**Company**`"
      PM[Packmind platform
      Source of truth]
      DEV[Developer environment
      repo + Copilot + packmind-cli]
      GH[GitHub Copilot]
    end
    subgraph "`**Customer**`"
      C_DEV[Developer environment
      repo + Claude Code + packmind-cli]
      C_CC[Claude Code]
    end
  end

  PM -->|copilot-instructions.md| DEV
  PM -.->|CLAUDE.md, skills, commands| C_DEV
  DEV <-->|read/write| GH
  C_DEV <-->|read/write| C_CC
  GH -->|update playbook - human| PM
  C_CC -.->|update playbook - human| PM
  DEV -->|deviation detected - Toolchain| PM
  C_DEV -.->|deviation detected - Toolchain| PM

  class PM primary
  class DEV,GH secondary
  class C_DEV,C_CC tertiary
  class Company,Customer cluster
  class Main main
```

---

## classDef token mapping

| Class | Role | Fill | Text | Stroke | Elevate tokens |
| :---- | :--- | :--- | :--- | :----- | :------------- |
| `main` | Outer wrapper subgraph — invisible | `#FFFAF0` | `#FFFAF0` | `#C5D8F6` | lt2 / lt2 / accent3 |
| `primary` | Primary brand nodes | `#1F24E9` | `#FFFAF0` | `#425F8B` | accent1 / lt2 / accent4 |
| `secondary` | Secondary nodes | `#6DA5FF` | `#FFFFFF` | `#425F8B` | accent2 / lt1 / accent4 |
| `tertiary` | Tertiary nodes | `#C5D8F6` | `#000000` | `#425F8B` | accent3 / dk1 / accent4 |
| `cluster` | Inner subgraph containers | `#FFFFFF` | `#0F0E2B` | `#0F0E2B` | lt1 / dk2 / dk2 |
| `ytbc` | Yet-to-be-classified nodes | `#D9E4F0` | `#3A3A4A` | `#425F8B` | (outside Elevate) / (outside Elevate) / accent4 |

---

## init block rationale

| Variable | Value | Reason |
| :--- | :--- | :--- |
| `edgeLabelBackground` | `#FFFFFF` | Matches canvas — hides the grey label box. `transparent` collapses the box and degrades rendering. Not settable via `classDef` or `linkStyle`. |

---

## linkStyle rationale

`linkStyle default color:#0F0E2B` sets edge label text to navy across all links.
Without it, label text color is renderer-dependent and frequently renders white.

---

## accent5 / accent6 — per-node only

accent5 (`#6164EB` violet-blue) and accent6 (`#8E8FEC` periwinkle) have no
subgraph-level role. Apply per-node via `classDef`:

```mermaid
  classDef alt5 fill:#6164EB,color:#FFFFFF,stroke:#0F0E2B
  classDef alt6 fill:#8E8FEC,color:#000000,stroke:#0F0E2B
```

---

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.5        |
| Last Updated | 2026-03-29 |
| Status       | Final      |
