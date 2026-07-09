"""Gold for one business use case (ADR-001, ADR-007).

Builds only on silver conformed tables. Materialized views with business aggregates,
served to BI and ML. Never reads bronze directly.

🔲 To be defined: the actual dimensional model and measures for this use case. The
below is a representative aggregate, not the final model.
"""

from pyspark import pipelines as dp

SILVER = spark.conf.get("silver_catalog")  # noqa: F821


@dp.materialized_view(name="customer_spending")
def customer_spending():
    orders = spark.read.table(f"{SILVER}.subject_area_silver.order_enriched")  # noqa: F821
    return (
        orders.groupBy("customer_id")
        .agg({"amount": "sum"})
        .withColumnRenamed("sum(amount)", "total_spend")
    )
