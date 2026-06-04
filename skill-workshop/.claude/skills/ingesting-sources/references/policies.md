# Policies — granularity, conflicts, collisions, dependencies

Loaded at Phase 3. Governs how extracted items become rows with a destination and an action.

## Granularity

Choose the coarsest level at which an action is atomic: `section`, `subsection`, `sub-subsection`, or `claim`. Recurse to a finer level only when one part of a section needs a different action from the rest (an 80/20 split inside a section). The chosen level is the row's `Category`. Reason: the coarsest atomic level keeps the report small enough to review while still letting the user reject exactly the part they disagree with.

## Conflict policies

A conflict exists when an extracted item disagrees with content already on a target page. Classify each into one action:

| Action | Meaning | When |
|---|---|---|
| `replace` | New content overwrites the existing content. | The existing claim is simply wrong or fully outdated and not worth keeping. |
| `supersede` | New content takes precedence; the old content is kept and annotated as superseded at the section level. | The old claim has historical or contrastive value worth preserving. |
| `coexist` | Both stand, framed as distinct claims (different scope, context, or source). | Not a true contradiction; both are valid in their own frame. |
| `do not add` | The new item is rejected. | Newer-wins says the wiki already holds the more recent and correct claim. |

Supersede annotations live in the page body at section level, never in front-matter (page-schema rule: no page-level status field).

## Newer-wins heuristic

Default for this domain: the more recent source wins (~80% of cases).

- Compare the new source's `issued_date` (extracted in Phase 1) with the existing source's `issued_date` (from the target page's front-matter `sources[]`).
- Newer source contradicting older wiki content → `replace` or `supersede`.
- Older source contradicting newer wiki content → propose `do not add`.
- Surface both dates in Table 3 as `new / existing`. When newer-wins suggests `do not add`, set the anomaly flag ⚠️ so the user sees the case where newer-wins may be wrong (primary sources, foundational texts, historical records). The user overrides the ~20%.

If either `issued_date` is `unknown`, do not apply newer-wins silently; flag the row ⚠️ and let the user decide.

Reason: newer-wins is a domain default, not a law. Primary sources, foundational texts, and historical records invert it, so the policy flags the inversion case for the user rather than auto-applying it.

**Example — newer-wins suggests do not add (⚠️):**

Correct (flag and propose, do not silently drop):
> New source `archive-1998.pdf` (issued 1998-03-01) states the HQ was in Detroit. The wiki already states Austin, cited to `relocation-2021.pdf` (issued 2021-06-01).
> Table 3 row: Action `do not add`, Dates `1998-03-01 / 2021-06-01`, ⚠️ set, Description "older source contradicts newer wiki claim; confirm before discarding".

Incorrect (silent drop):
> Discard the 1998 claim without a row because it is older. The user never sees that a primary historical source disagreed.

## Slug collisions

Detected while proposing modifications (Table 1 renames) and creations (Table 2). When a proposed slug already exists for a different referent:

- Propose a disambiguated slug (e.g. `mercury-planet` vs `mercury-element`), or
- Propose merging into the existing page when they are the same referent.

Put the proposal in the row's `Destination` and explain in `Description`. The user approves through row controls. Latent collisions discovered later are the health-check's job, not this skill's.

**Example — slug collision:**

Correct (disambiguate distinct referents):
> Proposed page `mercury` for the planet collides with existing `mercury` for the element.
> Destination `mercury-planet`; Description "disambiguated from existing [[mercury]] (element)".

Correct (merge same referent):
> Proposed page `tesla-motors` describes the same company as existing `tesla-inc`.
> Destination `tesla-inc`; Description "merge into existing page; same referent".

Incorrect (overwrite the collidee):
> Write the planet content onto the existing `mercury` page, replacing the element. Two referents, one slug, silent data loss.

## Cross-row dependencies

Declare `Depends on` whenever a row references a RowID that must be applied for this row to be valid. Examples: a Table 4 link update depends on the Table 2 creation of its target page; a Table 1 modification depends on a rename row.

- Declare the dependency explicitly in the `Depends on` column.
- Local rejection of a depended-on row is allowed during approval, but it leaves dangling references. The Phase 6 dangling check catches these before any mutation.
