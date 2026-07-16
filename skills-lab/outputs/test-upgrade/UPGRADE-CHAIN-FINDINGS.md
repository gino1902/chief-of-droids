# Upgrade chain findings

Test of the bootstrap to requirements chain on the sensor-filer project, run over six steps. This captures the five points asked for.

## 1. Small bootstrap fired the Small branch

The Small bootstrap produced no CONCEPTS.md and no Tracks. FRAMING.md was the five-question shape (goal stamp on line 1, no last_updated frontmatter). Step 2 confirmed CONCEPTS.md was absent on disk before the upgrade. This is the expected Small branch behaviour.

## 2. The upgrade produced the Medium+ shape

framing-project turned the Small doc into the Medium+ shape. It added Tracks (Filing and Retrieval) and seeded a context-structured CONCEPTS.md. CONCEPTS.md carries a shared core (drop, sensor, reading, store), one context block per track (Filing owns quarantine, Retrieval owns lookup), and a context map for the cross-context relationships.

## 3. Undefined-term warnings cleared

The undefined-term warning count went from 4 at step 3 to 0 at step 6, so it cleared (and is strictly fewer either way).

- Step 3 (v0.1, no CONCEPTS.md): drop, sensor, reading and store were used in the requirements but had no authoritative definition. They scored as auto-derived and Unambiguous was marked false on all four functional requirements.
- Step 6 (v0.2, CONCEPTS.md governing): the same four terms carried substrate definitions drawn from CONCEPTS.md, so the term-absence check found nothing and Unambiguous was marked true on all four.

The two warnings that remain at step 6 are constants, not regressions. They are the Constraints section rendered N/A (the FRAMING constraint about local only, one machine was never carried into the slice) and the filename literal, which is a format literal rather than a governed domain term.

## 4. Version incremented across the re-write

The requirements artifact incremented from version 0.1 (step 3) to version 0.2 (step 6), driven by the prior file being present on disk when the re-write ran.

## 5. framing-project consumed the Small doc cleanly

framing-project consumed the five-question FRAMING.md cleanly. It did not need reconciliation. Phase 0 detected the Small shape (goal stamp present, no last_updated key) and routed to a dedicated convert path (Phase 1b). That path carried each Small answer into its Medium+ target through a built-in map, re-interviewed nothing already answered, interviewed only the genuine gaps (the Business dimension and Tracks), added the frontmatter the Small path never wrote, and preserved the goal stamp. The stamp moved from line 1 to line 5, just under the new frontmatter, which is documented behaviour rather than drift.

### Chain-level finding to carry forward

writing-requirements does not read CONCEPTS.md. Its vocabulary phase extracts only from the substrate slice. So CONCEPTS.md governs which terms brainstorming-requirements chooses, but the definitions reach the formaliser only when the slice itself embeds them. Backticking a term alone leaves it auto-derived and still undefined. Explicit definition lines in the slice are what flip a term to substrate status and clear the warning.

The practical consequence: a re-brainstormed slice that omits the definitions would not clear the warnings even with CONCEPTS.md present. Worth deciding whether writing-requirements should read CONCEPTS.md directly, so the chain does not depend on each slice re-stating the definitions. A related wording tension sits in the elicitation template, which says no glossary section yet also says define every domain term. In practice the second wins, and the first is better read as do not emit the downstream Glossary table or category IDs.

| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |

