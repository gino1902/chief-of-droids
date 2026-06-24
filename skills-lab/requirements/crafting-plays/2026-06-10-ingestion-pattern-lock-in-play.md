# Play: ingestion pattern lock-in against deployment context

> A play is a reusable recipe reconstructed from a session. This one captures how
> a pre-enumerated, option-agnostic ingestion design was collapsed into a single
> context-specific verdict.

## When to trigger

You hold a design doc that lays out several candidate patterns option-agnostically (each with abstract benefit and tradeoff), and a concrete deployment context then arrives that should select among them. The trigger is the arrival of the context, not the writing of the catalogue. The catalogue is the input, the verdict is the output.

Concrete examples:

- "The extractor is already running, everything downstream is greenfield, we will stand up a new Databricks workspace on the latest runtime. Pick the ingestion option." (The originating session.)
- "Here is our medallion-options doc and our actual team size and cloud posture. Which layer model do we commit to?"
- "We enumerated three CDC approaches in the design. Given we are on SQL Server with Unity Catalog already in place, which one?"

## Why it matters

It converts an option-agnostic catalogue into a defensible, context-specific verdict without re-deriving the catalogue. The deliverable is a per-option table re-scored against the actual context, a single recommendation, and the one variable that would change it. The problem it solves is convergence: a generic comparison never selects on its own, because a tradeoff is only a cost when the context makes it bite.

## The play

### Optimal workflow

1. Take the option-agnostic comparison as the input. If one does not exist, this is design-from-scratch, not lock-in, so stop and run the design workflow instead.
2. Verify the comparison's version-sensitive claims against official sources before trusting it as the decision base. Fetch first-party docs, confirm each load-bearing claim, fold any deltas back into the doc.
3. Capture the deployment context as hard constraints: what already exists, what is greenfield, the runtime and governance posture, and the shape of the upstream.
4. Re-score each option against those constraints, not in the abstract. Drop any option whose sole rationale is nullified by the context.
5. Look for composition among the survivors, not only competition. Two options that read as rivals often stack.
6. Name the single deciding variable that splits the residual choice, and state the verdict conditionally on it.
7. Make the verdict architect-legible: separate the option identifier from the design pattern, and attach the concrete cloud and platform components to each scenario.

### Critical moves

| Move | Why it is load-bearing |
| :--- | :--- |
| Verify before deciding | The verdict rests on the doc's claims. In the session, two load-bearing facts (DBR 18.1 file-events default, file events default-on for new locations) were only confirmable in the FAQ, not the pages the doc itself cited. Decide on an unverified doc and the verdict can rest on a stale claim |
| Re-score against context, not in the abstract | The generic tradeoffs do not select. The context nullified whole branches: with Unity Catalog present, the two options whose only purpose was escaping UC lost their reason to exist. Remove this move and all options survive, so nothing converges |
| Challenge the upstream assumption | Recognising the extractor as a puller (periodic, bursty arrivals) flipped the default away from always-on streaming toward event-triggered ephemeral compute. Remove this and you default to a continuous stream and overspend on idle compute |
| Name the one deciding variable | Reducing the residual choice to a single checkable question (freshness SLA against pull cadence) replaces an open debate with a falsifiable fork. Remove this and the verdict stays mushy |
| Score against a weighted criteria set, not a one-line call | Re-scoring A1b and A2 against the weighted criteria inverted the first-pass lean. The narrative favoured A2 on compute cost, but the weighted sum favoured A1b once operational ownership and security carried equal weight. The score, not the narrative, is the defensible artefact |

### Pits to avoid

- Trusting a doc's own "checked against current docs" line without re-fetching. The doc was accurate here, but the claims that decided the verdict were the ones easiest to get wrong.
- Treating options as mutually exclusive. The file-arrival trigger and managed file events compose: the trigger starts the job, the Auto Loader inside uses the managed file events mechanism. Either/or framing hides the real answer.
- Scoring tradeoffs abstractly. "Cache hop adds latency" only bites if latency matters here. "Needs UC" only bites if UC is absent. Let the context decide which generic tradeoff is real.
- Stopping at the first-pass narrative verdict. The qualitative lean and the weighted score disagreed. Run the weighted scoring before committing, since the heaviest single criterion can be outweighed by two others of equal weight.
- Following a workspace tool contract past the point it serves its intent. The contract named a fetch tool that truncates long pages, which would have undermined full-content verification. The better tool for the domain was used and the deviation flagged.

## When to use it

- A pre-enumerated, option-agnostic comparison already exists or can be produced cheaply.
- The deployment context is concrete enough to nullify branches: known runtime, known governance, a clear split between what exists and what is greenfield.
- The options carry version-sensitive claims that can be checked against official sources.

## When not to use it

- The option set is not yet defined. That is design-from-scratch, so use the design workflow.
- The context is still open or hypothetical, so nothing collapses.
- Only one option is viable from the outset, so there is no convergence to perform.
- The decision is value-driven or political rather than constraint-driven.

## Expected outcome

| Check | Pass condition |
| :--- | :--- |
| Re-scored table | Each option has a benefit and tradeoff stated against the actual context, plus a keep, drop, or conditional verdict |
| Single deciding variable | Any residual choice hangs on exactly one named, checkable variable |
| Traceable claims | Every version-sensitive claim under the verdict is traced to an official source |
| Transferable | A future reader facing a similar lock-in reaches a verdict without re-enumerating options or re-verifying from scratch |

## Tradeoffs

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Verification depth | Trust the doc's self-attestation | Re-fetch every cited source | Re-fetch all sources, since the verdict rests on them, accepting the token cost |
| Tool routing | Follow the workspace contract tool | Use the better tool for the domain | Better tool, with the contract deviation flagged once |
| Verdict shape | One unconditional pick | A full conditional fork | A primary verdict plus one deciding variable, because the context left exactly one variable open |
| Verdict basis | First-pass narrative lean | Weighted criteria score | Weighted score, which overrode the narrative when the two disagreed |
| Recipe reconstruction | Transcribe the session as it ran | Reconstruct the idealised path | Reconstruct, detours removed |
| Scoring frame | Keep the generic tradeoffs | Re-score against context | Re-score, since generic tradeoffs do not select |

## Worked example: the originating session

The concrete artefacts this play was reconstructed from, retained as a worked instance for traceability. The recipe above generalises these. This appendix extends the play format, which otherwise keeps concrete instances to the trigger examples.

Context: the extractor is already running, everything downstream is greenfield, an Azure subscription is in place, and a new Databricks workspace will be stood up on the latest functionality (DBR 18.1+, Unity Catalog, file events default-on).

### Revised option comparison

Shared components (every scenario): Azure ADLS Gen2 (HNS), Event Grid system topic, blob event subscription filtered on FlushWithClose. Databricks UC external location with per-subpath volume, bronze Delta table (VARIANT). Rows show only what each option adds.

| Option | Design pattern | Technical components added | Benefit in this context | Tradeoff in this context | Verdict |
|---|---|---|---|---|---|
| A1a | Classic file notification | Azure: per-stream Event Grid subscription and Azure Queue Storage (auto-provisioned), access connector MI or Entra SP with Contributor, Storage Queue Data Contributor, EventGrid EventSubscription Contributor. Databricks: Auto Loader stream (useNotifications=true), checkpoint | Sub-cache latency, direct queue read | Per-stream queue and creds, more IAM, 500-pipeline-per-account ceiling, all unused without a sub-second SLA | Drop. Reopen only for a future sub-second source |
| A1b | Managed file events | Azure: one managed Event Grid subscription and Storage Queue per external location, access connector MI. Databricks: file events service (managed), Auto Loader stream (useManagedFileEvents), checkpoint, Lakeflow job | UC cost is free here, fewest moving parts, managed cleanup, exactly-once. Tops the weighted score (146/170) on ownership, security and guarantee | Continuous run bills idle between pulls, cache hop adds latency (irrelevant without a sub-cache need) | Lead option. Run as scheduled availableNow for a periodic puller, which keeps cost low while holding the ownership and security lead. Run continuous only if sub-minute freshness is required |
| A2 | File-arrival trigger plus ephemeral job | Azure: managed file events infra (Event Grid subscription, Storage Queue), access connector MI. Databricks: Lakeflow Job with file-arrival trigger on the UC volume, ephemeral job cluster, Auto Loader inside (useManagedFileEvents, Trigger.availableNow), checkpoint | Compute strictly on arrival, lowest idle for sparse bursty pulls. Caps do not apply with file events on. Same exactly-once from the Auto Loader inside | About one minute trigger plus cold cluster start. Extra orchestration surface (trigger, job) costs it on ownership and security, so it loses the weighted total (123/170) | Conditional second. Wins only when arrivals are sparse enough that idle billing dominates and compute cost is re-weighted above operational simplicity. Composes with the A1b mechanism inside |
| B | Azure Function to run-now | Azure: Event Grid subscription to an Azure Function (Event Grid trigger), Function App on Consumption, no queue, SP for storage read, PAT or OAuth for the Jobs API. Databricks: Jobs API run-now, notebook job, job cluster, MERGE into Delta | Custom event routing, any language | Loses exactly-once and UC governance, you own and operate the Function and subscription. Its only rationale, no UC, does not apply | Drop. Nothing in this context selects it |

### Criteria scoring of the held options

Rating 1 to 5 on how well the option satisfies the criterion (5 best), against this context. Weighted score is the appendix weight times the rating. Both options clear the two preconditions: both require UC (present), and the security baseline is excluded from scoring.

| # | Criterion | Weight | A1b rating | A2 rating | A1b weighted | A2 weighted |
|---|---|---|---|---|---|---|
| 1 | Compute cost impact | 5 | 3 | 5 | 15 | 25 |
| 2 | Latency, event to bronze | 3 | 4 | 3 | 12 | 9 |
| 3 | Scale ceiling and limits | 3 | 4 | 4 | 12 | 12 |
| 4 | Operational ownership | 5 | 5 | 4 | 25 | 20 |
| 5 | Ingestion guarantee | 5 | 5 | 5 | 25 | 25 |
| 6 | Maturity and longevity | 3 | 4 | 4 | 12 | 12 |
| 7 | Source format coverage | 2 | 4 | 4 | 8 | 8 |
| 8 | Security surface and access governance | 5 | 5 | 4 | 25 | 20 |
| 9 | GDPR and data protection | 3 | 4 | 4 | 12 | 12 |
| | Total (max 170) | | | | 146 | 123 |

### Rating rationale, separating dimensions

| Criterion | Reasoning |
|---|---|
| 1 Compute cost | A2 runs compute only on arrival via the ephemeral job, structurally lowest idle for a periodic puller, so 5. A1b as a continuous stream bills idle between pulls, so 3. Run A1b as a scheduled availableNow batch instead and it rises to about 4, which narrows but does not erase A2's edge |
| 2 Latency | A1b continuous reaches bronze faster, cache hop but no per-run cluster start, so 4. A2 carries about one minute trigger best-effort plus a cold cluster start, so 3 |
| 4 Operational ownership | A1b is one managed stream, managed tuning and cleanup, fewest moving parts, so 5. A2 adds the trigger config, debounce settings and job orchestration around the same Auto Loader, so 4 |
| 8 Security surface | Both stay inside the governed plane on the access connector identity. A1b adds no orchestration layer, so 5. A2's job and trigger add a small marginal surface, so 4 |
| 5, 3, 6, 7, 9 | Tie. Exactly-once comes from the same Auto Loader engine in both. Both scale without hitting caps once file events are on. Both are GA mechanisms. Both run the same Auto Loader readers. Both inherit UC lineage and classification equally |

### Final verdict

Consolidated recommendation: A1b run as a scheduled availableNow batch is the strongest single configuration for a periodic pull extractor, taking most of A2's compute saving while keeping A1b's lead on operational ownership and security. Move to A2 only if the extractor's arrivals prove sparse and bursty enough that idle compute is the dominant cost, or to a continuous A1b stream only if a sub-minute freshness SLA appears. The pull cadence and freshness target remain the inputs that finalise the choice.

| Field | Value |
| :--- | :--- |
| Version | 1.1 |
| Last Updated | 2026-06-10 |
| Status | Draft |
| Pairs with | desktop-chat/outputs/2606-o2-architecture-design/2026-06-09-adls-bronze-ingestion-design.md |
