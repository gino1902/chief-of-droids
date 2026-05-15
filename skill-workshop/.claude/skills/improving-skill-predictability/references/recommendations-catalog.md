# Recommendations catalog

Reusable patterns for skill-hardening recommendations. Each pattern names: the kind of drift it addresses, a template statement, and the typical projected lift band.

Use these as starting points — adapt the statement to the specific drift evidence found in Phase 3. Do not include a pattern if it does not match an observed deviation.

## Anti-drift on verbatim strings

**Drift signature**: a prompt fragment or quoted string varies across runs (casing, wording, presence).

**Template statement**: "In step `<step>`, the prompt to the user must read exactly `"<verbatim>"`. Do not paraphrase, recase, or wrap in additional words."

**Typical lift band**: +5 to +15 points on Substrate fidelity — verbatim strings.

**Risk**: pinning a wording may age poorly if the substrate's intent shifts. Note this only when the verbatim is non-load-bearing.

## Anchor identifiers to canonical statements

**Drift signature**: same ID labels different statements across runs, or one ID splits into two across runs.

**Template statement**: "Each statement of class `<class>` is anchored to a single identifier of the form `<prefix>-<NNN>`. Identifiers are assigned by the order in which statements appear in the substrate, not by the order in which they appear in the output."

**Typical lift band**: +10 to +20 points on Identifier alignment.

**Risk**: ordering rules may conflict when the substrate is restructured between iterations. Document the precedence.

## Pin modality by enforceability

**Drift signature**: same statement appears as MUST in some runs and SHOULD in others.

**Template statement**: "Modality is determined by enforceability, not by the author's preference. A statement is MUST if it has a verifiable acceptance test; SHOULD if it can be observed but not gated; MAY if it is a discretionary optimization."

**Typical lift band**: +5 to +15 points on Modality and surface drift.

**Risk**: forces the skill to evaluate enforceability before writing modality. Slower output.

## Lock section ordering

**Drift signature**: heading sequence differs across runs even when content is preserved.

**Template statement**: "Emit sections in the fixed order: `<list>`. A section is omitted only if it is empty, not relocated."

**Typical lift band**: +10 to +25 points on Section structure fidelity.

**Risk**: a rigid order may produce empty sections — accept this as the lesser cost.

## Re-read substrate before generating

**Drift signature**: a substrate concept is paraphrased away, dropped, or renamed in some runs.

**Template statement**: "Before drafting section `<section>`, re-read the substrate lines containing `<concept>`. Carry the substrate's literal phrasing into the output for any term defined in the substrate's glossary."

**Typical lift band**: +5 to +20 points on Substrate fidelity — domain concepts.

**Risk**: increases prompt length and re-read cost.

## Split a contested category

**Drift signature**: runs disagree on whether a class of statements belongs in category A or category B.

**Template statement**: "Statements with property `<P>` belong in `<A>`; statements without `<P>` belong in `<B>`. The decision is taken in Phase `<N>` before drafting any section."

**Typical lift band**: +5 to +15 points on Statement counts per category.

**Risk**: a poorly-drawn boundary will create new drift on the boundary itself.

## Fold a vestigial category

**Drift signature**: a category exists in some runs and is folded into another in other runs, with no semantic difference.

**Template statement**: "`<category>` is not a top-level section. Its content is merged into `<parent-category>`."

**Typical lift band**: +5 to +10 points on Section structure fidelity.

**Risk**: loses optionality — once folded, splitting is harder.

## Frame the topic from substrate, not slug

**Drift signature**: some runs use the user-supplied slug as the canonical name; others read the canonical name from the substrate.

**Template statement**: "The canonical topic name is read from the substrate's title or its first defining sentence. The user-supplied slug is a filename token only and is not used in the output's prose."

**Typical lift band**: +10 to +30 points on Naming framing.

**Risk**: rare — the substrate must actually carry a canonical name. If it doesn't, surface the gap rather than guess.

## When to refuse a recommendation

Do not include a recommendation that:

- Addresses a drift seen in only one run (insufficient signal).
- Trades a structural property the substrate explicitly varies on (e.g., the substrate itself uses different wordings for the same idea — runs reflecting that variance are doing the right thing).
- Has a projected lift of less than +5 points across all dimensions combined.

## Substrate-agnostic statements, substrate-specific evidence

A recommendation's `Statement` field must read as a rule the skill can apply to any future substrate, not as a transcription of the analyzed substrate. Substrate-specific content belongs in `Rationale` (which deviations it would have prevented) and in cited evidence — not in the rule itself.

Counter-example (over-fit, do not write this):

> Statement: For this substrate the FR order is: (1) sentinel read, (2) project prompt, (3) workspace CLAUDE.md load, …

The 16-item list is a finding, not a rule. The skill being analyzed cannot use that list when run on a different substrate. Refactor as:

> Statement: When assigning IDs in Phase 2, walk the substrate body top-to-bottom and assign identifiers in the order each requirement-shaped statement first appears. Do not renumber for narrative flow.
> Rationale: The 16-FR order in the analyzed substrate is: (1) sentinel read, (2) project prompt, …

The rule is portable. The order is evidence.
