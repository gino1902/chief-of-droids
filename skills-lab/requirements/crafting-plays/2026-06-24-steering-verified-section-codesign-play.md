# Steering a verified, deduplicated architecture section by iterative challenge

## Read first

This play is a way of working, not a template to fill in. It captures how a human steers an AI assistant to co-author a cluster of related architecture sections, turn by turn, until each section is short, correct against official sources, free of overlap with its siblings, and in the right register. The pattern is generic. It applies to any document where you draft sibling sections with an assistant and care about correctness, no repetition, and tone. The worked instance that produced it was a Solution Architecture Document, but nothing here depends on that subject.

The centre of gravity is the steering loop: challenge, verify, isolate, control the register, then file. Everything below is that loop, reconstructed with the wrong turns removed.

## When to trigger

You are co-authoring several related sections of a design or architecture document with an assistant, one section at a time. You want each section short, technically correct, distinct from its neighbours, and pitched at a known audience. The signal that this play is needed is a run of drafts that read well but fail on one of four axes: they assert facts you cannot trace to a source, they repeat the same fact across sections, they overstate with absolutes, or they drift in tone.

Concrete examples of the moves that make up the loop:

- You ask for a short access-control paragraph, then later catch a claim in it that is stated as an absolute. You force the assistant to qualify it to what a source actually supports, rather than accept the confident version.
- You require three environments, but the draft cites a source that argues for a minimum of two. You name the contradiction and make the assistant defend the count or correct the citation, rather than let the inconsistency stand.
- Before a governance claim is allowed into the document, you demand it be verified against the official source. You also re-check a claim that was already marked verified, because it is load-bearing.
- After noticing one fact appears in two sections, you instruct the assistant to isolate claims so each section owns one concern and nothing repeats.
- You set the tone in passes, moving from very terse to a plain professional register, with a word budget, iterating the register separately from the content.
- You probe a term the assistant used, asking it to define it, to confirm you both mean the same thing before it goes in the document.

## Why it matters

The problem is that an assistant produces fluent prose faster than it produces correct, non-overlapping, well-scoped prose. Left unsteered, a set of sibling sections drifts: claims arrive unverified, facts repeat, absolutes creep in, and the tone wanders. This play is the steering discipline that converts fluent drafts into document-grade sections. The deliverable is a set of sibling sections where each owns one concern, every load-bearing claim traces to an official source, absolutes are qualified with their exceptions named, and the register matches the audience.

## The play

### Optimal workflow

1. Establish the component vocabulary before designing. Ask the assistant to name and confirm the building blocks first. Pin current names and limits against official sources, because product names and constraints drift and a wrong name poisons everything built on it.
2. Draft each section as one short prose block, one concern per block, at a stated length.
3. Set the register as a separate axis. State the tone and a word budget, and iterate the register on its own rather than tangled with the content.
4. Challenge every draft against the stated intent. When a draft contradicts a requirement of yours, a count, a scope, a posture, name the contradiction and make the assistant defend or correct it.
5. Gate load-bearing claims on verification. Require the assistant to fetch the official source and mark each claim, never assert from memory. Re-verify any claim you doubt, including ones already marked verified.
6. Force claim isolation across siblings. Assign each fact to exactly one section, then remove the duplicates so each block owns its concern alone.
7. Correct overstatements. Watch for absolutes and make the assistant narrow each one to what its source supports, with the exception stated explicitly.
8. Validate terms on demand. When the assistant leans on a term, ask it to define it, to confirm the shared meaning before the term enters the document.
9. Decide placement. Map each block to its home section in the document structure, and split a block when it straddles two sections.
10. Run the final prose through a de-AI pass for register, then file it.

### Critical moves

Each row survives the collapse test: remove it and the result falls apart.

| Move | What collapses without it |
| :--- | :--- |
| Challenge each draft against your stated intent | Internal contradictions survive into the document, since the assistant optimises for a plausible answer, not for consistency with your constraints |
| Gate load-bearing claims on source verification | Plausible-but-wrong facts enter the document unflagged and read as authoritative |
| Isolate claims so each section owns one concern | Sections repeat the same fact, no section owns it, and later edits to one copy leave the others stale |
| Treat register as its own axis | Tone and content get iterated together, so every wording pass risks reopening settled facts |

### Pits to avoid

- Importing a source's floor as if it were your target. A source that justifies separation does not justify a specific count. Citing a minimum to support a larger number reads as an argument against your own decision.
- Letting the assistant state current product names, limits, or config from memory. These drift, and an unverified claim reads fine while being wrong.
- Absolute phrasing that outruns the source. Words like all, never, and only invite the one exception an auditor will probe. The exception is the part worth stating.
- Conflating a control with its configuration. A lock and the key cut for one identity are different objects. Precise vocabulary is the point of a security section.
- The same fact restated in two sections, so neither owns it and the two copies drift apart over time.
- Over-processing a terse reference block through a humanising pass. Adding voice to a control table damages it. Humanise prose, leave tables neutral.
- Accepting a verification marker once and never re-checking the claim the whole section rests on.

## When to use it

- You are producing document sections one at a time with an assistant, and the sections are siblings that risk overlap.
- The claims are version-sensitive or governance-relevant, so correctness against official sources is required.
- The audience is defined, so register and length matter.
- The assistant has a tool to fetch official sources, so the verification gate can actually run.

## When not to use it

- A single isolated paragraph with no siblings to deduplicate against.
- Content with no externally verifiable claims, where the value is internal opinion or framing.
- A throwaway draft where neither precision nor tone matters.
- No source-fetching tool is available, so the verification gate cannot be enforced and the play loses its spine.

## Expected outcome

| Promise | How to check |
| :--- | :--- |
| Each section owns one concern | No fact appears in more than one sibling section |
| Every load-bearing claim is traceable | Each carries a verification marker mapped to an official source |
| Absolutes are honest | Each all, never, or only is qualified to what the source supports, with the exception named in the text |
| Register fits the audience | Tone and length match the stated brief, checked by reading aloud |
| Placement is decided | Each block has a named home section, and any straddling block was split |

## Tradeoffs

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Verification effort | Accept claims from memory for speed | Verify everything, however trivial | Verify load-bearing claims, accept only inert trivia from memory |
| Section length | Exhaustive and complete | As terse as possible | Terse blocks that keep the one load-bearing exception rather than drop it |
| Register versus terms | Full casual or simplified register | Strict formal terminology | Casual tone, but keep the recognised term wherever an expert or auditor reads it |
| Section shape | One rich consolidated section | Isolated single-concern siblings | Split into single-concern siblings, accepting cross-references as the cost |
| Humanising pass | Add author voice everywhere | Keep everything neutral | Humanise prose only, leave control tables and reference rows neutral |

## Sources

The play itself is a methodology and has no external claims of its own. These are the official sources fetched and verified during the originating session, carried here for the paired SAD deliverables. All are Microsoft Learn or Databricks official documentation, fetched 2026-06-24, each last updated within the prior month unless noted.

| Topic verified | Source |
| :--- | :--- |
| Security, compliance, and privacy best practices | https://learn.microsoft.com/en-us/azure/databricks/lakehouse-architecture/security-compliance-and-privacy/best-practices |
| Workspace strategy, SDLC environment separation (Phase 2) | https://learn.microsoft.com/en-us/azure/databricks/lakehouse-architecture/deployment-guide/workspace-strategy |
| Well-Architected security pillar, resource segmentation | https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-databricks |
| Operational excellence best practices, environment isolation | https://learn.microsoft.com/en-us/azure/databricks/lakehouse-architecture/operational-excellence/best-practices |
| Databricks Apps best practices, least privilege and service principals | https://learn.microsoft.com/en-us/azure/databricks/dev-tools/databricks-apps/best-practices |
| Serverless Private Link and Network Connectivity Configuration | https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/serverless-private-link |
| ADLS Gen2 external location, storage firewall trusted services | https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/external-locations |
| Azure managed identities in Unity Catalog, access connector resource instance rule | https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/azure-managed-identities |
| Partner-powered AI features, model providers and residency | https://learn.microsoft.com/en-us/azure/databricks/databricks-ai/partner-powered |
| AI assistive features trust and safety, data retention and UC permissions | https://learn.microsoft.com/en-us/azure/databricks/databricks-ai/databricks-ai-trust |
| Genie Space set-up prerequisites and concepts | https://learn.microsoft.com/en-us/azure/databricks/genie/set-up |

## Version block

| Field | Value |
| :--- | :--- |
| Version | 1.1 |
| Last Updated | 2026-06-24 |
| Status | Draft |
| Pairs with | O2 SAD Security (segregation of rights), Environment strategy, and Network design blocks drafted in-session, not yet filed |
