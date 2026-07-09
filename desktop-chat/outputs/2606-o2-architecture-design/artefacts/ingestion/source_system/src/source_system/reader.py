"""Pure read logic, kept out of the pipeline decorator so it is unit-testable (ADR-007)."""

from pyspark.sql import DataFrame, SparkSession

from utils.shared_transforms import with_provenance


def read_landing(spark: SparkSession, landing_path: str) -> DataFrame:
    """Stream JSON from the landing path as one VARIANT column, with provenance (ADR-008)."""
    df = (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.useManagedFileEvents", "true")
        .option("singleVariantColumn", "payload")
        .load(landing_path)
    )
    return with_provenance(df)
