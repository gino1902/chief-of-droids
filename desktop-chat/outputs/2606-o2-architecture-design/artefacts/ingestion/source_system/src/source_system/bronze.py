"""Bronze ingestion for one producer (ADR-008).

Auto Loader with managed file events lands each JSON record whole into a single
VARIANT column, plus provenance. Streaming table, processed once (ADR-007 dataset
types). Runtime DBR 18.1+ enables managed file events automatically.
"""

from pyspark import pipelines as dp

from source_system.reader import read_landing  # thin read, testable pure logic below


@dp.table(
    name="orders_bronze",
    comment="Raw JSON from the extractor as a single VARIANT column, append-only.",
)
def orders_bronze():
    landing_path = spark.conf.get("landing_path")  # noqa: F821  (spark is provided)
    return read_landing(spark, landing_path)  # noqa: F821
