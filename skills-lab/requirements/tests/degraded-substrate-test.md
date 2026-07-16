# Degraded substrate test — XC-3

_These are illustrative fixtures. The subject, any scripted answers, thresholds, slugs, and file names below are examples to make the run concrete, not fixed requirements. Swap them freely. The acceptance criteria are what carry the test._

Run this in a fresh session. Positive-path stress for the conservative-emission stance of `writing-requirements`.

## Purpose

Exercise the safety property the whole no-synthesis design rests on: when substrate signal is absent or mis-shaped, `writing-requirements` renders `N/A` plus a Warning and never invents content. XC-1 covers argument hard-fails that halt at Phase 0. This is different, the substrate is valid enough to process but deliberately degraded, so the run proceeds (soft issues, not hard-fail) and must degrade gracefully per section rather than crash or fabricate. It confirms the title fallback fires to the slug verbatim, Scope and Actors render `N/A`, and any genuine requirement signal is still extracted.

## Directory and precedence

Directory: `outputs/test-wr-degraded`, created by this test.

Precedence: none. Independent of every other scenario.

## Preconditions

- A fresh session.
- The directory `skills-lab/outputs/test-wr-degraded` exists. Session cwd is that directory.
- Do not add a `CLAUDE.md` to the test dir. It must carry none, so the run exercises the fixed Phase 0.5 cwd-anchoring: with no `CLAUDE.md` at cwd, the skill resolves the repo root to cwd itself, emits a warning, and writes outputs under this directory. It no longer walks upward, so nothing escapes to the `skills-lab` root. Before the fix at `e4a0e06` this row needed a scaffold `CLAUDE.md` to contain the escape; that is no longer required, and running without one is now part of what the row proves.
- Create one fixture `bare.md` with prose only: no `#` H1, no `##` H2, no frontmatter title, no scope language (`covers`, `handles`, `owned by`), and no actor language. Include exactly one requirement-shaped line so functional extraction has something to find, for example: `The system shall store each record when it arrives.` Surround it with a sentence or two of plain prose that names no domain terms.

## Run steps

### 1. Formalise the degraded substrate

Invoke `writing-requirements bare-spec from bare.md --type generic`.

The substrate is a valid, non-empty `.md`, so Phase 0 passes and the run proceeds. The degradation shows up in Phases 1 to 5 as `N/A` plus Warnings, not as a halt.

## Expected outputs (under `outputs/test-wr-degraded`)

- `bare.md`, unchanged.
- `requirements/bare-spec/bare-spec-requirements.md` and `-report.md`, both written under cwd (`outputs/test-wr-degraded/requirements/bare-spec/`), not at the `skills-lab` root (soft issues do not halt the run).
- In the requirements file: the Title is the slug `bare-spec` verbatim; §Scope In and Out both `N/A`; §Actors `N/A`; one functional requirement extracted from the SHALL line.
- In the report: a Phase 0 `[WARNING-UNRESOLVED]` that no `CLAUDE.md` was found at cwd and cwd was used as the repo root. This adds one to the warning total versus a run with a `CLAUDE.md` present.
- In the report: a Warning that the substrate has no H1, H2, or frontmatter title and the slug was used verbatim; Warnings for the `N/A` Scope subsections and Actors.
- In the report: an undefined-term Warning that the SHALL line's domain object (`record` in the example) is used but absent from §Glossary. With no `CONCEPTS.md` upstream there is no source to define it, so this is the design's intended pre-`CONCEPTS.md` vocabulary noise, not a fault (see `requirements-chain-design.md`, §Project size and §What is proven). The skill flags it; it does not synthesise a definition.

## Acceptance criteria

- The Title is the slug `bare-spec` verbatim, not humanised (not `Bare Spec`, not `Bare-Spec`), and a Warning records the missing title.
- §Scope In, §Scope Out, and §Actors each render `N/A` with a Warning. None is populated with synthesised content.
- The one SHALL line is extracted as a functional requirement, showing degradation is per-section, not all-or-nothing, and that real signal is still captured.
- The SHALL line's domain object (`record`) is flagged as undefined, not passed silently: FR-001 scores Unambiguous ✗ and a Warning records the term absent from §Glossary. This is the design's intended behaviour on substrate with no `CONCEPTS.md` anchor; the skill must not resolve it by inventing a definition.
- Both output files are written. The run does not hard-fail on the degradation.
- Outputs land under cwd: `requirements/bare-spec/` is created inside `outputs/test-wr-degraded`, not at the `skills-lab` root, and a Phase 0 `[WARNING-UNRESOLVED]` records that no `CLAUDE.md` was found at cwd and cwd was used as the repo root.
- No section carries invented scope, actors, or a fabricated title.
- No extra artifacts: `writing-requirements` writes only its two output files and does not modify `bare.md` or anything else.

## Fail conditions

- The Title is humanised or otherwise synthesised instead of the slug verbatim.
- Scope or Actors are populated with invented content rather than `N/A`.
- The run hard-fails on the degraded substrate instead of emitting `N/A` plus Warnings (the conservative stance broken).
- The SHALL line is dropped, or a requirement is fabricated that the substrate did not carry.
- Outputs escape to `skills-lab/requirements/bare-spec/` instead of landing under cwd (the Phase 0.5 anchoring regressed), or the `no CLAUDE.md at cwd` Phase 0 warning is absent.
- Any file other than the two outputs is written or modified.

## Record

Confirm the Title equals the slug verbatim, list which sections rendered `N/A`, and confirm the SHALL line survived as a functional requirement. Confirm the two output files landed under cwd (not the `skills-lab` root) and that the Phase 0 no-`CLAUDE.md` warning is present, adding one to the warning total. Two vocabulary points. Auto-derived glossary warnings, if any, are the usual verification-pending kind, separate from the degradation Warnings this test targets. And the SHALL line's domain object (`record`) is expected to raise an undefined-term Warning and score Unambiguous ✗, because with no `CONCEPTS.md` upstream there is no source to define it. That warning is the design's intended pre-`CONCEPTS.md` vocabulary signal (`requirements-chain-design.md`), not a defect, and not something the skill should resolve by inventing a definition.

## Note

This is the graceful-degradation complement to XC-1's hard-fails. Together they cover both halves of Phase 0-to-5 robustness: stop cleanly on bad arguments, degrade cleanly on thin substrate, and in neither case invent content.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.3        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
