# QA — Architecture Requirements

> Loaded by writing-docs SKILL.md Step 8 when `template-architecture-requirements.md`
> is in use. Executable quality gate before any output is proposed.

## Activation

This QA file activates when the body template in use is `template-architecture-requirements.md`.

## Per-row criteria

For each requirement row in sub-sections 4.1–4.4, verify all five:

| # | Criterion | Pass test |
| :--- | :--- | :--- |
| 1 | Non-ambiguous | Single interpretation possible to a reasonable architect-reader |
| 2 | Complete | No implicit prerequisite, dependency, or trailing condition |
| 3 | Design-independent | Describes what must be true, not how to achieve it; no technology lock-in |
| 4 | Atomic | One requirement per row; "and" / "or" splitting another requirement triggers a fail |
| 5 | C4-friendly | Addressable at System or Container level; not a Component or Code-level concern |

## Rejection rule

A requirement failing one or more criteria must be either:
- **rewritten** in the "Suggested rephrasing/fix" column, leaving the original intact for diff review, or
- **removed** entirely if no valid rewrite exists.

Never silently leave a failing requirement in the table without flagging.

## Examples

### Pass

| Requirement | Verdict |
| :--- | :--- |
| Bulk data in the landing zone is in an agnostic format consumable by each subsystem. | All five — pass |

### Fail (compound)

| Requirement | Verdict | Suggested rephrasing/fix |
| :--- | :--- | :--- |
| The system pulls bulk data from sub-systems and exposes it to consumers via a REST API. | Atomicity (two requirements); design-independence (REST is a tech choice) | Split into: (1) "System pulls bulk data from sub-systems into a single staging zone." (2) "System exposes data to consumers via a documented interface." |

### Fail (ambiguous)

| Requirement | Verdict | Suggested rephrasing/fix |
| :--- | :--- | :--- |
| Data quality is good. | Non-ambiguity (no measure); completeness (no acceptance threshold) | "Data quality accountability is assigned per data product, with measurable thresholds defined in the data contract." |

## Output

After running this QA, emit a brief report inline:

```
QA Report — Architecture Requirements
Total requirements: {N}
Passed: {N}
Rephrased: {N}
Removed: {N}
```

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.0        |
| Last Updated | 2026-04-28 |
| Status       | Draft      |
