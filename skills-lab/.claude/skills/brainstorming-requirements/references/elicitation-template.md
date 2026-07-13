# elicitation-template

What a well-elicited component slice looks like, before `writing-requirements` formalises it. This is the emission spec for Phase 2 of `brainstorming-requirements`.

The governing rule: `writing-requirements` extracts, it does not synthesise. Anything absent or mis-shaped in the slice comes back downstream as `N/A` + Warning. So the slice must make every decision explicit and phrase it in the exact signal the formaliser reads for.

## Mapping: what writing-requirements extracts ← what the slice must emit

| Downstream target | Signal it reads | Slice field that feeds it | Discipline |
|:--|:--|:--|:--|
| Title | First H1 | Slice H1 = the component name | Always write an H1. Never rely on a fallback, it warns and prints the slug raw. |
| Purpose | Explicit opener ("This service…", "The purpose of…") | One purpose sentence under the H1 | Write it explicitly with a recognised opener. Do not leave it to inference. |
| In scope | Positive verbs: covers, handles, responsible for | `## In scope` bullets | Phrase each as "Covers X" / "Handles Y" / "Responsible for Z". Plain nouns will not match. |
| Out of scope | Negation: not handled, outside this, upstream, downstream, out of scope, owned by | `## Out of scope` bullets | Name the owning component, "owned by payments-gateway". This is where allocation becomes visible. |
| Actors and consumers | Upstream / downstream / role language | `## Actors and consumers`, directional | State upstream actors and downstream consumers explicitly. This block also carries the product-level edge. |
| Requirement statements | Requirement-shaped blocks | `## Requirements`, one per bullet, in the requirement contract | Write each as actor / action / result / conditions and limitations (see below). Tag each with an inert `(R-NN)` origin reference. |
| Acceptance criteria | A measurable predicate inside the requirement | The conditions-and-limitations clause of each requirement | The measurable predicate lives in the conditions clause. "within 200 ms" yields criteria; a requirement with no conditions clause yields a Warning and none. |
| Glossary | Backticked terms, explicit definitions | The domain terms the requirements use, drawn from `CONCEPTS.md` | Backtick or explicitly define every domain term the requirements lean on, not only literal identifiers. Plain-prose domain terms slip past the mechanical extraction and come back as undefined-term Warnings. Draw the terms from `CONCEPTS.md`; do not mint local synonyms. |
| Type | The `--type` invocation arg | A recommended type per slice | Recommend `technical` only when the slice carries non-functional, security, or observability requirements. |
| Slug | `^[a-z0-9-]+$`, no requirement/req/reqs | A suggested slug | Clean and reserved-token-safe, or the downstream run hard-fails. |

## Slice template

```markdown
# <Component name>

This <component> handles <purpose in one explicit sentence>.

## In scope
- Covers <capability>  (R-01)
- Handles <capability>  (R-02)

## Out of scope
- <capability>, owned by <other component>

## Actors and consumers
- Upstream: <actor or system>
- Downstream: <consumer> consumes <output>

## Requirements
- The <actor> shall <action>, so that <result>, when <conditions and limitations>.  (R-01)
- The <actor> shall <action>, so that <result>, when <conditions and limitations>.  (R-02)
```

## Requirement contract

Each requirement is one SHALL statement that exposes four parts:

- Actor — the component or role that acts. Default to "system" when the slice covers one component.
- Action — what it does, the SHALL verb and its object.
- Result — the outcome the action achieves, phrased "so that <consequence>". This is the purpose or resulting state, the why it matters, not the direct object of the action.
- Conditions and limitations — the trigger, state, threshold, or boundary under which it holds, phrased "when <condition>". This is where the measurable predicate lives, and it is what the acceptance criteria derive from downstream.

Written as: `The <actor> shall <action>, so that <result>, when <conditions and limitations>.`

Example: `The system shall write the landed data in its exact form, so that the ingested data is preserved in its prior form, when the data is subject to auditability.`

This maps onto EARS: the conditions clause becomes the EARS trigger (when / while / if / where), and the action becomes the SHALL response, so the formaliser has less to reconstruct. The "so that" result is carried rationale. A requirement with no conditions clause is under-specified and comes back as a Warning with no derivable acceptance criterion.

The `(R-NN)` tags are inert to the downstream ID scanner (it matches `FR`, `NFR`, `SEC`, `ERR` and the like, not `R`), so they annotate for traceability without being mistaken for requirement IDs.

## Do not emit (leave to the formaliser)

- No category IDs (`FR-001`, `NFR-002`, …). Categorisation is the formaliser's job; use the inert `R-NN` tags.
- No error entries. `writing-requirements` drafts the paired error requirements itself from the SHALL-verb shape.
- No glossary section. It is auto-extracted downstream; your only job is to make extraction possible by backticking or defining every domain term the requirements use, drawn from `CONCEPTS.md`.
- No interface wire contracts. The actors block carries the product-level edge, which is enough. Payloads, protocols, sequencing are a how, and out of scope for this chain.

## Type rule

A slice's type is a promise about its own content. Mark it `technical` only when it actually carries non-functional, security, and observability SHALL statements. Otherwise `generic`. Marking a slice technical without those statements only produces `N/A` sections downstream.

| Field        | Value      |
|--------------|------------|
| Version      | 1.3        |
| Last Updated | 2026-07-13 |
| Status       | Draft      |
