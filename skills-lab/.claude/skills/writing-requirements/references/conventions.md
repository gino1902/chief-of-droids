# Conventions

## Contents
- ID convention
- Report format
- Severity model
- Failure model
- Substrate-gap defaults
- Iteration model

---

## ID convention

| Element | Rule |
|:--|:--|
| Format | `<CATEGORY>-NNN` — three-digit zero-padded (e.g. `FR-001`, `NFR-012`) |
| IR split | Inbound: `IR-IN-NNN`; Outbound: `IR-OUT-NNN` |
| Sequence | Per-category, starting at `001` |
| Gaps | Allowed when a prior pass deletes an ID; vacated slots are not tombstoned |
| Renumbering | Never automatic; user-driven only |
| Duplicates | Not permitted within a category |

**Category prefixes:**

| Prefix | Section | Skeleton |
|:--|:--|:--|
| `FR` | Functional Requirements | S1 + S2 |
| `FR` | Constraints (S1 only — shares FR sequence) | S1 |
| `CON` | Constraints | S2 |
| `IR-IN` | Interface Requirements — Inbound | S2 |
| `IR-OUT` | Interface Requirements — Outbound | S2 |
| `DR` | Data Requirements | S2 |
| `TR` | Transformation Requirements | S2 |
| `NFR` | Non-Functional Requirements | S2 |
| `SEC` | Security | S2 |
| `ERR` | Error Handling | S2 |
| `OBS` | Observability | S2 |

**ID stability across iterations:**
The substrate-declared ID regex `\b(FR|CON|IR-IN|IR-OUT|IR|DR|TR|NFR|SEC|ERR|OBS)-\d{3}\b` is scanned in Phase 2. Matched IDs are preserved on output, attached to the nearest requirement-shaped block. Free-form substrate without IDs starts fresh — ID stability is opt-in.

### Canonical ordering for un-IDed substrate

When the substrate carries no `<CAT>-NNN` IDs to preserve, assign IDs deterministically by this walk so that two agents running against the same substrate with the same `--type` produce the same ID-to-content map:

1. Within each category section (FR, CON, IR-IN, IR-OUT, DR, TR, NFR, SEC, ERR, OBS), order requirements by the byte position of the first modal verb (`SHALL`, `MUST`, `SHOULD`, `MAY`) of the requirement-bearing sentence in the substrate file.
2. If two candidate requirements share the same source sentence (compound substrate), split into atomic requirements and order by left-to-right token position of each split.
3. If a substrate sentence forward-references a later sentence, the referenced sentence still takes its own byte-position rank — references do not reorder.
4. Ties broken by alphabetical order of the SHALL-action verb lemma.

**Exclusions from the byte-position walk:**
- Modal verbs inside fenced code blocks (```` ``` ```` … ```` ``` ````) are not counted.
- Modal verbs inside quoted strings ("…" or '…') used as examples or substrate references are not counted.
- Modal verbs in section headings are not counted.

The resulting `(category, sequence)` is deterministic for any fixed substrate text.

---

## Report format

`<slug>-report.md` structure:

```
# Report — <topic-slug>

## Summary

| Severity | Resolved | Unresolved |
|:---------|:--------:|:----------:|
| Blocking |    N     |     M      |
| Warning  |    N     |     M      |
| Info     |    N     |    N/A     |

## Phase 0 — Pre-flight
- [BLOCKING-UNRESOLVED] <description> → <remediation>
- [BLOCKING-RESOLVED] <description> → <remediation>
- [WARNING-UNRESOLVED] <description> → <remediation>
- [WARNING-RESOLVED] <description> → <remediation>
- [INFO] <description>

Outstanding: N blocking, M warnings, K info

## Phase 1 — Framing
...

## Phase 2 — Drafting
...

## Phase 3 — Vocabulary
...

## Phase 4 — Taxonomy hygiene
...

## Phase 5 — Verification
...

## Phase 6 — Format
...

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.x        |
| Last Updated | YYYY-MM-DD |
| Status       | Draft      |
```

**Summary table rules:**

- **Info** — always Resolved; Unresolved is always `N/A`.
- **Warning** — Resolved only if remediation has been fully applied within this pass, leaving no action for the user. Unresolved if any check or gap remains for the user, which includes verification-pending findings (auto-derived glossary entry, inferred scope signal, applied default) as well as unresolved hygiene issues.
- **Blocking** — resolution rules not yet defined; populate Resolved and Unresolved from phase findings.

**Per-finding tag rules:**

Every Blocking and Warning finding emitted in a phase section SHALL carry an explicit resolution state in its tag. The tag prefix encodes severity; the suffix encodes resolution.

| Tag | Meaning |
|:--|:--|
| `[BLOCKING-RESOLVED]` | Blocking finding whose remediation has been applied within this pass |
| `[BLOCKING-UNRESOLVED]` | Blocking finding that requires user action before the artifact is correct |
| `[WARNING-RESOLVED]` | Warning whose remediation has been fully applied within this pass, leaving no action for the user |
| `[WARNING-UNRESOLVED]` | Warning that leaves a real check or gap for the user — including verification-pending findings (auto-derived glossary entry, inferred scope signal, applied default) and unresolved hygiene issues; the artifact cannot be considered correct until the user acts |
| `[INFO]` | Trace event; always implicitly resolved — no suffix |

Bare `[BLOCKING]` or `[WARNING]` tags (without a `-RESOLVED` / `-UNRESOLVED` suffix) are not permitted on output.

Counts in the §Summary table SHALL agree with the suffix tallies in phase sections: the number of `[<SEVERITY>-RESOLVED]` lines equals the Resolved column; the number of `[<SEVERITY>-UNRESOLVED]` lines equals the Unresolved column. The per-phase `Outstanding:` closure line counts unresolved findings only.

Every phase section emits its closure line even when findings are zero:
```
Outstanding: 0 blocking, 0 warnings, 0 info
```

---

## Severity model

| Severity | Trigger |
|:--|:--|
| Blocking | Emitted content violates a mandatory output-shape rule |
| Warning | Substrate gap yielded `N/A` or default assumption; hygiene finding |
| Info | Trace event, scope-signal detection, conditional category gating |

Severity is purely diagnostic. It never gates writes. The user iterates based on report content.

---

## Failure model

| Type | Trigger | Behavior |
|:--|:--|:--|
| Hard fail | Unresolvable parse error, missing CLAUDE.md, non-`.md` substrate, write error, unreadable reference file | Halt; stream error; no outputs written |
| Soft issue | Substrate gap, absent scope signal, defaulted assumption | Recorded in report; both files written at end |

Hard-fail message (replaces current phase stream line):
```
✗ Phase <N> — <phase name>: <reason>
  context: <relevant path or arg>
  remediation: <one-line suggestion>
```

---

## Substrate-gap defaults

| Signal absent | Behavior |
|:--|:--|
| §Scope In or Out | `N/A` + Warning per subsection |
| §Actors | `N/A` + Warning |
| §Glossary candidates | Auto-extract with Warning (user review required) |
| Any requirement section | `N/A` + Warning; section always renders |

No `🔲 To be defined` scaffolding. `N/A` is the only placeholder.

**N/A sections SHALL NOT carry requirement IDs.** When a category section (SEC, OBS, or any requirement category) is rendered as `N/A` because substrate is silent, render the section heading followed by a prose statement only — for example: `N/A — substrate silent on <category>. Warning emitted.` Do not emit `SEC-001`, `OBS-001`, or any other numeric requirement ID to carry the N/A. The section heading itself records the absence; allocating a numeric ID for an N/A pollutes the requirement-ID space and breaks the canonical-ordering invariant for downstream iterations. If a downstream consumer requires a section-level identifier for tooling, use the literal sentinel `SEC-NONE` or `OBS-NONE` — never a numeric ID.

---

## Iteration model

Each invocation is a full stateless pass — no detection of first vs nth iteration. Output files are overwritten each pass. User judges convergence; skill never marks `Final`.

DoD per iteration: all seven phases complete and both files written.
