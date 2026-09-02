# Handover: audit the landing data

| Field | Value |
|:------|:------|
| Date | 2026-09-02 |
| For | A fresh session, scoped to auditing what is in the SharePoint landing zone |
| Audit target | `https://sqli468.sharepoint.com/sites/APP_FileShare/Shared Documents/SQLI-INTERNAL/app-reports/` |
| Not the target | `dev_sandbox.landing.sharepoint_replica`. See Access |
| Not for | Designing bronze. That is done and recorded. Do not redesign it here |

---

## Do this first

**Take the inventory of the SharePoint landing zone.** It is executable today, it is the deliverable,
and its value decays because the landing changes daily.

- Nothing else on this page can be answered without it.
- It is also the empirical half of TASK-097. Files older than any plausible read still sitting in the
  landing folders means the middleware is not deleting on read.
- If files really are being deleted, this inventory becomes the only surviving record of what was
  there, which is why it outranks everything else here.

---

## Preconditions, for a person, before the session starts

- **Decide the session type per question.** The SharePoint inventory needs a Claude Desktop session
  with the Microsoft 365 connector. That connector needs interactive `/mcp` auth and never reaches a
  `claude -p` subprocess, so `o2_data_sources.sh` cannot run it from the CLI despite being written
  for it. Anything touching Databricks needs a CLI session on the `o2_sandbox` profile. One session
  cannot do both.
- **Get the library's forensic permissions.** Recycle bin, version history and the Microsoft 365
  audit log are the difference between finding a loss and reporting an absence, and nobody has asked
  for any of them. Find out who administers `APP_FileShare` and request all three.
- **`READ VOLUME` on `dev_sandbox.landing.sharepoint_replica`** if the session will touch it, from
  eadeogun@sqli.com who owns it. Lower priority than it looks, see Access.

---

## What may already be gone

One thing, and it is contingent.

| Loss | Status |
|:-----|:-------|
| Closed months on five current-period feeds. Each landing carries only the month in progress, so once a month closes, the last landing of it is the only copy | Shape verified on the 2026-08-05 payloads. That they are rolling extracts rather than feeds that began that month is inferred from one day |

- The five are `cra_bilan_cra_report`, `cra_worklog`, `perso_collab_status_report`,
  `project_ca_collab_report` and `project_project_dataware_report`.
- This is only a loss if those landings are gone, which is what the inventory answers.
- TASK-097 is the multiplier. If the middleware deletes after reading, closed months disappear on a
  schedule rather than by accident.

## What has not happened, because nothing is ingesting yet

No ingestion pipeline exists. ADR-013 and ADR-014 are Draft, the only pipelines run on 2026-09-02
were probes and were swept, and building the pipeline is a stated non-goal below. Every item here
needs a reader that does not exist, so these are failures the build must avoid, not losses to find.

| Risk | Condition | Status |
|:-----|:----------|:-------|
| A file over 128 MiB becomes one VARIANT and lands in `corruptRecordColumn` rather than as rows. `whoz_profile_report` at 196.8 MB and `projects_report` at 143.1 MB | Only under `singleVariantColumn` with `multiLine=true`, already rejected, or under the `variant_explode` repair. Neither surviving route has any cap exposure | Documented, and the sources disagree on the figure |
| The checkpoint marks such a file processed, so a rerun does not reload it | Same condition | Inferred, not tested |
| A corrected file reusing its name is never reloaded at `allowOverwrites=false` | Any route | Documented |
| `whoz_user_report` lands as one object map, so 3,212 users never reach silver | If silver never explodes it | Verified from the payload |

No record in the corpus is near the cap. The largest is 410 KB. It is the file, not the record, that
would exceed it.

---

## Forensic routes, if something is missing

The audit cannot change the past. Its job is to make a loss findable.

- The library's recycle bin, and the second-stage recycle bin behind it.
- File version history on the library, which shows whether a name was ever rewritten.
- The Microsoft 365 audit log, for delete events on that path and who raised them.
- Who administers the library, since all three above are permissions the audit does not currently
  have.

---

## What the audit must answer

| # | Question | Session |
|:--|:---------|:--------|
| 1 | Full inventory: which feeds, how many files each, the date range, and gaps in the daily sequence. Includes whether `project_financial_report` is always empty or was empty only on 2026-08-05 | Desktop, M365 connector |
| 2 | How far back the history goes, per feed. This decides whether the five feeds' closed months are recoverable | Desktop, M365 connector |
| 3 | Whether filenames are ever reused. Two files, same name, different content or modification time, is the signature of a regenerated correction | Desktop, plus version history |
| 4 | Whether `whoz_user_report` still lands as an object map rather than an array | Desktop, M365 connector |
| 5 | TASK-097 confirmed with the middleware team, against what question 1 shows | A person, not a session |

Use the pattern in `../2607-o2-requirements/o2_data_sources.sh`: `read_resource` only, descend the
folder tree by returned URI, and **never read file contents**. That rule is what keeps an inventory
confidentiality-safe. The `DRIVE_ID` is in that script. The script's approach is right and its
harness is wrong, so lift the prompt rather than running the script.

---

## Deliverable

- A dated landing inventory in `2606-o2-architecture-design/`, one row per feed, carrying file count,
  date range, gaps and total size. Field paths and counts only, never file contents.
- A TASK number in `TASKS.md` for every question that does not close in the session, continuing from
  TASK-099.
- If the inventory shows files being removed, say so in the first paragraph rather than in a table.

---

## What is already settled. Do not redo it

- All 21 payloads are profiled, counts, sizes, shapes and personal data, in the design document's
  inventory.
- The grain question and the retirement question are both answered and recorded. See
  [2026-09-01-bronze-platform-tests.md](2026-09-01-bronze-platform-tests.md).
- The bronze design and its two records are written: ADR-013, ADR-014 and the design document.
- Four ADR claims are stale and already corrected. Do not re-verify VARIANT's status, the 128 MiB
  cap, the pipelines module name or `cleanSource`.

---

## Access

- **SharePoint is the audit target.** `dev_sandbox.landing.sharepoint_replica` is a volume someone
  else created as a mirror for sandbox testing. Its provenance, freshness and contents are unknown
  and nothing recorded says otherwise. An inventory of it answers nothing about what the middleware
  did to the real landing. Worth one line in the deliverable saying what is actually in it, and
  nothing more.
- CLI profile `o2_sandbox`, host `https://adb-7405605180591006.6.azuredatabricks.net`, from
  `pbi-databricks-sandbox/config/sandbox.yml`.
- Databricks statements run through `databricks api post /api/2.0/sql/statements` with `warehouse_id`
  `ca24aadb34697d64`, `statement` and `wait_timeout`. Set `wait_timeout` to `30s` or a cold start
  returns PENDING with a `statement_id` to poll.
- The workspace is on a private endpoint. Losing the network presents as a two-minute hang followed
  by an OAuth error that says nothing about the network. Do not read that as expired credentials.

---

## Constraints

- **16 of 21 feeds carry personal data.** Direct identifiers in `perso_workers` and
  `whoz_talent_report`, pseudonymous `uid` logins elsewhere. `2608-o2-data-sources/` is git-ignored
  for that reason and nothing from it is quoted verbatim in anything tracked. An inventory records
  names, counts and dates, never contents.
- If any part of this session touches Databricks, sweep what it creates. Throwaway schema, drop
  cascade, verify the catalog is back to its original schemas.
- Do not create a catalog. `pbi-databricks-sandbox` is explicit that one must not be invented in a
  shared metastore, and `dev_sandbox` already exists.

---

## Where things are

| What | Path |
|:-----|:-----|
| Bronze design | `2026-09-01-bronze-table-design.md` |
| The two records | `decisions/ADR-013-bronze-table-projection.md`, `decisions/ADR-014-bronze-write-block.md` |
| Test evidence, both rounds | `2026-09-01-bronze-platform-tests.md` |
| Feed configuration | `../2607-o2-requirements/o2-data-sources.md` |
| Inventory prompt to lift | `../2607-o2-requirements/o2_data_sources.sh` |
| Payload samples, 21 files | `../2608-o2-data-sources/`, git-ignored |
| Workspace runbook | `../../../../pbi-databricks-sandbox/docs/user-guide/RUNBOOK.md` |
| Open tasks | `TASKS.md`, notably TASK-097 |

---

## Deliberate non-goals

- Redesigning bronze. The grain and retirement questions are answered and recorded.
- Building the ingestion pipeline. It is blocked on the producer's answer, below.
- **One producer conversation, not two.** Newline-delimited JSON instead of pretty-printed arrays,
  and an array instead of an object map for `whoz_user_report`, are the same ask to the same team.
  Question 4 above establishes the current state, the ask itself is not this session's.
- The ADR-010 personal-data contradiction, which needs its five named decision-makers. TASK-099.
- Bronze retention, which needs this audit's answer on history depth first.
- The oversized-file platform test. It is a sandbox test, not a landing audit, and it has moved to
  `2026-09-01-bronze-platform-tests.md` as test 4.

Version history is git. This document carries no version field.
