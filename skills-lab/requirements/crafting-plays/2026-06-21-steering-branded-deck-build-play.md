# Steering a branded deck build from cleaned content

> A play for driving a model to produce a branded, on-template presentation from prepared content, holding one visual system across every slide and iterating the look without losing consistency. Worked instance: a 14-slide executive deck built from cleaned markdown on a branded corporate template.

## Advice (read first)

- Clean the content in its own pass before any design. Keep the author's words, show every change, then write.
- Read the generation tool's code, not just its description, to learn the real primitive set and palette. Confirm the template's layout names before you build.
- Decide the few real aesthetic choices once (theme, divider colour, card fill) and hold them across every slide. Route all styling through one helper.
- Render the deck to images and check the densest slide before delivering.
- Set card body text a step larger than feels safe, and add an accent so the cards are not flat.
- Use the native slide-number field, never literal page text. A later page deletion otherwise forces a full manual renumber.
- Expect the binary to leave through the download or outputs path, not a filesystem write.

## When to trigger

You hold authored content and you need a branded deck that follows a fixed template, produced through a generation skill rather than hand-placed slide by slide. The recognition signal is a requirement for visual consistency across many slides, paired with a generation tool whose primitive set and template are fixed, where you expect to iterate on the look after the first render.

Concrete examples, all from the originating session:

- A cleaned markdown source of headed prose blocks, no metrics, where the generation tool offers cover, divider, content canvas, card, KPI, and bar primitives, and it is not obvious which maps to the content. The qualitative blocks rule out the chart primitives and point to a card grid.
- A template that ships dozens of named layouts, where the build will call four of them and a wrong name fails the run.
- A first deck that reads well, followed by a list of visual edits scoped to specific pages, such as a navy header on a named subset, white cards everywhere, a larger body size, and a dark theme on the cover and end only.
- A chosen master that silently lacks a subtitle placeholder, so the subtitle vanishes until it is drawn by hand.

## Why it matters

A branded deck built by hand drifts in spacing, fill, and type from one slide to the next, and the drift is what makes a deck look assembled rather than designed. The play produces an on-template deck where every content slide shares one card system, the branding is inherited from the template rather than faked, and the few aesthetic choices are settled once and applied everywhere. The deliverable is the presentation file plus a build script that regenerates it from the cleaned source.

## The play

### Optimal workflow

1. Clean the source content in a separate pass. Fix grammar and formatting only, keep the author's words, display every change, then write. Treat any humaniser pass under a keep-the-words constraint as a no-op on substance.
2. Read the generation skill and its implementation module, not only the description. Extract the primitive set, the colour palette, and the layout names the build will use.
3. Verify the template's layouts before generating. Probe the template, list its layout names, and confirm each one the build calls.
4. Map the content to one repeating layout pattern. For headed prose blocks, a card grid per slide is the backbone that carries consistency.
5. Propose the slide plan and the consistency rules before building. Surface only the genuine aesthetic choices as one consolidated decision and lock them deck-wide.
6. Build through one parametric card helper. Drive numbering, fills, and the type scale from shared constants so every slide inherits the same look.
7. Render the deck to images and check overflow, branding, and footer or page-number inheritance before delivery.
8. Iterate each later change against an explicit slide range, re-render, and re-verify. Patch master gaps by drawing the missing element rather than assuming the layout carries it.
9. Deliver the binary through the download or outputs path. Keep the build script as the reproducible artifact.

### Critical moves

| Move | Collapse test |
| :--- | :--- |
| Read the tool's implementation to learn the true primitives and palette | Remove it and you propose designs the tool cannot render |
| Verify layout names against the template before the run | Remove it and the build fails mid-generation or binds the wrong layout in silence |
| Lock the consistency choices once, before building | Remove it and per-slide styling drifts, and the deck looks hand-assembled |
| Centralise card styling in one helper | Remove it and fills and type scale diverge across slides |
| Render to images for QA before delivery | Remove it and clipped text or a dropped placeholder ships unseen |
| Scope each later edit to a named slide range | Remove it and a global change lands on slides meant to keep the old treatment |

### Pits to avoid

- Page numbers written as literal text rather than a live slide-number field. Delete one slide and the whole deck needs manual renumbering. Prefer the native field.
- Sizing card body text for worst-case fit. It ends a step too small. Set a larger default and shrink only on the densest slides.
- One flat card style for the whole deck. Consistency does not require monotony. Add an accent inside the shared grid.
- Inline bold in the source markdown is lost when card text is passed as unstyled runs. Accept it and do not spend effort preserving bold during the content phase.
- A chosen master that lacks an expected placeholder drops that content without warning. Check what the master actually carries and draw what it does not.
- Writing the binary deck to local disk through a text-only filesystem write. It corrupts the file. Use the download or outputs path.

## When to use it

- The content is authored and cleaned, not still moving.
- A branded template and a generation skill already exist.
- Visual consistency across slides is a requirement, not a preference.
- You can render the result to images to QA it.
- You expect one or two rounds of visual iteration and the look matters to the audience.

## When not to use it

- A single slide or a one-off where a template buys nothing.
- No branded template or skill exists, so the work is free-hand design.
- The content is unsettled, where the design churns with every edit.
- A throwaway deck where speed beats polish.
- Heavy quantitative content, where the card and bar vocabulary cannot carry the data and a real charting path is needed.

## Expected outcome

A future reuse returns a deck that passes the checks below. If any check fails, the play was not fully applied.

| Check | Pass condition |
| :--- | :--- |
| Consistency | Every content slide uses the same card style, type scale, and grid. |
| Fit | No card text clips, verified on the densest slide by render. |
| Branding | Footer, page number, logo, and fonts are inherited from the template, not faked. |
| Choice lock | Theme, divider colour, and card fill were decided once and applied deck-wide. |
| Reproducibility | A build script regenerates the deck from the cleaned source. |
| Editability | Slide numbers survive a page deletion without manual renumbering. |

## Tradeoffs

### Consistency and polish

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Card style | One flat style deck-wide | Per-slide bespoke styling | One shared helper, accepting a plainer look that needed manual recolouring afterwards |
| Card body size | Fit-safe small | Larger and readable | Fit-safe on the first pass, which proved a step too conservative |
| Slide numbering | Static text | Live slide-number field | Static text inherited from the skill, which broke on page deletion |

### Process

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Design choices | Decide as you build | Lock upfront | Lock the few real choices before building, trading mid-build flexibility for consistency |
| Proposal grain | Per-slide proposals | One consolidated plan | One consolidated plan, faster to approve, less per-slide tailoring |
| QA | Trust the build | Render and inspect | Render to images every pass, slower but it caught overflow and a missing placeholder |
| Build medium | Hand-place shapes | Scripted build | Scripted, trading pixel control for a reproducible artifact |

### Content fidelity

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Source wording | Rewrite for the slide | Keep the author's words | Keep words, condensing only where a card head needed a short label |
| Humaniser pass | Let it rewrite | Hold it to the keep-words constraint | Held, so it made no substance change |
| Inline bold | Preserve in the deck | Drop it | Dropped, accepted as not worth handling in the content phase |

---

| Field | Value |
| :--- | :--- |
| Version | 1.0 |
| Last Updated | 2026-06-21 |
| Status | Draft |
| Pairs with | 20260622-excom-oujda-ai-delivery-and-operations.pptx |
