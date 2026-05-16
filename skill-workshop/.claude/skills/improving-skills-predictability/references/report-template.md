# Report template

Render exactly this structure. Replace bracketed tokens. Keep tables intact even if a row's value is `N/A`.

---

# [skill-name] predictability report

Generated: [YYYY-MM-DD HH:MM]
Runs analyzed: [N] — [list run identifiers, e.g., v01..v05]
Substrate: [substrate path]
Analyzed skill: [skill path]
Comparable roles: [list role keys]
Non-comparable roles excluded: [list or "none"]

## Top-line scores

Score is the worst-of across comparable roles. `Worst role` names the role producing it (`all` if tied at the same value across all comparable roles).

| Dimension | Worst role | Score | Reading |
|:--|:--|:--|:--|
| Section structure fidelity | [role] | **~X%** | [one-sentence evidence from the worst role — e.g., "M/M sections rendered identically in K/N runs of the requirements role; one demotion in vXX"] |
| Identifier alignment | [role] | **~X%** | [evidence citing IDs and runs in the worst role] |
| Substrate fidelity — domain concepts | [role] | **~X%** | [evidence — concepts and which runs preserve them in the worst role] |
| Substrate fidelity — schemas | [role] | **~X%** | [evidence — schema name and per-run preservation in the worst role] |
| Substrate fidelity — paths | [role] | **~X%** | [evidence — paths and verbatim status in the worst role] |
| Substrate fidelity — verbatim strings | [role] | **~X%** | [evidence — quoted strings and per-run preservation in the worst role] |
| Substrate fidelity — policies / constraints | [role] | **~X%** | [evidence — modality bundle in the worst role] |
| Modality and surface drift | [role] | **~X%** | [evidence — IDs whose modality changed across runs in the worst role] |
| Naming framing | [role] | **~X%** | [evidence — does the title read from substrate or from slug in the worst role?] |

**Overall predictability — current (measured, worst-of role):**   Substance ≈ **0.XX** · Structure ≈ **0.XX** · Naming ≈ **0.XX** [worst role(s): <list>].
**Overall predictability — projected (after R-001..R-NNN, analytical, worst-of role):** Substance ≈ **0.XX** · Structure ≈ **0.XX** · Naming ≈ **0.XX**.

Per-role aggregate breakdown:

| Role | Substance | Structure | Naming |
|:--|:--|:--|:--|
| [role-1] | 0.XX | 0.XX | 0.XX |
| [role-2] | 0.XX | 0.XX | 0.XX |
| … | … | … | … |

## Section structure fidelity

| Role | Run | Heading sequence delta |
|:--|:--|:--|
| [role-1] | v01 | [list of insertions / deletions / reorderings vs. canonical, or "—"] |
| [role-1] | v02 | … |
| [role-2] | v01 | … |
| … | … | … |

Canonical sequence per role:

- **[role-1]:** [ordered list]
- **[role-2]:** [ordered list]

Notes: [1–3 sentences on the most material structural deviations, noting per-role differences if they diverge].

## Identifier alignment

| Role | Identifier | Coverage (n/N) | Anchor stability | Notes |
|:--|:--|:--|:--|:--|
| [role] | [ID-001] | n/N | stable / drift / split | [evidence] |
| … | … | … | … | … |

Split/fold events: [list (role, IDs) where one run's ID maps to multiple in another, or "none"].

## Substrate fidelity — invariants probed

One row per (invariant, role) cell. An invariant that the analyzed skill never surfaces in a given role across any run is annotated `n/a` rather than `✗` and is excluded from that role's denominator.

| Invariant | Class | Role | Source span | v01 | v02 | v03 | v04 | v05 | … |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| [verbatim or paraphrased anchor] | path / schema / verbatim / concept / policy | [role] | [substrate line range or section] | ✓ / ≈ / ✗ / n/a | … | … | … | … | … |

Legend: ✓ verbatim · ≈ semantic match · ✗ missing or distorted · n/a invariant not expected in this role.

## Modality and surface drift

| Role | Identifier | Statement (anchor) | v01 | v02 | v03 | v04 | v05 |
|:--|:--|:--|:--|:--|:--|:--|:--|
| [role] | [ID] | [short anchor of the statement] | MUST | SHOULD | MUST | MUST | MAY |

Surface drift (semantic-equivalent rewordings worth flagging, scoped per role): [bullet list or "none"].

## Statement counts per category

One table per comparable role.

### Role: [role-1]

| Category | v01 | v02 | v03 | v04 | v05 | min | max | mean |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| [category] | n | n | n | n | n | n | n | n.n |
| … | … | … | … | … | … | … | … | … |

### Role: [role-2]

| Category | v01 | v02 | v03 | v04 | v05 | min | max | mean |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| [category] | n | n | n | n | n | n | n | n.n |
| … | … | … | … | … | … | … | … | … |

(Repeat per comparable role.)

## Naming framing finding

Substrate names this work: **"[canonical name from substrate]"** (source: [substrate location]).

| Role | Run | Title used | Framing |
|:--|:--|:--|:--|
| [role-1] | v01 | [title] | substrate / slug-literal / hybrid |
| [role-1] | v02 | … | … |
| [role-2] | v01 | … | … |
| … | … | … | … |

Finding: [one paragraph — whether runs read framing from substrate or from slug, with per-role notes if roles diverge; cite contrary evidence if the original premise was wrong].

## Per-file deviation summary

For each run, list 1–3 lines per role. At minimum, one line per (dimension, role) where this run is the outlier.

### v01

- **[role-1]:** [1–3 lines on what is distinctive about this run's file in this role]
- **[role-2]:** …

### v02

- **[role-1]:** …
- **[role-2]:** …

(Continue for every run.)

### Non-comparable roles

[List any roles present in < ⌈N/2⌉ runs, with the run identifiers where they appear, or "none". Excluded from scoring per SKILL.md Phase 0 comparability filter.]

## Predictability verdict

[Two to four sentences. State which (dimension, role) cell is the dominant source of variance, name the single highest-leverage fix, and note any (dimension, role) cell where runs are already at ≥95%. If the worst role differs across Substance / Structure / Naming, name each worst role explicitly.]

## Recommendations

*Stress test method: analytical projection — recommendations were applied to the recorded deviations from Phase 3 to estimate their effect. No re-runs were performed.*

### R-001 — [one-line title]     [projected lift: +N pts]
- Targets: [(dimension, role) cells, or "dimension X across all roles"]
- Statement: [imperative, one or two sentences]
- Rationale: [which observed deviations it would have prevented]
- Projected effect: prevented [A], partial [B], unaffected [C], regressed [D]
- Risk: [one sentence]

### R-002 — …

(Continue in ranked order. Highest projected lift first.)

| Field        | Value       |
|--------------|-------------|
| Version      | 1.x         |
| Last Updated | YYYY-MM-DD  |
| Status       | Draft       |
