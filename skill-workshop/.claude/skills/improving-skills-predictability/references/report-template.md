# Report template

Render exactly this structure. Replace bracketed tokens. Keep tables intact even if a row's value is `N/A`.

---

# [skill-name] predictability report

Generated: [YYYY-MM-DD HH:MM]
Runs analyzed: [N] — [list run identifiers, e.g., v01..v05]
Substrate: [substrate path]
Analyzed skill: [skill path]

## Top-line scores

| Dimension | Score | Reading |
|:--|:--|:--|
| Section structure fidelity | **~X%** | [one-sentence evidence — e.g., "M/M sections rendered identically and in order in K/N runs; one demotion in vXX"] |
| Identifier alignment | **~X%** | [evidence citing IDs and runs] |
| Substrate fidelity — domain concepts | **~X%** | [evidence — list 2–4 key concepts and which runs preserve them] |
| Substrate fidelity — schemas | **~X%** | [evidence — schema name + which runs altered it] |
| Substrate fidelity — paths | **~X%** | [evidence — list 2–4 paths and verbatim status] |
| Substrate fidelity — verbatim strings | **~X%** | [evidence — quoted strings and per-run preservation] |
| Substrate fidelity — policies / constraints | **~X%** | [evidence — modality bundle and divergences] |
| Modality and surface drift | **~X%** | [evidence — IDs whose modality changed across runs] |
| Naming framing | **~X%** | [evidence — does the title read from substrate or from slug?] |

**Overall predictability — current (measured):**   Substance ≈ **0.XX** · Structure ≈ **0.XX** · Naming ≈ **0.XX**.
**Overall predictability — projected (after R-001..R-NNN, analytical):** Substance ≈ **0.XX** · Structure ≈ **0.XX** · Naming ≈ **0.XX**.

## Section structure fidelity

| File role | Run | Heading sequence delta |
|:--|:--|:--|
| [file-role-1] | v01 | [list of insertions / deletions / reorderings vs. canonical, or "—"] |
| [file-role-1] | v02 | … |
| … | … | … |

Canonical sequence (longest common): [ordered list]

Notes: [1–3 sentences on the most material structural deviations].

## Identifier alignment

| Identifier | Coverage (n/N) | Anchor stability | Notes |
|:--|:--|:--|:--|
| [ID-001] | n/N | stable / drift / split | [evidence] |
| … | … | … | … |

Split/fold events: [list IDs where one run's ID maps to multiple in another, or "none"].

## Substrate fidelity — invariants probed

| Invariant | Class | Source span | v01 | v02 | v03 | v04 | v05 | … |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| [verbatim or paraphrased anchor] | path / schema / verbatim / concept / policy | [substrate line range or section] | ✓ / ≈ / ✗ | … | … | … | … | … |

Legend: ✓ verbatim · ≈ semantic match · ✗ missing or distorted.

## Modality and surface drift

| Identifier | Statement (anchor) | v01 | v02 | v03 | v04 | v05 |
|:--|:--|:--|:--|:--|:--|:--|
| [ID] | [short anchor of the statement] | MUST | SHOULD | MUST | MUST | MAY |

Surface drift (semantic-equivalent rewordings worth flagging): [bullet list or "none"].

## Statement counts per category

| Category | v01 | v02 | v03 | v04 | v05 | min | max | mean |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| [category] | n | n | n | n | n | n | n | n.n |
| … | … | … | … | … | … | … | … | … |

## Naming framing finding

Substrate names this work: **"[canonical name from substrate]"** (source: [substrate location]).

| Run | Title used | Framing |
|:--|:--|:--|
| v01 | [title] | substrate / slug-literal / hybrid |
| … | … | … |

Finding: [one paragraph — whether runs read framing from substrate or from slug; cite contrary evidence if the original premise was wrong].

## Per-file deviation summary

### v01
- [1–3 lines on what is distinctive about this run, at minimum one line per dimension it leads or lags]

### v02
- …

(Continue for every run.)

## Predictability verdict

[Two to four sentences. State which dimension is the dominant source of variance, name the single highest-leverage fix, and note any dimension where runs are already at ≥95%.]

## Recommendations

*Stress test method: analytical projection — recommendations were applied to the recorded deviations from Phase 3 to estimate their effect. No re-runs were performed.*

### R-001 — [one-line title]     [projected lift: +N pts]
- Targets: [dimensions]
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
