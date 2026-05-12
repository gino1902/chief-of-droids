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
- [BLOCKING] <description> → <remediation>
- [WARNING] <description> → <remediation>
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
- **Warning** — Resolved if the finding has been treated and requires user verification only (e.g. auto-derived glossary entry, inferred scope signal). Unresolved if the artifact cannot be considered correct without further action.
- **Blocking** — resolution rules not yet defined; populate Resolved and Unresolved from phase findings.

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

---

## Iteration model

Each invocation is a full stateless pass — no detection of first vs nth iteration. Output files are overwritten each pass. User judges convergence; skill never marks `Final`.

DoD per iteration: all seven phases complete and both files written.
