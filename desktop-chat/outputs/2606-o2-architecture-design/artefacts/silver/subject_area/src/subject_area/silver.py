"""Silver conforming for one subject area (ADR-001, ADR-005, ADR-007).

Reads one or more bronze tables (possibly across producers) and produces the
conformed enterprise view. Streaming tables for row-level cleaning, declarative
CDC via APPLY CHANGES, expectations for data quality, materialized views for
enrichment. This is the home of conformed entity definitions.

🔲 To be defined: the actual conformed entity model, keys, and CDC targets for this
subject area. The below is a representative shape, not the final model.
"""

from pyspark import pipelines as dp

SOURCE = spark.conf.get("source_catalog")  # noqa: F821


# Row-level cleaning as a streaming table, with an expectation (warn at silver entry).
# CLUSTER BY AUTO for self-tuning layout (ADR-007).
@dp.table(name="orders_clean", cluster_by_auto=True)
@dp.expect("valid_order_id", "order_id IS NOT NULL")
def orders_clean():
    return (
        spark.readStream.table(f"{SOURCE}.source_system_bronze.orders_bronze")  # noqa: F821
        .selectExpr(
            "payload:order_id::string as order_id",
            "payload:customer_id::string as customer_id",
            "payload:amount::double as amount",
            "_ingested_at",
        )
    )


# Declarative CDC into the conformed customer table (SCD type 1), instead of MERGE.
# The change feed is read from a bronze customers table (illustrative source).
@dp.table(name="customers_cdc")
def customers_cdc():
    return spark.readStream.table(f"{SOURCE}.source_system_bronze.customers_bronze")  # noqa: F821


dp.create_streaming_table("customers")

dp.apply_changes(
    target="customers",
    source="customers_cdc",
    keys=["customer_id"],
    sequence_by="_ingested_at",
    stored_as_scd_type=1,
)


# Enrichment join as a materialized view (incremental refresh).
@dp.materialized_view(name="order_enriched")
def order_enriched():
    orders = spark.read.table("orders_clean")  # noqa: F821
    customers = spark.read.table("customers")  # noqa: F821
    return orders.join(customers, "customer_id", "left")
