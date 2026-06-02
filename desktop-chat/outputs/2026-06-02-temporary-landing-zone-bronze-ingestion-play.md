# Quick-win bronze ingestion over a temporary un-governed landing zone

> A play for standing up lakehouse bronze ingestion when files land on a store
> the lakehouse does not govern, and that store is a stated-temporary bridge to
> a future event-driven state. Reconstructed from a single session.
>
> ⚠️ Unverified. Treat as provisional until validated against a second instance.

## When to trigger

An automated upstream writes files to a store the lakehouse does not control, and that landing is explicitly a temporary bridge toward a future event-driven design. You need bronze ingestion working now, without building infrastructure you will later delete. The recognition signal is the combination of three things: the landing store is outside the lakehouse governance perimeter, the upstream is already running, and someone has said the arrangement is temporary.

Concrete examples:

- A cron-driven extractor drops files on a SharePoint document library. Ingestion is manual today. The target is event-driven later. (the originating session)
- A partner SFTPs daily files to a shared folder while a proper API is pending.
- A legacy application emails reports that land in a watched mailbox folder awaiting a real integration.

## Why it matters

The trap is building migration-era scaffolding (bridges, custom event wiring, a hardened connector) for a landing zone that is already on death row. This play isolates the durable core (the file-detection-and-load logic plus the bronze table) from the throwaway parts (the landing store and its trigger substitute), so the eventual migration to governed storage swaps only the disposable pieces while the code that carries the value survives untouched.

## The play

### Optimal workflow

1. Interrogate the landing zone before anything else. Fixed constraint, or temporary bridge? If the upstream can write to governed storage instead, push for that now and skip the rest of the play.
2. Locate the event boundary. Native push triggers see only lakehouse-governed storage. An un-governed landing zone cannot fire them, so a real "file arrived" event does not exist yet.
3. Substitute a scheduled poll for the missing trigger. Run the loader on a schedule in fire-drain-stop mode, as an explicit stand-in that the future trigger will replace.
4. Pin the file format before designing the load. The format dominates the ingestion path. Designing before it is confirmed forces a redesign.
5. Choose the raw representation that fits the format and the fidelity obligation, not the most convenient default.
6. Set bronze as raw append-only history. Defer every resolution step (deduplication, last-write-wins, flattening) to silver.
7. Keep the loader source-agnostic, so the migration becomes a source-path swap rather than a rewrite.

### Critical moves

| Move | Collapse test |
| :--- | :--- |
| The landing-zone interrogation: why this store, and for how long | Skip it and you optimise the wrong target, hardening a path you will delete |
| Format-pinning before design | Skip it and you design the load twice |
| Source-agnostic durable core: loader and bronze independent of the landing surface | Skip it and the migration is a rewrite, not a swap |
| Bronze as raw append-only, resolution in silver | Skip it and full-refresh sources corrupt bronze with silent duplication |

### Pits to avoid

- Designing the load before the file format is confirmed.
- Conflating the upstream landing store with the lakehouse's own staging area. They are different surfaces with different governance.
- Assuming a native file-arrival trigger can watch the un-governed store.
- Building a bridge or connector for the temporary zone that you will later throw away.
- Mistaking file-level exactly-once (the loader processes each file once) for row-level deduplication (the data carries no duplicate keys). They are different problems.

## When to use it

- The landing zone is explicitly temporary, with a known target end-state.
- The file format is known, or can be pinned before the build starts.
- No byte-exact audit or replay obligation forces a heavier raw representation.
- A polling cadence in minutes to hours meets the latency requirement.

## When not to use it

- The landing zone is permanent. Invest in governed storage and a real trigger now rather than polling indefinitely.
- Sub-minute latency is required. A scheduled poll will not meet it.
- Byte-exact replay is mandated. The raw representation decision changes (see the paired JSON play, or dual-land raw bytes alongside the parsed form).
- The upstream can already write to governed storage with little effort. Skip the bridge and land there directly.

## Expected outcome

| Promise | How to check |
| :--- | :--- |
| The loader code and bronze schema survive the migration to governed storage unchanged | A diff of the loader before and after migration shows changes confined to the source path and the trigger configuration |
| No throwaway bridge infrastructure was built for the temporary zone | The component inventory contains no element whose only purpose is the temporary landing |
| Bronze holds a faithful append-only record, with current-state correctness provable downstream | Silver reproduces current state from bronze by deduplication on business key and load timestamp |

## Tradeoffs

Cadence and triggering

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Temporary trigger | Build event wiring for the temporary zone now | Poll on a schedule | Poll as a fire-drain-stop stand-in, swap for the native trigger at migration |
| Latency | Continuous always-on stream | Scheduled batch | Scheduled batch, lower cost, returns control to the scheduler each run |

Durability and scope

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Where to invest effort | Harden the temporary path | Harden only the durable core | Durable core only, the temporary path stays minimal |
| Landing surface | Accept the un-governed store permanently | Move to governed storage | Temporary now, governed later |

Bronze semantics

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Resolution point | Deduplicate at ingest | Resolve in silver | Silver. Bronze stays raw append-only |

## Version block

| Field | Value |
| :--- | :--- |
| Version | 1.0 |
| Last Updated | 2026-06-02 |
| Status | Draft |
| Pairs with | c4-sharepoint-databricks-bronze.pptx, 2026-06-02-json-sharpoint-to-bronze-ingestion-play.md |
