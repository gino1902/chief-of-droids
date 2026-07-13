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
- Add a minimal `CLAUDE.md` to the test dir so the skill's Phase 0.5 repo-root walk stops here and writes outputs under this directory rather than escaping upward to the `skills-lab` root. Without it, cwd carries no `CLAUDE.md`, the walk resolves repo root to `skills-lab`, and outputs land in `skills-lab/requirements/bare-spec/` instead. This `CLAUDE.md` is setup scaffold, established before the run, not a skill-written artifact, so the "no extra artifacts" acceptance check does not count it.
- Create one fixture `bare.md` with prose only: no `#` H1, no `##` H2, no frontmatter title, no scope language (`covers`, `handles`, `owned by`), and no actor language. Include exactly one requirement-shaped line so functional extraction has something to find, for example: `The system shall store each record when it arrives.` Surround it with a sentence or two of plain prose that names no domain terms.

## Run steps

### 1. Formalise the degraded substrate

Invoke `writing-requirements bare-spec from bare.md --type generic`.

The substrate is a valid, non-empty `.md`, so Phase 0 passes and the run proceeds. The degradation shows up in Phases 1 to 5 as `N/A` plus Warnings, not as a halt.

## Expected outputs (under `outputs/test-wr-degraded`)

- `bare.md`, unchanged.
- `requirements/bare-spec/bare-spec-requirements.md` and `-report.md`, both written (soft issues do not halt the run).
- In the requirements file: the Title is the slug `bare-spec` verbatim; §Scope In and Out both `N/A`; §Actors `N/A`; one functional requirement extracted from the SHALL line.
- In the report: a Warning that the substrate has no H1, H2, or frontmatter title and the slug was used verbatim; Warnings for the `N/A` Scope subsections and Actors.
- In the report: an undefined-term Warning that the SHALL line's domain object (`record` in the example) is used but absent from §Glossary. With no `CONCEPTS.md` upstream there is no source to define it, so this is the design's intended pre-`CONCEPTS.md` vocabulary noise, not a fault (see `requirements-chain-design.md`, §Project size and §What is proven). The skill flags it; it does not synthesise a definition.

## Acceptance criteria

- The Title is the slug `bare-spec` verbatim, not humanised (not `Bare Spec`, not `Bare-Spec`), and a Warning records the missing title.
- §Scope In, §Scope Out, and §Actors each render `N/A` with a Warning. None is populated with synthesised content.
- The one SHALL line is extracted as a functional requirement, showing degradation is per-section, not all-or-nothing, and that real signal is still captured.
- The SHALL line's domain object (`record`) is flagged as undefined, not passed silently: FR-001 scores Unambiguous ✗ and a Warning records the term absent from §Glossary. This is the design's intended behaviour on substrate with no `CONCEPTS.md` anchor; the skill must not resolve it by inventing a definition.
- Both output files are written. The run does not hard-fail on the degradation.
- No section carries invented scope, actors, or a fabricated title.
- No extra artifacts: `writing-requirements` writes only its two output files and does not modify `bare.md`, the setup `CLAUDE.md`, or anything else. The pre-run `CLAUDE.md` scaffold is not a skill artifact and does not count against this.

## Fail conditions

- The Title is humanised or otherwise synthesised instead of the slug verbatim.
- Scope or Actors are populated with invented content rather than `N/A`.
- The run hard-fails on the degraded substrate instead of emitting `N/A` plus Warnings (the conservative stance broken).
- The SHALL line is dropped, or a requirement is fabricated that the substrate did not carry.
- Any file other than the two outputs is written or modified (the pre-run `CLAUDE.md` scaffold excepted, since it predates the run).

## Record

Confirm the Title equals the slug verbatim, list which sections rendered `N/A`, and confirm the SHALL line survived as a functional requirement. Two vocabulary points. Auto-derived glossary warnings, if any, are the usual verification-pending kind, separate from the degradation Warnings this test targets. And the SHALL line's domain object (`record`) is expected to raise an undefined-term Warning and score Unambiguous ✗, because with no `CONCEPTS.md` upstream there is no source to define it. That warning is the design's intended pre-`CONCEPTS.md` vocabulary signal (`requirements-chain-design.md`), not a defect, and not something the skill should resolve by inventing a definition.

## Note

This is the graceful-degradation complement to XC-1's hard-fails. Together they cover both halves of Phase 0-to-5 robustness: stop cleanly on bad arguments, degrade cleanly on thin substrate, and in neither case invent content.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.2        |
| Last Updated | 2026-07-14 |
| Status       | Draft      |
