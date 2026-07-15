# Tool assessment funnel play

> Reconstructed from the 2026-07-15 session assessing Claude Code + Chrome integration for enterprise software engineering use.

## When to trigger

A new AI tooling integration (agent capability, connector, extension) is a candidate for enterprise adoption and the user needs a decision-ready view: what it does, how practitioners actually use it, and which usages fit the organisation's risk appetite. The signal is a request that mixes discovery ("scan official docs") with governance framing ("secure to not enterprise acceptable").

Concrete instances:

- This session: assess Claude Code + Chrome browser integration for software engineering use at SQLI. The user asked for official docs first, then a risk-tiered use case table, then community practices filtered to secure-medium with popularity signals, then worked examples, then a companion guide.
- Future match: a new MCP connector appears in the registry and the question is whether it belongs in client-facing workflows.
- Future match: a Databricks feature reaches GA and the O2 platform team needs a scoped adoption recommendation.
- Counter-example that looks similar but is not this play: "summarise what Claude Code does". That is a single docs scan with no risk tiering or community filter, no funnel needed.

The session friction worth recording here: a direct fetch of a Hacker News thread returned HTTP 429 mid-funnel, and the community stage proceeded on search snippets for that source with the citation-depth limit flagged in the deliverable.

## Premises

| Premise | As of | Revalidation check |
| :--- | :--- | :--- |
| Official vendor docs for the target tool are public and fetchable | 2026-07-15 | Fetch the vendor's primary docs page before stage 2; abort the funnel if paywalled or absent |
| Practitioner discussion venues (HN, engineering blogs, official power-user material) carry usable exposure signals for the tool | 2026-07-15 | Run one community search in stage 4; if fewer than two independent practitioner sources surface, downgrade the community stage to "official guidance only" and say so in the deliverable |
| web_search and web_fetch are available in the session | 2026-07-15 | Confirm tool availability at funnel start |

## Why it matters

Raw docs scans produce capability lists, and community scans produce anecdotes. Neither is decision-ready for an enterprise. The funnel solves that by forcing every finding through a risk scale and an exposure gate, so the deliverable is a single companion document a governance-minded reader can act on: which usages are in scope, how practitioners run them, and where the boundary sits.

## Inputs

| Artefact | Anchor | Content contract | On missing |
| :--- | :--- | :--- | :--- |
| Enterprise risk ceiling (the highest acceptable band for the deep-dive stages) | None on disk, supplied by the user in chat | A single band from the embedded risk scale, for example "medium" | Elicit from the user before stage 4. Do not assume |

No other on-disk inputs. The funnel consumes a topic string and produces its own corpus.

## The play

### Optimal workflow

1. Scope the assessment. Name the tool or integration, and obtain the enterprise risk ceiling (see Inputs).
2. Scan official vendor docs. Budget: three searches maximum, full-page fetch before any citation. Capture capabilities, prerequisites, the permission model, and the vendor's own safety guidance. The permission model is what the risk scale anchors on.
3. Build the risk-tiered use case table, covering the full spectrum from secure to not enterprise acceptable. Columns: use case, description, when to use, benefit, trade-offs, when not to use, risk level. Apply the embedded risk scale below and flag it as the author's mapping, not a vendor classification.
4. Run the community scan filtered to the approved risk band only. Budget: three searches maximum. Include a finding only if it passes the exposure heuristic below. Extend the table with two columns: community practice and exposure signal.
5. Produce worked examples (commands, prompts, config files) for the highest-frequency patterns only, not one per table row.
6. Fold stages 2 to 5 into a single companion document. Apply the humaniser pass and the organisation style rules. Land it in the sprint output folder. Date-stamp every fast-decaying claim (versions, vulnerability status) and add a re-verify note.

Embedded risk scale (F3):

| Band | Definition |
| :--- | :--- |
| Secure | No external data, no credential exposure, assets fully under the user's control |
| Low | User's own assets only, no untrusted content in the loop |
| Medium | Untrusted content or session inheritance, limited to reads or confirmed writes |
| High | Untrusted content combined with session inheritance, or unconfirmed writes |
| Not enterprise acceptable | Autonomous action on arbitrary external systems, or financial, legal, and production-write actions without per-action human confirmation |

Embedded exposure heuristic (F3): include a community finding if at least one of these holds: official vendor endorsement, a dedicated HN discussion, or recurrence across two or more independent practitioner guides. The heuristic is directional, not quantified, and the deliverable states that limit.

Budget accounting (F5): three searches per scanning stage. Sources surfaced during the official scan carry into the community corpus and do not count against the stage 4 budget. Failed fetches (rate limits, paywalls) do not earn replacement searches; proceed on snippets with the citation-depth limit flagged.

### Critical moves

- Official docs before community. The vendor's permission model is the anchor for the risk scale. Community claims tiered without it are guesswork.
- Risk ceiling applied before the community scan, not after. Filtering the corpus upfront halves the scan and keeps the deliverable scoped to what the organisation can adopt.
- Exposure heuristic as an inclusion gate, not a ranking. It exists to keep anecdotes out, not to sort what survives.
- One folded deliverable. Intermediate tables stay in chat, only the companion lands on disk.

### Pits to avoid

- Direct fetches of community threads can rate-limit. Do not block the funnel on one source, proceed on snippets and flag the depth limit.
- Search snippets invite citation without full fetch. The `reviewing-tech-claims` standard still applies to every claim that reaches the deliverable.
- Risk levels read as official classification unless explicitly flagged as the author's mapping.
- Vulnerability and version claims decay within weeks. An undated claim in the deliverable is a future error.
- The worked-examples stage balloons if you produce one example per table row. Frequency-of-use is the cut.

## When to use it

- The target is a discrete tool, integration, or capability with public vendor documentation.
- The organisation has, or can state, a risk appetite that maps to the embedded scale.
- The deliverable audience needs to act on the assessment, not just read about the tool.

## When not to use it

- Pure capability discovery with no adoption decision attached. A docs scan suffices.
- The tool is internal or undocumented publicly. The official-docs stage has nothing to anchor on.
- Deep security review is the actual need. This funnel surfaces disclosed issues and community hygiene, it does not replace a pentest or a formal risk assessment.
- The pattern is already covered: source discipline lives in `reviewing-tech-claims`, this play only adds the tiering and filtering stages on top.

## Expected outcome

One companion markdown document in `desktop-chat/outputs/<sprint-folder>/`, readable standalone. Checkable properties: it contains the full-spectrum risk table, community practices within the approved band each carrying an exposure signal, worked examples for the frequent patterns, security hygiene, and dated premises with a re-verify note. Every citation was either fully fetched or carries the snippet flag. The risk scale is flagged as the author's mapping.

Session instance: `desktop-chat/outputs/2607-claude-chrome-integration/claude-code-chrome-companion.md`, committed as `6f869ce`.

## Tradeoffs

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Coverage vs scope | Full risk spectrum everywhere | Approved band only | Full spectrum once, in the tiering table, for context. Community depth and examples only within the band. Cost: high-risk usages get no practitioner detail |
| Popularity measurement | Quantified signals (upvotes, stars) | Directional heuristic | Directional, with the limit stated in the deliverable. Cost: reproducibility, two authors could include different findings |
| Artefact count | One file per stage | Single folded companion | Single companion. Cost: intermediate tables are not persisted and cannot be diffed later |
| Speed vs source discipline | Full fetch always, block on failure | Snippets accepted freely | Full fetch as the standard, snippets on fetch failure with an explicit flag. Cost: citation depth on rate-limited sources |
| Freshness vs stability | Omit fast-decaying claims | Include them undated | Include, date-stamped, with a re-verify note in the deliverable. Cost: the document has a shelf life |

<!--
Version: 1.0
Last Updated: 2026-07-15
Status: Draft
Pairs with: deliverable desktop-chat/outputs/2607-claude-chrome-integration/claude-code-chrome-companion.md (no on-disk input artefacts)
-->
