---
name: improving-skills-predictability
description: Measures the output predictability of a Claude skill across multiple runs on a shared substrate and produces stress-tested recommendations to reduce variance. Use this skill whenever the user wants to audit how consistent a skill's outputs are run-to-run, compare N versioned outputs (e.g., `<slug>-v01` through `<slug>-vNN`) against the substrate that produced them, diagnose where a skill drifts (structure, identifiers, modality, verbatim invariants, naming), or get prioritized recommendations to harden the skill's prompt. Required inputs are the outputs directory (≥5 runs), the skill being analyzed, and the substrate file. Output is a single markdown report under `<CLAUDE.md parent dir>/predictability/<skill-name>/`. Generic — not limited to requirements-style outputs.
allowed-tools:
  - Read
  - Write
  - Bash
---

# improving-skills-predictability

QA assistant for skill engineering. Given N runs of the same skill on the same substrate, it quantifies how predictable the outputs are along several dimensions, produces a single markdown report, and ranks stress-tested recommendations by projected predictability lift.

The skill is read-only on the analyzed skill and its outputs. It writes exactly one file: the report.

## Reference files

| File | Load at | Condition |
|:--|:--|:--|
| `references/report-template.md` | Phase 5 | Always |
| `references/scoring.md` | Phase 4 | Always |
| `references/invariant-extraction.md` | Phase 2 | Always |
| `references/recommendations-catalog.md` | Phase 6 | Always |
| `references/summary.md` | Phase 5 + Phase 7 close | Always |

## Invocation

All four arguments are mandatory. The skill follows two paths depending on how the user invokes it:

- **Fast path** — every argument is provided on the command line and passes lightweight validation. Echo the resolved values and proceed; no per-argument user gate fires. The discovered-artifacts auto-confirm rule in Phase 0 step 3 may still suppress the only remaining gate, yielding a fully gate-free run.
- **Gated path** — any argument is missing, or any provided argument fails validation. For each such argument the skill scans cwd, ranks plausible candidates, and asks the user to confirm. No auto-accept — the user must confirm every proposed value even when there is a single high-confidence candidate. Arguments that were provided and passed validation are not re-proposed.

```
improving-skills-predictability --outputs <dir> --skill <path> --substrate <path> [--files <glob[,glob...]>]
```

| Argument | Rule | On failure |
|:--|:--|:--|
| `--outputs` | Directory containing ≥5 output runs. Each run is either a sibling subdirectory (e.g., `<slug>-v01/`, `<slug>-v02/`, …) or a flat set of files differentiated by a `v\d{2}` token in the basename | Scan cwd, propose candidates, confirm |
| `--skill` | Path to the analyzed skill. Accepts either the skill directory or its `SKILL.md` | Scan cwd, propose candidates, confirm |
| `--substrate` | Absolute or cwd-relative path to the substrate `.md` file that fed the runs | Scan cwd, propose candidates, confirm |
| `--files` | Comma-separated glob(s) selecting which files inside each run are compared (e.g., `*-requirements.md,*-report.md`). Use to exclude drafts, notes, READMEs from the sweep | Scan cwd, propose candidates, confirm |

### Auto-proposal flow

Resolution order: `outputs → skill → substrate → files`. Each downstream scan may use already-resolved values to narrow its candidate set (e.g., the substrate scan keys off the outputs slug; the files scan keys off the resolved outputs runs).

**Scan boundaries**
- Root: cwd
- Max depth: 3 levels
- Excludes: `.git/`, `node_modules/`, dotfiles except `.claude/skills/`

**Per-argument candidate definition**

| Argument | Candidate | Ranking |
|:--|:--|:--|
| `--outputs` | A directory holding ≥5 child dirs that share a slug prefix and each carry the v-token regex `(?:^|-)v\d{2}(?=[-./]|$)` | run count desc, then mtime desc |
| `--skill` | Any directory containing a readable `SKILL.md` (search includes `.claude/skills/*/`) | name-match with outputs slug, else alpha |
| `--substrate` | `.md` files near `outputs_dir` and inside any sibling `substrates/` dir whose basename shares ≥3 tokens with the outputs slug | token-overlap score desc |
| `--files` | Shape-B glob set derived from the resolved outputs runs: one entry per detected artifact-key as `*-<artifact>.md`, plus the union of all artifacts, plus `*.md` | most-specific first, `*.md` last |

**UX by candidate count**

| Candidates found | UX |
|:--|:--|
| 0 | Free-text prompt (no proposal possible) |
| 1 | Echo `proposed: <value>` and ask `y / refine / abort` |
| 2–4 | `AskUserQuestion` with each candidate as an option (plus the automatic "Other" escape) |
| 5+ | Top 4 plus an option labelled "show all" — selecting it re-renders the full list |

- `refine` → re-run the scan; the user may supply a narrowing hint (e.g., a partial slug, a sub-path)
- `abort` → exit cleanly, no report written

Echo back all four resolved values before continuing.

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
→ Phase 0 — Pre-flight (scanned cwd, found <N> candidates across <missing args>)
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

1. Resolve `(outputs_dir, skill_path, substrate_path, files_glob)`:
   - **1a — parse provided args.** Read every value passed on the command line.
   - **1b — fast-path validation (only when all four args are provided inline).** Validate each provided value against the rules below. If **all four pass**, skip 1c entirely and jump to 1d — no per-argument gate fires. If **any fail**, mark only the failing arg(s) as unresolved and fall through to 1c for those; provided args that passed stay as-is and are not re-proposed.

     | Argument | Validation |
     |:--|:--|
     | `--outputs` | Path exists, is a directory, is readable |
     | `--skill` | Path exists and resolves to a readable `SKILL.md` (either a directory containing one, or the file itself) |
     | `--substrate` | Path exists, is a regular file, is readable as UTF-8 text |
     | `--files` | Parses as a non-empty comma-separated list of glob patterns; each pattern is syntactically valid |

     Semantic coverage (≥5 runs, ≥1 comparable artifact, glob actually matches files in `outputs_dir`) is checked by run discovery in step 2 and the hard-fail in step 4 — not here. If discovery in step 2 produces 0 comparable artifacts or fewer than 5 runs after a fast-path resolve, fall back to the gated `refine` prompt in step 3 (do not auto-confirm).
   - **1c — for each unresolved arg, scan + propose + confirm.** Walk cwd (depth ≤ 3, exclusions as specified in the Invocation section). Apply the per-argument candidate definition. Present candidates per the UX-by-candidate-count table. Resolve in order `outputs → skill → substrate → files` so each scan can use earlier resolutions. The user must confirm every proposed value; never auto-accept.
   - **1d — echo the four resolved values.** Print `outputs_dir`, `skill_path`, `substrate_path`, `files_glob` before continuing. On the fast path, append the literal tag `fast-path` to the echo line.
2. Discover the runs and their artifacts:
   - **Version-token regex (canonical):** `(?:^|-)v\d{2}(?=[-./]|$)`. A name "carries a version token" iff this regex finds a match.
   - **Run discovery:** if `outputs_dir` contains subdirectories whose names carry a version token, treat each such subdirectory as one run; within each run, the files to compare are those matching any `--files` glob. Otherwise, treat each file in `outputs_dir` matching any `--files` glob whose basename also carries a version token as one run.
   - **Artifact key:** for each comparable file, derive the artifact key by removing every version-token match from the basename (extension preserved) and collapsing any resulting `--` to `-`. Two files share an artifact iff their artifact keys are equal. Pair files across runs by artifact key.
   - **Comparability filter:** an artifact is **comparable** iff it is present in ≥ ⌈N/2⌉ runs (rounded up). Artifacts below threshold are marked `[non-comparable]` in the echo, excluded from every Phase 3 scoring pass, and listed once in the per-file deviation summary. Never silently dropped.
3. Echo the discovery and ask the user to confirm, in this exact shape:
   ```
   Discovered: <N> runs × <M> artifacts (files glob: <glob>)
     Artifacts:
       - <artifact-key>  (present in K/N runs[, missing in vXX, vYY])
       - <artifact-key>  [non-comparable: K/N < ⌈N/2⌉]
       ...
     Runs:
       v01 v02 ...

   Proceed with these artifacts? [y / refine / abort]
   ```
   - `y` (or empty Enter) → continue
   - `refine` → re-prompt the files glob, repeat steps 2–3
   - `abort` → exit cleanly, no report written

   **Auto-confirm condition (strict).** If all three hold:
   (a) M ≥ 1,
   (b) every artifact is present in N/N runs,
   (c) no artifact is flagged `[non-comparable]`,
   then skip the prompt: stream the Discovered block as a one-shot status line, append `auto-confirmed (trivial discovery)`, and continue to step 4 without awaiting user input. No interjection (`refine` / `abort`) is accepted in the auto-confirm path — the next user message is treated as Phase 1 progress. To force the prompt back on, the user must re-invoke with a non-trivial `--files` glob that produces partial coverage or non-comparable artifacts.

   Otherwise (any artifact at K/N < N/N, any `[non-comparable]` row, or M = 0), prompt as above and await explicit user input.
4. If fewer than 5 runs are discovered, hard-fail.
5. Resolve the skill name from the `SKILL.md` frontmatter `name:` field. If absent, fall back to the directory name.
6. Resolve the report destination: `<CLAUDE.md parent dir>/predictability/<skill-name>/<skill-name>-predictability-<YYYYMMDD-HHMM>.md`. Create the directory if missing.

## Phase 1 — Ingest

Read into memory only — no writes yet:

- `SKILL.md` and every file referenced from it (table rows under "Reference files", template paths, examples). Resolve relative paths against the skill directory.
- The substrate file.
- For each run, every comparable artifact selected in Phase 0 (every file matching `--files`, default `*.md`). When a run contains multiple files, pair them across runs by the **artifact key** computed in Phase 0 (basename with all version-token matches removed and `--` collapsed) so that comparisons happen within each artifact, not across artifacts.

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

Run six analyses across the N runs, each applied per comparable artifact independently. Hold all results in memory; do not write until Phase 7.

### 3.1 Section structure fidelity

For each comparable artifact, extract the ordered list of headings (level + text) from every run that carries the artifact. Compute the longest common heading sequence across runs for that artifact. Per-artifact score = (matched headings / max heading count) averaged across runs. Note any demotions, promotions, or reorderings per run. The dimension's top-line score is the minimum across comparable artifacts (worst-of); cite the worst artifact in the evidence cell.

### 3.2 Identifier alignment

Detect identifiers using a generic regex over the analyzed outputs (default: `\b[A-Z]{1,5}-\d{2,4}\b`). Identifiers are scoped per artifact: an ID found in artifact R in some runs but absent from artifact R in others is a coverage gap in R, not in other artifacts. For each (artifact, identifier) pair, compute:

- Coverage: in how many runs does this ID appear in this artifact?
- Anchor stability: does the same ID label the same statement across runs (semantic match, not byte equality)?
- Split/fold events: when one run's ID maps to two IDs in another run (or vice versa).

Per-artifact identifier-alignment score is computed per `references/scoring.md`. The dimension's top-line score is the minimum across comparable artifacts; cite the worst artifact.

### 3.3 Substrate fidelity

For each invariant from Phase 2 and each comparable artifact, check whether each run's file in that artifact carries the invariant:

- Domain concepts → semantic presence (allow paraphrase)
- Schemas → field-set match; flag missing or added fields
- Paths → byte-level verbatim
- Verbatim strings → byte-level verbatim
- Policies / constraints → semantic presence + modality match (separate from Modality drift below, which is about identifiers)

An invariant need not appear in every artifact — only in artifacts where the analyzed skill is expected to surface it. If no artifact in a run carries the invariant, mark it missing for that run. Score per (sub-dimension, artifact); the top-line per sub-dimension is the minimum across comparable artifacts.

### 3.4 Modality and surface drift

For each (artifact, aligned identifier) pair, compare the modality keyword across runs (MUST/SHOULD/MAY/etc.). Flag mismatches. Also record surface drift on the statement text (clause changes that do not alter semantics but signal instability). Per-artifact modality score; top-line is the minimum across comparable artifacts.

### 3.5 Statement counts per category

For each comparable artifact and each run, count the statements that fall into the detected output categories (whatever section labels exist — e.g., FR, CON, NFR, DR, glossary entries, acceptance items). Present as one wide table per artifact, with rows per category, columns per run, and min/max/mean across runs.

### 3.6 Naming framing

For each comparable artifact, determine whether each run derives the topic name from the substrate or from a literal interpretation of the user-supplied slug. Heuristic: extract candidate names from the substrate (titles, key headings, glossary terms) and compare against the title/first heading of the file in that artifact. Flag any run whose framing diverges from the substrate. Per-artifact naming-framing score; top-line is the minimum across comparable artifacts.

### 3.7 Per-file deviation summary

For each run, write a 1–3 line summary of what is distinctive about it — at least one line per major dimension where this run is the outlier.

## Phase 4 — Scoring & verdict

Apply `references/scoring.md` to convert raw findings into per-dimension percentages. The rubric is intentionally coarse (multiples of 5) to avoid false precision.

Top-line score table (always include, even if a row is N/A). Score is the minimum across comparable artifacts (worst-of); `Worst artifact` names the artifact producing it (`all` if tied at the same value across all artifacts):

| Dimension | Source | Worst artifact | Score |
|:--|:--|:--|:--|
| Section structure fidelity | 3.1 | <artifact> | % |
| Identifier alignment | 3.2 | <artifact> | % |
| Substrate fidelity — domain concepts | 3.3 | <artifact> | % |
| Substrate fidelity — schemas | 3.3 | <artifact> | % |
| Substrate fidelity — paths | 3.3 | <artifact> | % |
| Substrate fidelity — verbatim strings | 3.3 | <artifact> | % |
| Substrate fidelity — policies / constraints | 3.3 | <artifact> | % |
| Modality and surface drift | 3.4 | <artifact> | % |
| Naming framing | 3.6 | <artifact> | % |

Verdict at the bottom of the section. Two lines, both required. Aggregates are computed per artifact first, then the verdict reports the worst-of-artifact value:

> Overall predictability — current (measured, worst-of artifact):   Substance ≈ X · Structure ≈ Y · Naming ≈ Z
> Overall predictability — projected (after recommendations, analytical, worst-of artifact): Substance ≈ X' · Structure ≈ Y' · Naming ≈ Z'

For each comparable artifact R: Substance(R) is the mean of all substrate-fidelity sub-dimension scores for R plus identifier alignment for R. Structure(R) is the structure-fidelity score for R. Naming(R) is the naming-framing score for R. The verdict line reports `min over R` for each. The per-artifact breakdown is rendered in the detail sections (see `references/report-template.md`).

The projected line is computed in Phase 6.3 — leave its placeholder values during Phase 4 and fill them after ranking. Phase 5's draft must contain the placeholders so Phase 6.3 can substitute them.

## Phase 5 — Report draft

Render the full report in memory using the exact template in `references/report-template.md`. Section order is fixed:

1. `# <skill-name> predictability report` (plus the standard generated-metadata lines below the H1)
2. `## Summary - Outputs Variance per Dimension` — rendered per `references/summary.md`. Body values for the `Projected` column are placeholders at this phase; Phase 6.3.5 substitutes the final projected values into both the Summary and the Predictability verdict before Phase 7 writes.
3. `## Top-line scores`
4. `## Section structure fidelity`
5. `## Identifier alignment`
6. `## Substrate fidelity — invariants probed`
7. `## Modality and surface drift`
8. `## Statement counts per category`
9. `## Naming framing finding`
10. `## Per-file deviation summary`
11. `## Predictability verdict`
12. `## Recommendations` (populated in Phase 6)
13. Version block

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

Substitute the placeholder values in two places before Phase 7 writes:
- the `## Predictability verdict` section's projected line (both verdict lines, current + projected, must appear in the final report);
- the `Projected` column of the `## Summary - Outputs Variance per Dimension` table, per the row→dimension mapping in `references/summary.md`. Comments cells that name a recommendation (e.g., `R-001 anchors IDs to substrate byte position`) are filled now, since the ranked IDs are finalised.

A dimension currently at 100% stays at 100%. A dimension that no recommendation targets stays at its current score. Never project above 100%.

### 6.4 Dependency annotation

For each ranked recommendation, scan the others and emit one `Dependencies / Overlap` line citing the related IDs and the relationship type. The line is rendered as the last bullet of the recommendation body (after `Risk`).

| Type | Meaning |
|:--|:--|
| `requires` | This R's projected lift assumes another R is also applied |
| `additive` | Same dimension; lifts compound (clamped at 100%) |
| `overlaps` | Partially same drift; combined lift < sum of individual lifts |
| `supersedes` | This R makes another redundant |
| `tension` | This R pushes against another (applying both narrows or reverses one's lift) |
| `independent` | No interaction with any other R |

Format:

```
- Dependencies / Overlap: <type> with R-XXX — <one-sentence relationship>; <type> with R-YYY — <one-sentence>
```

If no relationship to any other R, emit exactly:

```
- Dependencies / Overlap: independent
```

The annotation is a static pass over the ranked list — it does not change scores, ranks, or the projected aggregates already finalised in 6.3 / 6.3.5. No user gate. Phase 7 fires immediately after the last recommendation is annotated.

## Phase 7 — Write

Write exactly one file:

```
<CLAUDE.md parent dir>/predictability/<skill-name>/<skill-name>-predictability-<YYYYMMDD-HHMM>.md
```

The file must end with the version block required by the workspace CLAUDE.md.

After the write succeeds, stream the `## Summary - Outputs Variance per Dimension` block (table + model-attribution paragraph, per `references/summary.md`) to chat as the closing tokens of the run. The on-disk and chat renderings of the Summary are byte-identical; no other commentary appears between the `✓ Wrote …` line and the Summary block.

## Operational notes

- Stateless. Two consecutive runs on the same inputs may produce slightly different recommendation wording but identical scores within ±5 points per (dimension, artifact) cell. The top-line worst-of score may shift by more than 5 points only when the worst artifact flips between runs — call this out explicitly in the report when it happens. Differences beyond these tolerances are themselves a finding worth reporting.
- The report is the only artifact. Do not modify the analyzed skill or its outputs.
- The analytical projection is a projection, not a measurement. The report must state this explicitly in the `## Recommendations` preamble.
- When the substrate is large (>2000 lines), summarize the invariant set in the report rather than enumerating; keep evidence citations to the most discriminating ones.
- All numbers in the report are evidence-backed. A score with no evidence row is treated as a hard-fail in Phase 4.
- No scratch work in the output. The final report must not contain self-correction notes such as `(check)`, `(verify)`, `(TODO)`, `(unsure)`, parenthetical hedges directed at the reader, or any other in-line marker of analytical doubt. Either resolve the uncertainty before writing, or surface it as a one-sentence note in the relevant section. The reader is not a reviewer of the analyst's thinking — only of the result.

| Field        | Value       |
|--------------|-------------|
| Version      | 1.11        |
| Last Updated | 2026-05-16  |
| Status       | Draft       |
