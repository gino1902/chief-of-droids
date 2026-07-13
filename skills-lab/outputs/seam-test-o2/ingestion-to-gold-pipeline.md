# Ingestion to gold pipeline

This pipeline reads and writes data from an external `landing zone` into the `bronze` layer, then transforms it through `silver` to `gold`, so that the business is exposed trustworthy, high-quality enterprise data.

## In scope
- Covers reading and writing `landing zone` data into the `bronze` layer
- Handles the `bronze`-to-`silver` transformation, cleansing and conforming the data
- Handles the `silver`-to-`gold` transformation, building `enterprise entities`
- Responsible for gating publication to `gold` on `data-quality rules`

## Out of scope
- Populating the `landing zone`, owned by IT (the middleware that pushes data)
- Data governance and the catalog (`Unity Catalog`), owned by the Platform engineering track
- Exposing `gold` data through agentic workflows, owned by the Data exposition track

## Actors and consumers
- Upstream: the external `landing zone`, populated by the IT middleware
- Downstream: the Data exposition layer and its agentic workflows consume the `gold` layer
- Operator: the Platform engineering team runs the pipeline

## Requirements
- The pipeline shall write each `landing zone` dataset into the `bronze` layer, so that raw enterprise data is captured on the platform, when a dataset is delivered to the `landing zone` and within 30 minutes of delivery, for files matching the agreed `source contract`.  (R-01)
- The pipeline shall write the landed data in its exact form, so that the ingested data is preserved in its prior form, when the data is retained for audit.  (R-02)
- The pipeline shall cleanse and conform `bronze` data into the `silver` layer, so that the data is consistent and fit for building `enterprise entities`, when a record fails validation it is sent to `quarantine` rather than written to `silver`.  (R-03)
- The pipeline shall build `enterprise entities` in the `gold` layer from the `silver` layer, so that the business has trustworthy data to consume, when each entity has a unique `business key` and all `reference data` resolved.  (R-04)
- The pipeline shall publish to `gold` only data passing the `data-quality rules`, so that consumers can trust `gold` without reconciling it, when at least 99% of records pass the defined `data-quality rules`, holding the batch for review below that threshold.  (R-05)
- The pipeline shall re-run without producing duplicate `gold` records, so that reprocessing is safe and `gold` stays correct, when the same delivery is replayed.  (R-06)
