---
name: improving-skill-predictability
description: Measures the output predictability of a Claude skill across multiple runs on a shared substrate and produces stress-tested recommendations to reduce variance. Use this skill whenever the user wants to audit how consistent a skill's outputs are run-to-run, compare N versioned outputs (e.g., `<slug>-v01` through `<slug>-vNN`) against the substrate that produced them, diagnose where a skill drifts (structure, identifiers, modality, verbatim invariants, naming), or get prioritized recommendations to harden the skill's prompt. Required inputs are the outputs directory (≥5 runs), the skill being analyzed, and the substrate file. Output is a single markdown report under `<CLAUDE.md parent dir>/predictability/<skill-name>/`. Generic — not limited to requirements-style outputs.
allowed-tools:
  - Read
  - Write
  - Bash
---

# improving-skill-predictability

QA assistant for skill engineering. Given N runs of the same skill on the same substrate, it quantifies how predictable the outputs are along several dimensions, produces a single markdown report, and ranks stress-tested recommendations by projected predictability lift.

The skill is read-only on the analyzed skill and its outputs. It writes exactly one file: the report.

## Reference files

| File | Load at | Condition |
|:--|:--|:--|
| `references/report-template.md` | Phase 5 | Always |
| `references/scoring.md` | Phase 4 | Always |
| `references/invariant-extraction.md` | Phase 2 | Always |
| `references/recommendations-catalog.md` | Phase 6 | Always |

## Invocation

Hybrid: arguments parsed when present, interactive prompts for anything missing.

```
improving-skill-predictability --outputs <dir> --skill <path> --substrate <path>
```

| Argument | Rule | On failure |
|:--|:--|:--|
| `--outputs` | Directory containing ≥5 output runs. Each run is either a sibling subdirectory (e.g., `<slug>-v01/`, `<slug>-v02/`, …) or a flat set of `.md` files differentiated by a trailing `v\d{2}` token | Interactive prompt |
| `--skill` | Path to the analyzed skill. Accepts either the skill directory or its `SKILL.md` | Interactive prompt |
| `--substrate` | Absolute or cwd-relative path to the substrate `.md` file that fed the runs | Interactive prompt |

If invoked without arguments, ask in this order: outputs dir → skill path → substrate path. Echo back the resolved triple before continuing.

## Hard prerequisites

- ≥ 5 distinct output runs are required. Fewer runs cannot produce a meaningful predictability signal — hard-fail with remediation: "Provide at least 5 runs in `--outputs`; found N."
- The substrate must be readable as text. Hard-fail otherwise.
- The skill path must contain a readable `SKILL.md`. Hard-fail otherwise.

## Phase model

| Phase | Name | Produced |
|:--|:--|:--|
| 0 | Pre-flight | (validation only) |
| 1 | Ingest | normalized in-memory corpus: skill files, substrate, N runs |
| 2 | Invariant extraction | substrate invariants set |
| 3 | Cross-output analysis | structure, identifiers, substrate fidelity, modality, naming, counts, per-file deviation |
| 4 | Scoring & verdict | per-dimension scores + top-line table |
| 5 | Report draft | full markdown report rendered in memory |
| 6 | Recommendations & stress test | ranked recommendations appended |
| 7 | Write | one report file emitted |

Stream one header per phase as it begins:

```
→ Phase 0 — Pre-flight
→ Phase 1 — Ingest
→ Phase 2 — Invariant extraction
→ Phase 3 — Cross-output analysis
→ Phase 4 — Scoring & verdict
→ Phase 5 — Report draft
→ Phase 6 — Recommendations & stress test
→ Phase 7 — Write
✓ Wrote <skill-name>-predictability-<YYYYMMDD-HHMM>.md
```

On hard-fail, replace the current phase line and stop:

```
✗ Phase <N> — <name>: <reason>
  context: <relevant path or arg>
  remediation: <one-line suggestion>
```

## Phase 0 — Pre-flight

1. Resolve the triple `(outputs_dir, skill_path, substrate_path)` from arguments or interactive prompts.
2. Discover the runs:
   - If `outputs_dir` contains subdirectories matching `*v\d{2}*`, treat each as one run; expect each run to hold the file(s) to compare (default: every `.md` file inside).
   - Otherwise, treat each `*.md` file in `outputs_dir` whose name carries a `v\d{2}` token as one run.
3. If fewer than 5 runs are discovered, hard-fail.
4. Resolve the skill name from the `SKILL.md` frontmatter `name:` field. If absent, fall back to the directory name.
5. Resolve the report destination: `<CLAUDE.md parent dir>/predictability/<skill-name>/<skill-name>-predictability-<YYYYMMDD-HHMM>.md`. Create the directory if missing.

## Phase 1 — Ingest

Read into memory only — no writes yet:

- `SKILL.md` and every file referenced from it (table rows under "Reference files", template paths, examples). Resolve relative paths against the skill directory.
- The substrate file.
- For each run, every comparable artifact (default: all `.md` files in the run). When a run contains multiple files, pair them across runs by basename (strip the version token) so that comparisons happen within file roles, not across roles.

If a run is missing a file that other runs have, do not abort — record it as a per-file deviation ("file missing in run vX") and continue.

## Phase 2 — Invariant extraction

Walk the substrate and extract the set of invariants that downstream runs are expected to preserve. Categories are not hard-coded — detect what is actually there. See `references/invariant-extraction.md` for the heuristics. The five generic invariant classes are:

| Class | Detection |
|:--|:--|
| Domain concepts | named entities, model nouns, capitalized multi-word phrases, defined glossary terms |
| Schemas | fenced code blocks tagged `json`, `yaml`, `xml`, `mermaid`, or any block presenting field lists |
| Paths | filesystem paths, URI patterns, anchors, route literals |
| Verbatim strings | quoted strings, prompt fragments, error messages |
| Policies / constraints | sentences carrying modal verbs (MUST/SHOULD/MAY/WILL/SHALL or their lowercase equivalents) |

Each invariant is stored with its source span so the report can cite it.

## Phase 3 — Cross-output analysis

Run six analyses across the N runs. Hold all results in memory; do not write until Phase 7.

### 3.1 Section structure fidelity

For each file role, extract the ordered list of headings (level + text). Compute the longest common heading sequence across runs. Score = (matched headings / max heading count) averaged across runs. Note any demotions, promotions, or reorderings per run.

### 3.2 Identifier alignment

Detect identifiers using a generic regex over the analyzed outputs (default: `\b[A-Z]{1,5}-\d{2,4}\b`). For each identifier seen anywhere, compute:

- Coverage: in how many runs does this ID appear?
- Anchor stability: does the same ID label the same statement across runs (semantic match, not byte equality)?
- Split/fold events: when one run's ID maps to two IDs in another run (or vice versa).

### 3.3 Substrate fidelity

For each invariant from Phase 2, check whether each run carries it:

- Domain concepts → semantic presence (allow paraphrase)
- Schemas → field-set match; flag missing or added fields
- Paths → byte-level verbatim
- Verbatim strings → byte-level verbatim
- Policies / constraints → semantic presence + modality match (separate from Modality drift below, which is about identifiers)

### 3.4 Modality and surface drift

For each aligned identifier, compare its modality keyword across runs (MUST/SHOULD/MAY/etc.). Flag mismatches. Also record surface drift on the statement text (clause changes that do not alter semantics but signal instability).

### 3.5 Statement counts per category

For each run, count the statements that fall into the detected output categories (whatever section labels exist — e.g., FR, CON, NFR, DR, glossary entries, acceptance items). Present as a wide table with one row per category and one column per run, with min/max/mean across runs.

### 3.6 Naming framing

Determine whether each run derives the topic name from the substrate or from a literal interpretation of the user-supplied slug. Heuristic: extract candidate names from the substrate (titles, key headings, glossary terms) and compare against the title/first heading of each run. Flag any run whose framing diverges from the substrate.

### 3.7 Per-file deviation summary

For each run, write a 1–3 line summary of what is distinctive about it — at least one line per major dimension where this run is the outlier.

## Phase 4 — Scoring & verdict

Apply `references/scoring.md` to convert raw findings into per-dimension percentages. The rubric is intentionally coarse (multiples of 5) to avoid false precision.

Top-line score table (always include, even if a row is N/A):

| Dimension | Source | Score |
|:--|:--|:--|
| Section structure fidelity | 3.1 | % |
| Identifier alignment | 3.2 | % |
| Substrate fidelity — domain concepts | 3.3 | % |
| Substrate fidelity — schemas | 3.3 | % |
| Substrate fidelity — paths | 3.3 | % |
| Substrate fidelity — verbatim strings | 3.3 | % |
| Substrate fidelity — policies / constraints | 3.3 | % |
| Modality and surface drift | 3.4 | % |
| Naming framing | 3.6 | % |

Verdict at the bottom of the section. Two lines, both required:

> Overall predictability — current (measured):   Substance ≈ X · Structure ≈ Y · Naming ≈ Z
> Overall predictability — projected (after recommendations, analytical): Substance ≈ X' · Structure ≈ Y' · Naming ≈ Z'

Substance is the mean of all substrate-fidelity rows + identifier alignment. Structure is the structure-fidelity score. Naming is the naming-framing score.

The projected line is computed in Phase 6.3 — leave its placeholder values during Phase 4 and fill them after ranking. Phase 5's draft must contain the placeholders so Phase 6.3 can substitute them.

## Phase 5 — Report draft

Render the full report in memory using the exact template in `references/report-template.md`. Section order is fixed:

1. `# <skill-name> predictability report`
2. `## Top-line scores`
3. `## Section structure fidelity`
4. `## Identifier alignment`
5. `## Substrate fidelity — invariants probed`
6. `## Modality and surface drift`
7. `## Statement counts per category`
8. `## Naming framing finding`
9. `## Per-file deviation summary`
10. `## Predictability verdict`
11. `## Recommendations` (populated in Phase 6)
12. Version block

Every score must be accompanied by a one-sentence reading that cites concrete evidence (which run, which heading, which identifier). Numbers without evidence are not allowed.

## Phase 6 — Recommendations & stress test

### 6.1 Draft initial recommendations

Read every dimension where the score is below 95% and propose a candidate recommendation targeted at that gap. Pull recurring patterns from `references/recommendations-catalog.md`. Recommendations are about the **skill prompt** — not about post-hoc validation of outputs. Examples of valid recommendation shapes:

- Pin a verbatim string verbatim in the skill ("the prompt must read `Which project?` exactly")
- Promote a SHOULD to a MUST (only with explicit justification tied to the observed drift)
- Add a section ordering invariant
- Split or merge a category that runs disagree about
- Add an explicit re-read step for a substrate concept that some runs paraphrase away

Each recommendation has:

| Field | Content |
|:--|:--|
| ID | `R-001`, `R-002`, … |
| Targets | which dimension(s) it addresses |
| Statement | imperative, one or two sentences |
| Rationale | which deviations it would have prevented |
| Risk | what predictability or quality it might trade off |

### 6.2 Stress test (analytical projection)

For each candidate recommendation, walk back through the deviations recorded in Phase 3 and label each one:

- `prevented` — recommendation, if it had been in the skill, would have eliminated this deviation
- `partial` — recommendation would have narrowed the deviation but not eliminated it
- `unaffected` — deviation would still occur
- `regressed` — recommendation would have introduced a new deviation (e.g., over-constraining a section that legitimately varies with substrate)

Recompute the per-dimension scores under the assumption that `prevented` deviations are removed and `partial` count for half. Do not re-run the skill — this is an analytical projection, and the report must say so.

### 6.3 Rank

Rank recommendations by projected total lift = sum of per-dimension score deltas, weighted equally. Ties broken by lower risk first. After ranking, renumber the recommendations sequentially `R-001`, `R-002`, …, `R-NNN` in rank order — the IDs assigned during Phase 6.1 are scratch and must not appear in the final report. The highest-lift recommendation is `R-001`.

Output the ranked list and write it to the `## Recommendations` section of the report with this shape:

```
### R-00X — <one-line title>     [projected lift: +N pts]
- Targets: <dimensions>
- Statement: …
- Rationale: …
- Projected effect: prevented A, partial B, unaffected C, regressed D
- Risk: …
```

### 6.3.5 Projected aggregate

After ranking, compute the projected per-dimension percentages by walking the recommendations and applying their lifts to the current scores (rules in `references/scoring.md` — Projected aggregates). From the updated per-dimension percentages, compute the projected Substance / Structure / Naming aggregates using the same formulas as the current state.

Substitute the placeholder values in the `## Predictability verdict` section's projected line. Both verdict lines (current + projected) must appear in the final report.

A dimension currently at 100% stays at 100%. A dimension that no recommendation targets stays at its current score. Never project above 100%.

### 6.4 User confirmation

Before writing the report, surface the ranked recommendations to the user and ask:

> "Keep all N recommendations in the report, drop some, or edit any?"

Apply the user's response. The user's edits are absorbed silently; do not annotate the report with "user-modified".

## Phase 7 — Write

Write exactly one file:

```
<CLAUDE.md parent dir>/predictability/<skill-name>/<skill-name>-predictability-<YYYYMMDD-HHMM>.md
```

The file must end with the version block required by the workspace CLAUDE.md.

## Operational notes

- Stateless. Two consecutive runs on the same inputs may produce slightly different recommendation wording but identical scores within ±5 points. If scores differ by more than 5 points across consecutive runs on identical inputs, that itself is a finding worth reporting.
- The report is the only artifact. Do not modify the analyzed skill or its outputs.
- The analytical projection is a projection, not a measurement. The report must state this explicitly in the `## Recommendations` preamble.
- When the substrate is large (>2000 lines), summarize the invariant set in the report rather than enumerating; keep evidence citations to the most discriminating ones.
- All numbers in the report are evidence-backed. A score with no evidence row is treated as a hard-fail in Phase 4.
- No scratch work in the output. The final report must not contain self-correction notes such as `(check)`, `(verify)`, `(TODO)`, `(unsure)`, parenthetical hedges directed at the reader, or any other in-line marker of analytical doubt. Either resolve the uncertainty before writing, or surface it as a one-sentence note in the relevant section. The reader is not a reviewer of the analyst's thinking — only of the result.

| Field        | Value       |
|--------------|-------------|
| Version      | 1.2         |
| Last Updated | 2026-05-15  |
| Status       | Draft       |
