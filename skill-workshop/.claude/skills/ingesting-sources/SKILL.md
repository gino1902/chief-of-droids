---
name: ingesting-sources
description: Ingest one named source file from ./raw/ into the wiki through the governed pipeline. Extracts claims, entities, concepts, definitions, relationships, contradictions, and open questions; maps them to existing pages; applies contradiction policies; emits a four-table report for row-level approval; then mutates pages + index.md + log.md and commits. Invoke as `/ingesting-sources <raw-filename>` for a new or additional source, or `/ingesting-sources <raw-filename> --reingest` to correct source metadata. User-triggered only. Reads exactly the one named file; never lists or scans ./raw/.
disable-model-invocation: true
argument-hint: <raw-filename> [--reingest]
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash(git add *)
  - Bash(git commit *)
  - Bash(git status *)
  - Bash(git diff *)
  - Bash(git log *)
---

<!-- target-model: claude-opus-4-8 | target-environment: claude-code | snapshot-ref: 2026-05-17 -->

# ingesting-sources

Act as a Knowledge Curation Architect. This skill is the one and only write path into the wiki. It reads a single immutable source, proposes how to integrate it, takes row-level approval, then mutates `./wiki/` and commits. Every claim it writes traces back to a source in `./raw/`.

Read `.claude/rules/page-schema.md` before writing any page. It is the authority for front-matter, provenance lines, footnotes, page types, and naming. This skill never restates that schema. Reason: a second copy of the schema drifts from the first; one authority keeps pages and report consistent.

<operating-invariants>

- **`./raw/` is closed.** Read exactly the one source file named in the trigger. Do not list the directory, read sibling files, or scan `./raw/`. Never write to `./raw/`. Reason: `./raw/` is the immutable ground truth and is ungitted; any stray read or write erodes the one safety boundary the framework has.
- **One pending ingest report at a time.** A whole-wiki lock covers pages, `index.md`, and `log.md`. It releases on Apply (commit) or Cancel. Refuse to start a new ingest while a report is pending. Reason: two open reports race on the same pages and produce a non-deterministic merge.
- **No write before approval.** Phases 0-4 produce no wiki mutation. Pages, `index.md`, and `log.md` change only at Apply (Phase 6).
- **Navigate, do not bulk-load.** Start from `index.md`, identify candidate pages, read only those. Reason: practical quality degrades past roughly 200K-300K tokens, so hierarchical navigation through `index.md` is the access path, not an optimisation.
- **No environment mutation.** Do not install packages, run a package manager, or change the machine to read a source. Use only the tools already available. Reason: an ingest that mutates the machine is non-reproducible and varies its own extraction method run to run; a source that cannot be read with available tools is a clean hard-fail, not a setup task.

</operating-invariants>

<reasoning-output-contract>

Reason internally through extraction, mapping, and policy classification. Emit only the phase-header lines, the four-table report, and the apply/cancel confirmations. Do not include reasoning narration in the output. Reason: uncontrolled chain-of-thought leaks into the conversational report and corrupts the row tables the user approves against.

</reasoning-output-contract>

<conversational-adaptation>

The framework spec assumes an interactive report artefact with per-row controls. Claude Code has no such surface, so the report is rendered as conversational markdown and approval is taken as a prompt exchange. The four tables, the row-ID grammar, and the approval verbs are defined in `references/report-and-approval.md`. This is the only deviation from the spec; the row-level approve / edit / reject semantics are preserved exactly.

</conversational-adaptation>

<reference-files>

| File | Load at | Condition |
|---|---|---|
| `.claude/rules/page-schema.md` | Phase 1 | Always (page shape authority) |
| `references/policies.md` | Phase 3 | Always |
| `references/report-and-approval.md` | Phase 4 | Always |
| `references/applying-the-report.md` | Phase 6 | Always |
| `references/reingest.md` | Phase 0 | `--reingest` mode only |

</reference-files>

<invocation>

```
/ingesting-sources <raw-filename> [--reingest]
```

| Argument | Rule | On failure |
|---|---|---|
| `<raw-filename>` | First token after the skill name. The exact filename inside `./raw/`, with extension. No path, no glob, no directory. | Hard-fail |
| `--reingest` | Optional flag. Switches to the source-metadata correction path (`references/reingest.md`). | — |

If no filename is supplied, hard-fail and ask the user to name the one source to ingest. Reason: inferring a filename would require listing `./raw/`, which the closed-`./raw/` invariant forbids.

</invocation>

<phase-model>

| Phase | Name | Produces |
|---|---|---|
| 0 | Pre-flight | posture echo, lock acquired, mode resolved |
| 1 | Read & extract | extraction set from the one source |
| 2 | Map to wiki | candidate target pages (read only those) |
| 3 | Policy & conflict | per-row actions, conflicts, collisions, depends-on |
| 4 | Report | four tables + editable `log.md` entry preview |
| 5 | Approval | row-level approve / edit / reject |
| 6 | Apply or Cancel | mutate + commit + release lock, or release lock only |

Stream one header line per phase as it begins:

```
→ Phase 0 — Pre-flight
→ Phase 1 — Read & extract
→ Phase 2 — Map to wiki
→ Phase 3 — Policy & conflict
→ Phase 4 — Report
(await approval)
→ Phase 6 — Apply
✓ Committed <subject>; lock released
```

On hard-fail, replace the current phase line and stop:

```
✗ Phase <N> — <name>: <reason>
  context: <relevant arg or path>
  remediation: <one-line suggestion>
```

</phase-model>

<phase-0-preflight>

## Phase 0 — Pre-flight

1. Parse the trigger: extract `<raw-filename>` and the optional `--reingest` flag. If no filename, hard-fail.
2. Echo the `./raw/` posture reminder verbatim, substituting the filename:

   > Note: raw/ is not under git. Source file '<raw-filename>' exists only on your local disk. Ensure it is backed up separately if you rely on it.

3. Acquire the wiki lock: confirm no ingest report is pending in this session. If one is, hard-fail and tell the user to Apply or Cancel it first.
4. If `--reingest`, load `references/reingest.md` and follow it from here. Otherwise continue.

</phase-0-preflight>

<phase-1-read-extract>

## Phase 1 — Read & extract

Read exactly `./raw/<raw-filename>`. This read prompts you for confirmation (the `raw/` ask rule); approve the single named file only.

Extract, holding the result in memory (no writes yet): every distinct claim, entity, concept, definition, relationship, contradiction with what the source itself states, and open question, plus the source's own metadata (`source_title`, `issued_date`). Record the `issued_date` for the newer-wins policy.

Determine `issued_date` strictly from the source's stated content, per the precedence in `.claude/rules/page-schema.md`: an explicit date in the content, else a content-stated year (e.g. a copyright year), else `unknown`. Never read it from file or container metadata (PDF CreationDate/ModDate, file mtime); at most surface a metadata date as a flagged candidate in the report. Reason: file metadata and the stated publication date disagree often enough that taking metadata silently makes the field vary run to run.

Scope of effort: extract every distinct claim and entity the source asserts; do not summarise or sample. Stop only when the source yields no new item. Reason: the wiki's value is completeness of grounded claims; sampling silently drops claims the user expected to be captured.

Failure modes:
- If `<raw-filename>` is empty (0 bytes) or yields no extractable item, hard-fail with reason `empty_source`. Do not fabricate items.
- If the source cannot be read with the tools already available (for example a PDF the reader cannot open), hard-fail with reason `unreadable_source`. State what is missing and that the user should supply a readable form or install the dependency out-of-band. Do not install software or improvise an alternative reader. Reason: a per-run improvised reader gives a different extraction each run; a clean hard-fail is deterministic.
- For a quantitative source with no printed values (e.g. a chart with unlabelled bars), transcribe the labelled structure exactly and mark each unreadable figure `unknown` or approximate. Do not fabricate precise numbers.
- If the title or issue date is not determinable from content, mark it `unknown` and surface that in the report. Do not guess.

</phase-1-read-extract>

<phase-2-map>

## Phase 2 — Map to wiki

Read `./wiki/index.md`. If it does not exist, this is the first ingest into an empty wiki; treat every extracted item as a creation. Otherwise, identify candidate target pages from the index (by title, aliases, tags, description) and read only those pages, issuing the candidate-page reads in parallel since they are independent. Determine for each extracted item whether it lands on an existing page, needs a new page, or conflicts with existing content. Apply the entity / concept / synthesis boundary heuristic from the page-schema rule when proposing new pages.

</phase-2-map>

<phase-3-policy>

## Phase 3 — Policy & conflict

Load `references/policies.md`. Apply it to assign each item a destination and action, classify conflicts (`replace` / `supersede` / `coexist` / `do not add`) under the newer-wins heuristic, detect slug collisions and propose disambiguation or merge, and declare cross-row `Depends on`.

If a claim's meaning or a conflict's classification is uncertain, flag the row ⚠️ and state the uncertainty in `Description`. Do not pick a class silently. Reason: a silently-chosen class is a hidden guess the user cannot review; the flag turns it into a decision they can make.

</phase-3-policy>

<phase-4-report>

## Phase 4 — Report

Load `references/report-and-approval.md`. Render the four tables (Modifications, Creations, Conflicts, Link updates) plus the editable `log.md` entry preview, as conversational markdown with stable RowIDs. Then stop and wait for the user's row-level decisions before doing anything else.

</phase-4-report>

<phase-5-approval>

## Phase 5 — Approval

Take the user's row-level decisions using the approval grammar in `references/report-and-approval.md`. Apply edits to the affected rows and re-show changed rows if the edits are non-trivial. The user ends with `Apply` or `Cancel`.

</phase-5-approval>

<phase-6-apply>

## Phase 6 — Apply or Cancel

Load `references/applying-the-report.md`.

- **Cancel:** release the lock, make no mutations, confirm nothing changed.
- **Apply:** run the dangling-reference check across the approved set first. If it fails, block and report the dangling rows for the user to resolve; make no mutation. If it passes, mutate pages, regenerate `index.md`, append the `log.md` entry, then make one atomic git commit (auto-generated subject + the `log.md` entry as body). Release the lock and confirm.

Write only the content authorised by an approved row. Do not add sections, prose, or links that no approved row covers. Reason: unrequested additions bypass the row-level review that is the whole control surface of this pipeline. Run the four mutation steps strictly serially in the order given in the reference; they are not independent.

</phase-6-apply>

| Field | Value |
|---|---|
| Version | 1.2 |
| Last Updated | 2026-05-31 |
| Status | Draft |
| Target Model | claude-opus-4-8 |
| Target Environment | claude-code |
